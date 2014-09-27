

import logging

from django.test import TestCase
from django.utils import timezone
from django.test.client import Client


from libs import geomaps
from users.models import QuestrUserProfile, QuestrToken
from quests.models import Quests, QuestTransactional

class ManagerCase(TestCase):
    """Tests for User case"""
    def setUp(self):
        super(ManagerCase, self).setUp()
        # For Shipper
        self.username_shipper1 = "gaumire"
        self.first_name_shipper1 = "Gaurav"
        self.last_name_shipper1 = "Ghimire"
        self.password1_shipper1 = "123456"
        self.password2_shipper1 = "123456"
        self.email_shipper1 = "gaurav.ghimire@gmail.com"
        self.city_shipper1 = "Toronto"
        self.streetaddress_shipper1 = "16 Brookers Lane"
        self.postalcode_shipper1 = "M8V0A5"
        self.phone_shipper1 = "+1234567890"
        self.useraddress_shipper1 = dict(city=self.city_shipper1,streetaddress=self.streetaddress_shipper1,postalcode=self.postalcode_shipper1)
        self.post_data_shipper1={'first_name':self.first_name_shipper1,'last_name':self.last_name_shipper1,'displayname':self.username_shipper1,\
        'password1':self.password1_shipper1,'password2':self.password2_shipper1,'email':self.email_shipper1, 'city':self.city_shipper1, 'streetaddress':self.streetaddress_shipper1,\
        'postalcode':self.postalcode_shipper1, 'phone':self.phone_shipper1}                     

        # For Shipper  
        self.username_shipper2 = "gaumires"
        self.first_name_shipper2 = "Gaurav"
        self.last_name_shipper2 = "Ghimire"
        self.password1_shipper2 = "123456"
        self.password2_shipper2 = "123456"
        self.email_shipper2 = "gaurav.ghimire@gmail.coms"
        self.city_shipper2 = "Toronto"
        self.streetaddress_shipper2 = ""
        self.postalcode_shipper2 = "M8Y3L8"
        self.phone_shipper2 = "+1234567890"
        self.useraddress_shipper2 = dict(city=self.city_shipper2,streetaddress=self.streetaddress_shipper2,postalcode=self.postalcode_shipper2)
        self.post_data_shipper2={'first_name':self.first_name_shipper2,'last_name':self.last_name_shipper2,'displayname':self.username_shipper2,\
        'password1':self.password1_shipper2,'password2':self.password2_shipper2,'email':self.email_shipper2, 'city':self.city_shipper2, 'streetaddress':self.streetaddress_shipper2,\
        'postalcode':self.postalcode_shipper2, 'phone':self.phone_shipper2}

        # For Shipper unavailable
        self.username_shipper3 = "sgaumire"
        self.first_name_shipper3 = "sGaurav"
        self.last_name_shipper3 = "sGhimire"
        self.password1_shipper3 = "s123456"
        self.password2_shipper3 = "s123456"
        self.email_shipper3 = "sgaurav.ghimire@gmail.com"
        self.city_shipper3 = "Toronto"
        self.streetaddress_shipper3 = ""
        self.postalcode_shipper3 = "M8Z2J1"
        self.phone_shipper3 = "+1234567890"
        self.useraddress_shipper3 = dict(city=self.city_shipper3,streetaddress=self.streetaddress_shipper3,postalcode=self.postalcode_shipper3)
        self.post_data_shipper3={'first_name':self.first_name_shipper3,'last_name':self.last_name_shipper3,'displayname':self.username_shipper3,\
        'password1':self.password1_shipper3,'password2':self.password2_shipper3,'email':self.email_shipper3, 'city':self.city_shipper3, 'streetaddress':self.streetaddress_shipper3,\
        'postalcode':self.postalcode_shipper3, 'phone':self.phone_shipper3} 

        # For Shipper unavailable
        self.username_admin1 = "gaumsire"
        self.first_name_admin1 = "Gausrav"
        self.last_name_admin1 = "Ghimsire"
        self.password1_admin1 = "1234s56"
        self.password2_admin1 = "1234s56"
        self.email_admin1 = "gaurav.gshimire@gmail.com"
        self.city_admin1 = "Toronto"
        self.streetaddress_admin1 = ""
        self.postalcode_admin1 = "L4X1M3"
        self.phone_admin1 = "+1234567890"
        self.useraddress_admin1 = dict(city=self.city_admin1,streetaddress=self.streetaddress_admin1,postalcode=self.postalcode_admin1)
        self.post_data_admin1={'first_name':self.first_name_admin1,'last_name':self.last_name_admin1,'displayname':self.username_admin1,\
        'password1':self.password1_admin1,'password2':self.password2_admin1,'email':self.email_admin1, 'city':self.city_admin1, 'streetaddress':self.streetaddress_admin1,\
        'postalcode':self.postalcode_admin1, 'phone':self.phone_admin1}

        # For Shipper unavailable
        self.username_admin2 = "gauasmire"
        self.first_name_admin2 = "Gauaasdrav"
        self.last_name_admin2 = "Ghimiasre"
        self.password1_admin2 = "1234sad56"
        self.password2_admin2 = "1234sad56"
        self.email_admin2 = "gaurav.ghisdmire@gmail.com"
        self.city_admin2 = "Toronto"
        self.streetaddress_admin2 = ""
        self.postalcode_admin2 = "L4W3S7"
        self.phone_admin2 = "+1234567890"
        self.useraddress_admin2 = dict(city=self.city_admin2,streetaddress=self.streetaddress_admin2,postalcode=self.postalcode_admin2)
        self.post_data={'first_name':self.first_name_admin2,'last_name':self.last_name_admin2,'displayname':self.username_admin2,\
        'password1':self.password1_admin2,'password2':self.password2_admin2,'email':self.email_admin2, 'city':self.city_admin2, 'streetaddress':self.streetaddress_admin2,\
        'postalcode':self.postalcode_admin2, 'phone':self.phone_admin2}  

        # For Quest
        self.questrs = 1
        self.creation_date = timezone.now()
        self.title = "New Quest"
        self.size = "backpack"
        self.description = "This is for a new test"
        self.srccity = "Toronto"
        self.srcaddress = "Alan Powell Ln"
        self.srcpostalcode = dict(postalcode='M5S1K4', city="Canada")
        self.srcname = "Frank Qin"
        self.srcphone = "1234567890"
        self.pickup = dict(city=self.srccity,address=self.srcaddress,postalcode=self.srcpostalcode,
            name=self.srcname,phone=self.srcphone
            )
        self.dstcity = "Markham"
        self.dstaddress = "65 Maria Rd"
        self.dstpostalcode = "L6E2G9"
        self.dstname = "Gaurav Ghimire"
        self.dstphone = "1987654320"
        self.reward = "89"
        self.distance = "19"
        self.dropoff = dict(city=self.dstcity,address=self.dstaddress,postalcode=self.dstpostalcode,
            name=self.dstname,phone=self.dstphone
            )
        self.data = dict(questrs_id=self.questrs,title=self.title,size=self.size,description=self.description,pickup=self.pickup,
            dropoff=self.dropoff)
        self.post_data = dict(questrs_id=self.questrs,title=self.title,size=self.size,description=self.description,srccity=self.srccity,\
            srcaddress=self.srcaddress,srcpostalcode=self.srcpostalcode,srcname=self.srcname,srcphone=self.srcphone,dstcity=self.dstcity,\
            dstaddress=self.dstaddress,dstpostalcode=self.dstpostalcode,dstname=self.dstname,dstphone=self.dstphone)


    def tests_manager(self):
        #Create User
        user1 = QuestrUserProfile(email=self.email_shipper1, password=self.password1_shipper1, displayname=self.username_shipper1,\
            email_status=True, is_shipper=True, is_available=True, address=self.useraddress_shipper1)
        user1.save()
        get_user1 = QuestrUserProfile.objects.get(email=self.email_shipper1)
        self.assertEqual(get_user1.email, self.email_shipper1)

        user2 = QuestrUserProfile(email=self.email_shipper2, password=self.password1_shipper2, displayname=self.username_shipper2,\
            email_status=True,is_shipper=True, is_available=True, address=self.useraddress_shipper2 )
        user2.save()
        get_user2 = QuestrUserProfile.objects.get(email=self.email_shipper2)
        self.assertEqual(get_user2.email, self.email_shipper2)

        user3 = QuestrUserProfile(email=self.email_shipper3, password=self.password1_shipper3, displayname=self.username_shipper3,\
            email_status=True, is_shipper=True, is_available=True, address=self.useraddress_shipper3)
        user3.save()
        get_user3 = QuestrUserProfile.objects.get(email=self.email_shipper3)
        self.assertEqual(get_user3.email, self.email_shipper3)

        #Create SuperAdmins
        admin1 = QuestrUserProfile(email=self.email_admin1, password=self.password1_admin1, displayname=self.username_admin1,\
            email_status=True, is_superuser=True, address=self.useraddress_admin1)
        admin1.save()
        get_admin1 = QuestrUserProfile.objects.get(email=self.email_admin1)
        self.assertEqual(get_admin1.email, self.email_admin1)

        admin2 = QuestrUserProfile(email=self.email_admin2, password=self.password1_admin2, displayname=self.username_admin2,\
            email_status=True, is_superuser=True, address=self.useraddress_admin2)
        admin2.save()
        get_admin2 = QuestrUserProfile.objects.get(email=self.email_admin2)
        self.assertEqual(get_admin2.email, self.email_admin2)



        # Create Quest
        questdetails = Quests(questrs_id=self.questrs,title=self.title,size=self.size,description=self.description,pickup=self.pickup,
            dropoff=self.dropoff, reward=self.reward, creation_date = self.creation_date)
        Quests.save(questdetails)
        quest = Quests.objects.get(id=1)
        ## Check if quest is created fine
        self.assertEqual(questdetails.title, self.title)


        from users.contrib import user_handler
        from quests.contrib import quest_handler
        couriermanager = user_handler.CourierManager()
        # ##* Get the list of available shippers
        couriermanager.informShippers(quest)
        # courierlist = couriermanager.getActiveCouriers()
