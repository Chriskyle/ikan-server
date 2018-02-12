from django.contrib import admin

# Register your models here.
from ikan.models import Feed, Account, Category, Segment, Solution, Version, Notification, Denomination, Recommend

admin.site.register(Account)
admin.site.register(Feed)
admin.site.register(Category)
admin.site.register(Segment)
admin.site.register(Solution)
admin.site.register(Version)
admin.site.register(Notification)
admin.site.register(Denomination)
admin.site.register(Recommend)
