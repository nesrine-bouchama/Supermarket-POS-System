"""
Login View — Professional dark-themed login screen.
"""

import customtkinter as ctk
from controllers.auth_controller import AuthController
from views.theme import COLORS, FONTS


class LoginView(ctk.CTk):

    def __init__(self):
        super().__init__()

        self.geometry("460x580")
        self.title("Supermarket POS")
        self.configure(fg_color=COLORS["bg_darkest"])
        self.resizable(False, False)
        self.center_window(460, 580)

        # ─── Main container ───
        container = ctk.CTkFrame(self, fg_color="transparent")
        container.place(relx=0.5, rely=0.5, anchor="center")

        # ─── Logo area ───
        logo_frame = ctk.CTkFrame(container, fg_color="transparent")
        logo_frame.pack(pady=(0, 25))

        ctk.CTkLabel(
            logo_frame, text="🛒",
            font=("Segoe UI", 52),
        ).pack()

        ctk.CTkLabel(
            logo_frame, text="SUPERMARKET",
            font=FONTS["heading_xl"],
            text_color=COLORS["text_primary"],
        ).pack()

        ctk.CTkLabel(
            logo_frame, text="Point of Sale System",
            font=FONTS["body"],
            text_color=COLORS["text_secondary"],
        ).pack(pady=(2, 0))

        # ─── Login card ───
        card = ctk.CTkFrame(
            container,
            fg_color=COLORS["bg_card"],
            corner_radius=16,
            border_width=1,
            border_color=COLORS["border"],
        )
        card.pack(padx=30, ipadx=30, ipady=25)

        ctk.CTkLabel(
            card, text="Sign In",
            font=FONTS["heading"],
            text_color=COLORS["text_primary"],
        ).pack(pady=(5, 20))

        # Username
        ctk.CTkLabel(
            card, text="Username",
            font=FONTS["caption"],
            text_color=COLORS["text_secondary"],
        ).pack(anchor="w", padx=5)

        self.username = ctk.CTkEntry(
            card,
            placeholder_text="Enter your username",
            width=280, height=42,
            fg_color=COLORS["bg_input"],
            border_color=COLORS["border"],
            text_color=COLORS["text_primary"],
            font=FONTS["body"],
            corner_radius=10,
        )
        self.username.pack(pady=(4, 12))

        # Password
        ctk.CTkLabel(
            card, text="Password",
            font=FONTS["caption"],
            text_color=COLORS["text_secondary"],
        ).pack(anchor="w", padx=5)

        self.password = ctk.CTkEntry(
            card,
            placeholder_text="Enter your password",
            show="●",
            width=280, height=42,
            fg_color=COLORS["bg_input"],
            border_color=COLORS["border"],
            text_color=COLORS["text_primary"],
            font=FONTS["body"],
            corner_radius=10,
        )
        self.password.pack(pady=(4, 18))

        # Login button
        self.login_btn = ctk.CTkButton(
            card, text="LOGIN",
            width=280, height=44,
            fg_color=COLORS["accent"],
            hover_color=COLORS["accent_hover"],
            font=FONTS["button"],
            corner_radius=10,
            command=self.login,
        )
        self.login_btn.pack(pady=(0, 5))

        # Error message label
        self.error_label = ctk.CTkLabel(
            card, text="",
            text_color=COLORS["danger"],
            font=FONTS["body_sm"],
        )
        self.error_label.pack(pady=(5, 0))

        # ─── Footer ───
        ctk.CTkLabel(
            container,
            text="v2.0  •  Supermarket POS System",
            font=FONTS["caption"],
            text_color=COLORS["text_muted"],
        ).pack(pady=(20, 0))

        # ─── Key bindings ───
        self.bind("<Return>", lambda e: self.login())
        self.username.focus_set()

    # ─── Center the window on screen ───
    def center_window(self, width, height):
        sw = self.winfo_screenwidth()
        sh = self.winfo_screenheight()
        x = (sw // 2) - (width // 2)
        y = (sh // 2) - (height // 2)
        self.geometry(f"{width}x{height}+{x}+{y}")

    # ─── Login logic ───
    def login(self):
        username = self.username.get().strip()
        password = self.password.get().strip()

        if not username or not password:
            self.error_label.configure(text="⚠  Please fill in all fields")
            return

        user = AuthController.login(username, password)

        if user:
            self.destroy()
            from views.dashboard_view import DashboardView
            app = DashboardView(user)
            app.mainloop()
        else:
            self.error_label.configure(text="❌  Invalid username or password")
