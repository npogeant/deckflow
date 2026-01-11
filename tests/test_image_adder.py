"""Tests for image adder functionality."""

import tempfile
import os
from PIL import Image

from deckflow.adders.image_adder import ImageAdder


class FakeShape:
    """Fake shape object for tests."""
    def __init__(self, width=100, height=100, left=0, top=0):
        self.width = width
        self.height = height
        self.left = left
        self.top = top


class FakeTextElement:
    """Fake text element for tests."""
    def __init__(self, shape):
        self.shape = shape
        self.name = "TextElement"


class FakeSlide:
    """Fake slide object for tests."""
    def __init__(self):
        self.shapes = FakeShapes()


class FakeShapes:
    """Fake shapes collection for tests."""
    def __init__(self):
        self.pictures = []
    
    def add_picture(self, image_path, left, top, width, height):
        """Fake add_picture method that records the call."""
        self.pictures.append({
            'path': image_path,
            'left': left,
            'top': top,
            'width': width,
            'height': height
        })
        return None


def create_test_image(width=200, height=150):
    """Create a temporary test image."""
    img = Image.new('RGB', (width, height), color='red')
    temp_file = tempfile.NamedTemporaryFile(delete=False, suffix='.png')
    img.save(temp_file.name)
    temp_file.close()
    return temp_file.name


def test_add_image_from_text_keep_height():
    """Test adding an image keeping the text element's height."""
    # Create test image and fake objects
    image_path = create_test_image(width=400, height=200)
    
    try:
        shape = FakeShape(width=100, height=100, left=50, top=50)
        text_element = FakeTextElement(shape)
        slide = FakeSlide()
        
        # Add image keeping height
        result = ImageAdder.add_image_from_text(
            slide, text_element, image_path, keep_height=True, keep_width=False
        )
        
        assert result is True
        assert len(slide.shapes.pictures) == 1
        
        picture = slide.shapes.pictures[0]
        assert picture['height'] == 100  # Kept from text shape
        # Width should be calculated based on aspect ratio: (400/200) * 100 = 200
        assert picture['width'] == 200
        
    finally:
        os.remove(image_path)


def test_add_image_from_text_keep_width():
    """Test adding an image keeping the text element's width."""
    image_path = create_test_image(width=400, height=200)
    
    try:
        shape = FakeShape(width=100, height=100, left=50, top=50)
        text_element = FakeTextElement(shape)
        slide = FakeSlide()
        
        # Add image keeping width
        result = ImageAdder.add_image_from_text(
            slide, text_element, image_path, keep_height=False, keep_width=True
        )
        
        assert result is True
        assert len(slide.shapes.pictures) == 1
        
        picture = slide.shapes.pictures[0]
        assert picture['width'] == 100  # Kept from text shape
        # Height should be calculated based on aspect ratio: (200/400) * 100 = 50
        assert picture['height'] == 50
        
    finally:
        os.remove(image_path)


def test_add_image_from_text_keep_both():
    """Test adding an image keeping both dimensions of the text element."""
    image_path = create_test_image(width=400, height=200)
    
    try:
        shape = FakeShape(width=100, height=100, left=50, top=50)
        text_element = FakeTextElement(shape)
        slide = FakeSlide()
        
        # Add image keeping both dimensions
        result = ImageAdder.add_image_from_text(
            slide, text_element, image_path, keep_height=True, keep_width=True
        )
        
        assert result is True
        assert len(slide.shapes.pictures) == 1
        
        picture = slide.shapes.pictures[0]
        assert picture['width'] == 100
        assert picture['height'] == 100
        
    finally:
        os.remove(image_path)


def test_add_image_from_text_centered():
    """Test that the image is centered on the text element."""
    image_path = create_test_image(width=400, height=200)
    
    try:
        # Text shape at (50, 50) with size (100, 100)
        # Center should be at (100, 100)
        shape = FakeShape(width=100, height=100, left=50, top=50)
        text_element = FakeTextElement(shape)
        slide = FakeSlide()
        
        result = ImageAdder.add_image_from_text(
            slide, text_element, image_path, keep_height=True, keep_width=False
        )
        
        assert result is True
        picture = slide.shapes.pictures[0]
        
        # Image dimensions: width=200, height=100
        # Center at (100, 100), so left = 100 - 200/2 = 0, top = 100 - 100/2 = 50
        assert picture['left'] == 0
        assert picture['top'] == 50
        
    finally:
        os.remove(image_path)


def test_add_image_from_text_invalid_path():
    """Test adding an image with an invalid path."""
    shape = FakeShape(width=100, height=100, left=50, top=50)
    text_element = FakeTextElement(shape)
    slide = FakeSlide()
    
    # Try to add image with non-existent path
    result = ImageAdder.add_image_from_text(
        slide, text_element, '/invalid/path/image.png', keep_height=True
    )
    
    assert result is False
    assert len(slide.shapes.pictures) == 0
