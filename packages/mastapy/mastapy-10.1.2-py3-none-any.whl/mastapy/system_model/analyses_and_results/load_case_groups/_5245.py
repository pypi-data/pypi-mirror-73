'''_5245.py

ClutchEngagementStatus
'''


from mastapy.system_model.analyses_and_results.load_case_groups import _5249
from mastapy.system_model.connections_and_sockets.couplings import _1903
from mastapy._internal.python_net import python_net_import

_CLUTCH_ENGAGEMENT_STATUS = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.LoadCaseGroups', 'ClutchEngagementStatus')


__docformat__ = 'restructuredtext en'
__all__ = ('ClutchEngagementStatus',)


class ClutchEngagementStatus(_5249.GenericClutchEngagementStatus['_1903.ClutchConnection']):
    '''ClutchEngagementStatus

    This is a mastapy class.
    '''

    TYPE = _CLUTCH_ENGAGEMENT_STATUS

    __hash__ = None

    def __init__(self, instance_to_wrap: 'ClutchEngagementStatus.TYPE'):
        super().__init__(instance_to_wrap)
