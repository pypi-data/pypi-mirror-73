#Python replacement for PHP's isset
def isset(variable):
    return variable in locals() or variable in globals()