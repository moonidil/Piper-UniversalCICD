import click
from typing import Any, Dict, cast

from .detect import scan as do_scan, write_report
from .report import pretty
from .deps import install_for


@click.group()
def main() -> None:
    """CLI entry point for code detection tool"""
    ...


@main.command()
@click.option("--root", default=".", help="Root directory to scan")
@click.option("--report", default=".pipeline/detection.json", help="JSON report output path")
def scan(root: str, report: str) -> None:
    """
    scan directory for code patterns and generate detection report.

    performs static analysis on codebase and outputs results in both
    JSON format and pretty-printed console output.
    """
    # run detection scan and generate reports
    detection_data = do_scan(root)
    write_report(detection_data, report)
    pretty(cast(Dict[str, Any], detection_data))


@main.command()
@click.option("--root", default=".", help="Root directory to scan and install dependencies for")
def install(root: str) -> None:
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
    install_for(cast(Dict[str, Any], detection_data), root)
