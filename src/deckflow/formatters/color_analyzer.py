from typing import Optional, Tuple
import re

class ColorAnalyzer:
    """Analyze a line of text and return an RGB color if it contains a numeric value."""

    @staticmethod
    def get_color_for_value(text: str) -> Optional[Tuple[int, int, int]]:
        try:
            numbers = re.findall(r'-?\d+(?:\.\d+)?', text.replace(',', '').replace(' ', ''))
            if not numbers:
                return None
            value = float(numbers[0])
            if value > 0:
                return (0, 128, 0)      # green
            if value < 0:
                return (192, 0, 0)      # red
            return (0, 0, 0)           # black for 0
        except Exception:
            return None