"""
Receipt View — Sales history table with detail panel.
Uses the SaleController (MVC) instead of direct DB access.
"""

import os
import customtkinter as ctk
from tkinter import ttk
from controllers.sale_controller import SaleController
from utils.receipt import generate_pdf_receipt
from utils.notifications import success, error
from views.theme import COLORS, FONTS


class ReceiptView:

    def __init__(self, parent):
        self.frame = ctk.CTkFrame(parent, fg_color="transparent")
        self.frame.pack(fill="both", expand=True, padx=25, pady=25)

        # ─── Header ───
        header = ctk.CTkFrame(self.frame, fg_color="transparent")
        header.pack(fill="x", pady=(0, 15))

        ctk.CTkLabel(
            header, text="🧾  Sales History",
            font=FONTS["heading_lg"],
            text_color=COLORS["text_primary"],
        ).pack(side="left")

        # Refresh button
        ctk.CTkButton(
            header, text="🔄  Refresh",
            width=100, height=36,
            fg_color=COLORS["accent"],
            hover_color=COLORS["accent_hover"],
            font=FONTS["body_bold"],
            corner_radius=8,
            command=self._refresh,
        ).pack(side="right")

        # ═══════════════════════════════════
        #  SALES TABLE
        # ═══════════════════════════════════
        table_card = ctk.CTkFrame(
            self.frame, fg_color=COLORS["bg_card"],
            corner_radius=12, border_width=1,
            border_color=COLORS["border"],
        )
        table_card.pack(fill="both", expand=True, pady=(0, 15))

        self.tree = ttk.Treeview(
            table_card,
            columns=("Date", "Items", "Total"),
            show="headings", style="Dark.Treeview",
        )

        self.tree.heading("Date", text="Date & Time")
        self.tree.heading("Items", text="Items")
        self.tree.heading("Total", text="Total (DZD)")

        self.tree.column("Date", width=220, minwidth=160)
        self.tree.column("Items", width=80, anchor="center")
        self.tree.column("Total", width=130, anchor="center")

        scrollbar = ttk.Scrollbar(
            table_card, orient="vertical",
            command=self.tree.yview,
        )
        self.tree.configure(yscrollcommand=scrollbar.set)

        self.tree.pack(side="left", fill="both", expand=True, padx=(10, 0), pady=10)
        scrollbar.pack(side="right", fill="y", pady=10, padx=(0, 6))

        # ═══════════════════════════════════
        #  DETAIL PANEL
        # ═══════════════════════════════════
        self.detail_card = ctk.CTkFrame(
            self.frame, fg_color=COLORS["bg_card"],
            corner_radius=12, border_width=1,
            border_color=COLORS["border"],
        )
        self.detail_card.pack(fill="x")

        ctk.CTkLabel(
            self.detail_card,
            text="👆  Select a sale to view details",
            font=FONTS["body"],
            text_color=COLORS["text_muted"],
        ).pack(pady=20)

        # Bind selection
        self.tree.bind("<<TreeviewSelect>>", self._show_detail)

        # Track selected sale for printing
        self.selected_sale = None

        # Load data
        self.sales_data = []
        self._load_sales()

    # ─── Load sales into table (newest first) ───
    def _load_sales(self):
        self.tree.delete(*self.tree.get_children())
        self.sales_data = SaleController.get_sales()

        for i, s in enumerate(reversed(self.sales_data)):
            items_count = len(s.get("items", []))
            self.tree.insert(
                "", "end", iid=str(i),
                values=(
                    s.get("date", "N/A"),
                    items_count,
                    f"{s.get('total', 0):,.0f}",
                ),
            )

    # ─── Refresh ───
    def _refresh(self):
        self._load_sales()

        # Reset detail
        for w in self.detail_card.winfo_children():
            w.destroy()

        ctk.CTkLabel(
            self.detail_card,
            text="👆  Select a sale to view details",
            font=FONTS["body"],
            text_color=COLORS["text_muted"],
        ).pack(pady=20)

    # ─── Show sale detail ───
    def _show_detail(self, event=None):
        selected = self.tree.focus()
        if not selected:
            return

        # Reverse index since we display newest first
        idx = len(self.sales_data) - 1 - int(selected)
        if idx < 0 or idx >= len(self.sales_data):
            return

        sale = self.sales_data[idx]
        self.selected_sale = sale

        # Clear detail panel
        for w in self.detail_card.winfo_children():
            w.destroy()

        # Header
        ctk.CTkLabel(
            self.detail_card,
            text=f"📋  Sale Details  —  {sale.get('date', '')}",
            font=FONTS["heading_sm"],
            text_color=COLORS["text_primary"],
        ).pack(anchor="w", padx=18, pady=(14, 10))

        # Items list
        items = sale.get("items", [])
        if items:
            items_frame = ctk.CTkFrame(self.detail_card, fg_color="transparent")
            items_frame.pack(fill="x", padx=18)

            for item in items:
                qty = item.get("quantity", 1)
                price = item.get("price", 0)
                line_total = price * qty
                text = (
                    f"•  {item.get('name', 'Unknown')}"
                    f"   ×{qty}"
                    f"   @{price:,.0f}"
                    f"   =  {line_total:,.0f} DZD"
                )
                ctk.CTkLabel(
                    items_frame, text=text,
                    font=FONTS["body"],
                    text_color=COLORS["text_secondary"],
                ).pack(anchor="w", pady=1)
        else:
            ctk.CTkLabel(
                self.detail_card, text="No item details available",
                font=FONTS["body"],
                text_color=COLORS["text_muted"],
            ).pack(anchor="w", padx=18)

        # Total + Print row
        bottom_row = ctk.CTkFrame(self.detail_card, fg_color="transparent")
        bottom_row.pack(fill="x", padx=18, pady=(12, 16))

        ctk.CTkLabel(
            bottom_row,
            text=f"Total:  {sale.get('total', 0):,.0f}  DZD",
            font=FONTS["heading_sm"],
            text_color=COLORS["success"],
        ).pack(side="left")

        ctk.CTkButton(
            bottom_row, text="🖨  Print Receipt",
            width=140, height=36,
            fg_color=COLORS["accent"],
            hover_color=COLORS["accent_hover"],
            font=FONTS["body_bold"],
            corner_radius=8,
            command=self._print_receipt,
        ).pack(side="right")

    # ─── Print receipt for the selected sale ───
    def _print_receipt(self):
        if not self.selected_sale:
            error("No sale selected")
            return

        sale = self.selected_sale
        items = sale.get("items", [])
        total = sale.get("total", 0)

        if not items:
            error("No items in this sale to print")
            return

        try:
            # Generate the PDF receipt
            filepath = generate_pdf_receipt(items, total)

            # Open in default PDF viewer (user can print from there)
            os.startfile(filepath)
            success(f"🖨  Receipt opened — use Ctrl+P to print!")
        except OSError:
            # No PDF viewer — open the receipts folder instead
            folder = os.path.dirname(filepath)
            os.startfile(folder)
            success(f"📂  Receipt saved to receipts folder!")
        except Exception as e:
            error(f"Error: {e}")