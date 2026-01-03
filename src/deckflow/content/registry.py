from typing import Any, List, Dict, Optional


class ContentRegistry:
    """Registry for managing slide content items."""
    
    def __init__(self, charts: List[Dict[str, Any]], texts: List[Dict[str, Any]], tables: List[Dict[str, Any]]):
        self.charts = charts
        self.texts = texts
        self.tables = tables
    
    def get_item_by_name(self, items: List[Dict[str, Any]], name: str, item_type: str) -> Optional[Dict[str, Any]]:
        """Generic method to get an item by name with duplicate checking."""
        from .duplicate import DuplicateManager
        
        if DuplicateManager.has_duplicates(items, name):
            print(f"{name} has duplicates!")
            return None
        
        item = next((item for item in items if item['name'] == name), None)
        if item is None:
            print(f"No {item_type} found with this name")
            return None
        
        return item
    
    def get_text(self, name: str):
        """Get a text object by name."""
        item = self.get_item_by_name(self.texts, name, "text")
        return item['text_obj'] if item else None
    
    def get_chart(self, name: str):
        """Get a chart object by name."""
        item = self.get_item_by_name(self.charts, name, "chart")
        return item['chart_obj'] if item else None
    
    def get_table(self, name: str):
        """Get a table object by name."""
        item = self.get_item_by_name(self.tables, name, "table")
        return item['table_obj'] if item else None
    
    def count_duplicates(self, content_type: str) -> int:
        """Count duplicates for a specific content type."""
        items = getattr(self, content_type)
        return len([item for item in items if item['is_duplicated'] == 'yes'])