'''_3094.py

WormGearSetSteadyStateSynchronousResponse
'''


from typing import List

from mastapy.system_model.part_model.gears import _2100
from mastapy._internal import constructor, conversion
from mastapy.system_model.analyses_and_results.static_loads import _6223
from mastapy.system_model.analyses_and_results.steady_state_synchronous_responses import _3095, _3093, _3027
from mastapy._internal.python_net import python_net_import

_WORM_GEAR_SET_STEADY_STATE_SYNCHRONOUS_RESPONSE = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.SteadyStateSynchronousResponses', 'WormGearSetSteadyStateSynchronousResponse')


__docformat__ = 'restructuredtext en'
__all__ = ('WormGearSetSteadyStateSynchronousResponse',)


class WormGearSetSteadyStateSynchronousResponse(_3027.GearSetSteadyStateSynchronousResponse):
    '''WormGearSetSteadyStateSynchronousResponse

    This is a mastapy class.
    '''

    TYPE = _WORM_GEAR_SET_STEADY_STATE_SYNCHRONOUS_RESPONSE

    __hash__ = None

    def __init__(self, instance_to_wrap: 'WormGearSetSteadyStateSynchronousResponse.TYPE'):
        super().__init__(instance_to_wrap)

    @property
    def assembly_design(self) -> '_2100.WormGearSet':
        '''WormGearSet: 'AssemblyDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_2100.WormGearSet)(self.wrapped.AssemblyDesign) if self.wrapped.AssemblyDesign else None

    @property
    def assembly_load_case(self) -> '_6223.WormGearSetLoadCase':
        '''WormGearSetLoadCase: 'AssemblyLoadCase' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_6223.WormGearSetLoadCase)(self.wrapped.AssemblyLoadCase) if self.wrapped.AssemblyLoadCase else None

    @property
    def worm_gears_steady_state_synchronous_response(self) -> 'List[_3095.WormGearSteadyStateSynchronousResponse]':
        '''List[WormGearSteadyStateSynchronousResponse]: 'WormGearsSteadyStateSynchronousResponse' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.WormGearsSteadyStateSynchronousResponse, constructor.new(_3095.WormGearSteadyStateSynchronousResponse))
        return value

    @property
    def worm_meshes_steady_state_synchronous_response(self) -> 'List[_3093.WormGearMeshSteadyStateSynchronousResponse]':
        '''List[WormGearMeshSteadyStateSynchronousResponse]: 'WormMeshesSteadyStateSynchronousResponse' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.WormMeshesSteadyStateSynchronousResponse, constructor.new(_3093.WormGearMeshSteadyStateSynchronousResponse))
        return value
