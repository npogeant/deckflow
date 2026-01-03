from typing import Any, List

def extract_table_data(table: Any) -> List[List[str]]:
    """ 
    Extract table data safely from a pptx table object.
    
    Returns:
        List: 2D list containing all cell text values
    """
    data = []
    try:
        for row in table.rows:
            row_data = []
            for cell in row.cells:
                row_data.append(cell.text)
            data.append(row_data)
    except Exception as e:
        print(f"Error extracting table data: {e}")
    
    return data