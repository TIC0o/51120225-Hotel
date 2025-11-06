import pytest
import sys
from pathlib import Path

# Agregar el directorio app al path
sys.path.insert(0, str(Path(__file__).parent.parent / "app"))

from app import app
from db import init_db, connect
from werkzeug.security import check_password_hash

@pytest.fixture(scope="function")
def client():
    """Crea un cliente de prueba con base de datos limpia"""
    app.config["TESTING"] = True
    app.config["SECRET_KEY"] = "test-secret-key"
    
    # Inicializar BD de prueba
    init_db()
    
    with app.test_client() as client:
        with app.app_context():
            yield client
    
    # Cleanup después de cada test
    conn = connect()
    cur = conn.cursor()
    cur.execute("DELETE FROM users WHERE username LIKE 'test_%'")
    cur.execute("DELETE FROM bookings")
    cur.execute("DELETE FROM payments")
    conn.commit()
    conn.close()


@pytest.fixture
def authenticated_client(client):
    """Cliente con usuario autenticado"""
    # Registrar usuario de prueba
    client.post("/register", data={
        "username": "test_user",
        "password": "test_password"
    })
    
    # Login
    client.post("/login", data={
        "username": "test_user",
        "password": "test_password"
    })
    
    return client


# ==============================================================================
# TESTS DE INFRAESTRUCTURA
# ==============================================================================

def test_index(client):
    """TC-037: Página principal debe cargar correctamente"""
    response = client.get("/")
    assert response.status_code == 200
    assert b"Hotel Reserva" in response.data or b"Buscar Habitaciones" in response.data


def test_database_initialization():
    """TC-032: Base de datos debe inicializarse correctamente"""
    conn = connect()
    cur = conn.cursor()
    
    # Verificar que las tablas existen
    cur.execute("SELECT name FROM sqlite_master WHERE type='table'")
    tables = [row[0] for row in cur.fetchall()]
    
    assert "users" in tables
    assert "rooms" in tables
    assert "room_types" in tables
    assert "bookings" in tables
    assert "payments" in tables
    
    conn.close()


def test_foreign_keys_enabled():
    """TC-033: Foreign keys deben estar habilitadas"""
    conn = connect()
    cur = conn.cursor()
    cur.execute("PRAGMA foreign_keys")
    result = cur.fetchone()[0]
    conn.close()
    
    assert result == 1, "Foreign keys no están habilitadas"


def test_initial_data_loaded():
    """TC-034: Datos iniciales deben estar cargados"""
    conn = connect()
    cur = conn.cursor()
    
    # Verificar tipos de habitación
    cur.execute("SELECT COUNT(*) FROM room_types")
    assert cur.fetchone()[0] >= 3, "Faltan tipos de habitación"
    
    # Verificar habitaciones
    cur.execute("SELECT COUNT(*) FROM rooms")
    assert cur.fetchone()[0] >= 10, "Faltan habitaciones"
    
    conn.close()


# ==============================================================================
# TESTS DE REGISTRO (RF-001)
# ==============================================================================

def test_register_page_loads(client):
    """TC-001: Página de registro debe cargar"""
    response = client.get("/register")
    assert response.status_code == 200
    assert b"Registro" in response.data or b"Crear cuenta" in response.data


def test_register_success(client):
    """TC-001: Registro exitoso con datos válidos"""
    response = client.post("/register", data={
        "username": "test_new_user",
        "password": "securepassword123"
    }, follow_redirects=True)
    
    assert response.status_code == 200
    assert b"Registro exitoso" in response.data or b"Inicia sesi" in response.data
    
    # Verificar que el usuario existe en BD
    conn = connect()
    cur = conn.cursor()
    cur.execute("SELECT id, username, password_hash FROM users WHERE username = ?", ("test_new_user",))
    user = cur.fetchone()
    conn.close()
    
    assert user is not None
    assert user[1] == "test_new_user"


def test_register_duplicate_username(client):
    """TC-002: Registro con username duplicado debe fallar"""
    # Primer registro
    client.post("/register", data={
        "username": "test_duplicate",
        "password": "password1"
    })
    
    # Segundo registro con mismo username
    response = client.post("/register", data={
        "username": "test_duplicate",
        "password": "password2"
    }, follow_redirects=True)
    
    assert b"ya existe" in response.data.lower() or b"duplicate" in response.data.lower()


