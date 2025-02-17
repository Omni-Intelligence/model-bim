import os
from dotenv import load_dotenv
import openai
from tkinter import messagebox, simpledialog


class AIAnalyzer:
    def __init__(self):
        load_dotenv()
        openai.api_key = os.getenv("OPENAI_API_KEY")

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

    def analyze(self, content):
        try:
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
            # print(response)
            return response.choices[0].message.content
            '''
            return """
# Example Markdown

## Introduction

This is an example of markdown text. Markdown is a lightweight markup language with plain-text formatting syntax.

### Features

- Easy to read and write
- Converts to HTML
- Widely used in documentation

**Bold Text** and *Italic Text* are simple to create.

```python
# Example of Python code block
def greet():
    print("Hello, World!")
```

### Features

- Easy to read and write
- Converts to HTML
- Widely used in documentation

**Bold Text** and *Italic Text* are simple to create.

```python
# Example of Python code block
def greet():
    print("Hello, World!")
```

For more information, visit [Markdown Guide](https://www.markdownguide.org).
"""
'''
        except Exception as e:
            messagebox.showerror(
                "API Error", f"Failed to analyze with ChatGPT: {str(e)}"
            )
            return None

    def analyzeModel(self, content):
        try:
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
        except Exception as e:
            messagebox.showerror(
                "API Error", f"Failed to analyze with ChatGPT: {str(e)}"
            )
            return None
