from rich.console import Console
from rich.table import Table


def pretty(detection: dict):
    """
    display detection results in a formatted table using Rich library

    creates a visually appealing console output showing the detected
    project configuration including types, framework, and deployment target

    Args:
        detection: dictionary containing detection results from scan()
    """
    console = Console()

    # initialise table with title and columns
    table = Table(title="Piper Detection Report")
    table.add_column("Key")
    table.add_column("Value")

    # add rows for each detection category with fallback for missing values
    table.add_row("Types", ", ".join(detection.get("types", [])) or "-")
    table.add_row("Framework", detection.get("framework") or "-")
    table.add_row("Deploy", detection.get("deploy") or "-")

    # render the table to console
    console.print(table)
