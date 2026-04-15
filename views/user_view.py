"""
User View — User management with table, add form, and delete confirmation.
"""

import customtkinter as ctk
from tkinter import ttk
from controllers.auth_controller import AuthController
from models.user_model import UserModel
from utils.notifications import success, error, confirm
from views.theme import COLORS, FONTS


class UserView:

    def __init__(self, parent):
        self.frame = ctk.CTkFrame(parent, fg_color="transparent")
        self.frame.pack(fill="both", expand=True, padx=25, pady=25)

        # ─── Header ───
        ctk.CTkLabel(
            self.frame, text="👥  User Management",
            font=FONTS["heading_lg"],
            text_color=COLORS["text_primary"],
        ).pack(anchor="w", pady=(0, 15))

        # ═══════════════════════════════════
        #  USERS TABLE
        # ═══════════════════════════════════
        table_card = ctk.CTkFrame(
            self.frame, fg_color=COLORS["bg_card"],
            corner_radius=12, border_width=1,
            border_color=COLORS["border"],
        )
        table_card.pack(fill="both", expand=True, pady=(0, 15))

        self.tree = ttk.Treeview(
            table_card,
            columns=("Username", "Role"),
            show="headings", style="Dark.Treeview",
        )

        self.tree.heading("Username", text="Username")
        self.tree.heading("Role", text="Role")
        self.tree.column("Username", width=280, minwidth=180)
        self.tree.column("Role", width=150, anchor="center")

        # Role tags
        self.tree.tag_configure("admin", foreground=COLORS["accent_light"])
        self.tree.tag_configure("cashier", foreground=COLORS["success"])

        self.tree.pack(fill="both", expand=True, padx=10, pady=10)

        self.load_users()

        # ═══════════════════════════════════
        #  ADD USER FORM
        # ═══════════════════════════════════
        form_card = ctk.CTkFrame(
            self.frame, fg_color=COLORS["bg_card"],
            corner_radius=12, border_width=1,
            border_color=COLORS["border"],
        )
        form_card.pack(fill="x")

        ctk.CTkLabel(
            form_card, text="➕  Add New User",
            font=FONTS["heading_sm"],
            text_color=COLORS["text_primary"],
        ).pack(anchor="w", padx=20, pady=(15, 10))

        form_row = ctk.CTkFrame(form_card, fg_color="transparent")
        form_row.pack(fill="x", padx=20, pady=(0, 18))

        es = {
            "height": 40,
            "fg_color": COLORS["bg_input"],
            "border_color": COLORS["border"],
            "text_color": COLORS["text_primary"],
            "font": FONTS["body"],
            "corner_radius": 8,
        }

        self.username_entry = ctk.CTkEntry(
            form_row, placeholder_text="👤  Username",
            width=200, **es,
        )
        self.password_entry = ctk.CTkEntry(
            form_row, placeholder_text="🔒  Password",
            show="●", width=200, **es,
        )

        self.role_var = ctk.StringVar(value="cashier")
        role_menu = ctk.CTkOptionMenu(
            form_row, variable=self.role_var,
            values=["admin", "cashier"],
            width=130, height=40,
            fg_color=COLORS["bg_input"],
            button_color=COLORS["accent"],
            button_hover_color=COLORS["accent_hover"],
            text_color=COLORS["text_primary"],
            font=FONTS["body"],
            corner_radius=8,
        )

        self.username_entry.pack(side="left", padx=(0, 6))
        self.password_entry.pack(side="left", padx=(0, 6))
        role_menu.pack(side="left", padx=(0, 12))

        ctk.CTkButton(
            form_row, text="✓  Add User",
            width=120, height=40,
            fg_color=COLORS["accent"],
            hover_color=COLORS["accent_hover"],
            font=FONTS["body_bold"],
            corner_radius=8,
            command=self.add_user,
        ).pack(side="left", padx=(0, 6))

        ctk.CTkButton(
            form_row, text="🗑  Delete",
            width=100, height=40,
            fg_color=COLORS["danger"],
            hover_color="#d94040",
            font=FONTS["body_bold"],
            corner_radius=8,
            command=self.delete_user,
        ).pack(side="left")

    # ─── Load users into table ───
    def load_users(self):
        self.tree.delete(*self.tree.get_children())
        users = UserModel.get_users()

        for u in users:
            role = u.get("role", "cashier")
            self.tree.insert(
                "", "end",
                iid=str(u["_id"]),
                values=(u["username"], role.upper()),
                tags=(role,),
            )

    # ─── Add user ───
    def add_user(self):
        username = self.username_entry.get().strip()
        password = self.password_entry.get().strip()

        if not username or not password:
            error("Please fill in all fields")
            return

        try:
            AuthController.register(username, password, self.role_var.get())
            success("✅  User created successfully")

            self.username_entry.delete(0, "end")
            self.password_entry.delete(0, "end")
            self.load_users()

        except Exception as e:
            error(str(e))

    # ─── Delete user with confirmation ───
    def delete_user(self):
        selected = self.tree.focus()
        if not selected:
            error("Select a user to delete")
            return

        user = UserModel.find_by_id(selected)
        if not user:
            error("User not found")
            return

        # Safety: prevent deleting admin users
        if user["role"] == "admin":
            error("Cannot delete admin users")
            return

        if confirm(f"Are you sure you want to delete '{user['username']}'?"):
            UserModel.delete_user(selected)
            success("🗑  User deleted")
            self.load_users()