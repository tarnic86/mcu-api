import smtplib
from email.mime.text import MIMEText

import conf

class ErrorMail():
    """Prepare and send emails"""

    _server = "cernmx.cern.ch"
    _port = 25
    _from = "service-avc-operation"
    _to = ["service-avc-operation"]
    _body = None

    def __init__(self, body):
        self._body = MIMEText(body)

    def send(self):
        s = smtplib.SMTP(self._server, self._port)

        self._body['Subject'] = "[MCU] Error connecting endpoints"
        self._body['From'] = self._from
        self._body['To'] = ", ".join(self._to)

        if conf.EMAIL_ENABLED:
            s.sendmail(self._from, self._to, self._body.as_string())

        print self._body

        s.quit()
