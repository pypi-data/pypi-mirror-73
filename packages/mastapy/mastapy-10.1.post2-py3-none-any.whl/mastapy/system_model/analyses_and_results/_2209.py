'''_2209.py

CompoundPowerFlowAnalysis
'''


from typing import Iterable

from mastapy.system_model.part_model import (
    _1990, _1991, _1994, _1996,
    _1997, _1998, _2001, _2002,
    _2005, _2006, _1989, _2007,
    _2010, _2013, _2014, _2015,
    _2017, _2018, _2019, _2021,
    _2022, _2024, _2026, _2027,
    _2028
)
from mastapy.system_model.analyses_and_results.power_flows.compound import (
    _3351, _3352, _3357, _3368,
    _3369, _3375, _3386, _3397,
    _3398, _3402, _3356, _3406,
    _3410, _3421, _3422, _3423,
    _3424, _3425, _3431, _3432,
    _3433, _3438, _3442, _3465,
    _3466, _3439, _3379, _3381,
    _3399, _3401, _3353, _3355,
    _3360, _3362, _3363, _3364,
    _3365, _3367, _3382, _3384,
    _3393, _3395, _3396, _3403,
    _3405, _3407, _3409, _3412,
    _3414, _3415, _3417, _3418,
    _3420, _3430, _3443, _3445,
    _3449, _3451, _3452, _3454,
    _3455, _3456, _3467, _3469,
    _3470, _3472, _3426, _3428,
    _3359, _3371, _3373, _3376,
    _3378, _3387, _3389, _3391,
    _3392, _3434, _3440, _3436,
    _3435, _3446, _3448, _3457,
    _3458, _3459, _3460, _3461,
    _3463, _3464, _3390, _3358,
    _3374, _3385, _3411, _3429,
    _3437, _3441, _3361, _3380,
    _3400, _3450, _3366, _3383,
    _3354, _3394, _3408, _3413,
    _3416, _3419, _3444, _3453,
    _3468, _3471, _3404, _3427,
    _3372, _3377, _3388, _3447,
    _3462
)
from mastapy._internal import constructor, conversion
from mastapy.system_model.part_model.shaft_model import _2031
from mastapy.system_model.part_model.gears import (
    _2069, _2070, _2076, _2077,
    _2061, _2062, _2063, _2064,
    _2065, _2066, _2067, _2068,
    _2071, _2072, _2073, _2074,
    _2075, _2078, _2080, _2082,
    _2083, _2084, _2085, _2086,
    _2087, _2088, _2089, _2090,
    _2091, _2092, _2093, _2094,
    _2095, _2096, _2097, _2098,
    _2099, _2100, _2101, _2102
)
from mastapy.system_model.part_model.couplings import (
    _2131, _2132, _2120, _2122,
    _2123, _2125, _2126, _2127,
    _2128, _2129, _2130, _2133,
    _2141, _2139, _2140, _2142,
    _2143, _2144, _2146, _2147,
    _2148, _2149, _2150, _2152
)
from mastapy.system_model.connections_and_sockets import (
    _1846, _1841, _1842, _1845,
    _1854, _1857, _1861, _1865
)
from mastapy.system_model.connections_and_sockets.gears import (
    _1871, _1875, _1881, _1895,
    _1873, _1877, _1869, _1879,
    _1885, _1888, _1889, _1890,
    _1893, _1897, _1899, _1901,
    _1883
)
from mastapy.system_model.connections_and_sockets.couplings import (
    _1909, _1903, _1905, _1907,
    _1911, _1913
)
from mastapy.system_model.analyses_and_results import _2161
from mastapy._internal.python_net import python_net_import

_COMPOUND_POWER_FLOW_ANALYSIS = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults', 'CompoundPowerFlowAnalysis')


__docformat__ = 'restructuredtext en'
__all__ = ('CompoundPowerFlowAnalysis',)


