import pytest
from unittest.mock import patch, MagicMock
from django.http import Http404
from django.contrib.auth.models import User
from blog.models import Post
from blog.views import UserPostListView

# Add pytest configuration for Django settings
pytestmark = pytest.mark.django_db

class TestUserPostListViewGetQueryset:
    
    @pytest.fixture
    def setup_view(self):
        """Setup the UserPostListView instance with mock kwargs."""
        view = UserPostListView()
        view.kwargs = {'username': 'testuser'}
        return view
    
    @pytest.fixture
    def mock_user(self):
        """Create a mock User instance."""
        user = MagicMock(spec=User)
        user.username = 'testuser'
        return user
    
    @pytest.fixture
    def mock_posts(self):
        """Create mock Post queryset."""
        posts = MagicMock()
        ordered_posts = MagicMock()
        posts.order_by.return_value = ordered_posts
        return posts, ordered_posts
    
    def test_get_posts_for_existing_user(self, setup_view, mock_user, mock_posts):
        """
        Test that the method correctly retrieves all posts authored by a specific user
        when the username exists in the database.
        """
        posts, ordered_posts = mock_posts
        
        # Mock the get_object_or_404 function to return our mock user
        with patch('blog.views.get_object_or_404', return_value=mock_user) as mock_get_object:
            # Mock the Post.objects.filter to return our mock posts
            with patch('blog.views.Post.objects.filter', return_value=posts) as mock_filter:
                
                # Call the method
                result = setup_view.get_queryset()
                
                # Assert get_object_or_404 was called with correct parameters
                mock_get_object.assert_called_once_with(User, username='testuser')
                
                # Assert filter was called with the correct user
                mock_filter.assert_called_once_with(author=mock_user)
                
                # Assert order_by was called with '-date_posted'
                posts.order_by.assert_called_once_with('-date_posted')
                
                # Assert the result is the ordered posts
                assert result == ordered_posts
    
    def test_get_posts_for_nonexistent_user(self, setup_view):
        """
        Test that the method raises Http404 when the username does not exist in the database.
        """
        # Mock get_object_or_404 to raise Http404
        with patch('blog.views.get_object_or_404', side_effect=Http404()) as mock_get_object:
            # Call the method and expect Http404
            with pytest.raises(Http404):
                setup_view.get_queryset()
            
            # Assert get_object_or_404 was called with correct parameters
            mock_get_object.assert_called_once_with(User, username='testuser')
    
    def test_empty_posts_for_user(self, setup_view, mock_user):
        """
        Test that the method returns an empty queryset when the user exists but has no posts.
        """
        # Create an empty queryset
        empty_queryset = MagicMock()
        ordered_empty_queryset = MagicMock()
        empty_queryset.order_by.return_value = ordered_empty_queryset
        
        # Mock the get_object_or_404 function to return our mock user
        with patch('blog.views.get_object_or_404', return_value=mock_user) as mock_get_object:
            # Mock the Post.objects.filter to return an empty queryset
            with patch('blog.views.Post.objects.filter', return_value=empty_queryset) as mock_filter:
                
                # Call the method
                result = setup_view.get_queryset()
                
                # Assert get_object_or_404 was called with correct parameters
                mock_get_object.assert_called_once_with(User, username='testuser')
                
                # Assert filter was called with the correct user
                mock_filter.assert_called_once_with(author=mock_user)
                
                # Assert order_by was called with '-date_posted'
                empty_queryset.order_by.assert_called_once_with('-date_posted')
                
                # Assert the result is the ordered empty queryset
                assert result == ordered_empty_queryset