#         available = couriermanager.getAvailableCouriersWithProximity(courierlist, quest)
#         # logging.warn(courierlist)
#         # logging.warn("List of available shippers")
#         # self.assertIsInstance(couriermanager,user_handler.CourierManager)
#         ##* is list empty
#         if len(courierlist) == 0:
#             ##* inform Don and Frank
#             dothis = couriermanager.informSuperAdmins(quest)
#             self.assertEqual(dothis, 'success')
#             if dothis == "success":
#                 #its good
#                 pass
#             else:
#                 # Man we have a problem return 500 NO SHIPPERS AVAILABLE NOW, ASK THE USER TO HIT "process quest"
#                 # "process quest" will have to be put somewhere in his dashboard of quest which are not honored
#                 pass

#         ##* get_courier_dict
#         couriers_dict = couriermanager.getAvailableCouriersWithProximity(courierlist, quest)
#         # logging.warn("list of shippers with proximity details")
#         # logging.warn(couriers_dict)
# # Returns a KVP with keys as below userid, address, distance, is_available, in_proximity
#         # couriers_dict = {}
#         # for courier in courierlist:
#         #     courierdict = {}
#         #     origin = courier.address['postalcode']+", "+courier.address['city']
#         #     destination = str(quest.pickup['postalcode'])+", "+str(quest.pickup['city'])
#         #     # Check if user is in proximity
#         #     courierdict['proximity'] = couriermanager.checkProximity(origin, destination)
#         #     courierdict['is_available'] = True
#         #     courierdict['address'] = courier.address
#         #     # logging.warn(courierdict)
#         #     couriers_dict[courier.id] = courierdict
#         quest_handler.updateQuestWithAvailableCourierDetails(quest, couriers_dict)
#         quest = Quests.objects.get(id=1)
#         # Quests.objects.filter(id=1).update(available_couriers=couriers_dict)
#         # logging.warn(quest.available_couriers)
#         ##* if courier in proximity or not check
#         couriers_list = couriermanager.getCouriersInProximity(quest)
#         if len(couriers_list) == 0:
#             couriers_list = couriermanager.getCouriersNotInProximity(quest)

