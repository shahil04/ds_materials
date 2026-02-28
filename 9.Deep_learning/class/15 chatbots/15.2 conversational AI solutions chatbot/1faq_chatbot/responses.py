# responses.py

def get_response(user_input):
    user_input = user_input.lower()

    if "hello" in user_input or "hi" in user_input:
        return "Hello! 👋 How can I assist you today?"

    elif "refund" in user_input:
        return "Refunds are processed within 5–7 business days after product return confirmation."

    elif "return" in user_input:
        return "You can initiate a return from your account under 'Orders' → 'Return Item'."

    elif "delivery" in user_input:
        return "Standard delivery takes 3–5 business days. You can track it from your order page."

    elif "cancel order" in user_input or "cancellation" in user_input:
        return "You can cancel your order within 24 hours of placing it."

    elif "payment" in user_input:
        return "We accept payments via credit card, debit card, UPI, and PayPal."

    elif "contact" in user_input or "support" in user_input:
        return "You can reach our support team at 📧 support@easysolution.com or ☎️ +91-9876543210."

    elif "price" in user_input or "cost" in user_input:
        return "Our prices vary depending on the product category. Please visit the pricing page for details."

    elif "thank" in user_input:
        return "You're welcome! 😊 Happy to help."

    else:
        return "I'm sorry, I didn’t quite understand that. Please try asking about delivery, refund, or return."
