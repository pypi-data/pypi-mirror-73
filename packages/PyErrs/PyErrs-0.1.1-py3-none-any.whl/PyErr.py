class NumberError(TypeError):
    pass

class LessThanZeroError(NumberError):
    pass

class MoreThanZeroError(NumberError):
    pass

class EqualToZeroError(NumberError):
    pass

class NotLessThanZeroError(NumberError):
    pass

class NotMoreThanZeroError(NumberError):
    pass

class NotEqualToZeroError(NumberError):
    pass

class ArgError(TypeError):
    pass
