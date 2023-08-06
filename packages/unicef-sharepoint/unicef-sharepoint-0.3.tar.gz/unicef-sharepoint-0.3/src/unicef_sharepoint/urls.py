from rest_framework import routers

from unicef_sharepoint.views import (
    FileSharePointViewSet,
    ItemSharePointCamlViewSet,
    ItemSharePointViewSet,
    SharePointCamlViewSet,
    SharePointFileViewSet,
    SharePointLibraryViewSet,
    SharePointRestViewSet,
    SharePointSiteViewSet,
    SharePointTenantViewSet,
)

app_name = 'unicef_sharepoint'

router = routers.DefaultRouter()

router.register(r'tenants', SharePointTenantViewSet, basename='sharepoint-tenant')
router.register(r'sites', SharePointSiteViewSet, basename='sharepoint-site')
router.register(r'libraries', SharePointLibraryViewSet, basename='sharepoint-library')
router.register(r'sharepoint/(?P<tenant>[\w\-]+)/(?P<site>[\w\-]+)/(?P<folder>[\w\W]+)/files',
                FileSharePointViewSet, basename='sharepoint-files')
router.register(r'sharepoint/(?P<tenant>[\w\-]+)/(?P<site>[\w\-]+)/(?P<folder>[\w\W]+)/rest',
                ItemSharePointViewSet, basename='sharepoint-rest')
router.register(r'sharepoint/(?P<tenant>[\w\-]+)/(?P<site>[\w\-]+)/(?P<folder>[\w\W]+)/caml',
                ItemSharePointCamlViewSet, basename='sharepoint-caml')
router.register(r'sharepoint/(?P<folder>[\w\W]+)/rest', SharePointRestViewSet, basename='simple-sharepoint-rest')
router.register(r'sharepoint/(?P<folder>[\w\W]+)/caml', SharePointCamlViewSet, basename='simple-sharepoint-caml')
router.register(r'sharepoint/(?P<folder>[\w\W]+)/files', SharePointFileViewSet, basename='simple-sharepoint-files')

urlpatterns = router.urls
