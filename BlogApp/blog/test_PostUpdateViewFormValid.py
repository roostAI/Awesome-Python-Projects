import pytest
from unittest.mock import Mock, patch
from django.http import HttpResponse
from django.test import RequestFactory
from django.contrib.auth.models import AnonymousUser

# Configure Django settings for testing
import django
from django.conf import settings
if not settings.configured:
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

# Now import the view after Django is configured
from blog.views import PostUpdateView


class TestPostUpdateViewFormValid:
    """Test suite for the form_valid method of PostUpdateView."""

    def test_form_valid_sets_author_to_current_user(self):
        """
        Test that form_valid sets the form's instance author to the current user
        and calls the parent class's form_valid method.
        """
        # Arrange
        # Create mock objects
        mock_user = Mock()
        mock_request = Mock()
        mock_request.user = mock_user
        
        mock_form = Mock()
        mock_form.instance = Mock()
        
        # Create view instance and set request
        view = PostUpdateView()
        view.request = mock_request
        
        # Mock the super().form_valid call to return a response
        with patch('django.views.generic.UpdateView.form_valid', 
                   return_value=HttpResponse()) as mock_super_form_valid:
            
            # Act
            response = view.form_valid(mock_form)
            
            # Assert
            # Verify author is set to the current user
            assert mock_form.instance.author == mock_user
            # Verify super().form_valid was called with the form
            mock_super_form_valid.assert_called_once_with(mock_form)
            # Verify the response from super().form_valid is returned
            assert isinstance(response, HttpResponse)

    def test_form_valid_with_anonymous_user(self):
        """
        Test form_valid behavior when the user is AnonymousUser.
        This is an edge case that shouldn't happen in practice due to LoginRequiredMixin,
        but we test it for completeness.
        """
        # Arrange
        # Create mock objects with AnonymousUser
        from django.contrib.auth.models import AnonymousUser
        mock_request = Mock()
        mock_request.user = AnonymousUser()
        
        mock_form = Mock()
        mock_form.instance = Mock()
        
        # Create view instance and set request
        view = PostUpdateView()
        view.request = mock_request
        
        # Mock the super().form_valid call
        with patch('django.views.generic.UpdateView.form_valid', 
                   return_value=HttpResponse()) as mock_super_form_valid:
            
            # Act
            response = view.form_valid(mock_form)
            
            # Assert
            # Verify author is set to AnonymousUser
            assert mock_form.instance.author == mock_request.user
            # Verify super().form_valid was called
            mock_super_form_valid.assert_called_once_with(mock_form)
