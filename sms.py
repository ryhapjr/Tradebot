from twilio.rest import Client
import config

account_sid = config.TWILIO_ACCOUNT_SID
auth_token = config.TWILIO_AUTH_TOKEN

client = Client(account_sid, auth_token)


def send_sms(message):
    client.messages.create(
        from_=config.TWILIO_PHONE_NUMBER,
        to=config.CELL_PHONE_NUMBER,
        body=message)
