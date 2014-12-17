

#All Django Imports
from django.conf import settings
from django.http import Http404
from django.shortcuts import get_object_or_404
from django.utils import timezone

#All local imports (libs, contribs, models)
from libs import email_notifier, geomaps
from quests.contrib import quest_handler
from quests.models import Quests, QuestTransactional
from quests.tasks import inform_shipper_task
from users.models import QuestrUserProfile, UserToken, UserEvents, UserToken

#All external imports (libs, packages)
from collections import OrderedDict 
import logging
import simplejson as json
from random import choice

# Init Logger
logger = logging.getLogger(__name__)

def get_random_password():
    """
    Generates a random password.
    """
    random_password = ''.join([choice('1234567890qwertyuiopasdfghjklzxcvbnm') for i in range(7)])
    return random_password

def prepPasswordResetNotification(questr, reset_link):
    """Prepare the details for notification of resetting of password"""
    template_name="RESET_PASSWORD_EMAIL"
    subject="Questr - Password Reset Request !"
    quest_support_email="support@questr.co"

    email_details = {
                        'subject' : subject,
                        'template_name' : template_name,
                        'global_merge_vars': {
                                                'questr_first_name'   : questr.first_name,
                                                'questr_last_name'   : questr.last_name,
                                                'new_password'      : reset_link,
                                                'quest_support_mail': quest_support_email,
                                                'company'           : "Questr Co",
                                                },
                    }

    logger.debug("Password reset email is prepared")
    return email_details


def prepWelcomeNotification(questr, verf_link):
    """Prepare the details for notification emails after new user registers"""
    template_name="Welcome_Email"
    subject="Questr - Please verify your email !"
    quest_support_email="support@questr.co"

    email_details = {
                        'subject' : subject,
                        'template_name' : template_name,
                        'global_merge_vars': {
                                                'questr_first_name'   : questr.first_name,
                                                'questr_last_name'   : questr.last_name,
                                                'quest_support_mail': quest_support_email,
                                                'company'           : "Questr Co",
                                                'verf_link'         : verf_link,
                                                },
                    }

    logger.debug("Welcome email is prepared")
    return email_details

def prepSignupNotification(signup_link):
    """
    Prepare the details for notification emails for new signup invitation
    """
    template_name="Invitation_Email"
    subject="Questr - Join our private beta!"

    email_details = {
                        'subject' : subject,
                        'template_name' : template_name,
                        'global_merge_vars': {
                                                'company'           : "Questr Co",
                                                'signup_link'         : signup_link,
                                                },
                    }

    logger.debug("Signup invitation email is prepared")
    return email_details

def prepWelcomeCourierNotification(questr, password):
    """Prepare the details for notification emails after new courier registers"""
    template_name="Welcome_Courier_Email"
    subject="Questr - Welcome aboard !"
    quest_support_email="support@questr.co"

    email_details = {
                        'subject' : subject,
                        'template_name' : template_name,
                        'global_merge_vars': {
                                                'questr_first_name'   : questr.first_name,
                                                'questr_last_name'   : questr.last_name,
                                                'questr_email'   : questr.email,
                                                'quest_support_mail': quest_support_email,
                                                'company'           : "Questr Co",
                                                'password'         : password,
                                                },
                    }

    logger.debug("Welcome email is prepared")
    return email_details

def get_verification_url(user=None): 
    """
        Returns the verification url.
    """
    verf_link = ""
    if user:
        try:
            prev_token = UserToken.objects.get(email = user.email, token_type = 0, status = False)
            if prev_token:
                prev_token.status = True
                prev_token.save()
        except UserToken.DoesNotExist:
            pass
        verf_token = UserToken(email=user.email, token_type=0)
        verf_token.save()
        verf_link = "{0}/user/email/confirm/?questr_token={1}".format(settings.QUESTR_URL , verf_token.get_token())
    return verf_link

def get_signup_invitation_url(email=None, token_type=None): 
    """
        Returns the verification url.
    """
    signup_link = ""
    if email and token_type:
        try:
            prev_token = UserToken.objects.get(email = email, token_type = token_type, status = False)
            if prev_token:
                prev_token.status = True
                prev_token.save()
        except UserToken.DoesNotExist:
            pass
        signup_token = UserToken(email=email, token_type=token_type)
        signup_token.save()
        signup_link = "{0}/signup/invitation/?questr_token={1}".format(settings.QUESTR_URL , signup_token.get_token())
    return signup_link

