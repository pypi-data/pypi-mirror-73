from datetime import datetime
from typing import List, Dict

from kisters.water.time_series.core import TimeSeriesMetadata
from kisters.water.time_series.core.time_series import EnsembleMemberInfo, TimeSeries


class TimeSeriesDecorator(TimeSeries):
    def __init__(self, forward: TimeSeries):
        super().__init__(forward.store, forward.columns)
        self._forward = forward

    @property
    def path(self) -> str:
        return self._forward.path

    @property
    def metadata(self) -> TimeSeriesMetadata:
        return self._forward.metadata

    def coverage_from(
        self, t0: datetime = None, dispatch_info: str = None, member: str = None, **kwargs
    ) -> datetime:
        return self._forward.coverage_from(t0, dispatch_info, member, **kwargs)

    def coverage_until(
        self, t0: datetime = None, dispatch_info: str = None, member: str = None, **kwargs
    ) -> datetime:
        return self._forward.coverage_until(t0, dispatch_info, member, **kwargs)

    def coverage(
        self, t0: datetime = None, dispatch_info: str = None, member: str = None, **kwargs
    ) -> Dict[str, datetime]:
        return self._forward.coverage(t0, dispatch_info, member, **kwargs)

    def ensemble_members(
        self, t0_start: datetime = None, t0_end: datetime = None, **kwargs
    ) -> List[EnsembleMemberInfo]:
        return self._forward.ensemble_members(t0_start, t0_end, **kwargs)
