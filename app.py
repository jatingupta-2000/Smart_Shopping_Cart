"""
This application provides endpoints to interact with a shopping cart, allowing users to add items, 
remove items, retrieve the cart total, and set customer information.
"""

from flask import Flask, request, jsonify
from flask_cors import CORS  # type: ignore
from models.db_connection import db
from services import CartService
from models.model import Product, Customer, CartItem


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///smart_ecommerce_system.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db.init_app(app)
CORS(app)

import logging
app.logger.setLevel(logging.DEBUG)


@app.route("/cart", methods=["GET"])
def get_cart():
    """
    Returns the total amount of the shopping cart.
    """
    try:
        return jsonify(CartService.calculate_cart_total()), 200
    except Exception as e:
        return jsonify({"error": "Failed to fetch cart total", "details": str(e)}), 500


@app.route("/cart", methods=["POST"])
def add_item():
    """
    Adds products to the cart from the request JSON.
    """
    try:
        data = request.get_json(force=True)
        items = data.get("Items")

        if not isinstance(items, list) or not items:
            return jsonify({"error": "'Items' must be a non-empty list"}), 400

        for i, item in enumerate(items):
            if not all(k in item for k in ("name", "category", "price", "quantity")):
                return jsonify({"error": f"Missing fields in item {i}"}), 400

            CartService.add_product(item)

        return jsonify({"message": "All items added to cart"}), 201

    except Exception as e:
        return jsonify({"error": "Invalid input", "details": str(e)}), 400


@app.route("/cart/<int:item_id>", methods=["DELETE"])
def remove_item(item_id):
    """
    Removes a specific item from the cart.
    """
    try:
        removed = CartService.remove_product(item_id)
        if removed:
            return jsonify({"message": "Item removed"}), 200
        return jsonify({"error": "Item not found"}), 404
    except Exception as e:
        return jsonify({"error": "Failed to remove item", "details": str(e)}), 400


@app.route("/customer", methods=["POST"])
def set_customer():
    """
    Sets customer info in the cart.
    """
    try:
        data = request.get_json(force=True)
        customer = data.get("Customer")

        if not isinstance(customer, dict) or not customer:
            return jsonify({"error": "'Customer' must be a valid object"}), 400
    

        CartService.set_customer(customer)
        return jsonify({"message": "Customer set"}), 200

    except Exception as e:
        return jsonify({"error": "Invalid input", "details": str(e)}), 400



#Main Function
if __name__ == "__main__":
    with app.app_context():
        db.create_all()
    app.run(debug=True,host="0.0.0.0", port=5000)
