'''_3089.py

TorqueConverterSteadyStateSynchronousResponse
'''


from mastapy.system_model.part_model.couplings import _2149
from mastapy._internal import constructor
from mastapy.system_model.analyses_and_results.static_loads import _6212
from mastapy.system_model.analyses_and_results.steady_state_synchronous_responses import _3011
from mastapy._internal.python_net import python_net_import

_TORQUE_CONVERTER_STEADY_STATE_SYNCHRONOUS_RESPONSE = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.SteadyStateSynchronousResponses', 'TorqueConverterSteadyStateSynchronousResponse')


__docformat__ = 'restructuredtext en'
__all__ = ('TorqueConverterSteadyStateSynchronousResponse',)


class TorqueConverterSteadyStateSynchronousResponse(_3011.CouplingSteadyStateSynchronousResponse):
    '''TorqueConverterSteadyStateSynchronousResponse

    This is a mastapy class.
    '''

    TYPE = _TORQUE_CONVERTER_STEADY_STATE_SYNCHRONOUS_RESPONSE

    __hash__ = None

    def __init__(self, instance_to_wrap: 'TorqueConverterSteadyStateSynchronousResponse.TYPE'):
        super().__init__(instance_to_wrap)

    @property
    def assembly_design(self) -> '_2149.TorqueConverter':
        '''TorqueConverter: 'AssemblyDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_2149.TorqueConverter)(self.wrapped.AssemblyDesign) if self.wrapped.AssemblyDesign else None

    @property
    def assembly_load_case(self) -> '_6212.TorqueConverterLoadCase':
        '''TorqueConverterLoadCase: 'AssemblyLoadCase' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_6212.TorqueConverterLoadCase)(self.wrapped.AssemblyLoadCase) if self.wrapped.AssemblyLoadCase else None
