# StockGuard — práctica de GitHub Actions

Práctica individual de la guía *Introducción práctica a GitHub Actions* (Big Data,
Ingeniería de Sistemas y Computación). Clasifica el riesgo de inventario de un producto
y lo valida automáticamente con GitHub Actions en cada push, Pull Request y ejecución
manual.

## Reglas

`clasificar_stock(stock_actual, stock_minimo)`:

| Condición | Resultado |
| --- | --- |
| `stock_actual == 0` | `AGOTADO` |
| `stock_actual <= 50 % del mínimo` | `CRITICO` |
| `stock_actual <= mínimo` | `BAJO` |
| en otro caso | `NORMAL` |
| negativo o mínimo `<= 0` | `ValueError` |

`clasificar_sobrestock(stock_actual, stock_maximo)` (regla propia, rama
`feature/alerta-sobrestock`):

| Condición | Resultado |
| --- | --- |
| `stock_actual > máximo` | `SOBRESTOCK` |
| `stock_actual >= 90 % del máximo` | `CERCA_DEL_LIMITE` |
| en otro caso | `OK` |
| negativo o máximo `<= 0` | `ValueError` |

## Ejecutar local

```bash
python -m pip install -r requirements.txt
pytest -v
```

## Evidencias

Ver [`RESPUESTAS.md`](RESPUESTAS.md).
