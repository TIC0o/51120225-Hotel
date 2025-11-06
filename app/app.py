from flask import Flask, render_template, request, redirect, url_for, session, flash
import sqlite3
from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash
from pathlib import Path

# Usar la misma lógica de ruta que db.py
BASE_DIR = Path(__file__).resolve().parent.parent
DB_PATH = BASE_DIR / "hotel_reservas.db"

app = Flask(__name__)
app.secret_key = "dev-secret-key-change-me"

def get_db():
    conn = sqlite3.connect(str(DB_PATH), check_same_thread=False)
    conn.row_factory = sqlite3.Row
    return conn

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        username = request.form.get("username", "").strip()
        password = request.form.get("password", "").strip()
        
        if not username or not password:
            flash("Usuario y contraseña requeridos", "error")
            return redirect(url_for("register"))
        
        conn = get_db()
        cur = conn.cursor()
        
        try:
            cur.execute("SELECT id FROM users WHERE username = ?", (username,))
            if cur.fetchone():
                flash("El usuario ya existe", "error")
                return redirect(url_for("register"))
            
            pwd_hash = generate_password_hash(password)
            cur.execute("INSERT INTO users (username, password_hash) VALUES (?,?)", (username, pwd_hash))
            conn.commit()
            flash("Registro exitoso. Inicia sesión.", "success")
            return redirect(url_for("login"))
        except Exception as e:
            flash(f"Error en el registro: {str(e)}", "error")
            return redirect(url_for("register"))
        finally:
            conn.close()
    
    return render_template("register.html")

@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form.get("username", "").strip()
        password = request.form.get("password", "").strip()
        
        conn = get_db()
        cur = conn.cursor()
        
        try:
            cur.execute("SELECT id, password_hash FROM users WHERE username = ?", (username,))
            row = cur.fetchone()
            
            if row and check_password_hash(row["password_hash"], password):
                session["user_id"] = row["id"]
                session["username"] = username
                flash(f"Bienvenido, {username}!", "success")
                return redirect(url_for("index"))
            
            flash("Credenciales inválidas", "error")
            return redirect(url_for("login"))
        except Exception as e:
            flash(f"Error en el login: {str(e)}", "error")
            return redirect(url_for("login"))
        finally:
            conn.close()
    
    return render_template("login.html")

@app.route("/logout")
def logout():
    session.clear()
    flash("Sesión cerrada correctamente", "success")
    return redirect(url_for("index"))

@app.route("/search", methods=["GET", "POST"])
def search():
    if request.method == "POST":
        start_date = request.form.get("start_date")
        end_date = request.form.get("end_date")
        room_type = request.form.get("room_type")
        
        conn = get_db()
        cur = conn.cursor()

        try:
            query = """
            SELECT rooms.id as room_id, rooms.room_number, rt.name as room_type_name, rt.price
            FROM rooms rooms
            JOIN room_types rt ON rooms.room_type_id = rt.id
            WHERE rt.code = ?
            AND rooms.id NOT IN (
                SELECT room_id FROM bookings
                WHERE NOT (date(end_date) <= date(?) OR date(start_date) >= date(?))
            )
            ORDER BY rooms.room_number
            """
            cur.execute(query, (room_type, start_date, end_date))
            available_rooms = cur.fetchall()

            query_occupied = """
            SELECT rooms.room_number
            FROM rooms rooms
            JOIN bookings b ON rooms.id = b.room_id
            WHERE date(b.start_date) <= date(?) AND date(b.end_date) >= date(?)
            """
            cur.execute(query_occupied, (end_date, start_date))
            occupied_rooms = [row['room_number'] for row in cur.fetchall()]

            return render_template("search_results.html", available_rooms=available_rooms, 
                                   occupied_rooms=occupied_rooms, start_date=start_date, 
                                   end_date=end_date, room_type=room_type)
        finally:
            conn.close()

    return redirect(url_for("index"))

@app.route("/book", methods=["POST"])
def book():
    if "user_id" not in session:
        flash("Inicia sesión para reservar", "error")
        return redirect(url_for("login"))
    
    room_id = request.form.get("room_id")
    start_date = request.form.get("start_date")
    end_date = request.form.get("end_date")

    conn = get_db()
    cur = conn.cursor()
    
    try:
        cur.execute("""
            SELECT rt.price
            FROM rooms r JOIN room_types rt ON r.room_type_id = rt.id
            WHERE r.id = ?
        """, (room_id,))
        row = cur.fetchone()
        
        if not row:
            flash("Habitación no encontrada", "error")
            return redirect(url_for("index"))

        price = row["price"]
        sd = datetime.strptime(start_date, "%Y-%m-%d")
        ed = datetime.strptime(end_date, "%Y-%m-%d")
        nights = (ed - sd).days
        
        if nights <= 0:
            flash("Rango de fechas inválido", "error")
            return redirect(url_for("index"))
        
        total = price * nights

        cur.execute("""
            SELECT COUNT(1) as c FROM bookings
            WHERE room_id = ? AND NOT (date(end_date) <= date(?) OR date(start_date) >= date(?))
        """, (room_id, start_date, end_date))
        
        if cur.fetchone()["c"] > 0:
            flash("La habitación ya no está disponible en ese rango", "error")
            return redirect(url_for("index"))

        cur.execute("""
            INSERT INTO bookings (user_id, room_id, start_date, end_date, total_price, status)
            VALUES (?,?,?,?,?,?)
        """, (session["user_id"], room_id, start_date, end_date, total, "PENDING_PAYMENT"))
        conn.commit()

        booking_id = cur.lastrowid
        return render_template("booking.html", booking_id=booking_id, total=total)
    finally:
        conn.close()

@app.route("/pay", methods=["POST"])
def pay():
    booking_id = request.form.get("booking_id")
    conn = get_db()
    cur = conn.cursor()
    
    try:
        cur.execute("INSERT INTO payments (booking_id, amount, status, created_at) VALUES (?,?,?,datetime('now'))",
                    (booking_id, 0, "APPROVED"))
        cur.execute("UPDATE bookings SET status = 'CONFIRMED' WHERE id = ?", (booking_id,))
        conn.commit()
        flash("Pago simulado aprobado. Reserva confirmada.", "success")
        return redirect(url_for("index"))
    finally:
        conn.close()

if __name__ == "__main__":
    app.run(debug=True)