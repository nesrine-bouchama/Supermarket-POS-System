from config.db import sales_collection
from datetime import datetime

class SaleModel:

    @staticmethod
    def create_sale(cart, total):
        sales_collection.insert_one({
            "items": cart,
            "total": total,
            "date": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        })

    @staticmethod
    def get_sales():
        return list(sales_collection.find())