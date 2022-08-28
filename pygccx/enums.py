'''
Copyright Matthias Sedlmaier 2022
This file is part of pygccx.

pygccx is free software: you can redistribute it 
and/or modify it under the terms of the GNU General Public License as 
published by the Free Software Foundation, either version 3 of the 
License, or (at your option) any later version.

pygccx is distributed in the hope that it will 
be useful, but WITHOUT ANY WARRANTY; without even the implied warranty 
of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with pygccx.  
If not, see <http://www.gnu.org/licenses/>.
'''

from enum import Enum, IntEnum, auto

class ESetTypes(IntEnum):
    NODE = 0
    """Set or surface of nodes"""
    ELEMENT = 1
    """Set of elements or surface of element faces"""

class ESurfTypes(str, Enum):
    NODE = 'NODE'
    """Set or surface of nodes"""
    EL_FACE = 'ELEMENT'
    """Set of elements or surface of element faces"""

class EEtypes(IntEnum):
    # Point Elements
    SPRING1 = auto()
    """One-node 3-dimensional spring"""
    DCOUP3D = auto()
    """One-node coupling element"""
    MASS = auto()
    """One-node mass element"""
    # Spring, Gap und Dashpot
    GAPUNI = auto()
    """Two-node unidirectional gap element"""
    DASHPOTA = auto()
    """Two-node 3-dimensional dashpot"""
    SPRING2 = auto()
    """Two-node 3-dimensional spring"""
    SPRINGA = auto()
    """Two-node 3-dimensional spring"""
    # 3D Solid Elements
    C3D4 = auto()
    """Four-node tetrahedral element"""
    C3D8 = auto()
    """Eight-node brick element"""
    C3D8R = auto()
    """Eight-node brick element with reduced integration"""
    C3D8I = auto()
    """Incompatible mode eight-node brick element"""
    C3D6 = auto()
    """Six-node wedge element"""
    C3D10 = auto()
    """Ten-node tetrahedral element"""
    C3D20 = auto()
    """Twenty-node brick element"""
    C3D20R = auto()  
    """Twenty-node brick element with reduced integration"""
    C3D15 = auto()
    """Fifteen-node wedge element"""

class ECouplingTypes(str, Enum):
    DISTRIBUTING = '*DISTRIBUTING'
    """A distributing
        constraint specifies that a force or a moment in the reference node is distributed
        among the nodes belonging to the element surface. The weights are calculated
        from the area within the surface the reference node corresponds with."""
    KINEMATIC = '*KINEMATIC'
    """A kinematic constraint specifies that the displacement in a certain direction i  
       at a node corresponds to the rigid body motion of this node about a reference node. 
       Therefore, the location of the reference node is important."""

class EELasticTypes(str, Enum):
    ISO = 'ISO'
    """Isotropic"""
    ORTHO = 'ORTHO'
    """Orthotropic"""
    ENGINEERING_CONSTANTS = 'ENGINEERING CONSTANTS'
    """Orthotropic defined by engineering constants """
    ANISO = 'ANISO'
    """Anisotropic"""

class EOrientationSystems(str, Enum):
    RECTANGULAR = 'RECTANGULAR'
    """Right-handed cartesian system"""
    CYLINDRICAL = 'CYLINDRICAL'
    """Right-handed cylindrical system"""

class EOrientationRotAxis(IntEnum):
    NONE = 0
    """No rotation"""
    X = 1
    """Rotation about local X-Axis"""
    Y = 2
    """Rotation about local Y-Axis"""
    Z = 3
    """Rotation about local Z-Axis"""

class ELoadOps(str, Enum):
    MOD = 'MOD'
    NEW = 'NEW'

class EResultOutputs(str, Enum):
    DEFAULT = 'DEFAULT'
    """Default output for 1D and 2D Elements"""
    _2D = '2D'
    """Output of 1D and 2D Elements in their non-expanded form"""
    _3D = '3D'
    """Output of 1D and 2D Elements in their expanded form"""

class ENodeFileResults(str, Enum):
    KEQ = 'KEQ'
    """stress intensity factor"""
    MAXU = 'MAXU'
    """worst displacement orthogonal to a given vector in cyclic symmetric frequency calculations"""
    NT = 'NT'
    """structural temperature"""
    PNT = 'PNT'
    """magnitude and phase of temperature"""
    PRF = 'PRF'
    """magnitude and phase of external forces"""
    PU = 'PU'
    """magnitude and phase of displacement"""
    RF = 'RF'
    """total force"""
    SEN = 'SEN'
    """sensitivity"""
    U = 'U'
    """displacement"""
    V = 'V'
    """velocity of a structure"""

