from blog.Views.posts_views import PostsViewSet
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register("all_post", PostsViewSet, basename="post-viewsets")
urlpatterns = router.urls
