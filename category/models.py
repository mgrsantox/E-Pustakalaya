from django.db import models
from django.urls import reverse
import uuid
from datetime import date
from django.contrib.auth.models import User
from django.db.models.signals import post_delete
from django.dispatch import receiver

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

    permissions = (("can_mark_returned", "Allowed"),)

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
    borrower = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)

    LOAN_STATUS = (
        ('m', 'Maintance'),
        ('o', 'On Loan'),
        ('a', 'Availabe'),
        ('r', 'Reserved'),
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
        permissions = (("can_mark_returned", "Set book as returned"),)

    @property
    def is_overdue(self):
        if self.due_back and date.today() > self.due_back:
            return True
        return False

    def __str__(self):
        """String for representing the Model object."""
        return f'{self.id} ({self.book.title})'
'''
@receiver(post_delete, sender=Author)
def submission_delete(sender, instance, **kwargs):
    instance.profile_pic.delete(False)
    '''

def save(self, *args, **kwargs):
    try:
        this = Author.objects.get(id=self.id)
        if this.profile_pic != self.profile_pic:
            this.profile_pic.delete()
    except: pass
    super(Author, self).save(*args, **kwargs)