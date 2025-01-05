class NotFoundException(Exception):
    """
    Is used if a requested resource is not found.
    """
    def __init__(self, message='Resource not found'):
        self.message = message
        super().__init__(self.message) #call consturctor of base class

class ValidationException(Exception):
    """
    Is used when input data does not correspond to the expected conditions.    
    """
    def __init__(self, message='Validation error'):
        self.message = message
        super().__init__(self.message)
        