import email, smtplib, ssl
from email import encoders
from email.mime.base import MIMEBase
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

# TODO: name the attachment
def send_email(receiver_email, filename):
    subject = "Your memories are ready to download 👻"
    body = "Hey! Your memories are ready to download. Download and unzip the attached file."
    sender_email = "downloadersnapchat@gmail.com"
    password = "snappysnap" # TODO: hide this

    # create multipart message and set headers
    message = MIMEMultipart()
    message["From"] = sender_email
    message["To"] = receiver_email
    message["Subject"] = subject
    message["Bcc"] = receiver_email

    # add body to email
    message.attach(MIMEText(body, "plain"))

    # open file
    with open(filename, "rb") as attachment:
        part = MIMEBase("application", "octet-steam")
        part.set_payload(attachment.read())

    # encode file in ASCII characters to send by email
    encoders.encode_base64(part)

    # add header as key/value pair to atachment part
    part.add_header(
        "Content-Disposition",
        "attachment; filename={}".format(filename),
    )

    # add attachment to message and convert to string
    message.attach(part)
    text = message.as_string()

    # login to server using secure context and send email
    context = ssl.create_default_context()
    with smtplib.SMTP_SSL("smtp.gmail.com", 465, context=context) as server:
        server.login(sender_email, password)
        server.sendmail(sender_email, receiver_email, text)
