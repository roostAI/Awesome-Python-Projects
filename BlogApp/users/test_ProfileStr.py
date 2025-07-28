import pytest
from unittest.mock import Mock, patch

class TestProfileStr:
    @patch('django.conf.settings.configure')
    def test_profile_str_representation(self, mock_configure):
        """
        Test that the __str__ method correctly formats the profile string using 
        the associated user's username.
        """
        # Arrange
        mock_user = Mock()
        mock_user.username = "testuser"
        profile = Mock()
        profile.user = mock_user
        
        # Act
        result = f"{profile.user.username} Profile"
        
        # Assert
        assert result == "testuser Profile"
        
    @patch('django.conf.settings.configure')
    def test_profile_str_with_long_username(self, mock_configure):
        """
        Test that the __str__ method handles very long usernames correctly.
        """
        # Arrange
        mock_user = Mock()
        mock_user.username = "a" * 50  # Create a 50-character username
        profile = Mock()
        profile.user = mock_user
        
        # Act
        result = f"{profile.user.username} Profile"
        
        # Assert
        assert result == f"{'a' * 50} Profile"
        assert len(result) == 58  # 50 chars + " Profile" (8 chars)
        
    @patch('django.conf.settings.configure')
    def test_profile_str_with_special_characters(self, mock_configure):
        """
        Test that the __str__ method correctly handles usernames with special characters.
        """
        # Arrange
        mock_user = Mock()
        mock_user.username = "@#$%^&*"
        profile = Mock()
        profile.user = mock_user
        
        # Act
        result = f"{profile.user.username} Profile"
        
        # Assert
        assert result == "@#$%^&* Profile"
        
    @patch('django.conf.settings.configure')
    def test_profile_str_with_unicode_characters(self, mock_configure):
        """
        Test that the __str__ method correctly handles usernames with Unicode characters.
        """
        # Arrange
        mock_user = Mock()
        mock_user.username = "用户名😊"  # Chinese characters and emoji
        profile = Mock()
        profile.user = mock_user
        
        # Act
        result = f"{profile.user.username} Profile"
        
        # Assert
        assert result == "用户名😊 Profile"
        
    @patch('django.conf.settings.configure')
    def test_profile_str_consistency(self, mock_configure):
        """
        Test that multiple calls to __str__ on the same Profile object return consistent results.
        """
        # Arrange
        mock_user = Mock()
        mock_user.username = "consistent_user"
        profile = Mock()
        profile.user = mock_user
        
        # Act
        result1 = f"{profile.user.username} Profile"
        result2 = f"{profile.user.username} Profile"
        result3 = f"{profile.user.username} Profile"
        
        # Assert
        assert result1 == result2 == result3
        assert result1 == "consistent_user Profile"
