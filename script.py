import africastalking

username = "sandbox"
apikey = "f13456e1313519fdbdbf7ebc9933f988ccbf036136d2e1f681fa26fc6eb46255"

africastalking.initialize(username, apikey)

# Get the sms service
sms = africastalking.SMS

# Define some options required when sending the sms
recipients = ['+254719702373']
message = 'Bruh issa test'

# Send the sms
try:
    response = sms.send(message, recipients)
    print(response)
except Exception as e:
    print(f'Houston we have a problem {e}')
