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

import csv
from typing import Iterator
from .. import Mesh, Element, Set
from ..element import NODE_COUNT_TABLE
from ..surface import NodeSurface, ElementSurface
from pygccx.enums import EEtypes, ESetTypes, ESurfTypes
from pygccx.protocols import ISet, ISurface
from pygccx.exceptions import ElementTypeNotSupportedError


def mesh_from_inp(filename:str, ignore_unsup_elems:bool=False, clear_mesh:bool=False) -> Mesh:
    """
    Builds a pygccx mesh object from the given ccx input file.

    Only nodes, 3D solid elements, node- and element sets and surfaces will be read.

    If ignore_unsup_elems==True element blocks with unsupported elements (i.e. beam, shell) are skipped.
    If False, an ElementTypeNotSupportedError is raised if there are unsupported
    elements in the file.

    if clear_mesh==True the resulting mesh object is cleared. This means all element ids,
    node ids and element faces which are not referred by any element are removed from every
    set and surface. If False, no clearing is done. 

    Args:
        filename (str): File name incl. path of ccx input file. 
        ignore_unsup_elems (bool, optional): Flag if unsupported elements should be skipped. If False, an ElementTypeNotSupportedError
            is raised if an unsupported solid element is processed. Defaults to False.
        clear_mesh (bool, optional): Flag if mesh object should be cleared. 
    
    Returns:
        Mesh: The converted mesh
    """
    mesh = _parse_content(filename, ignore_unsup_elems, 
                read_nodes=True, read_elems=True,
                read_nsets=True, read_elsets=True,
                read_surfs=True,)
    if clear_mesh: return _clear_mesh(mesh)
    return mesh

def nsets_from_inp(filename:str) -> list[ISet]:

    mesh = _parse_content(filename, True, read_nsets=True)
    return mesh.node_sets

def elsets_from_inp(filename:str) -> list[ISet]:

    mesh = _parse_content(filename, True, read_elsets=True)
    return mesh.element_sets

def surfaces_from_inp(filename:str) -> list[ISurface]:

    mesh = _parse_content(filename, True, read_surfs=True)
    return mesh.surfaces

def _read_and_expand_inp(filename:str) -> list[list[str]]:

    out = []
    with open(filename) as f:
        csv_reader = csv.reader(f, delimiter=',')

        for line in csv_reader:
            if not line : continue
            line = line if line[-1] else line[:-1] # delete empty last element
            if line[0] == '*INCLUDE':
                input = line[1].split('=')[-1]
                out += _read_and_expand_inp(input)
            else:
                out.append(line)
    return out

def _parse_content(filename:str, ignore:bool=False, **options):

    read_nodes = options.get('read_nodes', False)
    read_elems = options.get('read_elems', False)
    read_nsets = options.get('read_nsets', False)
    read_elsets = options.get('read_elsets', False)
    read_surfs = options.get('read_surfs', False)

    lines = iter(_read_and_expand_inp(filename))
    nodes = {}
    elems = {}
    nsets:dict[str, ISet] = {}
    elsets:dict[str, ISet] = {}
    surfs:list[ISurface] = []

    line = next(lines, None)
    while line:

        key = line[0].upper()

        if key.startswith('*'):
            if key == '*NODE' and read_nodes:
                n, s, line = _read_node_block(line, lines)
                nodes.update(n)
                if s and read_nsets:
                    if s.name not in nsets: nsets[s.name] = s
                    else: nsets[s.name].ids.update(s.ids)             
                continue
            elif key == '*ELEMENT' and read_elems:
                e, s, line = _read_element_block(line, lines, ignore)
                elems.update(e)
                if s and read_elsets:
                    if s.name not in elsets: elsets[s.name] = s
                    else: elsets[s.name].ids.update(s.ids)  
                continue
            elif key == '*NSET' and read_nsets:
                s, line = _read_nset_block(line, lines)
                if s: 
                    if s.name not in nsets: nsets[s.name] = s
                    else: nsets[s.name].ids.update(s.ids)  
                continue
            elif key == '*ELSET' and read_elsets:
                s, line = _read_elset_block(line, lines)
                if s:
                    if s.name not in elsets: elsets[s.name] = s
                    else: elsets[s.name].ids.update(s.ids)  
                continue
            elif key == '*SURFACE' and read_surfs:
                surf, line = _read_surface_block(line, lines)
                if surf: surfs.append(surf)
                continue
                

        line = next(lines, None)
        
    return Mesh(nodes, elems, list(nsets.values()), 
                list(elsets.values()), surfs)

def _get_param_value(line:list[str], param_name:str) -> str|None:

    val = None
    for c in line:
        if c.upper().startswith(param_name.upper()):
            return c.split('=')[-1]

