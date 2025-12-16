from src.router.dispatcher import dispatch

def lambda_handler(event, context):
    return dispatch(event, context)
