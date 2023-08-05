from rest_framework.routers import DefaultRouter

from orionframework.metadata.views import *

router = DefaultRouter()

# model
router.register(r'model', MetadataModelViewSet, basename='metadata-model')

urlpatterns = router.urls
