import pytest
from unittest.mock import Mock, patch
from django.urls import reverse
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

# Import the method to test
from blog.models import Post


class TestPostGetAbsoluteUrl:
    """Test suite for the Post.get_absolute_url method."""

    def test_get_absolute_url_returns_correct_url(self):
        """
        Test that get_absolute_url returns the correct URL for a post.
        
        This test verifies that the method correctly uses Django's reverse
        function to generate a URL with the post's primary key.
        """
        # Arrange
        mock_post = Mock(spec=Post)
        mock_post.pk = 42  # Set a test primary key
        
        # Attach the method to test to our mock
        mock_post.get_absolute_url = Post.get_absolute_url.__get__(mock_post)
        
        # Act
        result_url = mock_post.get_absolute_url()
        
        # Assert
        expected_url = reverse('post-detail', kwargs={'pk': 42})
        assert result_url == expected_url, f"Expected URL: {expected_url}, but got: {result_url}"
    
    def test_get_absolute_url_with_different_pk_values(self):
        """
        Test get_absolute_url with various primary key values.
        
        This test ensures the method works correctly with different types
        of primary keys that might be encountered in real scenarios.
        """
        test_pks = [1, 999, 10000]  # Various realistic PK values
        
        for pk in test_pks:
            # Arrange
            mock_post = Mock(spec=Post)
            mock_post.pk = pk
            mock_post.get_absolute_url = Post.get_absolute_url.__get__(mock_post)
            
            # Act
            result_url = mock_post.get_absolute_url()
            
            # Assert
            expected_url = reverse('post-detail', kwargs={'pk': pk})
            assert result_url == expected_url, f"Failed with pk={pk}. Expected: {expected_url}, got: {result_url}"
    
    @patch('django.urls.reverse')
    def test_reverse_called_with_correct_arguments(self, mock_reverse):
        """
        Test that the reverse function is called with the correct arguments.
        
        This test verifies that the method correctly passes the view name
        and primary key to Django's reverse function.
        """
        # Arrange
        mock_post = Mock(spec=Post)
        mock_post.pk = 123
        mock_post.get_absolute_url = Post.get_absolute_url.__get__(mock_post)
        mock_reverse.return_value = '/expected/url/'
        
        # Act
        result = mock_post.get_absolute_url()
        
        # Assert
        mock_reverse.assert_called_once_with('post-detail', kwargs={'pk': 123})
        assert result == '/expected/url/'
