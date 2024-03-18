from blog.Views.posts_views import PostsViewSet
from rest_framework.routers import DefaultRouter
from blog.Views.comments_views import CommentsViewSet

router = DefaultRouter()
router.register("posts", PostsViewSet, basename="posts-api")
router.register("comments", CommentsViewSet, basename="comments-api")
urlpatterns = router.urls
