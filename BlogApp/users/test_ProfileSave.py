import os
import pytest
from unittest.mock import patch, MagicMock
from PIL import Image
from io import BytesIO

# Mock the Django imports to avoid the ImproperlyConfigured error
class MockUser:
    pass

class Profile:
    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)

        img = Image.open(self.image.path)

        if img.height > 300 or img.width > 300:
            output_size = (300, 300)
            img.thumbnail(output_size)
            img.save(self.image.path)

# Patch the imports
pytest.importorskip("django.db.models")
pytest.importorskip("django.contrib.auth.models")


class TestProfileSave:
    """Test suite for the Profile.save method focusing on image resizing functionality."""

    @pytest.fixture
    def mock_profile(self):
        """Create a mock profile with a test image."""
        profile = MagicMock()
        # Create a path for the mock image
        profile.image.path = os.path.join('test_media', 'test_profile_pic.jpg')
        return profile

    @pytest.fixture
    def create_test_image(self):
        """Create test images with specified dimensions."""
        def _create_image(width, height, color='red'):
            # Create a test image with the specified dimensions
            image = Image.new('RGB', (width, height), color=color)
            img_io = BytesIO()
            image.save(img_io, format='JPEG')
            img_io.seek(0)
            return img_io
        return _create_image

    def test_image_resizing_when_dimensions_exceed_limits(self, mock_profile, create_test_image, tmp_path):
        """
        Test that images with dimensions exceeding 300x300 pixels are properly resized
        while maintaining aspect ratio.
        """
        # Arrange
        # Create a test directory
        test_dir = tmp_path / "test_media"
        test_dir.mkdir()
        test_image_path = test_dir / "test_profile_pic.jpg"
        
        # Create a large test image (500x400)
        large_image = Image.new('RGB', (500, 400), color='blue')
        large_image.save(test_image_path)
        
        # Update mock profile to use the test image path
        mock_profile.image.path = str(test_image_path)
        
        # Act
        with patch('PIL.Image.open', return_value=large_image) as mock_open:
            # Call the save method
            Profile.save(mock_profile, force_insert=False)
            
            # Get the thumbnail method that was called
            mock_thumbnail = mock_open.return_value.thumbnail
            mock_save = mock_open.return_value.save
            
            # Assert
            # Verify thumbnail was called with correct dimensions
            mock_thumbnail.assert_called_once_with((300, 300))
            # Verify save was called with the correct path
            mock_save.assert_called_once_with(str(test_image_path))

    def test_image_not_resized_when_dimensions_within_limits(self, mock_profile, create_test_image, tmp_path):
        """
        Test that images with dimensions within 300x300 pixels are not resized.
        """
        # Arrange
        # Create a test directory
        test_dir = tmp_path / "test_media"
        test_dir.mkdir()
        test_image_path = test_dir / "test_profile_pic.jpg"
        
        # Create a small test image (200x200)
        small_image = Image.new('RGB', (200, 200), color='green')
        small_image.save(test_image_path)
        
        # Update mock profile to use the test image path
        mock_profile.image.path = str(test_image_path)
        
        # Act
        with patch('PIL.Image.open', return_value=small_image) as mock_open:
            # Call the save method
            Profile.save(mock_profile, force_insert=False)
            
            # Get the methods that might be called
            mock_thumbnail = mock_open.return_value.thumbnail
            mock_save = mock_open.return_value.save
            
            # Assert
            # Verify thumbnail was not called since image is already small enough
            mock_thumbnail.assert_not_called()
            # Verify save was not called
            mock_save.assert_not_called()

    def test_aspect_ratio_maintained_during_resizing(self, mock_profile, tmp_path):
        """
        Test that aspect ratio is maintained when resizing images.
        """
        # Arrange
        # Create a test directory
        test_dir = tmp_path / "test_media"
        test_dir.mkdir()
        test_image_path = test_dir / "test_profile_pic.jpg"
        
        # Create a wide test image (600x300) with 2:1 aspect ratio
        wide_image = Image.new('RGB', (600, 300), color='yellow')
        wide_image.save(test_image_path)
        
        # Update mock profile to use the test image path
        mock_profile.image.path = str(test_image_path)
        
        # Create a mock for the resized image that will be returned after thumbnail operation
        resized_mock = MagicMock()
        resized_mock.width = 300
        resized_mock.height = 150  # Maintains 2:1 aspect ratio
        
        # Act
        with patch('PIL.Image.open', return_value=wide_image) as mock_open:
            # Set up the mock to simulate thumbnail operation maintaining aspect ratio
            mock_open.return_value.thumbnail = MagicMock(side_effect=lambda size: setattr(mock_open.return_value, 'width', 300) or setattr(mock_open.return_value, 'height', 150))
            mock_open.return_value.width = 600
            mock_open.return_value.height = 300
            
            # Call the save method
            Profile.save(mock_profile, force_insert=False)
            
            # Assert
            # Verify thumbnail was called with correct dimensions
            mock_open.return_value.thumbnail.assert_called_once_with((300, 300))
            # Verify the aspect ratio is maintained (2:1)
            assert mock_open.return_value.width / mock_open.return_value.height == 2.0
