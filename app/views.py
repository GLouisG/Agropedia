from django.shortcuts import render
from rest_framework.views import APIView

from app.models import Plants
from app.serializer import PlantsSerializer
from rest_framework.response import Response
from django.views.decorators.clickjacking import xframe_options_exempt

# Create your views here.
class PlantList(APIView):
    serializer_class = PlantsSerializer
    @xframe_options_exempt
    def get(self, request, format=None):
        plants = Plants.objects.all()
        serializers = PlantsSerializer(plants, many=True)
        return Response(serializers.data) 
class PlantRecc(APIView):
    serializer_class = PlantsSerializer
    @xframe_options_exempt
    def get(self, request, *args,**kwargs):
        # params = kwargs
        # params_list = map(int, list(params['pk'].split('-')))
        alt = self.kwargs.get('alt', None)
        temp = self.kwargs.get('temp', None)    
        plants = Plants.objects.filter(temperature__range = (temp-5,temp+5), elevation__range = (alt-450, alt+450))    
        # plants = Plants.objects.filter(temperature__range = (params_list[0]-5,params_list[0]+5), elevation__range = (params_list[1]-100, params_list[1]+100))
        serializers = PlantsSerializer(plants, many=True)
        return Response(serializers.data)                 
