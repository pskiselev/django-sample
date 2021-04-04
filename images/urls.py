from rest_framework.routers import DefaultRouter

from images.views import ImagesView

router = DefaultRouter()
router.register(r'images', ImagesView, basename='images')
urlpatterns = router.urls
