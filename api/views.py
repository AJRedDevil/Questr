from django.shortcuts import render

# Create your views here.


#All Django Imports
from django.http import Http404

#All local imports (libs, contribs, models)
from quests.models import Quests
from quests.contrib import quest_handler
from users.contrib import user_handler
import serializers

#All external imports (libs, packages)
import logging
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
import simplejson as json

# Init Logger
logger = logging.getLogger(__name__)

class QuestsList(APIView):
    """
    Shipment resource
    """

    def get(self, request, format=None):
        """
        Returns a list of shipments
        """

        user = request.user
        if user.is_shipper:
            queryset = Quests.objects.filter(shipper=user.id, ishidden=False)
        elif user.is_superuser:
            queryset = Quests.objects.all()
        else:
            queryset = Quests.objects.filter(questrs_id=user)
        serializer = serializers.QuestSerializer(queryset, many=True)
        return Response(serializer.data)

    def post(self, request, format=None):
        """
        Creates a new shipment from the provided data
        ---
        request_serializer: serializers.NewQuestDataValidationSerializer
        response_serializer: serializers.NewQuestSerializer
        """

        user = request.user
        if user.is_shipper:
            return Response(status=status.HTTP_403_FORBIDDEN)

        ##Validate if all the data is available###
        serializer = serializers.NewQuestDataValidationSerializer(data=request.DATA)
        if serializer.is_valid():
            data = request.DATA
            ##Calculate distance and price
            pickupdict = {}
            dropoffdict = {}
            from libs import geomaps, pricing
            maps = geomaps.GMaps()
            price = pricing.WebPricing(user)
            size = data['size']
            pickupdict['city'] = data['srccity']
            pickupdict['address'] = data['srcaddress']
            pickupdict['address_2'] = data['srcaddress_2']
            pickupdict['postalcode'] = data['srcpostalcode']
            pickupdict['name'] = data['srcname']
            pickupdict['phone'] = data['srcphone']
            dropoffdict['city'] = data['dstcity']
            dropoffdict['address'] = data['dstaddress']
            dropoffdict['address_2'] = data['dstaddress_2']
            dropoffdict['postalcode'] = data['dstpostalcode']
            dropoffdict['name'] = data['dstname']
            dropoffdict['phone'] = data['dstphone']
            origin = pickupdict['address']+', '+pickupdict['city']+', '+pickupdict['postalcode']
            destination = dropoffdict['address']+', '+dropoffdict['city']+', '+dropoffdict['postalcode']
            maps.set_geo_args(dict(origin=origin, destination=destination))
            distance = maps.get_total_distance()
            map_image = maps.fetch_static_map()
            reward = price.get_price(distance, shipment_mode=size)
            questrs = user.id
            data['reward']=reward
            data['distance']=distance
            data['map_image']=map_image
            data['questrs']=questrs
            data['pickup'] = json.dumps(pickupdict)
            data['dropoff'] = json.dumps(dropoffdict)
            serializer = serializers.NewQuestSerializer(data=data)
            if serializer.is_valid():
                logging.warn(serializer.data)
                serializer.save()
                return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class QuestsDetail(APIView):
    def get_object(self, pk):
        try:
            return Quests.objects.get(pk=pk, ishidden=False)
        except Quests.DoesNotExist:
            raise Http404

    def get(self, request, pk, format=None):
        """
        Returns the details of the shipment
        """
        user = request.user
        quest = self.get_object(pk)
        serializer = serializers.QuestSerializer(quest)
        if quest.shipper == str(user.id) or user.is_superuser or quest.questrs_id == user.id:
            return Response(serializer.data)
        return Response(status=status.HTTP_403_FORBIDDEN)

class PriceCalculator(APIView):
    """
    Price calculator resource
    """
    def post(self, request, format=None):
        """
        Returns with price after receiving shipment information
        ---
        request_serializer: serializers.PriceCalcSerializer
        response_serializer: serializers.PriceCalcSerializer
        """

        user = request.user
        if user.is_shipper:
            return Response(status=status.HTTP_403_FORBIDDEN)

        ##Validate if all the data is available###
        serializer = serializers.PriceCalcSerializer(data=request.DATA)
        if serializer.is_valid():
            data = request.DATA
            ##Calculate distance and price
            pickupdict = {}
            dropoffdict = {}
            from libs import geomaps, pricing
            maps = geomaps.GMaps()
            price = pricing.WebPricing(user)
            size = data['size']
            pickupdict['city'] = data['srccity']
            pickupdict['address'] = data['srcaddress']
            pickupdict['postalcode'] = data['srcpostalcode']
            dropoffdict['city'] = data['dstcity']
            dropoffdict['address'] = data['dstaddress']
            dropoffdict['postalcode'] = data['dstpostalcode']
            origin = pickupdict['address']+', '+pickupdict['city']+', '+pickupdict['postalcode']
            destination = dropoffdict['address']+', '+dropoffdict['city']+', '+dropoffdict['postalcode']
            maps.set_geo_args(dict(origin=origin, destination=destination))
            distance = maps.get_total_distance()
            fee = price.get_price(distance, shipment_mode=size)
            responsedata=dict(fee=fee)
            return Response(responsedata, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class AvailabilityStatus(APIView):
    """
    Courier Status resource
    """

    def post(self, request, format=None):
        """
        Update status of courier
        ---
        request_serializer: serializers.StatusSeralizer
        """

        user = request.user
        if not user.is_shipper:
            return Response(status=status.HTTP_403_FORBIDDEN)

        ##Validate if all the data is available###
        serializer = serializers.StatusSeralizer(data=request.DATA)
        if serializer.is_valid():
            data = request.DATA.copy()
            userstatus = data['status'] in ['True', 'true', '1']
            result = user_handler.updateCourierAvailability(user, userstatus)
            if result['success'] == True:
                responsedata=dict(status=status.HTTP_200_OK, success=True)                
            else:
                responsedata=dict(data="Status already set", status=status.HTTP_409_CONFLICT, success=False)
            return Response(responsedata)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class QuestStatus(APIView):
    """
    Package Status resource
    """
    def post(self, request, format=None):
        """
        Update status of a shipment
        ---
        request_serializer: serializers.QuestStatusSerializer
        """

        user = request.user
        if not user.is_shipper:
            return Response(status=status.HTTP_403_FORBIDDEN)

        serializer = serializers.QuestStatusSerializer(data=request.DATA)
        if serializer.is_valid():
            data = request.DATA.copy()
            quest = data['quest']
            eventtype = data['event']
            extrainfo = json.loads(data['extrainfo'])
            qm = quest_handler.QuestEventManager()
            result = qm.updatestatus(quest, eventtype, extrainfo)
            if result['success'] == True:
                responsedata=dict(status=status.HTTP_200_OK, success=True)                
            else:
                responsedata=dict(status=status.HTTP_409_CONFLICT, success=False)
            return Response(responsedata)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)