class CompoundPowerFlowAnalysis(_2161.CompoundAnalysis):
    '''CompoundPowerFlowAnalysis

    This is a mastapy class.
    '''

    TYPE = _COMPOUND_POWER_FLOW_ANALYSIS

    __hash__ = None

    def __init__(self, instance_to_wrap: 'CompoundPowerFlowAnalysis.TYPE'):
        super().__init__(instance_to_wrap)

    def results_for_abstract_assembly(self, design_entity: '_1990.AbstractAssembly') -> 'Iterable[_3351.AbstractAssemblyCompoundPowerFlow]':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.AbstractAssembly)

        Returns:
            Iterable[mastapy.system_model.analyses_and_results.power_flows.compound.AbstractAssemblyCompoundPowerFlow]
        '''

        return conversion.pn_to_mp_objects_in_iterable(self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None), constructor.new(_3351.AbstractAssemblyCompoundPowerFlow))

    def results_for_abstract_shaft_or_housing(self, design_entity: '_1991.AbstractShaftOrHousing') -> 'Iterable[_3352.AbstractShaftOrHousingCompoundPowerFlow]':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.AbstractShaftOrHousing)

        Returns:
            Iterable[mastapy.system_model.analyses_and_results.power_flows.compound.AbstractShaftOrHousingCompoundPowerFlow]
        '''

        return conversion.pn_to_mp_objects_in_iterable(self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None), constructor.new(_3352.AbstractShaftOrHousingCompoundPowerFlow))

    def results_for_bearing(self, design_entity: '_1994.Bearing') -> 'Iterable[_3357.BearingCompoundPowerFlow]':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.Bearing)

        Returns:
            Iterable[mastapy.system_model.analyses_and_results.power_flows.compound.BearingCompoundPowerFlow]
        '''

        return conversion.pn_to_mp_objects_in_iterable(self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None), constructor.new(_3357.BearingCompoundPowerFlow))

    def results_for_bolt(self, design_entity: '_1996.Bolt') -> 'Iterable[_3368.BoltCompoundPowerFlow]':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.Bolt)

        Returns:
            Iterable[mastapy.system_model.analyses_and_results.power_flows.compound.BoltCompoundPowerFlow]
        '''

        return conversion.pn_to_mp_objects_in_iterable(self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None), constructor.new(_3368.BoltCompoundPowerFlow))

    def results_for_bolted_joint(self, design_entity: '_1997.BoltedJoint') -> 'Iterable[_3369.BoltedJointCompoundPowerFlow]':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.BoltedJoint)

        Returns:
            Iterable[mastapy.system_model.analyses_and_results.power_flows.compound.BoltedJointCompoundPowerFlow]
        '''

        return conversion.pn_to_mp_objects_in_iterable(self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None), constructor.new(_3369.BoltedJointCompoundPowerFlow))

    def results_for_component(self, design_entity: '_1998.Component') -> 'Iterable[_3375.ComponentCompoundPowerFlow]':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.Component)

        Returns:
            Iterable[mastapy.system_model.analyses_and_results.power_flows.compound.ComponentCompoundPowerFlow]
        '''

        return conversion.pn_to_mp_objects_in_iterable(self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None), constructor.new(_3375.ComponentCompoundPowerFlow))

    def results_for_connector(self, design_entity: '_2001.Connector') -> 'Iterable[_3386.ConnectorCompoundPowerFlow]':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.Connector)

        Returns:
            Iterable[mastapy.system_model.analyses_and_results.power_flows.compound.ConnectorCompoundPowerFlow]
        '''

        return conversion.pn_to_mp_objects_in_iterable(self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None), constructor.new(_3386.ConnectorCompoundPowerFlow))

    def results_for_datum(self, design_entity: '_2002.Datum') -> 'Iterable[_3397.DatumCompoundPowerFlow]':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.Datum)

        Returns:
            Iterable[mastapy.system_model.analyses_and_results.power_flows.compound.DatumCompoundPowerFlow]
        '''

        return conversion.pn_to_mp_objects_in_iterable(self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None), constructor.new(_3397.DatumCompoundPowerFlow))

    def results_for_external_cad_model(self, design_entity: '_2005.ExternalCADModel') -> 'Iterable[_3398.ExternalCADModelCompoundPowerFlow]':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.ExternalCADModel)

        Returns:
            Iterable[mastapy.system_model.analyses_and_results.power_flows.compound.ExternalCADModelCompoundPowerFlow]
        '''

        return conversion.pn_to_mp_objects_in_iterable(self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None), constructor.new(_3398.ExternalCADModelCompoundPowerFlow))

    def results_for_flexible_pin_assembly(self, design_entity: '_2006.FlexiblePinAssembly') -> 'Iterable[_3402.FlexiblePinAssemblyCompoundPowerFlow]':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.FlexiblePinAssembly)

        Returns:
            Iterable[mastapy.system_model.analyses_and_results.power_flows.compound.FlexiblePinAssemblyCompoundPowerFlow]
        '''

        return conversion.pn_to_mp_objects_in_iterable(self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None), constructor.new(_3402.FlexiblePinAssemblyCompoundPowerFlow))

    def results_for_assembly(self, design_entity: '_1989.Assembly') -> 'Iterable[_3356.AssemblyCompoundPowerFlow]':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.Assembly)

        Returns:
            Iterable[mastapy.system_model.analyses_and_results.power_flows.compound.AssemblyCompoundPowerFlow]
        '''

        return conversion.pn_to_mp_objects_in_iterable(self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None), constructor.new(_3356.AssemblyCompoundPowerFlow))

    def results_for_guide_dxf_model(self, design_entity: '_2007.GuideDxfModel') -> 'Iterable[_3406.GuideDxfModelCompoundPowerFlow]':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.GuideDxfModel)

        Returns:
            Iterable[mastapy.system_model.analyses_and_results.power_flows.compound.GuideDxfModelCompoundPowerFlow]
        '''

        return conversion.pn_to_mp_objects_in_iterable(self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None), constructor.new(_3406.GuideDxfModelCompoundPowerFlow))

    def results_for_imported_fe_component(self, design_entity: '_2010.ImportedFEComponent') -> 'Iterable[_3410.ImportedFEComponentCompoundPowerFlow]':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.ImportedFEComponent)

        Returns:
            Iterable[mastapy.system_model.analyses_and_results.power_flows.compound.ImportedFEComponentCompoundPowerFlow]
        '''

        return conversion.pn_to_mp_objects_in_iterable(self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None), constructor.new(_3410.ImportedFEComponentCompoundPowerFlow))

    def results_for_mass_disc(self, design_entity: '_2013.MassDisc') -> 'Iterable[_3421.MassDiscCompoundPowerFlow]':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.MassDisc)

        Returns:
            Iterable[mastapy.system_model.analyses_and_results.power_flows.compound.MassDiscCompoundPowerFlow]
        '''

        return conversion.pn_to_mp_objects_in_iterable(self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None), constructor.new(_3421.MassDiscCompoundPowerFlow))

    def results_for_measurement_component(self, design_entity: '_2014.MeasurementComponent') -> 'Iterable[_3422.MeasurementComponentCompoundPowerFlow]':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.MeasurementComponent)

        Returns:
            Iterable[mastapy.system_model.analyses_and_results.power_flows.compound.MeasurementComponentCompoundPowerFlow]
        '''

        return conversion.pn_to_mp_objects_in_iterable(self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None), constructor.new(_3422.MeasurementComponentCompoundPowerFlow))

    def results_for_mountable_component(self, design_entity: '_2015.MountableComponent') -> 'Iterable[_3423.MountableComponentCompoundPowerFlow]':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.MountableComponent)

        Returns:
            Iterable[mastapy.system_model.analyses_and_results.power_flows.compound.MountableComponentCompoundPowerFlow]
        '''

        return conversion.pn_to_mp_objects_in_iterable(self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None), constructor.new(_3423.MountableComponentCompoundPowerFlow))

    def results_for_oil_seal(self, design_entity: '_2017.OilSeal') -> 'Iterable[_3424.OilSealCompoundPowerFlow]':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.OilSeal)

        Returns:
            Iterable[mastapy.system_model.analyses_and_results.power_flows.compound.OilSealCompoundPowerFlow]
        '''

        return conversion.pn_to_mp_objects_in_iterable(self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None), constructor.new(_3424.OilSealCompoundPowerFlow))

    def results_for_part(self, design_entity: '_2018.Part') -> 'Iterable[_3425.PartCompoundPowerFlow]':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.Part)

        Returns:
            Iterable[mastapy.system_model.analyses_and_results.power_flows.compound.PartCompoundPowerFlow]
        '''

        return conversion.pn_to_mp_objects_in_iterable(self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None), constructor.new(_3425.PartCompoundPowerFlow))

    def results_for_planet_carrier(self, design_entity: '_2019.PlanetCarrier') -> 'Iterable[_3431.PlanetCarrierCompoundPowerFlow]':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.PlanetCarrier)

        Returns:
            Iterable[mastapy.system_model.analyses_and_results.power_flows.compound.PlanetCarrierCompoundPowerFlow]
        '''

        return conversion.pn_to_mp_objects_in_iterable(self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None), constructor.new(_3431.PlanetCarrierCompoundPowerFlow))

    def results_for_point_load(self, design_entity: '_2021.PointLoad') -> 'Iterable[_3432.PointLoadCompoundPowerFlow]':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.PointLoad)

        Returns:
            Iterable[mastapy.system_model.analyses_and_results.power_flows.compound.PointLoadCompoundPowerFlow]
        '''

        return conversion.pn_to_mp_objects_in_iterable(self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None), constructor.new(_3432.PointLoadCompoundPowerFlow))

    def results_for_power_load(self, design_entity: '_2022.PowerLoad') -> 'Iterable[_3433.PowerLoadCompoundPowerFlow]':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.PowerLoad)

        Returns:
            Iterable[mastapy.system_model.analyses_and_results.power_flows.compound.PowerLoadCompoundPowerFlow]
        '''

        return conversion.pn_to_mp_objects_in_iterable(self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None), constructor.new(_3433.PowerLoadCompoundPowerFlow))

    def results_for_root_assembly(self, design_entity: '_2024.RootAssembly') -> 'Iterable[_3438.RootAssemblyCompoundPowerFlow]':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.RootAssembly)

        Returns:
            Iterable[mastapy.system_model.analyses_and_results.power_flows.compound.RootAssemblyCompoundPowerFlow]
        '''

        return conversion.pn_to_mp_objects_in_iterable(self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None), constructor.new(_3438.RootAssemblyCompoundPowerFlow))

    def results_for_specialised_assembly(self, design_entity: '_2026.SpecialisedAssembly') -> 'Iterable[_3442.SpecialisedAssemblyCompoundPowerFlow]':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.SpecialisedAssembly)

        Returns:
            Iterable[mastapy.system_model.analyses_and_results.power_flows.compound.SpecialisedAssemblyCompoundPowerFlow]
        '''

        return conversion.pn_to_mp_objects_in_iterable(self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None), constructor.new(_3442.SpecialisedAssemblyCompoundPowerFlow))

    def results_for_unbalanced_mass(self, design_entity: '_2027.UnbalancedMass') -> 'Iterable[_3465.UnbalancedMassCompoundPowerFlow]':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.UnbalancedMass)

        Returns:
            Iterable[mastapy.system_model.analyses_and_results.power_flows.compound.UnbalancedMassCompoundPowerFlow]
        '''

        return conversion.pn_to_mp_objects_in_iterable(self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None), constructor.new(_3465.UnbalancedMassCompoundPowerFlow))

    def results_for_virtual_component(self, design_entity: '_2028.VirtualComponent') -> 'Iterable[_3466.VirtualComponentCompoundPowerFlow]':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.VirtualComponent)

        Returns:
            Iterable[mastapy.system_model.analyses_and_results.power_flows.compound.VirtualComponentCompoundPowerFlow]
        '''

        return conversion.pn_to_mp_objects_in_iterable(self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None), constructor.new(_3466.VirtualComponentCompoundPowerFlow))

    def results_for_shaft(self, design_entity: '_2031.Shaft') -> 'Iterable[_3439.ShaftCompoundPowerFlow]':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.shaft_model.Shaft)

        Returns:
            Iterable[mastapy.system_model.analyses_and_results.power_flows.compound.ShaftCompoundPowerFlow]
        '''

        return conversion.pn_to_mp_objects_in_iterable(self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None), constructor.new(_3439.ShaftCompoundPowerFlow))

    def results_for_concept_gear(self, design_entity: '_2069.ConceptGear') -> 'Iterable[_3379.ConceptGearCompoundPowerFlow]':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.gears.ConceptGear)

        Returns:
            Iterable[mastapy.system_model.analyses_and_results.power_flows.compound.ConceptGearCompoundPowerFlow]
        '''

        return conversion.pn_to_mp_objects_in_iterable(self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None), constructor.new(_3379.ConceptGearCompoundPowerFlow))

    def results_for_concept_gear_set(self, design_entity: '_2070.ConceptGearSet') -> 'Iterable[_3381.ConceptGearSetCompoundPowerFlow]':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.gears.ConceptGearSet)

        Returns:
            Iterable[mastapy.system_model.analyses_and_results.power_flows.compound.ConceptGearSetCompoundPowerFlow]
        '''

        return conversion.pn_to_mp_objects_in_iterable(self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None), constructor.new(_3381.ConceptGearSetCompoundPowerFlow))

    def results_for_face_gear(self, design_entity: '_2076.FaceGear') -> 'Iterable[_3399.FaceGearCompoundPowerFlow]':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.gears.FaceGear)

        Returns:
            Iterable[mastapy.system_model.analyses_and_results.power_flows.compound.FaceGearCompoundPowerFlow]
        '''

        return conversion.pn_to_mp_objects_in_iterable(self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None), constructor.new(_3399.FaceGearCompoundPowerFlow))

    def results_for_face_gear_set(self, design_entity: '_2077.FaceGearSet') -> 'Iterable[_3401.FaceGearSetCompoundPowerFlow]':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.gears.FaceGearSet)

        Returns:
            Iterable[mastapy.system_model.analyses_and_results.power_flows.compound.FaceGearSetCompoundPowerFlow]
        '''

        return conversion.pn_to_mp_objects_in_iterable(self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None), constructor.new(_3401.FaceGearSetCompoundPowerFlow))

    def results_for_agma_gleason_conical_gear(self, design_entity: '_2061.AGMAGleasonConicalGear') -> 'Iterable[_3353.AGMAGleasonConicalGearCompoundPowerFlow]':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.gears.AGMAGleasonConicalGear)

        Returns:
            Iterable[mastapy.system_model.analyses_and_results.power_flows.compound.AGMAGleasonConicalGearCompoundPowerFlow]
        '''

        return conversion.pn_to_mp_objects_in_iterable(self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None), constructor.new(_3353.AGMAGleasonConicalGearCompoundPowerFlow))

    def results_for_agma_gleason_conical_gear_set(self, design_entity: '_2062.AGMAGleasonConicalGearSet') -> 'Iterable[_3355.AGMAGleasonConicalGearSetCompoundPowerFlow]':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.gears.AGMAGleasonConicalGearSet)

        Returns:
            Iterable[mastapy.system_model.analyses_and_results.power_flows.compound.AGMAGleasonConicalGearSetCompoundPowerFlow]
        '''

        return conversion.pn_to_mp_objects_in_iterable(self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None), constructor.new(_3355.AGMAGleasonConicalGearSetCompoundPowerFlow))

    def results_for_bevel_differential_gear(self, design_entity: '_2063.BevelDifferentialGear') -> 'Iterable[_3360.BevelDifferentialGearCompoundPowerFlow]':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.gears.BevelDifferentialGear)

        Returns:
            Iterable[mastapy.system_model.analyses_and_results.power_flows.compound.BevelDifferentialGearCompoundPowerFlow]
        '''

        return conversion.pn_to_mp_objects_in_iterable(self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None), constructor.new(_3360.BevelDifferentialGearCompoundPowerFlow))

    def results_for_bevel_differential_gear_set(self, design_entity: '_2064.BevelDifferentialGearSet') -> 'Iterable[_3362.BevelDifferentialGearSetCompoundPowerFlow]':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.gears.BevelDifferentialGearSet)

        Returns:
            Iterable[mastapy.system_model.analyses_and_results.power_flows.compound.BevelDifferentialGearSetCompoundPowerFlow]
        '''

        return conversion.pn_to_mp_objects_in_iterable(self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None), constructor.new(_3362.BevelDifferentialGearSetCompoundPowerFlow))

    def results_for_bevel_differential_planet_gear(self, design_entity: '_2065.BevelDifferentialPlanetGear') -> 'Iterable[_3363.BevelDifferentialPlanetGearCompoundPowerFlow]':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.gears.BevelDifferentialPlanetGear)

        Returns:
            Iterable[mastapy.system_model.analyses_and_results.power_flows.compound.BevelDifferentialPlanetGearCompoundPowerFlow]
        '''

        return conversion.pn_to_mp_objects_in_iterable(self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None), constructor.new(_3363.BevelDifferentialPlanetGearCompoundPowerFlow))

    def results_for_bevel_differential_sun_gear(self, design_entity: '_2066.BevelDifferentialSunGear') -> 'Iterable[_3364.BevelDifferentialSunGearCompoundPowerFlow]':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.gears.BevelDifferentialSunGear)

        Returns:
            Iterable[mastapy.system_model.analyses_and_results.power_flows.compound.BevelDifferentialSunGearCompoundPowerFlow]
        '''

        return conversion.pn_to_mp_objects_in_iterable(self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None), constructor.new(_3364.BevelDifferentialSunGearCompoundPowerFlow))

    def results_for_bevel_gear(self, design_entity: '_2067.BevelGear') -> 'Iterable[_3365.BevelGearCompoundPowerFlow]':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.gears.BevelGear)

        Returns:
            Iterable[mastapy.system_model.analyses_and_results.power_flows.compound.BevelGearCompoundPowerFlow]
        '''

        return conversion.pn_to_mp_objects_in_iterable(self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None), constructor.new(_3365.BevelGearCompoundPowerFlow))

    def results_for_bevel_gear_set(self, design_entity: '_2068.BevelGearSet') -> 'Iterable[_3367.BevelGearSetCompoundPowerFlow]':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.gears.BevelGearSet)

        Returns:
            Iterable[mastapy.system_model.analyses_and_results.power_flows.compound.BevelGearSetCompoundPowerFlow]
        '''

        return conversion.pn_to_mp_objects_in_iterable(self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None), constructor.new(_3367.BevelGearSetCompoundPowerFlow))

    def results_for_conical_gear(self, design_entity: '_2071.ConicalGear') -> 'Iterable[_3382.ConicalGearCompoundPowerFlow]':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.gears.ConicalGear)

        Returns:
            Iterable[mastapy.system_model.analyses_and_results.power_flows.compound.ConicalGearCompoundPowerFlow]
        '''

        return conversion.pn_to_mp_objects_in_iterable(self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None), constructor.new(_3382.ConicalGearCompoundPowerFlow))

    def results_for_conical_gear_set(self, design_entity: '_2072.ConicalGearSet') -> 'Iterable[_3384.ConicalGearSetCompoundPowerFlow]':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.gears.ConicalGearSet)

        Returns:
            Iterable[mastapy.system_model.analyses_and_results.power_flows.compound.ConicalGearSetCompoundPowerFlow]
        '''

        return conversion.pn_to_mp_objects_in_iterable(self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None), constructor.new(_3384.ConicalGearSetCompoundPowerFlow))

    def results_for_cylindrical_gear(self, design_entity: '_2073.CylindricalGear') -> 'Iterable[_3393.CylindricalGearCompoundPowerFlow]':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.gears.CylindricalGear)

        Returns:
            Iterable[mastapy.system_model.analyses_and_results.power_flows.compound.CylindricalGearCompoundPowerFlow]
        '''

        return conversion.pn_to_mp_objects_in_iterable(self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None), constructor.new(_3393.CylindricalGearCompoundPowerFlow))

    def results_for_cylindrical_gear_set(self, design_entity: '_2074.CylindricalGearSet') -> 'Iterable[_3395.CylindricalGearSetCompoundPowerFlow]':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.gears.CylindricalGearSet)

        Returns:
            Iterable[mastapy.system_model.analyses_and_results.power_flows.compound.CylindricalGearSetCompoundPowerFlow]
        '''

        return conversion.pn_to_mp_objects_in_iterable(self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None), constructor.new(_3395.CylindricalGearSetCompoundPowerFlow))

    def results_for_cylindrical_planet_gear(self, design_entity: '_2075.CylindricalPlanetGear') -> 'Iterable[_3396.CylindricalPlanetGearCompoundPowerFlow]':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.gears.CylindricalPlanetGear)

        Returns:
            Iterable[mastapy.system_model.analyses_and_results.power_flows.compound.CylindricalPlanetGearCompoundPowerFlow]
        '''

        return conversion.pn_to_mp_objects_in_iterable(self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None), constructor.new(_3396.CylindricalPlanetGearCompoundPowerFlow))

    def results_for_gear(self, design_entity: '_2078.Gear') -> 'Iterable[_3403.GearCompoundPowerFlow]':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.gears.Gear)

        Returns:
            Iterable[mastapy.system_model.analyses_and_results.power_flows.compound.GearCompoundPowerFlow]
        '''

        return conversion.pn_to_mp_objects_in_iterable(self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None), constructor.new(_3403.GearCompoundPowerFlow))

    def results_for_gear_set(self, design_entity: '_2080.GearSet') -> 'Iterable[_3405.GearSetCompoundPowerFlow]':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.gears.GearSet)

        Returns:
            Iterable[mastapy.system_model.analyses_and_results.power_flows.compound.GearSetCompoundPowerFlow]
        '''

        return conversion.pn_to_mp_objects_in_iterable(self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None), constructor.new(_3405.GearSetCompoundPowerFlow))

    def results_for_hypoid_gear(self, design_entity: '_2082.HypoidGear') -> 'Iterable[_3407.HypoidGearCompoundPowerFlow]':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.gears.HypoidGear)

        Returns:
            Iterable[mastapy.system_model.analyses_and_results.power_flows.compound.HypoidGearCompoundPowerFlow]
        '''

        return conversion.pn_to_mp_objects_in_iterable(self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None), constructor.new(_3407.HypoidGearCompoundPowerFlow))

    def results_for_hypoid_gear_set(self, design_entity: '_2083.HypoidGearSet') -> 'Iterable[_3409.HypoidGearSetCompoundPowerFlow]':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.gears.HypoidGearSet)

        Returns:
            Iterable[mastapy.system_model.analyses_and_results.power_flows.compound.HypoidGearSetCompoundPowerFlow]
        '''

        return conversion.pn_to_mp_objects_in_iterable(self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None), constructor.new(_3409.HypoidGearSetCompoundPowerFlow))

    def results_for_klingelnberg_cyclo_palloid_conical_gear(self, design_entity: '_2084.KlingelnbergCycloPalloidConicalGear') -> 'Iterable[_3412.KlingelnbergCycloPalloidConicalGearCompoundPowerFlow]':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.gears.KlingelnbergCycloPalloidConicalGear)

        Returns:
            Iterable[mastapy.system_model.analyses_and_results.power_flows.compound.KlingelnbergCycloPalloidConicalGearCompoundPowerFlow]
        '''

        return conversion.pn_to_mp_objects_in_iterable(self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None), constructor.new(_3412.KlingelnbergCycloPalloidConicalGearCompoundPowerFlow))

    def results_for_klingelnberg_cyclo_palloid_conical_gear_set(self, design_entity: '_2085.KlingelnbergCycloPalloidConicalGearSet') -> 'Iterable[_3414.KlingelnbergCycloPalloidConicalGearSetCompoundPowerFlow]':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.gears.KlingelnbergCycloPalloidConicalGearSet)

        Returns:
            Iterable[mastapy.system_model.analyses_and_results.power_flows.compound.KlingelnbergCycloPalloidConicalGearSetCompoundPowerFlow]
        '''

        return conversion.pn_to_mp_objects_in_iterable(self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None), constructor.new(_3414.KlingelnbergCycloPalloidConicalGearSetCompoundPowerFlow))

    def results_for_klingelnberg_cyclo_palloid_hypoid_gear(self, design_entity: '_2086.KlingelnbergCycloPalloidHypoidGear') -> 'Iterable[_3415.KlingelnbergCycloPalloidHypoidGearCompoundPowerFlow]':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.gears.KlingelnbergCycloPalloidHypoidGear)

        Returns:
            Iterable[mastapy.system_model.analyses_and_results.power_flows.compound.KlingelnbergCycloPalloidHypoidGearCompoundPowerFlow]
        '''

        return conversion.pn_to_mp_objects_in_iterable(self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None), constructor.new(_3415.KlingelnbergCycloPalloidHypoidGearCompoundPowerFlow))

    def results_for_klingelnberg_cyclo_palloid_hypoid_gear_set(self, design_entity: '_2087.KlingelnbergCycloPalloidHypoidGearSet') -> 'Iterable[_3417.KlingelnbergCycloPalloidHypoidGearSetCompoundPowerFlow]':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.gears.KlingelnbergCycloPalloidHypoidGearSet)

        Returns:
            Iterable[mastapy.system_model.analyses_and_results.power_flows.compound.KlingelnbergCycloPalloidHypoidGearSetCompoundPowerFlow]
        '''

        return conversion.pn_to_mp_objects_in_iterable(self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None), constructor.new(_3417.KlingelnbergCycloPalloidHypoidGearSetCompoundPowerFlow))

    def results_for_klingelnberg_cyclo_palloid_spiral_bevel_gear(self, design_entity: '_2088.KlingelnbergCycloPalloidSpiralBevelGear') -> 'Iterable[_3418.KlingelnbergCycloPalloidSpiralBevelGearCompoundPowerFlow]':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.gears.KlingelnbergCycloPalloidSpiralBevelGear)

        Returns:
            Iterable[mastapy.system_model.analyses_and_results.power_flows.compound.KlingelnbergCycloPalloidSpiralBevelGearCompoundPowerFlow]
        '''

        return conversion.pn_to_mp_objects_in_iterable(self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None), constructor.new(_3418.KlingelnbergCycloPalloidSpiralBevelGearCompoundPowerFlow))

    def results_for_klingelnberg_cyclo_palloid_spiral_bevel_gear_set(self, design_entity: '_2089.KlingelnbergCycloPalloidSpiralBevelGearSet') -> 'Iterable[_3420.KlingelnbergCycloPalloidSpiralBevelGearSetCompoundPowerFlow]':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.gears.KlingelnbergCycloPalloidSpiralBevelGearSet)

        Returns:
            Iterable[mastapy.system_model.analyses_and_results.power_flows.compound.KlingelnbergCycloPalloidSpiralBevelGearSetCompoundPowerFlow]
        '''

        return conversion.pn_to_mp_objects_in_iterable(self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None), constructor.new(_3420.KlingelnbergCycloPalloidSpiralBevelGearSetCompoundPowerFlow))

    def results_for_planetary_gear_set(self, design_entity: '_2090.PlanetaryGearSet') -> 'Iterable[_3430.PlanetaryGearSetCompoundPowerFlow]':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.gears.PlanetaryGearSet)

        Returns:
            Iterable[mastapy.system_model.analyses_and_results.power_flows.compound.PlanetaryGearSetCompoundPowerFlow]
        '''

        return conversion.pn_to_mp_objects_in_iterable(self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None), constructor.new(_3430.PlanetaryGearSetCompoundPowerFlow))

    def results_for_spiral_bevel_gear(self, design_entity: '_2091.SpiralBevelGear') -> 'Iterable[_3443.SpiralBevelGearCompoundPowerFlow]':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.gears.SpiralBevelGear)

        Returns:
            Iterable[mastapy.system_model.analyses_and_results.power_flows.compound.SpiralBevelGearCompoundPowerFlow]
        '''

        return conversion.pn_to_mp_objects_in_iterable(self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None), constructor.new(_3443.SpiralBevelGearCompoundPowerFlow))

    def results_for_spiral_bevel_gear_set(self, design_entity: '_2092.SpiralBevelGearSet') -> 'Iterable[_3445.SpiralBevelGearSetCompoundPowerFlow]':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.gears.SpiralBevelGearSet)

        Returns:
            Iterable[mastapy.system_model.analyses_and_results.power_flows.compound.SpiralBevelGearSetCompoundPowerFlow]
        '''

        return conversion.pn_to_mp_objects_in_iterable(self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None), constructor.new(_3445.SpiralBevelGearSetCompoundPowerFlow))

    def results_for_straight_bevel_diff_gear(self, design_entity: '_2093.StraightBevelDiffGear') -> 'Iterable[_3449.StraightBevelDiffGearCompoundPowerFlow]':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.gears.StraightBevelDiffGear)

        Returns:
            Iterable[mastapy.system_model.analyses_and_results.power_flows.compound.StraightBevelDiffGearCompoundPowerFlow]
        '''

        return conversion.pn_to_mp_objects_in_iterable(self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None), constructor.new(_3449.StraightBevelDiffGearCompoundPowerFlow))

    def results_for_straight_bevel_diff_gear_set(self, design_entity: '_2094.StraightBevelDiffGearSet') -> 'Iterable[_3451.StraightBevelDiffGearSetCompoundPowerFlow]':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.gears.StraightBevelDiffGearSet)

        Returns:
            Iterable[mastapy.system_model.analyses_and_results.power_flows.compound.StraightBevelDiffGearSetCompoundPowerFlow]
        '''

        return conversion.pn_to_mp_objects_in_iterable(self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None), constructor.new(_3451.StraightBevelDiffGearSetCompoundPowerFlow))

    def results_for_straight_bevel_gear(self, design_entity: '_2095.StraightBevelGear') -> 'Iterable[_3452.StraightBevelGearCompoundPowerFlow]':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.gears.StraightBevelGear)

        Returns:
            Iterable[mastapy.system_model.analyses_and_results.power_flows.compound.StraightBevelGearCompoundPowerFlow]
        '''

        return conversion.pn_to_mp_objects_in_iterable(self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None), constructor.new(_3452.StraightBevelGearCompoundPowerFlow))

    def results_for_straight_bevel_gear_set(self, design_entity: '_2096.StraightBevelGearSet') -> 'Iterable[_3454.StraightBevelGearSetCompoundPowerFlow]':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.gears.StraightBevelGearSet)

        Returns:
            Iterable[mastapy.system_model.analyses_and_results.power_flows.compound.StraightBevelGearSetCompoundPowerFlow]
        '''

        return conversion.pn_to_mp_objects_in_iterable(self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None), constructor.new(_3454.StraightBevelGearSetCompoundPowerFlow))

    def results_for_straight_bevel_planet_gear(self, design_entity: '_2097.StraightBevelPlanetGear') -> 'Iterable[_3455.StraightBevelPlanetGearCompoundPowerFlow]':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.gears.StraightBevelPlanetGear)

        Returns:
            Iterable[mastapy.system_model.analyses_and_results.power_flows.compound.StraightBevelPlanetGearCompoundPowerFlow]
        '''

        return conversion.pn_to_mp_objects_in_iterable(self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None), constructor.new(_3455.StraightBevelPlanetGearCompoundPowerFlow))

    def results_for_straight_bevel_sun_gear(self, design_entity: '_2098.StraightBevelSunGear') -> 'Iterable[_3456.StraightBevelSunGearCompoundPowerFlow]':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.gears.StraightBevelSunGear)

        Returns:
            Iterable[mastapy.system_model.analyses_and_results.power_flows.compound.StraightBevelSunGearCompoundPowerFlow]
        '''

        return conversion.pn_to_mp_objects_in_iterable(self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None), constructor.new(_3456.StraightBevelSunGearCompoundPowerFlow))

    def results_for_worm_gear(self, design_entity: '_2099.WormGear') -> 'Iterable[_3467.WormGearCompoundPowerFlow]':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.gears.WormGear)

        Returns:
            Iterable[mastapy.system_model.analyses_and_results.power_flows.compound.WormGearCompoundPowerFlow]
        '''

        return conversion.pn_to_mp_objects_in_iterable(self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None), constructor.new(_3467.WormGearCompoundPowerFlow))

    def results_for_worm_gear_set(self, design_entity: '_2100.WormGearSet') -> 'Iterable[_3469.WormGearSetCompoundPowerFlow]':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.gears.WormGearSet)

        Returns:
            Iterable[mastapy.system_model.analyses_and_results.power_flows.compound.WormGearSetCompoundPowerFlow]
        '''

        return conversion.pn_to_mp_objects_in_iterable(self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None), constructor.new(_3469.WormGearSetCompoundPowerFlow))

    def results_for_zerol_bevel_gear(self, design_entity: '_2101.ZerolBevelGear') -> 'Iterable[_3470.ZerolBevelGearCompoundPowerFlow]':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.gears.ZerolBevelGear)

        Returns:
            Iterable[mastapy.system_model.analyses_and_results.power_flows.compound.ZerolBevelGearCompoundPowerFlow]
        '''

        return conversion.pn_to_mp_objects_in_iterable(self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None), constructor.new(_3470.ZerolBevelGearCompoundPowerFlow))

    def results_for_zerol_bevel_gear_set(self, design_entity: '_2102.ZerolBevelGearSet') -> 'Iterable[_3472.ZerolBevelGearSetCompoundPowerFlow]':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.gears.ZerolBevelGearSet)

        Returns:
            Iterable[mastapy.system_model.analyses_and_results.power_flows.compound.ZerolBevelGearSetCompoundPowerFlow]
        '''

        return conversion.pn_to_mp_objects_in_iterable(self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None), constructor.new(_3472.ZerolBevelGearSetCompoundPowerFlow))

    def results_for_part_to_part_shear_coupling(self, design_entity: '_2131.PartToPartShearCoupling') -> 'Iterable[_3426.PartToPartShearCouplingCompoundPowerFlow]':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.couplings.PartToPartShearCoupling)

        Returns:
            Iterable[mastapy.system_model.analyses_and_results.power_flows.compound.PartToPartShearCouplingCompoundPowerFlow]
        '''

        return conversion.pn_to_mp_objects_in_iterable(self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None), constructor.new(_3426.PartToPartShearCouplingCompoundPowerFlow))

    def results_for_part_to_part_shear_coupling_half(self, design_entity: '_2132.PartToPartShearCouplingHalf') -> 'Iterable[_3428.PartToPartShearCouplingHalfCompoundPowerFlow]':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.couplings.PartToPartShearCouplingHalf)

        Returns:
            Iterable[mastapy.system_model.analyses_and_results.power_flows.compound.PartToPartShearCouplingHalfCompoundPowerFlow]
        '''

        return conversion.pn_to_mp_objects_in_iterable(self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None), constructor.new(_3428.PartToPartShearCouplingHalfCompoundPowerFlow))

    def results_for_belt_drive(self, design_entity: '_2120.BeltDrive') -> 'Iterable[_3359.BeltDriveCompoundPowerFlow]':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.couplings.BeltDrive)

        Returns:
            Iterable[mastapy.system_model.analyses_and_results.power_flows.compound.BeltDriveCompoundPowerFlow]
        '''

        return conversion.pn_to_mp_objects_in_iterable(self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None), constructor.new(_3359.BeltDriveCompoundPowerFlow))

    def results_for_clutch(self, design_entity: '_2122.Clutch') -> 'Iterable[_3371.ClutchCompoundPowerFlow]':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.couplings.Clutch)

        Returns:
            Iterable[mastapy.system_model.analyses_and_results.power_flows.compound.ClutchCompoundPowerFlow]
        '''

        return conversion.pn_to_mp_objects_in_iterable(self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None), constructor.new(_3371.ClutchCompoundPowerFlow))

    def results_for_clutch_half(self, design_entity: '_2123.ClutchHalf') -> 'Iterable[_3373.ClutchHalfCompoundPowerFlow]':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.couplings.ClutchHalf)

        Returns:
            Iterable[mastapy.system_model.analyses_and_results.power_flows.compound.ClutchHalfCompoundPowerFlow]
        '''

        return conversion.pn_to_mp_objects_in_iterable(self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None), constructor.new(_3373.ClutchHalfCompoundPowerFlow))

    def results_for_concept_coupling(self, design_entity: '_2125.ConceptCoupling') -> 'Iterable[_3376.ConceptCouplingCompoundPowerFlow]':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.couplings.ConceptCoupling)

        Returns:
            Iterable[mastapy.system_model.analyses_and_results.power_flows.compound.ConceptCouplingCompoundPowerFlow]
        '''

        return conversion.pn_to_mp_objects_in_iterable(self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None), constructor.new(_3376.ConceptCouplingCompoundPowerFlow))

    def results_for_concept_coupling_half(self, design_entity: '_2126.ConceptCouplingHalf') -> 'Iterable[_3378.ConceptCouplingHalfCompoundPowerFlow]':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.couplings.ConceptCouplingHalf)

        Returns:
            Iterable[mastapy.system_model.analyses_and_results.power_flows.compound.ConceptCouplingHalfCompoundPowerFlow]
        '''

        return conversion.pn_to_mp_objects_in_iterable(self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None), constructor.new(_3378.ConceptCouplingHalfCompoundPowerFlow))

    def results_for_coupling(self, design_entity: '_2127.Coupling') -> 'Iterable[_3387.CouplingCompoundPowerFlow]':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.couplings.Coupling)

        Returns:
            Iterable[mastapy.system_model.analyses_and_results.power_flows.compound.CouplingCompoundPowerFlow]
        '''

        return conversion.pn_to_mp_objects_in_iterable(self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None), constructor.new(_3387.CouplingCompoundPowerFlow))

    def results_for_coupling_half(self, design_entity: '_2128.CouplingHalf') -> 'Iterable[_3389.CouplingHalfCompoundPowerFlow]':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.couplings.CouplingHalf)

        Returns:
            Iterable[mastapy.system_model.analyses_and_results.power_flows.compound.CouplingHalfCompoundPowerFlow]
        '''

        return conversion.pn_to_mp_objects_in_iterable(self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None), constructor.new(_3389.CouplingHalfCompoundPowerFlow))

    def results_for_cvt(self, design_entity: '_2129.CVT') -> 'Iterable[_3391.CVTCompoundPowerFlow]':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.couplings.CVT)

        Returns:
            Iterable[mastapy.system_model.analyses_and_results.power_flows.compound.CVTCompoundPowerFlow]
        '''

        return conversion.pn_to_mp_objects_in_iterable(self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None), constructor.new(_3391.CVTCompoundPowerFlow))

    def results_for_cvt_pulley(self, design_entity: '_2130.CVTPulley') -> 'Iterable[_3392.CVTPulleyCompoundPowerFlow]':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.couplings.CVTPulley)

        Returns:
            Iterable[mastapy.system_model.analyses_and_results.power_flows.compound.CVTPulleyCompoundPowerFlow]
        '''

        return conversion.pn_to_mp_objects_in_iterable(self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None), constructor.new(_3392.CVTPulleyCompoundPowerFlow))

    def results_for_pulley(self, design_entity: '_2133.Pulley') -> 'Iterable[_3434.PulleyCompoundPowerFlow]':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.couplings.Pulley)

        Returns:
            Iterable[mastapy.system_model.analyses_and_results.power_flows.compound.PulleyCompoundPowerFlow]
        '''

        return conversion.pn_to_mp_objects_in_iterable(self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None), constructor.new(_3434.PulleyCompoundPowerFlow))

    def results_for_shaft_hub_connection(self, design_entity: '_2141.ShaftHubConnection') -> 'Iterable[_3440.ShaftHubConnectionCompoundPowerFlow]':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.couplings.ShaftHubConnection)

        Returns:
            Iterable[mastapy.system_model.analyses_and_results.power_flows.compound.ShaftHubConnectionCompoundPowerFlow]
        '''

        return conversion.pn_to_mp_objects_in_iterable(self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None), constructor.new(_3440.ShaftHubConnectionCompoundPowerFlow))

    def results_for_rolling_ring(self, design_entity: '_2139.RollingRing') -> 'Iterable[_3436.RollingRingCompoundPowerFlow]':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.couplings.RollingRing)

        Returns:
            Iterable[mastapy.system_model.analyses_and_results.power_flows.compound.RollingRingCompoundPowerFlow]
        '''

        return conversion.pn_to_mp_objects_in_iterable(self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None), constructor.new(_3436.RollingRingCompoundPowerFlow))

    def results_for_rolling_ring_assembly(self, design_entity: '_2140.RollingRingAssembly') -> 'Iterable[_3435.RollingRingAssemblyCompoundPowerFlow]':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.couplings.RollingRingAssembly)

        Returns:
            Iterable[mastapy.system_model.analyses_and_results.power_flows.compound.RollingRingAssemblyCompoundPowerFlow]
        '''

        return conversion.pn_to_mp_objects_in_iterable(self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None), constructor.new(_3435.RollingRingAssemblyCompoundPowerFlow))

    def results_for_spring_damper(self, design_entity: '_2142.SpringDamper') -> 'Iterable[_3446.SpringDamperCompoundPowerFlow]':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.couplings.SpringDamper)

        Returns:
            Iterable[mastapy.system_model.analyses_and_results.power_flows.compound.SpringDamperCompoundPowerFlow]
        '''

        return conversion.pn_to_mp_objects_in_iterable(self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None), constructor.new(_3446.SpringDamperCompoundPowerFlow))

    def results_for_spring_damper_half(self, design_entity: '_2143.SpringDamperHalf') -> 'Iterable[_3448.SpringDamperHalfCompoundPowerFlow]':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.couplings.SpringDamperHalf)

        Returns:
            Iterable[mastapy.system_model.analyses_and_results.power_flows.compound.SpringDamperHalfCompoundPowerFlow]
        '''

        return conversion.pn_to_mp_objects_in_iterable(self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None), constructor.new(_3448.SpringDamperHalfCompoundPowerFlow))

    def results_for_synchroniser(self, design_entity: '_2144.Synchroniser') -> 'Iterable[_3457.SynchroniserCompoundPowerFlow]':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.couplings.Synchroniser)

        Returns:
            Iterable[mastapy.system_model.analyses_and_results.power_flows.compound.SynchroniserCompoundPowerFlow]
        '''

        return conversion.pn_to_mp_objects_in_iterable(self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None), constructor.new(_3457.SynchroniserCompoundPowerFlow))

    def results_for_synchroniser_half(self, design_entity: '_2146.SynchroniserHalf') -> 'Iterable[_3458.SynchroniserHalfCompoundPowerFlow]':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.couplings.SynchroniserHalf)

        Returns:
            Iterable[mastapy.system_model.analyses_and_results.power_flows.compound.SynchroniserHalfCompoundPowerFlow]
        '''

        return conversion.pn_to_mp_objects_in_iterable(self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None), constructor.new(_3458.SynchroniserHalfCompoundPowerFlow))

    def results_for_synchroniser_part(self, design_entity: '_2147.SynchroniserPart') -> 'Iterable[_3459.SynchroniserPartCompoundPowerFlow]':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.couplings.SynchroniserPart)

        Returns:
            Iterable[mastapy.system_model.analyses_and_results.power_flows.compound.SynchroniserPartCompoundPowerFlow]
        '''

        return conversion.pn_to_mp_objects_in_iterable(self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None), constructor.new(_3459.SynchroniserPartCompoundPowerFlow))

    def results_for_synchroniser_sleeve(self, design_entity: '_2148.SynchroniserSleeve') -> 'Iterable[_3460.SynchroniserSleeveCompoundPowerFlow]':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.couplings.SynchroniserSleeve)

        Returns:
            Iterable[mastapy.system_model.analyses_and_results.power_flows.compound.SynchroniserSleeveCompoundPowerFlow]
        '''

        return conversion.pn_to_mp_objects_in_iterable(self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None), constructor.new(_3460.SynchroniserSleeveCompoundPowerFlow))

    def results_for_torque_converter(self, design_entity: '_2149.TorqueConverter') -> 'Iterable[_3461.TorqueConverterCompoundPowerFlow]':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.couplings.TorqueConverter)

        Returns:
            Iterable[mastapy.system_model.analyses_and_results.power_flows.compound.TorqueConverterCompoundPowerFlow]
        '''

        return conversion.pn_to_mp_objects_in_iterable(self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None), constructor.new(_3461.TorqueConverterCompoundPowerFlow))

    def results_for_torque_converter_pump(self, design_entity: '_2150.TorqueConverterPump') -> 'Iterable[_3463.TorqueConverterPumpCompoundPowerFlow]':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.couplings.TorqueConverterPump)

        Returns:
            Iterable[mastapy.system_model.analyses_and_results.power_flows.compound.TorqueConverterPumpCompoundPowerFlow]
        '''

        return conversion.pn_to_mp_objects_in_iterable(self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None), constructor.new(_3463.TorqueConverterPumpCompoundPowerFlow))

    def results_for_torque_converter_turbine(self, design_entity: '_2152.TorqueConverterTurbine') -> 'Iterable[_3464.TorqueConverterTurbineCompoundPowerFlow]':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.couplings.TorqueConverterTurbine)

        Returns:
            Iterable[mastapy.system_model.analyses_and_results.power_flows.compound.TorqueConverterTurbineCompoundPowerFlow]
        '''

        return conversion.pn_to_mp_objects_in_iterable(self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None), constructor.new(_3464.TorqueConverterTurbineCompoundPowerFlow))

    def results_for_cvt_belt_connection(self, design_entity: '_1846.CVTBeltConnection') -> 'Iterable[_3390.CVTBeltConnectionCompoundPowerFlow]':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.connections_and_sockets.CVTBeltConnection)

        Returns:
            Iterable[mastapy.system_model.analyses_and_results.power_flows.compound.CVTBeltConnectionCompoundPowerFlow]
        '''

        return conversion.pn_to_mp_objects_in_iterable(self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None), constructor.new(_3390.CVTBeltConnectionCompoundPowerFlow))

    def results_for_belt_connection(self, design_entity: '_1841.BeltConnection') -> 'Iterable[_3358.BeltConnectionCompoundPowerFlow]':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.connections_and_sockets.BeltConnection)

        Returns:
            Iterable[mastapy.system_model.analyses_and_results.power_flows.compound.BeltConnectionCompoundPowerFlow]
        '''

        return conversion.pn_to_mp_objects_in_iterable(self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None), constructor.new(_3358.BeltConnectionCompoundPowerFlow))

    def results_for_coaxial_connection(self, design_entity: '_1842.CoaxialConnection') -> 'Iterable[_3374.CoaxialConnectionCompoundPowerFlow]':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.connections_and_sockets.CoaxialConnection)

        Returns:
            Iterable[mastapy.system_model.analyses_and_results.power_flows.compound.CoaxialConnectionCompoundPowerFlow]
        '''

        return conversion.pn_to_mp_objects_in_iterable(self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None), constructor.new(_3374.CoaxialConnectionCompoundPowerFlow))

    def results_for_connection(self, design_entity: '_1845.Connection') -> 'Iterable[_3385.ConnectionCompoundPowerFlow]':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.connections_and_sockets.Connection)

        Returns:
            Iterable[mastapy.system_model.analyses_and_results.power_flows.compound.ConnectionCompoundPowerFlow]
        '''

        return conversion.pn_to_mp_objects_in_iterable(self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None), constructor.new(_3385.ConnectionCompoundPowerFlow))

    def results_for_inter_mountable_component_connection(self, design_entity: '_1854.InterMountableComponentConnection') -> 'Iterable[_3411.InterMountableComponentConnectionCompoundPowerFlow]':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.connections_and_sockets.InterMountableComponentConnection)

        Returns:
            Iterable[mastapy.system_model.analyses_and_results.power_flows.compound.InterMountableComponentConnectionCompoundPowerFlow]
        '''

        return conversion.pn_to_mp_objects_in_iterable(self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None), constructor.new(_3411.InterMountableComponentConnectionCompoundPowerFlow))

    def results_for_planetary_connection(self, design_entity: '_1857.PlanetaryConnection') -> 'Iterable[_3429.PlanetaryConnectionCompoundPowerFlow]':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.connections_and_sockets.PlanetaryConnection)

        Returns:
            Iterable[mastapy.system_model.analyses_and_results.power_flows.compound.PlanetaryConnectionCompoundPowerFlow]
        '''

        return conversion.pn_to_mp_objects_in_iterable(self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None), constructor.new(_3429.PlanetaryConnectionCompoundPowerFlow))

    def results_for_rolling_ring_connection(self, design_entity: '_1861.RollingRingConnection') -> 'Iterable[_3437.RollingRingConnectionCompoundPowerFlow]':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.connections_and_sockets.RollingRingConnection)

        Returns:
            Iterable[mastapy.system_model.analyses_and_results.power_flows.compound.RollingRingConnectionCompoundPowerFlow]
        '''

        return conversion.pn_to_mp_objects_in_iterable(self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None), constructor.new(_3437.RollingRingConnectionCompoundPowerFlow))

    def results_for_shaft_to_mountable_component_connection(self, design_entity: '_1865.ShaftToMountableComponentConnection') -> 'Iterable[_3441.ShaftToMountableComponentConnectionCompoundPowerFlow]':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.connections_and_sockets.ShaftToMountableComponentConnection)

        Returns:
            Iterable[mastapy.system_model.analyses_and_results.power_flows.compound.ShaftToMountableComponentConnectionCompoundPowerFlow]
        '''

        return conversion.pn_to_mp_objects_in_iterable(self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None), constructor.new(_3441.ShaftToMountableComponentConnectionCompoundPowerFlow))

    def results_for_bevel_differential_gear_mesh(self, design_entity: '_1871.BevelDifferentialGearMesh') -> 'Iterable[_3361.BevelDifferentialGearMeshCompoundPowerFlow]':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.connections_and_sockets.gears.BevelDifferentialGearMesh)

        Returns:
            Iterable[mastapy.system_model.analyses_and_results.power_flows.compound.BevelDifferentialGearMeshCompoundPowerFlow]
        '''

        return conversion.pn_to_mp_objects_in_iterable(self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None), constructor.new(_3361.BevelDifferentialGearMeshCompoundPowerFlow))

    def results_for_concept_gear_mesh(self, design_entity: '_1875.ConceptGearMesh') -> 'Iterable[_3380.ConceptGearMeshCompoundPowerFlow]':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.connections_and_sockets.gears.ConceptGearMesh)

        Returns:
            Iterable[mastapy.system_model.analyses_and_results.power_flows.compound.ConceptGearMeshCompoundPowerFlow]
        '''

        return conversion.pn_to_mp_objects_in_iterable(self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None), constructor.new(_3380.ConceptGearMeshCompoundPowerFlow))

    def results_for_face_gear_mesh(self, design_entity: '_1881.FaceGearMesh') -> 'Iterable[_3400.FaceGearMeshCompoundPowerFlow]':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.connections_and_sockets.gears.FaceGearMesh)

        Returns:
            Iterable[mastapy.system_model.analyses_and_results.power_flows.compound.FaceGearMeshCompoundPowerFlow]
        '''

        return conversion.pn_to_mp_objects_in_iterable(self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None), constructor.new(_3400.FaceGearMeshCompoundPowerFlow))

    def results_for_straight_bevel_diff_gear_mesh(self, design_entity: '_1895.StraightBevelDiffGearMesh') -> 'Iterable[_3450.StraightBevelDiffGearMeshCompoundPowerFlow]':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.connections_and_sockets.gears.StraightBevelDiffGearMesh)

        Returns:
            Iterable[mastapy.system_model.analyses_and_results.power_flows.compound.StraightBevelDiffGearMeshCompoundPowerFlow]
        '''

        return conversion.pn_to_mp_objects_in_iterable(self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None), constructor.new(_3450.StraightBevelDiffGearMeshCompoundPowerFlow))

    def results_for_bevel_gear_mesh(self, design_entity: '_1873.BevelGearMesh') -> 'Iterable[_3366.BevelGearMeshCompoundPowerFlow]':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.connections_and_sockets.gears.BevelGearMesh)

        Returns:
            Iterable[mastapy.system_model.analyses_and_results.power_flows.compound.BevelGearMeshCompoundPowerFlow]
        '''

        return conversion.pn_to_mp_objects_in_iterable(self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None), constructor.new(_3366.BevelGearMeshCompoundPowerFlow))

    def results_for_conical_gear_mesh(self, design_entity: '_1877.ConicalGearMesh') -> 'Iterable[_3383.ConicalGearMeshCompoundPowerFlow]':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.connections_and_sockets.gears.ConicalGearMesh)

        Returns:
            Iterable[mastapy.system_model.analyses_and_results.power_flows.compound.ConicalGearMeshCompoundPowerFlow]
        '''

        return conversion.pn_to_mp_objects_in_iterable(self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None), constructor.new(_3383.ConicalGearMeshCompoundPowerFlow))

    def results_for_agma_gleason_conical_gear_mesh(self, design_entity: '_1869.AGMAGleasonConicalGearMesh') -> 'Iterable[_3354.AGMAGleasonConicalGearMeshCompoundPowerFlow]':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.connections_and_sockets.gears.AGMAGleasonConicalGearMesh)

        Returns:
            Iterable[mastapy.system_model.analyses_and_results.power_flows.compound.AGMAGleasonConicalGearMeshCompoundPowerFlow]
        '''

        return conversion.pn_to_mp_objects_in_iterable(self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None), constructor.new(_3354.AGMAGleasonConicalGearMeshCompoundPowerFlow))

    def results_for_cylindrical_gear_mesh(self, design_entity: '_1879.CylindricalGearMesh') -> 'Iterable[_3394.CylindricalGearMeshCompoundPowerFlow]':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.connections_and_sockets.gears.CylindricalGearMesh)

        Returns:
            Iterable[mastapy.system_model.analyses_and_results.power_flows.compound.CylindricalGearMeshCompoundPowerFlow]
        '''

        return conversion.pn_to_mp_objects_in_iterable(self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None), constructor.new(_3394.CylindricalGearMeshCompoundPowerFlow))

    def results_for_hypoid_gear_mesh(self, design_entity: '_1885.HypoidGearMesh') -> 'Iterable[_3408.HypoidGearMeshCompoundPowerFlow]':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.connections_and_sockets.gears.HypoidGearMesh)

        Returns:
            Iterable[mastapy.system_model.analyses_and_results.power_flows.compound.HypoidGearMeshCompoundPowerFlow]
        '''

        return conversion.pn_to_mp_objects_in_iterable(self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None), constructor.new(_3408.HypoidGearMeshCompoundPowerFlow))

    def results_for_klingelnberg_cyclo_palloid_conical_gear_mesh(self, design_entity: '_1888.KlingelnbergCycloPalloidConicalGearMesh') -> 'Iterable[_3413.KlingelnbergCycloPalloidConicalGearMeshCompoundPowerFlow]':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.connections_and_sockets.gears.KlingelnbergCycloPalloidConicalGearMesh)

        Returns:
            Iterable[mastapy.system_model.analyses_and_results.power_flows.compound.KlingelnbergCycloPalloidConicalGearMeshCompoundPowerFlow]
        '''

        return conversion.pn_to_mp_objects_in_iterable(self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None), constructor.new(_3413.KlingelnbergCycloPalloidConicalGearMeshCompoundPowerFlow))

    def results_for_klingelnberg_cyclo_palloid_hypoid_gear_mesh(self, design_entity: '_1889.KlingelnbergCycloPalloidHypoidGearMesh') -> 'Iterable[_3416.KlingelnbergCycloPalloidHypoidGearMeshCompoundPowerFlow]':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.connections_and_sockets.gears.KlingelnbergCycloPalloidHypoidGearMesh)

        Returns:
            Iterable[mastapy.system_model.analyses_and_results.power_flows.compound.KlingelnbergCycloPalloidHypoidGearMeshCompoundPowerFlow]
        '''

        return conversion.pn_to_mp_objects_in_iterable(self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None), constructor.new(_3416.KlingelnbergCycloPalloidHypoidGearMeshCompoundPowerFlow))

    def results_for_klingelnberg_cyclo_palloid_spiral_bevel_gear_mesh(self, design_entity: '_1890.KlingelnbergCycloPalloidSpiralBevelGearMesh') -> 'Iterable[_3419.KlingelnbergCycloPalloidSpiralBevelGearMeshCompoundPowerFlow]':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.connections_and_sockets.gears.KlingelnbergCycloPalloidSpiralBevelGearMesh)

        Returns:
            Iterable[mastapy.system_model.analyses_and_results.power_flows.compound.KlingelnbergCycloPalloidSpiralBevelGearMeshCompoundPowerFlow]
        '''

        return conversion.pn_to_mp_objects_in_iterable(self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None), constructor.new(_3419.KlingelnbergCycloPalloidSpiralBevelGearMeshCompoundPowerFlow))

    def results_for_spiral_bevel_gear_mesh(self, design_entity: '_1893.SpiralBevelGearMesh') -> 'Iterable[_3444.SpiralBevelGearMeshCompoundPowerFlow]':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.connections_and_sockets.gears.SpiralBevelGearMesh)

        Returns:
            Iterable[mastapy.system_model.analyses_and_results.power_flows.compound.SpiralBevelGearMeshCompoundPowerFlow]
        '''

        return conversion.pn_to_mp_objects_in_iterable(self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None), constructor.new(_3444.SpiralBevelGearMeshCompoundPowerFlow))

    def results_for_straight_bevel_gear_mesh(self, design_entity: '_1897.StraightBevelGearMesh') -> 'Iterable[_3453.StraightBevelGearMeshCompoundPowerFlow]':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.connections_and_sockets.gears.StraightBevelGearMesh)

        Returns:
            Iterable[mastapy.system_model.analyses_and_results.power_flows.compound.StraightBevelGearMeshCompoundPowerFlow]
        '''

        return conversion.pn_to_mp_objects_in_iterable(self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None), constructor.new(_3453.StraightBevelGearMeshCompoundPowerFlow))

    def results_for_worm_gear_mesh(self, design_entity: '_1899.WormGearMesh') -> 'Iterable[_3468.WormGearMeshCompoundPowerFlow]':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.connections_and_sockets.gears.WormGearMesh)

        Returns:
            Iterable[mastapy.system_model.analyses_and_results.power_flows.compound.WormGearMeshCompoundPowerFlow]
        '''

        return conversion.pn_to_mp_objects_in_iterable(self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None), constructor.new(_3468.WormGearMeshCompoundPowerFlow))

    def results_for_zerol_bevel_gear_mesh(self, design_entity: '_1901.ZerolBevelGearMesh') -> 'Iterable[_3471.ZerolBevelGearMeshCompoundPowerFlow]':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.connections_and_sockets.gears.ZerolBevelGearMesh)

        Returns:
            Iterable[mastapy.system_model.analyses_and_results.power_flows.compound.ZerolBevelGearMeshCompoundPowerFlow]
        '''

        return conversion.pn_to_mp_objects_in_iterable(self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None), constructor.new(_3471.ZerolBevelGearMeshCompoundPowerFlow))

    def results_for_gear_mesh(self, design_entity: '_1883.GearMesh') -> 'Iterable[_3404.GearMeshCompoundPowerFlow]':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.connections_and_sockets.gears.GearMesh)

        Returns:
            Iterable[mastapy.system_model.analyses_and_results.power_flows.compound.GearMeshCompoundPowerFlow]
        '''

        return conversion.pn_to_mp_objects_in_iterable(self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None), constructor.new(_3404.GearMeshCompoundPowerFlow))

    def results_for_part_to_part_shear_coupling_connection(self, design_entity: '_1909.PartToPartShearCouplingConnection') -> 'Iterable[_3427.PartToPartShearCouplingConnectionCompoundPowerFlow]':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.connections_and_sockets.couplings.PartToPartShearCouplingConnection)

        Returns:
            Iterable[mastapy.system_model.analyses_and_results.power_flows.compound.PartToPartShearCouplingConnectionCompoundPowerFlow]
        '''

        return conversion.pn_to_mp_objects_in_iterable(self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None), constructor.new(_3427.PartToPartShearCouplingConnectionCompoundPowerFlow))

    def results_for_clutch_connection(self, design_entity: '_1903.ClutchConnection') -> 'Iterable[_3372.ClutchConnectionCompoundPowerFlow]':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.connections_and_sockets.couplings.ClutchConnection)

        Returns:
            Iterable[mastapy.system_model.analyses_and_results.power_flows.compound.ClutchConnectionCompoundPowerFlow]
        '''

        return conversion.pn_to_mp_objects_in_iterable(self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None), constructor.new(_3372.ClutchConnectionCompoundPowerFlow))

    def results_for_concept_coupling_connection(self, design_entity: '_1905.ConceptCouplingConnection') -> 'Iterable[_3377.ConceptCouplingConnectionCompoundPowerFlow]':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.connections_and_sockets.couplings.ConceptCouplingConnection)

        Returns:
            Iterable[mastapy.system_model.analyses_and_results.power_flows.compound.ConceptCouplingConnectionCompoundPowerFlow]
        '''

        return conversion.pn_to_mp_objects_in_iterable(self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None), constructor.new(_3377.ConceptCouplingConnectionCompoundPowerFlow))

    def results_for_coupling_connection(self, design_entity: '_1907.CouplingConnection') -> 'Iterable[_3388.CouplingConnectionCompoundPowerFlow]':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.connections_and_sockets.couplings.CouplingConnection)

        Returns:
            Iterable[mastapy.system_model.analyses_and_results.power_flows.compound.CouplingConnectionCompoundPowerFlow]
        '''

        return conversion.pn_to_mp_objects_in_iterable(self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None), constructor.new(_3388.CouplingConnectionCompoundPowerFlow))

    def results_for_spring_damper_connection(self, design_entity: '_1911.SpringDamperConnection') -> 'Iterable[_3447.SpringDamperConnectionCompoundPowerFlow]':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.connections_and_sockets.couplings.SpringDamperConnection)

        Returns:
            Iterable[mastapy.system_model.analyses_and_results.power_flows.compound.SpringDamperConnectionCompoundPowerFlow]
        '''

        return conversion.pn_to_mp_objects_in_iterable(self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None), constructor.new(_3447.SpringDamperConnectionCompoundPowerFlow))

    def results_for_torque_converter_connection(self, design_entity: '_1913.TorqueConverterConnection') -> 'Iterable[_3462.TorqueConverterConnectionCompoundPowerFlow]':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.connections_and_sockets.couplings.TorqueConverterConnection)

        Returns:
            Iterable[mastapy.system_model.analyses_and_results.power_flows.compound.TorqueConverterConnectionCompoundPowerFlow]
        '''

        return conversion.pn_to_mp_objects_in_iterable(self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None), constructor.new(_3462.TorqueConverterConnectionCompoundPowerFlow))
