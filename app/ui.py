from threading import Thread
from queue import Queue, Empty
import logging
import os
import markdown2
import customtkinter as ctk
from PIL import Image
from tkinter import BooleanVar, messagebox, StringVar
from tkinterweb import HtmlFrame
from tkinterdnd2 import TkinterDnD, DND_FILES
from app.controller import Controller


COLORS = {
    "primary": "#6654f5",
    "primary-dark": "#f5f5f5",
    "dark-card": "#ebebeb",
    "secondary": "#0b0c18",
    "black": "#000000",
    "helper": "#ca5a8b",
    "action": "#f2b347",
    "warning": "#ff6900",
    "white": "#ffffff",
}


class DnDTk(ctk.CTk, TkinterDnD.DnDWrapper):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.TkdndVersion = TkinterDnD._require(self)


class GUI:
    def __init__(self, controller=None):
        # Main components
        self.root = None
        self.controller = controller or Controller()
        self.current_model = None

        # UI Elements
        self.upload_frame = None
        self.analysis_frame = None
        self.tabview = None
        self.html_frames = {}

        # State variables
        self.analysis_shown = None
        self.model_label = None
        self.analysis_label = None
        self.poppins_font = None
        self.logo_image = None

    def create_gui(self):
        ctk.set_appearance_mode("system")
        self.root = DnDTk()
        self.root.title("AnalystHub 2.0 - BIM Model Insights")
        self.root.geometry("1024x768")
        self.root.configure(fg_color=COLORS["primary-dark"])

        self.poppins_font = ctk.CTkFont(family="Poppins", size=12)

        main_frame = ctk.CTkFrame(
            self.root, fg_color=COLORS["primary-dark"], corner_radius=0
        )
        main_frame.pack(fill="both", expand=True, padx=20, pady=20)

        self._setup_header(main_frame)
        self._setup_upload_section(main_frame)
        self._setup_analysis_section(main_frame)

        self.controller.check_env_file()

        return self.root

    def _setup_header(self, parent):
        header_frame = ctk.CTkFrame(
            parent, fg_color=COLORS["primary-dark"], corner_radius=0
        )
        header_frame.pack(pady=(5, 20), fill="x")

        logo_path = os.path.join(
            os.path.dirname(os.path.dirname(__file__)),
            "assets",
            "images",
            "ah_logo.png",
        )
        image = Image.open(logo_path)
        self.logo_image = ctk.CTkImage(image, size=(232, 36))

        ctk.CTkLabel(
            header_frame,
            image=self.logo_image,
            text="",
            fg_color="transparent",
        ).pack(side="left", pady=(5, 0), padx=(10, 5))

        ctk.CTkLabel(
            header_frame,
            text="Power BI Model Insight Hub",
            text_color=COLORS["black"],
            font=(self.poppins_font.actual("family"), 16),
            fg_color="transparent",
        ).pack(side="right", pady=(5, 0), padx=(5, 10))

        gradient_width = int(parent.winfo_screenwidth() / 2)
        gradient_img = self.create_gradient(
            gradient_width, 4, (202, 90, 139), (242, 179, 71)
        )
        gradient_ctk_image = ctk.CTkImage(gradient_img, size=(gradient_width, 4))

        gradient_label = ctk.CTkLabel(parent, image=gradient_ctk_image, text="")
        gradient_label.pack(fill="x", anchor="center")

    def _setup_upload_section(self, parent):
        self.upload_frame = ctk.CTkFrame(
            parent, fg_color=COLORS["dark-card"], corner_radius=8
        )
        self.upload_frame.pack(side="bottom", fill="x", pady=20)

        self.upload_frame.drop_target_register(DND_FILES)
        self.upload_frame.dnd_bind("<<Drop>>", self._handle_upload_frame_drop)

        model_frame = ctk.CTkFrame(
            self.upload_frame, fg_color=COLORS["primary-dark"], corner_radius=0
        )
        model_frame.pack(side="left", padx=(10, 20))

        self.current_model = StringVar(value="gpt-4o-mini")

        model_selector = ctk.CTkOptionMenu(
            model_frame,
            values=list(self.controller._ai_models()),
            variable=self.current_model,
            command=self._on_model_change,
            width=150,
            font=(self.poppins_font.actual("family"), 12),
            fg_color=COLORS["primary-dark"],
            text_color=COLORS["black"],
            button_color=COLORS["primary"],
            button_hover_color=COLORS["helper"],
        )
        model_selector.pack(side="left")

        # Create a container frame for centered elements
        center_frame = ctk.CTkFrame(
            self.upload_frame, fg_color="transparent", corner_radius=0
        )
        center_frame.pack(expand=True, fill="both", padx=(0, model_frame.winfo_width()))

        ctk.CTkLabel(
            center_frame,
            text="Drag and drop your .bim file here or use the button below:",
            text_color=COLORS["black"],
            fg_color="transparent",
            font=self.poppins_font,
        ).pack(pady=(15, 5))

        ctk.CTkButton(
            center_frame,
            text="Upload BIM File",
            command=self._upload_file,
            font=(self.poppins_font.actual("family"), 12, "bold"),
            fg_color=COLORS["action"],
            text_color=COLORS["white"],
            hover_color=COLORS["helper"],
            border_spacing=10,
        ).pack(pady=(5, 20))

    def _handle_upload_frame_drop(self, event):
        file_path = event.data.strip("{}")  # handle curly braces on Windows
        self._process_file(file_path)

    def _upload_file(self):
        file_path = self.controller.file_handler.select_file()
        if not file_path:
            return

        self._process_file(file_path)

    def _setup_analysis_section(self, parent):
        self.analysis_shown = BooleanVar(value=False)

        self.analysis_frame = ctk.CTkFrame(
            parent, fg_color=COLORS["primary-dark"], corner_radius=0
        )

        header = ctk.CTkFrame(
            self.analysis_frame, fg_color=COLORS["primary-dark"], corner_radius=0
        )

        self.model_label = ctk.CTkLabel(
            header,
            text=self.current_model.get(),
            text_color=COLORS["primary"],
            font=(self.poppins_font.actual("family"), 10, "bold"),
            fg_color=COLORS["dark-card"],
            padx=5,
            pady=2,
        )
        self.model_label.pack(side="left")

        self.analysis_label = ctk.CTkLabel(
            header,
            text="Results:",
            text_color=COLORS["secondary"],
            font=(self.poppins_font.actual("family"), 16, "bold"),
            fg_color="transparent",
        ).pack(side="left", padx=(10, 0))

        self.start_over_button = ctk.CTkButton(
            header,
            text="Start Over",
            command=self.reset_interface,
            font=(self.poppins_font.actual("family"), 14, "bold"),
            fg_color=COLORS["action"],
            text_color=COLORS["white"],
            hover_color=COLORS["helper"],
        ).pack(side="right")

        # Add download button with dropdown
        download_frame = ctk.CTkFrame(
            header, fg_color=COLORS["primary-dark"], corner_radius=0
        )
        download_frame.pack(side="right", padx=(0, 10))

        self.download_button = ctk.CTkButton(
            download_frame,
            text="Download",
            command=self._show_download_options,
            font=(self.poppins_font.actual("family"), 14, "bold"),
            fg_color=COLORS["primary"],
            text_color=COLORS["white"],
            hover_color=COLORS["helper"],
        )
        self.download_button.pack(side="left")

        # Add download all button with dropdown
        self.download_all_button = ctk.CTkButton(
            download_frame,
            text="Download All",
            command=self._show_download_all_options,
            font=(self.poppins_font.actual("family"), 14, "bold"),
            fg_color=COLORS["primary"],
            text_color=COLORS["white"],
            hover_color=COLORS["helper"],
        )
        self.download_all_button.pack(side="left", padx=(10, 0))
        self.download_all_button.configure(state="disabled")  # Initially disabled

        header.pack(fill="x", pady=(0, 10))

        self._setup_tabs(self.analysis_frame)

    def _on_model_change(self, new_model: str):
        self.current_model.set(new_model)
        if hasattr(self, "model_label") and self.model_label:
            self.model_label.configure(text=new_model)

    def _setup_tabs(self, parent):
        self.tabview = ctk.CTkTabview(
            parent,
            fg_color=COLORS["dark-card"],
            segmented_button_fg_color=COLORS["primary-dark"],
            segmented_button_selected_color=COLORS["helper"],
            segmented_button_selected_hover_color=COLORS["helper"],
        )

        self.tabview._segmented_button.configure(
            font=ctk.CTkFont(family="Poppins", size=12, weight="bold"),
        )

        self.tabview.pack(fill="both", expand=True)

        for task_name in self.controller.analysis_tasks().keys():
            tab_title = " " + task_name.replace("_", " ").title() + " "
            tab = self.tabview.add(tab_title)

            html_frame = self._setup_html_frame(tab)
            self.html_frames[task_name] = html_frame

    def _setup_html_frame(self, parent):
        html_frame = HtmlFrame(
            parent,
            horizontal_scrollbar=False,
            vertical_scrollbar=False,
        )
        self._setup_custom_scrollbar(html_frame, parent)
        html_frame.pack(fill="both", expand=True)
        return html_frame

    def _setup_custom_scrollbar(self, widget, parent):
        internal_widget = widget.winfo_children()[0]
        custom_scrollbar = ctk.CTkScrollbar(parent, command=internal_widget.yview)
        custom_scrollbar.pack(side="right", fill="y")
        internal_widget.configure(yscrollcommand=custom_scrollbar.set)
        self._enable_mouse_scroll(self, internal_widget)

    def _enable_mouse_scroll(self, event, widget):
        def _on_mouse_wheel(event):
            widget.yview_scroll(int(-1 * (event.delta // 120)), "units")

        widget.bind("<MouseWheel>", _on_mouse_wheel, add="+")

        widget.bind("<Button-4>", lambda e: widget.yview_scroll(-1, "units"), add="+")
        widget.bind("<Button-5>", lambda e: widget.yview_scroll(1, "units"), add="+")

    def create_gradient(self, width, height, start_color, end_color):
        gradient = Image.new("RGB", (width, height))

        pixels = []
        for y in range(height):
            for x in range(width):
                ratio = x / (width - 1)
                r = int(start_color[0] * (1 - ratio) + end_color[0] * ratio)
                g = int(start_color[1] * (1 - ratio) + end_color[1] * ratio)
                b = int(start_color[2] * (1 - ratio) + end_color[2] * ratio)
                pixels.append((r, g, b))

        gradient.putdata(pixels)

        return gradient

    def display_analysis(self, analysis, widget):
        if not analysis:
            return

        css_path = os.path.join(
            os.path.dirname(os.path.dirname(__file__)), "assets", "css", "analysis.css"
        )

        # with open(css_path, "r", encoding="utf-8") as css_file:
        #     custom_css = f"<style>{css_file.read()}</style>"

        # html_body = markdown2.markdown(
        #     analysis, extras=["fenced-code-blocks", "tables", "break-on-newline"]
        # )
        # html_content = custom_css + "<body>" + html_body + "</body>"

        # widget.load_html(html_content)
        html_content = f"""
        <!DOCTYPE html>
        <html>
        <head>
            <meta charset="UTF-8">
            <link href="https://fonts.googleapis.com/css2?family=Poppins:wght@300;400;500;600;700;800&display=swap" rel="stylesheet">
            <style>
                {open(css_path, "r", encoding="utf-8").read()}
            </style>
            <script>
            // Force wait for fonts to load
            document.addEventListener('DOMContentLoaded', function() {{
                setTimeout(function() {{
                    document.body.style.opacity = '1';
                }}, 200);
            }});
        </script>
        </head>
        <body>
            {
            markdown2.markdown(
                analysis,
                extras=[
                    "fenced-code-blocks",
                    "tables",
                    "break-on-newline",
                    "code-friendly",
                    "numbering",
                    "cuddled-lists",
                    "code-color",
                ],
            )
        }
        </body>
        </html>
        """

        widget.load_html(html_content)

    def reset_interface(self):
        # Clear and hide analysis section
        for html_frame in self.html_frames.values():
            html_frame.load_html("")
        self.analysis_frame.pack_forget()

        # Show upload section again
        self.upload_frame.pack(side="bottom", fill="x", pady=20)
        self.analysis_shown.set(False)
        self.controller.reset()

    def _process_file(self, file_path):
        self.upload_frame.pack_forget()

        if not self.analysis_shown.get():
            self.analysis_frame.pack(fill="both", expand=True)
            self.analysis_shown.set(True)

        for html_frame in self.html_frames.values():
            html_frame.load_html("<p>Analyzing file... Please wait...</p>")
        self.root.update()

        self.result_queue = Queue()
        analysis_thread = Thread(
            target=self._run_analysis, args=(file_path, self.result_queue), daemon=True
        )
        analysis_thread.start()

        # Store the analysis results for later use (e.g., downloading)
        self.analysis_results = {}

        self._check_results()

    def _run_analysis(self, file_path, queue):
        """Run analysis in a separate thread"""
        task_generator = self.controller.process_file(
            file_path, self.current_model.get()
        )
        if task_generator:
            try:
                for result in task_generator:
                    queue.put(("result", result))
            except Exception as e:
                queue.put(("error", str(e)))
            finally:
                queue.put(("done", None))

    def _check_results(self):
        try:
            message_type, data = self.result_queue.get_nowait()

            if message_type == "result":
                task_name, analysis_result = data
                if task_name in self.html_frames:
                    # Store the raw markdown for later use
                    self.analysis_results[task_name] = analysis_result

                    self.display_analysis(analysis_result, self.html_frames[task_name])
                    self.html_frames[task_name].update()

                self.root.after(10, self._check_results)

            elif message_type == "error":
                error_message = f"Analysis error: {data}"
                logging.getLogger("app").error(error_message)

                # Display error in all tabs that haven't received results yet
                error_html = f"""
                    <div style="color: #ff6900; padding: 20px; text-align: center;">
                        <h3>Error During Analysis</h3>
                        <p>{error_message}</p>
                    </div>
                """
                for html_frame in self.html_frames.values():
                    if (
                        html_frame.html.get()
                        == "<p>Analyzing file... Please wait...</p>"
                    ):
                        html_frame.load_html(error_html)

            elif message_type == "done":
                self._check_all_tabs_ready()

        except Empty:
            self.root.after(100, self._check_results)
        except Exception as e:
            logging.getLogger("app").error(f"Error checking results: {str(e)}")
            # Display error in UI
            error_html = f"""
                <div style="color: #ff6900; padding: 20px; text-align: center;">
                    <h3>Unexpected Error</h3>
                    <p>An error occurred while processing results: {str(e)}</p>
                </div>
            """
            for html_frame in self.html_frames.values():
                html_frame.load_html(error_html)

    def _check_all_tabs_ready(self):
        """Check if all tabs have content and show the download button if they do."""
        if not hasattr(self, "analysis_results"):
            return False

        all_tasks = self.controller.analysis_tasks().keys()
        all_ready = all(task in self.analysis_results for task in all_tasks)

        if all_ready:
            self.download_button.configure(state="normal")
            self.download_all_button.configure(state="normal")
        else:
            self.download_button.configure(state="disabled")
            self.download_all_button.configure(state="disabled")

        return all_ready

    def _show_download_options(self):
        """Show dropdown menu with file format options for download."""
        # Create a dropdown menu
        download_menu = ctk.CTkToplevel(self.root)
        download_menu.title("Choose Format")
        download_menu.geometry("200x170")
        download_menu.resizable(False, False)
        download_menu.attributes("-topmost", True)

        # Position the menu below the download button
        x = self.download_button.winfo_rootx()
        y = self.download_button.winfo_rooty() + self.download_button.winfo_height()
        download_menu.geometry(f"+{x}+{y}")

        # Add format options
        ctk.CTkLabel(
            download_menu,
            text="Select format:",
            font=(self.poppins_font.actual("family"), 14),
        ).pack(pady=(10, 5))

        formats = [("PDF", "pdf"), ("Text File", "txt"), ("Word Document", "doc")]

        for label, format_type in formats:
            ctk.CTkButton(
                download_menu,
                text=label,
                command=lambda fmt=format_type: self._download_analysis(
                    fmt, download_menu
                ),
                font=self.poppins_font,
                fg_color=COLORS["primary"],
                text_color=COLORS["white"],
                hover_color=COLORS["helper"],
            ).pack(fill="x", padx=10, pady=5)

    def _download_analysis(self, file_format, menu=None):
        """Download the current analysis in the specified format."""
        if menu:
            menu.destroy()

        current_tab = self.tabview.get()
        if not current_tab:
            return

        task_name = current_tab.strip().lower().replace(" ", "_")

        for key in self.controller.analysis_tasks().keys():
            if key in task_name:
                task_name = key
                break

        if (
            not hasattr(self, "analysis_results")
            or task_name not in self.analysis_results
        ):
            messagebox.showerror("Error", "No analysis content available for download")
            return

        content = self.analysis_results[task_name]
        file_prefix = current_tab.strip().replace(" ", "_").lower()

        try:
            self.controller.file_handler.save_analysis(
                content, file_format, file_prefix
            )
        except Exception as e:
            messagebox.showerror("Error", f"Failed to save file: {str(e)}")

    def _show_download_all_options(self):
        """Show dropdown menu with file format options for downloading all tabs."""

        download_menu = ctk.CTkToplevel(self.root)
        download_menu.title("Choose Format")
        download_menu.geometry("200x170")
        download_menu.resizable(False, False)
        download_menu.attributes("-topmost", True)

        x = self.download_all_button.winfo_rootx()
        y = (
            self.download_all_button.winfo_rooty()
            + self.download_all_button.winfo_height()
        )
        download_menu.geometry(f"+{x}+{y}")

        ctk.CTkLabel(
            download_menu,
            text="Select format:",
            font=(self.poppins_font.actual("family"), 14),
        ).pack(pady=(10, 5))

        formats = [("PDF", "pdf"), ("Text File", "txt"), ("Word Document", "doc")]

        for label, format_type in formats:
            ctk.CTkButton(
                download_menu,
                text=label,
                command=lambda fmt=format_type: self._download_all_analyses(
                    fmt, download_menu
                ),
                font=self.poppins_font,
                fg_color=COLORS["primary"],
                text_color=COLORS["white"],
                hover_color=COLORS["helper"],
            ).pack(fill="x", padx=10, pady=5)

    def _download_all_analyses(self, file_format, menu=None):
        """Download all analyses combined into a single file."""
        if menu:
            menu.destroy()

        if not hasattr(self, "analysis_results") or not self.analysis_results:
            messagebox.showerror("Error", "No analysis content available for download")
            return

        combined_content = ""

        task_display_names = {}
        for task_name in self.controller.analysis_tasks().keys():
            display_name = task_name.replace("_", " ").title()
            task_display_names[task_name] = display_name

        for task_name, display_name in task_display_names.items():
            if task_name in self.analysis_results:
                current_result = self.analysis_results[task_name]

                if not current_result.startswith("#"):
                    combined_content += f"# {display_name}\n\n"
                combined_content += current_result
                combined_content += "\n\n\n---\n\n\n"

        if combined_content.endswith("\n\n\n---\n\n\n"):
            combined_content = combined_content[:-9]

        try:
            self.controller.file_handler.save_analysis(
                combined_content, file_format, "all_analyses"
            )
        except Exception as e:
            messagebox.showerror("Error", f"Failed to save file: {str(e)}")
