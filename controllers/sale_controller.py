"""
Sale controller — handles sale processing, reporting, and receipt generation.
"""

from models.sale_model import SaleModel
from models.product_model import ProductModel
from utils.receipt import generate_pdf_receipt
from collections import defaultdict


class SaleController:

    @staticmethod
    def process_sale(cart):
        """
        Process a sale: deduct stock, record in DB, generate receipt.
        Returns (total, receipt_filepath).
        """
        total = sum(item["price"] * item["quantity"] for item in cart)

        for item in cart:
            ProductModel.update_quantity(item["_id"], item["quantity"])

        SaleModel.create_sale(cart, total)
        filepath = generate_pdf_receipt(cart, total)

        return total, filepath

    @staticmethod
    def daily_report():
        """Return total revenue across all sales."""
        sales = SaleModel.get_sales()
        return sum(s["total"] for s in sales)

    @staticmethod
    def sales_per_day():
        """Return a dict of {date_str: total_revenue} grouped by day."""
        sales = SaleModel.get_sales()
        data = defaultdict(int)
        for s in sales:
            day = s["date"][:10]  # YYYY-MM-DD
            data[day] += s["total"]
        return dict(data)

    @staticmethod
    def get_sales():
        """Return all sales records."""
        return SaleModel.get_sales()

    @staticmethod
    def sales_per_month():
        """Return a dict of {YYYY-MM: total_revenue} grouped by month."""
        sales = SaleModel.get_sales()
        data = defaultdict(int)
        for s in sales:
            month = s["date"][:7]  # YYYY-MM
            data[month] += s["total"]
        return dict(data)