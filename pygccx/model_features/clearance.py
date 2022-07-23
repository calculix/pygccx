from dataclasses import dataclass
from protocols import ISurface

number = int|float

@dataclass(frozen=True, slots=True)
class Clearance:
    """
    Class to define a clearance between the slave and master surface of a contact pair

    Args:
        master: Independant surface
        slave: Dependant surface
        value: Clearance value
        name: Optional. The name of this Instance. Not used
        desc: Optional. A short description of this Instance. This is written to the ccx input file.
    """
    
    master:ISurface
    """Independant surface"""
    slave:ISurface
    """Dependant surface"""
    value:number
    """Clearance value"""
    name:str = ''
    """The name of this Instance. Not used"""
    desc:str = ''
    """A short description of this Instance. This is written to the ccx input file."""

    def __str__(self):
        return f'*CLEARANCE,MASTER={self.master.name},SLAVE={self.slave.name},VALUE={self.value}\n' 