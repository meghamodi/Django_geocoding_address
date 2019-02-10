from django.shortcuts import render
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from excel_sheet.models import Sheet
from rest_framework.authtoken.models import Token
from django.contrib.auth import authenticate
from excel_sheet.serializers import SheetSerializer
import xlrd
import requests
# class SheetView(APIView):
# 	def post(self,request,format=None,*args,**kwargs):
# 		try:
# 			data = request.data.dict()
# 			file = data['file'] 
# 			user = request.user
# 			if not file:
# 				raise ValueError('file not found')
# 			Sheet.objects.create(user=user, file=file)

# 			response = {'status': 200, 'message': 'File uploaded'}


# 		except ValueError as err:
#         	response = {'status': status.HTTP_400_BAD_REQUEST, 'error_message': str(err)}
#         except RuntimeError as err:
#             response = {'status': status.HTTP_500_INTERNAL_SERVER_ERROR, 'error_message': str(err)}

#         return Response(response, status=response['status'])
# Create your views here.
# def read_excel(file_path):
# 	print(file_path)
# 	loc = file_path
# 	wb = xlrd.open_workbook(loc) 
# 	sheet = wb.sheet_by_index(0)
# 	for i in range(sheet.max_row):

# 		GOOGLE_MAPS_API_URL = 'http://maps.googleapis.com/maps/api/geocode/json'
# 		params = {
# 	    	'address': sheet.cell_value[i,0]
# 	    }
# 	    req= requests.get(GOOGLE_MAPS_API_URL, params=params)
# 	    res = req.json()
# 	    result = res['results'][0]
# 	    geodata = dict()
# 		geodata['lat'] = result['geometry']['location']['lat']
# 		geodata['lng'] = result['geometry']['location']['lng']
# 		geodata['address'] = result['formatted_address']

def read_excel(file_path):
	print(file_path)
	loc = file_path.url
	wb = xlrd.open_workbook(loc)
	sheet = wb.sheet_by_index(0)
	print(sheet.nrows)
	for i in range(sheet.nrows):
		GOOGLE_MAPS_API_URL = 'https://maps.googleapis.com/maps/api/geocode/json?key=AIzaSyDtQm3_0QFkJZEbvGEGXci6U38-Ihy1sAc&address='+sheet.cell_value(i,0)
		print(sheet.cell_value(i,0))
		
		req = requests.get(GOOGLE_MAPS_API_URL)
		res = req.json()
		print(res)
		result = res['results'][0]
		
		lat = result['geometry']['location']['lat']
		lng = result['geometry']['location']['lng']
		
		print(geodata)




class SheetView(APIView):
	def post(self,request,format=None,*args,**kwargs):
		try:
			data = request.data.dict()
			file = data['file'] 
			user = request.user
			if not file:
				raise ValueError('file not found')
			sh = Sheet.objects.create(user=user, file=file)
			read_excel(sh.file)
			response = {'status': 200, 'message': 'File uploaded'}
		except ValueError as err:
			response = {'status': status.HTTP_400_BAD_REQUEST, 'error_message': str(err)}
		except RuntimeError as err:
			response = {'status': status.HTTP_500_INTERNAL_SERVER_ERROR, 'error_message': str(err)}
		return Response(response, status=response['status'])

	# def get(self, request, format=None, *args, **kwargs):
 #        try:
 #            files = Sheet.objects.filter(user=request.user)
 #            serializer = SheetSerializer(files, many=True)

 #            response = {'status': 200, 'data': serializer.data} 

 #        except RuntimeError as err:
	# 		response = {'status': status.HTTP_500_INTERNAL_SERVER_ERROR, 'error_message': str(err)}
	# 	return Response(response, status=response['status'])
	def get(self, request, format=None, *args, **kwargs):
		try:
			files = Sheet.objects.filter(user=request.user)
			serializer = SheetSerializer(files, many=True)
			response = {'status': 200, 'data': serializer.data} 
		except RuntimeError as err:
			response = {'status': status.HTTP_500_INTERNAL_SERVER_ERROR, 'error_message': str(err)}
		return Response(response, status=response['status'])




class LoginView(APIView):
    authentication_classes = []
    permission_classes = []
    def post(self, request, format=None, *args, **kwargs):
        try:
            if hasattr(request.data, 'dict'):
                data = request.data.dict()
            else:
                data = request.data

            username = data.pop('username', None)
            password = data.pop('password', None)



            if not username:
                raise ValueError('username not found')
            if not password:
                raise ValueError('password not found')

            user = authenticate(username=username, password=password)
            if not user:
                return Response({'error': 'Invalid Credentials'},
                                status=status.HTTP_404_NOT_FOUND)
            token, _ = Token.objects.get_or_create(user=user)

            response = {'token': token.key, 'status': status.HTTP_200_OK}

        except ValueError as err:
            response = {'status': status.HTTP_400_BAD_REQUEST, 'error_message': str(err)}
        except RuntimeError as err:
            response = {'status': status.HTTP_500_INTERNAL_SERVER_ERROR, 'error_message': str(err)}

        return Response(response, status=response['status'])


