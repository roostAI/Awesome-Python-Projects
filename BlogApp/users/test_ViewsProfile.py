import pytest
from django.contrib.auth.models import User
from django.contrib.messages import get_messages
from django.http import HttpRequest
from django.test import RequestFactory, TestCase
from django.urls import reverse
from unittest.mock import patch, MagicMock

# Configure Django settings before importing Django modules
import django
from django.conf import settings
if not settings.configured:
    settings.configure(
        INSTALLED_APPS=[
            'django.contrib.auth',
            'django.contrib.contenttypes',
            'users',
        ],
        DATABASES={
            'default': {
                'ENGINE': 'django.db.backends.sqlite3',
                'NAME': ':memory:',
            }
        }
    )
    django.setup()

from users.views import profile


class ViewsProfile:
    @pytest.fixture
    def setup_user(self):
        """Create a test user with a profile"""
        user = MagicMock(spec=User)
        user.profile = MagicMock()
        return user

    @pytest.fixture
    def setup_request(self, setup_user):
        """Set up a request object with an authenticated user"""
        factory = RequestFactory()
        request = factory.get(reverse('profile'))
        request.user = setup_user
        request._messages = MagicMock()
        return request

    @patch('users.views.UserUpdateForm')
    @patch('users.views.ProfileUpdateForm')
    @patch('users.views.messages')
    @patch('users.views.redirect')
    def test_successful_profile_update(self, mock_redirect, mock_messages, 
                                      mock_profile_form, mock_user_form, 
                                      setup_request, setup_user):
        """Test that profile updates successfully with valid form data"""
        # Arrange
        post_request = setup_request
        post_request.method = 'POST'
        
        # Mock forms
        mock_user_form_instance = MagicMock()
        mock_user_form_instance.is_valid.return_value = True
        mock_user_form.return_value = mock_user_form_instance
        
        mock_profile_form_instance = MagicMock()
        mock_profile_form_instance.is_valid.return_value = True
        mock_profile_form.return_value = mock_profile_form_instance
        
        # Act
        response = profile(post_request)
        
        # Assert
        mock_user_form_instance.save.assert_called_once()
        mock_profile_form_instance.save.assert_called_once()
        mock_messages.success.assert_called_once_with(
            post_request, 
            f'Your profile has been updated. '
        )
        mock_redirect.assert_called_once_with('profile')
        
    @patch('users.views.UserUpdateForm')
    @patch('users.views.ProfileUpdateForm')
    @patch('users.views.render')
    def test_get_profile_page(self, mock_render, mock_profile_form, 
                             mock_user_form, setup_request, setup_user):
        """Test that GET request renders profile page with correct forms"""
        # Arrange
        get_request = setup_request
        get_request.method = 'GET'
        
        mock_user_form_instance = MagicMock()
        mock_user_form.return_value = mock_user_form_instance
        
        mock_profile_form_instance = MagicMock()
        mock_profile_form.return_value = mock_profile_form_instance
        
        # Act
        response = profile(get_request)
        
        # Assert
        mock_user_form.assert_called_once_with(instance=setup_user)
        mock_profile_form.assert_called_once_with(instance=setup_user.profile)
        mock_render.assert_called_once_with(
            get_request, 
            'users/profile.html', 
            {
                'u_form': mock_user_form_instance,
                'p_form': mock_profile_form_instance
            }
        )
        
    # Note: There's a bug in the profile view function:
    # p_form.is_valid is a method but it's not being called with parentheses
    # It should be p_form.is_valid() instead of p_form.is_valid
    # This would cause the form validation to always pass regardless of the form data
