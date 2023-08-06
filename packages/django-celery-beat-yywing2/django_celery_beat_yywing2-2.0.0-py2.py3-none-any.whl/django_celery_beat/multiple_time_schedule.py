"""multiple time schedule Implementation."""

from datetime import timedelta
from celery import schedules
from .utils import subtract_time, NEVER_CHECK_TIMEOUT


class multipletime(schedules.BaseSchedule):
    """multiple time schedule."""

    def __init__(self, timezone, times,
                 model=None, nowfun=None, app=None):
        """Initialize multiple time."""
        self.timezone = timezone
        times.sort()
        self.times = times
        # save for next_run_time
        self._next_time = 0
        super(multipletime, self).__init__(nowfun=nowfun, app=app)

    def _get_next_time(self, times, now_time):
        if len(times) > 1:
            return subtract_time(times[1], now_time)
        elif len(times) == 1:
            return subtract_time(self.times[0], now_time) + timedelta(hours=24)
        # times=0
        elif len(self.times) > 1:
            return subtract_time(self.times[1], now_time) + timedelta(hours=24)
        else:
            # self.times=1
            return subtract_time(self.times[0], now_time) + timedelta(hours=48)

    def remaining_estimate(self, last_run_at):
        times = []
        for i in range(len(self.times)):
            if self.times[i] >= last_run_at.time():
                times = self.times[i:]
                break
        now_time = self.now().astimezone(self.timezone).time()
        if times:
            r = subtract_time(times[0], now_time)
        else:
            r = subtract_time(self.times[0], now_time) + timedelta(hours=24)
        self._next_time = self._get_next_time(times, now_time)
        return r

    def is_due(self, last_run_at):
        if len(self.times) == 0:
            return schedules.schedstate(is_due=False, next=NEVER_CHECK_TIMEOUT)

        last_run_at = last_run_at.astimezone(self.timezone)
        # will update self._next_time
        rem_delta = self.remaining_estimate(last_run_at)
        remaining_s = max(rem_delta.total_seconds(), 0)
        if remaining_s == 0:
            return schedules.schedstate(
                is_due=True, next=self._next_time.total_seconds()
            )
        return schedules.schedstate(is_due=False, next=remaining_s)

    def __repr__(self):
        return '<multipletime: {} {}>'.format(self.timezone, self.times)

    def __eq__(self, other):
        if isinstance(other, multipletime):
            return self.times == other.times and \
                self.timezone == other.timezone
        return False

    def __ne__(self, other):
        return not self.__eq__(other)

    def __reduce__(self):
        return self.__class__, (self.timezone, self.times)
