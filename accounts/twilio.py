from twilio.rest import Client
import random


account_sid = 'AC141881095e39d02974f275d639eb92c4'
auth_token = 'ec48255278afae99c84c6741738174c9'
client = Client(account_sid, auth_token)
generated_otp = ''.join([str(random.randint(0, 9)) for _ in range(6)])


message = client.messages.create(
    body=f'Your OTP for sign up is: {generated_otp}',
   from_='+19292982006',
   to='+919744727684'
)

print(message.sid)