from django.contrib import admin
from django.urls import path

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
]