class EElFileResults(str, Enum):
    E = 'E'
    """Lagrange strain"""
    ENER = 'ENER'
    """internal energy density"""
    ERR = 'ERR'
    """error estimator for the worst principal stress"""
    HER = 'HER'
    """error estimator for the temperature"""
    HFL = 'HFL'
    """heat flux in a structure"""
    MAXE = 'MAXE'
    """worst principal strain in cyclic symmetric frequency calculations"""
    MAXS = 'MAXS'
    """worst principal stress in cyclic symmetric frequency calculations"""
    ME = 'ME'
    """mechanical strain"""
    PEEQ = 'PEEQ'
    """equivalent plastic strain"""
    S = 'S'
    """Cauchy stress (structure)"""
    THE = 'THE'
    """thermal strain"""
    ZZS = 'ZZS'
    """Zienkiewicz-Zhu stress"""

class EContactFileResults(str, Enum):
    CDIS = 'CDIS'
    """relative contact displacements"""
    CSTR = 'CSTR'
    """contact stress"""
    CELS = 'CELS'
    """contact energy"""
    PCON = 'PCON'
    """amplitude and phase of the relative contact"""

class ENodePrintResults(str, Enum):
    NT = 'NT'
    """structural temperature"""
    RF = 'RF'
    """total force"""
    U = 'U'
    """displacement"""
    V = 'V'
    """velocity of a structure"""

class EElPrintResults(str, Enum):
    COORD = 'COORD'
    """Coordinates"""
    E = 'E'
    """Lagrange strain"""
    ENER = 'ENER'
    """Internal energy density"""
    HFL = 'HFL'
    """Heat flux in a structure"""
    ME = 'ME'
    """Mechanical strain"""
    PEEQ = 'PEEQ'
    """Equivalent plastic strain"""
    S = 'S'
    """Cauchy stress (structure)"""
    ELKE = 'ELKE'
    """Kinetic energy"""
    ELSE = 'ELSE'
    """Internal energy"""
    EMAS = 'EMAS'  
    """Mass and mass moments of inertia"""
    EVOL = 'EVOL'
    """Volume"""

class EContactPrintResults(str, Enum):
    CDIS = 'CDIS' 
    """relative contact displacements"""
    CELS = 'CELS'
    """contact energy"""
    CF = 'CF'
    """total contact force"""
    CFN = 'CFN'
    """total normal contact force"""
    CFS = 'CFS'
    """total shear contact force"""
    CNUM = 'CNUM'
    """total number of contact elements"""
    CSTR = 'CSTR'
    """contact stress"""
    
class EFrdEntities(str, Enum):
    CT3D_MIS = 'CT3D-MIS'
    """Stress intensity factor"""
    MDISP = 'MDISP'
    """Worst displacement orthogonal to a given vector
     in cyclic symmetric frequency calculations"""
    NDTEMP = 'NDTEMP'
    """Structural temperature; total temperature in a network"""
    PNDTEMP = 'PNDTEMP'
    """magnitude and phase of temperature"""
    PFORC = 'PFORC'
    """Magnitude and phase of external forces"""
    PDISP = 'PDISP'
    """Magnitude and phase of displacement"""
    FORC = 'FORC'
    """Real part of total force"""
    FORCI = 'FORCI'
    """Imaginary part of total force"""
    SEN = 'SEN'
    """Sensitifity"""
    DISP = 'DISP'
    """Real part of displacement"""
    DISPI = 'DISPI'
    """Imaginary part of displacement"""
    VELO = 'VELO'
    """Velocity"""

    TOSTRAIN = 'TOSTRAIN'
    """Real part of lagrange strain"""
    TOSTRAII = 'TOSTRAII'
    """Imaginary part of lagrange strain"""
    ENER = 'ENER'
    """Internal energy density"""
    ERROR = 'ERROR'
    """Real part of error estimator for the worst principal stress"""
    ERRORI = 'ERRORI'
    """Imaginary part of error estimator for the worst principal stress"""
    HERROR = 'HERROR'
    """Real part of error estimator for the temperature"""
    HERRORI = 'HERRORI'
    """Imaginary part of error estimator for the temperature"""
    FLUX = 'FLUX'
    """Heat flux in a structure"""
    MSTRAIN = 'MSTRAIN'
    """worst principal strain in cyclic symmetric frequency calculations"""
    MSTRESS = 'MSTRESS'
    """worst principal stress in cyclic symmetric frequency calculations"""
    MESTRAIN = 'MESTRAIN'
    """Real part of mechanical strain"""
    MESTRAII = 'MESTRAII'
    """Imaginary part of mechanical strain"""
    PE = 'PE'
    """Equivalent plastic strain"""
    STRESS = 'STRESS'
    """Real part of Cauchy stress (structure)"""
    STRESSI = 'STRESSI'
    """Imaginary part of Cauchy stress (structure)"""
    THSTRAIN = 'THSTRAIN'
    """thermal strain"""
    ZZSTR = 'ZZSTR'
    """Real part of Zienkiewicz-Zhu stress"""
    ZZSTRI = 'ZZSTRI'
    """Imaginary part of Zienkiewicz-Zhu stress"""

    CONTACT = 'CONTACT'
    """Real part of relative contact displacements"""
    CONTACTI = 'CONTACTI'
    """Imaginary part of relative contact displacements"""
    CELS = 'CELS'
    """contact energy"""
    PCONTAC = 'PCONTAC'
    """amplitude and phase of the relative contact displacements and contact stresses"""

