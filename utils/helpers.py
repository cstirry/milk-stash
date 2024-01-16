def safe_divide(numerator, denominator):
    if numerator is None or denominator is None or denominator == 0:
        return 0
    else:
        return numerator / denominator
