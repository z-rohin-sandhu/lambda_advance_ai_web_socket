from src.router.dispatcher import dispatch

def lambda_handler(event, context):
    print(
        "[lambda_handler] Invoked: "
        f"event_type={type(event).__name__}, "
        f"event_keys={(list(event.keys()) if isinstance(event, dict) else 'n/a')}, "
        f"aws_request_id={getattr(context, 'aws_request_id', None)}"
    )
    response = dispatch(event, context)
    print(
        "[lambda_handler] Completed: "
        f"response_type={type(response).__name__}"
    )
    return response
