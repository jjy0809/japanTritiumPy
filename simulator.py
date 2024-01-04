import math
import sys
import random
import folium

m = folium.Map(location = [37.5,127], zoom_start = 5, tiles = 'OpenStreetMap')

DUMPING_POINT = [37.4279, 141.0444] # 오염수 방류 지점 위도, 경도
AMERICA_LONG = 360 - 126 # 아메리카(미국) 대륙 시작점 경도
START_TRITIUM = 2600 # 방류된 오염수의 삼중수소 농도 (Bq/L)
KILO_KNOT = 1.852 # 1 kn = 1.852 km/h

water_point = DUMPING_POINT.copy() # 현재 오염수의 위치 (가장 최초로 방류된 오염수의 (가상의)물분자의 위도와 경도)
water_tritium = START_TRITIUM #오염수가 지닌 삼중수소 농도
day = 0 # 방류 후 지난 시간 (일)
speed = 1 # 해류 속도
day_per_speed = speed * 24 # 하루동안 이동하는 해류의 속도 (km/d)

# 경도 1도 = 111.320 * cos(위도) km
# 위도 1도 = 110.574 km
# 1L = 0.001m^3

while water_point[1] <= AMERICA_LONG: # 쿠로시오 해류 & 북태평양 해류
    if water_point[1] < 160:
        speed = float(str(random.uniform(3*KILO_KNOT, 5*KILO_KNOT))[:6]) # 해류 속도 3~5kn 사이 실수로 랜덤하게 설정 (쿠로시오 해류)
    else:
        speed = float(str(random.uniform(0.5*KILO_KNOT, 1.5*KILO_KNOT))[:6]) # 해류 속도 0.5~1.5kn 사이 실수로 랜덤하게 설정 (북태평양 해류)
    day += 1
    day_per_speed = speed * 24
    water_point[1] += day_per_speed / 111.320 / math.cos(water_point[0]) # 오염수 이동
    water_tritium = START_TRITIUM / (0.1 * 10 * (water_point[1] - DUMPING_POINT[1]) * 111.320 * math.cos(DUMPING_POINT[0])) # 삼중수소 농도 계산
    col = ''
    if water_tritium > 10:
        col = 'red'
    elif water_tritium > 1:
        col = 'orange'
    elif water_tritium > 0.5:
        col = 'beige'
    elif water_tritium > 0.25:
        col = 'green'
    else:
        col = 'blue'
    folium.Marker(water_point, popup = '삼중수소: {} / {}일 후'.format(water_tritium, day), icon = folium.Icon(icon = 'info-sign', color = col)).add_to(m) # 지도에 마커 표시
    
while water_point[0] >= 20: # 캘리포니아 해류
    speed = float(str(random.uniform(0.4*KILO_KNOT, 0.8*KILO_KNOT))[:6]) # 해류 속도 0.4~0.8kn 사이 실수로 랜덤하게 설정
    day += 1
    day_per_speed = speed * 24
    water_point[0] -= day_per_speed / 110.574 # 오염수 이동
    water_tritium = START_TRITIUM / ((0.1 * 10 * (water_point[1] - DUMPING_POINT[1]) * 111.320 * math.cos(DUMPING_POINT[0])) + ((DUMPING_POINT[0] - water_point[0]) * 110.574) * 0.001 * 10) # 삼중수소 농도 계산
    col = ''
    if water_tritium > 10:
        col = 'red'
    elif water_tritium > 1:
        col = 'orange'
    elif water_tritium > 0.5:
        col = 'beige'
    elif water_tritium > 0.25:
        col = 'green'
    else:
        col = 'blue'
    folium.Marker(water_point, popup = '삼중수소: {} / {}일 후'.format(water_tritium, day), icon = folium.Icon(icon = 'info-sign', color = col)).add_to(m) # 지도에 마커 표시


tmp = (0.1 * 10 * (water_point[1] - DUMPING_POINT[1]) * 111.320 * math.cos(DUMPING_POINT[0]))
while water_point[1] >= 128: # 북적도 해류
    speed = float(str(random.uniform(0.5*KILO_KNOT, 1.5*KILO_KNOT))[:6]) # 해류 속도 0.5~1.5kn 사이 실수로 랜덤하게 설정 (쿠로시오 해류)
    day += 1
    day_per_speed = speed * 24
    water_point[1] -= day_per_speed / 111.320 / math.cos(water_point[0]) # 오염수 이동
    water_tritium = START_TRITIUM / (tmp + (((DUMPING_POINT[0] - water_point[0]) * 110.574) * 0.1 * 10) + (((AMERICA_LONG - water_point[1]) * 111.320 * math.cos(water_point[0])) * 0.1 * 10)) # 삼중수소 농도 계산
    col = ''
    if water_tritium > 10:
        col = 'red'
    elif water_tritium > 1:
        col = 'orange'
    elif water_tritium > 0.5:
        col = 'beige'
    elif water_tritium > 0.25:
        col = 'green'
    else:
        col = 'blue'
    folium.Marker(water_point, popup = '삼중수소: {} / {}일 후'.format(water_tritium, day), icon = folium.Icon(icon = 'info-sign', color = col)).add_to(m) # 지도에 마커 표시

m.save('./res.html')
