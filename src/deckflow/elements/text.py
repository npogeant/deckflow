from typing import Any

from ..content.text_extractor import extract_text
from ..formatters.color_analyzer import ColorAnalyzer
from ..formatters.font_properties import copy_font_properties
from ..updaters.text_updater import TextUpdater

class DeckText:
    """Class to manage an individual PowerPoint text element."""

    def __init__(self, shape: Any, name: str):
        """
        Initialize with a PowerPoint text shape object
        
        Args:
            shape: python-pptx Shape object
            name: Shape name extracted
        """
        self.shape = shape
        self.name = name
        self.original_content = extract_text(shape)
        self.current_content = self.original_content
        self.color_by_value = False
        self._updater = TextUpdater(ColorAnalyzer, copy_font_properties)

    def get_content(self):
        return self.current_content

    def get_original_content(self):
        return self.original_content

    def update(self, new_text: str, color_by_value: bool = False):
        self.current_content = str(new_text)
        self.color_by_value = color_by_value

        if self.current_content == self.original_content:
            print(f"No changes to save for shape {self.name}")
            return True

        try:
            if getattr(self.shape, "has_text_frame", False):
                self._updater.update_text_frame(self.shape.text_frame, self.current_content, color_by_value=self.color_by_value)
            elif hasattr(self.shape, "text"):
                self.shape.text = self.current_content
            else:
                print(f"Text {self.name} has no text support")
                return False
            print(f"Text updated for {self.name}")
            return True
        except Exception as e:
            print(f"Error updating text {self.name}: {e}")
            return False