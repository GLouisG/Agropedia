from django.shortcuts import render
from rest_framework.views import APIView

from app.models import Plants
from app.serializer import PlantsSerializer
from rest_framework.response import Response
from django.views.decorators.clickjacking import xframe_options_exempt


import pandas as pd                                                       
from sklearn import preprocessing                              
from sklearn.neighbors import KNeighborsClassifier                       
import numpy as np   


excel = pd.read_excel('crop.xlsx', header = 0)                                      
print(excel)                                                              # Printing our excel file data.
print(excel.shape)

le = preprocessing.LabelEncoder()
crop = le.fit_transform(list(excel["CROP"])) 

NITROGEN = list(excel["NITROGEN"])
PHOSPHORUS = list(excel["PHOSPHORUS"])
POTASSIUM = list(excel["POTASSIUM"])
TEMPERATURE = list(excel["TEMPERATURE"]) 
HUMIDITY = list(excel["HUMIDITY"])
PH = list(excel["PH"])
RAINFALL = list(excel["RAINFALL"]) 

features = list(zip(NITROGEN, PHOSPHORUS, POTASSIUM, TEMPERATURE, HUMIDITY, PH, RAINFALL))
features = np.array([NITROGEN, PHOSPHORUS, POTASSIUM, TEMPERATURE, HUMIDITY, PH, RAINFALL])                    # Converting all the features into a array form     

features = features.transpose()                                                                                # Making transpose of the features 

print(features.shape)                                                                                          # Printing the shape of the features after getting transposed.

print(crop.shape)                                                                                              # Printing the shape of crop. Please note that the shape of the features and crop should match each other to make predictions.

model = KNeighborsClassifier(n_neighbors=3)                                                                    # The number of neighbors is the core deciding factor. K is generally an odd number if the number of classes is 2. When K=1, then the algorithm is known as the nearest neighbor algorithm.

