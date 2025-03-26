import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from lib.static import APP_URL, SMTP_EMAIL_SEND_FROM, SMTP_PASSWORD_FROM, SMTP_SERVER, SMTP_PORT


def send_confirmation_email(to_email: str, token: str) -> bool:
    confirmation_link = f"{APP_URL}/registration?token={token}&email={to_email}"

    from_email = SMTP_EMAIL_SEND_FROM
    from_password = SMTP_PASSWORD_FROM  # generate password in 'App password' setting.

    subject = "Confirm Your Registration"
    body = f"Click the link to confirm your registration: {confirmation_link}"
    mess = f"Subject: {subject}\n\n{body}"

    # Create the email
    msg = MIMEMultipart()
    msg['From'] = from_email
    msg['To'] = to_email
    msg['Subject'] = subject
    msg.attach(MIMEText(mess, 'plain'))

    # Connect to the SMTP server
    with smtplib.SMTP(SMTP_SERVER, SMTP_PORT) as server:
        server.starttls()  # Upgrade to a secure connection
        server.login(from_email, from_password)
        server.send_message(msg)
        # print('----> письмо отправлено!!!')
        return True

