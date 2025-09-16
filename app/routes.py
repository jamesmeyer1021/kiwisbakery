from flask import Flask, request, redirect, render_template, Blueprint, jsonify, session
import os
from datetime import datetime
from .config import DB_PARAMS,SECRET_KEY
from .sheets import log_order, log_order_item
from . import mail
from flask_mail import Message
import re

main = Blueprint('main', __name__)

@main.route('/')
def index():
    return render_template('order.html', current_year=datetime.now().year)

@main.route('/checkout', methods=['GET'])
def checkout():
    return render_template('checkout.html', current_year=datetime.now().year)

@main.route('/submit_order', methods=['POST'])
def submit_order():
    data = request.json
    EMAIL_REGEX = r"^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$"
    PHONE_REGEX = r"^\(?\d{3}\)?[-.\s]?\d{3}[-.\s]?\d{4}$"

    order_number = data.get('order_number', int(datetime.now().timestamp()))
    customer_name = data.get('customer_name')
    customer_email = data.get('customer_email')
    customer_phone = data.get('customer_phone')
    order_date = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    # Basic presence check
    if not customer_name:
        return jsonify({"status": "error", "message": "Missing customer name"}), 400
    if not customer_email:
        return jsonify({"status": "error", "message": "Missing email"}), 400
    if not customer_phone:
        return jsonify({"status": "error", "message": "Missing phone number"}), 400

    # Format validation
    if not re.match(EMAIL_REGEX, customer_email):
        return jsonify({"status": "error", "message": "Invalid email format"}), 400
    if not re.match(PHONE_REGEX, customer_phone):
        return jsonify({"status": "error", "message": "Invalid phone format"}), 400

    # Log the order
    log_order(order_number, customer_name, customer_email, customer_phone, order_date)

    items = data.get('items', [])

    # Loop through items and log each one
    for item in items:
        item_name = item.get('name')  # Adjusted to match your payload
        quantity = item.get('quantity')
        price = item.get('price')

        if not all([item_name, quantity, price]):
            print("Skipping incomplete item:", item)
            continue

        log_order_item(order_number, item_name, quantity, price)

    from flask_mail import Message

    msg = Message(
        subject="Your Kiwi's Bakery Order Confirmation",
        recipients=[customer_email]
    )

    msg.body = f"""
    Hi {customer_name},

    Thanks for your order! Here's what you got:

    Order #{order_number}

    Items:
    {chr(10).join([f"- {item['name']} × {item['quantity']} @ ${item['price']}" for item in items])}

    We'll be in touch when it's ready for pickup or delivery.

    Warmly,
    Kiwi's Bakery
    """

    mail.send(msg)

    return jsonify({"status": "success", "order_number": order_number})

@main.route('/orderSubmitted')
def orderSubmitted():
    return render_template('orderSubmitted.html')

@main.route('/privacy')
def privacy():
    return render_template('privacy.html')

@main.route('/terms')
def terms():
    return render_template('terms.html')

@main.route("/ping")
def ping():
    return "pong", 200