import logging
import os
import sys
from dotenv import load_dotenv
import openai
from tkinter import messagebox


class AIAnalyzer:
    def __init__(self):
        if getattr(sys, "frozen", False):
            # If the application is run as a bundle (PyInstaller executable)
            env_path = os.path.join(sys._MEIPASS, ".env")
        else:
            application_path = os.path.dirname(os.path.abspath(__file__))
            env_path = os.path.join(application_path, ".env")

        load_dotenv(env_path)
        openai.api_key = os.getenv("OPENAI_API_KEY")

    def analyze(self, task, content, model="gpt-4o-mini"):
        # logging.getLogger("app").info(f"Analyzing with ChatGPT: {task}")
        try:
            # client = openai.OpenAI()
            # response = client.chat.completions.create(
            #     model=model,
            #     messages=[
            #         {
            #             "role": "developer" if model in ["o1", "o3-mini"] else "system",
            #             "content": task
            #             + "Generated response must be compatible with markdown2 for pretty rendering, so avoid unexpected characters and wrap code snippets carefully.",
            #         },
            #         {
            #             "role": "user",
            #             "content": f"Please analyze this for me:\n{content}",
            #         },
            #     ],
            # )

            # # logging.getLogger("app").info("Response generated")
            # print("model:", model)

            # return response.choices[0].message.content

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
                "chat_response.md",
            ),
            "r",
        ) as f:
            return f.read()
