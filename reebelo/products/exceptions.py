from reebelo.core.api.result import Error, ErrorCode


class InsufficientQuantity(Exception):
    """
    An when there isn't enough inventory to process a request
    """

    def __init__(self):
        self.error = Error(
            code=ErrorCode.INSUFFICIENT_QUANTITY,
            message="Error processing request due to insufficient quantity.",
        )
