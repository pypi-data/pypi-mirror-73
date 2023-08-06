'''_5534.py

TorqueConverterTurbineSingleMeshWhineAnalysis
'''


from mastapy.system_model.part_model.couplings import _2152
from mastapy._internal import constructor
from mastapy.system_model.analyses_and_results.static_loads import _6214
from mastapy.system_model.analyses_and_results.gear_whine_analyses.single_mesh_whine_analyses import _5456
from mastapy._internal.python_net import python_net_import

_TORQUE_CONVERTER_TURBINE_SINGLE_MESH_WHINE_ANALYSIS = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.GearWhineAnalyses.SingleMeshWhineAnalyses', 'TorqueConverterTurbineSingleMeshWhineAnalysis')


__docformat__ = 'restructuredtext en'
__all__ = ('TorqueConverterTurbineSingleMeshWhineAnalysis',)


class TorqueConverterTurbineSingleMeshWhineAnalysis(_5456.CouplingHalfSingleMeshWhineAnalysis):
    '''TorqueConverterTurbineSingleMeshWhineAnalysis

    This is a mastapy class.
    '''

    TYPE = _TORQUE_CONVERTER_TURBINE_SINGLE_MESH_WHINE_ANALYSIS

    __hash__ = None

    def __init__(self, instance_to_wrap: 'TorqueConverterTurbineSingleMeshWhineAnalysis.TYPE'):
        super().__init__(instance_to_wrap)

    @property
    def component_design(self) -> '_2152.TorqueConverterTurbine':
        '''TorqueConverterTurbine: 'ComponentDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_2152.TorqueConverterTurbine)(self.wrapped.ComponentDesign) if self.wrapped.ComponentDesign else None

    @property
    def component_load_case(self) -> '_6214.TorqueConverterTurbineLoadCase':
        '''TorqueConverterTurbineLoadCase: 'ComponentLoadCase' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_6214.TorqueConverterTurbineLoadCase)(self.wrapped.ComponentLoadCase) if self.wrapped.ComponentLoadCase else None
