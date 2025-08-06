# intent_router.py

from tools.poster_generator import generate_poster_from_intent
from tools.flowchart_builder import generate_flowchart_from_intent
from tools.task_automator import run_automation_from_intent
from tools.file_generator import generate_file_from_intent
from tools.prompt_lab import prompt_lab_from_intent
from tools.api_wrapper_gen import generate_api_wrapper_from_intent
from tools.research_assistant import research_assistant_from_intent
from tools.ui_designer import generate_ui_from_intent
from tools.code_editor import edit_code_from_intent
from tools.data_analyzer import analyze_data_from_intent


# ----------------------------------------
# Tool dispatch map
# ----------------------------------------
TOOL_DISPATCHER = {
    "poster_generator": generate_poster_from_intent,
    "flowchart_builder": generate_flowchart_from_intent,
    "task_automator": run_automation_from_intent,
    "file_generator": generate_file_from_intent,
    "prompt_lab": prompt_lab_from_intent,
    "api_wrapper_gen": generate_api_wrapper_from_intent,
    "research_assistant": research_assistant_from_intent,
    "ui_designer": generate_ui_from_intent,
    "code_editor": edit_code_from_intent,
    "data_analyzer": analyze_data_from_intent
}


# ----------------------------------------
# Main router function
# ----------------------------------------
def route_tool_intent(tool_name: str, params: dict):
    tool = TOOL_DISPATCHER.get(tool_name)
    if not tool:
        return f"❌ Unknown tool: {tool_name}"
    return tool(params)