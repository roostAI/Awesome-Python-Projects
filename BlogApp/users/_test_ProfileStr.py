import pytest
from unittest.mock import Mock, patch

class TestProfileStr:
    """Test suite for the Profile.__str__ method."""

    @patch('django.conf.settings.configure')
    def test_profile_string_representation(self, mock_configure):
        """
        Test that the __str__ method returns the expected string format.
        """
        # Import Profile after configuring Django settings
        from users.models import Profile
        
        # Arrange
        # Create a mock user with a username
        mock_user = Mock()
        mock_user.username = "testuser"
        
        # Create a profile instance with the mock user
        profile = Profile()
        profile.user = mock_user
        
        # Act
        result = profile.__str__()
        
        # Assert
        expected = "testuser Profile"
        assert result == expected, f"Expected '{expected}', but got '{result}'"
        
    @patch('django.conf.settings.configure')
    def test_profile_string_with_special_characters(self, mock_configure):
        """
        Test that the __str__ method handles usernames with special characters.
        """
        # Import Profile after configuring Django settings
        from users.models import Profile
        
        # Arrange
        mock_user = Mock()
        mock_user.username = "user@123_!#"
        
        profile = Profile()
        profile.user = mock_user
        
        # Act
        result = profile.__str__()
        
        # Assert
        expected = "user@123_!# Profile"
        assert result == expected, f"Expected '{expected}', but got '{result}'"
        
    @patch('django.conf.settings.configure')
    def test_profile_string_with_empty_username(self, mock_configure):
        """
        Test that the __str__ method handles empty usernames gracefully.
        """
        # Import Profile after configuring Django settings
        from users.models import Profile
        
        # Arrange
        mock_user = Mock()
        mock_user.username = ""
        
        profile = Profile()
        profile.user = mock_user
        
        # Act
        result = profile.__str__()
        
        # Assert
        expected = " Profile"  # Note the space before "Profile"
        assert result == expected, f"Expected '{expected}', but got '{result}'"