#         # logging.warn("couriers with distance filtered")
#         # logging.warn(couriers_list)
#         # accept_url = quest_handler.get_accept_url(quest, user_handler.getQuestrDetails(couriers_list[0][0]))
#         # reject_url = quest_handler.get_reject_url(quest, user_handler.getQuestrDetails(couriers_list[0][0]))
#         # logging.warn(accept_url)
#         # logging.warn(reject_url)
#         # couriermanager.informCourier(couriers_list[0][0], quest)

#         # logging.warn(couriers_in_proximity.iteritems())
#         # logging.warn(couriers_in_proximity[0][0][1])
#         # sorted(couriers_in_proximity.iteritems(), key=lambda x: (x[1]))
#         # logging.warn(couriers_list[0])
#         # couriers_not_in_proximity = quest_handler.getCouriersInProximity(quest.available_couriers)
#         # for courier in quest.available_couriers:
#         #     if quest.available_couriers[courier]['proximity']['in_proximity'] == True:
#         #         logging.warn("Courier is in proximity")
#         #     else:
#         #         logging.warn("He is not")
#             # logging.warn(courier.email_status)

#         # ## Check if the shipper count is true, there are 3 shippers created above
#         # self.assertEqual(len(courierlist), 3)

#         # # Update availability of second shipper 
#         # user_handler.updateCourierAvailability(courierlist[1], 0)

#         # courierlist = couriermanager.getActiveCouriers()
#         # # 2 shippers are available 
#         # self.assertEqual(len(courierlist), 3)
