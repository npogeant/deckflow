from collections import Counter
from typing import List, Dict

class DuplicateManager:
    """Manages duplicate detection and marking."""
    
    @staticmethod
    def mark_duplicates(items : List[Dict]):
        """Mark items with duplicate names."""
        counts = Counter(item['name'] for item in items)
        duplicates = {name for name, count in counts.items() if count > 1}
        
        for item in items:
            item['is_duplicated'] = "yes" if item['name'] in duplicates else "no"
    
    @staticmethod
    def get_duplicates(items : List[Dict]) -> Dict[str, int]:
        """Get dictionary of duplicate names and their counts."""
        return dict(Counter([
            item['name'] for item in items 
            if item['is_duplicated'] == "yes"
        ]))
    
    @staticmethod
    def has_duplicates(items: List[Dict], name: str) -> bool:
        """Check if a specific name has duplicates."""
        duplicates = DuplicateManager.get_duplicates(items)
        return name in duplicates