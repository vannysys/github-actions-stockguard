# Taller GitHub Actions — StockGuard

**Estudiante:** Luis Jaraba (`vannysys`)
**Repositorio:** https://github.com/vannysys/github-actions-stockguard

## Evidencias

| Evidencia | Link |
| --- | --- |
| Ejecución exitosa inicial (Run #2) | https://github.com/vannysys/github-actions-stockguard/actions/runs/40806026424 |
| Ejecución fallida intencional (Run #3) | https://github.com/vannysys/github-actions-stockguard/actions/runs/40806246331 |
| Ejecución corregida (Run #4) | https://github.com/vannysys/github-actions-stockguard/actions/runs/40806682762 |
| Pull Request con los checks de Actions | https://github.com/vannysys/github-actions-stockguard/pull/1 |
| Ejecución manual `workflow_dispatch` (Run #7) | https://github.com/vannysys/github-actions-stockguard/actions/runs/40808001873 |
| Regla propia (sobrestock) | https://github.com/vannysys/github-actions-stockguard/pull/1 |

## Respuestas

**1. Ejecución exitosa y fallida.**
La ejecución exitosa inicial fue el Run #2, producido por el commit
`fix: configurar pythonpath para que pytest encuentre src`. El Run #1 había fallado
porque pytest no encontraba el paquete `src` (`ModuleNotFoundError: No module named
'src'`); se corrigió agregando `pytest.ini` con `pythonpath = .`. La ejecución fallida
intencional fue el Run #3, producido por el commit `a6e6fc7`
(`test: provocar fallo controlado de CI`), donde cambié la expectativa de
`test_stock_critico` a `"NORMAL"`. El step que determinó el resultado fue
*Ejecutar pruebas*: compileall pasó, pero pytest terminó con `1 failed, 4 passed` y el
proceso salió con exit code 1. El Run #4 restauró la prueba y volvió a verde.

**2. ¿Por qué pytest local no reemplaza pytest en Actions?**
Porque mi máquina no es neutral: ya tiene librerías instaladas, archivos que quizás no
subí y una versión de Python concreta. El runner de Actions arranca limpio, descarga
solo lo que está en el repo e instala solo lo que dice `requirements.txt`. Si pasa ahí,
pasa para cualquiera del equipo. Además queda registrado en GitHub, y un compañero
puede ver el resultado sin confiar en mi palabra.

**3. Riesgo de mergear sin esperar los checks.**
Que entre a `main` código que rompe pruebas o ni siquiera compila, y el error le aparece
al siguiente que haga pull, que no tiene por qué saber qué lo causó. En un equipo de tres
eso bloquea a los otros dos.

**4. Línea esencial del error.**
`AssertionError: assert 'CRITICO' == 'NORMAL'`
Me dijo exactamente qué devolvió la función (`CRITICO`) y qué esperaba la prueba
(`NORMAL`). Con 7 unidades y mínimo 20, 7 ≤ 10 (50 % de 20), así que `CRITICO` es lo
correcto: el error estaba en la prueba, no en la función.

**5. `uses:` vs `run:`.**
`uses:` ejecuta una acción ya hecha y versionada por otros (por ejemplo
`actions/checkout@v6` descarga el repo, `actions/setup-python@v5` instala Python).
`run:` ejecuta comandos de shell que yo escribo (`pip install`, `pytest -v`). Uno
reutiliza, el otro define la verificación propia del proyecto.

**6. `${{ github.actor }}` en `run-name`.**
Pone el usuario que disparó la corrida en el nombre de la ejecución
("CI ejecutado por vannysys"). En un equipo sirve para saber quién hizo cada push o
quién lanzó una ejecución manual sin abrir el detalle, y es evidencia de participación
individual, que es justamente para lo que el proyecto pide el `workflow_dispatch`.

**7. Si Actions pasa pero Docker falla localmente.**
No significa que Actions no sirva: significa que verifica otra cosa. El workflow
comprueba sintaxis, reglas de negocio con pytest y que la configuración sea válida
(`docker compose config`), pero no levanta Kafka ni Spark. Errores de red entre
contenedores, puertos ocupados o falta de memoria solo aparecen en la corrida
integrada, que se valida aparte.

**8. Tres checks para la variante 7 (experiencia del cliente).**

| Check | Error concreto que evita |
| --- | --- |
| Pruebas de bordes de A1 y A2 (`3.59` con `n=20` → warning, `3.60` → sin alerta, `0.30` con 10 reclamos → warning, `0.50` → critical) | Que un `<` cambiado por `<=` haga sonar (o callar) la alerta de caída de calificación o de concentración de reclamos. |
| Pruebas de las reglas de rechazo del contrato (rating fuera de 1..5, canal inválido, `occurred_at` futuro, rating ≤ 3 sin motivo) | Que eventos inválidos entren a `processed` y contaminen los KPIs. |
| `docker compose config --quiet` + verificación de estructura del pipeline (`verify_pipeline --structure-only`) | Un compose con indentación rota, o un job de Spark que deja de aceptar `--lake-dir`/`--once` y rompe la corrida integrada sin que nadie lo note. |

**9. ¿Cuál primero?**
Las pruebas de bordes de A1 y A2, porque son la razón de ser de la variante: si la
alerta suena mal, todo el pipeline puede funcionar y aun así dar una respuesta
equivocada al negocio. Además son lógica pura, rápidas y no dependen de Docker.

**10. Prueba demasiado costosa para cada push.**
La corrida end-to-end: levantar Kafka, publicar 300 eventos, correr los dos jobs de
Spark en contenedor y leer el lake. Tarda minutos, descarga la imagen de Spark y el
conector, y puede fallar por la red o la memoria del runner aunque el código esté bien.
La valido con un script (`python -m scripts.verify_pipeline`) que corremos en local
antes de cada checkpoint y cuyo resumen queda como evidencia; en CI solo corre su modo
`--structure-only`.
