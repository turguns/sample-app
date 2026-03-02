import os
import time

import pymysql
from flask import Flask, redirect, render_template, request

app = Flask(__name__)

DB_HOST = os.getenv("DB_HOST", "mariadb")
DB_PORT = int(os.getenv("DB_PORT", "3306"))
DB_NAME = os.getenv("DB_NAME", "appdb")
DB_USER = os.getenv("DB_USER", "appuser")
DB_PASSWORD = os.getenv("DB_PASSWORD", "apppass")


def get_connection(retries=20, delay=3):
    last_error = None
    for _ in range(retries):
        try:
            return pymysql.connect(
                host=DB_HOST,
                port=DB_PORT,
                user=DB_USER,
                password=DB_PASSWORD,
                database=DB_NAME,
                charset="utf8mb4",
                cursorclass=pymysql.cursors.DictCursor,
                connect_timeout=5,
            )
        except Exception as exc:
            last_error = exc
            time.sleep(delay)
    raise last_error


def init_db():
    with get_connection() as conn:
        with conn.cursor() as cur:
            cur.execute(
                """
                CREATE TABLE IF NOT EXISTS notes (
                    id INT AUTO_INCREMENT PRIMARY KEY,
                    content VARCHAR(255) NOT NULL,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
                """
            )
        conn.commit()


@app.route("/", methods=["GET", "POST"])
def index():
    error = None
    try:
        init_db()
        if request.method == "POST":
            content = (request.form.get("content") or "").strip()
            if content:
                with get_connection() as conn:
                    with conn.cursor() as cur:
                        cur.execute("INSERT INTO notes (content) VALUES (%s)", (content,))
                    conn.commit()
            return redirect("/")

        with get_connection() as conn:
            with conn.cursor() as cur:
                cur.execute("SELECT id, content, created_at FROM notes ORDER BY id DESC")
                rows = cur.fetchall()
        return render_template("index.html", rows=rows, error=None)
    except Exception as exc:
        error = str(exc)
        return render_template("index.html", rows=[], error=error)


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080)

