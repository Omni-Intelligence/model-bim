import os
from dotenv import load_dotenv
import openai
from tkinter import messagebox


class AIAnalyzer:
    def __init__(self):
        load_dotenv()
        openai.api_key = os.getenv("OPENAI_API_KEY")

    def analyze(self, task, content):
        try:
            """
            client = openai.OpenAI()
            response = client.chat.completions.create(
                model="o3-mini",
                messages=[
                    {
                        "role": "developer",
                        "content": (
                            "You are a Power BI expert analyzing a report structure and content. "
                            "Provide clear, concise analysis with key insights and recommendations."
                            "Make sure you respond in proper structured Markdown format."
                        ),
                    },
                    {
                        "role": "user",
                        "content": f"Please analyze this for me:\n{content}",
                    },
                ],
            )
            
            return response.choices[0].message.content
            """
            return self._return_test_response()

        except Exception as e:
            messagebox.showerror(
                "API Error", f"Failed to analyze with ChatGPT: {str(e)}"
            )
            return None

    def analyzeModel(self, content):
        try:
            """
            client = openai.OpenAI()
            response = client.chat.completions.create(
                model="o3-mini",
                messages=[
                    {
                        "role": "developer",
                        "content": (
                            "You are a Power BI expert analyzing a report data model structure. "
                            "Provide clear, concise analysis with key insights and recommendations."
                            "Make sure you respond in proper structured Markdown format."
                        ),
                    },
                    {"role": "user", "content": f"Analyze this data model:\n{content}"},
                ],
            )

            return response.choices[0].message.content
            """
            return self._return_test_response()

        except Exception as e:
            messagebox.showerror(
                "API Error", f"Failed to analyze with ChatGPT: {str(e)}"
            )
            return None

    @staticmethod
    def _return_test_response():
        with open(
            os.path.join(
                os.path.dirname(os.path.dirname(__file__)),
                "assets",
                "examples",
                "md_response",
            ),
            "r",
        ) as f:
            return f.read()

        """
        Best ideas
 
Here are some ideas for adding value and boosting productivity for a data analyst working with this model:
 
• Enhanced Data Documentation:
  - Create a data dictionary that not only lists the tables, columns, and measures but also explains what each field represents and how measures are calculated.
  - Include descriptions of key business logic (for example, how outliers are defined) and any assumptions built into the calculations.
 
• Interactive Metadata Dashboard:
  - Develop an internal dashboard that displays metadata details—such as relationships, measure dependencies, and data lineage.
  - This can help analysts quickly understand how the model is structured and identify which measures or tables to focus on for a given analysis.
 
• Best Practices and Usage Guides:
  - Offer guidelines on when to use specific measures (for example, explaining the context behind [Total Sales] versus [Outlier Sales]).
  - Provide examples of how to combine measures with visualizations (e.g., line charts for trends, scatter plots for outlier detection) along with interpretation tips.
 
• Performance and Diagnostic Insights:
  - Supply diagnostic views that show which parts of the model are most used or might be causing performance bottlenecks.
  - Include recommendations on improving query performance (for example, by checking relationships or reviewing calculated column logic).
 
Analysis Ideas
 
Report Ideas
 
Missing Analysis
 
Improved DAX measures"""
