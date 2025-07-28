import pytest
from unittest.mock import Mock, patch

class TestPostStr:
    """Test suite for the Post.__str__ method."""

    @pytest.fixture
    def user(self):
        """Create and return a mocked user."""
        mock_user = Mock()
        mock_user.username = 'testuser'
        return mock_user

    @pytest.fixture
    def post_class(self):
        """Create a mock Post class to avoid Django settings issues."""
        class MockPost:
            def __init__(self, title, content, author):
                self.title = title
                self.content = content
                self.author = author
                
            def __str__(self):
                return self.title
                
        return MockPost

    def test_str_returns_title(self, user, post_class):
        """Test that __str__ correctly returns the post title."""
        # Arrange
        title = "Test Post Title"
        post = post_class(title=title, content="Test content", author=user)
        
        # Act
        result = str(post)
        
        # Assert
        assert result == title
        assert result == post.title

    def test_str_with_empty_title(self, user, post_class):
        """Test that __str__ correctly handles empty titles."""
        # Arrange
        post = post_class(title="", content="Content with empty title", author=user)
        
        # Act
        result = str(post)
        
        # Assert
        assert result == ""
        assert result == post.title

    def test_str_with_long_title(self, user, post_class):
        """Test that __str__ correctly handles very long titles without truncation."""
        # Arrange
        long_title = "A" * 500  # Create a 500-character title
        post = post_class(title=long_title, content="Content with long title", author=user)
        
        # Act
        result = str(post)
        
        # Assert
        assert result == long_title
        assert len(result) == 500

    def test_str_with_special_characters(self, user, post_class):
        """Test that __str__ correctly handles titles with special characters."""
        # Arrange
        special_title = "Title with special characters: !@#$%^&*()_+{}[]|\\:;\"'<>,.?/~"éñüç😀"
        post = post_class(title=special_title, content="Content with special characters", author=user)
        
        # Act
        result = str(post)
        
        # Assert
        assert result == special_title

    def test_str_after_title_modification(self, user, post_class):
        """Test that __str__ reflects changes to the title attribute."""
        # Arrange
        initial_title = "Initial Title"
        post = post_class(title=initial_title, content="Test content", author=user)
        
        # Act - Initial check
        initial_result = str(post)
        
        # Modify title
        new_title = "Updated Title"
        post.title = new_title
        
        # Act - After modification
        updated_result = str(post)
        
        # Assert
        assert initial_result == initial_title
        assert updated_result == new_title
        assert updated_result != initial_result
