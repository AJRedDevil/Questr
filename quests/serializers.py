

from .models import Quests

from rest_framework import serializers

class QuestSerializer(serializers.ModelSerializer):
    class Meta:
        model = Quests
        fields = (
            'id',
            'description',
            'status',
            'size',
            'pickup',
            'dropoff',
            'delivery_code',
            'pickup_time',
            'tracking_number',
            'distance'
            )