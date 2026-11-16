# Titan Haul Lab

Laboratorio académico reproducible de tiempos de ciclo de acarreo. **Todos los datos son sintéticos**; este repositorio no estima el rendimiento de una faena real.

## Pregunta e hipótesis

Pregunta: ¿cómo cambia el tiempo total de ciclo cuando se reduce el tiempo de espera en carga? Hipótesis de simulación: si los demás componentes permanecen iguales, reducir la cola reduce el tiempo total en la misma cantidad. La relación es una propiedad del modelo aditivo, no un hallazgo empírico.

## Ejecutar

Requiere Python 3.10 o superior y no instala dependencias.

```powershell
python haul_lab.py --seed 42 --cycles 120 --queue-reduction 0.30 --output results
```

Genera `results/cycles.csv` y `results/summary.json`. Para ejecutar las pruebas:

```powershell
python -m unittest discover -s tests -v
```

## Modelo

Cada ciclo simulado suma viaje cargado, espera en carga, carga, viaje vacío y descarga. Ambos escenarios usan las mismas observaciones base; el escenario alternativo reduce solo la espera en carga. El generador usa una semilla fija para reproducibilidad. Las unidades son minutos. El resumen reporta media y mediana, sin pruebas de significación ni afirmaciones causales sobre operaciones reales.

## Límites

No modela tráfico, capacidad de ruta, variabilidad por equipo, clima, seguridad ni restricciones de despacho. No sirve para tomar decisiones operacionales.

## Licencia

MIT.
