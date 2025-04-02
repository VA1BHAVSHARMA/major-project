import requests
import smtplib

def generate_summary(text):
    response = requests.post("https://api.summarization.com/summarize", json={"text": text})
    return response.json().get("summary", "No summary available.")

def send_email_summary(user_email):
    server = smtplib.SMTP("smtp.gmail.com", 587)
    server.starttls()
    server.login("your_email@gmail.com", "your_app_password")
    message = "Subject: Meeting Summary\n\nHere is your meeting summary."
    server.sendmail("your_email@gmail.com", user_email, message)
    server.quit()