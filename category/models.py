from django.db import models
from django.urls import reverse
import uuid

class Author(models.Model):
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    profile_pic = models.ImageField(upload_to='images/authors/', default='image')
    date_of_birth = models.DateTimeField(null=True, blank=True)

    class Meta:
        ordering = ['first_name', 'last_name']

    def get_absolute_url(self):
        """Returns the url to access a particular author instance."""
        return reverse('author_detail', args=[str(self.id)])
    def date_of_birth_preety(self):
        return self.date_of_birth.strftime('%b %e, %Y')

    def __str__(self):
        return f'{self.last_name}, {self.first_name}'

#Genre Model

class Genre(models.Model):
    name = models.CharField(max_length=100, help_text='Enter the Genre of book eg.(Science Fiction)')


    def __str__(self):
        return self.name



#Book Model


class Book(models.Model):
    title = models.CharField(max_length=200)
    author = models.ForeignKey('Author',
                               on_delete=models.SET_NULL, null=True)
    image = models.ImageField(upload_to='images/books/', default='image')
    summery = models.TextField(max_length=1000, help_text='description of book')
    isbn = models.CharField('ISBN',
                            max_length=13,
                            help_text='enter the 13 numbers ISBN')
    genre = models.ManyToManyField(Genre, help_text='Enter the Genre of the book')
    language = models.CharField(max_length=200, default='English')



    def __str__(self):
        return self.title

    def get_absolute_url(self):
        """Returns the url to access a detail record for this book."""
        return reverse('book_detail', args=[str(self.isbn)])

    def display_genre(self):
        """Create a string for the Genre. This is required to display genre in Admin."""
        return ', '.join(genre.name for genre in self.genre.all()[:3])

    display_genre.short_description = 'Genre'

    def get_author_url(self):
         """Returns the url to access a particular author instance."""
         return reverse('author_detail', args=[str(self.id)])



#BookInstance model

class BookInstance(models.Model):
    id = models.UUIDField(primary_key=True,
                          default=uuid.uuid4,
                          help_text='Unique id for book')
    book = models.ForeignKey('Book', on_delete=models.SET_NULL, null=True)
    imprint = models.CharField(max_length=200)
    due_back = models.DateField(null=True, blank=True)


    LOAN_STATUS = (
        ('m', 'Maintance'),
        ('o', 'On Loan'),
        ('a', 'Availabe'),
        ('r', 'Reverse'),
    )
    status = models.CharField(
        max_length=1,
        choices=LOAN_STATUS,
        blank=True,
        default='m',
        help_text='Book Availabality'

    )


    class Meta:
        ordering = ['-due_back']

    def __str__(self):
        """String for representing the Model object."""
        return f'{self.id} ({self.book.title})'