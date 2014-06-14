from quests.models import Quests

# Create your views here.
def listfeaturedquests():
    """List all the featured quests"""
    allquests = Quests.objects.all()
    return allquests

def getQuestsByUser(questrs_id):
    """List all the quests by a particular user"""
    questsbysuer = Quests.objects.filter(questrs_id=questrs_id)
    return questsbysuer

def prepNewQuestNotification(user, questdetails):
    """Prepare the details for notification emails for new quests"""
    template_name="New_Quest_Notification"
    subject="New Quest Notification"
    quest_browse_link="http://questr.co/quest"
    quest_support_email="support@questr.co"
    questr_unsubscription_link="http://questr.co/unsub"

    email_details = {
                        'subject' : subject,
                        'template_name' : template_name,
                        'global_merge_vars': {
                                                'quest_public_link' : "http://questr.co/quest/"+str(questdetails.id),
                                                'quest_description' : questdetails.description,
                                                'user_first_name'   : user.first_name,
                                                'email_unsub_link'  : questr_unsubscription_link,
                                                'quest_title'       : questdetails.title,
                                                'quest_reward'      : str(questdetails.reward),
                                                'quest_browse_link' : quest_browse_link,
                                                'quest_support_mail': quest_support_email,
                                                'recipient_id'      : user.id,
                                                'questr_unsubscription_link' : questr_unsubscription_link,
                                                'company'           : "Questr Co"

                                                },
                    }
    return email_details