def _read_node_block(line:list[str], lines:Iterator[list[str]]) -> tuple[dict, ISet|None, list[str]]:

    set_name = _get_param_value(line, 'NSET')

    nodes = {}
    for line in lines:
        if line[0].startswith('*'): break

        id = int(line[0])
        coords = tuple(float(c) for c in line[1:])
        nodes[id] = coords

    nset = None
    if set_name:
        nset = Set(set_name.upper(), ESetTypes.NODE, set(nodes.keys()))

    return nodes, nset, line

def _read_element_block(line:list[str], lines:Iterator[list[str]], ignore:bool) -> tuple[dict, ISet|None, list[str]]:

    # check if node set is specified:
    set_name = _get_param_value(line, 'ELSET')

    # get element type
    etype = _get_param_value(line, 'TYPE')
    if not _check_etype(etype, ignore):
        return {}, None, next(lines, None)  # type: ignore

    etype = EEtypes[etype.upper()] # type: ignore
      
    elems = {}
    for line in lines:
        if line[0].startswith('*'): break

        eid = int(line[0])
        nids = tuple(int(c) for c in line[1:])
        if NODE_COUNT_TABLE[etype] > 15:
            nids += tuple(int(c) for c in next(lines))
        elems[eid] = Element(eid, etype, nids)

    elset = None
    if set_name:
        elset = Set(set_name.upper(), ESetTypes.ELEMENT, set(elems.keys()))

    return elems, elset, line

def _read_nset_block(line:list[str], lines:Iterator[list[str]]) -> tuple[ISet, list[str]]:

    set_name = _get_param_value(line, 'NSET')   
    generate = 'GENERATE' in ','.join(line).upper()

    if generate:
        line = next(lines)
        start, stop, inc = [int(c) for c in line]
        nids = range(start, stop+1, inc)
        return Set(set_name.upper(), ESetTypes.NODE, 0, set(nids)), line  # type: ignore

    nids = []
    for line in lines:
        if line[0].startswith('*'): break
        nids += [int(c) for c in line if c]
    return Set(set_name.upper(), ESetTypes.NODE, set(nids)), line  # type: ignore

def _read_elset_block(line:list[str], lines:Iterator[list[str]]) -> tuple[ISet, list[str]]:
    set_name = _get_param_value(line, 'ELSET')   
    generate = 'GENERATE' in ','.join(line).upper()

    if generate:
        line = next(lines)
        start, stop, inc = [int(c) for c in line]
        eids = range(start, stop+1, inc)
        return Set(set_name.upper(), ESetTypes.ELEMENT, 0, set(eids)), line  # type: ignore

    eids = []
    for line in lines:
        if line[0].startswith('*'): break
        eids += [int(c) for c in line if c]
    return Set(set_name.upper(), ESetTypes.ELEMENT, set(eids)), line  # type: ignore

def _read_surface_block(line:list[str], lines:Iterator[list[str]]) -> tuple[ISurface, list[str]]:

    surf_name = _get_param_value(line, 'NAME')   
    if surf_name: surf_name = surf_name.upper()
    surf_type = _get_param_value(line, 'TYPE')
    if surf_type: surf_type = ESurfTypes(surf_type)
    else: surf_type = ESurfTypes.EL_FACE

    if surf_type == ESurfTypes.EL_FACE:
        faces = set[tuple[int,...]]()
        for line in lines:
            if line[0].startswith('*'): break
            faces.add((int(line[0]), int(line[1][1:])))
        
        return ElementSurface(surf_name, faces), line  # type: ignore

    nids = set[int]()
    set_names = set[str]()
    for line in lines:
        if line[0].startswith('*'): break
        try:
            nids.add(int(line[0]))
        except:
            set_names.add(line[0])
    return NodeSurface(surf_name, nids, set_names), line  # type: ignore

def _check_etype(etype:str|None, ignore:bool) -> bool:

    if not etype:
        if ignore: return False
        raise ElementTypeNotSupportedError(
            f'Element with type {etype} is not supported!'
        )

    if not etype.upper() in {e.name for e in EEtypes}:
        if ignore: return False
        raise ElementTypeNotSupportedError(
            f'Element with type {etype} is not supported!'
        )
    return True

def _clear_mesh(mesh:Mesh) -> Mesh:

    used_nodes = set[int]()
    for e in mesh.elements.values():
        used_nodes.update(e.node_ids)

    # clear nodes
    mesh.nodes = {nid: mesh.nodes[nid] for nid in used_nodes}

    # clear nsets
    for nset in mesh.node_sets:
        nset.ids.intersection_update(used_nodes)

    # clear elsets
    for elset in mesh.element_sets:
        elset.ids.intersection_update(mesh.elements)

    # clear surfaces
    node_set_names = {s.name for s in mesh.node_sets}
    for s in mesh.surfaces:
        if isinstance(s, ElementSurface): 
            faces = {f for f in s.element_faces if f[0] in mesh.elements}
            s.element_faces.intersection_update(faces)
        elif isinstance(s, NodeSurface):
            s.node_ids.intersection_update(used_nodes)
            s.node_set_names.intersection_update(node_set_names)

    return mesh


