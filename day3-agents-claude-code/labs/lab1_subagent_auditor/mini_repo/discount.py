def apply_discount(price, pct):
    return price - (price * pct / 100)


def tiered_price(qty, unit):
    if qty >= 100:
        return apply_discount(qty * unit, 15)
    if qty >= 10:
        return apply_discount(qty * unit, 5)
    return qty * unit
