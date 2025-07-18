import pytest
from unittest.mock import Mock, patch
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

from django.db.models.signals import post_save
from django.contrib.auth.models import User
from users.signals import save_profile

class SignalsSaveProfile:
    
    def test_profile_saves_when_user_saved(self, monkeypatch):
        """
        Test that when a User instance is saved, the associated Profile is also saved.
        """
        # Arrange
        mock_profile = Mock()
        mock_user = Mock()
        mock_user.profile = mock_profile
        
        # Act
        save_profile(sender=User, instance=mock_user)
        
        # Assert
        mock_profile.save.assert_called_once()
    
    def test_profile_attribute_access(self):
        """
        Test that the function correctly accesses the profile attribute of the instance.
        """
        # Arrange
        mock_profile = Mock()
        mock_instance = Mock()
        mock_instance.profile = mock_profile
        
        # Act
        save_profile(sender=None, instance=mock_instance)
        
        # Assert
        mock_profile.save.assert_called_once()
    
    def test_missing_profile_handling(self):
        """
        Test how the function behaves when the instance doesn't have a profile attribute.
        """
        # Arrange
        mock_instance = Mock(spec=[])  # Instance without profile attribute
        
        # Act & Assert
        with pytest.raises(AttributeError):
            save_profile(sender=None, instance=mock_instance)
    
    def test_signal_connection(self):
        """
        Test that the save_profile function is correctly connected to the post_save signal.
        """
        # This test requires integration with Django's signal framework
        # We'll mock the signal connection to verify it's properly set up
        
        with patch('django.db.models.signals.post_save.connect') as mock_connect:
            # Re-import to trigger signal connection
            # TODO: Adjust the import path based on your project structure
            from users import signals
            
            # Assert
            mock_connect.assert_any_call(
                save_profile, 
                sender=User,
                # Additional arguments might be present depending on your implementation
            )
    
    def test_multiple_user_saves(self):
        """
        Test that multiple saves of the same User instance correctly trigger profile saves each time.
        """
        # Arrange
        mock_profile = Mock()
        mock_user = Mock()
        mock_user.profile = mock_profile
        
        # Act
        save_profile(sender=User, instance=mock_user)
        save_profile(sender=User, instance=mock_user)
        save_profile(sender=User, instance=mock_user)
        
        # Assert
        assert mock_profile.save.call_count == 3
    
    def test_different_user_instances(self):
        """
        Test that saving different User instances correctly saves their respective Profiles.
        """
        # Arrange
        mock_profile1 = Mock()
        mock_user1 = Mock()
        mock_user1.profile = mock_profile1
        
        mock_profile2 = Mock()
        mock_user2 = Mock()
        mock_user2.profile = mock_profile2
        
        # Act
        save_profile(sender=User, instance=mock_user1)
        save_profile(sender=User, instance=mock_user2)
        
        # Assert
        mock_profile1.save.assert_called_once()
        mock_profile2.save.assert_called_once()
    
    def test_profile_save_exception_handling(self):
        """
        Test how the function handles exceptions raised during profile save.
        """
        # Arrange
        mock_profile = Mock()
        mock_profile.save.side_effect = Exception("Database error")
        mock_user = Mock()
        mock_user.profile = mock_profile
        
        # Act & Assert
        with pytest.raises(Exception, match="Database error"):
            save_profile(sender=User, instance=mock_user)
    
    def test_kwargs_ignored(self):
        """
        Test that additional kwargs are properly ignored by the function.
        """
        # Arrange
        mock_profile = Mock()
        mock_user = Mock()
        mock_user.profile = mock_profile
        
        # Act - pass additional kwargs that should be ignored
        save_profile(sender=User, instance=mock_user, created=True, update_fields=['username'])
        
        # Assert - function should work normally despite extra kwargs
        mock_profile.save.assert_called_once()
