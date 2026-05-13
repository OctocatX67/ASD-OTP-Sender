from flask import Flask, render_template, request, session, redirect, url_for
import smtplib
import random
from email.message import EmailMessage

app = Flask(__name__)
app.secret_key = "any_random_string"

def send_otp_email(receiver_email, otp_code):
    msg = EmailMessage()
    msg.set_content(f"Your code is: {otp_code}")
    msg['Subject'] = 'Login Code'
    msg['From'] = "test@localhost"
    msg['To'] = receiver_email
    # Connects to the local server we will start in Step 4
    with smtplib.SMTP('127.0.0.1', 1025) as smtp:
        smtp.send_message(msg)

@app.route('/')
def index():
    return '<form action="/login" method="POST">Email: <input name="email"><button>Send OTP</button></form>'

@app.route('/login', methods=['POST'])
def login():
    email = request.form.get('email')
    otp = str(random.randint(1000, 9999)) # 4-digit for easy testing
    session['otp'] = otp
    send_otp_email(email, otp)
    return redirect(url_for('verify'))

@app.route('/verify', methods=['GET', 'POST'])
def verify():
    if request.method == 'POST':
        if request.form.get('u_otp') == session.get('otp'):
            return "<h1>🔓 Success!</h1>"
        return "<h1>❌ Wrong code!</h1>"
    return '<form action="/verify" method="POST">Enter Code: <input name="u_otp"><button>Verify</button></form>'

app.run(host='0.0.0.0', port=1707)

