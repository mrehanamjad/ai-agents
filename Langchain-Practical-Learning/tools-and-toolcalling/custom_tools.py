from datetime import datetime
from typing import List
from langchain_core.tools import tool, BaseTool
from langchain_community.agent_toolkits.base import BaseToolkit

# --- Define Individual Tools ---

@tool
def get_current_time() -> str:
    """Returns the current local time in HH:MM:SS format."""
    return datetime.now().strftime("%H:%M:%S")

@tool
def get_current_date() -> str:
    """Returns today's date in YYYY-MM-DD format."""
    return datetime.now().strftime("%Y-%m-%d")

@tool
def get_current_day() -> str:
    """Returns the name of the current day of the week (e.g., Monday)."""
    return datetime.now().strftime("%A")

@tool
def get_current_timezone() -> str:
    """Returns the local system timezone name."""
    return datetime.now().astimezone().tzname() or "UTC"

# --- Define the Toolkit ---

class TemporalToolkit(BaseToolkit):
    """A toolkit for providing current temporal information (date, time, day)."""

    def get_tools(self) -> List[BaseTool]:
        """Return the list of tools in the toolkit."""
        return [
            get_current_time, 
            get_current_date, 
            get_current_day, 
            get_current_timezone
        ]
