import pytest
from django.test import TestCase
from django.contrib.auth.models import User
from django.utils import timezone
from django.conf import settings
from django.apps import apps

# Configure Django settings before importing models
settings.configure(
    INSTALLED_APPS=[
        'django.contrib.auth',
        'django.contrib.contenttypes',
        'django.contrib.sessions',
        'django.contrib.admin',
        'blog',
    ],
    DATABASES={
        'default': {
            'ENGINE': 'django.db.backends.sqlite3',
            'NAME': ':memory:',
        }
    }
)
apps.populate(settings.INSTALLED_APPS)

# Now import the Post model after Django is configured
from blog.models import Post

class TestPostStr(TestCase):
    """Test suite for the Post.__str__ method."""
    
    def setUp(self):
        """Set up test data."""
        self.user = User.objects.create_user(
            username='testuser',
            email='test@example.com',
            password='testpassword'
        )
        
    def test_str_returns_title(self):
        """Test that __str__ method returns the post title."""
        # Arrange
        title = "Test Post Title"
        post = Post(
            title=title,
            content="Test content",
            author=self.user,
            date_posted=timezone.now()
        )
        
        # Act
        result = str(post)
        
        # Assert
        assert result == title, f"Expected '{title}', but got '{result}'"
        
    def test_str_with_empty_title(self):
        """Test that __str__ method handles empty title correctly."""
        # Arrange
        post = Post(
            title="",
            content="Test content with empty title",
            author=self.user,
            date_posted=timezone.now()
        )
        
        # Act
        result = str(post)
        
        # Assert
        assert result == "", f"Expected empty string, but got '{result}'"
        
    def test_str_with_special_characters(self):
        """Test that __str__ method handles titles with special characters."""
        # Arrange
        title = "Special Characters: !@#$%^&*()"
        post = Post(
            title=title,
            content="Content with special characters in title",
            author=self.user,
            date_posted=timezone.now()
        )
        
        # Act
        result = str(post)
        
        # Assert
        assert result == title, f"Expected '{title}', but got '{result}'"