def get_password_reset_url(email=None): 
    """
        Returns the password reset url.
    """
    reset_link = ""
    if email:
        try:
            prev_token = UserToken.objects.get(email = email, token_type = 3, status = False)
            if prev_token:
                prev_token.status = True
                prev_token.save()
        except UserToken.DoesNotExist:
            pass
        passwd_reset_token = UserToken(email=email, token_type=3)
        passwd_reset_token.save()
        reset_link = "{0}/user/passwordreset/?questr_token={1}".format(settings.QUESTR_URL , passwd_reset_token.get_token())
    return reset_link

def getQuestrDetails(questr_id):
    """Lists Questr information"""
    logging.warn(questr_id)
    questr = get_object_or_404(QuestrUserProfile, id=questr_id, is_active=True)
    return questr

def getShippers():
    """List all the list of couriers"""
    shippers = QuestrUserProfile.objects.filter(is_shipper=True, is_active=True)
    return shippers

def userExists(user_id):
    """Checks if the user by the provided displayname exists already"""
    try:
        user = QuestrUserProfile.objects.get(id=user_id)
    except QuestrUserProfile.DoesNotExist:
        return False
    if user:
        return True

def passwordExists(user):
    """Checks if the user has created a password for himself, passwords created by PSA are unusable"""
    return user.has_usable_password()

def updateCourierAvailability(questr, status):
    """Takes a Questr User Profile object and a status ( 0 | 1 ) and updates the availability status as per the same"""
    status = int(status)
    if userExists(questr.id):
        if status == False:
            statusupdate = QuestrUserProfile.objects.filter(id=questr.id, is_active=True).update(is_available=False)
            if statusupdate == 1:
                return dict(success=True)
            return dict(success=False)
        elif status == True:
            statusupdate = QuestrUserProfile.objects.filter(id=questr.id, is_active=True).update(is_available=True)
            if statusupdate == 1:
                return dict(success=True)
            return dict(success=False)
        else :
            raise ValueError('Status %d not acceptable, use True or False' % (status))
    return dict(success=False)


