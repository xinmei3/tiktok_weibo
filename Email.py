import smtplib
from email.mime.text import MIMEText


mail_host = "smtp.qq.com"
mail_user = "12345678"           # This is the QQ email account without the @qq.com part
mail_pass = "ginbizweplqoijbh"     # This is the QQ email authorization code, not the password
sender = "12345678@qq.com"       # This is the full QQ email address
receiver = "987654321@163.com"   # This is the receiver's email address


def send_email(subject, content):
    msg = MIMEText(content, "plain", "utf-8")
    msg["Subject"] = subject
    msg["From"] = sender
    msg["To"] = receiver

    try:
        with smtplib.SMTP_SSL(mail_host, 465) as server:
            server.login(mail_user, mail_pass)
            server.sendmail(sender, [receiver], msg.as_string())
        print("Email sent successfully.")
    except Exception as e:
        print(f"Failed to send email: {e}")

if __name__ == "__main__":
    subject = "Test Email"
    content = "This is a test email sent from Python."
    send_email(subject, content)