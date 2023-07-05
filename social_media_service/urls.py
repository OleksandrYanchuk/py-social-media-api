from django.urls import include, path
from rest_framework import routers
from .views import ProfileViewSet, PostViewSet

app_name = "social_media_service"

router = routers.DefaultRouter()
router.register(r"profiles", ProfileViewSet)
router.register(r"posts", PostViewSet)

urlpatterns = [
    path("", include(router.urls)),
]
