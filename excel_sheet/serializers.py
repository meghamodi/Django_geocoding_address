from rest_framework import serializers
from excel_sheet.models import Sheet

class SheetSerializer(serializers.ModelSerializer):
	class Meta:
		model = Sheet
		fields= ('file',)