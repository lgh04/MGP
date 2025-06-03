import smtplib
from email.mime.text import MIMEText

def send_email(to_email: str, code: str):
    sender = "mgp040505@gmail.com"
    app_password = "tijj xwis cipp gszx"

    msg = MIMEText(f"[ACT:ON] 인증번호는 {code} 입니다.")
    msg["Subject"] = "ACT:ON 이메일 인증번호"
    msg["From"] = sender
    msg["To"] = to_email

    server = smtplib.SMTP_SSL("smtp.gmail.com", 465)
    server.login(sender, app_password)
    server.sendmail(sender, to_email, msg.as_string())
    server.quit()