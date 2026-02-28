from flask import Flask, request, redirect, render_template
import string, random
import pymysql

app = Flask(__name__)

# ------------------------------
# LOCAL DATABASE CONFIG
# ------------------------------
DB_HOST = "localhost"
DB_USER = "root"          # change if different
DB_PASSWORD = "root"      # change if different
DB_NAME = "url_db"

# ------------------------------
# DB CONNECTION
# ------------------------------
def get_db():
    return pymysql.connect(
        host=DB_HOST,
        user=DB_USER,
        password=DB_PASSWORD,
        database=DB_NAME,
        cursorclass=pymysql.cursors.Cursor
    )

# ------------------------------
# SHORT CODE GENERATOR
# ------------------------------
def generate_code(length=6):
    chars = string.ascii_letters + string.digits
    return ''.join(random.choice(chars) for _ in range(length))

# ------------------------------
# HOME PAGE
# ------------------------------
@app.route("/", methods=["GET", "POST"])
def index():
    short_url = None

    if request.method == "POST":
        long_url = request.form["long_url"]
        code = generate_code()

        db = get_db()
        cur = db.cursor()
        cur.execute(
            "INSERT INTO urls (short_code, long_url) VALUES (%s, %s)",
            (code, long_url)
        )
        db.commit()
        cur.close()
        db.close()

        short_url = request.host_url + code

    return render_template("index.html", short_url=short_url)

# ------------------------------
# REDIRECT SHORT URL
# ------------------------------
@app.route("/<code>")
def redirect_url(code):
    db = get_db()
    cur = db.cursor()

    cur.execute(
        "SELECT long_url FROM urls WHERE short_code=%s",
        (code,)
    )
    result = cur.fetchone()

    if result:
        cur.execute(
            "UPDATE urls SET click_count = click_count + 1 WHERE short_code=%s",
            (code,)
        )
        db.commit()
        cur.close()
        db.close()

        return redirect(result[0])
    else:
        cur.close()
        db.close()
        return "URL not found", 404

# ------------------------------
# RUN SERVER
# ------------------------------
if __name__ == "__main__":
    app.run(debug=True)
