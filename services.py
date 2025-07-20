"""
This module contains the PricingEngine and CartService classes for managing
pricing calculations and cart operations in a smart shopping cart system.
"""

from models.model import Product, Customer, CartItem, db
from Constant import TAX_RATES, LOYALTY_DISCOUNTS

class PricingEngine:
    """
    PricingEngine is a class that provides methods for calculating item prices in a shopping cart.
    """

    @staticmethod
    def calculate_item_price(cart_item: CartItem):
        """
        Calculates the final price of a cart item, including base price, tax, and applicable discounts.
        Parameters:
            cart_item (CartItem): The cart item for which the price is to be calculated.
        Returns:
            dict: A dictionary containing the item's id, name, category, quantity, base price, tax, item discount, and final price.
        """
        product = cart_item.product

        if not product or product.quantity <= 0 or product.price < 0:
            return {}
        
        base_price = product.price * product.quantity
        tax = base_price * TAX_RATES.get(product.category, 0)

        discount = 0
        if product.category == "Electronics" and product.quantity > 2:
            discount = base_price * 0.15

        final_price = base_price + tax - discount
        return {
            "id": product.id,
            "name": product.name,
            "category": product.category,
            "quantity": product.quantity,
            "base_price": base_price,
            "tax": tax,
            "item_discount": discount,
            "final_price": final_price
        }

    @staticmethod
    def apply_bulk_discount(total):
        """
        Applies a bulk discount to the total if it exceeds a specified amount.
        
        Parameters:
            total (float): The total amount before discount.
        Returns:
            float: The bulk discount amount, or 0 if the total does not exceed the threshold.
        """
        return total * 0.10 if total > 200 else 0

    @staticmethod
    def apply_loyalty_discount(total, loyalty_level):
        """
        Applies a loyalty discount based on the customer's loyalty level.
        Parameters:
            total (float): The total amount before discount.
            loyalty_level (str): The loyalty level of the customer.
        Returns:
            float: The loyalty discount amount based on the loyalty level.
        """
        return total * LOYALTY_DISCOUNTS.get(loyalty_level, 0)


class CartService:
    """
    CartService is a service class that provides methods to manage a shopping cart.
    """
    @staticmethod
    def add_product(product_data):
        """
        Adds a new product to the database and creates a corresponding cart item.
        """
        if not all(k in product_data for k in ("name", "category", "price", "quantity")):
            raise ValueError("Missing product fields")

        product = Product(**product_data)
        db.session.add(product)
        db.session.commit()

        db.session.add(CartItem(product_id=product.id))
        db.session.commit()
    @staticmethod
    def remove_product(item_id):
        """
        Removes a product and its associated cart item from the database using the item ID.
        """
        if not Product.query.get(item_id):
            return False
        
        CartItem.query.filter_by(product_id=item_id).delete()
        Product.query.filter_by(id=item_id).delete()
        db.session.commit()
        return True

    @staticmethod
    def set_customer(data):
        """
        Sets or updates the customer information in the database, deleting any existing customer records.
        """

        Customer.query.delete()
        db.session.add(Customer(**data))
        db.session.commit()

    @staticmethod
    def calculate_cart_total():
        """
        Calculates the total cost of items in the cart, applying bulk and loyalty discounts.
        Returns:
             A dictionary containing itemized prices, subtotal, discounts, and final total.
        """
        cart_items = CartItem.query.all()
        customer = Customer.query.first()
        itemized = [PricingEngine.calculate_item_price(ci) for ci in cart_items]
        subtotal = sum(i['final_price'] for i in itemized)

        bulk_discount = PricingEngine.apply_bulk_discount(subtotal)
        after_bulk = subtotal - bulk_discount

        loyalty_discount = PricingEngine.apply_loyalty_discount(after_bulk, customer.loyalty_level if customer else "")
        final_total = after_bulk - loyalty_discount

        return {
            "items": itemized,
            "subtotal": subtotal,
            "bulk_discount": bulk_discount,
            "loyalty_discount": loyalty_discount,
            "total": final_total
        }
