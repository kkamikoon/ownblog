from flask import current_app as app

from app.utils import set_config, get_config

def is_setup():
    return bool(get_config("setup")) is True


def set_email():
    set_config("mail_server",   "smtp.gmail.com")
    set_config("mail_port",     465)
    set_config("mail_username", "kkamikoon@gmail.com")
    set_config("mail_password", "owubcnctfpfbngqh")
    set_config("mail_use_tls",  False)
    set_config("mail_use_ssl",  True)

    get_email()


def get_email():
    mail_settings ={
        "MAIL_SERVER"   : get_config("mail_server"),
        "MAIL_PORT"     : get_config("mail_port"),
        "MAIL_USERNAME" : get_config("mail_username"),
        "MAIL_PASSWORD" : get_config("mail_password"),
        "MAIL_USE_TLS"  : get_config("mail_use_tls"),
        "MAIL_USE_SSL"  : get_config("mail_use_ssl")
    }

    app.config.update(mail_settings)