from django.shortcuts import render
from rest_framework.views import APIView

from app.models import Plants
from app.serializer import PlantsSerializer
from rest_framework.response import Response


# Create your views here.
class PlantList(APIView):
    def get(self, request, format=None):
        plants = Plants.objects.all()
        serializers = PlantsSerializer(plants, many=True)
        return Response(serializers.data) 
    def retrieve(self, request, *args,**kwargs):
        # params = kwargs
        # params_list = map(int, list(params['pk'].split('-')))
        alt = self.kwargs.get('elevation', None)
        temp = self.kwargs.get('temperature', None)    
        plants = Plants.objects.filter(temperature__range = (temp-5,temp+5), elevation__range = (alt-100, alt+100))    
        # plants = Plants.objects.filter(temperature__range = (params_list[0]-5,params_list[0]+5), elevation__range = (params_list[1]-100, params_list[1]+100))
        serializers = PlantsSerializer(plants, many=True)
        return Response(serializers.data)                 
# class PlantRecc(APIView):
#         def get(self, request, format=None):
#           all_plants = Plants.objects.all()
#           serializers = PlantsSerializer(all_plants, many=True)
#           return Response(serializers.data)         