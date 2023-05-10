from django.contrib import admin

from .models import Achievement, AchievementCat, Cat

admin.site.register(Achievement)
admin.site.register(AchievementCat)
admin.site.register(Cat)
