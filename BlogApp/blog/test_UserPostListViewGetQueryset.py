import pytest
from unittest.mock import patch, MagicMock
from django.http import Http404
from django.contrib.auth.models import User
from django.test import override_settings
from blog.views import UserPostListView

# Add Django settings configuration for tests
pytestmark = pytest.mark.django_db

class TestUserPostListViewGetQueryset:
    """Test suite for the get_queryset method of UserPostListView class."""
    
    @pytest.fixture
    def setup_view(self):
        """Fixture to set up a UserPostListView instance."""
        view = UserPostListView()
        view.kwargs = {}
        return view
    
    @patch('blog.views.get_object_or_404')
    @patch('blog.views.Post.objects.filter')
    def test_get_queryset_with_valid_username(self, mock_filter, mock_get_object, setup_view):
        """
        Test that get_queryset correctly retrieves posts for an existing user.
        
        This test verifies that when a valid username is provided in the kwargs,
        the method retrieves all posts authored by that user and orders them
        by date_posted in descending order.
        """
        # Arrange
        view = setup_view
        view.kwargs = {'username': 'testuser'}
        
        # Mock the user object
        mock_user = MagicMock(spec=User)
        mock_user.username = 'testuser'
        mock_get_object.return_value = mock_user
        
        # Mock the queryset
        mock_queryset = MagicMock()
        mock_filter.return_value = mock_queryset
        mock_queryset.order_by.return_value = 'ordered_posts'
        
        # Act
        result = view.get_queryset()
        
        # Assert
        mock_get_object.assert_called_once_with(User, username='testuser')
        mock_filter.assert_called_once_with(author=mock_user)
        mock_queryset.order_by.assert_called_once_with('-date_posted')
        assert result == 'ordered_posts'
    
    @patch('blog.views.get_object_or_404')
    def test_get_queryset_with_nonexistent_username(self, mock_get_object, setup_view):
        """
        Test that get_queryset raises Http404 when username doesn't exist.
        
        This test verifies that when a username that doesn't correspond to any
        user in the database is provided, the method raises an Http404 exception.
        """
        # Arrange
        view = setup_view
        view.kwargs = {'username': 'nonexistentuser'}
        
        # Mock get_object_or_404 to raise Http404
        mock_get_object.side_effect = Http404("User does not exist")
        
        # Act & Assert
        with pytest.raises(Http404):
            view.get_queryset()
        
        mock_get_object.assert_called_once_with(User, username='nonexistentuser')
