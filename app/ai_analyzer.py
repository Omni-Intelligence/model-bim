import logging
import os
from dotenv import load_dotenv
import openai
from tkinter import messagebox


class AIAnalyzer:
    def __init__(self):
        load_dotenv()
        openai.api_key = os.getenv("OPENAI_API_KEY")

    def analyze(self, task, content):
        logging.getLogger("app").info(f"Analyzing with ChatGPT: {task}")
        try:
            client = openai.OpenAI()
            response = client.chat.completions.create(
                model="gpt-4o-mini",
                messages=[
                    {
                        "role": "system",
                        "content": task,
                    },
                    {
                        "role": "user",
                        "content": f"Please analyze this for me:\n{content}",
                    },
                ],
            )

            logging.getLogger("app").info("Response generated")

            return response.choices[0].message.content

            # return self._return_test_response()

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
                "chat_response.md",
            ),
            "r",
        ) as f:
            return f.read()
