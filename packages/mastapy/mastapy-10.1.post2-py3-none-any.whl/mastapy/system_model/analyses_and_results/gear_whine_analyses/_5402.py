'''_5402.py

UnbalancedMassGearWhineAnalysis
'''


from mastapy.system_model.part_model import _2027
from mastapy._internal import constructor
from mastapy.system_model.analyses_and_results.static_loads import _6219
from mastapy.system_model.analyses_and_results.system_deflections import _2348
from mastapy.system_model.analyses_and_results.gear_whine_analyses import _5403
from mastapy._internal.python_net import python_net_import

_UNBALANCED_MASS_GEAR_WHINE_ANALYSIS = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.GearWhineAnalyses', 'UnbalancedMassGearWhineAnalysis')


__docformat__ = 'restructuredtext en'
__all__ = ('UnbalancedMassGearWhineAnalysis',)


class UnbalancedMassGearWhineAnalysis(_5403.VirtualComponentGearWhineAnalysis):
    '''UnbalancedMassGearWhineAnalysis

    This is a mastapy class.
    '''

    TYPE = _UNBALANCED_MASS_GEAR_WHINE_ANALYSIS

    __hash__ = None

    def __init__(self, instance_to_wrap: 'UnbalancedMassGearWhineAnalysis.TYPE'):
        super().__init__(instance_to_wrap)

    @property
    def component_design(self) -> '_2027.UnbalancedMass':
        '''UnbalancedMass: 'ComponentDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_2027.UnbalancedMass)(self.wrapped.ComponentDesign) if self.wrapped.ComponentDesign else None

    @property
    def component_load_case(self) -> '_6219.UnbalancedMassLoadCase':
        '''UnbalancedMassLoadCase: 'ComponentLoadCase' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_6219.UnbalancedMassLoadCase)(self.wrapped.ComponentLoadCase) if self.wrapped.ComponentLoadCase else None

    @property
    def system_deflection_results(self) -> '_2348.UnbalancedMassSystemDeflection':
        '''UnbalancedMassSystemDeflection: 'SystemDeflectionResults' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_2348.UnbalancedMassSystemDeflection)(self.wrapped.SystemDeflectionResults) if self.wrapped.SystemDeflectionResults else None
