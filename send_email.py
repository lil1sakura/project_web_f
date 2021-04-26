from flask_mail import Message
import config



def sendMessage(result):
    msg = Message("Contact Form from Tim Pizza", sender=result['email'], recipients=[config.email])

    msg.body = """
    Здраствуйте

    Вы получили писмо от

    Имя: {}
    Фамилия: {}
    Телефон: {}
    Электронная почта: {}

    Письмо: {}
    """.format(result['first_name'], result['last_name'], result['phone'], result['email'], result['message'])
    return msg
