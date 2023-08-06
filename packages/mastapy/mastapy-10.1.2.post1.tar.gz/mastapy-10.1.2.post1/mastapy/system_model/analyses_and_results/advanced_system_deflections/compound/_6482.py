'''_6482.py

TorqueConverterCompoundAdvancedSystemDeflection
'''


from typing import List

from mastapy.system_model.part_model.couplings import _2149
from mastapy._internal import constructor, conversion
from mastapy.system_model.analyses_and_results.advanced_system_deflections import _6359
from mastapy.system_model.analyses_and_results.advanced_system_deflections.compound import _6408
from mastapy._internal.python_net import python_net_import

_TORQUE_CONVERTER_COMPOUND_ADVANCED_SYSTEM_DEFLECTION = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.AdvancedSystemDeflections.Compound', 'TorqueConverterCompoundAdvancedSystemDeflection')


__docformat__ = 'restructuredtext en'
__all__ = ('TorqueConverterCompoundAdvancedSystemDeflection',)


class TorqueConverterCompoundAdvancedSystemDeflection(_6408.CouplingCompoundAdvancedSystemDeflection):
    '''TorqueConverterCompoundAdvancedSystemDeflection

    This is a mastapy class.
    '''

    TYPE = _TORQUE_CONVERTER_COMPOUND_ADVANCED_SYSTEM_DEFLECTION

    __hash__ = None

    def __init__(self, instance_to_wrap: 'TorqueConverterCompoundAdvancedSystemDeflection.TYPE'):
        super().__init__(instance_to_wrap)

    @property
    def component_design(self) -> '_2149.TorqueConverter':
        '''TorqueConverter: 'ComponentDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_2149.TorqueConverter)(self.wrapped.ComponentDesign) if self.wrapped.ComponentDesign else None

    @property
    def assembly_design(self) -> '_2149.TorqueConverter':
        '''TorqueConverter: 'AssemblyDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_2149.TorqueConverter)(self.wrapped.AssemblyDesign) if self.wrapped.AssemblyDesign else None

    @property
    def load_case_analyses_ready(self) -> 'List[_6359.TorqueConverterAdvancedSystemDeflection]':
        '''List[TorqueConverterAdvancedSystemDeflection]: 'LoadCaseAnalysesReady' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.LoadCaseAnalysesReady, constructor.new(_6359.TorqueConverterAdvancedSystemDeflection))
        return value

    @property
    def assembly_advanced_system_deflection_load_cases(self) -> 'List[_6359.TorqueConverterAdvancedSystemDeflection]':
        '''List[TorqueConverterAdvancedSystemDeflection]: 'AssemblyAdvancedSystemDeflectionLoadCases' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.AssemblyAdvancedSystemDeflectionLoadCases, constructor.new(_6359.TorqueConverterAdvancedSystemDeflection))
        return value
