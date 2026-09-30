import os
import sqlite3
from datetime import date, datetime
from functools import wraps

from flask import (Flask, flash, g, redirect, render_template, request,
                   session, url_for)
from werkzeug.security import check_password_hash, generate_password_hash

app = Flask(__name__)
app.secret_key = os.environ.get("SECRET_KEY", "cambia-esta-clave")

DATABASE = os.path.join(os.path.dirname(__file__), "hotel.db")


# ---------------------------------------------------------------
# Base de datos
# ---------------------------------------------------------------
def get_db():
    if "db" not in g:
        g.db = sqlite3.connect(DATABASE)
        g.db.row_factory = sqlite3.Row
    return g.db


@app.teardown_appcontext
def cerrar_db(error):
    db = g.pop("db", None)
    if db is not None:
        db.close()


def init_db():
    db = sqlite3.connect(DATABASE)
    db.executescript("""
        CREATE TABLE IF NOT EXISTS usuarios (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nombre TEXT NOT NULL,
            email TEXT NOT NULL UNIQUE,
            password TEXT NOT NULL,
            rol TEXT NOT NULL DEFAULT 'cliente'   -- 'cliente' o 'dueno'
        );

        CREATE TABLE IF NOT EXISTS habitaciones (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            numero TEXT NOT NULL UNIQUE,
            tipo TEXT NOT NULL,
            capacidad INTEGER NOT NULL,
            precio INTEGER NOT NULL
        );

        CREATE TABLE IF NOT EXISTS reservas (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            usuario_id INTEGER NOT NULL REFERENCES usuarios(id),
            habitacion_id INTEGER NOT NULL REFERENCES habitaciones(id),
            entrada TEXT NOT NULL,
            salida TEXT NOT NULL,
            estado TEXT NOT NULL DEFAULT 'activa'  -- 'activa' o 'cancelada'
        );
    """)

    # Habitaciones de ejemplo (la primera vez que se corre la app)
    if db.execute("SELECT COUNT(*) FROM habitaciones").fetchone()[0] == 0:
        db.executemany(
            "INSERT INTO habitaciones (numero, tipo, capacidad, precio) VALUES (?, ?, ?, ?)",
            [
                ("101", "Sencilla", 1, 120000),
                ("102", "Sencilla", 2, 150000),
                ("201", "Doble", 2, 220000),
                ("202", "Doble", 3, 250000),
                ("203", "Doble", 4, 280000),
                ("301", "Suite", 4, 450000),
                ("302", "Suite", 5, 520000),
            ],
        )

    # Usuario dueño por defecto
    if db.execute("SELECT COUNT(*) FROM usuarios WHERE rol = 'dueno'").fetchone()[0] == 0:
        db.execute(
            "INSERT INTO usuarios (nombre, email, password, rol) VALUES (?, ?, ?, 'dueno')",
            ("Dueño Hotel Bacatá", "dueno@bacata.com", generate_password_hash("dueno123")),
        )

    db.commit()
    db.close()


# ---------------------------------------------------------------
# Funciones de ayuda
# ---------------------------------------------------------------
@app.template_filter("cop")
def formato_cop(valor):
    return "$" + f"{valor:,.0f}".replace(",", ".")


def leer_fecha(texto):
    try:
        return datetime.strptime(texto, "%Y-%m-%d").date()
    except (ValueError, TypeError):
        return None


def habitacion_esta_libre(db, habitacion_id, entrada, salida):
    """Una habitación está libre si no tiene reservas activas que se crucen con las fechas."""
    choque = db.execute(
        """SELECT 1 FROM reservas
           WHERE habitacion_id = ? AND estado = 'activa'
             AND entrada < ? AND salida > ?""",
        (habitacion_id, salida, entrada),
    ).fetchone()
    return choque is None


def login_requerido(rol):
    def decorador(funcion):
        @wraps(funcion)
        def envoltura(*args, **kwargs):
            if "usuario_id" not in session:
                flash("Inicia sesión para continuar.")
                return redirect(url_for("login"))
            if session.get("rol") != rol:
                flash("No tienes permiso para entrar a esa página.")
                return redirect(url_for("inicio"))
            return funcion(*args, **kwargs)
        return envoltura
    return decorador


# ---------------------------------------------------------------
# Inicio, registro y sesión
# ---------------------------------------------------------------
@app.route("/")
def inicio():
    if session.get("rol") == "dueno":
        return redirect(url_for("panel_dueno"))
    if session.get("rol") == "cliente":
        return redirect(url_for("panel_cliente"))
    return redirect(url_for("login"))


@app.route("/registro", methods=["GET", "POST"])
def registro():
    if request.method == "POST":
        nombre = request.form["nombre"].strip()
        email = request.form["email"].strip().lower()
        password = request.form["password"]

        if not nombre or not email or len(password) < 6:
            flash("Completa todos los campos. La contraseña debe tener mínimo 6 caracteres.")
            return render_template("registro.html")

        db = get_db()
        if db.execute("SELECT 1 FROM usuarios WHERE email = ?", (email,)).fetchone():
            flash("Ya existe una cuenta con ese correo.")
            return render_template("registro.html")

        db.execute(
            "INSERT INTO usuarios (nombre, email, password, rol) VALUES (?, ?, ?, 'cliente')",
            (nombre, email, generate_password_hash(password)),
        )
        db.commit()
        flash("Cuenta creada. Ya puedes iniciar sesión.")
        return redirect(url_for("login"))

    return render_template("registro.html")


