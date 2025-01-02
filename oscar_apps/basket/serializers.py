from rest_framework import serializers

from .models import Basket, Line


class LineSerializer(serializers.ModelSerializer):
	class Meta:
		model = Line
		fields = "__all__"


class BasketSerializer(serializers.ModelSerializer):
	lines = LineSerializer(many=True)

	class Meta:
		model = Basket
		fields = "__all__"