class EDatEntities(str, Enum):
    # Node Print entities
    U = 'displacements' 
    """Displacements"""
    RF = 'forces' 
    """Total force"""

    # El Print entities
    S = 'stresses' 
    """Cauchy stress (structure)"""
    E = 'strains' 
    """Lagrange strain"""
    ME = 'mechanical strains' 
    """Mechanical strain"""
    PEEQ = 'equivalent plastic strain' 
    """Equivalent plastic strain"""
    EVOL = 'volume' 
    """Volume"""
    COORD = 'global coordinates' 
    """Global coordinates"""
    ENER = 'internal energy density' 
    """Internal energy density"""
    ELKE = 'kinetic energy' 
    """Kinetic energy"""
    ELSE = 'internal energy' 
    """Internal energy"""
    EMAS = 'mass'
    """Mass and mass moments of inertia"""
    # Contact print entities
    CELS = 'contact print energy' 
    """Contact energy"""
    CSTR = 'contact stress' 
    """Contact stress"""
    CDIS = 'relative contact displacement' 
    """Relative contact displacement"""
    
class EPrintTotals(str, Enum):
    YES = 'YES'
    ONLY = 'ONLY'
    NO = 'NO'

class ESolvers(str, Enum):
    DEFAULT = 'DEFAUL'
    ITERATIVE_SCALING = 'ITERATIVE SCALING'
    ITERATIVE_CHOLESKY = 'ITERATIVE CHOLESKY'
    SPOOLES = 'SPOOLES'
    PASTIX = 'PASTIX'

class EStepAmplitudes(str, Enum):
    RAMP = 'RAMP'
    """Loads are ramped during the step"""
    STEP = 'STEP'
    """Loads are fully applied at beginning of step"""

class EHardeningRules(str, Enum):
    ISOTROPIC = 'ISOTROPIC'
    """Isotropic hardening rule"""
    KINEMATIC = 'KINEMATIC'
    """Kinematic hardening rule"""
    COMBINED = 'COMBINED'
    """Combined isotropic and kinematic hardening rule"""

class EPressureOverclosures(str, Enum):
    EXPONENTIAL = 'EXPONENTIAL'
    LINEAR = 'LINEAR'
    TABULAR = 'TABULAR'
    TIED = 'TIED'
    HARD = 'HARD'

class EContactTypes(str, Enum):
    NODE_TO_SURFACE = 'NODE TO SURFACE'
    SURFACE_TO_SURFACE = 'SURFACE TO SURFACE'
    MORTAR = 'MORTAR' 
    LINMORTAR = 'LINMORTAR'
    PGLINMORTAR = 'PGLINMORTAR'

class EReultEntityTypes(str, Enum):
    SCALAR = 'SCALAR'
    VECTOR = 'VECTOR'
    TENSOR = 'TENSOR'

class EResultLocations(str, Enum):
    NODAL = 'NODAL'
    ELEMENT = 'ELEMENT'
    INT_PNT = 'INT_PNT'


