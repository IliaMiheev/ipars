import time
import pytest
from ipars import TimerManager


def test_getWorkTime_seconds():
    timer = TimerManager()
    timer.start()
    time.sleep(0.1)
    timer.end()
    result = timer.getWorkTime('seconds')
    assert 0.05 < result < 0.5


def test_getWorkTime_minutes():
    timer = TimerManager()
    timer.start()
    time.sleep(0.1)
    timer.end()
    result = timer.getWorkTime('minutes')
    assert result < 0.01


def test_getWorkTime_hours():
    timer = TimerManager()
    timer.start()
    time.sleep(0.1)
    timer.end()
    result = timer.getWorkTime('hours')
    assert result < 0.001


def test_getWorkTime_ndigits():
    timer = TimerManager()
    timer.start()
    time.sleep(0.1)
    timer.end()
    result = timer.getWorkTime('seconds', ndigits=2)
    assert isinstance(result, float)
    assert len(str(result).split('.')[-1]) <= 2


def test_getWorkTime_returns_float():
    timer = TimerManager()
    timer.start()
    timer.end()
    result = timer.getWorkTime()
    assert isinstance(result, float)


def test_raises_without_start():
    timer = TimerManager()
    with pytest.raises(ValueError, match='"start"'):
        timer.getWorkTime()


def test_raises_without_end():
    timer = TimerManager()
    timer.start()
    with pytest.raises(ValueError, match='"end"'):
        timer.getWorkTime()


def test_raises_invalid_format():
    timer = TimerManager()
    timer.start()
    timer.end()
    with pytest.raises(ValueError, match='milliseconds'):
        timer.getWorkTime('milliseconds')
