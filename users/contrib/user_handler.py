

from random import choice
from collections import OrderedDict 
from django.conf import settings
from django.shortcuts import render
from django.http import Http404

import logging

from quests.contrib import quest_handler
from libs import email_notifier, geomaps

from users.models import QuestrUserProfile, UserTransactional, QuestrToken
from quests.models import Quests
from quests.tasks import inform_shipper_task

logger = logging.getLogger(__name__)

def get_random_password():
	"""
	Generates a random password.
	"""
	random_password = ''.join([choice('1234567890qwertyuiopasdfghjklzxcvbnm') for i in range(7)])
	return random_password

def prepPasswordResetNotification(questr, new_password):
    """Prepare the details for notification of resetting of password"""
    template_name="RESET_PASSWORD_EMAIL"
    subject="Questr - Your password has been reset !"
    quest_support_email="support@questr.co"
    questr_unsubscription_link="http://questr.co/unsub"

    email_details = {
                        'subject' : subject,
                        'template_name' : template_name,
                        'global_merge_vars': {
                                                'questr_first_name'   : questr.first_name,
                                                'questr_last_name'   : questr.last_name,
                                                'new_password'      : new_password,
                                                'quest_support_mail': quest_support_email,
                                                'questr_unsubscription_link' : questr_unsubscription_link,
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
    questr_unsubscription_link="http://questr.co/unsub"

    email_details = {
                        'subject' : subject,
                        'template_name' : template_name,
                        'global_merge_vars': {
                                                'questr_first_name'   : questr.first_name,
                                                'questr_last_name'   : questr.last_name,
                                                'quest_support_mail': quest_support_email,
                                                'questr_unsubscription_link' : questr_unsubscription_link,
                                                'company'           : "Questr Co",
                                                'verf_link'         : verf_link,
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
            prev_transactional = UserTransactional.objects.get(email = user.email, status = False)
            if prev_transactional:
                prev_transactional.status = True
                prev_transactional.save()
        except UserTransactional.DoesNotExist:
            pass
        count = UserTransactional.objects.count()
        transcational = UserTransactional(id=count+1,email=user.email)
        transcational.save()
        token_id = transcational.get_token_id()
        questr_token = QuestrToken(token_id=token_id)
        questr_token.save()
        verf_link = "{0}/user/email/confirm/{1}?questr_token={2}".format(settings.QUESTR_URL , transcational.get_truncated_user_code(), token_id)
    return verf_link

def getShipper(shipper_id):
    """List shipper information"""
    try:
        shipper = QuestrUserProfile.objects.filter(id=shipper_id, is_active=True)
    except QuestrUserProfile.DoesNotExist:
        raise Http404
        return render('404.html', locals())
    return shipper

def getQuestrDetails(questr_id):
    """List shipper information"""
    try:
        questr = QuestrUserProfile.objects.get(id=questr_id, is_active=True)
    except QuestrUserProfile.DoesNotExist:
        raise Http404
        return render('404.html', locals())
    return questr

def getShippers():
    """List all the shippers"""
    shippers = QuestrUserProfile.objects.filter(is_shipper=True, is_active=True)
    return shippers

def getShippersOfQuest(questname):
    """List of shippers for a given quest"""
    shippers = str(Quests.objects.get(id=questname).shipper).split(',')
    return shippers

def isShipper(user):
    """Checks if the user is a shipper or a regular questr"""
    if user.is_shipper == True:
        return True #is a shipper
    return False #is a regular questr

def getAccountStatus(status_id):
    '''Get account status of user'''
    status_list = ["Normal","Starred","Warned","Suspended","Closed"]
    if status_id < len(status_list):
        return status_list[status_id]

def isActive(status):
    """Returns if the account is active for the user"""
    return "Yes" if status else "No"

def isEmailVerified(status):
    """Returns if the email of the user has been verified"""
    return "Yes" if status else "No"

def usernameExists(user):
    """Checks if the user by the provided displayname exists already"""
    try:
        user = QuestrUserProfile.objects.get(displayname=user)
    except QuestrUserProfile.DoesNotExist:
        return False
    if user:
        return True

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
        
def emailExists(email):
    """Checks if the user with the provided email exists already"""
    try:
        user = QuestrUserProfile.objects.get(email=email)
    except QuestrUserProfile.DoesNotExist:
        return False
    if user:
        return True

def updateCourierAvailability(questr, status):
    """Takes a Questr User Profile object and a status ( 0 | 1 ) and updates the availability status as per the same"""
    status = int(status)
    if userExists(questr.id):
        if status == 0:
            statusupdate = QuestrUserProfile.objects.filter(id=questr.id, is_active=True).update(is_available=False)
            if statusupdate == 1:
                return dict(status='success')
            return dict(status="fail")
        elif status == 1:
            statusupdate = QuestrUserProfile.objects.filter(id=questr.id, is_active=True).update(is_available=True)
            if statusupdate == 1:
                return dict(status='success')
            return dict(status="fail")
        else :
            raise ValueError('Status %d not acceptable, use 0 or 1' % (status))
    return dict(status='fail')


class CourierManager(object):
    """This is the manager that processes and assigns couriers automatically"""
    
    def __init__(self):
        pass

    def getActiveCouriers(self):
        """Returns a list of couriers"""
        try:
            courierlist = QuestrUserProfile.objects.filter(is_shipper=True, is_superuser=False, is_available=True, is_active=True)
        except Exception, e:
            raise e

        return courierlist

    def getCourierAvailability(self, courier):
        """Returns if a courier is available"""
        courier_details = getQuestrDetails(courier)
        return courier_details.is_available

    def updateCourierAvailability(questr, status):
        """Takes a Questr User Profile object and a status ( 0 | 1 ) and updates the availability status as per the same"""
        status = int(status)
        if userExists(questr.id):
            if status == 0:
                statusupdate = QuestrUserProfile.objects.filter(id=questr.id, is_active=True).update(is_available=False)
                if statusupdate == 1:
                    return dict(status='success')
                return dict(status="fail")
            elif status == 1:
                statusupdate = QuestrUserProfile.objects.filter(id=questr.id, is_active=True).update(is_available=True)
                if statusupdate == 1:
                    return dict(status='success')
                return dict(status="fail")
            else :
                raise ValueError('Status %d not acceptable, use 0 or 1' % (status))
        return dict(status='fail')

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
            activecouriers = self.getActiveCouriers()
            if len(activecouriers) == 0:
                logger.warn("No active couriers in the system now")
                ##* inform the master couriers
                dothis = self.informSuperAdmins(quest)
                questdetails = Quests.objects.get(id=int(quest.id))
                if dothis == "success":
                    logger.warn("Master Couriers have been informed as no shippers were available for quest %d" % (quest.id))
                    questdetails.isaccepted = True
                    questdetails.shipper = 0
                    questdetails.save()
                    return "fail"
                else:
                    # Man we have a problem return 500 NO SHIPPERS AVAILABLE NOW, ASK THE USER TO HIT "process quest"
                    # "process quest" will have to be put somewhere in his dashboard of quest which are not honored
                    logger.warn("Some serious problem")        
            available_couriers = self.getAvailableCouriersWithProximity(activecouriers, quest)
            ## Updating the respecitve quest with courier details
            quest_handler.updateQuestWithAvailableCourierDetails(quest, available_couriers)
        quest = quest_handler.getQuestDetails(quest.id)
        couriers_list = self.getCouriersInProximity(quest)
        if len(couriers_list) == 0:
            couriers_list = self.getCouriersNotInProximity(quest)

        designated_courier = getQuestrDetails(couriers_list[0][0])
        self.informCourier(designated_courier, quest)
        # Set courier as unavailable
        self.updateCourierAvailability(designated_courier, 0) 
        ## Run the job to inform shippers in queue
        inform_shipper_task.apply_async((quest.id, designated_courier.id), countdown=settings.COURIER_SELECTION_DELAY)       
    
    def updateCouriersForQuset(self, quest, courier):
        """Removes a courier from the set of available shippers for a quest"""
        quest = quest_handler.getQuestDetails(quest.id)
        courier = getQuestrDetails(courier.id)
        available_couriers = quest.available_couriers
        available_couriers.pop(courier.id)
