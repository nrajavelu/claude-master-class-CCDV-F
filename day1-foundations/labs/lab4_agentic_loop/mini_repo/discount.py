def apply_discount(price, percent):
    """Return price after a discount.

    percent is a fraction: 0.2 means 20% off, 1.0 means free.
    """
    if percent < 0 or percent > 1:
        raise ValueError("percent must be between 0 and 1")
    if percent > 1:
        return 0.0
    return round(price * (1 - percent), 2)
