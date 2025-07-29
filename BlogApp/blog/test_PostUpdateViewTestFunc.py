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
from blog.views import PostUpdateView


class PostUpdateViewTestFunc:
    """Test suite for the test_func method of PostUpdateView class."""

    @pytest.fixture
    def setup_view(self):
        """Setup a PostUpdateView instance with mocked dependencies."""
        view = PostUpdateView()
        view.request = Mock()
        return view

    @pytest.fixture
    def user(self):
        """Create a test user."""
        return Mock(spec=User, id=1, username='testuser')

    @pytest.fixture
    def different_user(self):
        """Create a different test user."""
        return Mock(spec=User, id=2, username='otheruser')

    @pytest.fixture
    def post(self, user):
        """Create a test post with the test user as author."""
        return Mock(spec=Post, id=1, title='Test Post', author=user)

    def test_user_is_post_author(self, setup_view, user, post):
        """
        Test that test_func returns True when the logged-in user is the author of the post.
        
        This validates the core permission logic that allows post authors to 
        perform actions on their own posts.
        """
        # Arrange
        view = setup_view
        view.request.user = user
        
        # Mock the get_object method to return our test post
        with patch.object(PostUpdateView, 'get_object', return_value=post):
            # Act
            result = view.test_func()
            
            # Assert
            assert result is True, "test_func should return True when user is the post author"

    def test_user_is_not_post_author(self, setup_view, different_user, post):
        """
        Test that test_func returns False when the logged-in user is not the author of the post.
        
        This validates that unauthorized users cannot modify posts they don't own.
        """
        # Arrange
        view = setup_view
        view.request.user = different_user
        
        # Mock the get_object method to return our test post (owned by a different user)
        with patch.object(PostUpdateView, 'get_object', return_value=post):
            # Act
            result = view.test_func()
            
            # Assert
            assert result is False, "test_func should return False when user is not the post author"

    def test_anonymous_user(self, setup_view, post):
        """
        Test that test_func returns False when the user is anonymous (not authenticated).
        
        This validates that unauthenticated users cannot modify any posts.
        """
        # Arrange
        view = setup_view
        view.request.user = Mock(is_authenticated=False)
        
        # Mock the get_object method to return our test post
        with patch.object(PostUpdateView, 'get_object', return_value=post):
            # Act
            result = view.test_func()
            
            # Assert
            assert result is False, "test_func should return False for anonymous users"
