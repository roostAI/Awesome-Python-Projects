import pytest
import os
import django
from django.conf import settings

# Configure Django settings before importing models
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'mysite.settings')
# Alternative if the above doesn't work:
# settings.configure(
#     INSTALLED_APPS=['django.contrib.auth', 'django.contrib.contenttypes', 'blog'],
#     DATABASES={'default': {'ENGINE': 'django.db.backends.sqlite3', 'NAME': ':memory:'}},
# )
django.setup()

from django.contrib.auth.models import User
from blog.models import Post


class TestPostStr:
    """Test suite for the Post.__str__ method."""

    @pytest.fixture
    def user(self):
        """Create and return a test user."""
        return User.objects.create_user(
            username='testuser',
            email='test@example.com',
            password='testpassword'
        )

    def test_str_returns_title(self, user):
        """Test that __str__ method returns the post title."""
        # Arrange
        title = "Test Post Title"
        post = Post(title=title, content="Test content", author=user)
        
        # Act
        result = str(post)
        
        # Assert
        assert result == title
        assert result == post.title

    def test_str_with_empty_title(self, user):
        """Test that __str__ method handles empty title correctly."""
        # Arrange
        post = Post(title="", content="Content with empty title", author=user)
        
        # Act
        result = str(post)
        
        # Assert
        assert result == ""
        assert result == post.title

    def test_str_with_long_title(self, user):
        """Test that __str__ method handles very long titles without truncation."""
        # Arrange
        long_title = "A" * 500  # Create a 500-character title
        post = Post(title=long_title, content="Content with long title", author=user)
        
        # Act
        result = str(post)
        
        # Assert
        assert result == long_title
        assert len(result) == 500

    def test_str_with_special_characters(self, user):
        """Test that __str__ method handles titles with special characters."""
        # Arrange
        special_title = "Title with special characters: !@#$%^&*()_+{}[]|\\:;\"'<>,.?/~"éñüç😀"
        post = Post(title=special_title, content="Content with special characters", author=user)
        
        # Act
        result = str(post)
        
        # Assert
        assert result == special_title

    def test_str_after_title_modification(self, user):
        """Test that __str__ method reflects changes to the title attribute."""
        # Arrange
        initial_title = "Initial Title"
        post = Post(title=initial_title, content="Test content", author=user)
        
        # Act & Assert - Initial title
        assert str(post) == initial_title
        
        # Modify title
        new_title = "Updated Title"
        post.title = new_title
        
        # Act & Assert - Updated title
        assert str(post) == new_title
        assert str(post) != initial_title