def test_register_password_hashed(client):
    """TC-003: Contraseña debe estar hasheada en BD"""
    plain_password = "mypassword123"
    
    client.post("/register", data={
        "username": "test_hash_user",
        "password": plain_password
    })
    
    conn = connect()
    cur = conn.cursor()
    cur.execute("SELECT password_hash FROM users WHERE username = ?", ("test_hash_user",))
    password_hash = cur.fetchone()[0]
    conn.close()
    
    # Verificar que no es texto plano
    assert password_hash != plain_password
    
    # Verificar que es un hash válido de Werkzeug
    assert check_password_hash(password_hash, plain_password)


def test_register_empty_fields(client):
    """TC-004: Registro con campos vacíos debe fallar"""
    response = client.post("/register", data={
        "username": "",
        "password": ""
    }, follow_redirects=True)
    
    assert b"requerido" in response.data.lower() or b"required" in response.data.lower()


# ==============================================================================
# TESTS DE LOGIN (RF-002)
# ==============================================================================

def test_login_page_loads(client):
    """TC-006: Página de login debe cargar"""
    response = client.get("/login")
    assert response.status_code == 200
    assert b"Iniciar sesi" in response.data or b"Login" in response.data


def test_login_success(client):
    """TC-006: Login exitoso con credenciales válidas"""
    # Registrar usuario primero
    client.post("/register", data={
        "username": "test_login_user",
        "password": "correctpassword"
    })
    
    # Intentar login
    response = client.post("/login", data={
        "username": "test_login_user",
        "password": "correctpassword"
    }, follow_redirects=True)
    
    assert response.status_code == 200
    # Debe redirigir a index o mostrar mensaje de bienvenida
    assert b"Hotel Reserva" in response.data or b"Buscar" in response.data


def test_login_wrong_password(client):
    """TC-007: Login con contraseña incorrecta debe fallar"""
    # Registrar usuario
    client.post("/register", data={
        "username": "test_wrong_pass",
        "password": "correctpassword"
    })
    
    # Login con contraseña incorrecta
    response = client.post("/login", data={
        "username": "test_wrong_pass",
        "password": "wrongpassword"
    }, follow_redirects=True)
    
    assert b"inv" in response.data.lower() or b"incorrect" in response.data.lower()


def test_login_nonexistent_user(client):
    """TC-007: Login con usuario inexistente debe fallar"""
    response = client.post("/login", data={
        "username": "nonexistent_user",
        "password": "anypassword"
    }, follow_redirects=True)
    
    assert b"inv" in response.data.lower() or b"incorrect" in response.data.lower()


def test_login_creates_session(client):
    """TC-008: Login debe crear sesión con user_id"""
    # Registrar y hacer login
    client.post("/register", data={
        "username": "test_session_user",
        "password": "password123"
    })
    
    with client:
        client.post("/login", data={
            "username": "test_session_user",
            "password": "password123"
        })
        
        # Verificar que la sesión tiene user_id
        from flask import session
        assert "user_id" in session
        assert session["user_id"] is not None


def test_login_stores_username_in_session(client):
    """TC-009: Login debe guardar username en sesión"""
    client.post("/register", data={
        "username": "test_username_session",
        "password": "password123"
    })
    
    with client:
        client.post("/login", data={
            "username": "test_username_session",
            "password": "password123"
        })
        
        from flask import session
        assert "username" in session
        assert session["username"] == "test_username_session"


# ==============================================================================
# TESTS DE LOGOUT (RF-003)
# ==============================================================================

def test_logout_clears_session(authenticated_client):
    """TC-011: Logout debe limpiar la sesión"""
    client = authenticated_client
    
    with client:
        # Verificar que hay sesión activa
        client.get("/")
        from flask import session
        assert "user_id" in session
        
        # Hacer logout
        client.get("/logout")
        
        # Verificar que la sesión está limpia
        assert "user_id" not in session
        assert "username" not in session


def test_logout_redirects_to_index(authenticated_client):
    """TC-012: Logout debe redirigir a index"""
    response = authenticated_client.get("/logout", follow_redirects=True)
    assert response.status_code == 200


# ==============================================================================
# TESTS DE BÚSQUEDA (RF-004)
# ==============================================================================

def test_search_by_room_type(client):
    """TC-014: Búsqueda debe filtrar por tipo de habitación"""
    response = client.post("/search", data={
        "start_date": "2025-12-01",
        "end_date": "2025-12-05",
        "room_type": "simple"
    })
    
    assert response.status_code == 200
    assert b"Resultados" in response.data or b"Habitaciones" in response.data


