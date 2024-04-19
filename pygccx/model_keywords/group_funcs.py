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

from typing import Optional

from . import ContactPair, SurfaceInteraction, SurfaceBehavior, Friction, Clearance
from pygccx.enums import EContactTypes, EPressureOverclosures
from pygccx.protocols import ISet, ISurface, IKeyword, number

def make_contact(name:str, contact_type:EContactTypes, dep_surf:ISurface, ind_surf:ISurface,
                pressure_overclosure:EPressureOverclosures, small_sliding:bool=False,              
                adjust:Optional[number|ISet]=None, clearance:Optional[number]=None, 
                mue:Optional[number]=None, lam:Optional[number]=None, desc:str='', **kwargs) -> tuple[IKeyword]:

    """
    Function to set up a contact.

    This function creates all the necessary model keywords needed for a contact and
    returns this keywords in a tuple

    Args:
        name (str): Name of the contact.
        contact_type (EContactTypes): Enum of the contact type(i.e. NODE_TO_SURFACE)
        dep_surf (ISurface): Surface object for the dependent contact side. 
                             surf_type can be EL_FACE or NODE for contact_type NODE_TO_SURFACE 
        ind_surf (ISurface): Surface object for the independent contact side.
                             surf_type must be EL_FACE 
        pressure_overclosure (EPressureOverclosures): Enum of the pressure overclosure (i.e. EXPONENTIAL)
        small_sliding (bool): Optional. Flag is small sliding should be turned on. 
                              Only for contact_type NODE_TO_SURFACE.
        adjust (number | ISet): Optional. Value or node set for contact adjustment
        clearance (number): Optional. Clearance between contact surfaces. 
                            If specified, a Clearance object is generated.
        mue (number): Friction coefficient. If specified, a Friction object is generated.
        lam (number): Stick slope. Must be provided if mue is given for frictional contact.
                      Optional for TIED. If ommitted for TIED, normal stiffness k is used.
        desc (str): Optional. Description of this contact.

    Keyword Args:
        c0 (number): decay-length for contact type EXPONENTIAL, spring generation 
                     distance for contact type LINEAR
        p0 (number): pressure at zero distance for contact type EXPONENTIAL
        k (number): contact stiffness for contact type LINEAR and TIED.
                    For TIED this value is also used for the tangential stiffness
                    if not specified by lam.
        sig_inf (number): pressure at high contact distance for contact type LINEAR 
                          and NODE TO SURFACE
        table (Iterable[Iterable[number]]): Pressure - Overclosure pairs for contact 
                                            type TABULAR


    Raises:
        ValueError: Raised if mue is specified, but not lam

    Returns:
        tuple[IKeyword]: All model keywords needed for this contact
    """
    out:list[IKeyword] = []

    # Surface Interaction
    interaction = SurfaceInteraction(name, desc)
    out.append(interaction)

    # Surface behavior
    if not (contact_type in (EContactTypes.MORTAR, EContactTypes.LINMORTAR, EContactTypes.PGLINMORTAR) and
        pressure_overclosure == EPressureOverclosures.HARD):
        out.append(
            SurfaceBehavior(pressure_overclosure, 
                            c0=kwargs.get('c0'),
                            p0=kwargs.get('p0'),
                            k=kwargs.get('k'),
                            sig_inf=kwargs.get('sig_inf'),
                            table=kwargs.get('table'))
        )

    # Friction
    if pressure_overclosure == EPressureOverclosures.TIED:
        # TIED needs always friction. mue is irrelevant
        lam_tie = lam if lam is not None else kwargs.get('k')
        out.append(
            Friction(mue=0.5, lam=lam_tie)  # type: ignore | this is save, because k is checked in SurfaceBehavior
        )
    else:
        if mue is not None: 
            if lam is None:
                raise ValueError('A value for lam has to be specified if a value for mue is given')
            out.append(Friction(mue, lam))

    # Clearance
    if clearance is not None:
        out.append(Clearance(ind_surf, dep_surf, clearance))

    # Contact Pair
    if contact_type != EContactTypes.NODE_TO_SURFACE: small_sliding = False
    out.append(
        ContactPair(interaction, contact_type, dep_surf, ind_surf, small_sliding, adjust)
    )

    return tuple(out)