"""
Dashboard View — Main application shell with professional sidebar navigation.
Handles role-based menu items, active state highlighting, and logout.
"""

import customtkinter as ctk
from views.theme import COLORS, FONTS, setup_treeview_style, toggle_mode, get_mode


class DashboardView(ctk.CTk):

    def __init__(self, user):
        super().__init__()

        self.user = user
        self.title("Supermarket POS — Dashboard")
        self.geometry("1280x720")
        self.configure(fg_color=COLORS["bg_darkest"])

        # Fullscreen mode
        self.attributes("-fullscreen", True)
        self.bind("<Escape>", lambda e: self.attributes("-fullscreen", False))
        self.bind("<F11>", lambda e: self.attributes(
            "-fullscreen", not self.attributes("-fullscreen")))

        # Track current view for reloading after theme toggle
        self.current_view = "sales"

        # Track navigation buttons for active-state styling
        self.nav_buttons = []

        # Configure treeview style once
        setup_treeview_style()

        # ══════════════════════════════════════
        #  SIDEBAR
        # ══════════════════════════════════════
        self.sidebar = ctk.CTkFrame(
            self, width=250,
            fg_color=COLORS["bg_sidebar"],
            corner_radius=0,
        )
        self.sidebar.pack(side="left", fill="y")
        self.sidebar.pack_propagate(False)

        # ─── App branding ───
        brand = ctk.CTkFrame(self.sidebar, fg_color="transparent")
        brand.pack(fill="x", padx=18, pady=(22, 8))

        ctk.CTkLabel(
            brand, text="🛒  SUPERMARKET",
            font=FONTS["heading_sm"],
            text_color=COLORS["accent_light"],
        ).pack(anchor="w")

        ctk.CTkLabel(
            brand, text="Point of Sale System",
            font=FONTS["caption"],
            text_color=COLORS["text_muted"],
        ).pack(anchor="w")

        # ─── Separator ───
        ctk.CTkFrame(
            self.sidebar, height=1,
            fg_color=COLORS["border"],
        ).pack(fill="x", padx=18, pady=(12, 12))

        # ─── User info card ───
        user_card = ctk.CTkFrame(
            self.sidebar,
            fg_color=COLORS["bg_card"],
            corner_radius=10,
            border_width=1,
            border_color=COLORS["border"],
        )
        user_card.pack(fill="x", padx=15, pady=(0, 18))

        user_inner = ctk.CTkFrame(user_card, fg_color="transparent")
        user_inner.pack(padx=14, pady=12, fill="x")

        ctk.CTkLabel(
            user_inner,
            text=f"👤  {user['username']}",
            font=FONTS["body_bold"],
            text_color=COLORS["text_primary"],
        ).pack(anchor="w")

        role_color = COLORS["accent"] if user["role"] == "admin" else COLORS["success"]
        ctk.CTkLabel(
            user_inner,
            text=f"●  {user['role'].upper()}",
            font=FONTS["caption"],
            text_color=role_color,
        ).pack(anchor="w", pady=(2, 0))

        # ─── Navigation section ───
        ctk.CTkLabel(
            self.sidebar, text="  NAVIGATION",
            font=("Segoe UI", 9, "bold"),
            text_color=COLORS["text_muted"],
        ).pack(anchor="w", padx=18, pady=(0, 6))

        # Cashier + Admin: Sales & Receipts
        self._add_nav("🛒   Sales", "sales")
        self._add_nav("🧾   Receipts", "receipts")

        # Admin-only section
        role = user["role"]
        if role == "admin":
            ctk.CTkFrame(
                self.sidebar, height=1,
                fg_color=COLORS["border"],
            ).pack(fill="x", padx=18, pady=10)

            ctk.CTkLabel(
                self.sidebar, text="  ADMIN",
                font=("Segoe UI", 9, "bold"),
                text_color=COLORS["text_muted"],
            ).pack(anchor="w", padx=18, pady=(0, 6))

            self._add_nav("📊   Dashboard", "dashboard")
            self._add_nav("📦   Products", "products")
            self._add_nav("👥   Users", "users")

        # ─── Spacer ───
        ctk.CTkFrame(self.sidebar, fg_color="transparent").pack(fill="both", expand=True)

        # ─── Separator ───
        ctk.CTkFrame(
            self.sidebar, height=1,
            fg_color=COLORS["border"],
        ).pack(fill="x", padx=18, pady=(5, 8))

        # ─── Theme toggle button ───
        mode = get_mode()
        theme_text = "☀️   Light Mode" if mode == "dark" else "🌙   Dark Mode"
        self.theme_btn = ctk.CTkButton(
            self.sidebar, text=theme_text,
            fg_color=COLORS["bg_card"],
            hover_color=COLORS["bg_card_hover"],
            text_color=COLORS["text_secondary"],
            font=FONTS["body"],
            height=40,
            corner_radius=10,
            command=self._toggle_theme,
        )
        self.theme_btn.pack(fill="x", padx=15, pady=(0, 8))

        # ─── Logout button ───
        ctk.CTkButton(
            self.sidebar, text="🚪   Logout",
            fg_color=COLORS["danger"],
            hover_color="#d94040",
            font=FONTS["button"],
            height=46,
            corner_radius=10,
            command=self.logout,
        ).pack(fill="x", padx=15, pady=(0, 25))

        # ══════════════════════════════════════
        #  MAIN CONTENT AREA
        # ══════════════════════════════════════
        self.main = ctk.CTkFrame(
            self,
            fg_color=COLORS["bg_darkest"],
            corner_radius=0,
        )
        self.main.pack(side="right", fill="both", expand=True)

        # Load default view
        self._load_view("sales")

    # ─── Add a navigation button ───
    def _add_nav(self, text, view_name):
        btn = ctk.CTkButton(
            self.sidebar, text=text,
            fg_color="transparent",
            hover_color=COLORS["bg_card_hover"],
            text_color=COLORS["text_secondary"],
            font=FONTS["body"],
            height=40,
            anchor="w",
            corner_radius=8,
            command=lambda v=view_name: self._load_view(v),
        )
        btn.pack(fill="x", padx=12, pady=2)
        btn._view_name = view_name
        self.nav_buttons.append(btn)

    # ─── Load a view into the main content area ───
    def _load_view(self, view_name):
        # Track current view for theme toggle reload
        self.current_view = view_name

        # Update active button styling
        for btn in self.nav_buttons:
            if btn._view_name == view_name:
                btn.configure(
                    fg_color=COLORS["accent"],
                    text_color="#ffffff",
                )
            else:
                btn.configure(
                    fg_color="transparent",
                    text_color=COLORS["text_secondary"],
                )

        # Clear main content
        for w in self.main.winfo_children():
            w.destroy()

        # Import and instantiate the requested view
        if view_name == "sales":
            from views.sales_view import SalesView
            SalesView(self.main)
        elif view_name == "receipts":
            from views.receipt_view import ReceiptView
            ReceiptView(self.main)
        elif view_name == "dashboard":
            from views.dashboard_stats import DashboardStats
            DashboardStats(self.main)
        elif view_name == "products":
            from views.product_view import ProductView
            ProductView(self.main)
        elif view_name == "users":
            from views.user_view import UserView
            UserView(self.main)

    # ─── Toggle dark/light theme ───
    def _toggle_theme(self):
        new_mode = toggle_mode()

        # Rebuild the entire UI with new colors
        self._rebuild()

    # ─── Rebuild the full dashboard UI ───
    def _rebuild(self):
        """Destroy all widgets and reconstruct the dashboard."""
        saved_view = self.current_view

        # Destroy everything
        for w in self.winfo_children():
            w.destroy()

        # Reset nav tracking
        self.nav_buttons = []

        # Re-run the full constructor body (without __init__ super call)
        self.configure(fg_color=COLORS["bg_darkest"])
        setup_treeview_style()

        # ── Rebuild sidebar ──
        self.sidebar = ctk.CTkFrame(
            self, width=250,
            fg_color=COLORS["bg_sidebar"],
            corner_radius=0,
        )
        self.sidebar.pack(side="left", fill="y")
        self.sidebar.pack_propagate(False)

        # Brand
        brand = ctk.CTkFrame(self.sidebar, fg_color="transparent")
        brand.pack(fill="x", padx=18, pady=(22, 8))
        ctk.CTkLabel(brand, text="🛒  SUPERMARKET", font=FONTS["heading_sm"],
                     text_color=COLORS["accent_light"]).pack(anchor="w")
        ctk.CTkLabel(brand, text="Point of Sale System", font=FONTS["caption"],
                     text_color=COLORS["text_muted"]).pack(anchor="w")

        ctk.CTkFrame(self.sidebar, height=1, fg_color=COLORS["border"]
                     ).pack(fill="x", padx=18, pady=(12, 12))

        # User card
        user_card = ctk.CTkFrame(self.sidebar, fg_color=COLORS["bg_card"],
                                  corner_radius=10, border_width=1,
                                  border_color=COLORS["border"])
        user_card.pack(fill="x", padx=15, pady=(0, 18))
        ui = ctk.CTkFrame(user_card, fg_color="transparent")
        ui.pack(padx=14, pady=12, fill="x")
        ctk.CTkLabel(ui, text=f"👤  {self.user['username']}",
                     font=FONTS["body_bold"],
                     text_color=COLORS["text_primary"]).pack(anchor="w")
        rc = COLORS["accent"] if self.user["role"] == "admin" else COLORS["success"]
        ctk.CTkLabel(ui, text=f"●  {self.user['role'].upper()}",
                     font=FONTS["caption"], text_color=rc).pack(anchor="w", pady=(2, 0))

        # Nav
        ctk.CTkLabel(self.sidebar, text="  NAVIGATION",
                     font=("Segoe UI", 9, "bold"),
                     text_color=COLORS["text_muted"]
                     ).pack(anchor="w", padx=18, pady=(0, 6))

        self._add_nav("🛒   Sales", "sales")
        self._add_nav("🧾   Receipts", "receipts")

        if self.user["role"] == "admin":
            ctk.CTkFrame(self.sidebar, height=1, fg_color=COLORS["border"]
                         ).pack(fill="x", padx=18, pady=10)
            ctk.CTkLabel(self.sidebar, text="  ADMIN",
                         font=("Segoe UI", 9, "bold"),
                         text_color=COLORS["text_muted"]
                         ).pack(anchor="w", padx=18, pady=(0, 6))
            self._add_nav("📊   Dashboard", "dashboard")
            self._add_nav("📦   Products", "products")
            self._add_nav("👥   Users", "users")

        # Spacer
        ctk.CTkFrame(self.sidebar, fg_color="transparent").pack(fill="both", expand=True)

        ctk.CTkFrame(self.sidebar, height=1, fg_color=COLORS["border"]
                     ).pack(fill="x", padx=18, pady=(5, 8))

        # Theme toggle
        mode = get_mode()
        theme_text = "☀️   Light Mode" if mode == "dark" else "🌙   Dark Mode"
        self.theme_btn = ctk.CTkButton(
            self.sidebar, text=theme_text,
            fg_color=COLORS["bg_card"],
            hover_color=COLORS["bg_card_hover"],
            text_color=COLORS["text_secondary"],
            font=FONTS["body"], height=40, corner_radius=10,
            command=self._toggle_theme,
        )
        self.theme_btn.pack(fill="x", padx=15, pady=(0, 8))

        # Logout
        ctk.CTkButton(
            self.sidebar, text="🚪   Logout",
            fg_color=COLORS["danger"], hover_color="#d94040",
            font=FONTS["button"], height=46, corner_radius=10,
            command=self.logout,
        ).pack(fill="x", padx=15, pady=(0, 25))

        # ── Rebuild main area ──
        self.main = ctk.CTkFrame(self, fg_color=COLORS["bg_darkest"], corner_radius=0)
        self.main.pack(side="right", fill="both", expand=True)

        # Reload the view they were on
        self._load_view(saved_view)

    # ─── Logout and return to login ───
    def logout(self):
        self.destroy()
        from views.login_view import LoginView
        app = LoginView()
        app.mainloop()