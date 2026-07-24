import logging
from typing import Any

logger = logging.getLogger(__name__)

def extract_text(shape: Any) -> str:
    """ Extract text data safely from a pptx shape."""
    try:
        if hasattr(shape, "text") and isinstance(shape.text, str):
            return shape.text
        if getattr(shape, "has_text_frame", False):
            parts = [p.text for p in shape.text_frame.paragraphs]
            return "\n".join(parts)
        return ""
    except Exception:
        logger.exception("Error extracting text")
        return ""