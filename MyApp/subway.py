#--------------------------데이터 불러오기와서 딕셔너리로 그래프그리기-------------------------------------
import csv 
from pprint import pprint as pp

station = {}

f1 = open('./stations_node.csv', 'r', encoding='utf-8-sig')
csv_read_node = csv.DictReader(f1)  
for col in csv_read_node: 
    snum = col['역번호'] # print(type(col['역번호'])) str
    del col['역번호']
    station.update({snum:col})
    station[snum].update({'근처역':{}})
f1.close()
f2 = open('./stations.csv', 'r', encoding='utf-8-sig')
csv_read_node = csv.DictReader(f2)  
for col in csv_read_node: 
    startsnum = col['출발역']
    del col['출발역']
    endsnum = col['도착역']
    del col['도착역']
    station[startsnum]['근처역'].update({endsnum:col})
    station[endsnum]['근처역'].update({startsnum:col})
pp(station)                     #------------------------------------------------------------그래프 및 역 정리
f2.close()


#--------------------------데이터 불러오기 끝-------------------------------------

#--------------------------데이터 저장 및 클래스 작업 + 호선-------------------------------------
class S:
    def __init__(self, name, args):
        self.__s_num = name              #역번호
        self.__s_name = args['역이름']
        self.__latitude = args['위도']
        self.__longitude = args['경도']
        self.__address = args['주소']
        self.__lineNumber = [args['호선']]
        if args['환승(없다면0)']!='0':
            self.__lineNumber.append(args['환승(없다면0)'])
        self.__nearStation = args['근처역']

    @property
    def s_num(self):
        return self.__s_num

    @property
    def s_name(self):
        return self.__s_name

    @property
    def latitude(self):
        return self.__latitude

    @property
    def longitude(self):
        return self.__longitude

    @property
    def address(self):
        return self.__address

    @property
    def lineNumber(self):
        return self.__lineNumber

    @property
    def nearStation(self):
        return self.__nearStation

    def sprint(self):
        print(self.s_num)
        print(self.s_name)
        print(self.latitude)
        print(self.longitude)
        print(self.address)
        print(self.lineNumber)
        print(self.nearStation)

    def __str__(self):
        return self.s_name


#--------------------------클래스 딕셔너리 station_class_dict -------------------------------------
station_class_dict = {}
for i,j in station.items():
    station_class_dict.update({i:S(i,j)})

# print(station_class_dict)
# station_class_dict['101'].sprint()
# print(station_class_dict['101'].lineNumber)
# print(station_class_dict['904'].lineNumber)

#--------------------------호선 딕셔너리 끝-------------------------------------
station_lineNumber_dict = {}
for i in range(1,10):
    station_lineNumber_dict.update({str(i):[]})
for s_num, s_class in station_class_dict.items():
    if len(s_class.lineNumber)==2:
        station_lineNumber_dict[s_class.lineNumber[1]].append(s_num)
    station_lineNumber_dict[s_class.lineNumber[0]].append(s_num)
# print(station_lineNumber_dict)

#--------------------------데이터 저장 및 클래스 작업 + 호선 끝-------------------------------------

#--------------------------다익스트라-------------------------------------

import heapq  # 우선순위 큐 구현을 위함
import copy

def d(graph, start, end, *args):
    queue = [start, args, end]
    result = []
    for i in range(len(args)+1):
        result.append(dijkstra(graph, start, end))
    return result


def dijkstra(graph, dmt_num, start, end): # distance+money+time dmt_num => str 문자임
    distances = {node: {'min_dis':float('inf'), 'route':[]} for node in graph}  # start로 부터의 최소 거리값 구해야 하므로 가장 큰 값인 무한대inf를 넣어두고 각 루트를 표현한 route에 출발역인 start를 넣는다.
    distances[start]['min_dis'] = 0  # 시작 값은 0이어야 함
    queue = []
    heapq.heappush(queue, [distances[start]['min_dis'], start, []])  # 시작 노드부터 탐색 시작 하기 위함. #[시작 0, 시작노드이름, 시작 루트]
    while queue:  # queue에 남아 있는 노드가 없으면 끝
        current_distance, current_destination, current_route = heapq.heappop(queue)  # 탐색 할 노드, 거리를 가져옴.
        distances[current_destination]['route'] = copy.deepcopy(current_route)
        distances[current_destination]['route'].append(current_destination)
        if current_destination == end: # 만약 여기서 current_destination이 목적지라면 break 거기까지가 목적지임 
            break
        if distances[current_destination]['min_dis'] < current_distance:  # 기존에 있는 거리보다 길다면, 볼 필요도 없음
            continue

        for new_destination, new_distanceitem in graph[current_destination]['근처역'].items():
            new_distance = new_distanceitem[dmt_num]
            distance = current_distance + int(new_distance)  # 해당 노드를 거쳐 갈 때 거리
            if distance < distances[new_destination]['min_dis']:  # 알고 있는 거리 보다 작으면 갱신
                distances[new_destination]['min_dis'] = distance
                heapq.heappush(queue, [distance, new_destination, distances[current_destination]['route']])  # 다음 인접 거리를 계산 하기 위해 큐에 삽입 - 방금 계산한 거리와 새로운 목적지
    return distances[end] # start부터 end까지 걸리는 숫자와 길(루트) 반환 {'min_dis': 1540, 'route': ['101', '101', '123', '305', '306', '307', '401']}

