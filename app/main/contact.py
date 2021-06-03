from flask  import current_app as app
from flask  import (
    request,
    abort,
)
from flask_mail import Mail, Message

from app.utils.decorators   import ratelimit

from app.utils      import user, get_config

from app.main       import main

import hashlib

@main.route("/contact", methods=['POST'])
def contact():
    name    = request.form.get("name")
    email   = request.form.get("email")
    subject = request.form.get("subject")
    message = request.form.get("message")

    # Mail Sending
    try:
        # print(f"[+] app.config : {app.config}")
        mail    = Mail(app)
        msg     = Message(  subject=subject,
                            sender=get_config("mail_username"),
                            reply_to=email,
                            body=f"Email From : {name}\n\n{message}",
                            recipients=[get_config("mail_username")])
        mail.send(msg)
        return 'OK'
    except Exception as e:
        return "Sorry... unable to send your email. :("
    
    abort(500)
    
    
