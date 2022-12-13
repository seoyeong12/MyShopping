from django.urls import path
from . import views
app_name = 'item'
urlpatterns = [
    path('', views.ItemList.as_view()),
    path('<int:pk>/',views.ItemDetail.as_view()),
    path('<int:pk>/new_comment/', views.new_comment),
    path('update_comment/<int:pk>/', views.CommentUpdate.as_view()),
    path('comment/<int:pk>/re_comment/',views.re_comment),
    path('delete_comment/<int:pk>/', views.delete_comment),
    path('create_item/', views.ItemCreate.as_view()),
    path('update_item/<int:pk>/', views.ItemUpdate.as_view()),
    path('seller/<str:slug>/',views.seller_page), # IP주소/item/seller/slug/
    path('category/<str:slug>/', views.category_page),
    path('tag/<str:slug>/', views.tag_page),  # IP주소/item/tag/slug/
    path('search/<str:q>/',views.ItemSearch.as_view()),
    path('<int:pk>/likes/', views.likes, name='likes'),
]