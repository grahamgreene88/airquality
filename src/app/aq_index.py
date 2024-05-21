import math

def calculate_AQHI(no2, o3, pm25):
    AQHI = round((10/10.4)*100*(math.exp(0.000871*no2)-1 + math.exp(0.000537*o3)-1 + math.exp(0.000487*pm25)-1), 0)
    return AQHI