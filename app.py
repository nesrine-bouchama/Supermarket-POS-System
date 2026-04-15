"""
Supermarket POS System — Entry Point.
Launches the login window with dark theme.
"""

import customtkinter as ctk
from views.login_view import LoginView

# Global appearance
ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")

if __name__ == "__main__":
    app = LoginView()
    app.mainloop()