print(dijkstra(station, '비용(원)', '104', '116'))
print(dijkstra(station, '거리(미터)', '104', '116'))
print(dijkstra(station, '시간(초)', '104', '116'))

#--------------------------환승(정신나갈것같애)-------------------------------------
def transfer(graph,start,end):
    isequal_hosun, hosun = isEqual_Hosun(graph, start, end)
    
    if isequal_hosun: #일자 노선을 찾아라
        return map(graph, isTwoHosun_Equal(graph,start,end), start, end)

    else: #3개중 가장 환승이 적은 노선
        num1 = hosun_count(graph, dijkstra(station, '비용(원)', start, end)['route'])
        num2 = hosun_count(graph, dijkstra(station, '거리(미터)', start, end)['route'])
        num3 = hosun_count(graph, dijkstra(station, '시간(초)', start, end)['route'])
        if max(num1, num2, num3)==num1:
            return dijkstra(station, '비용(원)', start, end)['route']
        elif max(num1, num2, num3)==num2:
            return dijkstra(station, '거리(미터)', start, end)['route']
        elif max(num1, num2, num3)==num3:
            return dijkstra(station, '시간(초)', start, end)['route']


def map(graph, hosun, start, end): #출발점부터 도착점까지 일자인 맵 구하는 함수
    graph_map = [start]
    graph_maps = []
    if len(hosun)==2: #이중노선도라면 3개짜리가 있고 4개짜리가 있다
        current_hosun = 0
        if ('1'and'6') in hosun: # 4개짜리
            current_hosun = '1'
            hosun.remove('1')
        elif ('1') in hosun: # 3개짜리
            current_hosun = '1'
            hosun.remove('1')
        elif ('6') in hosun: # 3개짜리
            current_hosun = '6'
            hosun.remove('6')
        hcount = 0 #이중 노선도 여러 노선 구하기
        station = {'station_name':start, 'station_count':0}
        key = graph[station['station_name']]['근처역'].keys()
        for s in key:
            station['station_name'] = s
            station['station_count'] += 1
            graph_map.append(station['station_name'])
            
            if isEqual_station_hosun(graph, s, current_hosun):
                find_map(graph, graph_map, station, end, current_hosun)
                if station['station_name'] == end:
                    graph_maps.append(graph_map)
                    graph_map = [start]
                    station = {'station_name':start, 'station_count':0}
                    hcount += 1
                    if hcount >= 2:
                        current_hosun = hosun[0]
                    continue
            else:
                station['station_name'] = graph_map[-2]
                graph_map.pop()
                station['station_count'] -= 1
            for i in range(station['station_count']):
                graph_map.pop()
                station['station_count'] -=1
        result_list = []
        for m in graph_maps:
            result_list.append([evaluate(graph,'시간(초)',m),m])
        result_list.sort(key=lambda x:x[0])
        return result_list[0][1]
    else:
        station = {'station_name':start, 'station_count':0}
        key = graph[station['station_name']]['근처역'].keys()
        for s in key:
            station['station_name'] = s
            station['station_count'] += 1
            graph_map.append(station['station_name'])
            
            if isEqual_station_hosun(graph, s, hosun):
                find_map(graph, graph_map, station, end, hosun)
                if station['station_name'] == end:
                    break
            else:
                station['station_name'] = graph_map[-2]
                graph_map.pop()
                station['station_count'] -= 1
            for i in range(station['station_count']):
                graph_map.pop()
                station['station_count'] -=1
        return graph_map


