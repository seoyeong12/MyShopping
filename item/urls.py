from django.urls import path
from . import views

urlpatterns = [
    path('', views.ItemList.as_view()),
    path('<int:pk>/',views.ItemDetail.as_view()),
    path('create_item/', views.ItemCreate.as_view()),
    path('update_item/<int:pk>/', views.ItemUpdate.as_view()),
    path('seller/<str:slug>/',views.seller_page), # IP주소/item/seller/slug/
    path('category/<str:slug>/', views.category_page),
    path('tag/<str:slug>/', views.tag_page),  # IP주소/item/tag/slug/

]