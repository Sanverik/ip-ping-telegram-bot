import time

def lambda_handler(event, context):
    print("Hello from lambda!")
    print(time.time())
    return 