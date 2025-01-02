from rest_framework import serializers

from .models import Line, WishList


class LineSerializer(serializers.ModelSerializer):
	class Meta:
		model = Line
		fields = "__all__"


class WishListSerializer(serializers.ModelSerializer):
	lines = LineSerializer(many=True)

	class Meta:
		model = WishList
		fields = "__all__"
