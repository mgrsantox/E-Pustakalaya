from django.contrib import admin
from .models import BookInstance, Book, Genre, Author


@admin.register(Author)
class AuthorAdmin(admin.ModelAdmin):
    list_display = ('first_name', 'last_name', 'date_of_birth')
    fields = ('first_name', 'last_name')
@admin.register(Book)
class BookAdmin(admin.ModelAdmin):
    list_display = ('title', 'author')
@admin.register(Genre)
class GenreAdmin(admin.ModelAdmin):
    pass
@admin.register(BookInstance)
class BookInstance(admin.ModelAdmin):
    list_filter = ('status','due_back')
    fieldsets = (
        (None, {
            'fields':('book', 'imprint', 'id')
        }),
        ('Availability', {
            'fields':('status', 'due_back')
        }),
    )
