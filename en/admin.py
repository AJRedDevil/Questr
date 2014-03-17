from django.contrib import admin
from en.models import User, Quest, OfferBid, Offer, QuestBid, Location


class UserAdmin(admin.ModelAdmin):
    fieldsets = [
        (None,               {'fields': ['name']}),
        (None,               {'fields': ['email']}),
        (None,               {'fields': ['ratings']}),
        ('Date information', {'fields': ['reg_date']}),
    ]

class QuestAdmin(admin.ModelAdmin):
    fieldsets = [
        (None,               {'fields': ['user']}),
        (None,               {'fields': ['location1']}),
        (None,               {'fields': ['location2']}),
        (None,               {'fields': ['bounty']}),
        ('Date information', {'fields': ['pub_date']}),
    ]







admin.site.register(User, UserAdmin)



admin.site.register(Quest, QuestAdmin)
admin.site.register(OfferBid)
admin.site.register(Location)
