from typing import Any

class TablePrinter:
    """Formats and prints table rows and columns data."""
    
    @staticmethod
    def print_data(table: Any):
        """Display table data in a readable format."""
        print(f"📋 Table {table.name} ({table.rows}x{table.cols}):")
        
        # Calculate column widths for better formatting
        col_widths = [0] * table.cols
        for row in table.data:
            for col_idx, cell in enumerate(row):
                col_widths[col_idx] = max(col_widths[col_idx], len(str(cell)))
        
        # Print table with proper alignment
        for row_idx, row in enumerate(table.data):
            row_str = "  | "
            for col_idx, cell in enumerate(row):
                row_str += str(cell).ljust(col_widths[col_idx]) + " | "
            print(row_str)
            
            # Print separator after header row
            if row_idx == 0:
                separator = "  +" + "+".join(["-" * (w + 2) for w in col_widths]) + "+"
                print(separator)