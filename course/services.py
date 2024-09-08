import stripe
from django.conf import settings
from rest_framework.reverse import reverse

stripe.api_key = settings.STRIPE_API_KEY


def create_product(course):
    return stripe.Product.create(name=course.name)


def create_price(product, amount):
    return stripe.Price.create(
        product=product.get("id"), currency="rub", unit_amount=int(amount) * 100
    )


def create_session(price):
    session = stripe.checkout.Session.create(
        success_url="http://localhost:8000/course/courses/",
        line_items=[{"price": price.get("id"), "quantity": 1}],
        mode="payment",
    )
    return session.get("id"), session.get("url")
