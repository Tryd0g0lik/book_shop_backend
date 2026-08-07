from rest_framework import routers

from download.views.view_load_file import DownloadOfCatalogViewSet

router = routers.DefaultRouter()
router.register("load/file", DownloadOfCatalogViewSet)
urlpatterns = router.urls
