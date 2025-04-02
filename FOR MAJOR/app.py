from flask import Flask, render_template, request, redirect, session
from auth import get_google_auth
from meeting_bot import join_meeting_and_record
from summarize import generate_summary
from database import save_summary, get_user_history
from flask_login import LoginManager, login_user, logout_user, current_user


app = Flask(__name__)
app.secret_key = "your_secret_key"
login_manager = LoginManager()
# login_manager.init_app(app)

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/login")
def login():
    return redirect(get_google_auth())

@app.route("/join_meeting", methods=["POST"])
# @login_required
def join_meeting():
    platform = request.form.get("platform")
    meeting_link = request.form.get("meeting_link")
    transcript = join_meeting_and_record(platform, meeting_link)
    summary = generate_summary(transcript)
    save_summary(current_user.id, summary)
    return render_template("index.html", summary=summary)

@app.route("/history")
# @login_required
def history():
    summaries = get_user_history(current_user.id)
    return render_template("history.html", summaries=summaries)

@app.route("/send_email")
# @login_required
def send_email():
    from summarize import send_email_summary
    send_email_summary(current_user.email)
    return "Email Sent!"

if __name__ == "__main__":
    app.run(debug=True)