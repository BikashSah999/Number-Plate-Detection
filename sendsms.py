from twilio.rest import Client


# Your Account Sid and Auth Token from twilio.com/console
# DANGER! This is insecure. See http://twil.io/secure
account_sid = ''
auth_token = ''
client = Client(account_sid, auth_token)

message = client.messages \
                .create(
                     body="Oee mug randi valu. Madar**** college ma aba dekhi thulo kura garis bhane thau ko thau janxas. Bichar garera bolne gar.",
                     from_='+13073174108',
                     to='+9779861397078'
                 )

print(message.sid)
