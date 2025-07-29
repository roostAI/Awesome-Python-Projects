import pytest
from django.test import RequestFactory, TestCase
from django.conf import settings
from django.test import override_settings
from django.template.response import TemplateResponse
from unittest.mock import patch, MagicMock

# Mock the render function to avoid Django settings configuration issues
@pytest.fixture
def mock_render():
    with patch('blog.views.render') as mock_render:
        # Configure the mock to return a TemplateResponse with context data
        mock_response = MagicMock(spec=TemplateResponse)
        mock_response.status_code = 200
        mock_response.templates = [MagicMock(name='blog/about.html')]
        mock_response.context_data = {'title': 'About'}
        
        mock_render.return_value = mock_response
        yield mock_render

class ViewsAbout(TestCase):
    """Test suite for the about view function."""
    
    def test_about_page_renders_with_correct_template(self, mock_render):
        """
        Test that the about function renders the correct template when called.
        """
        # Import here to use the mocked render function
        from blog.views import about
        
        # Arrange
        factory = RequestFactory()
        request = factory.get('/about/')
        
        # Act
        response = about(request)
        
        # Assert
        assert response.status_code == 200
        assert 'blog/about.html' in [template.name for template in response.templates]
        assert response.context_data['title'] == 'About'
        
        # Verify render was called with correct arguments
        mock_render.assert_called_once_with(request, 'blog/about.html', {'title': 'About'})
    
    def test_about_page_context_contains_title(self, mock_render):
        """
        Test that the about function includes the correct title in the context.
        """
        # Import here to use the mocked render function
        from blog.views import about
        
        # Arrange
        factory = RequestFactory()
        request = factory.get('/about/')
        
        # Act
        response = about(request)
        
        # Assert
        assert 'title' in response.context_data
        assert response.context_data['title'] == 'About'
        
        # Verify render was called with correct arguments
        mock_render.assert_called_once_with(request, 'blog/about.html', {'title': 'About'})
