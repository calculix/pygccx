from dataclasses import dataclass

@dataclass(frozen=True, slots=True)
class SurfaceInteraction:

    """
    Class to define the start of a surface interaction

    Args:
        name: Name of this surface interaction up to 80 characters
        desc: Optional. A short description of this instance. This is written to 
                the ccx input file.
    """
    name:str
    desc:str = ''

    def __post_init__(self):
        if len(self.name) > 80:
            raise ValueError(f'name can only contain up to 80 characters, got {len(self.name)}')


    def __str__(self):
        return f'*SURFACE INTERACTION,NAME={self.name}\n'