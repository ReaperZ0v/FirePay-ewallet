from twilio.rest import Client

def send_verification(to, otp):
    account_sid = ""
    auth_token = ""
    client = Client(account_sid, auth_token)

    client.messages.create(
        body=f"Your FirePay Wallet Verification code is {otp}, DO NOT share with Anyone!",
        from_="",
        to=to
    )
