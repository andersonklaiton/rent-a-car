from flask import current_app, render_template
from flask_mail import Message, Mail
from os import getenv


def flask_mail():
    mail: Mail = current_app.mail

    msg = Message(
        subject="Teste Flask",
        sender=getenv("MAIL_USERNAME"),
        recipients=["rental.cars.api@gmail.com"],
        html=render_template("email/template.html", resumo="rental_cars")
    )

    mail.send(msg)

    return {"message": "e-mail enviado!"}, 200