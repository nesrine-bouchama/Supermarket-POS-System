"""
Product model — MongoDB operations for the products collection.
"""

from config.db import products_collection
from bson import ObjectId


class ProductModel:

    @staticmethod
    def add_product(data):
        """Insert a new product document."""
        products_collection.insert_one(data)

    @staticmethod
    def get_products():
        """Return all products."""
        return list(products_collection.find())

    @staticmethod
    def update_quantity(product_id, qty):
        """Decrease product quantity by the given amount."""
        products_collection.update_one(
            {"_id": ObjectId(product_id)},
            {"$inc": {"quantity": -qty}}
        )

    @staticmethod
    def low_stock(threshold=5):
        """Return products with quantity at or below the threshold."""
        return list(products_collection.find({"quantity": {"$lte": threshold}}))

    @staticmethod
    def find_by_name(name):
        """Search products by name (case-insensitive regex)."""
        return list(products_collection.find(
            {"name": {"$regex": name, "$options": "i"}}
        ))

    @staticmethod
    def find_by_barcode(code):
        """Find a single product by its barcode."""
        return products_collection.find_one({"barcode": code})

    @staticmethod
    def delete_product(product_id):
        """Delete a product by its ObjectId string."""
        products_collection.delete_one({"_id": ObjectId(product_id)})

    @staticmethod
    def update_product(product_id, data):
        """Update a product's fields."""
        products_collection.update_one(
            {"_id": ObjectId(product_id)},
            {"$set": data}
        )

    @staticmethod
    def get_categories():
        """Return a sorted list of distinct product categories."""
        return sorted(products_collection.distinct("category"))

    @staticmethod
    def filter_products(category=None, min_price=None, max_price=None, name=None):
        """Filter products by category, price range, and/or name."""
        query = {}
        if category and category != "All":
            query["category"] = category
        if name:
            query["name"] = {"$regex": name, "$options": "i"}
        price_query = {}
        if min_price is not None:
            price_query["$gte"] = min_price
        if max_price is not None:
            price_query["$lte"] = max_price
        if price_query:
            query["price"] = price_query
        return list(products_collection.find(query))

    @staticmethod
    def out_of_stock():
        """Return products with quantity equal to 0."""
        return list(products_collection.find({"quantity": {"$lte": 0}}))