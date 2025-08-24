# Solver SAT - Algoritmos DPLL y Fuerza Bruta

Implementación completa de dos algoritmos para resolver el problema de satisfacibilidad booleana (SAT) en Python: el algoritmo Davis-Putnam-Logemann-Loveland (DPLL) y el algoritmo de Fuerza Bruta.

## 📋 Descripción

Este proyecto implementa el algoritmo DPLL, un algoritmo completo de backtracking utilizado para determinar la satisfacibilidad de fórmulas proposicionales en Forma Normal Conjuntiva (CNF). El algoritmo incluye optimizaciones como propagación unitaria, eliminación de literales puros y diferentes heurísticas de ramificación.

## ✨ Características

### Algoritmos Implementados
- **Algoritmo DPLL completo** con backtracking sistemático
- **Algoritmo de Fuerza Bruta** que prueba todas las asignaciones posibles
- **Comparación directa** entre ambos algoritmos

### Optimizaciones DPLL
- **Propagación unitaria** automática
- **Eliminación de literales puros**
- **Múltiples heurísticas** de selección de variables:
  - First: Primera variable disponible
  - Most Frequent: Variable más frecuente
  - Jeroslow-Wang: Heurística basada en pesos

### Funcionalidades Generales
- **Menú interactivo** simplificado para selección de algoritmo
- **Ejemplos predefinidos** para aprendizaje
- **Análisis de fórmulas** con estadísticas detalladas
- **Búsqueda de todas las soluciones** (ambos algoritmos)
- **Guardar/cargar fórmulas** en formato DIMACS
- **Benchmark y pruebas** de rendimiento
- **Modo verbose** para seguimiento de pasos

## 🚀 Instalación

### Requisitos
- Python 3.7 o superior
- No se requieren dependencias externas

### Instalación
1. Clone o descargue el proyecto
2. Navegue al directorio del proyecto
3. Ejecute el programa principal:

```bash
python main.py
```

## 📁 Estructura del Proyecto

```
Proyecto SAT Solver/
├── main.py                    # Programa principal con menú interactivo
├── dpll_solver.py            # Implementación del algoritmo DPLL
├── brute_force_solver.py     # Implementación del algoritmo de fuerza bruta
├── cnf_formula.py            # Clase para representar fórmulas CNF
├── utils.py                  # Funciones auxiliares y utilidades
├── examples.py               # Ejemplos predefinidos y benchmarks
├── ejemplos_detallados.md    # Ejemplos detallados con conversiones CNF
├── requirements.txt          # Dependencias del proyecto
└── README.md                # Este archivo
```

## 🎯 Uso

### Menú Principal

Al ejecutar `python main.py`, se presenta un menú simplificado para seleccionar el algoritmo:

1. **Algoritmo de Fuerza Bruta**: Prueba todas las posibles asignaciones
2. **Algoritmo DPLL**: Utiliza backtracking inteligente con optimizaciones

Cada algoritmo incluye:
- Ingreso de fórmulas CNF personalizadas
- Ejemplos predefinidos
- Análisis de fórmulas con estadísticas
- Búsqueda de todas las soluciones
- Guardar/cargar fórmulas
- Modo verbose para seguimiento detallado

### Formato de Entrada

#### Ingreso Manual
Para ingresar fórmulas manualmente, use el siguiente formato:
- Cada cláusula en una línea separada
- Literales separados por espacios
- Use `-` para negación (ej: `-A` para ¬A)
- Escriba `FIN` para terminar

**Ejemplo:**
```
Cláusula 1: A B
Cláusula 2: -A C
Cláusula 3: -B -C
Cláusula 4: FIN
```

#### Formato DIMACS
Para archivos, se soporta el formato DIMACS estándar:
```
c Comentario
p cnf 3 3
1 2 0
-1 3 0
-2 -3 0
```

## ⚙️ Configuración

### Heurísticas Disponibles

1. **First**: Selecciona la primera variable disponible
   - Rápida pero puede no ser óptima
   - Buena para fórmulas pequeñas

2. **Most Frequent**: Selecciona la variable más frecuente
   - Balancea velocidad y calidad
   - Recomendada para uso general

