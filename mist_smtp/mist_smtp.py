import smtplib
import ssl
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.image import MIMEImage
from datetime import datetime, timezone
from .mist_qrcode import get_qrcode_as_html

class Mist_SMTP():
    def __init__(self, smtp_config):
        self.smtp_config=smtp_config
        self.smtp = smtplib.SMTP

    def _send_email(self, recipients, msg, log_message):
        print(log_message, end="", flush=True)
        #try:
        with self.smtp(self.smtp_config["host"], self.smtp_config["port"]) as smtp:
            if self.smtp_config["use_ssl"]:
                context = ssl.SSLContext(ssl.PROTOCOL_TLS)
                smtp.ehlo()
                smtp.starttls(context=context)
                smtp.ehlo()
            if self.smtp_config["username"] and self.smtp_config["password"]:
                smtp.login(self.smtp_config["username"], self.smtp_config["password"])
            smtp.sendmail(self.smtp_config["from_email"], recipients, msg)
        print("\033[92m\u2714\033[0m")
        return True
        # except:
        #     print('\033[31m\u2716\033[0m')
        #     return False

    def send_psk(self, psk: str, ssid: str, recipients):
        # if len(recipients) == 1:
        #     recipients = recipients[0]
        # else:
        #     recipients = ",".join(recipients)

        msg = MIMEMultipart('alternative')
        msg["Subject"] = "New Wi-Fi access code"
        msg["From"] = "{0} <{1}>".format(self.smtp_config["from_name"], self.smtp_config["from_email"])
        
        qr_info = "You can also scan the QRCode below to configure your device:"
        qr_html = get_qrcode_as_html(ssid, psk) 

        with open("./mist_smtp/template.html", "r") as template:
            html = template.read()
        html = html.format(self.smtp_config["logo_url"], ssid, psk, qr_info, qr_html)
        msg_body = MIMEText(html, "html")
        msg.attach(msg_body)

        for recipient in recipients:
            msg["To"] = recipient
            self._send_email(recipient, msg.as_string(), "Sending email to {0} ".format(recipient).ljust(79, "."))
        return 

