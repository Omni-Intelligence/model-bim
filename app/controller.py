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
        if not self.file_handler.is_valid_file_type(file_path):
            messagebox.showerror("Error", "Unsupported file type")
            return None

        content = self.file_handler.read_file(file_path)
        if not content:
            return None

        def process_tasks():
            for task_name, task in self.analysis_tasks().items():
                if content:
                    try:
                        formatTask = "\nAvoid generating Table of Contents. Please respond with proper well-structured Markdown format."
                        result = self.ai_analyzer.analyze(task + formatTask, content)
                        yield task_name, result
                    except Exception as e:
                        logging.getLogger("app").error(
                            f"Error processing task {task_name}: {str(e)}"
                        )
                        yield task_name, f"Analysis failed: {str(e)}"

        return process_tasks()

    @staticmethod
    def analysis_tasks():
        return {
            "general": "Analyze the overall Power BI data model (.bim file), identifying its structure, key components, and metadata to provide an overview of the model’s complexity and purpose. Title the report as General Analysis.",
            "model": "Examine the data model structure, including tables, columns, relationships, and hierarchies, identifying potential design improvements and documenting key insights for better understanding. Title the report as Model Analysis",
            "dax": "Analyze and improve DAX measures by identifying redundant or inefficient calculations, suggesting optimizations, and providing alternative expressions that enhance performance and readability. Title the report as DAX Analysis.",
            "dictionary": "Generate a structured data dictionary for the Power BI model, including descriptions of tables, columns, and measures. Explain the purpose of each field and document key business logic, such as how calculations are performed and what assumptions are applied. Title the report as Data Documentation & Dictionary",
            "performance": "Detect and diagnose performance bottlenecks within the data model, including inefficient DAX calculations, high cardinality columns, complex relationships, or excessive calculated columns. Provide practical recommendations such as indexing strategies, aggregations, measure optimizations, and best practices for reducing query execution time. Title the report as Performance Analysis",
            "missing": "Identify gaps in the current model, such as missing relationships, unreferenced tables, underutilized fields, or opportunities for additional calculated measures that could improve reporting and analysis. Title the report as Missing Data Analysis",
            "report_ideas": "Suggest potential report and dashboard enhancements based on the existing model, including new KPIs, visualization recommendations, and user-friendly ways to present insights that align with business needs. Title the report as Report Ideas",
            "analysis_ideas": "Generate ideas for deeper analytical insights using the current dataset, such as trend analysis, segmentation strategies, anomaly detection, or advanced forecasting techniques that could add business value. Title the report as Analysis Ideas",
        }

    def reset(self):
        # Reset any state if needed
        pass
