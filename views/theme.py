"""
Centralized theme configuration for the Supermarket POS System.
Supports Dark and Light modes with a toggle function.
"""

from tkinter import ttk
import customtkinter as ctk


# ============================================
# 🎨 DARK COLOR PALETTE
# ============================================
DARK_COLORS = {
    "bg_darkest":    "#08081a",
    "bg_dark":       "#0d0d2b",
    "bg_sidebar":    "#0f0f2d",
    "bg_card":       "#161640",
    "bg_card_hover": "#1e1e55",
    "bg_input":      "#12122e",
    "bg_header":     "#0a0a25",
    "accent":        "#635bff",
    "accent_hover":  "#7a74ff",
    "accent_light":  "#a5a0ff",
    "success":       "#3ecf8e",
    "warning":       "#f5a623",
    "danger":        "#f25a5a",
    "info":          "#4da6ff",
    "text_primary":  "#e8e8f0",
    "text_secondary": "#7a7a9b",
    "text_muted":    "#4a4a6b",
    "border":        "#2a2a50",
    "border_light":  "#3a3a60",
}

# ============================================
# ☀️ LIGHT COLOR PALETTE
# ============================================
LIGHT_COLORS = {
    "bg_darkest":    "#f0f2f5",
    "bg_dark":       "#e4e6eb",
    "bg_sidebar":    "#ffffff",
    "bg_card":       "#ffffff",
    "bg_card_hover": "#f0f0f8",
    "bg_input":      "#f5f5fa",
    "bg_header":     "#e8e8f0",
    "accent":        "#635bff",
    "accent_hover":  "#7a74ff",
    "accent_light":  "#4a42dd",
    "success":       "#0d9f6e",
    "warning":       "#d97706",
    "danger":        "#dc2626",
    "info":          "#2563eb",
    "text_primary":  "#1a1a2e",
    "text_secondary": "#555577",
    "text_muted":    "#8888aa",
    "border":        "#d0d0e0",
    "border_light":  "#e0e0ee",
}

# ============================================
# 🔄 ACTIVE COLORS (mutable — changes on toggle)
# ============================================
COLORS = dict(DARK_COLORS)

# Current mode tracker
_current_mode = "dark"


def get_mode():
    """Return the current theme mode ('dark' or 'light')."""
    return _current_mode


def toggle_mode():
    """Toggle between dark and light mode. Returns the new mode string."""
    global _current_mode
    if _current_mode == "dark":
        _current_mode = "light"
        COLORS.update(LIGHT_COLORS)
        ctk.set_appearance_mode("light")
    else:
        _current_mode = "dark"
        COLORS.update(DARK_COLORS)
        ctk.set_appearance_mode("dark")

    # Re-apply treeview styling for the new colors
    setup_treeview_style()
    return _current_mode


# ============================================
# 🔤 FONTS
# ============================================
FONTS = {
    "heading_xl":   ("Segoe UI", 28, "bold"),
    "heading_lg":   ("Segoe UI", 22, "bold"),
    "heading":      ("Segoe UI", 18, "bold"),
    "heading_sm":   ("Segoe UI", 14, "bold"),
    "body":         ("Segoe UI", 12),
    "body_sm":      ("Segoe UI", 11),
    "body_bold":    ("Segoe UI", 12, "bold"),
    "caption":      ("Segoe UI", 10),
    "button":       ("Segoe UI", 13, "bold"),
    "mono":         ("Consolas", 12),
}


# ============================================
# 🎨 COMMON ENTRY STYLE (reusable dict)
# ============================================
ENTRY_STYLE = {
    "height": 40,
    "fg_color": COLORS["bg_input"],
    "border_color": COLORS["border"],
    "text_color": COLORS["text_primary"],
    "font": FONTS["body"],
    "corner_radius": 10,
}


def setup_treeview_style():
    """Configure ttk Treeview to match the current theme."""
    style = ttk.Style()
    style.theme_use("clam")

    style.configure(
        "Dark.Treeview",
        background=COLORS["bg_card"],
        foreground=COLORS["text_primary"],
        fieldbackground=COLORS["bg_card"],
        borderwidth=0,
        rowheight=36,
        font=FONTS["body"],
    )

    style.configure(
        "Dark.Treeview.Heading",
        background=COLORS["bg_header"],
        foreground=COLORS["accent_light"],
        borderwidth=0,
        font=FONTS["body_bold"],
        padding=(10, 8),
    )

    style.map(
        "Dark.Treeview",
        background=[("selected", COLORS["accent"])],
        foreground=[("selected", "#ffffff")],
    )

    style.layout("Dark.Treeview", [
        ("Dark.Treeview.treearea", {"sticky": "nswe"})
    ])

    style.configure(
        "Dark.Vertical.TScrollbar",
        background=COLORS["bg_card"],
        troughcolor=COLORS["bg_dark"],
        borderwidth=0,
        arrowsize=0,
    )

    return style
