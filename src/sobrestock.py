"""Regla propia: detecta sobrestock frente a la capacidad maxima del producto."""

UMBRAL_LIMITE = 0.9


def clasificar_sobrestock(stock_actual: int, stock_maximo: int) -> str:
    if stock_actual < 0:
        raise ValueError("El stock actual no puede ser negativo")
    if stock_maximo <= 0:
        raise ValueError("El stock maximo debe ser mayor que cero")
    if stock_actual > stock_maximo:
        return "SOBRESTOCK"
    if stock_actual >= stock_maximo * UMBRAL_LIMITE:
        return "CERCA_DEL_LIMITE"
    return "OK"
