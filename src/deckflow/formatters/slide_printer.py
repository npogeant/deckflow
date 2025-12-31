from typing import Any

class SlidePrinter:
    """Formats and prints slide content information."""
    
    @staticmethod
    def print_summary(registry: Any) -> dict[str, int]:
        """Print content summary."""
        charts_count = len(registry.charts)
        texts_count = len(registry.texts)
        tables_count = len(registry.tables)
        text_duplicates = registry.count_duplicates('texts')
        
        print(f"📊 SLIDE CONTENT SUMMARY:")
        print(f"  📈 {charts_count} chart(s) found")
        
        duplicate_msg = f" \033[31m{text_duplicates} duplicates\033[0m" if text_duplicates > 1 else ""
        print(f"  📄 {texts_count} text shape(s) found{duplicate_msg}")
        print(f"  📋 {tables_count} table(s) found")
        
        if registry.charts:
            SlidePrinter._print_charts(registry.charts)
        if registry.texts:
            SlidePrinter._print_texts(registry.texts)
        if registry.tables:
            SlidePrinter._print_tables(registry.tables)
        
        return {
            'charts': charts_count,
            'texts': texts_count,
            'tables': tables_count
        }
    
    @staticmethod
    def _print_charts(charts: list[dict[str, Any]]):
        print(f"\n📈 CHARTS:")
        for chart_info in charts:
            chart_name = chart_info['name']
            print(f"  \033[1m{chart_name}\033[0;0m.")
    
    @staticmethod
    def _print_texts(texts: list[dict[str, Any]]):
        print(f"\n📄 TEXT SHAPES:")
        for text_info in texts:
            text_obj = text_info['text_obj']
            text_name = text_info['name']
            content = text_obj.get_content()
            preview = content[:50] + ('...' if len(content) > 50 else '')
            print(f"  \033[1m{text_name}\033[0;0m.: '{preview}'")
    
    @staticmethod
    def _print_tables(tables: list[dict[str, Any]]):
        print(f"\n📋 TABLES:")
        for table_info in tables:
            table_obj = table_info['table_obj']
            table_name = table_info['name']
            print(f"  \033[1m{table_name}\033[0;0m. Table: {table_obj.rows}x{table_obj.cols}")