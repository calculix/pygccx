from dataclasses import dataclass, field
from typing import Optional, Iterable
from enums import EPressureOverclosures
import numpy as np
import numpy.typing as npt

number = int|float

@dataclass(frozen=True, slots=True)
class SurfaceBehavior:
    """ 
    Class to define the surface behavior of a surface interaction.
    The surface behavior is required for a contact analysis.

    Args:
        pressure_overclosure: Option for pressure-overclosure
        c0: Mandatory for pressure_overclosure == EXPONENTIAL, optional for LINEAR and 
            node-to-face-contact, not used for LINEAR face-to-face-contact.

            For EXPONENTIAL: 
                Distance from the master surface at which the pressure is decreased to 1 % of p0.

            For LINEAR node-to-face-contact: 
                Distance factor from which the maximum clearance is calculated for which a spring 
                contact element is generated (by multiplying with the square root of the spring 
                area). Default value 10−3.
                
        p0: Mandatory for pressure_overclosure == EXPONENTIAL\n
            Contact pressureat zero distance

        k:bMandatory for pressure_overclosure == LINEAR and TIED\n
            Slope of the pressure-overclosure curve

        sig_inf: Mandatory for pressure_overclosure == LINEAR and node-to-face contact,
            not used for face-to-face contact.\n
            Tension value for large clearances

        table: Mandatory for pressure_overclosure == TABULAR\n
            Table with pressure - overclosure pairs in ascending order.

        name: Name of this instance

        desc: A short description of this instance. This is written to the ccx input file.
    """

    pressure_overclosure:EPressureOverclosures
    """Option for pressure-overclosure"""

    c0:Optional[number] = field(kw_only=True, default=None)
    """Mandatory for pressure_overclosure == EXPONENTIAL, optional for LINEAR and 
    node-to-face-contact, not used for LINEAR face-to-face-contact.

    For EXPONENTIAL: 
        Distance from the master surface at which the pressure is decreased to 1 % of p0.

    For LINEAR node-to-face-contact: 
        Distance factor from which the maximum clearance is calculated for which a spring 
        contact element is generated (by multiplying with the square root of the spring 
        area). Default value 10−3."""

    p0:Optional[number] = field(kw_only=True, default=None)
    """Mandatory for pressure_overclosure == EXPONENTIAL\n
    Contact pressureat zero distance"""

    k:Optional[number] = field(kw_only=True, default=None)
    """Mandatory for pressure_overclosure == LINEAR and TIED\n
    Slope of the pressure-overclosure curve"""

    sig_inf:Optional[number] = field(kw_only=True, default=None)
    """Mandatory for pressure_overclosure == LINEAR and node-to-face contact,
    not used for face-to-face contact.\n
    Tension value for large clearances"""

    table:Optional[Iterable[Iterable[number]]|npt.NDArray[np.float64]] = field(kw_only=True, default=None)
    """Mandatory for pressure_overclosure == TABULAR\n
    Table with pressure - overclosure pairs in ascending order."""

    name:str = ''
    """Name of this instance"""

    desc:str = ''
    """A short description of this instance. This is written to the ccx input file."""

    def __post_init__(self):
        if self.pressure_overclosure == EPressureOverclosures.EXPONENTIAL:
            if self.c0 is None:
                raise ValueError(f'c0 must be specified for pressure_overclosure == EXPONENTIAL')
            if self.c0 <= 0:
                raise ValueError(f'c0 must be greater than 0, got {self.c0}')
            if self.p0 is None:
                raise ValueError(f'p0 must be specified for pressure_overclosure == EXPONENTIAL')
            if self.p0 <= 0:
                raise ValueError(f'p0 must be greater than 0, got {self.p0}')
        if self.pressure_overclosure == EPressureOverclosures.LINEAR:
            if self.k is None:
                raise ValueError(f'k must be specified for pressure_overclosure == LINEAR')
            if self.k <= 0:
                raise ValueError(f'k must be greater than 0, got {self.k}')
            if self.sig_inf is not None and self.sig_inf <= 0:
                raise ValueError(f'sig_inf must be greater than 0, got {self.sig_inf}')
            if self.c0 is not None and self.c0 <= 0:
                raise ValueError(f'c0 must be greater than 0, got {self.c0}')
        if self.pressure_overclosure == EPressureOverclosures.TABULAR:
            if self.table is None:
                raise ValueError(f'tabl must be specified for pressure_overclosure == TABULAR')
        if self.pressure_overclosure == EPressureOverclosures.TIED:
            if self.k is None:
                raise ValueError(f'k must be specified for pressure_overclosure == TIED')
            if self.k <= 0:
                raise ValueError(f'k must be greater than 0, got {self.k}')

    def __str__(self):

        s = f'*SURFACE BEHAVIOR,PRESSURE-OVERCLOSURE={self.pressure_overclosure.value}\n'

        if self.pressure_overclosure == EPressureOverclosures.EXPONENTIAL:
            s += f'{self.c0:15.7e},{self.p0:15.7e}\n'

        if self.pressure_overclosure == EPressureOverclosures.LINEAR:
            s += f'{self.k:15.7e}'
            if self.sig_inf is not None:
                s += f',{self.sig_inf:15.7e}'
            if self.c0 is not None:
                s += f',{self.c0:15.7e}'
            s += '\n'

        if self.pressure_overclosure == EPressureOverclosures.TABULAR and self.table:
            for row in self.table:
                s += ','.join(f'{x:15.7e}' for x in row) + '\n'

        if self.pressure_overclosure == EPressureOverclosures.TIED:
            s += f'{self.k:15.7e}\n'

        return s