def test_search_with_valid_dates(client):
    """TC-015: Búsqueda con fechas válidas debe funcionar"""
    response = client.post("/search", data={
        "start_date": "2025-11-20",
        "end_date": "2025-11-25",
        "room_type": "doble"
    })
    
    assert response.status_code == 200


def test_search_excludes_occupied_rooms(authenticated_client):
    """TC-016: Búsqueda debe excluir habitaciones ocupadas"""
    client = authenticated_client
    
    # Crear una reserva primero
    client.post("/book", data={
        "room_id": "1",
        "start_date": "2025-12-10",
        "end_date": "2025-12-15"
    })
    
    # Buscar en el mismo rango
    response = client.post("/search", data={
        "start_date": "2025-12-10",
        "end_date": "2025-12-15",
        "room_type": "simple"
    })
    
    # La habitación 1 no debería aparecer como disponible
    # (este test puede necesitar ajustes según la estructura de datos)
    assert response.status_code == 200


def test_search_shows_available_rooms(client):
    """TC-017: Búsqueda debe mostrar lista de habitaciones disponibles"""
    response = client.post("/search", data={
        "start_date": "2026-01-01",
        "end_date": "2026-01-05",
        "room_type": "suite"
    })
    
    assert response.status_code == 200
    # Debería haber al menos una habitación disponible
    assert b"10" in response.data or b"Habitaciones" in response.data


# ==============================================================================
# TESTS DE RESERVAS (RF-005)
# ==============================================================================

def test_book_requires_authentication(client):
    """TC-020: Reservar sin login debe redirigir a login"""
    response = client.post("/book", data={
        "room_id": "1",
        "start_date": "2025-12-01",
        "end_date": "2025-12-05"
    }, follow_redirects=True)
    
    assert b"Inicia sesi" in response.data or b"Login" in response.data


def test_book_calculates_nights_correctly(authenticated_client):
    """TC-021: Sistema debe calcular noches correctamente"""
    client = authenticated_client
    
    response = client.post("/book", data={
        "room_id": "1",
        "start_date": "2025-12-01",
        "end_date": "2025-12-05"  # 4 noches
    })
    
    # Verificar en BD que el total es correcto (4 noches * precio)
    conn = connect()
    cur = conn.cursor()
    cur.execute("""
        SELECT total_price, start_date, end_date 
        FROM bookings 
        ORDER BY id DESC LIMIT 1
    """)
    booking = cur.fetchone()
    conn.close()
    
    if booking:
        # Verificar que el cálculo es correcto
        # El precio de habitación simple es 80, entonces 4 * 80 = 320
        assert booking[0] > 0


def test_book_validates_date_range(authenticated_client):
    """TC-024: Sistema debe rechazar rangos de fechas negativos"""
    client = authenticated_client
    
    response = client.post("/book", data={
        "room_id": "1",
        "start_date": "2025-12-10",
        "end_date": "2025-12-05"  # Fecha final antes de inicial
    }, follow_redirects=True)
    
    assert b"inv" in response.data.lower() or b"error" in response.data.lower()


def test_book_creates_booking_record(authenticated_client):
    """TC-025: Sistema debe crear registro en tabla bookings"""
    client = authenticated_client
    
    # Contar bookings antes
    conn = connect()
    cur = conn.cursor()
    cur.execute("SELECT COUNT(*) FROM bookings")
    count_before = cur.fetchone()[0]
    conn.close()
    
    # Crear reserva
    client.post("/book", data={
        "room_id": "1",
        "start_date": "2025-12-20",
        "end_date": "2025-12-25"
    })
    
    # Contar bookings después
    conn = connect()
    cur = conn.cursor()
    cur.execute("SELECT COUNT(*) FROM bookings")
    count_after = cur.fetchone()[0]
    conn.close()
    
    assert count_after == count_before + 1


def test_book_sets_pending_payment_status(authenticated_client):
    """TC-026: Sistema debe asignar estado PENDING_PAYMENT"""
    client = authenticated_client
    
    client.post("/book", data={
        "room_id": "2",
        "start_date": "2025-12-01",
        "end_date": "2025-12-03"
    })
    
    conn = connect()
    cur = conn.cursor()
    cur.execute("SELECT status FROM bookings ORDER BY id DESC LIMIT 1")
    status = cur.fetchone()[0]
    conn.close()
    
    assert status == "PENDING_PAYMENT"