@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        email = request.form["email"].strip().lower()
        password = request.form["password"]

        usuario = get_db().execute(
            "SELECT * FROM usuarios WHERE email = ?", (email,)
        ).fetchone()

        if usuario is None or not check_password_hash(usuario["password"], password):
            flash("Correo o contraseña incorrectos.")
            return render_template("login.html")

        session.clear()
        session["usuario_id"] = usuario["id"]
        session["nombre"] = usuario["nombre"]
        session["rol"] = usuario["rol"]
        return redirect(url_for("inicio"))

    return render_template("login.html")


@app.route("/logout")
def logout():
    session.clear()
    return redirect(url_for("login"))


# ---------------------------------------------------------------
# Cliente: buscar habitaciones libres, reservar y ver sus reservas
# ---------------------------------------------------------------
@app.route("/cliente")
@login_requerido("cliente")
def panel_cliente():
    db = get_db()
    entrada_txt = request.args.get("entrada", "")
    salida_txt = request.args.get("salida", "")
    libres = None
    noches = 0

    if entrada_txt or salida_txt:
        entrada, salida = leer_fecha(entrada_txt), leer_fecha(salida_txt)
        if entrada is None or salida is None:
            flash("Escribe las dos fechas.")
        elif entrada < date.today():
            flash("La fecha de entrada no puede ser anterior a hoy.")
        elif salida <= entrada:
            flash("La salida debe ser después de la entrada.")
        else:
            noches = (salida - entrada).days
            habitaciones = db.execute("SELECT * FROM habitaciones ORDER BY numero").fetchall()
            libres = [h for h in habitaciones
                      if habitacion_esta_libre(db, h["id"], entrada_txt, salida_txt)]

    mis_reservas = db.execute(
        """SELECT r.*, h.numero, h.tipo, h.precio
           FROM reservas r JOIN habitaciones h ON h.id = r.habitacion_id
           WHERE r.usuario_id = ?
           ORDER BY r.entrada DESC""",
        (session["usuario_id"],),
    ).fetchall()

    return render_template("cliente.html", libres=libres, noches=noches,
                           entrada=entrada_txt, salida=salida_txt,
                           hoy=date.today().isoformat(), reservas=mis_reservas)


@app.route("/reservar", methods=["POST"])
@login_requerido("cliente")
def reservar():
    db = get_db()
    habitacion_id = request.form.get("habitacion_id")
    entrada_txt = request.form.get("entrada")
    salida_txt = request.form.get("salida")
    entrada, salida = leer_fecha(entrada_txt), leer_fecha(salida_txt)

    if not habitacion_id or entrada is None or salida is None or entrada < date.today() or salida <= entrada:
        flash("Las fechas no son válidas.")
        return redirect(url_for("panel_cliente"))

    if not habitacion_esta_libre(db, habitacion_id, entrada_txt, salida_txt):
        flash("Lo sentimos, esa habitación ya fue reservada en esas fechas.")
        return redirect(url_for("panel_cliente", entrada=entrada_txt, salida=salida_txt))

    db.execute(
        "INSERT INTO reservas (usuario_id, habitacion_id, entrada, salida) VALUES (?, ?, ?, ?)",
        (session["usuario_id"], habitacion_id, entrada_txt, salida_txt),
    )
    db.commit()
    flash("¡Reserva realizada con éxito!")
    return redirect(url_for("panel_cliente"))


@app.route("/cancelar/<int:reserva_id>", methods=["POST"])
@login_requerido("cliente")
def cancelar(reserva_id):
    db = get_db()
    db.execute(
        "UPDATE reservas SET estado = 'cancelada' WHERE id = ? AND usuario_id = ?",
        (reserva_id, session["usuario_id"]),
    )
    db.commit()
    flash("Reserva cancelada.")
    return redirect(url_for("panel_cliente"))


# ---------------------------------------------------------------
# Dueño: habitaciones, disponibilidad y fechas reservadas
# ---------------------------------------------------------------
@app.route("/dueno")
@login_requerido("dueno")
def panel_dueno():
    db = get_db()
    hoy = date.today()
    entrada_txt = request.args.get("entrada", hoy.isoformat())
    salida_txt = request.args.get("salida", "")
    entrada = leer_fecha(entrada_txt)
    salida = leer_fecha(salida_txt)

    # Si no se eligió una salida válida, se consulta solo la noche de la fecha de entrada
    if entrada is None:
        flash("Fecha no válida, se muestra la disponibilidad de hoy.")
        entrada = hoy
    if salida is None or salida <= entrada:
        salida = date.fromordinal(entrada.toordinal() + 1)

    habitaciones = db.execute("SELECT * FROM habitaciones ORDER BY numero").fetchall()
    estado = []
    for h in habitaciones:
        libre = habitacion_esta_libre(db, h["id"], entrada.isoformat(), salida.isoformat())
        estado.append({"hab": h, "libre": libre})

    reservas = db.execute(
        """SELECT r.*, h.numero, h.tipo, u.nombre AS cliente, u.email
           FROM reservas r
           JOIN habitaciones h ON h.id = r.habitacion_id
           JOIN usuarios u ON u.id = r.usuario_id
           ORDER BY r.entrada, h.numero"""
    ).fetchall()

    return render_template("dueno.html", estado=estado, reservas=reservas,
                           entrada=entrada.isoformat(), salida=salida.isoformat())


init_db()

if __name__ == "__main__":
    app.run(debug=True)
