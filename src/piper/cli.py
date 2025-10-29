import click
from .detect import scan as do_scan, write_report
from .report import pretty
from .deps import install_for


@click.group()
def main():
    """CLI entry point for code detection tool"""
    ...


@main.command()
@click.option("--root", default=".", help="Root directory to scan")
@click.option("--report", default=".pipeline/detection.json", help="JSON report output path")
def scan(root, report):
    """
    scan directory for code patterns and generate detection report.

    performs static analysis on codebase and outputs results in both
    JSON format and pretty-printed console output.
    """
    # run detection scan and generate reports
    detection_data = do_scan(root)
    write_report(detection_data, report)
    # display results in readable format
    pretty(detection_data)


@main.command()
@click.option("--root", default=".", help="Root directory to scan and install dependencies for")
def install(root):
    """
    Scan project and install dependencies for detected technologies.

    Automatically detects the project type and runs the appropriate
    package manager commands to install all dependencies.

    Args:
        root: Root directory path containing the project to install
    """
    # detect project configuration and tech stack
    detection_data = do_scan(root)

    # install dependencies based on the detected technologies
    install_for(detection_data, root)
