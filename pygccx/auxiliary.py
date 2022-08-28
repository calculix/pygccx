from .protocols import number

def f2s(x:number) -> str:
    """Returns a string of the given number in the form 15.7e"""
    return f'{x:.7e}'