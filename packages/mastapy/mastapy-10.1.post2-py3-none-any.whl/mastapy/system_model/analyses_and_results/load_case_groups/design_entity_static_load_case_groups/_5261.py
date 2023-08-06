'''_5261.py

PartStaticLoadCaseGroup
'''


from typing import Callable, List

from mastapy._internal import constructor, conversion
from mastapy.system_model.part_model import (
    _2018, _1989, _1990, _1991,
    _1994, _1996, _1997, _1998,
    _2001, _2002, _2005, _2006,
    _2007, _2010, _2013, _2014,
    _2015, _2017, _2019, _2021,
    _2022, _2024, _2026, _2027,
    _2028
)
from mastapy._internal.cast_exception import CastException
from mastapy.system_model.part_model.shaft_model import _2031
from mastapy.system_model.part_model.gears import (
    _2061, _2062, _2063, _2064,
    _2065, _2066, _2067, _2068,
    _2069, _2070, _2071, _2072,
    _2073, _2074, _2075, _2076,
    _2077, _2078, _2080, _2082,
    _2083, _2084, _2085, _2086,
    _2087, _2088, _2089, _2090,
    _2091, _2092, _2093, _2094,
    _2095, _2096, _2097, _2098,
    _2099, _2100, _2101, _2102
)
from mastapy.system_model.part_model.couplings import (
    _2120, _2122, _2123, _2125,
    _2126, _2127, _2128, _2129,
    _2130, _2131, _2132, _2133,
    _2139, _2140, _2141, _2142,
    _2143, _2144, _2146, _2147,
    _2148, _2149, _2150, _2152
)
from mastapy.system_model.analyses_and_results.static_loads import _6167
from mastapy.system_model.analyses_and_results.load_case_groups.design_entity_static_load_case_groups import _5259
from mastapy._internal.python_net import python_net_import

_PART_STATIC_LOAD_CASE_GROUP = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.LoadCaseGroups.DesignEntityStaticLoadCaseGroups', 'PartStaticLoadCaseGroup')


__docformat__ = 'restructuredtext en'
__all__ = ('PartStaticLoadCaseGroup',)