def find_map(graph, graph_map, station, end, hosun):
    key=list(graph[station['station_name']]['근처역'].keys())
    key.remove(graph_map[-2])
    for s in key:
        station['station_name'] = s
        station['station_count'] += 1
        graph_map.append(station['station_name'])
        if isEqual_station_hosun(graph, s, hosun):
            if station['station_name'] == end:
                break
            find_map(graph, graph_map, station, end, hosun)
        else:
            station['station_name'] = graph_map[-2]
            graph_map.pop()
            station['station_count'] -= 1


def hosun_count(graph, args): #리스트에 환승 개수 구하는 함수
    count = 0
    r1=0
    r2=0
    hosun=0
    isequal_hosun=False
    for r in args:
        if r1==0 and r2==0:
            r1 = r
        elif r2==0:
            r2 = r
            isequal_hosun, hosun= isEqual_Hosun(graph, r1, r2)
        elif r1!=0 and r2!=0:
            r1 = r2
            r2 = r
            if isEqual_station_hosun(graph, r, hosun):
                pass
            else:
                count += 1
                isequal_hosun, hosun= isEqual_Hosun(graph, r1, r2)
    return count


def isEqual_station_hosun(graph, station, hosun):
    s1 = graph[station]['호선']
    s2 = graph[station]['환승(없다면0)']
    if s1 == hosun:
        return True
    elif s2 == hosun:
        return True
    else:
        return False


def isEqual_Hosun(graph, station1, station2):
    isequal_hosun = False
    hosun = 0
    s1 = graph[station1]['호선']
    s2 = graph[station1]['환승(없다면0)']
    e1 = graph[station2]['호선']
    e2 = graph[station2]['환승(없다면0)']

    if s2==0 and e2== 0:
        isequal_hosun = s1 == s2
        if isequal_hosun:
            hosun = s1
    elif s2==0:
        if s1 == e1:
            isequal_hosun = True
            hosun = s1
        elif s1 == e2:
            isequal_hosun = True
            hosun = s1
    elif e2==0:
        if s1 == e1:
            isequal_hosun = True
            hosun = e1
        elif s2 == e1:
            isequal_hosun = True
            hosun = e1
    else:
        if s1 == e1:
            isequal_hosun = True
            hosun = s1
        elif s2 == e1:
            isequal_hosun = True
            hosun = s2
        elif s1 == e2:
            isequal_hosun = True
            hosun = s1
        elif s2 == e2:
            isequal_hosun = True
            hosun = s2
    return isequal_hosun, hosun

def isTwoHosun_Equal(graph, station1, station2):
    isequal_hosun = False
    hosun = 0
    s1 = graph[station1]['호선']
    s2 = graph[station1]['환승(없다면0)']
    e1 = graph[station2]['호선']
    e2 = graph[station2]['환승(없다면0)']
    if s1=='0' or s2=='0' or e1=='0' or e2=='0':
        isequal_hosun, hosun = isEqual_Hosun(graph, station1, station2)
        return hosun
    else:
        if (s1==e1 and s2==e2) or (s1==e2 and s2==e1):
            return [s1, s2]
        else:
            isequal_hosun, hosun = isEqual_Hosun(graph, station1, station2)
            return hosun
# print(isTwoHosun_Equal(station,'102','103'))
# print(isTwoHosun_Equal(station,'122','109'))
# print(len(isTwoHosun_Equal(station,'122','109')))
# print(('1'and'6') in isTwoHosun_Equal(station,'122','109'))
#--------------------------검증-------------------------------------
def evaluate(graph,dmt,args):  #검증
    i1=0
    i2=0
    num=0
    for i in args: 
        if i1==0 and i2==0:
            i1 = i
        elif i2==0:
            i2 = i
            num += int(graph[i1]['근처역'][i2][dmt])
        elif i1!=0 and i2!=0:
            i1 = i2
            i2 = i
            num += int(graph[i1]['근처역'][i2][dmt])
    return num
    
print(evaluate(station,'비용(원)',['104', '401', '307', '402', '403', '404', '405', '406', '407', '115', '116']))
print(evaluate(station,'거리(미터)',['104', '401', '307', '402', '403', '404', '405', '406', '605', '606', '116']))
print(evaluate(station,'시간(초)',['104', '401', '307', '402', '403', '404', '405', '406', '407', '115', '116']))
print(transfer(station,'109','122'))
print(transfer(station,'107','123'))
print(transfer(station,'104','115'))
print(transfer(station,'109','122'))
print(transfer(station,'116','121'))
print(transfer(station,'112','804'))
