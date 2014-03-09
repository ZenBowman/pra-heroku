from email.MIMEMultipart import MIMEMultipart
from email.MIMEText import MIMEText
from email.MIMEImage import MIMEImage
import smtplib

def send_qr_msg(email, img):
    msg = MIMEMultipart()
    msg['Subject'] = "Pasadena Roving Archers class registration QR code"
    msg.attach(MIMEText("Your QR code"))
    msg.attach(MIMEImage(img))

    # to send
    mailer = smtplib.SMTP()
    mailer.connect()
    mailer.sendmail("classregistration@rovingarchers.com", email, msg.as_string())
    mailer.close()