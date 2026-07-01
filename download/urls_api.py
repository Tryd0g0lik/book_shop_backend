from rest_framework import routers

from download.views.view_load_file import CatalogViewSet

router = routers.DefaultRouter()
router.register("load/file", CatalogViewSet)
urlpatterns = router.urls
