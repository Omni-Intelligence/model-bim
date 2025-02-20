import logging
import os
from tkinter import messagebox, simpledialog
from app.file_handler import FileHandler
from app.ai_analyzer import AIAnalyzer


class Controller:
    def __init__(self, file_handler=None, ai_analyzer=None):
        self.file_handler = file_handler or FileHandler()
        self.ai_analyzer = ai_analyzer or AIAnalyzer()

    def check_env_file(self):
        if not os.path.exists(".env"):
            api_key = simpledialog.askstring(
                "API Key", "Please enter your OpenAI API key:"
            )
            if api_key:
                with open(".env", "w") as f:
                    f.write(f"OPENAI_API_KEY={api_key}")
            else:
                messagebox.showerror(
                    "Error", "OpenAI API key is required to use this application."
                )
                return False

        return True

    def process_file(self, file_path):
        # Validate file
        if not self.file_handler.is_valid_file_type(file_path):
            messagebox.showerror("Error", "Unsupported file type")
            return None

        # Read file content
        content = self.file_handler.read_file(file_path)
        if not content:
            return None

        # Initialize results dictionary
        results = {}

        # Process each analysis task
        for task_name, task in self.analysis_tasks().items():
            if content:
                try:
                    results[task_name] = self.ai_analyzer.analyze(task, content)
                except Exception as e:
                    logging.getLogger("app").error(
                        f"Error processing task {task_name}: {str(e)}"
                    )
                    results[task_name] = f"Analysis failed: {str(e)}"

        return results if results else None

    @staticmethod
    def analysis_tasks():
        return {
            "general_analysis": "Analyze the overall Power BI file structure and components",
            "model_analysis": "Analyze the data model structure and relationships",
            "dax_analysis": "Review and analyze DAX expressions and calculations",
            "performance_analysis": "Identify potential performance bottlenecks",
        }

    def reset(self):
        # Reset any state if needed
        pass
