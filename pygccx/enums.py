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
    """coordinates"""
    E = 'E'
    """Lagrange strain"""
    ENER = 'ENER'
    """internal energy density"""
    HFL = 'HFL'
    """heat flux in a structure"""
    ME = 'ME'
    """mechanical strain"""
    PEEQ = 'PEEQ'
    """equivalent plastic strain"""
    S = 'S'
    """Cauchy stress (structure)"""
    ELKE = 'ELKE'
    """kinetic energy"""
    ELSE = 'ELSE'
    """ELSE"""
    EMAS = 'EMAS'  
    """mass and mass moments of inertia"""
    EVOL = 'EVOL'
    """volume"""

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
    MDISP = 'MDISP'
    NDTEMP = 'NDTEMP'
    PNDTEMP = 'PNDTEMP'
    PFORC = 'PFORC'
    PDISP = 'PDISP'
    FORC = 'FORC'
    FORCI = 'FORCI'
    SEN = 'SEN'
    DISP = 'DISP'
    DISPI = 'DISPI'
    VELO = 'VELO'

    TOSTRAIN = 'TOSTRAIN'
    TOSTRAII = 'TOSTRAII'
    ENER = 'ENER'
    ERROR = 'ERROR'
    ERRORI = 'ERRORI'
    HERROR = 'HERROR'
    HERRORI = 'HERRORI'
    FLUX = 'FLUX'
    MSTRAIN = 'MSTRAIN'
    MSTRESS = 'MSTRESS'
    MESTRAIN = 'MESTRAIN'
    MESTRAII = 'MESTRAII'
    PE = 'PE'
    STRESS = 'STRESS'
    STRESSI = 'STRESSI'
    THSTRAIN = 'THSTRAIN'
    ZZSTR = 'ZZSTR'
    ZZSTRI = 'ZZSTRI'

    CONTACT = 'CONTACT'
    CONTACTI = 'CONTACTI'
    CELS = 'CELS'
    PCONTAC = 'PCONTAC'

class EDatEntities(str, Enum):
    # Node Print entities
    U = 'displacements' 
    RF = 'forces' 
    # El Print entities
    S = 'stresses' 
    E = 'strains' 
    ME = 'mechanical strains' 
    PEEQ = 'equivalent plastic strain' 
    EVOL = 'volume' 
    COORD = 'global coordinates' 
    ENER = 'internal energy density' 
    ELKE = 'kinetic energy' 
    ELSE = 'internal energy' 
    # Contact print entities
    CELS = 'contact print energy' 
    CSTR = 'contact stress' 
    CDIS = 'relative contact displacement' 
    
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


