class CustomError(Exception):
    """Base class for exceptions in this module."""
    pass

class InputCustomError(CustomError):
    """Exception raised for errors in the input.

    Attributes:
        expression -- input expression in which the error occurred
        message -- explanation of the error
    """

    def __init__(self, expression, message):
        self.expression = expression
        self.message = message

class TransitionCustomError(CustomError):
    """Raised when an operation attempts a state transition that's not
    allowed.

    Attributes:
        previous -- state at beginning of transition
        next -- attempted new state
        message -- explanation of why the specific transition is not allowed
    """

    def __init__(self, previous, nextt, message):
        self.previous = previous
        self.next = nextt
        self.message = message

class ErrorTest(CustomError):
    def __init__(self, error, message):
        self.expression = error
        self.message = message

