from twilio.rest import Client


def call_emergency():
    account_sid = 'sid'
    auth_token = 'token'

    client = Client(account_sid, auth_token)

    call = client.calls.create(
        twiml='<Response><Say>Hi, My name is Diluni and I am at 123 Maple Street. I am concerned about the possibility of a stroke. Please send an ambulance.</Say></Response>',
        to='+436574364534',
        from_='+14706345365'
    )
    print(call.sid)
