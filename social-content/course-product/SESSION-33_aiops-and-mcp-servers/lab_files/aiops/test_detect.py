from detect import anomalies
import random
random.seed(3)
calm = [10 + random.gauss(0, 1) for _ in range(60)]

def test_calm_series_is_quiet():
    assert anomalies(calm) == []

def test_single_spike_does_not_alarm():
    v = calm[:40] + [50] + calm[41:]
    assert anomalies(v) == []

def test_sustained_jump_alarms():
    v = calm[:40] + [30, 31, 32, 33, 34] + calm[45:]
    assert anomalies(v)

def test_flat_series_is_ignored():
    assert anomalies([5.0] * 60) == []

def test_flat_then_jump_is_ignored_the_known_blind_spot():
    assert anomalies([0.0] * 40 + [9.0] * 20) == []

def test_new_service_with_short_history_is_silent():
    assert anomalies([1, 2, 3, 100, 100, 100]) == []

def test_a_slow_ramp_hides_in_the_window():
    ramp = [10 + 0.2 * i for i in range(120)]
    assert anomalies(ramp) == []
