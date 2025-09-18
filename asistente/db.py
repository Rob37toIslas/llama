# db.py
import sqlite3

def init_db():
    conn = sqlite3.connect("tienda.db")
    cursor = conn.cursor()

    # Crear tabla productos
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS productos (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        nombre TEXT NOT NULL,
        descripcion TEXT,
        precio REAL NOT NULL,
        stock INTEGER NOT NULL
    )
    """)

    # Insertar datos de ejemplo
    productos = [
        ("Laptop Dell", "Laptop Dell Inspiron 15 con 16GB RAM y 512GB SSD", 13500, 10),
        ("Mouse Logitech", "Mouse inalámbrico Logitech M185", 350, 25),
        ("Teclado Mecánico", "Teclado mecánico retroiluminado RGB", 1200, 15),
        ("Monitor Samsung", "Monitor Samsung 24'' Full HD", 2800, 8),
        ("Audífonos Sony", "Audífonos Sony con cancelación de ruido", 2200, 12),
    ]

    cursor.executemany("""
    INSERT INTO productos (nombre, descripcion, precio, stock) 
    VALUES (?, ?, ?, ?)
    """, productos)

    conn.commit()
    conn.close()
    print("✅ Base de datos inicializada con productos.")

if __name__ == "__main__":
    init_db()
