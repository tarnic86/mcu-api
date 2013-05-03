from datetime import datetime
import logging
import os

import conf

# create logger
logger = logging.getLogger("MCU")
logger.setLevel(conf.LOG_LEVEL)

formatter = logging.Formatter('%(asctime)s | %(levelname)s | %(message)s')
formatter_error = logging.Formatter('****** ERROR ****** %(asctime)s | %(module)s/%(filename)s | %(funcName)s():%(lineno)d | %(message)s')

file_handler = logging.FileHandler(conf.LOG_FILEPATH)
file_error_handler = logging.FileHandler(conf.LOG_ERROR_FILEPATH)

file_handler.setLevel(logging.DEBUG)
file_handler.setFormatter(formatter)
logger.addHandler(file_handler)

file_error_handler.setLevel(logging.ERROR)
file_error_handler.setFormatter(formatter_error)
logger.addHandler(file_error_handler)

if conf.LOG_EMAIL:
    # email in case of errors
    mail_handler = logging.SMTPHandler(conf.LOG_MAIL_HOSTNAME, conf.LOG_MAIL_FROM, conf.LOG_MAIL_TO, "[MCU] Error")
    mail_handler.setLevel(logging.ERROR)
    mail_handler.setFormatter(formatter_error)
    logger.addFilter(ErrorEmailFilter())
    logger.addHandler(mail_handler)

################################################################################
# EMAIL Filter
# To avoid email spam, sent error email 1 per hour (to warn the administrator, who can check and fix the problem)

class ErrorEmailFilter(logging.Filter):
    def filter(self, record):
        # check if the level is error
        if record.level == logging.ERROR:
            last_sent = None
            send_email = False
            filepath = os.path.join('temp', 'last_email_sent.txt')
            now = datetime.now()

            # save locally in a file last time email was sent
            if os.path.exists(filepath):
                # read the configuration
                fp = open(filepath)
                date_read = fp.readline()
                last_sent = datetime.strptime(date_read, '%Y-%m-%d %H:%M:%S')
                fp.close()

            # if time expired, send error email
            return not last_sent or (now - last_sent) > timedelta(minutes=conf.LOG_EMAIL_FREQUENCY):

        return True