import pytest
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from unittest.mock import patch
import django
from django.conf import settings

# Configure Django settings before importing models
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

from users.signals import create_profile
from users.models import Profile  # Assuming Profile is in users.models


@pytest.fixture
def disconnect_signals():
    """Temporarily disconnect post_save signals to isolate tests."""
    # Store the original receivers
    original_receivers = post_save.receivers
    # Disconnect all receivers
    post_save.receivers = []
    
    yield
    
    # Restore original receivers after test
    post_save.receivers = original_receivers


class SignalsCreateProfile:
    
    @pytest.mark.django_db
    def test_profile_created_for_new_user(self):
        """Test that a Profile is created when a new User is created."""
        # Connect our signal handler
        post_save.connect(create_profile, sender=User)
        
        # Create a new user
        user = User.objects.create_user(
            username='testuser',
            email='test@example.com',
            password='password123'
        )
        
        # Check if a profile was created for this user
        profile_exists = Profile.objects.filter(user=user).exists()
        
        # Assert that a profile was created
        assert profile_exists, "Profile was not created for the new user"
        
        # Clean up by disconnecting the signal
        post_save.disconnect(create_profile, sender=User)
    
    @pytest.mark.django_db
    def test_profile_not_created_for_user_update(self, disconnect_signals):
        """Test that a Profile is not created when an existing User is updated."""
        # First create a user without the signal
        user = User.objects.create_user(
            username='updateuser',
            email='update@example.com',
            password='password123'
        )
        
        # Delete any profile that might have been created
        Profile.objects.filter(user=user).delete()
        
        # Now connect our signal
        post_save.connect(create_profile, sender=User)
        
        # Count profiles before update
        profile_count_before = Profile.objects.count()
        
        # Update the user
        user.first_name = "Updated"
        user.save()
        
        # Count profiles after update
        profile_count_after = Profile.objects.count()
        
        # Assert that no new profile was created
        assert profile_count_before == profile_count_after, "A profile was incorrectly created when updating a user"
        
        # Clean up
        post_save.disconnect(create_profile, sender=User)
    
    @pytest.mark.django_db
    def test_profile_creation_with_mocked_profile_model(self):
        """Test the signal handler with a mocked Profile model to verify correct parameters."""
        # Connect our signal handler
        post_save.connect(create_profile, sender=User)
        
        # Mock the Profile.objects.create method
        with patch('users.models.Profile.objects.create') as mock_create:
            # Create a new user
            user = User.objects.create_user(
                username='mockuser',
                email='mock@example.com',
                password='password123'
            )
            
            # Verify that Profile.objects.create was called with the correct parameters
            mock_create.assert_called_once_with(user=user)
        
        # Clean up
        post_save.disconnect(create_profile, sender=User)
