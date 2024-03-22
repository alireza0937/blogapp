from rest_framework.routers import DefaultRouter
from . import views

router = DefaultRouter()
router.register("", views.RegisterationViewSet, basename="register-api")
urlpatterns = router.urls
