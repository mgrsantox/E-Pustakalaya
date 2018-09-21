from django.urls import path
from . import views

urlpatterns=[
    path('', views.index, name='category_index'),
    path('books/', views.BookListView.as_view(), name='books'),
    path('books/<int:pk>/', views.BookDetailView.as_view(), name='book_detail'),
]