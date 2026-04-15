"""
Notification helpers using tkinter messageboxes.
"""
import tkinter.messagebox as msg


def success(text):
    """Show a success info dialog."""
    msg.showinfo("Success", text)


def error(text):
    """Show an error dialog."""
    msg.showerror("Error", text)


def warning(text):
    """Show a warning dialog."""
    msg.showwarning("Warning", text)


def confirm(text):
    """Show a yes/no confirmation dialog. Returns True if user clicks Yes."""
    return msg.askyesno("Confirm", text)