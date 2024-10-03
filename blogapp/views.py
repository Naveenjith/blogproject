from rest_framework.views import APIView
from django.contrib.auth.models import User
from rest_framework.response import Response
from rest_framework import status,generics,permissions
from .serializers import RegisterSerializer
from rest_framework.permissions import IsAuthenticated,AllowAny
from .serializers import ProfileSerializer,BlogPostSerializer
from .models import Profile,BlogPost
from rest_framework import status

class RegisterView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = RegisterSerializer
    permission_classes = [AllowAny]  

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

# Profile Update View
class ProfileUpdateView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        try:
            profile = Profile.objects.get(user=request.user)
            serializer = ProfileSerializer(profile)
            return Response(serializer.data)
        except Profile.DoesNotExist:
            return Response({'error': 'Profile not found'}, status=status.HTTP_404_NOT_FOUND)

    def put(self, request):
        try:
            profile = Profile.objects.get(user=request.user)
            user = request.user
            user_data = request.data.get('user', {})
            user.username = user_data.get('username', user.username)
            user.email = user_data.get('email', user.email)
            user.save()

            # Update the profile data
            serializer = ProfileSerializer(profile, data=request.data, partial=True)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except Profile.DoesNotExist:
            return Response({'error': 'Profile not found'}, status=status.HTTP_404_NOT_FOUND)

#blog data
class BlogPostListCreateView(generics.ListCreateAPIView):
    serializer_class = BlogPostSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return BlogPost.objects.filter(author=self.request.user)

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)


class BlogPostDetailView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = BlogPostSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return BlogPost.objects.filter(author=self.request.user)