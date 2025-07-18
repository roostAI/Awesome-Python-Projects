import pytest
from unittest.mock import Mock, patch
import django
import os
from django.conf import settings

# Configure Django settings before importing models
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'django_project.settings')
django.setup()

from django.contrib.auth.models import User
from blog.models import Post
from blog.views import PostDeleteView


class PostDeleteViewTestFunc:
    """Test suite for the test_func method of PostDeleteView class."""

    @pytest.fixture
    def setup_user(self):
        """Create and return a test user."""
        return User.objects.create_user(
            username='testuser',
            email='test@example.com',
            password='testpassword'
        )
    
    @pytest.fixture
    def setup_other_user(self):
        """Create and return another test user."""
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
        """
        # Arrange
        view = PostDeleteView()
        view.request = Mock()
        view.request.user = setup_user
        
        # Mock the get_object method to return our test post
        view.get_object = Mock(return_value=setup_post)
        
        # Act
        result = view.test_func()
        
        # Assert
        assert result is True, "test_func should return True when user is the post author"
    
    def test_user_is_not_post_author(self, setup_other_user, setup_post):
        """
        Test that test_func returns False when the logged-in user is not the author of the post.
        """
        # Arrange
        view = PostDeleteView()
        view.request = Mock()
        view.request.user = setup_other_user
        
        # Mock the get_object method to return our test post
        view.get_object = Mock(return_value=setup_post)
        
        # Act
        result = view.test_func()
        
        # Assert
        assert result is False, "test_func should return False when user is not the post author"
    
    def test_with_anonymous_user(self, setup_post):
        """
        Test that test_func returns False when the user is anonymous (not logged in).
        """
        # Arrange
        view = PostDeleteView()
        view.request = Mock()
        view.request.user = Mock(is_authenticated=False)  # Anonymous user
        
        # Mock the get_object method to return our test post
        view.get_object = Mock(return_value=setup_post)
        
        # Act
        result = view.test_func()
        
        # Assert
        assert result is False, "test_func should return False for anonymous users"
    
    def test_with_nonexistent_post(self, setup_user):
        """
        Test handling when the post doesn't exist or can't be retrieved.
        """
        # Arrange
        view = PostDeleteView()
        view.request = Mock()
        view.request.user = setup_user
        
        # Mock get_object to simulate a post that doesn't exist
        # This could happen in real scenarios due to race conditions or DB issues
        view.get_object = Mock(return_value=None)
        
        # Act & Assert
        with pytest.raises(AttributeError):
            view.test_func()
        
        # This test verifies that the method properly handles (or in this case, fails appropriately)
        # when the post doesn't exist
