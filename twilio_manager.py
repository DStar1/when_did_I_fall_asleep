from twilio.rest import Client

# get auth_token here https://www.twilio.com/console
class TwilioApi:
    def __init__(self):
        self.account_sid = "AC19c8546ea2823242274796cb4c562ef2"
        self.auth_token = self.get_auth_token()

    def get_auth_token(self):
        token_file = "token.txt"
        with open(token_file) as f:
            token = f.read().replace('\n', '')
        print(token)
        return token

    def authenticate_twilio(self):
        return Client(self.account_sid, self.auth_token)

    def send_text(self, body):
        client = self.authenticate_twilio()

        message = client.messages.create(
                                    from_='+19713514315', 
                                    to='+15037244805',
                                    body=body
        )
        print(message.sid)
    
    def get_message_responses(self):
        client = self.authenticate_twilio()

        for sms in client.messages.list():
            if sms.to == '+19713514315':
                print(sms.body)


