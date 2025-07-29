import pytest
from unittest.mock import Mock, patch
from django.contrib.auth.models import User
from django.conf import settings
from blog.views import PostCreateView


# Configure Django settings before importing Django models
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
    """Test suite for the form_valid method of PostCreateView."""

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
        
        # Act
        with patch('django.views.generic.CreateView.form_valid') as mock_super_form_valid:
            mock_super_form_valid.return_value = "success_response"
            response = view.form_valid(mock_form)
        
        # Assert
        assert mock_form.instance.author == mock_user, "Form instance author should be set to the request user"
        mock_super_form_valid.assert_called_once_with(mock_form)
        assert response == "success_response", "Method should return the result of super().form_valid()"

    def test_form_valid_with_no_user_in_request(self):
        """
        Test that form_valid handles the case where request.user is not available.
        This is an edge case that should be handled gracefully.
        """
        # Arrange
        # Create a mock request without a user
        mock_request = Mock()
        delattr(mock_request, 'user')  # Ensure user attribute doesn't exist
        
        # Create a mock form with an instance
        mock_form = Mock()
        mock_form.instance = Mock()
        
        # Create the view and set the request
        view = PostCreateView()
        view.request = mock_request
        
        # Act & Assert
        with pytest.raises(AttributeError):
            # This should raise an AttributeError since request.user doesn't exist
            view.form_valid(mock_form)
