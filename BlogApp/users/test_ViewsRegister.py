import pytest
from django.test import RequestFactory
from django.contrib.messages.storage.fallback import FallbackStorage
from django.contrib.auth.models import User
from django.urls import reverse
from users.views import register
from forms import UserRegisterForm
import django
from django.conf import settings

# Configure Django settings before importing models
settings.configure(
    INSTALLED_APPS=[
        'django.contrib.auth',
        'django.contrib.contenttypes',
        'django.contrib.sessions',
        'django.contrib.messages',
        'users',
    ],
    DATABASES={
        'default': {
            'ENGINE': 'django.db.backends.sqlite3',
            'NAME': ':memory:',
        }
    },
    MIDDLEWARE=[
        'django.contrib.sessions.middleware.SessionMiddleware',
        'django.contrib.messages.middleware.MessageMiddleware',
    ],
    ROOT_URLCONF='users.urls',
)

django.setup()

class ViewsRegister:
    
    @pytest.fixture
    def request_factory(self):
        return RequestFactory()
    
    def setup_request_messages(self, request):
        """Set up messages for the request"""
        setattr(request, 'session', 'session')
        messages = FallbackStorage(request)
        setattr(request, '_messages', messages)
        return request
    
    def test_successful_registration(self, request_factory, monkeypatch):
        """
        Test that a valid form submission creates a user, shows success message,
        and redirects to login page
        """
        # Arrange
        request = request_factory.post('/register/', {
            'username': 'testuser',
            'email': 'test@example.com',
            'password1': 'TestPassword123',
            'password2': 'TestPassword123'
        })
        request = self.setup_request_messages(request)
        
        # Mock form validation to always return True
        class MockForm:
            def __init__(self, *args, **kwargs):
                self.cleaned_data = {'username': 'testuser'}
            
            def is_valid(self):
                return True
                
            def save(self):
                # Create a user for testing
                return User.objects.create_user(
                    username='testuser',
                    email='test@example.com',
                    password='TestPassword123'
                )
        
        monkeypatch.setattr('forms.UserRegisterForm', MockForm)
        
        # Act
        response = register(request)
        
        # Assert
        assert response.status_code == 302  # Check for redirect
        assert response.url == reverse('login')  # Check redirect destination
        
        # Verify user was created
        assert User.objects.filter(username='testuser').exists()
        
        # Check for success message
        messages = list(request._messages)
        assert len(messages) == 1
        assert 'Your account has been created' in str(messages[0])
    
    def test_invalid_form_submission(self, request_factory, monkeypatch):
        """
        Test that an invalid form submission returns the register page with form errors
        """
        # Arrange
        request = request_factory.post('/register/', {
            'username': 'testuser',
            'email': 'invalid-email',  # Invalid email format
            'password1': 'password',
            'password2': 'different-password'  # Passwords don't match
        })
        request = self.setup_request_messages(request)
        
        # Mock form validation to always return False
        class MockInvalidForm:
            def __init__(self, *args, **kwargs):
                self.errors = {'email': ['Enter a valid email address.'], 
                              'password2': ['Passwords do not match.']}
            
            def is_valid(self):
                return False
        
        monkeypatch.setattr('forms.UserRegisterForm', MockInvalidForm)
        
        # Mock render function to verify template and context
        def mock_render(request, template, context):
            assert template == 'users/register.html'
            assert 'form' in context
            return "rendered_template"
        
        monkeypatch.setattr('users.views.render', mock_render)
        
        # Act
        response = register(request)
        
        # Assert
        assert response == "rendered_template"
        
        # Verify no user was created
        assert not User.objects.filter(username='testuser').exists()
        
        # Verify no success message was added
        messages = list(request._messages)
        assert len(messages) == 0
