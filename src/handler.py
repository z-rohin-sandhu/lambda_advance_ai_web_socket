from src.router.dispatcher import dispatch
from src.utils.logging import log

def lambda_handler(event, context):
    log(
        "lambda_handler invoked",
        event_type=type(event).__name__,
        event_keys=(list(event.keys()) if isinstance(event, dict) else "n/a"),
        aws_request_id=getattr(context, "aws_request_id", None),
    )
    response = dispatch(event, context)
    log(
        "lambda_handler completed",
        response_type=type(response).__name__,
    )
    return response
