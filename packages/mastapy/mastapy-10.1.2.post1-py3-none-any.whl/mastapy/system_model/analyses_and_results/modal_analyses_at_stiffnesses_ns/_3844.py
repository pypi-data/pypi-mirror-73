'''_3844.py

TorqueConverterModalAnalysesAtStiffnesses
'''


from mastapy.system_model.part_model.couplings import _2149
from mastapy._internal import constructor
from mastapy.system_model.analyses_and_results.static_loads import _6212
from mastapy.system_model.analyses_and_results.modal_analyses_at_stiffnesses_ns import _3768
from mastapy._internal.python_net import python_net_import

_TORQUE_CONVERTER_MODAL_ANALYSES_AT_STIFFNESSES = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.ModalAnalysesAtStiffnessesNS', 'TorqueConverterModalAnalysesAtStiffnesses')


__docformat__ = 'restructuredtext en'
__all__ = ('TorqueConverterModalAnalysesAtStiffnesses',)


class TorqueConverterModalAnalysesAtStiffnesses(_3768.CouplingModalAnalysesAtStiffnesses):
    '''TorqueConverterModalAnalysesAtStiffnesses

    This is a mastapy class.
    '''

    TYPE = _TORQUE_CONVERTER_MODAL_ANALYSES_AT_STIFFNESSES

    __hash__ = None

    def __init__(self, instance_to_wrap: 'TorqueConverterModalAnalysesAtStiffnesses.TYPE'):
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
