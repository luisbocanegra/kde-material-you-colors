def clip(number, min, max, fallback):
    if number != None:
        return min if number < min else max if number > max else number
    else:
        return fallback
