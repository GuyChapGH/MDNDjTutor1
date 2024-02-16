from django.db import models
from django.urls import reverse

from django.conf import settings
from datetime import date

# Create your models here.

class Genre(models.Model):
    """Model representing a book genre."""
    name = models.CharField(max_length=200, unique=True, help_text='Enter a book genre(e.g. Science Fiction, French Poetry etc.)')

    def __str__(self):
        """String for representing the Model object."""
        return self.name
    
    def get_absolute_url(self):
        """Returns the url to access a particular genre instance."""
        return reverse('genre-detail', args=[str(self.id)])
    

class Language(models.Model):
    name = models.CharField(max_length=200, unique=True, help_text="Enter a language for this book. E.g. English, French, Japanese etc.")

    def __str__(self):
        """Returns a string representing this Model object."""
        return self.name
    
    def get_absolute_url(self):
        """Returns the url to access a particular language instance."""
        return reverse('language-detail', args=[str(self.id)])

    
class Book(models.Model):
    """Model representing a book (but not a specific copy of a book)."""
    title = models.CharField(max_length=200)
    author = models.ForeignKey('Author', on_delete=models.RESTRICT, null=True)
    #Foreign Key used because book can have only one author(in this implementation)
    #but authors can have multiple books.
    #Author as a string rather than object because it hasn't been declared yet in file

    summary = models.TextField(max_length=1000, help_text="Enter a brief description of the book")
    isbn = models.CharField('ISBN', max_length=13, unique=True, help_text='13 character <a href="https://www.isbn-international.org/content/what-isbn''">ISBN number</a>')

    genre = models.ManyToManyField(Genre, help_text="Select a genre for this book.")
    #ManytoManyField used because genre can contain many books and books can cover many genres.
    #Genre class defined above so can use object.

    language = models.ForeignKey(Language, on_delete=models.SET_NULL, null=True, help_text="Select a language for this book.")
    #Foreign Key because each book is in one language but many books can have the same language.

    def __str__(self):
        """String for representing the Model object."""
        return self.title
    
    def get_absolute_url(self):
        """Returns the url to access a detail record for this book."""
        return reverse('book-detail', args=[str(self.id)])
    
    def display_genre(self):
        """Create a string for the Genre. This is required to display genre in Admin"""
        return ', '.join(genre.name for genre in self.genre.all()[:3])
    
    display_genre.short_description = 'Genre'



import uuid #Required for unique book instances

class BookInstance(models.Model):
    """Model representing a specific copy of a book (i.e. one that can be borrowed from the library.)"""
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, help_text="Unique ID for this particular book across whole library.")
    book = models.ForeignKey('Book', on_delete=models.RESTRICT, null=True)
    imprint = models.CharField(max_length=200)
    due_back = models.DateField(null=True, blank=True)

    borrower = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, blank=True)

    LOAN_STATUS = (
        ('m', 'Maintenance'),
        ('o', 'On loan'),
        ('a', 'Available'),
        ('r', 'Reserved'),
    )

    status = models.CharField(max_length=1, choices=LOAN_STATUS, blank=True, default='m', help_text='Book availabilty',)

    class Meta:
        ordering = ['due_back']
        permissions = (("can_mark_returned", "Set book as returned"),)

    
    def __str__(self):
        """String for representing the Model object"""
        return f'{self.id} ({self.book.title})'
    
    def is_overdue(self):
        """Determines if the book is overdue based on due date and current date"""
        return bool(self.due_back and date.today() > self.due_back)



class Author(models.Model):
    """Model representing an author."""
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    date_of_birth = models.DateField(null=True, blank=True)
    date_of_death = models.DateField('died', null=True, blank=True)

    class Meta:
        ordering = ['last_name', 'first_name']
    
    def get_absolute_url(self):
        """Returns the URL to access a particular author instance"""
        return reverse('author-detail', args=[str(self.id)])
    
    def __str__(self):
        """String for representing the Model object"""
        return f'{self.last_name}, {self.first_name}'