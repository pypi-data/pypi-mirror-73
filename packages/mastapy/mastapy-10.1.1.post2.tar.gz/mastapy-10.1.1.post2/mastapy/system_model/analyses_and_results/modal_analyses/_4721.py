﻿'''_4721.py

CoaxialConnectionModalAnalysis
'''


from mastapy.system_model.connections_and_sockets import _1833
from mastapy._internal import constructor
from mastapy.system_model.analyses_and_results.static_loads import _6070
from mastapy.system_model.analyses_and_results.system_deflections import _2229
from mastapy.system_model.analyses_and_results.modal_analyses import _4796
from mastapy._internal.python_net import python_net_import

_COAXIAL_CONNECTION_MODAL_ANALYSIS = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.ModalAnalyses', 'CoaxialConnectionModalAnalysis')


__docformat__ = 'restructuredtext en'
__all__ = ('CoaxialConnectionModalAnalysis',)


class CoaxialConnectionModalAnalysis(_4796.ShaftToMountableComponentConnectionModalAnalysis):
    '''CoaxialConnectionModalAnalysis

    This is a mastapy class.
    '''

    TYPE = _COAXIAL_CONNECTION_MODAL_ANALYSIS

    __hash__ = None

    def __init__(self, instance_to_wrap: 'CoaxialConnectionModalAnalysis.TYPE'):
        super().__init__(instance_to_wrap)

    @property
    def connection_design(self) -> '_1833.CoaxialConnection':
        '''CoaxialConnection: 'ConnectionDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_1833.CoaxialConnection)(self.wrapped.ConnectionDesign) if self.wrapped.ConnectionDesign else None

    @property
    def connection_load_case(self) -> '_6070.CoaxialConnectionLoadCase':
        '''CoaxialConnectionLoadCase: 'ConnectionLoadCase' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_6070.CoaxialConnectionLoadCase)(self.wrapped.ConnectionLoadCase) if self.wrapped.ConnectionLoadCase else None

    @property
    def system_deflection_results(self) -> '_2229.CoaxialConnectionSystemDeflection':
        '''CoaxialConnectionSystemDeflection: 'SystemDeflectionResults' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_2229.CoaxialConnectionSystemDeflection)(self.wrapped.SystemDeflectionResults) if self.wrapped.SystemDeflectionResults else None
