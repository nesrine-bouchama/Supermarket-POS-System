"""
Dashboard Stats View — Admin overview with stat cards, low-stock alerts,
daily sales chart, and monthly sales report.
"""

import customtkinter as ctk
from controllers.product_controller import ProductController
from controllers.sale_controller import SaleController
from models.product_model import ProductModel
from views.theme import COLORS, FONTS

import matplotlib
matplotlib.use("TkAgg")
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure


class DashboardStats:

    def __init__(self, parent):
        # Scrollable frame for all content
        self.scroll = ctk.CTkScrollableFrame(parent, fg_color="transparent")
        self.scroll.pack(fill="both", expand=True, padx=25, pady=25)
        self.frame = self.scroll

        # ─── Header ───
        ctk.CTkLabel(
            self.frame, text="📊  Dashboard Overview",
            font=FONTS["heading_lg"],
            text_color=COLORS["text_primary"],
        ).pack(anchor="w", pady=(0, 20))

        # ─── Stat cards row ───
        cards = ctk.CTkFrame(self.frame, fg_color="transparent")
        cards.pack(fill="x", pady=(0, 20))
        cards.columnconfigure((0, 1, 2, 3, 4), weight=1)

        # Fetch data
        products = ProductController.get_products()
        low_stock = ProductModel.low_stock()
        out_of_stock = ProductModel.out_of_stock()
        revenue = SaleController.daily_report()
        sales = SaleController.get_sales()

        # Create stat cards (5 cards now including out-of-stock)
        self._stat_card(cards, "📦", "Total Products",
                        str(len(products)), COLORS["accent"], 0)
        self._stat_card(cards, "💰", "Total Revenue",
                        f"{revenue:,.0f} DZD", COLORS["success"], 1)
        self._stat_card(cards, "⚠️", "Low Stock",
                        str(len(low_stock)), COLORS["warning"], 2)
        self._stat_card(cards, "🚫", "Out of Stock",
                        str(len(out_of_stock)), COLORS["danger"], 3)
        self._stat_card(cards, "🧾", "Total Sales",
                        str(len(sales)), COLORS["info"], 4)

        # ─── Low stock list ───
        if low_stock:
            low_card = ctk.CTkFrame(
                self.frame, fg_color=COLORS["bg_card"],
                corner_radius=12, border_width=1,
                border_color=COLORS["border"],
            )
            low_card.pack(fill="x", pady=(0, 15))

            ctk.CTkLabel(
                low_card, text="⚠️  Low Stock Alerts",
                font=FONTS["heading_sm"],
                text_color=COLORS["warning"],
            ).pack(anchor="w", padx=20, pady=(15, 8))

            for item in low_stock:
                qty = item.get('quantity', 0)
                status = "OUT OF STOCK" if qty <= 0 else f"{qty} left"
                color = COLORS["danger"] if qty <= 0 else COLORS["warning"]
                text = f"  •  {item['name']}  —  {status}"
                ctk.CTkLabel(
                    low_card, text=text,
                    font=FONTS["body"],
                    text_color=color,
                ).pack(anchor="w", padx=25, pady=1)

            # Bottom padding
            ctk.CTkFrame(low_card, fg_color="transparent", height=12).pack()

        # ─── Daily sales chart ───
        chart_card = ctk.CTkFrame(
            self.frame, fg_color=COLORS["bg_card"],
            corner_radius=12, border_width=1,
            border_color=COLORS["border"],
        )
        chart_card.pack(fill="x", pady=(0, 15))

        ctk.CTkLabel(
            chart_card, text="📈  Daily Sales Trend",
            font=FONTS["heading_sm"],
            text_color=COLORS["text_primary"],
        ).pack(anchor="w", padx=20, pady=(15, 5))

        self._create_daily_chart(chart_card)

        # ─── Monthly sales report ───
        monthly_card = ctk.CTkFrame(
            self.frame, fg_color=COLORS["bg_card"],
            corner_radius=12, border_width=1,
            border_color=COLORS["border"],
        )
        monthly_card.pack(fill="x", pady=(0, 15))

        ctk.CTkLabel(
            monthly_card, text="📅  Monthly Sales Report",
            font=FONTS["heading_sm"],
            text_color=COLORS["text_primary"],
        ).pack(anchor="w", padx=20, pady=(15, 5))

        self._create_monthly_chart(monthly_card)

    # ─── Create a single stat card ───
    def _stat_card(self, parent, icon, label, value, color, col):
        card = ctk.CTkFrame(
            parent, fg_color=COLORS["bg_card"],
            corner_radius=12, border_width=1,
            border_color=COLORS["border"],
        )
        card.grid(row=0, column=col, padx=6, pady=5, sticky="nsew")

        inner = ctk.CTkFrame(card, fg_color="transparent")
        inner.pack(padx=16, pady=16)

        ctk.CTkLabel(inner, text=icon, font=("Segoe UI", 28)).pack()
        ctk.CTkLabel(
            inner, text=value,
            font=FONTS["heading"],
            text_color=color,
        ).pack(pady=(4, 2))
        ctk.CTkLabel(
            inner, text=label,
            font=FONTS["caption"],
            text_color=COLORS["text_secondary"],
        ).pack()

    # ─── Create the daily sales chart ───
    def _create_daily_chart(self, parent):
        data = SaleController.sales_per_day()

        if not data:
            ctk.CTkLabel(
                parent, text="No sales data yet — make some sales to see the chart!",
                font=FONTS["body"],
                text_color=COLORS["text_muted"],
            ).pack(pady=40)
            return

        days = list(data.keys())
        totals = list(data.values())

        fig = Figure(figsize=(9, 2.8), dpi=100)
        fig.patch.set_facecolor(COLORS["bg_card"])

        ax = fig.add_subplot(111)
        ax.set_facecolor(COLORS["bg_card"])

        # Plot line + fill
        ax.plot(
            days, totals,
            color=COLORS["accent"], linewidth=2.5,
            marker="o", markersize=7,
            markerfacecolor=COLORS["accent_light"],
            markeredgecolor=COLORS["accent"],
        )
        ax.fill_between(days, totals, alpha=0.08, color=COLORS["accent"])

        # Styling
        ax.set_xlabel("Date", color=COLORS["text_secondary"], fontsize=10)
        ax.set_ylabel("Revenue (DZD)", color=COLORS["text_secondary"], fontsize=10)
        ax.tick_params(colors=COLORS["text_muted"], labelsize=9)

        ax.spines["top"].set_visible(False)
        ax.spines["right"].set_visible(False)
        ax.spines["bottom"].set_color(COLORS["border"])
        ax.spines["left"].set_color(COLORS["border"])

        ax.grid(axis="y", color=COLORS["border"], alpha=0.3, linestyle="--")

        for lbl in ax.get_xticklabels():
            lbl.set_rotation(45)

        fig.tight_layout(pad=2)

        canvas = FigureCanvasTkAgg(fig, parent)
        canvas.draw()
        canvas.get_tk_widget().pack(fill="x", padx=10, pady=(0, 10))

    # ─── Create the monthly sales report chart ───
    def _create_monthly_chart(self, parent):
        data = SaleController.sales_per_month()

        if not data:
            ctk.CTkLabel(
                parent, text="No sales data yet — monthly report will appear here.",
                font=FONTS["body"],
                text_color=COLORS["text_muted"],
            ).pack(pady=40)
            return

        months = list(data.keys())
        totals = list(data.values())

        # Summary row
        summary = ctk.CTkFrame(parent, fg_color="transparent")
        summary.pack(fill="x", padx=20, pady=(5, 0))

        total_revenue = sum(totals)
        avg_monthly = total_revenue / len(months) if months else 0
        best_month = months[totals.index(max(totals))] if months else "N/A"

        stats_data = [
            ("Total Revenue", f"{total_revenue:,.0f} DZD", COLORS["success"]),
            ("Monthly Average", f"{avg_monthly:,.0f} DZD", COLORS["info"]),
            ("Best Month", f"{best_month}", COLORS["accent"]),
            ("Months Tracked", str(len(months)), COLORS["text_primary"]),
        ]

        for label, val, color in stats_data:
            frame = ctk.CTkFrame(summary, fg_color="transparent")
            frame.pack(side="left", padx=(0, 30))
            ctk.CTkLabel(
                frame, text=label,
                font=FONTS["caption"],
                text_color=COLORS["text_muted"],
            ).pack(anchor="w")
            ctk.CTkLabel(
                frame, text=val,
                font=FONTS["body_bold"],
                text_color=color,
            ).pack(anchor="w")

        # Bar chart
        fig = Figure(figsize=(9, 3), dpi=100)
        fig.patch.set_facecolor(COLORS["bg_card"])

        ax = fig.add_subplot(111)
        ax.set_facecolor(COLORS["bg_card"])

        bars = ax.bar(
            months, totals,
            color=COLORS["accent"],
            edgecolor=COLORS["accent_light"],
            linewidth=0.5,
            width=0.6,
            alpha=0.85,
        )

        # Add value labels on bars
        for bar, val in zip(bars, totals):
            ax.text(
                bar.get_x() + bar.get_width() / 2,
                bar.get_height() + max(totals) * 0.02,
                f"{val:,.0f}",
                ha="center", va="bottom",
                color=COLORS["text_secondary"],
                fontsize=8,
            )

        ax.set_xlabel("Month", color=COLORS["text_secondary"], fontsize=10)
        ax.set_ylabel("Revenue (DZD)", color=COLORS["text_secondary"], fontsize=10)
        ax.tick_params(colors=COLORS["text_muted"], labelsize=9)

        ax.spines["top"].set_visible(False)
        ax.spines["right"].set_visible(False)
        ax.spines["bottom"].set_color(COLORS["border"])
        ax.spines["left"].set_color(COLORS["border"])

        ax.grid(axis="y", color=COLORS["border"], alpha=0.3, linestyle="--")

        for lbl in ax.get_xticklabels():
            lbl.set_rotation(45)

        fig.tight_layout(pad=2)

        canvas = FigureCanvasTkAgg(fig, parent)
        canvas.draw()
        canvas.get_tk_widget().pack(fill="x", padx=10, pady=(5, 10))