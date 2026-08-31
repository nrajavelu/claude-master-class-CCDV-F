from discount import apply_discount


def cart_total(items, member_discount=0.0):
    """items: list of (unit_price, quantity). Returns the discounted total."""
    subtotal = sum(price * qty for price, qty in items)
    return apply_discount(subtotal, member_discount)