class PartStaticLoadCaseGroup(_5259.DesignEntityStaticLoadCaseGroup):
    '''PartStaticLoadCaseGroup

    This is a mastapy class.
    '''

    TYPE = _PART_STATIC_LOAD_CASE_GROUP

    __hash__ = None

    def __init__(self, instance_to_wrap: 'PartStaticLoadCaseGroup.TYPE'):
        super().__init__(instance_to_wrap)

    @property
    def clear_user_specified_excitation_data_for_all_load_cases(self) -> 'Callable[[], None]':
        '''Callable[[], None]: 'ClearUserSpecifiedExcitationDataForAllLoadCases' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return self.wrapped.ClearUserSpecifiedExcitationDataForAllLoadCases

    @property
    def part(self) -> '_2018.Part':
        '''Part: 'Part' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_2018.Part)(self.wrapped.Part) if self.wrapped.Part else None

    @property
    def part_of_type_assembly(self) -> '_1989.Assembly':
        '''Assembly: 'Part' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _1989.Assembly.TYPE not in self.wrapped.Part.__class__.__mro__:
            raise CastException('Failed to cast part to Assembly. Expected: {}.'.format(self.wrapped.Part.__class__.__qualname__))

        return constructor.new(_1989.Assembly)(self.wrapped.Part) if self.wrapped.Part else None

    @property
    def part_of_type_abstract_assembly(self) -> '_1990.AbstractAssembly':
        '''AbstractAssembly: 'Part' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _1990.AbstractAssembly.TYPE not in self.wrapped.Part.__class__.__mro__:
            raise CastException('Failed to cast part to AbstractAssembly. Expected: {}.'.format(self.wrapped.Part.__class__.__qualname__))

        return constructor.new(_1990.AbstractAssembly)(self.wrapped.Part) if self.wrapped.Part else None

    @property
    def part_of_type_abstract_shaft_or_housing(self) -> '_1991.AbstractShaftOrHousing':
        '''AbstractShaftOrHousing: 'Part' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _1991.AbstractShaftOrHousing.TYPE not in self.wrapped.Part.__class__.__mro__:
            raise CastException('Failed to cast part to AbstractShaftOrHousing. Expected: {}.'.format(self.wrapped.Part.__class__.__qualname__))

        return constructor.new(_1991.AbstractShaftOrHousing)(self.wrapped.Part) if self.wrapped.Part else None

    @property
    def part_of_type_bearing(self) -> '_1994.Bearing':
        '''Bearing: 'Part' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _1994.Bearing.TYPE not in self.wrapped.Part.__class__.__mro__:
            raise CastException('Failed to cast part to Bearing. Expected: {}.'.format(self.wrapped.Part.__class__.__qualname__))

        return constructor.new(_1994.Bearing)(self.wrapped.Part) if self.wrapped.Part else None

    @property
    def part_of_type_bolt(self) -> '_1996.Bolt':
        '''Bolt: 'Part' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _1996.Bolt.TYPE not in self.wrapped.Part.__class__.__mro__:
            raise CastException('Failed to cast part to Bolt. Expected: {}.'.format(self.wrapped.Part.__class__.__qualname__))

        return constructor.new(_1996.Bolt)(self.wrapped.Part) if self.wrapped.Part else None

    @property
    def part_of_type_bolted_joint(self) -> '_1997.BoltedJoint':
        '''BoltedJoint: 'Part' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _1997.BoltedJoint.TYPE not in self.wrapped.Part.__class__.__mro__:
            raise CastException('Failed to cast part to BoltedJoint. Expected: {}.'.format(self.wrapped.Part.__class__.__qualname__))

        return constructor.new(_1997.BoltedJoint)(self.wrapped.Part) if self.wrapped.Part else None

    @property
    def part_of_type_component(self) -> '_1998.Component':
        '''Component: 'Part' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _1998.Component.TYPE not in self.wrapped.Part.__class__.__mro__:
            raise CastException('Failed to cast part to Component. Expected: {}.'.format(self.wrapped.Part.__class__.__qualname__))

        return constructor.new(_1998.Component)(self.wrapped.Part) if self.wrapped.Part else None

    @property
    def part_of_type_connector(self) -> '_2001.Connector':
        '''Connector: 'Part' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _2001.Connector.TYPE not in self.wrapped.Part.__class__.__mro__:
            raise CastException('Failed to cast part to Connector. Expected: {}.'.format(self.wrapped.Part.__class__.__qualname__))

        return constructor.new(_2001.Connector)(self.wrapped.Part) if self.wrapped.Part else None

    @property
    def part_of_type_datum(self) -> '_2002.Datum':
        '''Datum: 'Part' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _2002.Datum.TYPE not in self.wrapped.Part.__class__.__mro__:
            raise CastException('Failed to cast part to Datum. Expected: {}.'.format(self.wrapped.Part.__class__.__qualname__))

        return constructor.new(_2002.Datum)(self.wrapped.Part) if self.wrapped.Part else None

    @property
    def part_of_type_external_cad_model(self) -> '_2005.ExternalCADModel':
        '''ExternalCADModel: 'Part' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _2005.ExternalCADModel.TYPE not in self.wrapped.Part.__class__.__mro__:
            raise CastException('Failed to cast part to ExternalCADModel. Expected: {}.'.format(self.wrapped.Part.__class__.__qualname__))

        return constructor.new(_2005.ExternalCADModel)(self.wrapped.Part) if self.wrapped.Part else None

    @property
    def part_of_type_flexible_pin_assembly(self) -> '_2006.FlexiblePinAssembly':
        '''FlexiblePinAssembly: 'Part' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _2006.FlexiblePinAssembly.TYPE not in self.wrapped.Part.__class__.__mro__:
            raise CastException('Failed to cast part to FlexiblePinAssembly. Expected: {}.'.format(self.wrapped.Part.__class__.__qualname__))

        return constructor.new(_2006.FlexiblePinAssembly)(self.wrapped.Part) if self.wrapped.Part else None

    @property
    def part_of_type_guide_dxf_model(self) -> '_2007.GuideDxfModel':
        '''GuideDxfModel: 'Part' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _2007.GuideDxfModel.TYPE not in self.wrapped.Part.__class__.__mro__:
            raise CastException('Failed to cast part to GuideDxfModel. Expected: {}.'.format(self.wrapped.Part.__class__.__qualname__))

        return constructor.new(_2007.GuideDxfModel)(self.wrapped.Part) if self.wrapped.Part else None

    @property
    def part_of_type_imported_fe_component(self) -> '_2010.ImportedFEComponent':
        '''ImportedFEComponent: 'Part' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _2010.ImportedFEComponent.TYPE not in self.wrapped.Part.__class__.__mro__:
            raise CastException('Failed to cast part to ImportedFEComponent. Expected: {}.'.format(self.wrapped.Part.__class__.__qualname__))

        return constructor.new(_2010.ImportedFEComponent)(self.wrapped.Part) if self.wrapped.Part else None

    @property
    def part_of_type_mass_disc(self) -> '_2013.MassDisc':
        '''MassDisc: 'Part' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _2013.MassDisc.TYPE not in self.wrapped.Part.__class__.__mro__:
            raise CastException('Failed to cast part to MassDisc. Expected: {}.'.format(self.wrapped.Part.__class__.__qualname__))

        return constructor.new(_2013.MassDisc)(self.wrapped.Part) if self.wrapped.Part else None

    @property
    def part_of_type_measurement_component(self) -> '_2014.MeasurementComponent':
        '''MeasurementComponent: 'Part' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _2014.MeasurementComponent.TYPE not in self.wrapped.Part.__class__.__mro__:
            raise CastException('Failed to cast part to MeasurementComponent. Expected: {}.'.format(self.wrapped.Part.__class__.__qualname__))

        return constructor.new(_2014.MeasurementComponent)(self.wrapped.Part) if self.wrapped.Part else None

    @property
    def part_of_type_mountable_component(self) -> '_2015.MountableComponent':
        '''MountableComponent: 'Part' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _2015.MountableComponent.TYPE not in self.wrapped.Part.__class__.__mro__:
            raise CastException('Failed to cast part to MountableComponent. Expected: {}.'.format(self.wrapped.Part.__class__.__qualname__))

        return constructor.new(_2015.MountableComponent)(self.wrapped.Part) if self.wrapped.Part else None

    @property
    def part_of_type_oil_seal(self) -> '_2017.OilSeal':
        '''OilSeal: 'Part' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _2017.OilSeal.TYPE not in self.wrapped.Part.__class__.__mro__:
            raise CastException('Failed to cast part to OilSeal. Expected: {}.'.format(self.wrapped.Part.__class__.__qualname__))

        return constructor.new(_2017.OilSeal)(self.wrapped.Part) if self.wrapped.Part else None

    @property
    def part_of_type_planet_carrier(self) -> '_2019.PlanetCarrier':
        '''PlanetCarrier: 'Part' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _2019.PlanetCarrier.TYPE not in self.wrapped.Part.__class__.__mro__:
            raise CastException('Failed to cast part to PlanetCarrier. Expected: {}.'.format(self.wrapped.Part.__class__.__qualname__))

        return constructor.new(_2019.PlanetCarrier)(self.wrapped.Part) if self.wrapped.Part else None

    @property
    def part_of_type_point_load(self) -> '_2021.PointLoad':
        '''PointLoad: 'Part' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _2021.PointLoad.TYPE not in self.wrapped.Part.__class__.__mro__:
            raise CastException('Failed to cast part to PointLoad. Expected: {}.'.format(self.wrapped.Part.__class__.__qualname__))

        return constructor.new(_2021.PointLoad)(self.wrapped.Part) if self.wrapped.Part else None

    @property
    def part_of_type_power_load(self) -> '_2022.PowerLoad':
        '''PowerLoad: 'Part' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _2022.PowerLoad.TYPE not in self.wrapped.Part.__class__.__mro__:
            raise CastException('Failed to cast part to PowerLoad. Expected: {}.'.format(self.wrapped.Part.__class__.__qualname__))

        return constructor.new(_2022.PowerLoad)(self.wrapped.Part) if self.wrapped.Part else None

    @property
    def part_of_type_root_assembly(self) -> '_2024.RootAssembly':
        '''RootAssembly: 'Part' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _2024.RootAssembly.TYPE not in self.wrapped.Part.__class__.__mro__:
            raise CastException('Failed to cast part to RootAssembly. Expected: {}.'.format(self.wrapped.Part.__class__.__qualname__))

        return constructor.new(_2024.RootAssembly)(self.wrapped.Part) if self.wrapped.Part else None

    @property
    def part_of_type_specialised_assembly(self) -> '_2026.SpecialisedAssembly':
        '''SpecialisedAssembly: 'Part' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _2026.SpecialisedAssembly.TYPE not in self.wrapped.Part.__class__.__mro__:
            raise CastException('Failed to cast part to SpecialisedAssembly. Expected: {}.'.format(self.wrapped.Part.__class__.__qualname__))

        return constructor.new(_2026.SpecialisedAssembly)(self.wrapped.Part) if self.wrapped.Part else None

    @property
    def part_of_type_unbalanced_mass(self) -> '_2027.UnbalancedMass':
        '''UnbalancedMass: 'Part' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _2027.UnbalancedMass.TYPE not in self.wrapped.Part.__class__.__mro__:
            raise CastException('Failed to cast part to UnbalancedMass. Expected: {}.'.format(self.wrapped.Part.__class__.__qualname__))

        return constructor.new(_2027.UnbalancedMass)(self.wrapped.Part) if self.wrapped.Part else None

    @property
    def part_of_type_virtual_component(self) -> '_2028.VirtualComponent':
        '''VirtualComponent: 'Part' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _2028.VirtualComponent.TYPE not in self.wrapped.Part.__class__.__mro__:
            raise CastException('Failed to cast part to VirtualComponent. Expected: {}.'.format(self.wrapped.Part.__class__.__qualname__))

        return constructor.new(_2028.VirtualComponent)(self.wrapped.Part) if self.wrapped.Part else None

    @property
    def part_of_type_shaft(self) -> '_2031.Shaft':
        '''Shaft: 'Part' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _2031.Shaft.TYPE not in self.wrapped.Part.__class__.__mro__:
            raise CastException('Failed to cast part to Shaft. Expected: {}.'.format(self.wrapped.Part.__class__.__qualname__))

        return constructor.new(_2031.Shaft)(self.wrapped.Part) if self.wrapped.Part else None

    @property
    def part_of_type_agma_gleason_conical_gear(self) -> '_2061.AGMAGleasonConicalGear':
        '''AGMAGleasonConicalGear: 'Part' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _2061.AGMAGleasonConicalGear.TYPE not in self.wrapped.Part.__class__.__mro__:
            raise CastException('Failed to cast part to AGMAGleasonConicalGear. Expected: {}.'.format(self.wrapped.Part.__class__.__qualname__))

        return constructor.new(_2061.AGMAGleasonConicalGear)(self.wrapped.Part) if self.wrapped.Part else None

    @property
    def part_of_type_agma_gleason_conical_gear_set(self) -> '_2062.AGMAGleasonConicalGearSet':
        '''AGMAGleasonConicalGearSet: 'Part' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _2062.AGMAGleasonConicalGearSet.TYPE not in self.wrapped.Part.__class__.__mro__:
            raise CastException('Failed to cast part to AGMAGleasonConicalGearSet. Expected: {}.'.format(self.wrapped.Part.__class__.__qualname__))

        return constructor.new(_2062.AGMAGleasonConicalGearSet)(self.wrapped.Part) if self.wrapped.Part else None

    @property
    def part_of_type_bevel_differential_gear(self) -> '_2063.BevelDifferentialGear':
        '''BevelDifferentialGear: 'Part' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _2063.BevelDifferentialGear.TYPE not in self.wrapped.Part.__class__.__mro__:
            raise CastException('Failed to cast part to BevelDifferentialGear. Expected: {}.'.format(self.wrapped.Part.__class__.__qualname__))

        return constructor.new(_2063.BevelDifferentialGear)(self.wrapped.Part) if self.wrapped.Part else None

    @property
    def part_of_type_bevel_differential_gear_set(self) -> '_2064.BevelDifferentialGearSet':
        '''BevelDifferentialGearSet: 'Part' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _2064.BevelDifferentialGearSet.TYPE not in self.wrapped.Part.__class__.__mro__:
            raise CastException('Failed to cast part to BevelDifferentialGearSet. Expected: {}.'.format(self.wrapped.Part.__class__.__qualname__))

        return constructor.new(_2064.BevelDifferentialGearSet)(self.wrapped.Part) if self.wrapped.Part else None

    @property
    def part_of_type_bevel_differential_planet_gear(self) -> '_2065.BevelDifferentialPlanetGear':
        '''BevelDifferentialPlanetGear: 'Part' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _2065.BevelDifferentialPlanetGear.TYPE not in self.wrapped.Part.__class__.__mro__:
            raise CastException('Failed to cast part to BevelDifferentialPlanetGear. Expected: {}.'.format(self.wrapped.Part.__class__.__qualname__))

        return constructor.new(_2065.BevelDifferentialPlanetGear)(self.wrapped.Part) if self.wrapped.Part else None

    @property
    def part_of_type_bevel_differential_sun_gear(self) -> '_2066.BevelDifferentialSunGear':
        '''BevelDifferentialSunGear: 'Part' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _2066.BevelDifferentialSunGear.TYPE not in self.wrapped.Part.__class__.__mro__:
            raise CastException('Failed to cast part to BevelDifferentialSunGear. Expected: {}.'.format(self.wrapped.Part.__class__.__qualname__))

        return constructor.new(_2066.BevelDifferentialSunGear)(self.wrapped.Part) if self.wrapped.Part else None

    @property
    def part_of_type_bevel_gear(self) -> '_2067.BevelGear':
        '''BevelGear: 'Part' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _2067.BevelGear.TYPE not in self.wrapped.Part.__class__.__mro__:
            raise CastException('Failed to cast part to BevelGear. Expected: {}.'.format(self.wrapped.Part.__class__.__qualname__))

        return constructor.new(_2067.BevelGear)(self.wrapped.Part) if self.wrapped.Part else None

    @property
    def part_of_type_bevel_gear_set(self) -> '_2068.BevelGearSet':
        '''BevelGearSet: 'Part' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _2068.BevelGearSet.TYPE not in self.wrapped.Part.__class__.__mro__:
            raise CastException('Failed to cast part to BevelGearSet. Expected: {}.'.format(self.wrapped.Part.__class__.__qualname__))

        return constructor.new(_2068.BevelGearSet)(self.wrapped.Part) if self.wrapped.Part else None

    @property
    def part_of_type_concept_gear(self) -> '_2069.ConceptGear':
        '''ConceptGear: 'Part' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _2069.ConceptGear.TYPE not in self.wrapped.Part.__class__.__mro__:
            raise CastException('Failed to cast part to ConceptGear. Expected: {}.'.format(self.wrapped.Part.__class__.__qualname__))

        return constructor.new(_2069.ConceptGear)(self.wrapped.Part) if self.wrapped.Part else None

    @property
    def part_of_type_concept_gear_set(self) -> '_2070.ConceptGearSet':
        '''ConceptGearSet: 'Part' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _2070.ConceptGearSet.TYPE not in self.wrapped.Part.__class__.__mro__:
            raise CastException('Failed to cast part to ConceptGearSet. Expected: {}.'.format(self.wrapped.Part.__class__.__qualname__))

        return constructor.new(_2070.ConceptGearSet)(self.wrapped.Part) if self.wrapped.Part else None

    @property
    def part_of_type_conical_gear(self) -> '_2071.ConicalGear':
        '''ConicalGear: 'Part' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _2071.ConicalGear.TYPE not in self.wrapped.Part.__class__.__mro__:
            raise CastException('Failed to cast part to ConicalGear. Expected: {}.'.format(self.wrapped.Part.__class__.__qualname__))

        return constructor.new(_2071.ConicalGear)(self.wrapped.Part) if self.wrapped.Part else None

    @property
    def part_of_type_conical_gear_set(self) -> '_2072.ConicalGearSet':
        '''ConicalGearSet: 'Part' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _2072.ConicalGearSet.TYPE not in self.wrapped.Part.__class__.__mro__:
            raise CastException('Failed to cast part to ConicalGearSet. Expected: {}.'.format(self.wrapped.Part.__class__.__qualname__))

        return constructor.new(_2072.ConicalGearSet)(self.wrapped.Part) if self.wrapped.Part else None

    @property
    def part_of_type_cylindrical_gear(self) -> '_2073.CylindricalGear':
        '''CylindricalGear: 'Part' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _2073.CylindricalGear.TYPE not in self.wrapped.Part.__class__.__mro__:
            raise CastException('Failed to cast part to CylindricalGear. Expected: {}.'.format(self.wrapped.Part.__class__.__qualname__))

        return constructor.new(_2073.CylindricalGear)(self.wrapped.Part) if self.wrapped.Part else None

    @property
    def part_of_type_cylindrical_gear_set(self) -> '_2074.CylindricalGearSet':
        '''CylindricalGearSet: 'Part' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _2074.CylindricalGearSet.TYPE not in self.wrapped.Part.__class__.__mro__:
            raise CastException('Failed to cast part to CylindricalGearSet. Expected: {}.'.format(self.wrapped.Part.__class__.__qualname__))

        return constructor.new(_2074.CylindricalGearSet)(self.wrapped.Part) if self.wrapped.Part else None

    @property
    def part_of_type_cylindrical_planet_gear(self) -> '_2075.CylindricalPlanetGear':
        '''CylindricalPlanetGear: 'Part' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _2075.CylindricalPlanetGear.TYPE not in self.wrapped.Part.__class__.__mro__:
            raise CastException('Failed to cast part to CylindricalPlanetGear. Expected: {}.'.format(self.wrapped.Part.__class__.__qualname__))

        return constructor.new(_2075.CylindricalPlanetGear)(self.wrapped.Part) if self.wrapped.Part else None

    @property
    def part_of_type_face_gear(self) -> '_2076.FaceGear':
        '''FaceGear: 'Part' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _2076.FaceGear.TYPE not in self.wrapped.Part.__class__.__mro__:
            raise CastException('Failed to cast part to FaceGear. Expected: {}.'.format(self.wrapped.Part.__class__.__qualname__))

        return constructor.new(_2076.FaceGear)(self.wrapped.Part) if self.wrapped.Part else None

    @property
    def part_of_type_face_gear_set(self) -> '_2077.FaceGearSet':
        '''FaceGearSet: 'Part' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _2077.FaceGearSet.TYPE not in self.wrapped.Part.__class__.__mro__:
            raise CastException('Failed to cast part to FaceGearSet. Expected: {}.'.format(self.wrapped.Part.__class__.__qualname__))

        return constructor.new(_2077.FaceGearSet)(self.wrapped.Part) if self.wrapped.Part else None

    @property
    def part_of_type_gear(self) -> '_2078.Gear':
        '''Gear: 'Part' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _2078.Gear.TYPE not in self.wrapped.Part.__class__.__mro__:
            raise CastException('Failed to cast part to Gear. Expected: {}.'.format(self.wrapped.Part.__class__.__qualname__))

        return constructor.new(_2078.Gear)(self.wrapped.Part) if self.wrapped.Part else None

    @property
    def part_of_type_gear_set(self) -> '_2080.GearSet':
        '''GearSet: 'Part' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _2080.GearSet.TYPE not in self.wrapped.Part.__class__.__mro__:
            raise CastException('Failed to cast part to GearSet. Expected: {}.'.format(self.wrapped.Part.__class__.__qualname__))

        return constructor.new(_2080.GearSet)(self.wrapped.Part) if self.wrapped.Part else None

    @property
    def part_of_type_hypoid_gear(self) -> '_2082.HypoidGear':
        '''HypoidGear: 'Part' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _2082.HypoidGear.TYPE not in self.wrapped.Part.__class__.__mro__:
            raise CastException('Failed to cast part to HypoidGear. Expected: {}.'.format(self.wrapped.Part.__class__.__qualname__))

        return constructor.new(_2082.HypoidGear)(self.wrapped.Part) if self.wrapped.Part else None

    @property
    def part_of_type_hypoid_gear_set(self) -> '_2083.HypoidGearSet':
        '''HypoidGearSet: 'Part' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _2083.HypoidGearSet.TYPE not in self.wrapped.Part.__class__.__mro__:
            raise CastException('Failed to cast part to HypoidGearSet. Expected: {}.'.format(self.wrapped.Part.__class__.__qualname__))

        return constructor.new(_2083.HypoidGearSet)(self.wrapped.Part) if self.wrapped.Part else None

    @property
    def part_of_type_klingelnberg_cyclo_palloid_conical_gear(self) -> '_2084.KlingelnbergCycloPalloidConicalGear':
        '''KlingelnbergCycloPalloidConicalGear: 'Part' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _2084.KlingelnbergCycloPalloidConicalGear.TYPE not in self.wrapped.Part.__class__.__mro__:
            raise CastException('Failed to cast part to KlingelnbergCycloPalloidConicalGear. Expected: {}.'.format(self.wrapped.Part.__class__.__qualname__))

        return constructor.new(_2084.KlingelnbergCycloPalloidConicalGear)(self.wrapped.Part) if self.wrapped.Part else None

    @property
    def part_of_type_klingelnberg_cyclo_palloid_conical_gear_set(self) -> '_2085.KlingelnbergCycloPalloidConicalGearSet':
        '''KlingelnbergCycloPalloidConicalGearSet: 'Part' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _2085.KlingelnbergCycloPalloidConicalGearSet.TYPE not in self.wrapped.Part.__class__.__mro__:
            raise CastException('Failed to cast part to KlingelnbergCycloPalloidConicalGearSet. Expected: {}.'.format(self.wrapped.Part.__class__.__qualname__))

        return constructor.new(_2085.KlingelnbergCycloPalloidConicalGearSet)(self.wrapped.Part) if self.wrapped.Part else None

    @property
    def part_of_type_klingelnberg_cyclo_palloid_hypoid_gear(self) -> '_2086.KlingelnbergCycloPalloidHypoidGear':
        '''KlingelnbergCycloPalloidHypoidGear: 'Part' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _2086.KlingelnbergCycloPalloidHypoidGear.TYPE not in self.wrapped.Part.__class__.__mro__:
            raise CastException('Failed to cast part to KlingelnbergCycloPalloidHypoidGear. Expected: {}.'.format(self.wrapped.Part.__class__.__qualname__))

        return constructor.new(_2086.KlingelnbergCycloPalloidHypoidGear)(self.wrapped.Part) if self.wrapped.Part else None

    @property
    def part_of_type_klingelnberg_cyclo_palloid_hypoid_gear_set(self) -> '_2087.KlingelnbergCycloPalloidHypoidGearSet':
        '''KlingelnbergCycloPalloidHypoidGearSet: 'Part' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _2087.KlingelnbergCycloPalloidHypoidGearSet.TYPE not in self.wrapped.Part.__class__.__mro__:
            raise CastException('Failed to cast part to KlingelnbergCycloPalloidHypoidGearSet. Expected: {}.'.format(self.wrapped.Part.__class__.__qualname__))

        return constructor.new(_2087.KlingelnbergCycloPalloidHypoidGearSet)(self.wrapped.Part) if self.wrapped.Part else None

    @property
    def part_of_type_klingelnberg_cyclo_palloid_spiral_bevel_gear(self) -> '_2088.KlingelnbergCycloPalloidSpiralBevelGear':
        '''KlingelnbergCycloPalloidSpiralBevelGear: 'Part' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _2088.KlingelnbergCycloPalloidSpiralBevelGear.TYPE not in self.wrapped.Part.__class__.__mro__:
            raise CastException('Failed to cast part to KlingelnbergCycloPalloidSpiralBevelGear. Expected: {}.'.format(self.wrapped.Part.__class__.__qualname__))

        return constructor.new(_2088.KlingelnbergCycloPalloidSpiralBevelGear)(self.wrapped.Part) if self.wrapped.Part else None

    @property
    def part_of_type_klingelnberg_cyclo_palloid_spiral_bevel_gear_set(self) -> '_2089.KlingelnbergCycloPalloidSpiralBevelGearSet':
        '''KlingelnbergCycloPalloidSpiralBevelGearSet: 'Part' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _2089.KlingelnbergCycloPalloidSpiralBevelGearSet.TYPE not in self.wrapped.Part.__class__.__mro__:
            raise CastException('Failed to cast part to KlingelnbergCycloPalloidSpiralBevelGearSet. Expected: {}.'.format(self.wrapped.Part.__class__.__qualname__))

        return constructor.new(_2089.KlingelnbergCycloPalloidSpiralBevelGearSet)(self.wrapped.Part) if self.wrapped.Part else None

    @property
    def part_of_type_planetary_gear_set(self) -> '_2090.PlanetaryGearSet':
        '''PlanetaryGearSet: 'Part' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _2090.PlanetaryGearSet.TYPE not in self.wrapped.Part.__class__.__mro__:
            raise CastException('Failed to cast part to PlanetaryGearSet. Expected: {}.'.format(self.wrapped.Part.__class__.__qualname__))

        return constructor.new(_2090.PlanetaryGearSet)(self.wrapped.Part) if self.wrapped.Part else None

    @property
    def part_of_type_spiral_bevel_gear(self) -> '_2091.SpiralBevelGear':
        '''SpiralBevelGear: 'Part' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _2091.SpiralBevelGear.TYPE not in self.wrapped.Part.__class__.__mro__:
            raise CastException('Failed to cast part to SpiralBevelGear. Expected: {}.'.format(self.wrapped.Part.__class__.__qualname__))

        return constructor.new(_2091.SpiralBevelGear)(self.wrapped.Part) if self.wrapped.Part else None

    @property
    def part_of_type_spiral_bevel_gear_set(self) -> '_2092.SpiralBevelGearSet':
        '''SpiralBevelGearSet: 'Part' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _2092.SpiralBevelGearSet.TYPE not in self.wrapped.Part.__class__.__mro__:
            raise CastException('Failed to cast part to SpiralBevelGearSet. Expected: {}.'.format(self.wrapped.Part.__class__.__qualname__))

        return constructor.new(_2092.SpiralBevelGearSet)(self.wrapped.Part) if self.wrapped.Part else None

    @property
    def part_of_type_straight_bevel_diff_gear(self) -> '_2093.StraightBevelDiffGear':
        '''StraightBevelDiffGear: 'Part' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _2093.StraightBevelDiffGear.TYPE not in self.wrapped.Part.__class__.__mro__:
            raise CastException('Failed to cast part to StraightBevelDiffGear. Expected: {}.'.format(self.wrapped.Part.__class__.__qualname__))

        return constructor.new(_2093.StraightBevelDiffGear)(self.wrapped.Part) if self.wrapped.Part else None

    @property
    def part_of_type_straight_bevel_diff_gear_set(self) -> '_2094.StraightBevelDiffGearSet':
        '''StraightBevelDiffGearSet: 'Part' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _2094.StraightBevelDiffGearSet.TYPE not in self.wrapped.Part.__class__.__mro__:
            raise CastException('Failed to cast part to StraightBevelDiffGearSet. Expected: {}.'.format(self.wrapped.Part.__class__.__qualname__))

        return constructor.new(_2094.StraightBevelDiffGearSet)(self.wrapped.Part) if self.wrapped.Part else None

    @property
    def part_of_type_straight_bevel_gear(self) -> '_2095.StraightBevelGear':
        '''StraightBevelGear: 'Part' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _2095.StraightBevelGear.TYPE not in self.wrapped.Part.__class__.__mro__:
            raise CastException('Failed to cast part to StraightBevelGear. Expected: {}.'.format(self.wrapped.Part.__class__.__qualname__))

        return constructor.new(_2095.StraightBevelGear)(self.wrapped.Part) if self.wrapped.Part else None

    @property
    def part_of_type_straight_bevel_gear_set(self) -> '_2096.StraightBevelGearSet':
        '''StraightBevelGearSet: 'Part' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _2096.StraightBevelGearSet.TYPE not in self.wrapped.Part.__class__.__mro__:
            raise CastException('Failed to cast part to StraightBevelGearSet. Expected: {}.'.format(self.wrapped.Part.__class__.__qualname__))

        return constructor.new(_2096.StraightBevelGearSet)(self.wrapped.Part) if self.wrapped.Part else None

    @property
    def part_of_type_straight_bevel_planet_gear(self) -> '_2097.StraightBevelPlanetGear':
        '''StraightBevelPlanetGear: 'Part' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _2097.StraightBevelPlanetGear.TYPE not in self.wrapped.Part.__class__.__mro__:
            raise CastException('Failed to cast part to StraightBevelPlanetGear. Expected: {}.'.format(self.wrapped.Part.__class__.__qualname__))

        return constructor.new(_2097.StraightBevelPlanetGear)(self.wrapped.Part) if self.wrapped.Part else None

    @property
    def part_of_type_straight_bevel_sun_gear(self) -> '_2098.StraightBevelSunGear':
        '''StraightBevelSunGear: 'Part' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _2098.StraightBevelSunGear.TYPE not in self.wrapped.Part.__class__.__mro__:
            raise CastException('Failed to cast part to StraightBevelSunGear. Expected: {}.'.format(self.wrapped.Part.__class__.__qualname__))

        return constructor.new(_2098.StraightBevelSunGear)(self.wrapped.Part) if self.wrapped.Part else None

    @property
    def part_of_type_worm_gear(self) -> '_2099.WormGear':
        '''WormGear: 'Part' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _2099.WormGear.TYPE not in self.wrapped.Part.__class__.__mro__:
            raise CastException('Failed to cast part to WormGear. Expected: {}.'.format(self.wrapped.Part.__class__.__qualname__))

        return constructor.new(_2099.WormGear)(self.wrapped.Part) if self.wrapped.Part else None

    @property
    def part_of_type_worm_gear_set(self) -> '_2100.WormGearSet':
        '''WormGearSet: 'Part' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _2100.WormGearSet.TYPE not in self.wrapped.Part.__class__.__mro__:
            raise CastException('Failed to cast part to WormGearSet. Expected: {}.'.format(self.wrapped.Part.__class__.__qualname__))

        return constructor.new(_2100.WormGearSet)(self.wrapped.Part) if self.wrapped.Part else None

    @property
    def part_of_type_zerol_bevel_gear(self) -> '_2101.ZerolBevelGear':
        '''ZerolBevelGear: 'Part' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _2101.ZerolBevelGear.TYPE not in self.wrapped.Part.__class__.__mro__:
            raise CastException('Failed to cast part to ZerolBevelGear. Expected: {}.'.format(self.wrapped.Part.__class__.__qualname__))

        return constructor.new(_2101.ZerolBevelGear)(self.wrapped.Part) if self.wrapped.Part else None

    @property
    def part_of_type_zerol_bevel_gear_set(self) -> '_2102.ZerolBevelGearSet':
        '''ZerolBevelGearSet: 'Part' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _2102.ZerolBevelGearSet.TYPE not in self.wrapped.Part.__class__.__mro__:
            raise CastException('Failed to cast part to ZerolBevelGearSet. Expected: {}.'.format(self.wrapped.Part.__class__.__qualname__))

        return constructor.new(_2102.ZerolBevelGearSet)(self.wrapped.Part) if self.wrapped.Part else None

    @property
    def part_of_type_belt_drive(self) -> '_2120.BeltDrive':
        '''BeltDrive: 'Part' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _2120.BeltDrive.TYPE not in self.wrapped.Part.__class__.__mro__:
            raise CastException('Failed to cast part to BeltDrive. Expected: {}.'.format(self.wrapped.Part.__class__.__qualname__))

        return constructor.new(_2120.BeltDrive)(self.wrapped.Part) if self.wrapped.Part else None

    @property
    def part_of_type_clutch(self) -> '_2122.Clutch':
        '''Clutch: 'Part' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _2122.Clutch.TYPE not in self.wrapped.Part.__class__.__mro__:
            raise CastException('Failed to cast part to Clutch. Expected: {}.'.format(self.wrapped.Part.__class__.__qualname__))

        return constructor.new(_2122.Clutch)(self.wrapped.Part) if self.wrapped.Part else None

    @property
    def part_of_type_clutch_half(self) -> '_2123.ClutchHalf':
        '''ClutchHalf: 'Part' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _2123.ClutchHalf.TYPE not in self.wrapped.Part.__class__.__mro__:
            raise CastException('Failed to cast part to ClutchHalf. Expected: {}.'.format(self.wrapped.Part.__class__.__qualname__))

        return constructor.new(_2123.ClutchHalf)(self.wrapped.Part) if self.wrapped.Part else None

    @property
    def part_of_type_concept_coupling(self) -> '_2125.ConceptCoupling':
        '''ConceptCoupling: 'Part' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _2125.ConceptCoupling.TYPE not in self.wrapped.Part.__class__.__mro__:
            raise CastException('Failed to cast part to ConceptCoupling. Expected: {}.'.format(self.wrapped.Part.__class__.__qualname__))

        return constructor.new(_2125.ConceptCoupling)(self.wrapped.Part) if self.wrapped.Part else None

    @property
    def part_of_type_concept_coupling_half(self) -> '_2126.ConceptCouplingHalf':
        '''ConceptCouplingHalf: 'Part' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _2126.ConceptCouplingHalf.TYPE not in self.wrapped.Part.__class__.__mro__:
            raise CastException('Failed to cast part to ConceptCouplingHalf. Expected: {}.'.format(self.wrapped.Part.__class__.__qualname__))

        return constructor.new(_2126.ConceptCouplingHalf)(self.wrapped.Part) if self.wrapped.Part else None

    @property
    def part_of_type_coupling(self) -> '_2127.Coupling':
        '''Coupling: 'Part' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _2127.Coupling.TYPE not in self.wrapped.Part.__class__.__mro__:
            raise CastException('Failed to cast part to Coupling. Expected: {}.'.format(self.wrapped.Part.__class__.__qualname__))

        return constructor.new(_2127.Coupling)(self.wrapped.Part) if self.wrapped.Part else None

    @property
    def part_of_type_coupling_half(self) -> '_2128.CouplingHalf':
        '''CouplingHalf: 'Part' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _2128.CouplingHalf.TYPE not in self.wrapped.Part.__class__.__mro__:
            raise CastException('Failed to cast part to CouplingHalf. Expected: {}.'.format(self.wrapped.Part.__class__.__qualname__))

        return constructor.new(_2128.CouplingHalf)(self.wrapped.Part) if self.wrapped.Part else None

    @property
    def part_of_type_cvt(self) -> '_2129.CVT':
        '''CVT: 'Part' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _2129.CVT.TYPE not in self.wrapped.Part.__class__.__mro__:
            raise CastException('Failed to cast part to CVT. Expected: {}.'.format(self.wrapped.Part.__class__.__qualname__))

        return constructor.new(_2129.CVT)(self.wrapped.Part) if self.wrapped.Part else None

    @property
    def part_of_type_cvt_pulley(self) -> '_2130.CVTPulley':
        '''CVTPulley: 'Part' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _2130.CVTPulley.TYPE not in self.wrapped.Part.__class__.__mro__:
            raise CastException('Failed to cast part to CVTPulley. Expected: {}.'.format(self.wrapped.Part.__class__.__qualname__))

        return constructor.new(_2130.CVTPulley)(self.wrapped.Part) if self.wrapped.Part else None

    @property
    def part_of_type_part_to_part_shear_coupling(self) -> '_2131.PartToPartShearCoupling':
        '''PartToPartShearCoupling: 'Part' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _2131.PartToPartShearCoupling.TYPE not in self.wrapped.Part.__class__.__mro__:
            raise CastException('Failed to cast part to PartToPartShearCoupling. Expected: {}.'.format(self.wrapped.Part.__class__.__qualname__))

        return constructor.new(_2131.PartToPartShearCoupling)(self.wrapped.Part) if self.wrapped.Part else None

    @property
    def part_of_type_part_to_part_shear_coupling_half(self) -> '_2132.PartToPartShearCouplingHalf':
        '''PartToPartShearCouplingHalf: 'Part' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _2132.PartToPartShearCouplingHalf.TYPE not in self.wrapped.Part.__class__.__mro__:
            raise CastException('Failed to cast part to PartToPartShearCouplingHalf. Expected: {}.'.format(self.wrapped.Part.__class__.__qualname__))

        return constructor.new(_2132.PartToPartShearCouplingHalf)(self.wrapped.Part) if self.wrapped.Part else None

    @property
    def part_of_type_pulley(self) -> '_2133.Pulley':
        '''Pulley: 'Part' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _2133.Pulley.TYPE not in self.wrapped.Part.__class__.__mro__:
            raise CastException('Failed to cast part to Pulley. Expected: {}.'.format(self.wrapped.Part.__class__.__qualname__))

        return constructor.new(_2133.Pulley)(self.wrapped.Part) if self.wrapped.Part else None

    @property
    def part_of_type_rolling_ring(self) -> '_2139.RollingRing':
        '''RollingRing: 'Part' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _2139.RollingRing.TYPE not in self.wrapped.Part.__class__.__mro__:
            raise CastException('Failed to cast part to RollingRing. Expected: {}.'.format(self.wrapped.Part.__class__.__qualname__))

        return constructor.new(_2139.RollingRing)(self.wrapped.Part) if self.wrapped.Part else None

    @property
    def part_of_type_rolling_ring_assembly(self) -> '_2140.RollingRingAssembly':
        '''RollingRingAssembly: 'Part' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _2140.RollingRingAssembly.TYPE not in self.wrapped.Part.__class__.__mro__:
            raise CastException('Failed to cast part to RollingRingAssembly. Expected: {}.'.format(self.wrapped.Part.__class__.__qualname__))

        return constructor.new(_2140.RollingRingAssembly)(self.wrapped.Part) if self.wrapped.Part else None

    @property
    def part_of_type_shaft_hub_connection(self) -> '_2141.ShaftHubConnection':
        '''ShaftHubConnection: 'Part' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _2141.ShaftHubConnection.TYPE not in self.wrapped.Part.__class__.__mro__:
            raise CastException('Failed to cast part to ShaftHubConnection. Expected: {}.'.format(self.wrapped.Part.__class__.__qualname__))

        return constructor.new(_2141.ShaftHubConnection)(self.wrapped.Part) if self.wrapped.Part else None

    @property
    def part_of_type_spring_damper(self) -> '_2142.SpringDamper':
        '''SpringDamper: 'Part' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _2142.SpringDamper.TYPE not in self.wrapped.Part.__class__.__mro__:
            raise CastException('Failed to cast part to SpringDamper. Expected: {}.'.format(self.wrapped.Part.__class__.__qualname__))

        return constructor.new(_2142.SpringDamper)(self.wrapped.Part) if self.wrapped.Part else None

    @property
    def part_of_type_spring_damper_half(self) -> '_2143.SpringDamperHalf':
        '''SpringDamperHalf: 'Part' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _2143.SpringDamperHalf.TYPE not in self.wrapped.Part.__class__.__mro__:
            raise CastException('Failed to cast part to SpringDamperHalf. Expected: {}.'.format(self.wrapped.Part.__class__.__qualname__))

        return constructor.new(_2143.SpringDamperHalf)(self.wrapped.Part) if self.wrapped.Part else None

    @property
    def part_of_type_synchroniser(self) -> '_2144.Synchroniser':
        '''Synchroniser: 'Part' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _2144.Synchroniser.TYPE not in self.wrapped.Part.__class__.__mro__:
            raise CastException('Failed to cast part to Synchroniser. Expected: {}.'.format(self.wrapped.Part.__class__.__qualname__))

        return constructor.new(_2144.Synchroniser)(self.wrapped.Part) if self.wrapped.Part else None

    @property
    def part_of_type_synchroniser_half(self) -> '_2146.SynchroniserHalf':
        '''SynchroniserHalf: 'Part' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _2146.SynchroniserHalf.TYPE not in self.wrapped.Part.__class__.__mro__:
            raise CastException('Failed to cast part to SynchroniserHalf. Expected: {}.'.format(self.wrapped.Part.__class__.__qualname__))

        return constructor.new(_2146.SynchroniserHalf)(self.wrapped.Part) if self.wrapped.Part else None

    @property
    def part_of_type_synchroniser_part(self) -> '_2147.SynchroniserPart':
        '''SynchroniserPart: 'Part' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _2147.SynchroniserPart.TYPE not in self.wrapped.Part.__class__.__mro__:
            raise CastException('Failed to cast part to SynchroniserPart. Expected: {}.'.format(self.wrapped.Part.__class__.__qualname__))

        return constructor.new(_2147.SynchroniserPart)(self.wrapped.Part) if self.wrapped.Part else None

    @property
    def part_of_type_synchroniser_sleeve(self) -> '_2148.SynchroniserSleeve':
        '''SynchroniserSleeve: 'Part' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _2148.SynchroniserSleeve.TYPE not in self.wrapped.Part.__class__.__mro__:
            raise CastException('Failed to cast part to SynchroniserSleeve. Expected: {}.'.format(self.wrapped.Part.__class__.__qualname__))

        return constructor.new(_2148.SynchroniserSleeve)(self.wrapped.Part) if self.wrapped.Part else None

    @property
    def part_of_type_torque_converter(self) -> '_2149.TorqueConverter':
        '''TorqueConverter: 'Part' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _2149.TorqueConverter.TYPE not in self.wrapped.Part.__class__.__mro__:
            raise CastException('Failed to cast part to TorqueConverter. Expected: {}.'.format(self.wrapped.Part.__class__.__qualname__))

        return constructor.new(_2149.TorqueConverter)(self.wrapped.Part) if self.wrapped.Part else None

    @property
    def part_of_type_torque_converter_pump(self) -> '_2150.TorqueConverterPump':
        '''TorqueConverterPump: 'Part' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _2150.TorqueConverterPump.TYPE not in self.wrapped.Part.__class__.__mro__:
            raise CastException('Failed to cast part to TorqueConverterPump. Expected: {}.'.format(self.wrapped.Part.__class__.__qualname__))

        return constructor.new(_2150.TorqueConverterPump)(self.wrapped.Part) if self.wrapped.Part else None

    @property
    def part_of_type_torque_converter_turbine(self) -> '_2152.TorqueConverterTurbine':
        '''TorqueConverterTurbine: 'Part' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _2152.TorqueConverterTurbine.TYPE not in self.wrapped.Part.__class__.__mro__:
            raise CastException('Failed to cast part to TorqueConverterTurbine. Expected: {}.'.format(self.wrapped.Part.__class__.__qualname__))

        return constructor.new(_2152.TorqueConverterTurbine)(self.wrapped.Part) if self.wrapped.Part else None

    @property
    def part_load_cases(self) -> 'List[_6167.PartLoadCase]':
        '''List[PartLoadCase]: 'PartLoadCases' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.PartLoadCases, constructor.new(_6167.PartLoadCase))
        return value
