from django.shortcuts import render,get_object_or_404
from django.http import HttpResponse
from .models import BookInstance, Book, Author
from django.views import generic
from django.contrib.auth.mixins import LoginRequiredMixin,PermissionRequiredMixin

#this is not used in project ...its only test
def main_index(request):
    return HttpResponse('<p>Welcome to E-Pustakalaya developed by <em>Pysantosh</em>!</p>')

def index(request):
    my_books = Book.objects.all().count()
    my_instances = BookInstance.objects.all().count()

    # Available books (status = 'a')
    my_instances_available = BookInstance.objects.filter(status__exact='a').count()


    my_authors = Author.objects.count()

    num_visits = request.session.get('num_visits', 0)
    request.session['num_visits'] = num_visits + 1

    my_queryset ={
        'my_books':my_books,
        'my_instances':my_instances,
        'my_instances_available':my_instances_available,
        'my_authors':my_authors,
        'num_visits':num_visits,
    }

    return render(request, 'index.html', context=my_queryset)


class BookListView(generic.ListView):
    model = Book
    context_object_name = 'book_list'
    paginate_by = 6 #more than 2 records the view will start paginating
    queryset = Book.objects.all() #.filter(title__icontains='two')[:5] # Get 5 books containing the title two
    template_name = 'books/book_list.html'


# def book_detail(request, isbn):
#     book = get_object_or_404(Book, isbn=isbn,)
#     return render(request, 'books/book_detail.html', context={'book':book})

class BookDetailView(generic.DetailView):

    def get_object(self):
        return Book.objects.get(isbn=self.kwargs.get("isbn"))
    context_object_name = 'book'
    model = Book

    template_name = 'books/book_detail.html'

class AuthorListView(generic.ListView):
    model = Author
    context_object_name = 'author_list'
    queryset = Author.objects.all()
    template_name = 'authors/author_list.html'

class AuthorDetailView(generic.DetailView):
    context_object_name = 'author'
    model = Author
    template_name = 'authors/author_detail.html'


class LoanedBooksByUserListView(LoginRequiredMixin, generic.ListView):
    """Generic class-based view listing books on loan to current user."""
    model = BookInstance
    template_name = 'book_borrowed_user.html'
    paginate_by = 10

    def get_queryset(self):
        return BookInstance.objects.filter(borrower=self.request.user).filter(status__exact='o').order_by('due_back')


from django.contrib.auth.mixins import PermissionRequiredMixin


class LoanedBooksAllListView(PermissionRequiredMixin, generic.ListView):
    """
    Generic class-based view listing all books on loan. Only visible to users with can_mark_returned permission.
    """
    model = BookInstance
    permission_required = 'category.can_mark_returned'
    template_name = 'book_borrowed_all.html'
    paginate_by = 10

    def get_queryset(self):
        return BookInstance.objects.filter(status__exact='o').order_by('due_back')

import datetime

from django.shortcuts import get_object_or_404
from django.http import HttpResponseRedirect
from django.urls import reverse
from .forms import RenewBookForm
from django.contrib.auth.decorators import permission_required



@permission_required('category.can_mark_returned')
def renew_book_librarian(request, pk):
    book_instance = get_object_or_404(BookInstance, pk=pk)

    # If this is a POST request then process the Form data
    if request.method == 'POST':

        # Create a form instance and populate it with data from the request (binding):
        book_renewal_form = RenewBookForm(request.POST)

        # Check if the form is valid:
        if book_renewal_form.is_valid():
            # process the data in form.cleaned_data as required (here we just write it to the model due_back field)
            book_instance.due_back = book_renewal_form.cleaned_data['renewal_date']
            book_instance.save()

            # redirect to a new URL:
            return HttpResponseRedirect(reverse('all_borrowed') )

    # If this is a GET (or any other method) create the default form.
    else:
        proposed_renewal_date = datetime.date.today() + datetime.timedelta(weeks=3)
        book_renewal_form = RenewBookForm(initial={'renewal_date': proposed_renewal_date})

    context = {
        'form': book_renewal_form,
        'book_instance': book_instance,
    }

    return render(request, 'book_renew_librarian.html', context)



from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy

from .models import Author

class AuthorCreate(PermissionRequiredMixin, generic.CreateView):
    model = Author
    permission_required = 'category.can_mark_returned'
    fields = '__all__'
    template_name = 'authors/author_form.html'
    success_url = reverse_lazy('index')

class AuthorUpdate(PermissionRequiredMixin, generic.UpdateView):
    context_object_name = 'author'
    model = Author
    permission_required = 'category.can_mark_returned'
    fields = '__all__'
    template_name = 'authors/author_edit.html'

class AuthorDelete(PermissionRequiredMixin, generic.DeleteView):
    model = Author
    permission_required = 'category.can_mark_returned'
    success_url = reverse_lazy('authors')
    template_name = 'authors/author_confirm_delete.html'


from django.urls import reverse_lazy

from .models import Book

class BookCreate(PermissionRequiredMixin, generic.CreateView):
    model = Book
    permission_required = 'category.can_mark_returned'
    fields = '__all__'
    template_name = 'books/book_form.html'
    success_url = reverse_lazy('index')

class BookUpdate(PermissionRequiredMixin, generic.UpdateView):
    model = Book
    permission_required = 'category.can_mark_returned'
    fields = '__all__'
    template_name = 'books/book_edit.html'
    def get_object(self):
        return Book.objects.get(isbn=self.kwargs.get("isbn"))


    
    
class BookDelete(PermissionRequiredMixin, generic.DeleteView):
    model = Book
    permission_required = 'category.can_mark_returned'
    success_url = reverse_lazy('books')
    template_name = 'books/book_confirm_delete.html'
    def get_object(self):
        return Book.objects.get(isbn=self.kwargs.get("isbn"))