from rest_framework import serializers
from .models import Plants

class PlantsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Plants
        fields = ('id','name','temperature', 'description', 'elevation', 'pic')  
        