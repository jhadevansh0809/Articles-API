from django.urls import path,include
from . import views
from rest_framework_simplejwt.views import (
    TokenRefreshView,
)

from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register('', views.ArticleViewSet, basename='articles')

urlpatterns = [
     path('articles/',include(router.urls)),
     path('register/',views.getUser,name="users"),
     path('token/', views.MyTokenObtainPairView.as_view(), name='token_obtain_pair'),
     path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
     path('<str:username>/',views.getUserArticles,name='userarticles'),
]
