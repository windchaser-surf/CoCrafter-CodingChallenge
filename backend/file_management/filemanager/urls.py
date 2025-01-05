from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import FolderViewSet, DocumentAPIView

router = DefaultRouter()
router.register(r'folders', FolderViewSet)

urlpatterns = [
    path('api/v2/', include(router.urls)),
    path('api/v2/documents/', DocumentAPIView.as_view(), name='documents'),
    path('api/v2/documents/<int:id>/', DocumentAPIView.as_view(), name='document-detail'),
]