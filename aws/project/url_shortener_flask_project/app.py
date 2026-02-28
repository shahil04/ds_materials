
from flask import Flask, request, redirect, render_template
import string, random
import MySQLdb

app = Flask(__name__)

# Database config (UPDATE THESE)
DB_HOST = "database-1.cud2siaa2jqh.us-east-1.rds.amazonaws.com"
DB_USER = "admin"
DB_PASSWORD = "1234root"
DB_NAME = "url_db"

def get_db():
    return MySQLdb.connect(
        host=DB_HOST,
        user=DB_USER,
        passwd=DB_PASSWORD,
        db=DB_NAME
    )

def generate_code(length=6):
    chars = string.ascii_letters + string.digits
    return ''.join(random.choice(chars) for _ in range(length))

@app.route("/", methods=["GET", "POST"])
def index():
    short_url = None
    if request.method == "POST":
        long_url = request.form['long_url']
        code = generate_code()

        db = get_db()
        cur = db.cursor()
        cur.execute(
            "INSERT INTO urls (short_code, long_url) VALUES (%s, %s)",
            (code, long_url)
        )
        db.commit()
        cur.close()

        short_url = request.host_url + code

    return render_template("index.html", short_url=short_url)

@app.route("/<code>")
def redirect_url(code):
    db = get_db()
    cur = db.cursor()
    cur.execute(
        "SELECT long_url FROM urls WHERE short_code=%s", (code,)
    )
    result = cur.fetchone()

    if result:
        cur.execute(
            "UPDATE urls SET click_count = click_count + 1 WHERE short_code=%s",
            (code,)
        )
        db.commit()
        return redirect(result[0])
    else:
        return "URL not found", 404

if __name__ == "__main__":
    app.run()
