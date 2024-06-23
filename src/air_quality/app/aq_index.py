import math


def calculate_AQHI(no2, o3, pm25):
    """Calculates the Air quality health index value based on the concentration of no2, o3 and pm25.

    Args:
        no2 (float64): no2 concentration.
        o3 (float64): o3 concentration.
        pm25 (float64): pm25 concentration.

    Returns:
        float64: air quality health index value between 1-10+
    """
    # Input validation for pollutant values
    if no2 < 0 or o3 < 0 or pm25 < 0:
        raise ValueError("The pollutant concentration values cannot be lower than 0.")

    if any(not isinstance(val, (int, float)) for val in (no2, o3, pm25)):
        raise TypeError("Input pollutant values must be numeric.")

    AQHI = round(
        (10 / 10.4)
        * 100
        * (
            math.exp(0.000871 * no2)
            - 1
            + math.exp(0.000537 * o3)
            - 1
            + math.exp(0.000487 * pm25)
            - 1
        ),
        0,
    )
    return AQHI
