def clip(number, min, max, fallback):
    if number is not None:
        return min if number < min else max if number > max else number
    else:
        return fallback
