



from quests.models import Quests, PACKAGE_SELECTION, CITY_SELECTION

from rest_framework import serializers


class QuestSerializer(serializers.ModelSerializer):
    questr = serializers.Field(source='questrs.displayname')
    class Meta:
        model = Quests
        fields = (
            'id',
            'title',
            'questr',
            'size',
            'description',
            'pickup',
            'dropoff',
            'pickup_time',
            'reward',
            'distance',
            ) 

class NewQuestDataValidationSerializer(serializers.Serializer):
    title = serializers.CharField()
    size = serializers.ChoiceField(choices=PACKAGE_SELECTION)
    pickup_time = serializers.DateTimeField()
    description = serializers.CharField()
    srccity = serializers.ChoiceField(choices=CITY_SELECTION)
    srcaddress = serializers.CharField()
    srcaddress_2 = serializers.CharField(required=False)
    srcpostalcode = serializers.CharField()
    srcname = serializers.CharField()
    srcphone = serializers.CharField(required=False)
    dstcity = serializers.ChoiceField(choices=CITY_SELECTION)
    dstaddress = serializers.CharField()
    dstaddress_2 = serializers.CharField(required=False)
    dstpostalcode = serializers.CharField()
    dstname = serializers.CharField()
    dstphone = serializers.CharField(required=False)

class NewQuestSerializer(serializers.ModelSerializer):
    class Meta:
        model = Quests
        fields = (
            'title',
            'size',
            'description',
            'pickup',
            'dropoff',
            'pickup_time',
            'reward',
            'distance',
            'questrs',
            'map_image'
            ) 

class PriceCalcSerializer(serializers.Serializer):
    size = serializers.ChoiceField(choices=PACKAGE_SELECTION, default="backpack")
    srccity = serializers.ChoiceField(choices=CITY_SELECTION, default="Toronto")
    srcaddress = serializers.CharField()
    srcaddress_2 = serializers.CharField(required=False)
    srcpostalcode = serializers.CharField()
    dstcity = serializers.ChoiceField(choices=CITY_SELECTION, default="Toronto")
    dstaddress = serializers.CharField()
    dstaddress_2 = serializers.CharField(required=False)
    dstpostalcode = serializers.CharField()

