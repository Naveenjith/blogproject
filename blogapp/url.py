from django.urls import path
from .views import RegisterView,ProfileUpdateView
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from django.conf import settings
from django.conf.urls.static import static
from .views import BlogPostListCreateView, BlogPostDetailView

urlpatterns = [
    path('api/register', RegisterView.as_view(), name='register'),
    path('api/login/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('api/profile/', ProfileUpdateView.as_view(), name='profile_update'),
    path('api/posts/', BlogPostListCreateView.as_view(), name='blog_post_list_create'),
    path('api/posts/<int:pk>/', BlogPostDetailView.as_view(), name='blog_post_detail'),
]


urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)