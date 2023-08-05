from src.django_cassandra.common.messages import Messages


def response(data=[], message=Messages.SUCCESSFUL_MESSAGE, status=True):
    return {
        'status': status,
        'message': message,
        'data': data
    }
