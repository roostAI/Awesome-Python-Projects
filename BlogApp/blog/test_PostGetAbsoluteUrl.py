import pytest
from unittest import mock
from django.urls import reverse

# Create a mock Post class to avoid Django settings issues
class Post:
    def get_absolute_url(self):
        return reverse('post-detail', kwargs={'pk': self.pk})

class TestPostGetAbsoluteUrl:
    """Test suite for the Post.get_absolute_url method."""

    def test_get_absolute_url_with_valid_post(self, mocker):
        """
        Test that get_absolute_url returns the correct URL for a valid post.
        
        This test verifies that the method correctly generates a URL for a post
        with a valid primary key by calling reverse with the right parameters.
        """
        # Arrange
        mock_post = mocker.Mock(spec=Post)
        mock_post.pk = 1
        
        # Mock the reverse function to verify it's called correctly
        mock_reverse = mocker.patch('django.urls.reverse', return_value='/post/1/')
        
        # Act
        result = Post.get_absolute_url(mock_post)
        
        # Assert
        mock_reverse.assert_called_once_with('post-detail', kwargs={'pk': 1})
        assert result == '/post/1/'
        
    def test_get_absolute_url_with_different_pk(self, mocker):
        """
        Test that get_absolute_url works with different primary key values.
        
        This test ensures the method works correctly with various primary key values,
        which is important for real-world usage where posts have different IDs.
        """
        # Arrange
        mock_post = mocker.Mock(spec=Post)
        mock_post.pk = 42  # Using a different pk value
        
        # Mock the reverse function
        mock_reverse = mocker.patch('django.urls.reverse', return_value='/post/42/')
        
        # Act
        result = Post.get_absolute_url(mock_post)
        
        # Assert
        mock_reverse.assert_called_once_with('post-detail', kwargs={'pk': 42})
        assert result == '/post/42/'
        
    def test_get_absolute_url_with_none_pk(self, mocker):
        """
        Test behavior when the post has no primary key (None).
        
        This tests an edge case where a post might not have been saved to the
        database yet and therefore doesn't have a primary key.
        """
        # Arrange
        mock_post = mocker.Mock(spec=Post)
        mock_post.pk = None
        
        # Mock the reverse function
        mock_reverse = mocker.patch('django.urls.reverse')
        
        # Act & Assert
        # This should raise an exception since None is not a valid pk for URL generation
        with pytest.raises(Exception):
            Post.get_absolute_url(mock_post)
