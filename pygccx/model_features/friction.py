from dataclasses import dataclass

number = int|float
@dataclass(frozen=True, slots=True)
class Friction:

    """
    Class to define the friction behavior of a surface interaction 

    Args:
        mue: Friction coefficient > 0
        lam: Stick-slope in force/volume > 0
        name: Optional. Name of this instance
        desc: Optional. A short description of this instance. This is written to 
                the ccx input file.
    """
    mue:number
    """Friction coefficient > 0"""
    lam:number
    """Stick-slope in force/volume > 0"""
    name:str = ''
    """Name of this instance"""
    desc:str = ''
    """A short description of this instance. This is written to the ccx input file."""

    def __post_init__(self):
        if self.mue <= 0:
            raise ValueError(f'mue must be greater than 0, got {self.mue}')
        if self.lam <= 0:
            raise ValueError(f'lam must be greater than 0, got {self.lam}')

    def __str__(self):
        s = '*FRICTION\n'
        s += f'{self.mue},{self.lam}\n'
        return s