﻿'''_4520.py

KlingelnbergCycloPalloidHypoidGearSetModalAnalysisAtASpeed
'''


from typing import List

from mastapy.system_model.part_model.gears import _2077
from mastapy._internal import constructor, conversion
from mastapy.system_model.analyses_and_results.static_loads import _6143
from mastapy.system_model.analyses_and_results.modal_analyses_at_a_speed import _4519, _4518, _4517
from mastapy._internal.python_net import python_net_import

_KLINGELNBERG_CYCLO_PALLOID_HYPOID_GEAR_SET_MODAL_ANALYSIS_AT_A_SPEED = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.ModalAnalysesAtASpeed', 'KlingelnbergCycloPalloidHypoidGearSetModalAnalysisAtASpeed')


__docformat__ = 'restructuredtext en'
__all__ = ('KlingelnbergCycloPalloidHypoidGearSetModalAnalysisAtASpeed',)


class KlingelnbergCycloPalloidHypoidGearSetModalAnalysisAtASpeed(_4517.KlingelnbergCycloPalloidConicalGearSetModalAnalysisAtASpeed):
    '''KlingelnbergCycloPalloidHypoidGearSetModalAnalysisAtASpeed

    This is a mastapy class.
    '''

    TYPE = _KLINGELNBERG_CYCLO_PALLOID_HYPOID_GEAR_SET_MODAL_ANALYSIS_AT_A_SPEED

    __hash__ = None

    def __init__(self, instance_to_wrap: 'KlingelnbergCycloPalloidHypoidGearSetModalAnalysisAtASpeed.TYPE'):
        super().__init__(instance_to_wrap)

    @property
    def assembly_design(self) -> '_2077.KlingelnbergCycloPalloidHypoidGearSet':
        '''KlingelnbergCycloPalloidHypoidGearSet: 'AssemblyDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_2077.KlingelnbergCycloPalloidHypoidGearSet)(self.wrapped.AssemblyDesign) if self.wrapped.AssemblyDesign else None

    @property
    def assembly_load_case(self) -> '_6143.KlingelnbergCycloPalloidHypoidGearSetLoadCase':
        '''KlingelnbergCycloPalloidHypoidGearSetLoadCase: 'AssemblyLoadCase' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_6143.KlingelnbergCycloPalloidHypoidGearSetLoadCase)(self.wrapped.AssemblyLoadCase) if self.wrapped.AssemblyLoadCase else None

    @property
    def klingelnberg_cyclo_palloid_hypoid_gears_modal_analysis_at_a_speed(self) -> 'List[_4519.KlingelnbergCycloPalloidHypoidGearModalAnalysisAtASpeed]':
        '''List[KlingelnbergCycloPalloidHypoidGearModalAnalysisAtASpeed]: 'KlingelnbergCycloPalloidHypoidGearsModalAnalysisAtASpeed' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.KlingelnbergCycloPalloidHypoidGearsModalAnalysisAtASpeed, constructor.new(_4519.KlingelnbergCycloPalloidHypoidGearModalAnalysisAtASpeed))
        return value

    @property
    def klingelnberg_cyclo_palloid_hypoid_meshes_modal_analysis_at_a_speed(self) -> 'List[_4518.KlingelnbergCycloPalloidHypoidGearMeshModalAnalysisAtASpeed]':
        '''List[KlingelnbergCycloPalloidHypoidGearMeshModalAnalysisAtASpeed]: 'KlingelnbergCycloPalloidHypoidMeshesModalAnalysisAtASpeed' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.KlingelnbergCycloPalloidHypoidMeshesModalAnalysisAtASpeed, constructor.new(_4518.KlingelnbergCycloPalloidHypoidGearMeshModalAnalysisAtASpeed))
        return value
