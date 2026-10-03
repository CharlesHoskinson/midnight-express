"""Refresh repair evidence in the checked-in coverage table without reading another workspace."""
from pathlib import Path
import runpy
runpy.run_path(str(Path(__file__).with_name("update_repair_reports.py")), run_name="__main__")
