from typing import Any
from PIL import Image

class ImageAdder:
    """Adder for adding images to slides."""

    @staticmethod
    def add_image_from_text(slide: Any, text_element: Any, image_path: str, keep_height: bool = True, keep_width: bool = False) -> bool:
        """
        Add an image to the slide positioned at a text element's location.
        
        Args:
            slide: python-pptx Slide object
            text_element: DeckText element
            image_path: Path to the image file
            keep_height: Keep the text element's height
            keep_width: Keep the text element's width
        """
        try:
            text_shape = text_element.shape
                         
            # Determine if we keep both dimensions
            keep_both = keep_height and keep_width
            
            # Get the center of the text shape on the slide
            center_x = text_shape.left + text_shape.width // 2
            center_y = text_shape.top + text_shape.height // 2
            
            # Open the image to get its size
            with Image.open(image_path) as img:
                img_width, img_height = img.size
            
            # Determine new width and height
            if keep_both:
                width = text_shape.width
                height = text_shape.height
            elif keep_height:
                height = text_shape.height
                width = int((img_width / img_height) * height)
            elif keep_width:
                width = text_shape.width
                height = int((img_height / img_width) * width)
            
            # Calculate new left and top to center the image
            left = center_x - width // 2
            top = center_y - height // 2
            
            # Add the image to the slide
            slide.shapes.add_picture(image_path, left=left, top=top, width=width, height=height)
            return True
            
        except Exception as e:
            print(f"Error adding image: {e}")
            return False
