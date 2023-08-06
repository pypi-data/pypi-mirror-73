'''_4099.py

ZerolBevelGearModalAnalysesAtSpeeds
'''


from mastapy.system_model.part_model.gears import _2101
from mastapy._internal import constructor
from mastapy.system_model.analyses_and_results.static_loads import _6224
from mastapy.system_model.analyses_and_results.modal_analyses_at_speeds_ns import _3991
from mastapy._internal.python_net import python_net_import

_ZEROL_BEVEL_GEAR_MODAL_ANALYSES_AT_SPEEDS = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.ModalAnalysesAtSpeedsNS', 'ZerolBevelGearModalAnalysesAtSpeeds')


__docformat__ = 'restructuredtext en'
__all__ = ('ZerolBevelGearModalAnalysesAtSpeeds',)


class ZerolBevelGearModalAnalysesAtSpeeds(_3991.BevelGearModalAnalysesAtSpeeds):
    '''ZerolBevelGearModalAnalysesAtSpeeds

    This is a mastapy class.
    '''

    TYPE = _ZEROL_BEVEL_GEAR_MODAL_ANALYSES_AT_SPEEDS

    __hash__ = None

    def __init__(self, instance_to_wrap: 'ZerolBevelGearModalAnalysesAtSpeeds.TYPE'):
        super().__init__(instance_to_wrap)

    @property
    def component_design(self) -> '_2101.ZerolBevelGear':
        '''ZerolBevelGear: 'ComponentDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_2101.ZerolBevelGear)(self.wrapped.ComponentDesign) if self.wrapped.ComponentDesign else None

    @property
    def component_load_case(self) -> '_6224.ZerolBevelGearLoadCase':
        '''ZerolBevelGearLoadCase: 'ComponentLoadCase' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_6224.ZerolBevelGearLoadCase)(self.wrapped.ComponentLoadCase) if self.wrapped.ComponentLoadCase else None
