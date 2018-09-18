from django.db import models
from django.urls import reverse
import uuid

class Author(models.Model):
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    date_of_birth = models.DateTimeField(null=True, blank=True)

    class Meta:
        ordering = ['first_name', 'last_name']

    def get_absolute_url(self):
        """Returns the url to access a particular author instance."""
        return reverse('author-detail', args=[str(self.id)])

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
    summery = models.TextField(max_length=1000, help_text='description of book')
    isbn = models.CharField('ISBN',
                            max_length=13,
                            help_text='enter the 13 numbers ISBN')
    genre = models.ManyToManyField(Genre, help_text='Enter the Genre of the book')



    def __str__(self):
        return self.title

    def get_absolute_url(self):
        """Returns the url to access a detail record for this book."""
        return reverse('book-detail', args=[str(self.id)])




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