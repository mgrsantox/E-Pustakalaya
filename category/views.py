from django.shortcuts import render
from django.http import HttpResponse
from .models import BookInstance, Book, Author
from django.views import generic

#this is not used in project ...its only test
def main_index(request):
    return HttpResponse('<p>Welcome to E-Pustakalaya developed by <em>Pysantosh</em>!</p>')

def index(request):
    my_books = Book.objects.all().count()
    my_instances = BookInstance.objects.all().count()

    # Available books (status = 'a')
    my_instances_available = BookInstance.objects.filter(status__exact='a').count()


    my_authors = Author.objects.count()

    my_queryset ={
        'my_books':my_books,
        'my_instances':my_instances,
        'my_instances_available':my_instances_available,
        'my_authors':my_authors,
    }

    return render(request, 'index.html', context=my_queryset)


class BookListView(generic.ListView):
    model = Book
    context_object_name = 'book_list'
    queryset = Book.objects.all() #.filter(title__icontains='two')[:5] # Get 5 books containing the title two
    template_name = 'books/book_list.html'