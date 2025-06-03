import smtplib
from email.mime.text import MIMEText
from fastapi import HTTPException

def send_email(to_email: str, code: str):
    try:
        sender = "mgp040505@gmail.com"
        app_password = "tijj xwis cipp gszx"

        msg = MIMEText(f"[ACT:ON] 인증번호는 {code} 입니다.")
        msg["Subject"] = "ACT:ON 이메일 인증번호"
        msg["From"] = sender
        msg["To"] = to_email

        server = smtplib.SMTP_SSL("smtp.gmail.com", 465)
        try:
            server.login(sender, app_password)
            server.sendmail(sender, to_email, msg.as_string())
        except smtplib.SMTPAuthenticationError:
            raise HTTPException(
                status_code=500,
                detail="이메일 서버 인증 실패. 관리자에게 문의하세요."
            )
        except smtplib.SMTPException as e:
            raise HTTPException(
                status_code=500,
                detail=f"이메일 전송 중 오류 발생: {str(e)}"
            )
        finally:
            server.quit()
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"이메일 전송 실패: {str(e)}"
        )