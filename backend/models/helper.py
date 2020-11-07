from uuid import uuid4


def uuid_maker():
    return str(uuid4())


def seconds_to_mmss(seconds):
    minutes = seconds // 60
    seconds %= 60
    return "%02i:%02i" % (minutes, seconds)
