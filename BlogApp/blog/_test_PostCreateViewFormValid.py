import pytest
from unittest.mock import Mock, patch
from django.http import HttpResponse
from django.contrib.auth.models import User
from django.conf import settings
from blog.views import PostCreateView


# Configure Django settings before tests run
@pytest.fixture(scope="session", autouse=True)
def configure_django_settings():
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


class TestPostCreateViewFormValid:
    """Test suite for the form_valid method of PostCreateView class."""

    def test_form_valid_sets_author_to_current_user(self):
        """
        Test that form_valid sets the form's instance author to the current user
        and calls the parent class's form_valid method.
        """
        # Arrange
        # Create a mock user
        mock_user = Mock(spec=User)
        mock_user.id = 1
        mock_user.username = "testuser"
        
        # Create a mock request with the user
        mock_request = Mock()
        mock_request.user = mock_user
        
        # Create a mock form with an instance
        mock_form = Mock()
        mock_form.instance = Mock()
        
        # Create the view and set the request
        view = PostCreateView()
        view.request = mock_request
        
        # Mock the super().form_valid() call to return a response
        with patch('blog.views.CreateView.form_valid', return_value=HttpResponse()) as mock_super_form_valid:
            # Act
            response = view.form_valid(mock_form)
            
            # Assert
            # Check that the author was set to the current user
            assert mock_form.instance.author == mock_user
            # Check that super().form_valid() was called with the form
            mock_super_form_valid.assert_called_once_with(mock_form)
            # Check that the response from super().form_valid() is returned
            assert isinstance(response, HttpResponse)

    def test_form_valid_with_anonymous_user(self):
        """
        Test that form_valid handles the case when the user is not authenticated.
        This should not happen in practice due to LoginRequiredMixin, but we test it
        for completeness.
        """
        # Arrange
        # Create a mock request with an AnonymousUser
        mock_request = Mock()
        mock_request.user = None  # Simulating no user or anonymous user
        
        # Create a mock form with an instance
        mock_form = Mock()
        mock_form.instance = Mock()
        
        # Create the view and set the request
        view = PostCreateView()
        view.request = mock_request
        
        # Mock the super().form_valid() call
        with patch('blog.views.CreateView.form_valid', return_value=HttpResponse()) as mock_super_form_valid:
            # Act
            response = view.form_valid(mock_form)
            
            # Assert
            # Check that the author was set to None (or whatever the request.user is)
            assert mock_form.instance.author is None
            # Check that super().form_valid() was still called
            mock_super_form_valid.assert_called_once_with(mock_form)
