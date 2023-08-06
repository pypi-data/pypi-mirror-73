'''_2479.py

UnbalancedMassCompoundSystemDeflection
'''


from typing import List

from mastapy.system_model.part_model import _2027
from mastapy._internal import constructor, conversion
from mastapy.system_model.analyses_and_results.system_deflections import _2348
from mastapy.system_model.analyses_and_results.system_deflections.compound import _2480
from mastapy._internal.python_net import python_net_import

_UNBALANCED_MASS_COMPOUND_SYSTEM_DEFLECTION = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.SystemDeflections.Compound', 'UnbalancedMassCompoundSystemDeflection')


__docformat__ = 'restructuredtext en'
__all__ = ('UnbalancedMassCompoundSystemDeflection',)


class UnbalancedMassCompoundSystemDeflection(_2480.VirtualComponentCompoundSystemDeflection):
    '''UnbalancedMassCompoundSystemDeflection

    This is a mastapy class.
    '''

    TYPE = _UNBALANCED_MASS_COMPOUND_SYSTEM_DEFLECTION

    __hash__ = None

    def __init__(self, instance_to_wrap: 'UnbalancedMassCompoundSystemDeflection.TYPE'):
        super().__init__(instance_to_wrap)

    @property
    def component_design(self) -> '_2027.UnbalancedMass':
        '''UnbalancedMass: 'ComponentDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_2027.UnbalancedMass)(self.wrapped.ComponentDesign) if self.wrapped.ComponentDesign else None

    @property
    def load_case_analyses_ready(self) -> 'List[_2348.UnbalancedMassSystemDeflection]':
        '''List[UnbalancedMassSystemDeflection]: 'LoadCaseAnalysesReady' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.LoadCaseAnalysesReady, constructor.new(_2348.UnbalancedMassSystemDeflection))
        return value

    @property
    def component_system_deflection_load_cases(self) -> 'List[_2348.UnbalancedMassSystemDeflection]':
        '''List[UnbalancedMassSystemDeflection]: 'ComponentSystemDeflectionLoadCases' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.ComponentSystemDeflectionLoadCases, constructor.new(_2348.UnbalancedMassSystemDeflection))
        return value
