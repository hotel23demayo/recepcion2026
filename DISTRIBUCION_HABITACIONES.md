# 🏨 HOTEL 23 DE MAYO - Distribución de Habitaciones

## 📊 Información General

- **Total de habitaciones:** 53
- **Total de pisos:** 3
- **Capacidad total:** 114 plazas

---

## 🏢 Distribución por Pisos

### PISO 1 - 21 habitaciones (101-121)
**Rango:** 101 a 121

| Hab | Tipo | Hab | Tipo | Hab | Tipo | Hab | Tipo |
|-----|------|-----|------|-----|------|-----|------|
| 101 | X    | 102 | X    | 103 | X    | 104 | II   |
| 105 | X    | 106 | X    | 107 | X    | 108 | II   |
| 109 | X    | 110 | X    | 111 | X    | 112 | X    |
| 113 | X    | 114 | II   | 115 | X    | 116 | III  |
| 117 | III  | 118 | X    | 119 | X    | 120 | X    |
| 121 | X    |      |      |      |      |      |      |

### PISO 2 - 21 habitaciones (222-242)
**Rango:** 222 a 242

| Hab | Tipo | Hab | Tipo | Hab | Tipo | Hab | Tipo |
|-----|------|-----|------|-----|------|-----|------|
| 222 | X    | 223 | II   | 224 | II   | 225 | X    |
| 226 | X    | 227 | X    | 228 | X    | 229 | X    |
| 230 | X    | 231 | II   | 232 | II   | 233 | X    |
| 234 | X    | 235 | X    | 236 | X    | 237 | III  |
| 238 | III  | 239 | X    | 240 | IIII | 241 | X    |
| 242 | X    |      |      |      |      |      |      |

### PISO 3 - 11 habitaciones (343-353)
**Rango:** 343 a 353

| Hab | Tipo | Hab | Tipo | Hab | Tipo | Hab | Tipo |
|-----|------|-----|------|-----|------|-----|------|
| 343 | X    | 344 | X    | 345 | X    | 346 | X    |
| 347 | X    | 348 | X    | 349 | II   | 350 | II   |
| 351 | X    | 352 | X    | 353 | II   |      |      |

---

## 🛏️ Tipos de Habitación

### Nomenclatura
- **X** = Matrimonial (1 cama doble)
- **II** = 2 camas individuales
- **III** = 3 camas (puede ser matrimonial + individual o 3 individuales)
- **XI** = Matrimonial + individual
- **XII** = Matrimonial + 2 individuales
- **IIII** = 4 camas (departamento cuádruple)

### Distribución por Tipo

| Tipo | Cantidad | Descripción |
|------|----------|-------------|
| **X** | 38 | Matrimoniales |
| **II** | 15 | Dobles individuales |
| **III** | 3 | Triples |
| **IIII** | 1 | Cuádruple (solo hab. 240) |
| **TOTAL** | **53** | |

---

## 🔧 Configuración en el Sistema

### Rangos Configurados

```python
PISO_RANGES = {
    'PISO_1': (101, 121),  # 21 habitaciones
    'PISO_2': (222, 242),  # 21 habitaciones
    'PISO_3': (343, 353),  # 11 habitaciones
}
```

### ⚠️ Importante

- **PISO 1:** Las habitaciones van del 101 al 121 (SIN SALTOS)
- **PISO 2:** Las habitaciones van del 222 al 242 (NO desde 201, comienza en 222)
- **PISO 3:** Las habitaciones van del 343 al 353 (NO desde 301, comienza en 343)

### Habitaciones que NO existen

El sistema NO debe buscar estas habitaciones (no existen en el hotel):
- 122 a 199
- 200 a 221
- 243 a 299
- 300 a 342
- 354 en adelante

---

## 📋 Uso del Sistema

### Importación Automática

Cuando importas un CSV, el sistema automáticamente:

1. **Detecta el piso** según el número de habitación:
   - 101-121 → PISO 1
   - 222-242 → PISO 2
   - 343-353 → PISO 3

2. **Distribuye los datos** a la pestaña correspondiente

3. **Ignora habitaciones inválidas** (fuera de los rangos)

### Ejemplo de Distribución

```
CSV contiene:
- Habitación 105 → Se distribuye a PISO 1 ✅
- Habitación 225 → Se distribuye a PISO 2 ✅
- Habitación 350 → Se distribuye a PISO 3 ✅
- Habitación 150 → Solo en Ingresos, NO se distribuye ⚠️
- Habitación 201 → Solo en Ingresos, NO se distribuye ⚠️
```

---

## 📍 Ubicación Física

Según el mapa del hotel:

```
         CALLE SALTA
    ┌─────────────────┐
    │  PISO 1 y 2     │
    │  (21 hab c/u)   │
    └─────────────────┘

         CALLE SALTA
    ┌─────────────────┐
    │  PISO 3         │
    │  (11 hab)       │
    └─────────────────┘
```

---

## 📝 Notas

- Capacidad total: **114 plazas** (considerando todas las camas disponibles)
- La habitación 240 (IIII) es la única cuádruple del hotel
- Existen 3 habitaciones triples (116, 117, 237, 238)
- La mayoría son matrimoniales (X): 38 de 53 habitaciones

---

**Documento generado:** 28 de Noviembre de 2025  
**Fuente:** Estado Original Hab.ods (mapa oficial del hotel)
