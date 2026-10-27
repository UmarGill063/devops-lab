import os, socket, time
from flask import Flask
import psycopg2

app = Flask(__name__)

def get_conn():
    for _ in range(10):  # wait for DB to be ready
        try:
            return psycopg2.connect(host=os.getenv("DB_HOST", "db"),
                                    dbname="appdb", user="appuser",
                                    password=os.getenv("DB_PASS", "apppass"))
        except psycopg2.OperationalError:
            time.sleep(2)
    raise RuntimeError("DB not reachable")

@app.route("/")
def home():
    conn = get_conn(); cur = conn.cursor()
    cur.execute("CREATE TABLE IF NOT EXISTS visits (id SERIAL PRIMARY KEY)")
    cur.execute("INSERT INTO visits DEFAULT VALUES")
    cur.execute("SELECT COUNT(*) FROM visits")
    count = cur.fetchone()[0]
    conn.commit(); cur.close(); conn.close()
    return f"<h1 id='title'>DevOps Lab App</h1><p>Visits: {count}</p><p>Served by: {socket.gethostname()}</p>"

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)