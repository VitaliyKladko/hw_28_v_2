from django.conf.urls.static import static
from django.urls import path
from hw_28_v_2 import settings

import ads.views


urlpatterns = [
    path('cat/', ads.views.CategoryListView.as_view()),
    path('cat/<int:pk>/', ads.views.CategoryDetailView.as_view()),
    path('cat/<int:pk>/delete/', ads.views.CategoryDeleteView.as_view()),
    path('cat/<int:pk>/update/', ads.views.CategoryUpdateView.as_view()),
    path('cat/create/', ads.views.CategoryCreateView.as_view()),
    path('ad/', ads.views.AdsListView.as_view()),
    path('ad/<int:pk>/', ads.views.AdsDetailView.as_view()),
    path('ad/<int:pk>/update/', ads.views.AdsUpdateView.as_view()),
    path('ad/<int:pk>/delete/', ads.views.AdsDeleteView.as_view()),
    path('ad/create/', ads.views.AdsCreateView.as_view()),
    path('ad/<int:pk>/upload_image/', ads.views.AdsImageView.as_view()),
    path('user/', ads.views.UserListView.as_view()),
    path('user/<int:pk>/', ads.views.UserDetailView.as_view()),
    path('user/<int:pk>/delete/', ads.views.UserDeleteView.as_view()),
    path('user/<int:pk>/update/', ads.views.UserUpdateView.as_view()),
    path('user/create/', ads.views.UserCreateView.as_view()),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)