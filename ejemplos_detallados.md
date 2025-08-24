# Ejemplos Detallados - Expresiones Lógicas SAT

Este documento muestra cómo convertir y probar las expresiones lógicas usando nuestro solver SAT.

## Formato de Entrada

Nuestro programa acepta fórmulas en **Forma Normal Conjuntiva (CNF)**:
- Cada cláusula en una línea separada
- Literales separados por espacios
- Use `-` para negación (ej: `-A` para ¬A)
- Escriba `FIN` para terminar la entrada

## Ejemplos de la Imagen

### 1. (p ∨ q) ∧ ¬p

**Conversión a CNF:**
- Ya está en CNF: (p ∨ q) ∧ (¬p)
- Cláusula 1: p ∨ q → `p q`
- Cláusula 2: ¬p → `-p`

**Entrada en el programa:**
```
Cláusula 1: p q
Cláusula 2: -p
Cláusula 3: FIN
```

**Resultado esperado:** SATISFACIBLE
**Solución:** p = F, q = V

---

### 2. (p → q) ∧ p

**Conversión a CNF:**
- p → q ≡ ¬p ∨ q
- Fórmula: (¬p ∨ q) ∧ p
- Cláusula 1: ¬p ∨ q → `-p q`
- Cláusula 2: p → `p`

**Entrada en el programa:**
```
Cláusula 1: -p q
Cláusula 2: p
Cláusula 3: FIN
```

**Resultado esperado:** SATISFACIBLE
**Solución:** p = V, q = V

---

### 3. (p ⊕ q) - XOR: "exactamente uno"

**Conversión a CNF:**
- p ⊕ q ≡ (p ∨ q) ∧ (¬p ∨ ¬q)
- Cláusula 1: p ∨ q → `p q`
- Cláusula 2: ¬p ∨ ¬q → `-p -q`

**Entrada en el programa:**
```
Cláusula 1: p q
Cláusula 2: -p -q
Cláusula 3: FIN
```

**Resultado esperado:** SATISFACIBLE
**Soluciones:** p = V, q = F ó p = F, q = V

---

### 4. (p ∨ q ∨ r) ∧ (¬p ∨ r) ∧ (¬r ∨ q)

**Conversión a CNF:**
- Ya está en CNF
- Cláusula 1: p ∨ q ∨ r → `p q r`
- Cláusula 2: ¬p ∨ r → `-p r`
- Cláusula 3: ¬r ∨ q → `-r q`

**Entrada en el programa:**
```
Cláusula 1: p q r
Cláusula 2: -p r
Cláusula 3: -r q
Cláusula 4: FIN
```

**Resultado esperado:** SATISFACIBLE
**Solución:** q = V (con cualquier p, r satisface todas)

---

### 5. (p ↔ q) ∧ (q ∨ r)

**Conversión a CNF:**
- p ↔ q ≡ (p → q) ∧ (q → p) ≡ (¬p ∨ q) ∧ (¬q ∨ p)
- Fórmula completa: (¬p ∨ q) ∧ (¬q ∨ p) ∧ (q ∨ r)
- Cláusula 1: ¬p ∨ q → `-p q`
- Cláusula 2: ¬q ∨ p → `-q p`
- Cláusula 3: q ∨ r → `q r`

**Entrada en el programa:**
```
Cláusula 1: -p q
Cláusula 2: -q p
Cláusula 3: q r
Cláusula 4: FIN
```

**Resultado esperado:** SATISFACIBLE
**Solución:** p = V, q = V, r = F

---

### 6. p ∨ ¬p (Tautología)

**Conversión a CNF:**
- Ya está en CNF: p ∨ ¬p
- Cláusula 1: p ∨ ¬p → `p -p`

**Entrada en el programa:**
```
Cláusula 1: p -p
Cláusula 2: FIN
```

**Resultado esperado:** SATISFACIBLE
**Solución:** Cualquier valuación (p = V ó p = F)

---

## Ejemplos Adicionales de Fórmulas No Satisfacibles

### Ejemplo 1: p ∧ ¬p (Contradicción)

**Entrada en el programa:**
```
Cláusula 1: p
Cláusula 2: -p
Cláusula 3: FIN
```

**Resultado esperado:** NO SATISFACIBLE

### Ejemplo 2: (p ∨ q) ∧ (¬p ∨ r) ∧ (¬q ∨ s) ∧ ¬r ∧ ¬s

**Entrada en el programa:**
```
Cláusula 1: p q
Cláusula 2: -p r
Cláusula 3: -q s
Cláusula 4: -r
Cláusula 5: -s
Cláusula 6: FIN
```

**Resultado esperado:** NO SATISFACIBLE

---

## Cómo Ejecutar los Ejemplos

1. **Ejecutar el programa:**
   ```
   py main.py
   ```

2. **Seleccionar algoritmo:**
   - Opción 1: Algoritmo de Fuerza Bruta
   - Opción 2: Algoritmo DPLL

3. **Ingresar la fórmula:**
   - Copie y pegue las cláusulas de los ejemplos
   - Termine con `FIN`

4. **Analizar resultados:**
   - El programa mostrará si es satisfacible
   - Si es satisfacible, mostrará una asignación válida
   - También mostrará estadísticas de ejecución

---

## Consejos para Crear Nuevos Ejemplos

1. **Conversión de operadores lógicos:**
   - `p → q` ≡ `¬p ∨ q`
   - `p ↔ q` ≡ `(¬p ∨ q) ∧ (¬q ∨ p)`
   - `p ⊕ q` ≡ `(p ∨ q) ∧ (¬p ∨ ¬q)`
   - `¬(p ∧ q)` ≡ `¬p ∨ ¬q` (De Morgan)
   - `¬(p ∨ q)` ≡ `¬p ∧ ¬q` (De Morgan)

2. **Verificación manual:**
   - Para fórmulas pequeñas, puede verificar manualmente
   - Use tablas de verdad para confirmar

3. **Comparación de algoritmos:**
   - Pruebe la misma fórmula con ambos algoritmos
   - Compare tiempos de ejecución y estadísticas
   - DPLL es más eficiente para fórmulas grandes
   - Fuerza bruta es útil para encontrar todas las soluciones

---

## Formato DIMACS (Alternativo)

Si prefiere usar formato DIMACS estándar:

```
p cnf 3 3
1 2 0
-1 3 0
-3 2 0
```

Donde:
- `p cnf [variables] [cláusulas]` es el encabezado
- Cada línea termina con `0`
- Variables se numeran desde 1
- `-` indica negación

Pero nuestro programa usa nombres de variables más intuitivos (A, B, C, p, q, r, etc.).