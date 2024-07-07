from typing import Optional

from pygccx.enums import EEtypes
from pygccx.exceptions import ElementTypeNotSupportedError
from .. import Mesh, Element
from . inp_factory import _clear_mesh

FRD_2_CCX_ETYPE_MAP = {  
    1 : EEtypes.C3D8I,
    2 : EEtypes.C3D6,
    3 : EEtypes.C3D4,
    4: EEtypes.C3D20R,  
    5: EEtypes.C3D15,
    6: EEtypes.C3D10
}

FRD_2_CCX_ALLOWED_MAPPING = {
    1 : (EEtypes.C3D8I, EEtypes.C3D8, EEtypes.C3D8R),
    2 : (EEtypes.C3D6,),
    3 : (EEtypes.C3D4,),
    4: (EEtypes.C3D20R, EEtypes.C3D20),
    5: (EEtypes.C3D15,),
    6: (EEtypes.C3D10,)
}

def mesh_from_frd(filename:str, type_mapping:Optional[dict[int, EEtypes]]=None, 
                  ignore_unsup_elems:bool=False, clear_mesh:bool=False) -> Mesh:
    """
    Builds a pygccx mesh object from the given cgx result file.

    Only nodes and 3D solid elements will be read.

    If ignore_unsup_elems==True element blocks with unsupported elements (all 1D and 2D elements) are skipped.
    If False, an ElementTypeNotSupportedError is raised if there are unsupported
    elements in the file.

    if clear_mesh==True the resulting mesh object is cleared. This means all element ids,
    node ids and element faces which are not referred by any element are removed from every
    set and surface. If False, no clearing is done. 

    Args:
        filename (str): File name incl. path of cgx result file. 
        ignore_unsup_elems (bool, optional): Flag if unsupported elements should be skipped. If False, an ElementTypeNotSupportedError
            is raised if an unsupported solid element is processed. Defaults to False.
        clear_mesh (bool, optional): Flag if mesh object should be cleared. 
    
    Returns:
        Mesh: The converted mesh
    """
    
    #Conversion Table for Element Types. if not specified as Parameter, take FRD_2_CCX_ETYPE_MAP as default
    if type_mapping is None: type_mapping = FRD_2_CCX_ETYPE_MAP
    _check_type_mapping(type_mapping)
    
    # For the format definition of *.frd look at the CGX Manual
    nodes = {}
    elems = {}
    
    # Parse the file
    #-----------------------------------------------------
    with open(filename) as f:
        line = next(f)
        while line:
            line_split = line.split() #split line at white spaces
            line_key = line_split[0]    
            if line_key == '2C':
                n, line = _read_node_block(line, f)
                nodes.update(n)
                continue
            if line_key == '3C': 
                e, line = _read_element_block(line, f, type_mapping, ignore_unsup_elems)
                elems.update(e)
                continue
            if line_key.startswith('100C'):
                break # Nodal Result block starts -> Finish
            
            line = next(f, None)

    mesh = Mesh(nodes, elems, [], [])
    if clear_mesh: return _clear_mesh(mesh)
    return mesh

def _read_node_block(line:str, f) -> tuple[dict[int, tuple[float,...]], str]:

    nodes = {}
    for line in f:
        line_split = line.split()
        key = line_split[0] 
        if key == '-3': break

        n_id=int(line[3:13])
        n_x=float(line[13:25])
        n_y=float(line[25:37])
        n_z=float(line[37:])
        nodes[n_id] = (n_x, n_y, n_z)

    return nodes, line

def _read_element_block(line:str, f, type_mapping:dict, skip_unsup_elems:bool):

    elems = {}
    for line in f:
        line_split = line.split()
        key = line_split[0]    
        if key == '-3': 
            break
       
        if key == '-1':
            e_id = int(line_split[1])
            e_type = int(line_split[2])
            skip = False
            if e_type not in FRD_2_CCX_ALLOWED_MAPPING:
                if skip_unsup_elems: 
                    skip = True
                    continue
                raise ElementTypeNotSupportedError(
                    f'{e_type} is not a supported frd element type number.'
                )
            nids = []

        if key == '-2' and not skip:
            for nId in line_split[1:]:
                nId = int(nId)
                nids.append(nId)

            elems[e_id] = Element(e_id, type_mapping[e_type], tuple(nids))

    return elems, line

def _check_type_mapping(type_mapping:dict[int, EEtypes]):

    for gt, ccxt in type_mapping.items():
        if gt not in FRD_2_CCX_ALLOWED_MAPPING:
            raise ValueError(f'{gt} is not a supported frd element type number.')

        allowed_types = FRD_2_CCX_ALLOWED_MAPPING[gt]
        if ccxt not in allowed_types:
            allowed_str = ','.join([x.name for x in allowed_types])
            raise ValueError(f'frd type {gt} can not be mapped to {ccxt.name}. Only {allowed_str} are allowed')
