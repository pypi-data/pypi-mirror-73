﻿'''_5926.py

WormGearSetDynamicAnalysis
'''


from typing import List

from mastapy.system_model.part_model.gears import _2100
from mastapy._internal import constructor, conversion
from mastapy.system_model.analyses_and_results.static_loads import _6223
from mastapy.system_model.analyses_and_results.dynamic_analyses import _5924, _5925, _5862
from mastapy._internal.python_net import python_net_import

_WORM_GEAR_SET_DYNAMIC_ANALYSIS = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.DynamicAnalyses', 'WormGearSetDynamicAnalysis')


__docformat__ = 'restructuredtext en'
__all__ = ('WormGearSetDynamicAnalysis',)


class WormGearSetDynamicAnalysis(_5862.GearSetDynamicAnalysis):
    '''WormGearSetDynamicAnalysis

    This is a mastapy class.
    '''

    TYPE = _WORM_GEAR_SET_DYNAMIC_ANALYSIS

    __hash__ = None

    def __init__(self, instance_to_wrap: 'WormGearSetDynamicAnalysis.TYPE'):
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
    def worm_gears_dynamic_analysis(self) -> 'List[_5924.WormGearDynamicAnalysis]':
        '''List[WormGearDynamicAnalysis]: 'WormGearsDynamicAnalysis' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.WormGearsDynamicAnalysis, constructor.new(_5924.WormGearDynamicAnalysis))
        return value

    @property
    def worm_meshes_dynamic_analysis(self) -> 'List[_5925.WormGearMeshDynamicAnalysis]':
        '''List[WormGearMeshDynamicAnalysis]: 'WormMeshesDynamicAnalysis' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.WormMeshesDynamicAnalysis, constructor.new(_5925.WormGearMeshDynamicAnalysis))
        return value
