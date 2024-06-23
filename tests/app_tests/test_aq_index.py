import pytest
from src.air_quality.app.aq_index import calculate_AQHI


def test_calculate_AQHI():
    """Test ensures function can properly handle wide range of values and incorrect inputs."""
    # normal values
    assert calculate_AQHI(2, 38, 10) == 3
    # extreme values
    assert calculate_AQHI(24, 75, 54) == 9
    # zero values
    assert calculate_AQHI(0, 0, 0) == 0
    # negative values - should raise ValueError
    with pytest.raises(ValueError):
        calculate_AQHI(-4, -9, -12)
    # non-numeric inputs (should raise TypeError)
    with pytest.raises(TypeError):
        calculate_AQHI("no2", "o3", "pm25")
