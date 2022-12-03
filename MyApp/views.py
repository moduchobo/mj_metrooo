from django.core.exceptions import *
from rest_framework import status
from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework.decorators import api_view
from .models import *
from .serializers import *
from rest_framework.views import APIView


# Test View
class UserDataAPI(APIView):
    def get(self, request):
        queryset = User.objects.all()
        print(queryset)
        serializer = UserSerializer(queryset, many=True)
        return Response(serializer.data)

class SingleUserDataAPI(APIView):
    def get(self, request, userid):
        queryset = User.objects.all().filter(user__exact=userid)
        print(queryset)
        serializer = UserSerializer(queryset, many=False)
        return Response(serializer.data)


class ScheduleDataAPI(APIView):
    def get(self, request):
        queryset = Schedule.objects.all()
        print(queryset)
        serializer = ScheduleSerializer(queryset,many=True)
        return Response(serializer.data)
# Actual View
class StationDataAPI(APIView):
    def get(self, request):
        queryset = Station.objects.all()
        print(queryset)
        serializer = StationSerializer(queryset, many=True)
        return Response(serializer.data)

# User의 Schedule을 관리한다.
class UserScheduleAPI(APIView):
    def get(self, request, userid):
        queryset = Schedule.objects.all().filter(user__exact=userid)
        print(queryset.values)
        serializer = UserScheduleSerializer(queryset, many=True)
        return Response(serializer.data)

# User의 FavStation을 관리한다.
class UserStationAPI(APIView):
    def get(self, request, userid):
        queryset = FavStation.objects.all().filter(user__exact=userid)
        print(queryset.values)
        serializer = UserStationSerializer(queryset, many=True)
        return Response(serializer.data)

class UserRouteAPI(APIView):
    def get(self, request, userid):
        queryset = FavRoute.objects.all().filter(user__exact=userid)
        print(queryset.values)
        serializer = UserRouteAPI(queryset, many=True)
        return Response(serializer.data)





def create_schedule(request, user_id):
    pass

def delete_schedule(request, user_id, schedule_id):
    pass