model.fit(features, crop)                                                                                      # fit your model on the train set using fit() and perform prediction on the test set using predict().



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
class PlantsSuggest(APIView):
    def get(self, request, *args,**kwargs):
        # params = kwargs
        params = self.kwargs.get('params', None)
        params_list = list(map(int, params.split('-')))
        values = params_list 
                        

        while True:
            print(values[0])
            nitrogen_content =         values[0]                                                                                                        # Taking input from the user about nitrogen content in the soil.
            phosphorus_content =       values[1]                                                                                                        # Taking input from the user about phosphorus content in the soil.
            potassium_content =        values[2]                                                                                                        # Taking input from the user about potassium content in the soil.
            temperature_content =      values[3]                                                                                                        # Taking input from the user about the surrounding temperature.
            humidity_content =         values[4]                                                                                                        # Taking input from the user about the surrounding humidity. 
            ph_content =               values[5]                                                                                                        # Taking input from the user about the ph level of the soil.
            rainfall =                 values[6]                                                                                                        # Taking input from the user about the rainfall.
            predict1 = np.array([nitrogen_content,phosphorus_content, potassium_content, temperature_content, humidity_content, ph_content, rainfall])  # Converting all the data that we collected from the user into a array form to make further predictions.
            print(predict1)                                                                                                                             # Printing the data after being converted into a array form.
            predict1 = predict1.reshape(1,-1)                                                                              # Reshaping the input data so that it can be applied in the model for getting accurate results.
            print(predict1)                                                                                                # Printing the input data value after being reshaped.
            predict1 = model.predict(predict1)                                                                             # Applying the user input data into the model. 
            print(predict1)                                                                                                # Finally printing out the results.
            crop_name = str()
            if predict1 == 0:                                                                                              # Above we have converted the crop names into numerical form, so that we can apply the machine learning model easily. Now we have to again change the numerical values into names of crop so that we can print it when required. 
                crop_name = 'Apple'
            elif predict1 == 1:
                crop_name = 'Banana'
            elif predict1 == 2:
                crop_name = 'Blackgram'
            elif predict1 == 3:
                crop_name = 'Chickpea'
            elif predict1 == 4:
                crop_name = 'Coconut'
            elif predict1 == 5:
                crop_name = 'Coffee'
            elif predict1 == 6:
                crop_name = 'Cotton'
            elif predict1 == 7:
                crop_name = 'Grapes'
            elif predict1 == 8:
                crop_name = 'Jute'
            elif predict1 == 9:
                crop_name = 'Kidneybeans'
            elif predict1 == 10:
                crop_name = 'Lentil'
            elif predict1 == 11:
                crop_name = 'Maize'
            elif predict1 == 12:
                crop_name = 'Mango'
            elif predict1 == 13:
                crop_name = 'Mothbeans'
            elif predict1 == 14:
                crop_name = 'Mungbeans'
            elif predict1 == 15:
                crop_name = 'Muskmelon'
            elif predict1 == 16:
                crop_name = 'Orange'
            elif predict1 == 17:
                crop_name = 'Papaya'
            elif predict1 == 18:
                crop_name = 'Pigeonpeas'
            elif predict1 == 19:
                crop_name = 'Pomegranate'
            elif predict1 == 20:
                crop_name = 'Rice'
            elif predict1 == 21:
                crop_name = 'Watermelon'

            if int(humidity_content) >=1 and int(humidity_content)<= 33 :                                                # Here I have divided the humidity values into three categories i.e low humid, medium humid, high humid.
                humidity_level = 'low humid'
            elif int(humidity_content) >=34 and int(humidity_content) <= 66:
                humidity_level = 'medium humid'
            else:
                humidity_level = 'high humid'

            if int(temperature_content) >= 0 and int(temperature_content)<= 6:                                           # Here I have divided the temperature values into three categories i.e cool, warm, hot.
                temperature_level = 'cool'
            elif int(temperature_content) >=7 and int(temperature_content) <= 25:
                temperature_level = 'warm'
            else:
                temperature_level= 'hot' 

            if int(rainfall) >=1 and int(rainfall) <= 100:                                                              # Here I have divided the humidity values into three categories i.e less, moderate, heavy rain.
                rainfall_level = 'less'
            elif int(rainfall) >= 101 and int(rainfall) <=200:
                rainfall_level = 'moderate'
            elif int(rainfall) >=201:
                rainfall_level = 'heavy rain'

            if int(nitrogen_content) >= 1 and int(nitrogen_content) <= 50:                                             # Here I have divided the nitrogen values into three categories.
                nitrogen_level = 'less'
            elif int(nitrogen_content) >=51 and int(nitrogen_content) <=100:
                nitrogen_level = 'not to less but also not to high'
            elif int(nitrogen_content) >=101:
                nitrogen_level = 'high'

            if int(phosphorus_content) >= 1 and int(phosphorus_content) <= 50:                                         # Here I have divided the phosphorus values into three categories.
                phosphorus_level = 'less'
            elif int(phosphorus_content) >= 51 and int(phosphorus_content) <=100:
                phosphorus_level = 'not to less but also not to high'
            elif int(phosphorus_content) >=101:
                phosphorus_level = 'high'

            if int(potassium_content) >= 1 and int(potassium_content) <=50:                                           # Here I have divided the potassium values into three categories.
                potassium_level = 'less'
            elif int(potassium_content) >= 51 and int(potassium_content) <= 100:
                potassium_level = 'not to less but also not to high'
            elif int(potassium_content) >=101:
                potassium_level = 'high'

            if float(ph_content) >=0 and float(ph_content) <=5:                                                        # Here I have divided the ph values into three categories.
                phlevel = 'acidic' 
            elif float(ph_content) >= 6 and float(ph_content) <= 8:
                phlevel = 'neutral'
            elif float(ph_content) >= 9 and float(ph_content) <= 14:
                phlevel = 'alkaline'
            
            print(crop_name)
            print(humidity_level)
            print(temperature_level)
            print(rainfall_level)
            print(nitrogen_level)
            print(phosphorus_level)
            print(potassium_level)
            print(phlevel)    
            res = "We suggest you grow "+crop_name
            return Response({'result':res})            