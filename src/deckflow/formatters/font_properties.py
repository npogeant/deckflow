from typing import Any

def copy_font_properties(source_font: Any, target_font: Any):
    """Copy font properties while tolerating missing attributes."""

    try:
        if getattr(source_font, "name", None):
            target_font.name = source_font.name
        if getattr(source_font, "size", None):
            target_font.size = source_font.size
        if getattr(source_font, "bold", None) is not None:
            target_font.bold = source_font.bold
        if getattr(source_font, "italic", None) is not None:
            target_font.italic = source_font.italic

        try:
            if getattr(source_font.color, "rgb", None):
                target_font.color.rgb = source_font.color.rgb
            elif getattr(source_font.color, "theme_color", None) is not None:
                target_font.color.theme_color = source_font.color.theme_color
                if hasattr(source_font.color, "brightness") and source_font.color.brightness is not None:
                    target_font.color.brightness = source_font.color.brightness
        except Exception:
            pass
    except Exception as e:
        print(f"Warning: Could not copy some font properties: {e}")