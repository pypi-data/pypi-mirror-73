from django.core.cache import caches
from django.http import Http404, HttpResponse
from django_filters.rest_framework import DjangoFilterBackend
from office365.runtime.client_request_exception import ClientRequestException
from office365.sharepoint.files.file import File
from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.exceptions import ErrorDetail, PermissionDenied
from rest_framework.filters import OrderingFilter, SearchFilter

from unicef_sharepoint import config
from unicef_sharepoint.client import SharePointClient, SharePointClientException
from unicef_sharepoint.filters import SharePointLibraryFilter
from unicef_sharepoint.models import SharePointLibrary, SharePointSite, SharePointTenant
from unicef_sharepoint.serializers import (
    SharePointFileSerializer,
    SharePointItemSerializer,
    SharePointLibrarySerializer,
    SharePointSiteSerializer,
    SharePointTenantSerializer,
    SimpleSharePointItemSerializer,
)
from unicef_sharepoint.utils import get_cache_key

cache = caches['default']


class AbstractSharePointViewSet(viewsets.ReadOnlyModelViewSet):
    serializer_class = None
    filter_backends = (SearchFilter, DjangoFilterBackend, OrderingFilter)

    def get_serializer_context(self):
        ctx = super().get_serializer_context()
        ctx.update({
            'tenant': self.tenant,
            'site': self.site,
            'folder': self.folder
        })
        return ctx

    def handle_exception(self, exc):
        response = super().handle_exception(exc)
        if isinstance(exc, Http404):
            response.data['detail'] = ErrorDetail('No document found using selected filters', 'not_found')
        return response

    def get_cache_key(self, **kwargs):
        key = get_cache_key([self.tenant, self.site, self.folder], **kwargs)
        return key


class UrlBasedSharePointViewSet(AbstractSharePointViewSet):

    def get_library(self):
        return SharePointLibrary.objects.get(
            site__tenant__url__contains=self.tenant, name=self.folder, site__name=self.site)

    def is_public(self):
        return self.get_library().public

    @property
    def client(self):
        key = self.get_cache_key(**{'client': 'client'})
        client = cache.get(key)
        if client is None:
            dl = self.get_library()
            dl_info = {
                'url': dl.site.site_url(),
                'relative_url': dl.site.relative_url(),
                'folder': dl.name
            }
            if dl.site.tenant.username:
                dl_info['username'] = dl.site.tenant.username
                dl_info['password'] = dl.site.tenant.password
            try:
                client = SharePointClient(**dl_info)
                cache.set(key, client)
            except SharePointClientException:
                raise PermissionDenied

        return client

    @property
    def tenant(self):
        return self.kwargs.get('tenant')

    @property
    def site(self):
        return self.kwargs.get('site')

    @property
    def folder(self):
        return self.kwargs.get('folder')


class SettingsBasedSharePointViewSet(AbstractSharePointViewSet):

    def is_public(self):
        return SharePointLibrary.objects.filter(name=self.folder, public=True)

    @property
    def tenant(self):
        return config.SHAREPOINT_TENANT

    @property
    def site(self):
        return config.SHAREPOINT_SITE

    @property
    def folder(self):
        return self.kwargs.get('folder')

    @property
    def site_type(self):
        return config.SHAREPOINT_SITE_TYPE

    @property
    def client(self):
        key = self.get_cache_key(**{'client': 'client'})
        client = cache.get(key)
        if client is None:
            dl_info = {
                'url': f'{self.tenant}/{self.site_type}/{self.site}',
                'relative_url': f'{self.site_type}/{self.site}',
                'folder': self.folder
            }
            try:
                client = SharePointClient(**dl_info)
                cache.set(key, client)
            except SharePointClientException:
                raise PermissionDenied

        return client


class CamlQuerySetMixin:

    def get_queryset(self):
        kwargs = self.request.query_params.dict()
        cache_dict = kwargs.copy()
        cache_dict['caml'] = 'true'
        try:
            key = self.get_cache_key(**cache_dict)
            response = cache.get(key)
            if response is None:
                response = self.client.read_caml_items(filters=kwargs)
                cache.set(key, response)
            return response
        except ClientRequestException:
            raise Http404


class RestQuerySetMixin:

    def get_queryset(self):
        kwargs = self.request.query_params.dict()
        try:
            key = self.get_cache_key(**kwargs)
            response = cache.get(key)
            if response is None:
                response = self.client.read_items(filters=kwargs)
                cache.set(key, response)
            return response
        except ClientRequestException:
            raise Http404


class SharePointRestViewSet(RestQuerySetMixin, SettingsBasedSharePointViewSet):
    serializer_class = SimpleSharePointItemSerializer


class SharePointCamlViewSet(CamlQuerySetMixin, SettingsBasedSharePointViewSet):
    serializer_class = SimpleSharePointItemSerializer


class ItemSharePointViewSet(RestQuerySetMixin, UrlBasedSharePointViewSet):
    serializer_class = SharePointItemSerializer


class ItemSharePointCamlViewSet(CamlQuerySetMixin, UrlBasedSharePointViewSet):
    serializer_class = SharePointItemSerializer


class BaseFileSharePointViewSet(SettingsBasedSharePointViewSet):
    serializer_class = SharePointFileSerializer
    lookup_field = 'filename'
    lookup_value_regex = '[^/]+'

    def get_object(self):
        filename = self.kwargs.get('filename', None)
        try:
            doc_file = self.client.read_file(f'{filename}')
        except ClientRequestException:
            raise Http404
        return doc_file

    def get_queryset(self):
        kwargs = self.request.query_params.dict()
        try:
            return self.client.read_files(filters=kwargs)
        except ClientRequestException:
            raise Http404

    @action(detail=True, methods=['get'])
    def download(self, request, *args, **kwargs):
        sh_file = self.get_object()
        relative_url = sh_file.properties['ServerRelativeUrl']
        response = File.open_binary(self.client.context, relative_url)

        django_response = HttpResponse(
            content=response.content,
            status=response.status_code,
            content_type=response.headers['Content-Type'],
        )
        django_response['Content-Disposition'] = 'attachment; filename=%s' % sh_file.properties['Name']
        return django_response


class FileSharePointViewSet(BaseFileSharePointViewSet, UrlBasedSharePointViewSet):
    pass


class SharePointFileViewSet(BaseFileSharePointViewSet, SettingsBasedSharePointViewSet):
    pass


class SharePointTenantViewSet(viewsets.ReadOnlyModelViewSet):
    filter_backends = (SearchFilter, DjangoFilterBackend, OrderingFilter)
    queryset = SharePointTenant.objects.all()
    serializer_class = SharePointTenantSerializer
    search_fields = ('url', )


class SharePointSiteViewSet(viewsets.ReadOnlyModelViewSet):
    filter_backends = (SearchFilter, DjangoFilterBackend, OrderingFilter)
    queryset = SharePointSite.objects.all()
    serializer_class = SharePointSiteSerializer
    search_fields = ('name', )


class SharePointLibraryViewSet(viewsets.ReadOnlyModelViewSet):
    filter_backends = (SearchFilter, DjangoFilterBackend, OrderingFilter)
    queryset = SharePointLibrary.objects.all()
    serializer_class = SharePointLibrarySerializer
    search_fields = ('name', )
    filterset_class = SharePointLibraryFilter
