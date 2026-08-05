from flask import Flask, render_template, request
import pickle
import sqlite3
from datetime import datetime

app = Flask(__name__)

# Load Model
model = pickle.load(open("model.pkl", "rb"))
vectorizer = pickle.load(open("vectorizer.pkl", "rb"))

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/predict", methods=["POST"])
def predict():

    email_text = request.form["email"]

    vector = vectorizer.transform([email_text])

    prediction = model.predict(vector)[0]

    probability = model.predict_proba(vector)
    confidence = max(probability[0]) * 100
    scan_time = datetime.now().strftime("%d-%m-%y %I: %m %p")

    if prediction == 1:
        result = "⚠️ Phishing Email Detected"
    else:
        result = "✅ Safe Email"
    conn = sqlite3.connect("emails.db")
    cursor = conn.cursor()

    
    cursor.execute(
    """
    INSERT INTO scan_history(email, prediction, confidence, scan_time)
    VALUES (?, ?, ?, ?)
    """,
    (email_text, result, round(confidence, 2), scan_time))

    conn.commit()
    conn.close()
    return render_template("index.html", 
    prediction = result, 
    confidence = round(confidence,2))

@app.route("/history")
def history():

    conn = sqlite3.connect("emails.db")
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM scan_history ORDER BY id DESC")

    history_data = cursor.fetchall()

    conn.close()

    return render_template("history.html", history=history_data)

@app.route("/dashboard")
def dashboard():

    conn = sqlite3.connect("emails.db")
    cursor = conn.cursor()

    # Total emails
    cursor.execute("SELECT COUNT(*) FROM scan_history")
    total = cursor.fetchone()[0]

    cursor.execute("SELECT AVG(confidence) FROM scan_history")
    avg_confidence = cursor.fetchone()[0]

    if avg_confidence is None:
        avg_confidence = 0

    # Total phishing emails
    cursor.execute("SELECT COUNT(*) FROM scan_history WHERE prediction LIKE '%Phishing%'")
    phishing = cursor.fetchone()[0]

    # Total safe emails
    cursor.execute("SELECT COUNT(*) FROM scan_history WHERE prediction LIKE '%Safe%'")
    safe = cursor.fetchone()[0]

    conn.close()

    return render_template(
    "dashboard.html",
    total=total,
    phishing=phishing,
    safe=safe,
    avg_confidence=round(avg_confidence,2)
)

if __name__ == "__main__":
    app.run(debug=True)


