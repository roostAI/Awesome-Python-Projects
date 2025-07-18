import pytest
from unittest.mock import Mock, patch
from django.http import HttpResponse


class PostUpdateViewFormValid:
    """Test suite for the form_valid method of PostUpdateView class."""

    @pytest.mark.django_db
    def test_form_valid_sets_author_to_current_user(self, monkeypatch):
        """
        Test that form_valid sets the form's instance author to the current user
        and calls the parent class's form_valid method.
        """
        # Import here to avoid Django settings configuration issues
        from blog.views import PostUpdateView
        
        # Arrange
        # Create a mock user
        mock_user = Mock()
        mock_user.username = "testuser"
        
        # Create a mock request with the user
        mock_request = Mock()
        mock_request.user = mock_user
        
        # Create a mock form with an instance
        mock_form = Mock()
        mock_form.instance = Mock()
        
        # Create the view and set the request
        view = PostUpdateView()
        view.request = mock_request
        
        # Mock the super().form_valid() call to return a response
        with patch('django.views.generic.UpdateView.form_valid', 
                  return_value=HttpResponse()) as mock_super_form_valid:
            
            # Act
            response = view.form_valid(mock_form)
            
            # Assert
            # Check that the author was set to the current user
            assert mock_form.instance.author == mock_user, \
                "The form instance author should be set to the current user"
            
            # Check that super().form_valid() was called with the form
            mock_super_form_valid.assert_called_once_with(mock_form)
            
            # Check that the response from super().form_valid() is returned
            assert isinstance(response, HttpResponse), \
                "The method should return the response from super().form_valid()"

    @pytest.mark.django_db
    def test_form_valid_with_anonymous_user(self, monkeypatch):
        """
        Test form_valid behavior when the user is anonymous (edge case).
        This should still set the author to whatever user is in the request.
        """
        # Import here to avoid Django settings configuration issues
        from blog.views import PostUpdateView
        
        # Arrange
        # Create an anonymous user
        mock_user = Mock()
        mock_user.is_authenticated = False
        mock_user.username = "anonymous"
        
        # Create a mock request with the anonymous user
        mock_request = Mock()
        mock_request.user = mock_user
        
        # Create a mock form with an instance
        mock_form = Mock()
        mock_form.instance = Mock()
        
        # Create the view and set the request
        view = PostUpdateView()
        view.request = mock_request
        
        # Mock the super().form_valid() call
        with patch('django.views.generic.UpdateView.form_valid', 
                  return_value=HttpResponse()) as mock_super_form_valid:
            
            # Act
            view.form_valid(mock_form)
            
            # Assert
            # Even with an anonymous user, the author should be set to request.user
            assert mock_form.instance.author == mock_user, \
                "The form instance author should be set to the request user even if anonymous"
