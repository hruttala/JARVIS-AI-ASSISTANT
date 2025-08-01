import datetime

def jarvis():
    now = datetime.datetime.now()
    current_time = now.strftime("%H:%M:%S")
    return f"The time now is {current_time}"

print(jarvis())