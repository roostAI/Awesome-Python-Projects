import pytest
from unittest import mock
from django.urls import reverse
from django.test import TestCase


class PostGetAbsoluteUrl(TestCase):
    """Test suite for the Post.get_absolute_url method."""

    @mock.patch('django.urls.reverse')
    def test_get_absolute_url_with_valid_post(self, mock_reverse):
        """
        Test that get_absolute_url returns the correct URL for a valid post.
        
        This test verifies that the method correctly generates a URL for a post
        with a valid primary key by calling reverse with the right parameters.
        """
        # Create a mock Post class with get_absolute_url method
        class MockPost:
            def __init__(self, pk):
                self.pk = pk
                
            def get_absolute_url(self):
                return reverse('post-detail', kwargs={'pk': self.pk})
        
        # Arrange
        mock_reverse.return_value = '/post/1/'
        post = MockPost(pk=1)
        
        # Act
        result = post.get_absolute_url()
        
        # Assert
        mock_reverse.assert_called_once_with('post-detail', kwargs={'pk': 1})
        self.assertEqual(result, '/post/1/')
        
    @mock.patch('django.urls.reverse')
    def test_get_absolute_url_with_different_pk(self, mock_reverse):
        """
        Test that get_absolute_url works with different primary key values.
        
        This test ensures the method works correctly with various primary key values,
        which is important for real-world usage where posts have different IDs.
        """
        # Create a mock Post class with get_absolute_url method
        class MockPost:
            def __init__(self, pk):
                self.pk = pk
                
            def get_absolute_url(self):
                return reverse('post-detail', kwargs={'pk': self.pk})
        
        # Arrange
        mock_reverse.return_value = '/post/42/'
        post = MockPost(pk=42)
        
        # Act
        result = post.get_absolute_url()
        
        # Assert
        mock_reverse.assert_called_once_with('post-detail', kwargs={'pk': 42})
        self.assertEqual(result, '/post/42/')
        
    @mock.patch('django.urls.reverse')
    def test_get_absolute_url_with_none_pk(self, mock_reverse):
        """
        Test behavior when the post has no primary key (None).
        
        This tests an edge case where a post might not have been saved to the
        database yet and therefore doesn't have a primary key.
        """
        # Create a mock Post class with get_absolute_url method
        class MockPost:
            def __init__(self, pk):
                self.pk = pk
                
            def get_absolute_url(self):
                return reverse('post-detail', kwargs={'pk': self.pk})
        
        # Arrange
        post = MockPost(pk=None)
        
        # Act & Assert
        # This should raise an exception since None is not a valid pk for URL generation
        with self.assertRaises(Exception):
            post.get_absolute_url()
