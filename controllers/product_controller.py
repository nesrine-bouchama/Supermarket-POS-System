"""
Product controller — business logic for product operations.
"""

from models.product_model import ProductModel


class ProductController:

    @staticmethod
    def add_product(data):
        """Add a new product with validation."""
        if not data.get("name", "").strip():
            raise ValueError("Product name is required")
        if not isinstance(data.get("price"), (int, float)) or data["price"] <= 0:
            raise ValueError("Price must be a positive number")
        if not isinstance(data.get("quantity"), int) or data["quantity"] < 0:
            raise ValueError("Quantity must be a non-negative integer")
        ProductModel.add_product(data)

    @staticmethod
    def get_products():
        """Return all products."""
        return ProductModel.get_products()

    @staticmethod
    def search(name):
        """Search products by name (case-insensitive)."""
        return ProductModel.find_by_name(name)

    @staticmethod
    def update_product(product_id, data):
        """Update an existing product with validation."""
        if not data.get("name", "").strip():
            raise ValueError("Product name is required")
        if not isinstance(data.get("price"), (int, float)) or data["price"] <= 0:
            raise ValueError("Price must be a positive number")
        if not isinstance(data.get("quantity"), int) or data["quantity"] < 0:
            raise ValueError("Quantity must be a non-negative integer")
        ProductModel.update_product(product_id, data)

    @staticmethod
    def filter_products(category=None, min_price=None, max_price=None, name=None):
        """Filter products by category, price range, and/or name."""
        return ProductModel.filter_products(category, min_price, max_price, name)

    @staticmethod
    def get_categories():
        """Return all distinct categories."""
        return ProductModel.get_categories()