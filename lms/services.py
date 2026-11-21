import stripe
from django.conf import settings


stripe.api_key = settings.STRIPE_SECRET_KEY


def create_stripe_product(name: str) -> str:
    """Создает продукт в Stripe и возвращает его ID."""
    product = stripe.Product.create(name=name)
    return product.id


def create_stripe_price(product_id: str, amount_kopecks: int) -> str:
    """Создает цену в Stripe и возвращает её ID. Сумма в копейках!"""
    price = stripe.Price.create(
        product=product_id,
        unit_amount=amount_kopecks,
        currency="rub",
    )
    return price.id


def create_stripe_session(price_id: str, success_url: str, cancel_url: str) -> dict:
    """Создает сессию оплаты и возвращает объект сессии."""
    session = stripe.checkout.Session.create(
        # payment_method_types=['card'],
        line_items=[{
            'price': price_id,
            'quantity': 1,
        }],
        mode='payment',
        success_url=success_url,
        cancel_url=cancel_url,
    )
    return session


def get_stripe_session_status(session_id: str) -> str:
    """Возвращает статус сессии по её ID."""
    try:
        session = stripe.checkout.Session.retrieve(session_id)
        return session.payment_status
    except stripe.error.StripeError:
        return "error"
