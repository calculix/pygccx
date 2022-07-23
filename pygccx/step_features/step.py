from dataclasses import dataclass, field
from typing import Optional
from enums import EStepAmplitudes
from protocols import IStepFeature

@dataclass(frozen=True, slots=True)
class Step:
    """
    Class to define a step
    
    Args:
        nlgeom: Optional. Flag if geometrically nonlinear effects should be taken into account.
                If True, nlgeom is turned on for this and all subsequent steps
                if False, nlgeom is explicitely turned off for this and all subsequent steps
                if None, nlgeom is ommitted for this step and the value from the previous step remains active
        inc: Optional. Max number of increments for this step
        amplitude: Optional. Enum if load should be ramped (default) or stepped within this step
        perturbation: Optional. Flag if the last non-perturbative step should be used as a preload
        desc: Optional. A short description of this step. This is written to the ccx input file.
    """

    nlgeom:Optional[bool] = None
    """Flag if geometrically nonlinear effects should be taken into account"""
    inc:int = 100
    """Max number of increments for this step"""
    amplitude:EStepAmplitudes = EStepAmplitudes.RAMP
    """Enum if load should be ramped or stepped within this step"""
    perturbation:bool = False
    """Flag if the last non-perturbative step should be used as a preload"""
    desc:str = ''
    """A short description of this step. This is written to the ccx input file."""

    step_features:list[IStepFeature] = field(default_factory=list, init=False)

    def __post_init__(self):
        if self.inc < 1:
            raise ValueError(f'inc must be greater than 1, got {self.inc}')

    def add_step_features(self, *step_features:IStepFeature):
        """Adds the given step features to this step"""
        self.step_features.extend(step_features)

    def __str__(self):

        s = '*STEP'
        if self.perturbation: s += ',PERTURBATION'
        if self.nlgeom is not None:
            if self.nlgeom: s += ',NLGEOM'
            else:  s += ',NLGEOM=NO'
        s += f',INC={self.inc}'
        s += f',AMPLITUDE={self.amplitude.value}'
        s += '\n'

        return s