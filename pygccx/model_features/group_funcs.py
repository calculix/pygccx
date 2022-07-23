from typing import Optional

from . import ContactPair, SurfaceInteraction, SurfaceBehavior, Friction, Clearance
from enums import EContactTypes, EPressureOverclosures
from protocols import ISet, ISurface, IModelFeature

number = int|float

def make_contact(name:str, contact_type:EContactTypes, dep_surf:ISurface, ind_surf:ISurface,
                pressure_overclosure:EPressureOverclosures, small_sliding:bool=False,              
                adjust:Optional[number|ISet]=None, clearance:Optional[number]=None, desc:str='', **kwargs) -> tuple[IModelFeature]:

    out:list[IModelFeature] = []

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
        out.append(
            Friction(mue=0.5, lam=kwargs.get('k'))  # type: ignore | this is save, because k is checked in SurfaceBehavior
        )
    else:
        mue:number|None = kwargs.get('mue')
        lam:number|None = kwargs.get('lam')
        if mue is not None: 
            if lam is None:
                raise ValueError('A value for lam has to be specified if a value for mue is given')
            out.append(Friction(mue, lam))

    # Clearance
    if clearance is not None:
        out.append(Clearance(ind_surf, dep_surf, clearance))

    # Contact Pair
    out.append(
        ContactPair(interaction, contact_type, dep_surf, ind_surf, small_sliding, adjust)
    )

    return tuple(out)