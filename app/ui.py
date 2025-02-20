import logging
import os
import markdown
import customtkinter as ctk
from PIL import Image
from tkinter import BooleanVar
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

        # UI Elements
        self.upload_frame = None
        self.analysis_frame = None
        self.tabview = None
        self.html_frames = {}

        # State
        self.analysis_shown = None
        self.analysis_label = None
        self.poppins_font = None
        self.logo_image = None

    def create_gui(self):
        ctk.set_appearance_mode("system")
        self.root = DnDTk()
        self.root.title("AnalystHub 2.0")
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
            text="Power BI Analysis Toolkit",
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

        ctk.CTkLabel(
            self.upload_frame,
            text="Drag and drop your file here or use the button below:",
            text_color=COLORS["black"],
            fg_color="transparent",
            font=self.poppins_font,
        ).pack(pady=(15, 5))

        ctk.CTkButton(
            self.upload_frame,
            text="Upload Power BI File",
            command=self._upload_file,
            font=(self.poppins_font.actual("family"), 12, "bold"),
            fg_color=COLORS["action"],
            text_color=COLORS["white"],
            hover_color=COLORS["helper"],
            border_spacing=10,
        ).pack(padx=30, pady=(5, 20))

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

        header.pack(fill="x", pady=(0, 10))

        self._setup_tabs(self.analysis_frame)

    def _setup_tabs(self, parent):
        self.tabview = ctk.CTkTabview(
            parent,
            fg_color=COLORS["dark-card"],
            segmented_button_fg_color=COLORS["primary-dark"],
            segmented_button_selected_color=COLORS["helper"],
            segmented_button_selected_hover_color=COLORS["helper"],
        )

        self.tabview._segmented_button.configure(
            font=ctk.CTkFont(family="Poppins", size=14, weight="bold"),
        )

        self.tabview.pack(fill="both", expand=True)

        for task_name in self.controller.analysis_tasks().keys():
            tab_title = " " + task_name.replace("_", " ").title() + " "
            tab = self.tabview.add(tab_title)

            html_frame = self._setup_html_frame(tab)
            self.html_frames[task_name] = html_frame

        # self.analysis_tab = self.tabview.add(" Analysis ")
        # self.model_analysis_tab = self.tabview.add(" Model Analysis ")

        # self.analysis_html = HtmlFrame(
        #     self.analysis_tab, horizontal_scrollbar=False, vertical_scrollbar=False
        # )
        # self._setup_custom_scrollbar(self.analysis_html, self.analysis_tab)
        # self.analysis_html.pack(fill="both", expand=True)

        # self.model_analysis_html = HtmlFrame(
        #     self.model_analysis_tab,
        #     horizontal_scrollbar=False,
        #     vertical_scrollbar=False,
        # )
        # self._setup_custom_scrollbar(self.model_analysis_html, self.model_analysis_tab)
        # self.model_analysis_html.pack(fill="both", expand=True)

    def _setup_html_frame(self, parent):
        html_frame = HtmlFrame(
            parent, horizontal_scrollbar=False, vertical_scrollbar=False
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

        with open(css_path, "r", encoding="utf-8") as css_file:
            custom_css = f"<style>{css_file.read()}</style>"

        html_body = markdown.markdown(analysis, extensions=["fenced_code"])
        html_content = custom_css + "<body>" + html_body + "</body>"

        widget.load_html(html_content)

    def show_analysis_widgets(self):
        if not self.analysis_shown.get():
            self.analysis_frame.pack(fill="both", expand=True)
            self.analysis_shown.set(True)

    def show_loading(self):
        for html_frame in self.html_frames.values():
            html_frame.load_html("<p>Analyzing file... Please wait...</p>")
        self.root.update()

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
        result = self.controller.process_file(file_path)
        if result:
            self.upload_frame.pack_forget()
            self.show_analysis_widgets()
            self.show_loading()

            for task_name, analysis_result in result.items():
                if task_name in self.html_frames:
                    self.display_analysis(analysis_result, self.html_frames[task_name])
