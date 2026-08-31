"""A tiny module for Lab 1 to explain. Nothing here is important — it's just input."""


def average(values):
    """Return the arithmetic mean of ``values``. An empty list averages to 0.0."""
    if not values:
        return 0.0
    return sum(values) / len(values)


def find_extreme(values):
    if not values:
        return None
    return min(values), max(values)


def running_totals(values):
    total = 0
    out = []
    for v in values:
        total += v
        out.append(total)
    return out
