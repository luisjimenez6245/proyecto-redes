import logging
import smtplib
import ssl


def send_email(content, ):
    logger = logging.getLogger("fastapi")
    logger.info(f"Sending email to  {content}....")

    smtp_server = "smtp.gmail.com"
    port = 587
    sender_email = "luiguituner@gmail.com"
    password =  "password"
    context = ssl.create_default_context()
    server = None
    try:
        server = smtplib.SMTP(smtp_server, port)
        server.ehlo()
        server.starttls(context=context)
        server.ehlo()
        server.login(sender_email, password)
        server.sendmail(sender_email, "luis@finalsa.com", content)
    except Exception as e:
        logger.exception(e)
    finally:
        if(server is not None):
            server.quit()
    logger.info(f"Sending email to  {content}....")
