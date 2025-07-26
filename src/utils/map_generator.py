"""
Map generation utilities for the Antarctic Iceberg Tracker.
"""

import os

from templates.map_template import get_map_html_template

from .data_handler import get_data_file_path


def generate_map():
    """Generate a simple interactive map."""
    data_file = get_data_file_path()

    if not os.path.exists(data_file):
        print("No data file found. Run 'python main.py scrape' first.")
        return False

    print("Generating professional interactive map...")

    try:
        # Get the project root and create output directory
        project_root = os.path.dirname(
            os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        )
        output_dir = os.path.join(project_root, "output")

        # Create output directory if it doesn't exist
        if not os.path.exists(output_dir):
            os.makedirs(output_dir)

        # Get HTML template
        html_content = get_map_html_template()

        # Write to file
        output_file = os.path.join(output_dir, "iceberg_map.html")
        with open(output_file, "w") as f:
            f.write(html_content)

        print(f"Interactive map generated: {output_file}")
        print("Open output/iceberg_map.html in your browser to view the map")
        return True

    except Exception as e:
        print(f"Error generating map: {e}")
        return False
