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
    def setup_user(self):
        """Create and return a test user."""
        return User.objects.create_user(
            username='testuser',
            email='test@example.com',
            password='testpassword'
        )

    @pytest.fixture
    def setup_different_user(self):
        """Create and return a different test user."""
        return User.objects.create_user(
            username='otheruser',
            email='other@example.com',
            password='otherpassword'
        )

    @pytest.fixture
    def setup_post(self, setup_user):
        """Create and return a test post with the test user as author."""
        return Post.objects.create(
            title='Test Post',
            content='Test Content',
            author=setup_user
        )

    def test_user_is_post_author(self, setup_user, setup_post):
        """
        Test that test_func returns True when the logged-in user is the author of the post.
        
        This validates the core permission logic that allows authors to access their own posts.
        """
        # Arrange
        view = PostUpdateView()
        view.request = Mock()
        view.request.user = setup_user
        
        # Mock the get_object method to return our test post
        view.get_object = Mock(return_value=setup_post)
        
        # Act
        result = view.test_func()
        
        # Assert
        assert result is True, "test_func should return True when user is the post author"

    def test_user_is_not_post_author(self, setup_different_user, setup_post):
        """
        Test that test_func returns False when the logged-in user is not the author of the post.
        
        This validates that the permission logic correctly prevents unauthorized users from
        editing posts they don't own.
        """
        # Arrange
        view = PostUpdateView()
        view.request = Mock()
        view.request.user = setup_different_user
        
        # Mock the get_object method to return our test post
        view.get_object = Mock(return_value=setup_post)
        
        # Act
        result = view.test_func()
        
        # Assert
        assert result is False, "test_func should return False when user is not the post author"

    def test_with_anonymous_user(self, setup_post):
        """
        Test that test_func returns False when the user is anonymous (not authenticated).
        
        This validates that unauthenticated users cannot edit any posts.
        """
        # Arrange
        view = PostUpdateView()
        view.request = Mock()
        view.request.user = Mock(is_authenticated=False)
        
        # Mock the get_object method to return our test post
        view.get_object = Mock(return_value=setup_post)
        
        # Act
        result = view.test_func()
        
        # Assert
        assert result is False, "test_func should return False for anonymous users"
