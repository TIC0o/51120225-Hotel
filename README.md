# 🏨 Sistema de Reservas de Hotel - Testing Pack

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
# Foto

---
## Foto 1
<img width="958" height="821" alt="image" src="https://github.com/user-attachments/assets/d8a310e6-142b-42c2-8d6a-d6adc750cf33" />

---
## Foto 2
<img width="957" height="706" alt="image" src="https://github.com/user-attachments/assets/6f0dda7a-2339-4a86-9f00-7faf36a46a04" />

---
## Foto 3
<img width="960" height="707" alt="image" src="https://github.com/user-attachments/assets/81c488c5-c639-4eb6-b413-3b7734fd8cd8" />

---
## Foto 4
<img width="959" height="893" alt="image" src="https://github.com/user-attachments/assets/6edf6112-98f1-432c-b804-d4339775633f" />

---
## Foto 5
<img width="955" height="692" alt="image" src="https://github.com/user-attachments/assets/61916533-9d91-4e86-acea-0b2dcdfcf9e1" />

---
## Foto 6
<img width="523" height="736" alt="image" src="https://github.com/user-attachments/assets/3102d732-e6c3-465e-8c3d-068ef34cdfac" />
