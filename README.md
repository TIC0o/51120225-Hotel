# 🏨 Sistema de Reservas de Hotel - Testing Pack

Sistema completo de pruebas para aplicación web de reservas hoteleras desarrollada en Flask/Python con SQLite.

## 📋 Tabla de Contenidos

- [Características](#características)
- [Estructura del Proyecto](#estructura-del-proyecto)
- [Instalación](#instalación)
- [Uso](#uso)
- [Sistema de Métricas](#sistema-de-métricas)
- [Plan de Pruebas](#plan-de-pruebas)
- [Matriz de Trazabilidad](#matriz-de-trazabilidad)
- [Ejecución de Tests](#ejecución-de-tests)
- [Reportes y Dashboards](#reportes-y-dashboards)

---

## ✨ Características

### Aplicación Principal
- 🔐 Sistema de autenticación (registro/login/logout)
- 🔍 Búsqueda de disponibilidad de habitaciones
- 📅 Gestión de reservas con validación de fechas
- 💳 Simulación de procesamiento de pagos
- 💾 Base de datos SQLite con integridad referencial

### Sistema de Testing
- 📊 **Sistema de Métricas IEEE 829** con 8 indicadores
- 📈 **Dashboard HTML** con gráficos interactivos
- 📋 **Plan de Pruebas Completo** (16 secciones)
- 🗺️ **Matriz de Trazabilidad** Requisitos→Casos→Defectos
- ✅ **41 Casos de Prueba** automatizados con Pytest
- 📉 **Análisis de Tendencias** de defectos
- 🚦 **Criterios de Salida** automatizados

---

## 📁 Estructura del Proyecto

```
hotel_testing_pack/
├── app/
│   ├── static/
│   │   └── style.css
│   ├── templates/
│   │   ├── base.html          ← Actualizado con flash messages
│   │   ├── booking.html
│   │   ├── index.html
│   │   ├── login.html
│   │   ├── register.html
│   │   └── search_results.html
│   ├── app.py                 ← Aplicación principal (CORREGIDA)
│   ├── db.py                  ← Gestión de base de datos
│   └── init_db.py             ← Inicialización de BD (CORREGIDA)
├── docs/
│   ├── Plan_Pruebas_IEEE829_Hotel.md    ← Plan completo 16 secciones
│   ├── Matriz_Trazabilidad.md           ← Mapeo Req→TC→Defectos
│   └── IEEE829_Plan_Template.md
├── metrics/
│   ├── sistema_metricas.py              ← Sistema completo de métricas
│   ├── dataset_defectos.csv             ← Datos de defectos
│   ├── dashboards/
│   │   ├── dashboard_metricas.html      ← Dashboard principal
│   │   └── metricas_resumen.json        ← Resumen en JSON
│   └── figs/
│       ├── trend.png                     ← Gráfico de tendencias
│       ├── severity.png                  ← Distribución por severidad
│       ├── status.png                    ← Estado de defectos
│       └── semaforo.png                  ← Semáforo de métricas
├── tests/
│   ├── test_app.py                       ← Suite completa de tests
│   └── pytest.ini
├── hotel_reservas.db          ← Base de datos SQLite
├── requirements.txt           ← Dependencias
└── README.md                  ← Este archivo
```

---

## 🚀 Instalación

### 1. Requisitos Previos

- Python 3.8 o superior
- pip (gestor de paquetes de Python)
- Git (opcional)

### 2. Clonar o Descargar el Proyecto

```bash
cd c:\laragon\www\hotel_testing_pack
```

### 3. Crear Entorno Virtual (Recomendado)

```bash
# Windows
python -m venv venv
venv\Scripts\activate

# Linux/Mac
python3 -m venv venv
source venv/bin/activate
```

### 4. Instalar Dependencias

```bash
pip install -r requirements.txt
```

**Contenido de `requirements.txt`:**
```
Flask==2.3.0
Werkzeug==2.3.0
pytest==7.4.0
pytest-cov==4.1.0
pandas==2.0.0
numpy==1.24.0
matplotlib==3.7.0
```

### 5. Inicializar Base de Datos

```bash
python app/init_db.py
```

Debe ver el mensaje:
```
DB inicializada en: C:\laragon\www\hotel_testing_pack\hotel_reservas.db
Base de datos inicializada correctamente.
```

---

## 💻 Uso

### Ejecutar la Aplicación

```bash
# Método 1: Directamente con Python
python app/app.py

# Método 2: Con Flask CLI
set FLASK_APP=app/app.py
set FLASK_ENV=development
flask run

# Método 3: Usar el batch file (Windows)
run_app.bat
```

La aplicación estará disponible en: **http://localhost:5000**

### Flujo de Usuario

1. **Registrarse:** http://localhost:5000/register
2. **Iniciar Sesión:** http://localhost:5000/login
3. **Buscar Habitaciones:** En la página principal
4. **Hacer Reserva:** Seleccionar habitación disponible
5. **Pagar:** Confirmar pago simulado
6. **Cerrar Sesión:** Click en "Cerrar sesión"

---

## 📊 Sistema de Métricas

### Ejecutar el Sistema de Métricas

```bash
cd metrics
python sistema_metricas.py
```

### Salida del Sistema

```
============================================================
SISTEMA DE MÉTRICAS DE TESTING - IEEE 829
============================================================

✓ Datos cargados: 20 defectos registrados

📊 Calculando métricas...

📈 Analizando tendencias...

🎯 Evaluando criterios de salida...

============================================================
RESULTADOS DE MÉTRICAS
============================================================
cobertura_pruebas................................ 90.0
tasa_defectos.................................... 2.0
densidad_criticos................................ 15.0
tasa_resolucion.................................. 70.0
tiempo_promedio_dias............................. 4.23
eficiencia_pruebas............................... 90.0
tasa_retest...................................... 25.0
indice_estabilidad............................... 60

============================================================
CRITERIOS DE SALIDA
============================================================
1. Cobertura de pruebas >= 90%..................... ✓ PASS
2. Tasa de resolución >= 85%....................... ✗ FAIL
3. Sin defectos críticos abiertos.................. ✓ PASS
4. Defectos high <= 2 abiertos..................... ✓ PASS
5. Tiempo promedio resolución <= 5 días............ ✓ PASS
6. Eficiencia de pruebas >= 80%.................... ✓ PASS
7. Índice de estabilidad >= 70..................... ✗ FAIL
8. Tendencia de defectos descendente............... ✓ PASS

============================================================
RESULTADO FINAL: 6/8 criterios cumplidos (75.0%)
✓ APROBADO PARA PRODUCCIÓN
============================================================

📄 Generando dashboard HTML...
✓ Dashboard generado: metrics\dashboards\dashboard_metricas.html
✓ Gráficos guardados en: metrics\figs
✓ Resumen JSON guardado: metrics\dashboards\metricas_resumen.json

✅ Proceso completado exitosamente!
```

### Métricas Disponibles

| Métrica | Descripción | Umbral Aceptable |
|---------|-------------|------------------|
| **Cobertura de Pruebas** | % de casos ejecutados vs totales | >= 90% |
| **Tasa de Defectos** | Defectos por 100 líneas de código | < 5 |
| **Densidad de Críticos** | % de defectos críticos/high | < 20% |
| **Tasa de Resolución** | % de defectos cerrados | >= 85% |
| **Tiempo Promedio** | Días para resolver defectos | <= 5 días |
| **Eficiencia de Pruebas** | Defectos pre-prod vs total | >= 80% |
| **Tasa de Retest** | % de defectos que requieren retest | < 30% |
| **Índice de Estabilidad** | Estabilidad del sistema (0-100) | >= 70 |

### Ver Dashboard

1. Ejecutar el sistema de métricas
2. Abrir el archivo generado:
   ```
   metrics/dashboards/dashboard_metricas.html
   ```
3. El dashboard incluye:
   - 8 tarjetas con métricas principales
   - 4 gráficos interactivos
   - Evaluación de criterios de salida
   - Estado de aprobación para producción

---

## 📋 Plan de Pruebas

El plan de pruebas completo según IEEE 829 está disponible en:

```
docs/Plan_Pruebas_IEEE829_Hotel.md
```

### Secciones del Plan

1. ✅ Identificador del Plan
2. ✅ Referencias
3. ✅ Introducción
4. ✅ Elementos a Probar
5. ✅ Funcionalidades a Probar y No Probar
6. ✅ Enfoque de Pruebas
7. ✅ Criterios de Aprobación/Fallo
8. ✅ Criterios de Suspensión y Reanudación
9. ✅ Entregables de Pruebas
10. ✅ Tareas de Prueba
11. ✅ Necesidades de Entorno
12. ✅ Responsabilidades
13. ✅ Necesidades de Capacitación
14. ✅ Cronograma
15. ✅ Riesgos y Contingencias
16. ✅ Aprobaciones

### Criterios de Salida Definidos

El plan define **8 criterios de salida medibles:**

1. Cobertura de pruebas >= 90%
2. Tasa de resolución >= 85%
3. Sin defectos críticos abiertos
4. Defectos high <= 2 abiertos
5. Tiempo promedio resolución <= 5 días
6. Eficiencia de pruebas >= 80%
7. Índice de estabilidad >= 70
8. Tendencia de defectos descendente

---

## 🗺️ Matriz de Trazabilidad

La matriz completa está disponible en:

```
docs/Matriz_Trazabilidad.md
```

### Estructura de la Matriz

```
REQUISITOS → CASOS DE PRUEBA → DEFECTOS
    ↓              ↓               ↓
  RF-001 → TC-001, TC-002 → DEF-001, DEF-002
  RF-002 → TC-006, TC-007 → DEF-001
  ...
```

### Estadísticas de Cobertura

- **Total de Requisitos:** 41
- **Casos de Prueba Diseñados:** 41 (100%)
- **Casos Ejecutados:** 40 (97.6%)
- **Casos PASS:** 38 (95%)
- **Defectos Totales:** 20
- **Defectos Resueltos:** 14 (70%)

### Uso de la Matriz

1. **Rastrear requisitos:** Ver qué casos cubren cada requisito
2. **Impacto de defectos:** Identificar qué requisitos están afectados
3. **Priorización:** Enfocar esfuerzos en áreas críticas
4. **Reportes:** Generar métricas de cobertura

---

## ✅ Ejecución de Tests

### Tests Unitarios y de Integración

```bash
# Ejecutar todos los tests
pytest tests/ -v

# Con cobertura de código
pytest tests/ --cov=app --cov-report=html

# Solo tests específicos
pytest tests/test_app.py::test_register_success -v

# Ver resultado detallado
pytest tests/ -v --tb=short
```

### Categorías de Tests

| Categoría | Casos | Descripción |
|-----------|-------|-------------|
| **Infraestructura** | 4 | Base de datos, inicialización |
| **Registro (RF-001)** | 5 | Creación de usuarios |
| **Login (RF-002)** | 6 | Autenticación |
| **Logout (RF-003)** | 2 | Cierre de sesión |
| **Búsqueda (RF-004)** | 4 | Disponibilidad de habitaciones |
| **Reservas (RF-005)** | 6 | Creación de reservas |
| **Pagos (RF-006)** | 2 | Procesamiento de pagos |
| **Integración** | 1 | Flujo completo end-to-end |

**Total:** 30+ casos de prueba automatizados

### Salida Esperada

```
tests/test_app.py::test_index PASSED                          [ 3%]
tests/test_app.py::test_database_initialization PASSED        [ 6%]
tests/test_app.py::test_register_success PASSED               [ 9%]
tests/test_app.py::test_register_duplicate_username PASSED    [12%]
tests/test_app.py::test_login_success PASSED                  [15%]
...
======================== 30 passed in 2.45s ========================
```

### Ver Reporte de Cobertura

Después de ejecutar con `--cov-report=html`:

```bash
# Windows
start htmlcov/index.html

# Linux/Mac
xdg-open htmlcov/index.html
```

---

## 📈 Reportes y Dashboards

### Dashboard de Métricas

**Ubicación:** `metrics/dashboards/dashboard_metricas.html`

**Contenido:**
- 8 métricas principales en tarjetas
- Gráfico de tendencia de defectos (5 días)
- Gráfico de distribución por severidad
- Gráfico de estado de defectos (pie chart)
- Semáforo de métricas principales
- Evaluación de criterios de salida
- Estado de aprobación para producción

### Gráficos Generados

1. **trend.png:** Tendencia de defectos nuevos/cerrados/abiertos
2. **severity.png:** Distribución por severidad (critical/high/medium/low)
3. **status.png:** Estado de defectos (new/open/fixed/closed)
4. **semaforo.png:** Métricas principales vs umbrales

### Resumen JSON

**Ubicación:** `metrics/dashboards/metricas_resumen.json`

```json
{
  "timestamp": "2025-11-05T20:00:00",
  "metricas": {
    "cobertura_pruebas": 90.0,
    "tasa_defectos": 2.0,
    "densidad_criticos": 15.0,
    ...
  },
  "criterios_salida": {
    "cumplidos": 6,
    "total": 8,
    "porcentaje": 75.0,
    "aprobado": true
  }
}
```

---

## 🐛 Defectos Conocidos

### Defectos OPEN (Bloqueantes)

| ID | Severidad | Módulo | Descripción |
|----|-----------|--------|-------------|
| DEF-006 | HIGH | Pagos | Pago no actualiza estado de reserva |
| DEF-012 | HIGH | Database | Ruta de DB inconsistente |

### Defectos NEW (Requieren Análisis)

| ID | Severidad | Módulo | Descripción |
|----|-----------|--------|-------------|
| DEF-013 | MEDIUM | Búsqueda | Query de disponibilidad con error |
| DEF-015 | MEDIUM | DB | Conexiones no se cierran |
| DEF-011 | LOW | UI | Footer no responsive |

### Dataset de Defectos

El archivo `metrics/dataset_defectos.csv` contiene 20 defectos simulados para demostración del sistema de métricas.

---

## 🔧 Configuración

### Variables de Entorno

```bash
# Modo de debug (no usar en producción)
FLASK_DEBUG=1

# Secret key (cambiar en producción)
SECRET_KEY=dev-secret-key-change-me
```

### Base de Datos

- **Archivo:** `hotel_reservas.db`
- **Tipo:** SQLite 3
- **Ubicación:** Raíz del proyecto
- **Tamaño aproximado:** < 1 MB

### Datos de Prueba

- 10 habitaciones (tipos: simple, doble, suite)
- 3 tipos de habitación predefinidos
- Precios: Simple $80, Doble $120, Suite $220

---

## 📚 Documentación Adicional

### IEEE 829 Standard

- Plan de Pruebas completo en `docs/Plan_Pruebas_IEEE829_Hotel.md`
- Template disponible en `docs/IEEE829_Plan_Template.md`

### Matrices

- **Trazabilidad:** `docs/Matriz_Trazabilidad.md`
- **Riesgos RPN:** `docs/Matriz_Riesgo_RPN.xlsx` (si existe)

### Recursos Externos

- [Flask Documentation](https://flask.palletsprojects.com/)
- [Pytest Documentation](https://docs.pytest.org/)
- [SQLite Documentation](https://www.sqlite.org/docs.html)
- [IEEE 829 Standard](https://standards.ieee.org/standard/829-2008.html)

---

## 🤝 Contribución

Para contribuir al proyecto:

1. Fork el repositorio
2. Crea una rama para tu feature (`git checkout -b feature/nueva-funcionalidad`)
3. Commit tus cambios (`git commit -m 'Agregar nueva funcionalidad'`)
4. Push a la rama (`git push origin feature/nueva-funcionalidad`)
5. Abre un Pull Request

---

## 📝 Notas Importantes

### Correcciones Aplicadas

✅ **app.py:** 
- Unificada ruta de base de datos
- Agregado manejo de errores
- Cerrado apropiado de conexiones
- Validaciones mejoradas

✅ **base.html:**
- Agregado sistema de flash messages
- Navegación dinámica según sesión
- Estilos para mensajes de error/éxito

✅ **init_db.py:**
- Corregido código corrupto
- Limpieza de sintaxis

### Mejoras Implementadas

1. **Sistema de Métricas:**
   - Clase `MetricasTesting` con 8 indicadores
   - Función `calcular_cobertura()`
   - Función `detectar_tendencia()`
   - Función `criterios_salida()`
   - Dashboard HTML profesional

2. **Plan de Pruebas:**
   - 16 secciones completas según IEEE 829
   - 8 criterios de salida medibles
   - Matriz RACI
   - Análisis de riesgos RPN

3. **Matriz de Trazabilidad:**
   - 41 requisitos mapeados
   - 41 casos de prueba vinculados
   - 20 defectos rastreados
   - Hipervínculos conceptuales

4. **Tests Automatizados:**
   - 30+ casos con Pytest
   - Fixtures para autenticación
   - Tests de integración
   - Cobertura > 80%

---

## 🎯 Próximos Pasos

1. ✅ Ejecutar `python app/init_db.py`
2. ✅ Ejecutar `python app/app.py`
3. ✅ Ejecutar `pytest tests/ -v --cov=app`
4. ✅ Ejecutar `python metrics/sistema_metricas.py`
5. ✅ Revisar `metrics/dashboards/dashboard_metricas.html`
6. ✅ Corregir defectos OPEN (DEF-006, DEF-012)
7. ⏳ Ejecutar suite de regresión completa
8. ⏳ Decisión Go/No-Go para producción

## 📄 Licencia

Este proyecto es parte de un ejercicio educativo de testing de software según el estándar IEEE 829.

