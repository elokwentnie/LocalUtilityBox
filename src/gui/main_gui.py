"""Main GUI Application for LocalUtilityBox."""
import customtkinter as ctk

from .tabs.image_tab import IMAGE_SECTIONS
from .tabs.file_tab import FILE_SECTIONS
from .tabs.video_tab import VIDEO_SECTIONS
from .widgets import StatusBar, bind_mousewheel

try:
    from tkinterdnd2 import TkinterDnD
    _HAS_DND = True
except ImportError:
    _HAS_DND = False

ALL_SECTIONS = IMAGE_SECTIONS + FILE_SECTIONS + VIDEO_SECTIONS


class LocalUtilityBoxGUI(ctk.CTk, TkinterDnD.DnDWrapper if _HAS_DND else object):
    """Main application window with sidebar navigation."""

    def __init__(self):
        super().__init__()
        global _HAS_DND
        if _HAS_DND:
            try:
                self.TkdndVersion = TkinterDnD._require(self)
            except Exception:
                _HAS_DND = False
        self.title("LocalUtilityBox")
        self.geometry("1100x750")
        self.minsize(950, 620)

        ctk.set_appearance_mode("system")
        ctk.set_default_color_theme("blue")

        self._sidebar_buttons: list[ctk.CTkButton] = []

        self._build_sidebar()

        self.content = ctk.CTkFrame(self, corner_radius=0, fg_color="transparent")
        self.content.pack(side="left", fill="both", expand=True)

        self._show_welcome()
        self._center_window()

    # ------------------------------------------------------------------
    # Sidebar
    # ------------------------------------------------------------------

    def _build_sidebar(self):
        sidebar = ctk.CTkFrame(
            self, width=260, corner_radius=0,
            fg_color=("gray92", "gray14"),
        )
        sidebar.pack(side="left", fill="y")
        sidebar.pack_propagate(False)

        # App branding
        brand = ctk.CTkFrame(sidebar, fg_color="transparent")
        ctk.CTkLabel(
            brand, text="LocalUtilityBox", font=("", 20, "bold"), anchor="w"
        ).pack(fill="x")
        ctk.CTkLabel(
            brand, text="Local file processing", font=("", 12),
            text_color="gray50", anchor="w",
        ).pack(fill="x", pady=(2, 0))
        brand.pack(fill="x", padx=20, pady=(24, 12))

        ctk.CTkFrame(
            sidebar, height=1, fg_color=("gray80", "gray25")
        ).pack(fill="x", padx=16, pady=(0, 4))

        # Scrollable tool list
        scroll = ctk.CTkScrollableFrame(
            sidebar, fg_color="transparent",
            scrollbar_button_color=("gray75", "gray30"),
        )

        for section_label, tools in ALL_SECTIONS:
            ctk.CTkLabel(
                scroll, text=section_label, font=("", 11, "bold"),
                text_color=("gray45", "gray55"), anchor="w",
            ).pack(fill="x", padx=10, pady=(16, 4))

            for tool in tools:
                btn = ctk.CTkButton(
                    scroll, text=tool["name"], anchor="w", height=34,
                    font=("", 13), corner_radius=8,
                    fg_color="transparent",
                    text_color=("gray15", "gray85"),
                    hover_color=("gray82", "gray25"),
                    command=lambda t=tool: self._show_tool(t),
                )
                btn.pack(fill="x", padx=4, pady=1)
                self._sidebar_buttons.append(btn)
                tool["_btn"] = btn

        scroll.pack(fill="both", expand=True, padx=4, pady=(0, 4))
        bind_mousewheel(scroll)

        # Theme picker at bottom
        ctk.CTkFrame(
            sidebar, height=1, fg_color=("gray80", "gray25")
        ).pack(fill="x", padx=16)

        bottom = ctk.CTkFrame(sidebar, fg_color="transparent")
        ctk.CTkLabel(
            bottom, text="Theme", font=("", 12), text_color="gray50"
        ).pack(side="left", padx=(4, 10))
        ctk.CTkOptionMenu(
            bottom, values=["System", "Light", "Dark"],
            command=lambda m: ctk.set_appearance_mode(m.lower()),
            width=120, height=28, font=("", 12),
            fg_color=("gray80", "gray25"),
            button_color=("gray70", "gray35"),
            text_color=("gray15", "gray85"),
        ).pack(side="left", fill="x", expand=True)
        bottom.pack(fill="x", padx=16, pady=14)

    # ------------------------------------------------------------------
    # Content area
    # ------------------------------------------------------------------

    def _clear_content(self):
        for w in self.content.winfo_children():
            w.destroy()

    def _set_active(self, tool):
        for btn in self._sidebar_buttons:
            btn.configure(fg_color="transparent")
        tool["_btn"].configure(fg_color=("gray78", "gray28"))

    def _show_welcome(self):
        self._clear_content()
        for btn in self._sidebar_buttons:
            btn.configure(fg_color="transparent")

        center = ctk.CTkFrame(self.content, fg_color="transparent")
        center.place(relx=0.5, rely=0.42, anchor="center")

        ctk.CTkLabel(
            center, text="Welcome to LocalUtilityBox",
            font=("", 28, "bold"),
        ).pack(pady=(0, 8))

        ctk.CTkLabel(
            center, text="Select a tool from the sidebar to get started.",
            font=("", 15), text_color="gray50",
        ).pack(pady=(0, 28))

        info = ctk.CTkFrame(center, corner_radius=12, fg_color=("gray88", "gray20"))
        ctk.CTkLabel(
            info,
            text="All processing is done locally \u2014 your data stays private.",
            font=("", 14), text_color=("gray30", "gray70"), wraplength=420,
        ).pack(padx=28, pady=18)
        info.pack()

    def _show_tool(self, tool):
        self._set_active(tool)
        self._clear_content()

        # Header
        header = ctk.CTkFrame(self.content, fg_color="transparent")
        ctk.CTkLabel(
            header, text=tool["name"], font=("", 24, "bold"), anchor="w"
        ).pack(fill="x")
        ctk.CTkLabel(
            header, text=tool["description"], font=("", 14),
            text_color=("gray40", "gray60"), anchor="w",
        ).pack(fill="x", pady=(4, 0))
        header.pack(fill="x", padx=36, pady=(30, 16))

        ctk.CTkFrame(
            self.content, height=1, fg_color=("gray82", "gray28")
        ).pack(fill="x", padx=36)

        # Scrollable tool body
        body = ctk.CTkScrollableFrame(self.content, fg_color="transparent")
        body.pack(fill="both", expand=True, padx=36, pady=(20, 8))

        # Status bar
        status_bar = StatusBar(self.content)
        status_bar.pack(fill="x", padx=36, pady=(8, 24))

        # Build the tool's widgets
        tool["build_fn"](body, status_bar)
        bind_mousewheel(body)

    # ------------------------------------------------------------------
    # Helpers
    # ------------------------------------------------------------------

    def _center_window(self):
        self.update_idletasks()
        w = self.winfo_width()
        h = self.winfo_height()
        x = (self.winfo_screenwidth() // 2) - (w // 2)
        y = (self.winfo_screenheight() // 2) - (h // 2)
        self.geometry(f"{w}x{h}+{x}+{y}")


def main():
    """Main entry point for GUI application."""
    app = LocalUtilityBoxGUI()
    app.mainloop()


if __name__ == "__main__":
    main()
