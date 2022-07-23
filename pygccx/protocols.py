from typing import Protocol, runtime_checkable
import enums

class ISurface(Protocol):
    name:str
    """Gets the name of this surface """
    type: enums.ESurfTypes
    """Gets the type of this surface"""

    def write_ccx(self, buffer:list[str]): 
        """Writes the ccx input string of this surface to the given buffer"""

class IElementFace(Protocol):
    number:int
    """Gets the number of this element face inside the element with element_id"""
    element_id:int
    """Gets the id of the element this element face belongs to"""
    node_ids:tuple[int, ...]
    """Gets the node ids of this element face"""
    name:str
    """Gets the name of this element face"""

class IElement(Protocol):
    id:int
    """Gets the id of this element"""
    type:enums.EEtypes
    """Gets the GMSH type of this element"""
    node_ids:tuple[int, ...]
    """Gets the node ids of this element"""

    def get_dim(self) -> int:
        """Gets the dimension of this element"""
        ...
    def get_corner_node_count(self) -> int:
        """Gets the number of corner nodes for this element"""
        ...
    def get_corner_node_ids(self) -> tuple[int, ...]:
        """Gets the corner node ids for this element"""
        ...
    def get_faces(self) -> tuple[IElementFace, ...]:
        """Gets the faces for this element"""
        ...

@runtime_checkable
class ISet(Protocol):
    name:str
    """Gets the name of this set"""
    type:enums.ESetTypes
    """Gets the type of this set"""
    dim:int
    """Gets the dimension of this set"""
    ids:set[int]
    """Gets the ids of this set"""

@runtime_checkable
class IModelFeature(Protocol):
    name:str
    """Gets the name of this model feature"""
    desc:str
    """Gets the dircription of this model feature. This will alse be written to the ccx input file"""

@runtime_checkable
class IStepFeature(Protocol):
    name:str
    """Gets the name of this model feature"""
    desc:str
    """Gets the dircription of this model feature. This will alse be written to the ccx input file"""

@runtime_checkable
class IStep(Protocol):
    desc:str
    step_features:list[IStepFeature]

    def add_step_features(self, *step_features:IStepFeature): ...