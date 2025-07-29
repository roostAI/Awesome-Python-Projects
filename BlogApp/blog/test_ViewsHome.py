import pytest
from django.test import RequestFactory
from django.http import HttpResponse
from django.test import override_settings
from django.conf import settings
from django.apps import apps
from django.shortcuts import render
from blog.models import Post
from django.contrib.auth.models import User

# Configure Django settings for testing
@pytest.fixture(scope="session", autouse=True)
def django_setup():
    settings.configure(
        INSTALLED_APPS=[
            'django.contrib.auth',
            'django.contrib.contenttypes',
            'django.contrib.sessions',
            'django.contrib.messages',
            'django.contrib.staticfiles',
            'blog',
        ],
        DATABASES={
            'default': {
                'ENGINE': 'django.db.backends.sqlite3',
                'NAME': ':memory:',
            }
        },
        TEMPLATES=[{
            'BACKEND': 'django.template.backends.django.DjangoTemplates',
            'APP_DIRS': True,
        }],
        SECRET_KEY='test_key',
    )
    apps.populate(settings.INSTALLED_APPS)

# Import home view after Django setup
@pytest.fixture(scope="session", autouse=True)
def import_home_view():
    from blog.views import home
    return home

class ViewsHome:
    @pytest.fixture
    def request_factory(self):
        return RequestFactory()
    
    @pytest.fixture
    def user(self):
        return User.objects.create_user(
            username='testuser',
            email='test@example.com',
            password='testpassword'
        )
    
    def test_home_retrieves_all_posts(self, request_factory, user, import_home_view):
        """Test that home view retrieves all posts and includes them in context."""
        # Arrange
        request = request_factory.get('/')
        # Create multiple posts
        post1 = Post.objects.create(
            title='Test Post 1',
            content='Content for test post 1',
            author=user
        )
        post2 = Post.objects.create(
            title='Test Post 2',
            content='Content for test post 2',
            author=user
        )
        post3 = Post.objects.create(
            title='Test Post 3',
            content='Content for test post 3',
            author=user
        )
        
        # Act
        response = import_home_view(request)
        
        # Assert
        assert isinstance(response, HttpResponse)
        # Extract context from response
        context = response.context_data
        assert 'posts' in context
        posts = context['posts']
        assert len(posts) == 3
        assert post1 in posts
        assert post2 in posts
        assert post3 in posts
    
    def test_home_with_no_posts(self, request_factory, import_home_view):
        """Test that home view works correctly when there are no posts."""
        # Arrange
        request = request_factory.get('/')
        # Ensure no posts exist
        Post.objects.all().delete()
        
        # Act
        response = import_home_view(request)
        
        # Assert
        assert isinstance(response, HttpResponse)
        context = response.context_data
        assert 'posts' in context
        posts = context['posts']
        assert len(posts) == 0
    
    def test_home_renders_correct_template(self, request_factory, import_home_view):
        """Test that home view renders the correct template."""
        # Arrange
        request = request_factory.get('/')
        
        # Act
        response = import_home_view(request)
        
        # Assert
        assert isinstance(response, HttpResponse)
        # Check that the correct template is used
        assert 'blog/home.html' in [template.name for template in response.templates]
        
    def test_home_with_many_posts(self, request_factory, user, import_home_view):
        """Test that home view can handle a large number of posts."""
        # Arrange
        request = request_factory.get('/')
        # Create a large number of posts
        posts = []
        for i in range(100):  # Creating 100 posts
            posts.append(Post.objects.create(
                title=f'Test Post {i}',
                content=f'Content for test post {i}',
                author=user
            ))
        
        # Act
        response = import_home_view(request)
        
        # Assert
        assert isinstance(response, HttpResponse)
        context = response.context_data
        assert 'posts' in context
        retrieved_posts = context['posts']
        assert len(retrieved_posts) == 100
        # Check that all posts are retrieved
        for post in posts:
            assert post in retrieved_posts
