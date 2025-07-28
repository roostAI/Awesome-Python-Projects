import pytest
from unittest.mock import Mock, patch
import django
from django.conf import settings

# Configure Django settings before importing models
settings.configure(
    INSTALLED_APPS=[
        'django.contrib.auth',
        'django.contrib.contenttypes',
        'blog',
    ],
    DATABASES={
        'default': {
            'ENGINE': 'django.db.backends.sqlite3',
            'NAME': ':memory:',
        }
    }
)
django.setup()

from django.contrib.auth.models import User
from blog.models import Post
from blog.views import PostDeleteView


class PostDeleteViewTestFunc:
    """Test suite for the test_func method of PostDeleteView."""

    @pytest.fixture
    def setup_view(self):
        """Set up a PostDeleteView instance with mocked dependencies."""
        view = PostDeleteView()
        view.request = Mock()
        return view

    @pytest.fixture
    def create_user(self):
        """Create and return a test user."""
        return User.objects.create_user(
            username='testuser',
            email='test@example.com',
            password='testpassword'
        )

    @pytest.fixture
    def create_post(self, create_user):
        """Create and return a test post with the specified author."""
        return Post.objects.create(
            title='Test Post',
            content='Test Content',
            author=create_user
        )

    def test_user_is_post_author(self, setup_view, create_user, create_post):
        """
        Test that test_func returns True when the logged-in user is the author of the post.
        """
        # Arrange
        view = setup_view
        view.request.user = create_user
        
        # Mock get_object to return our test post
        with patch.object(view, 'get_object', return_value=create_post):
            # Act
            result = view.test_func()
            
            # Assert
            assert result is True, "test_func should return True when user is the post author"

    def test_user_is_not_post_author(self, setup_view, create_post):
        """
        Test that test_func returns False when the logged-in user is not the author of the post.
        """
        # Arrange
        view = setup_view
        different_user = User.objects.create_user(
            username='anotheruser',
            email='another@example.com',
            password='anotherpassword'
        )
        view.request.user = different_user
        
        # Mock get_object to return our test post (which has a different author)
        with patch.object(view, 'get_object', return_value=create_post):
            # Act
            result = view.test_func()
            
            # Assert
            assert result is False, "test_func should return False when user is not the post author"

    def test_anonymous_user(self, setup_view, create_post):
        """
        Test that test_func returns False when the user is anonymous (not authenticated).
        """
        # Arrange
        view = setup_view
        view.request.user = Mock(is_authenticated=False)
        
        # Mock get_object to return our test post
        with patch.object(view, 'get_object', return_value=create_post):
            # Act
            result = view.test_func()
            
            # Assert
            assert result is False, "test_func should return False for anonymous users"