class CourierManager(object):
    """This is the manager that processes and assigns couriers automatically"""
    
    def __init__(self):
        pass

    def getActiveCouriers(self, quest):
        """Returns a list of couriers"""
        try:
            courierlist = QuestrUserProfile.objects.filter(is_shipper=True, is_superuser=False, is_available=True, is_active=True, email_status=True, vehicle=quest.size)
        except Exception, e:
            raise e

        return courierlist

    def getCourierAvailability(self, courier):
        """Returns if a courier is available"""
        courier_details = getQuestrDetails(courier)
        return courier_details.is_available

    # def updateCourierAvailability(questr, status):
    #     """Takes a Questr User Profile object and a status ( 0 | 1 ) and updates the availability status as per the same"""
    #     status = int(status)
    #     if userExists(questr.id):
    #         if status == 0:
    #             statusupdate = QuestrUserProfile.objects.filter(id=questr.id, is_active=True).update(is_available=False)
    #             if statusupdate == 1:
    #                 return dict(status='success')
    #             return dict(status="fail")
    #         elif status == 1:
    #             statusupdate = QuestrUserProfile.objects.filter(id=questr.id, is_active=True).update(is_available=True)
    #             if statusupdate == 1:
    #                 return dict(status='success')
    #             return dict(status="fail")
    #         else :
    #             raise ValueError('Status %d not acceptable, use 0 or 1' % (status))
    #     return dict(status='fail')

    def getSuperAdmins(self):
        """Returns a list of superadmins"""
        try:
            courierlist = QuestrUserProfile.objects.filter(is_superuser=True, is_active=True)
        except Exception, e:
            raise e

        return courierlist

    def informSuperAdmins(self, quest):
        """Takes in a questobject and informs the superadmins of the same"""
        superadmins = self.getSuperAdmins()
        if len(superadmins) == 0:
            return "fail"
        else:
            for admin in superadmins: # send notifcations to all the shippers
                email_details = quest_handler.prepNewQuestAdminNotification(admin, quest)
                email_notifier.send_email_notification(admin, email_details)
            return "success"

    def informCourier(self, courier, quest):
        """Takes in a questobject and informs the superadmins of the same"""
        accept_url = quest_handler.get_accept_url(quest, courier)
        reject_url = quest_handler.get_reject_url(quest, courier)
        logging.warn(accept_url)
        logging.warn(reject_url)
        from libs.twilio_handler import twclient
        tw = twclient()
        alert_message = tw.load_newquest_notif(quest, accept_url, reject_url)
        logger.warn(alert_message)
        tw.sendmessage(courier.phone, alert_message)
        email_details = quest_handler.prepNewQuestNotification(courier, quest, accept_url, reject_url)
        email_notifier.send_email_notification(courier, email_details)
        return "success"

    def informCourierAfterAcceptance(self, courier, quest):
        """Takes in a questobject and a courier object and informs the courier of the accepted quest"""
        email_details = quest_handler.prepOfferAcceptedNotification(courier, quest)
        email_notifier.send_email_notification(courier, email_details)
        return "success"

    def informQuestrAfterAcceptance(self, courier, questr, quest):
        """Takes in a questobject, a questr object and a courier object and informs the questr of the accepted quest"""
        email_details = quest_handler.prepQuestAppliedNotification(courier, questr, quest)
        email_notifier.send_email_notification(questr, email_details)
        return "success"

    def checkProximity(self, address_1, address_2):
        proximity = settings.QUESTR_PROXIMITY
        maps = geomaps.GMaps()
        maps.set_geo_args(dict(origin=address_1, destination=address_2))
        distance = maps.get_total_distance()
        if int(distance) <= proximity:
            proximity = True
            return dict(in_proximity=proximity, distance=distance)
        else:
            proximity = False
            return dict(in_proximity=proximity, distance=distance)

    def getAvailableCouriersWithProximity(self, activecouriers, quest):
        """From the list of active couriers and respective quest, it returns a dict of couriers  with \
        their proximity details to that particular quest"""
        ## Dict of all the couriers
        couriers_dict_with_details = {}
        for courier in activecouriers:
            ## Dict of courier with their detail
            courier_dict_with_detail = {}
            ## Address of the courier
            origin = courier.address['postalcode']+", "+courier.address['city']
            ## Address of the questr
            destination = str(quest.pickup['postalcode'])+", "+str(quest.pickup['city'])
            ## Proximity details
            proximity_details = self.checkProximity(origin, destination)
            courier_dict_with_detail['in_proximity'] = proximity_details['in_proximity']
            courier_dict_with_detail['distance'] = proximity_details['distance']
            courier_dict_with_detail['is_available'] = self.getCourierAvailability(courier.id)
            courier_dict_with_detail['address'] = courier.address
            # logging.warn(courier_dict_with_detail)
            couriers_dict_with_details[courier.id] = courier_dict_with_detail
        return couriers_dict_with_details

    def getCouriersInProximity(self, quest):
        """Returns couriers in proximity sorted as per their distance"""
        couriers_in_proximity = {}
        for courier in quest.available_couriers:
            if quest.available_couriers[courier]['in_proximity'] == True:
                couriers_in_proximity[courier] = quest.available_couriers[courier]

        couriers_in_proximity = OrderedDict(sorted(couriers_in_proximity.iteritems(), key=lambda x: x[1]['distance']))

        return couriers_in_proximity.items()


    def getCouriersNotInProximity(self, quest):
        """Returns couriers in proximity sorted as per their distance"""
        couriers_not_in_proximity = {}
        for courier in quest.available_couriers:
            if quest.available_couriers[courier]['in_proximity'] == False:
                couriers_not_in_proximity[courier] = quest.available_couriers[courier]
        
        couriers_not_in_proximity = OrderedDict(sorted(couriers_not_in_proximity.iteritems(), key=lambda x: x[1]['distance']))

        return couriers_not_in_proximity.items()

    def informShippers(self, quest):
        """Takes a quest object and informs the relative shippers"""
        # Update available shippers for a quest only if it's blank
        if len(quest.available_couriers) == 0:
            logger.warn("No available couriers for this quest")
            activecouriers = self.getActiveCouriers(quest)
            if len(activecouriers) == 0:
                logger.warn("No active couriers in the system now")
                ##* inform the master couriers
                dothis = self.informSuperAdmins(quest)
                questdetails = quest_handler.getQuestDetails(int(quest.id))
                if dothis == "success":
                    logger.warn("Master Couriers have been informed as no shippers were available for quest %d" % (quest.id))
                    questdetails.isaccepted = True
                    questdetails.shipper = 0
                    questdetails.save()
                    # Setting all questtransactions for this quest as completed because MC are selected
                    transaction_update = QuestTransactional.objects.filter(quest=questdetails.id).update(status=True)
                    # Setting status of all considered couriers to True
                    considered_couriers = json.loads(questdetails.considered_couriers.strip(','))
                    for courier in considered_couriers:
                        courier = getQuestrDetails(courier)
                        courier.is_available = True
                        courier.save()

                    eventmanager = quest_handler.QuestEventManager()
                    extrainfo = dict(detail="master courier selected")
                    eventmanager.setevent(quest, 7, extrainfo)
                    return "fail"
                else:
                    # Man we have a problem return 500 NO SHIPPERS AVAILABLE NOW, ASK THE USER TO HIT "process quest"
                    # "process quest" will have to be put somewhere in his dashboard of quest which are not honored
                    logger.warn("Some serious problem")        
            available_couriers = self.getAvailableCouriersWithProximity(activecouriers, quest)
            ## Updating the respecitve quest with available courier details and considered couriers
            quest_handler.updateQuestWithAvailableCourierDetails(quest, available_couriers)
        quest = quest_handler.getQuestDetails(quest.id)
        couriers_list = self.getCouriersInProximity(quest)
        if len(couriers_list) == 0:
            couriers_list = self.getCouriersNotInProximity(quest)

        designated_courier = getQuestrDetails(couriers_list[0][0])
        if designated_courier.is_available:
            logger.warn("courier %s is available for quest %s, and is informed" % (designated_courier.displayname, quest))
            updateCourierAvailability(designated_courier, False) 
            # designated_courier.is_available = False
            # designated_courier.save()
            eventmanager = quest_handler.QuestEventManager()
            extrainfo = dict(selected_courier=designated_courier.id, courier_availability=True, detail="courier selected and available")
            eventmanager.setevent(quest, 3, extrainfo)
            self.informCourier(designated_courier, quest)
        else:
            available_couriers = quest.available_couriers
            if len(available_couriers) > 0:
                logging.warn(available_couriers)
                available_couriers.pop(str(designated_courier.id), None)
                quest.available_couriers = available_couriers
                ##Save all the details
                quest.save()
                quest = quest_handler.getQuestDetails(quest.id)
                logger.warn("courier %s is unavailable for quest %s, and is uninformed" % (designated_courier.displayname, quest))
                eventmanager = quest_handler.QuestEventManager()
                extrainfo = dict(selected_courier=designated_courier.id, courier_availability=False, detail="courier selected but unavailable")
                eventmanager.setevent(quest, 3, extrainfo)
                #Recursion trigger to get rid of couriers who are on the available_couriers list but are not actually!!
                self.informShippers(quest)
        # Set courier as unavailable
        ## Run the job to inform shippers in queue
        inform_shipper_task.apply_async((quest.id, designated_courier.id), countdown=int(settings.COURIER_SELECTION_DELAY))       
    
    def updateCouriersForQuset(self, quest, courier):
        """Removes a courier from the set of available shippers for a quest"""
        quest = quest_handler.getQuestDetails(quest.id)
        courier = getQuestrDetails(courier.id)
        available_couriers = quest.available_couriers
        available_couriers.pop(courier.id)


class UserEventManager(object):
    """docstring for UserEventManager"""
    
    def __init__(self):
        pass

    def getallevents(self, user):
        """Returns all the events of a user"""
        allevents = UserEvents.objects.filter(questr=user.id)
        return allevents

    def getlatestevent(self, user):
        """Returns the latest event of the user"""
        event = UserEvents.objects.filter(questr=user.id).order_by('-updated_on')[:1]
        return event

    def setevent(self, user, eventtype, extrainfo=None):
        """Sets the event for the user with the type given"""
        eventtype = int(eventtype)
        event = UserEvents(questr=user, event=eventtype, extrainfo=extrainfo, updated_on=timezone.now())
        UserEvents.save(event)
        return "success"