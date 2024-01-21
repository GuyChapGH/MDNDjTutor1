from django.shortcuts import render

from .models import Book, BookInstance, Author, Genre
# Create your views here.


def index(request):
    """View function for home page of site"""

    #Generate counts of some of the main objects
    num_books = Book.objects.all().count()
    num_instances = BookInstance.objects.all().count()

    #Available books (status = 'a')
    num_instances_available = BookInstance.objects.filter(status__exact='a').count()

    # The 'all()' is defined by default
    num_authors = Author.objects.count()

    # Count for Genres
    num_genres = Genre.objects.all().count()

    # Count for books that include the word 'the' (case-insensitive)
    num_books_the = Book.objects.filter(title__icontains='the').count()

    # Using session to track number of visits by browser to LocalLibrary Home page 
    num_visits = request.session.get('num_books', 0)
    request.session['num_books'] = num_visits + 1

    context = {
        'num_books': num_books,
        'num_instances': num_instances,
        'num_instances_available': num_instances_available,
        'num_authors': num_authors,
        'num_genres': num_genres,
        'num_books_the': num_books_the,
        'num_visits': num_visits,    
    }

    # Render the index.html template with the data from context variable 
    return render(request, 'index.html', context=context)

from django.views import generic

class BookListView(generic.ListView):
    model = Book
    paginate_by = 10


class BookDetailView(generic.DetailView):
    model = Book    

class AuthorListView(generic.ListView):
    model = Author
    paginate_by = 10

class AuthorDetailView(generic.DetailView):
    model = Author

from django.contrib.auth.mixins import LoginRequiredMixin

class LoanedBooksByUserListView(LoginRequiredMixin,generic.ListView):
    """Generic class-based view listing books on loan to current user."""
    model = BookInstance
    template_name = 'catalog/bookinstance_list_borrowed_user.html'
    paginate_by = 10

    def get_queryset(self):
        return (
            BookInstance.objects.filter(borrower=self.request.user)
            .filter(status__exact='o')
            .order_by('due_back')
        )