3. **Jeroslow-Wang**: Heurística basada en pesos de cláusulas
   - Más sofisticada y generalmente mejor rendimiento
   - Recomendada para fórmulas complejas

### Opciones de Visualización

- **Modo Verbose**: Muestra información detallada durante la ejecución
- **Mostrar Pasos**: Visualiza cada paso del algoritmo
- **Estadísticas**: Presenta métricas de rendimiento

## 📊 Análisis y Estadísticas

El programa proporciona análisis detallado de las fórmulas:

- Número de variables y cláusulas
- Tamaño promedio, máximo y mínimo de cláusulas
- Detección de cláusulas unitarias
- Identificación de literales puros
- Tiempo de ejecución
- Nodos explorados en el árbol de búsqueda
- Número de propagaciones unitarias
- Número de literales puros eliminados

## 🧪 Testing y Benchmark

El proyecto incluye herramientas de testing:

### Ejemplos Predefinidos
- Fórmulas satisfacibles e insatisfacibles
- Casos que demuestran diferentes técnicas
- Casos especiales (fórmula vacía, cláusula vacía)

### Benchmark Automático
- Generación de fórmulas aleatorias
- Medición de tiempo de ejecución
- Estadísticas de rendimiento
- Análisis de escalabilidad

## 📚 Algoritmos Implementados

### Algoritmo de Fuerza Bruta

#### Descripción Técnica
El algoritmo de fuerza bruta es un enfoque exhaustivo que:

1. **Genera todas las asignaciones**: Crea todas las combinaciones posibles de valores para las variables
2. **Evaluación sistemática**: Prueba cada asignación contra la fórmula CNF
3. **Garantía de completitud**: Si existe una solución, la encontrará

#### Complejidad
- **Tiempo**: O(2^n × m) donde n es el número de variables y m el número de cláusulas
- **Espacio**: O(n) para almacenar la asignación actual

#### Ventajas
- Implementación simple y directa
- Garantiza encontrar la solución si existe
- Puede encontrar todas las soluciones fácilmente
- Útil para fórmulas pequeñas y propósitos educativos

#### Desventajas
- Complejidad exponencial
- Ineficiente para fórmulas con muchas variables
- No utiliza técnicas de optimización

### Algoritmo DPLL

#### Descripción Técnica
El algoritmo DPLL es un procedimiento completo para el problema SAT que combina:

1. **Propagación Unitaria**: Cuando una cláusula contiene un solo literal no asignado, ese literal debe ser verdadero
2. **Eliminación de Literales Puros**: Si una variable aparece solo en forma positiva o negativa, se puede asignar para satisfacer todas sus cláusulas
3. **Backtracking**: Búsqueda sistemática con retroceso cuando se encuentra una contradicción

#### Complejidad
- **Tiempo**: O(2^n) en el peor caso, donde n es el número de variables
- **Espacio**: O(n) para la pila de recursión

#### Ventajas
- Mucho más eficiente que fuerza bruta en la práctica
- Utiliza optimizaciones inteligentes
- Escalable para fórmulas grandes
- Estándar en la industria

#### Optimizaciones Implementadas
- Detección temprana de conflictos
- Simplificación de fórmulas
- Heurísticas de ramificación inteligentes
- Reutilización de cálculos

### Comparación de Algoritmos

| Aspecto | Fuerza Bruta | DPLL |
|---------|--------------|------|
| **Complejidad** | O(2^n × m) | O(2^n) |
| **Eficiencia** | Baja | Alta |
| **Implementación** | Simple | Compleja |
| **Escalabilidad** | Limitada | Buena |
| **Uso recomendado** | Aprendizaje, fórmulas pequeñas | Producción, fórmulas grandes |
| **Todas las soluciones** | Fácil | Requiere modificaciones |

## 🔗 Referencias

- Davis, M., & Putnam, H. (1960). "A computing procedure for quantification theory"
- Davis, M., Logemann, G., & Loveland, D. (1962). "A machine program for theorem-proving"
- Jeroslow, R. G., & Wang, J. (1990). "Solving propositional satisfiability problems"

---