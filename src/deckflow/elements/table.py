from typing import Any

from ..content.table_extractor import extract_table_data
from ..updaters.table_updater import TableUpdater
from ..formatters.table_printer import TablePrinter

class DeckTable:
    """Class to manage an individual PowerPoint table."""
    
    def __init__(self, table: Any, name: str):
        """
        Initialize with a PowerPoint table object
        
        Args:
            table: python-pptx Table object
            name: Table name extracted
        """
        self.table = table
        self.name = name
        self.rows = len(table.rows)
        self.cols = len(table.columns)
        self.data = extract_table_data(table)
        self.original_data = [row[:] for row in self.data]
        self._updater = TableUpdater(self)
    
    def get_data(self) -> list[list[str]]:
        return [row[:] for row in self.data]
    
    def get_cell(self, row: int, col: int) -> str | None:
        if 0 <= row < self.rows and 0 <= col < self.cols:
            return self.data[row][col]
        else:
            print(f"Invalid cell indices ({row}, {col}). Table size: {self.rows}x{self.cols}")
            return None
    
    def get_row(self, row_index: int) -> list[str] | None:
        if 0 <= row_index < self.rows:
            return self.data[row_index][:]
        else:
            print(f"Invalid row index {row_index}. Table has {self.rows} rows")
            return None
    
    def get_column(self, col_index: int) -> list[str] | None:
        if 0 <= col_index < self.cols:
            return [row[col_index] for row in self.data]
        else:
            print(f"Invalid column index {col_index}. Table has {self.cols} columns")
            return None
        
    def update_cell(self, row: int, col: int, value: str):
        self._updater.update_cell(row, col, value)
        return self._updater.save_changes()
    
    def update_row(self, row_index: int, values: list[str]):
        self._updater.update_row(row_index, values)
        return self._updater.save_changes()
    
    def update_column(self, col_index: int, values: list[str]):
        self._updater.update_column(col_index, values)
        return self._updater.save_changes()
    
    def show_data(self):
        return TablePrinter.print_data(self)