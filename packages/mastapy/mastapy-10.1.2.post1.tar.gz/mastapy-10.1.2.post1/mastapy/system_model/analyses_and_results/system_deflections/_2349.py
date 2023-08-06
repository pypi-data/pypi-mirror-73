'''_2349.py

VirtualComponentSystemDeflection
'''


from mastapy.system_model.part_model import (
    _2028, _2013, _2014, _2021,
    _2022, _2027
)
from mastapy._internal import constructor
from mastapy._internal.cast_exception import CastException
from mastapy.system_model.analyses_and_results.power_flows import (
    _3344, _3296, _3297, _3307,
    _3310, _3343
)
from mastapy.system_model.analyses_and_results.system_deflections import _2299
from mastapy._internal.python_net import python_net_import

_VIRTUAL_COMPONENT_SYSTEM_DEFLECTION = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.SystemDeflections', 'VirtualComponentSystemDeflection')


__docformat__ = 'restructuredtext en'
__all__ = ('VirtualComponentSystemDeflection',)


class VirtualComponentSystemDeflection(_2299.MountableComponentSystemDeflection):
    '''VirtualComponentSystemDeflection

    This is a mastapy class.
    '''

    TYPE = _VIRTUAL_COMPONENT_SYSTEM_DEFLECTION

    __hash__ = None

    def __init__(self, instance_to_wrap: 'VirtualComponentSystemDeflection.TYPE'):
        super().__init__(instance_to_wrap)

    @property
    def component_design(self) -> '_2028.VirtualComponent':
        '''VirtualComponent: 'ComponentDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_2028.VirtualComponent)(self.wrapped.ComponentDesign) if self.wrapped.ComponentDesign else None

    @property
    def component_design_of_type_mass_disc(self) -> '_2013.MassDisc':
        '''MassDisc: 'ComponentDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _2013.MassDisc.TYPE not in self.wrapped.ComponentDesign.__class__.__mro__:
            raise CastException('Failed to cast component_design to MassDisc. Expected: {}.'.format(self.wrapped.ComponentDesign.__class__.__qualname__))

        return constructor.new(_2013.MassDisc)(self.wrapped.ComponentDesign) if self.wrapped.ComponentDesign else None

    @property
    def component_design_of_type_measurement_component(self) -> '_2014.MeasurementComponent':
        '''MeasurementComponent: 'ComponentDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _2014.MeasurementComponent.TYPE not in self.wrapped.ComponentDesign.__class__.__mro__:
            raise CastException('Failed to cast component_design to MeasurementComponent. Expected: {}.'.format(self.wrapped.ComponentDesign.__class__.__qualname__))

        return constructor.new(_2014.MeasurementComponent)(self.wrapped.ComponentDesign) if self.wrapped.ComponentDesign else None

    @property
    def component_design_of_type_point_load(self) -> '_2021.PointLoad':
        '''PointLoad: 'ComponentDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _2021.PointLoad.TYPE not in self.wrapped.ComponentDesign.__class__.__mro__:
            raise CastException('Failed to cast component_design to PointLoad. Expected: {}.'.format(self.wrapped.ComponentDesign.__class__.__qualname__))

        return constructor.new(_2021.PointLoad)(self.wrapped.ComponentDesign) if self.wrapped.ComponentDesign else None

    @property
    def component_design_of_type_power_load(self) -> '_2022.PowerLoad':
        '''PowerLoad: 'ComponentDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _2022.PowerLoad.TYPE not in self.wrapped.ComponentDesign.__class__.__mro__:
            raise CastException('Failed to cast component_design to PowerLoad. Expected: {}.'.format(self.wrapped.ComponentDesign.__class__.__qualname__))

        return constructor.new(_2022.PowerLoad)(self.wrapped.ComponentDesign) if self.wrapped.ComponentDesign else None

    @property
    def component_design_of_type_unbalanced_mass(self) -> '_2027.UnbalancedMass':
        '''UnbalancedMass: 'ComponentDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _2027.UnbalancedMass.TYPE not in self.wrapped.ComponentDesign.__class__.__mro__:
            raise CastException('Failed to cast component_design to UnbalancedMass. Expected: {}.'.format(self.wrapped.ComponentDesign.__class__.__qualname__))

        return constructor.new(_2027.UnbalancedMass)(self.wrapped.ComponentDesign) if self.wrapped.ComponentDesign else None

    @property
    def power_flow_results(self) -> '_3344.VirtualComponentPowerFlow':
        '''VirtualComponentPowerFlow: 'PowerFlowResults' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_3344.VirtualComponentPowerFlow)(self.wrapped.PowerFlowResults) if self.wrapped.PowerFlowResults else None

    @property
    def power_flow_results_of_type_mass_disc_power_flow(self) -> '_3296.MassDiscPowerFlow':
        '''MassDiscPowerFlow: 'PowerFlowResults' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _3296.MassDiscPowerFlow.TYPE not in self.wrapped.PowerFlowResults.__class__.__mro__:
            raise CastException('Failed to cast power_flow_results to MassDiscPowerFlow. Expected: {}.'.format(self.wrapped.PowerFlowResults.__class__.__qualname__))

        return constructor.new(_3296.MassDiscPowerFlow)(self.wrapped.PowerFlowResults) if self.wrapped.PowerFlowResults else None

    @property
    def power_flow_results_of_type_measurement_component_power_flow(self) -> '_3297.MeasurementComponentPowerFlow':
        '''MeasurementComponentPowerFlow: 'PowerFlowResults' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _3297.MeasurementComponentPowerFlow.TYPE not in self.wrapped.PowerFlowResults.__class__.__mro__:
            raise CastException('Failed to cast power_flow_results to MeasurementComponentPowerFlow. Expected: {}.'.format(self.wrapped.PowerFlowResults.__class__.__qualname__))

        return constructor.new(_3297.MeasurementComponentPowerFlow)(self.wrapped.PowerFlowResults) if self.wrapped.PowerFlowResults else None

    @property
    def power_flow_results_of_type_point_load_power_flow(self) -> '_3307.PointLoadPowerFlow':
        '''PointLoadPowerFlow: 'PowerFlowResults' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _3307.PointLoadPowerFlow.TYPE not in self.wrapped.PowerFlowResults.__class__.__mro__:
            raise CastException('Failed to cast power_flow_results to PointLoadPowerFlow. Expected: {}.'.format(self.wrapped.PowerFlowResults.__class__.__qualname__))

        return constructor.new(_3307.PointLoadPowerFlow)(self.wrapped.PowerFlowResults) if self.wrapped.PowerFlowResults else None

    @property
    def power_flow_results_of_type_power_load_power_flow(self) -> '_3310.PowerLoadPowerFlow':
        '''PowerLoadPowerFlow: 'PowerFlowResults' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _3310.PowerLoadPowerFlow.TYPE not in self.wrapped.PowerFlowResults.__class__.__mro__:
            raise CastException('Failed to cast power_flow_results to PowerLoadPowerFlow. Expected: {}.'.format(self.wrapped.PowerFlowResults.__class__.__qualname__))

        return constructor.new(_3310.PowerLoadPowerFlow)(self.wrapped.PowerFlowResults) if self.wrapped.PowerFlowResults else None

    @property
    def power_flow_results_of_type_unbalanced_mass_power_flow(self) -> '_3343.UnbalancedMassPowerFlow':
        '''UnbalancedMassPowerFlow: 'PowerFlowResults' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _3343.UnbalancedMassPowerFlow.TYPE not in self.wrapped.PowerFlowResults.__class__.__mro__:
            raise CastException('Failed to cast power_flow_results to UnbalancedMassPowerFlow. Expected: {}.'.format(self.wrapped.PowerFlowResults.__class__.__qualname__))

        return constructor.new(_3343.UnbalancedMassPowerFlow)(self.wrapped.PowerFlowResults) if self.wrapped.PowerFlowResults else None
