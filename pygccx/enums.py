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
    """Two-node 3-dimensional dashpo"""
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
    """Six-node wedge elemen"""
    C3D10 = auto()
    """Ten-node tetrahedral element"""
    C3D20 = auto()
    """Twenty-node brick element"""
    C3D20R = auto()  
    """Twenty-node brick element with reduced integration"""
    C3D15 = auto()
    """Fifteen-node wedge elemen"""

class ECouplingTypes(str, Enum):
    DISTRIBUTING = '*DISTRIBUTING'
    """A distributing
        constraint specifies that a force or a moment in the reference node is distributed
        among the nodes belonging to the element surface. The weights are calculated
        from the area within the surface the reference node corresponds with."""
    KINEMATIC = '*KINEMATIC'
    """A kinematic con-
        straint specifies that the displacement in a certain direction i at a node corre-
        sponds to the rigid body motion of this node about a reference node. Therefore,
        the location of the reference node is important."""

class EELasticTypes(str, Enum):
    ISO = 'ISO'
    """Isotropic"""
    ORTHO = 'ORTHO'
    """Orthotropic"""
    ENGINEERING_CONSTANTS = 'ENGINEERING CONSTANTS'
    """Orthotropic defined by eng. constants """
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

class ENodeResults(str, Enum):
    KEQ = 'KEQ'
    """Equivalent stress intensity factor and related quantities in crack propagation 
        calculations."""
    MAXU = 'MAXU'
    """Maximum displacements orthogonal to a given vector
        at all times for *FREQUENCY calculations with cyclic symmetry. The
        components of the vector are the coordinates of a node stored in a node
        set with the name RAY. This node and node set must have been defined
        by the user."""
    NT = 'NT'
    """Temperatures. This includes both structural temperatures and total fluid 
        temperatures in a network."""
    PNT = 'PNT'
    """Temperatures: magnitude and phase (only for *STEADY STATE DYNAMICS calculations)."""
    PRF = 'PRF'
    """External forces: magnitude and phase (only for *FREQUENCY calculations with 
        cyclic symmetry)."""
    PU = 'PU'
    """Displacements: magnitude and phase (only for *STEADY STATE DYNAMICS
        calculations and *FREQUENCY calculations with cyclic symmetry)."""
    RF = 'RF'
    """External forces (only static forces;
        dynamic forces, such as those caused by dashpots, are not included)"""
    SEN = 'SEN'
    """Sensitivities."""
    U = 'U'
    """Displacements."""
    V = 'V'
    """Velocities in dynamic calculations."""

class EElementResults(str, Enum):
    CEEQ= 'CEEQ'
    """equivalent creep strain (is converted internally into PEEQ
        since the viscoplastic theory does not distinguish between the two; conse-
        quently, the user will find PEEQ in the frd file, not CEEQ."""
    E = 'E'
    """strain. This is the total
        Lagrangian strain for (hyper)elastic materials and incremental plasticity
        and the total Eulerian strain for deformation plasticity."""
    ENER = 'ENER'
    """the energy density."""
    ERR = 'ERR'
    """error estimator for structural calculations, Notice that ERR and ZZS are 
        mutually exclusive."""
    HER = 'HER'
    """error estimator for heat transfer calculations."""
    HFL = 'Heat flux in structures.'
    """Displacements: magnitude and phase (only for *STEADY STATE DYNAMICS
        calculations and *FREQUENCY calculations with cyclic symmetry)."""
    MAXE = 'MAXE'
    """Maximum of the absolute value of the worst principal
        strain at all times for *FREQUENCY calculations with cyclic symmetry.
        It is stored for nodes belonging to the node set with name STRAINDO-
        MAIN. This node set must have been defined by the user with the *NSET
        command. The worst principal strain is the maximum of the absolute
        value of the principal strains times its original sign"""
    MAXS = 'MAXS'
    """maximum of the absolute value of the worst principal
        stress at all times for *FREQUENCY calculations with cyclic symmetry.
        It is stored for nodes belonging to the node set with name STRESSDO-
        MAIN. This node set must have been defined by the user with the *NSET
        7.50 *EL FILE 439 command. The worst principal stress is the maximum 
        of the absolute value of the principal stresses times its original sign."""
    ME = 'ME'
    """strain. This is the
        mechanical Lagrangian strain for (hyper)elastic materials and incremental
        plasticity and the mechanical Eulerian strain for deformation plasticity
        (mechanical strain = total strain - thermal strain)."""
    PEEQ = 'PEEQ'
    """equivalent plastic strain."""
    PHS = 'PHS'
    """ stress: magnitude and phase (only for *STEADY STATE DYNAMICS
        calculations and *FREQUENCY calculations with cyclic symmetry)."""
    S = 'S'
    """true (Cauchy) stress in structures. For beam elements this tensor is 
        replaced by the section forces
        if SECTION FORCES is selected. Selection of S automatically triggers
        output of the error estimator ERR, unless NOE is selected after S (either
        immediately following S, or with some other output requests in between,
        irrespective whether these output requests are on the same keyword card
        or on different keyword cards)"""
    THE = 'THE'
    """strain. This is the thermal strain calculated by sub-
        tracting the mechanical strain (extrapolated to the nodes) from the total
        strain (extrapolated to the nodes) at the nodes. Selection of THE triggers
        the selection of E and ME. This is needed to ensure that E (the total
        strain) and ME (the mechanical strain) are extrapolated to the nodes."""
    ZZS = 'ZZS'
    """Zienkiewicz-Zhu improved stress. Notice that ZZS and ERR are mutually ex-
        clusive."""

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