from django.urls import path
from . import views

urlpatterns=[
    path('', views.index, name='category_index'),
    # path('books/<int:pk>/', views.BookDetailView.as_view(), name='book_detail'),
]

# Books UrlConfig
urlpatterns +=[
    path('books/', views.BookListView.as_view(), name='books'),
    path('books/<int:isbn>/', views.book_detail, name='book_detail'),
    path('books/create/', views.BookCreate.as_view(), name='book_create'),
    path('books/<int:isbn>/update/', views.BookUpdate.as_view(), name='book_update'),
    path('books/<int:isbn>/delete/', views.BookDelete.as_view(), name='book_delete'),
]

# Authors URLconfig
urlpatterns += [
    path('authors/', views.AuthorListView.as_view(), name='authors'),
    path('authors/<int:pk>/', views.AuthorDetailView.as_view(), name='author_detail'),
    path('authors/create/', views.AuthorCreate.as_view(), name='author_create'),
    path('authors/<int:pk>/update/', views.AuthorUpdate.as_view(), name='author_update'),
    path('authors/<int:pk>/delete/', views.AuthorDelete.as_view(), name='author_delete'),
]

# Super user URLConig
urlpatterns += [
    path('mybooks/', views.LoanedBooksByUserListView.as_view(), name='my_borrowed'),
    path(r'borrowed/', views.LoanedBooksAllListView.as_view(), name='all_borrowed'),
    path('books/<uuid:pk>/renew/', views.renew_book_librarian, name='renew_book_librarian'),

]