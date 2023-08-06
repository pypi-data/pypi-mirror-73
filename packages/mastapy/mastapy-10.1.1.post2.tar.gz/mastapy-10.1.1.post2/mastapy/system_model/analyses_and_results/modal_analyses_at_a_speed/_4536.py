﻿'''_4536.py

PlanetCarrierModalAnalysisAtASpeed
'''


from mastapy.system_model.part_model import _2010
from mastapy._internal import constructor
from mastapy.system_model.analyses_and_results.static_loads import _6162
from mastapy.system_model.analyses_and_results.modal_analyses_at_a_speed import _4528
from mastapy._internal.python_net import python_net_import

_PLANET_CARRIER_MODAL_ANALYSIS_AT_A_SPEED = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.ModalAnalysesAtASpeed', 'PlanetCarrierModalAnalysisAtASpeed')


__docformat__ = 'restructuredtext en'
__all__ = ('PlanetCarrierModalAnalysisAtASpeed',)


class PlanetCarrierModalAnalysisAtASpeed(_4528.MountableComponentModalAnalysisAtASpeed):
    '''PlanetCarrierModalAnalysisAtASpeed

    This is a mastapy class.
    '''

    TYPE = _PLANET_CARRIER_MODAL_ANALYSIS_AT_A_SPEED

    __hash__ = None

    def __init__(self, instance_to_wrap: 'PlanetCarrierModalAnalysisAtASpeed.TYPE'):
        super().__init__(instance_to_wrap)

    @property
    def component_design(self) -> '_2010.PlanetCarrier':
        '''PlanetCarrier: 'ComponentDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_2010.PlanetCarrier)(self.wrapped.ComponentDesign) if self.wrapped.ComponentDesign else None

    @property
    def component_load_case(self) -> '_6162.PlanetCarrierLoadCase':
        '''PlanetCarrierLoadCase: 'ComponentLoadCase' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_6162.PlanetCarrierLoadCase)(self.wrapped.ComponentLoadCase) if self.wrapped.ComponentLoadCase else None
