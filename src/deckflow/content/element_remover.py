from typing import Any

from pptx.shapes.base import BaseShape

class ElementRemover:
    """Method to remove elements from PowerPoint slides."""
    
    @staticmethod
    def remove_shape(shape: Any) -> bool:
        """
        Remove a shape from the slide.
        
        Args:
            shape: Shape object to remove
            
        Returns:
            True if removal was successful, False otherwise
        """
        try:
            # GraphicFrame (tables, charts) doesn't have _sp, use _element instead
            if hasattr(shape, '_element'):
                sp = shape._element
            elif hasattr(shape, '_sp'):
                sp = shape._sp
            else:
                return False
            
            sp.getparent().remove(sp)
            return True
        except Exception:
            return False