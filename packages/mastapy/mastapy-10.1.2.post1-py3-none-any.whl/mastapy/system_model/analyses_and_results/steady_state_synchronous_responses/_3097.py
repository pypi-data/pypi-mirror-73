﻿'''_3097.py

ZerolBevelGearSetSteadyStateSynchronousResponse
'''


from typing import List

from mastapy.system_model.part_model.gears import _2102
from mastapy._internal import constructor, conversion
from mastapy.system_model.analyses_and_results.static_loads import _6226
from mastapy.system_model.analyses_and_results.steady_state_synchronous_responses import _3098, _3096, _2989
from mastapy._internal.python_net import python_net_import

_ZEROL_BEVEL_GEAR_SET_STEADY_STATE_SYNCHRONOUS_RESPONSE = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.SteadyStateSynchronousResponses', 'ZerolBevelGearSetSteadyStateSynchronousResponse')


__docformat__ = 'restructuredtext en'
__all__ = ('ZerolBevelGearSetSteadyStateSynchronousResponse',)


class ZerolBevelGearSetSteadyStateSynchronousResponse(_2989.BevelGearSetSteadyStateSynchronousResponse):
    '''ZerolBevelGearSetSteadyStateSynchronousResponse

    This is a mastapy class.
    '''

    TYPE = _ZEROL_BEVEL_GEAR_SET_STEADY_STATE_SYNCHRONOUS_RESPONSE

    __hash__ = None

    def __init__(self, instance_to_wrap: 'ZerolBevelGearSetSteadyStateSynchronousResponse.TYPE'):
        super().__init__(instance_to_wrap)

    @property
    def assembly_design(self) -> '_2102.ZerolBevelGearSet':
        '''ZerolBevelGearSet: 'AssemblyDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_2102.ZerolBevelGearSet)(self.wrapped.AssemblyDesign) if self.wrapped.AssemblyDesign else None

    @property
    def assembly_load_case(self) -> '_6226.ZerolBevelGearSetLoadCase':
        '''ZerolBevelGearSetLoadCase: 'AssemblyLoadCase' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_6226.ZerolBevelGearSetLoadCase)(self.wrapped.AssemblyLoadCase) if self.wrapped.AssemblyLoadCase else None

    @property
    def zerol_bevel_gears_steady_state_synchronous_response(self) -> 'List[_3098.ZerolBevelGearSteadyStateSynchronousResponse]':
        '''List[ZerolBevelGearSteadyStateSynchronousResponse]: 'ZerolBevelGearsSteadyStateSynchronousResponse' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.ZerolBevelGearsSteadyStateSynchronousResponse, constructor.new(_3098.ZerolBevelGearSteadyStateSynchronousResponse))
        return value

    @property
    def zerol_bevel_meshes_steady_state_synchronous_response(self) -> 'List[_3096.ZerolBevelGearMeshSteadyStateSynchronousResponse]':
        '''List[ZerolBevelGearMeshSteadyStateSynchronousResponse]: 'ZerolBevelMeshesSteadyStateSynchronousResponse' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.ZerolBevelMeshesSteadyStateSynchronousResponse, constructor.new(_3096.ZerolBevelGearMeshSteadyStateSynchronousResponse))
        return value