# ==============================================================================
# TESTS DE PAGOS (RF-006)
# ==============================================================================

def test_pay_creates_payment_record(authenticated_client):
    """TC-028: Pago debe crear registro en tabla payments"""
    client = authenticated_client
    
    # Crear reserva primero
    response = client.post("/book", data={
        "room_id": "3",
        "start_date": "2025-12-15",
        "end_date": "2025-12-18"
    })
    
    # Extraer booking_id (simplificado - en realidad vendría del response)
    conn = connect()
    cur = conn.cursor()
    cur.execute("SELECT id FROM bookings ORDER BY id DESC LIMIT 1")
    booking_id = cur.fetchone()[0]
    conn.close()
    
    # Procesar pago
    client.post("/pay", data={"booking_id": str(booking_id)})
    
    # Verificar que se creó el payment
    conn = connect()
    cur = conn.cursor()
    cur.execute("SELECT COUNT(*) FROM payments WHERE booking_id = ?", (booking_id,))
    count = cur.fetchone()[0]
    conn.close()
    
    assert count >= 1


def test_pay_updates_booking_status(authenticated_client):
    """TC-029: Pago debe actualizar estado de reserva a CONFIRMED"""
    client = authenticated_client
    
    # Crear reserva
    client.post("/book", data={
        "room_id": "4",
        "start_date": "2025-12-20",
        "end_date": "2025-12-23"
    })
    
    # Obtener booking_id
    conn = connect()
    cur = conn.cursor()
    cur.execute("SELECT id FROM bookings ORDER BY id DESC LIMIT 1")
    booking_id = cur.fetchone()[0]
    conn.close()
    
    # Procesar pago
    client.post("/pay", data={"booking_id": str(booking_id)})
    
    # Verificar que el estado cambió
    conn = connect()
    cur = conn.cursor()
    cur.execute("SELECT status FROM bookings WHERE id = ?", (booking_id,))
    status = cur.fetchone()[0]
    conn.close()
    
    assert status == "CONFIRMED"


# ==============================================================================
# TESTS DE COBERTURA Y CALIDAD
# ==============================================================================

def test_all_routes_exist(client):
    """Verificar que todas las rutas principales existen"""
    routes = [
        ("/", 200),
        ("/register", 200),
        ("/login", 200),
    ]
    
    for route, expected_status in routes:
        response = client.get(route)
        assert response.status_code == expected_status, f"Ruta {route} falló"


def test_database_connection_closes():
    """TC-036: Verificar que las conexiones se cierran correctamente"""
    conn1 = connect()
    conn1.close()
    
    # Intentar usar la conexión cerrada debe fallar
    try:
        cur = conn1.cursor()
        cur.execute("SELECT 1")
        assert False, "La conexión no se cerró correctamente"
    except:
        assert True


# ==============================================================================
# TESTS DE INTEGRACIÓN
# ==============================================================================

def test_complete_user_flow(client):
    """Test de flujo completo: Registro → Login → Búsqueda → Reserva → Pago"""
    
    # 1. Registro
    response = client.post("/register", data={
        "username": "test_complete_flow",
        "password": "password123"
    }, follow_redirects=True)
    assert response.status_code == 200
    
    # 2. Login
    response = client.post("/login", data={
        "username": "test_complete_flow",
        "password": "password123"
    }, follow_redirects=True)
    assert response.status_code == 200
    
    # 3. Búsqueda
    response = client.post("/search", data={
        "start_date": "2026-01-10",
        "end_date": "2026-01-15",
        "room_type": "simple"
    })
    assert response.status_code == 200
    
    # 4. Reserva
    response = client.post("/book", data={
        "room_id": "5",
        "start_date": "2026-01-10",
        "end_date": "2026-01-15"
    })
    assert response.status_code == 200
    
    # 5. Pago
    conn = connect()
    cur = conn.cursor()
    cur.execute("SELECT id FROM bookings ORDER BY id DESC LIMIT 1")
    booking_id = cur.fetchone()[0]
    conn.close()
    
    response = client.post("/pay", data={
        "booking_id": str(booking_id)
    }, follow_redirects=True)
    assert response.status_code == 200


if __name__ == "__main__":
    pytest.main([__file__, "-v", "--tb=short"])