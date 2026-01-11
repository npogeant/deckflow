from typing import Any, Dict, List

from .content.finder import ContentFinder
from .content.registry import ContentRegistry
from .content.duplicate import DuplicateManager
from .formatters.slide_printer import SlidePrinter
from .adders.image_adder import ImageAdder

class DeckSlide:
    """Manage all content in a slide."""

    def __init__(self, slide: Any):
        self.slide = slide
        self._initialize_content()

    def _initialize_content(self) -> None:
        """Discover slide content and build the registry."""
        finder = ContentFinder()
        content = finder.find_all(self.slide)

        DuplicateManager.mark_duplicates(content["charts"])
        DuplicateManager.mark_duplicates(content["texts"])
        DuplicateManager.mark_duplicates(content["tables"])

        self.registry = ContentRegistry(
            content["charts"], content["texts"], content["tables"]
        )

    def get_duplicates(self, items: str):
        """Return items with duplicate names for the given type."""
        items_map = {
            "texts": self.registry.texts,
            "charts": self.registry.charts,
            "tables": self.registry.tables,
        }
        return DuplicateManager.get_duplicates(items_map.get(items, []))

    def list_content(self):
        """Return a summary of all detected content."""
        return SlidePrinter.print_summary(self.registry)

    def get_text(self, name: str):
        """Retrieve a text element by its name."""
        return self.registry.get_text(name)

    def get_chart(self, name: str):
        """Retrieve a chart element by its name."""
        return self.registry.get_chart(name)

    def get_table(self, name: str):
        """Retrieve a table element by its name."""
        return self.registry.get_table(name)

    def update_text(self, name: str, new_text: str, color_by_value: bool = False) -> None:
        """Update a text element with new content."""
        text_obj = self.get_text(name)
        if not text_obj:
            raise ValueError(f"Text element '{name}' not found")
        text_obj.update(new_text, color_by_value=color_by_value)

    def update_chart(self, name: str, new_data: Dict[str, Any]) -> None:
        """
        Update a chart using the provided data structure.
        
        The new_data dictionary must contain 'categories' and 'series' keys.
        """
        chart = self.get_chart(name)
        if not chart:
            raise ValueError(f"Chart '{name}' not found")

        if "categories" in new_data:
            chart.update_categories(new_data["categories"])
        if "series" in new_data:
            for series_name, values in new_data["series"].items():
                chart.update_series(series_name, values)
        chart.save_changes()

    def update_table(self, name: str, new_data: List, by_rows: bool = True, by_columns: bool = False) -> None:
        """Update a table with new data either by rows or by columns."""
        if by_rows and by_columns:
            raise ValueError("Only one of by_rows or by_columns can be True.")
        
        if not by_rows and not by_columns:
            raise ValueError("At least one of by_rows or by_columns must be True.")

        table = self.get_table(name)
        if not table:
            raise ValueError(f"Table '{name}' not found")

        if by_rows:
            for row_idx, row_data in enumerate(new_data):
                table.update_row(row_idx, row_data)
        elif by_columns:
            for col_idx, col_data in enumerate(new_data):
                table.update_column(col_idx, col_data)

    def add_image_from_text(self, text_name: str, image_path: str, keep_height: bool = True, keep_width: bool = False) -> None:
        """Add an image to the slide positioned at a text element's location."""
        text_element = self.get_text(text_name)
        if not text_element:
            raise ValueError(f"Text element '{text_name}' not found")
        
        success = ImageAdder.add_image_from_text(
            self.slide, text_element, image_path, keep_height, keep_width
        )
        if not success:
            raise RuntimeError(f"Failed to add image at text element '{text_name}'")