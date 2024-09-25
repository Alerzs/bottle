from django.contrib.admin import register , ModelAdmin
from .models import Survivior ,Island ,Bottle ,Shop


@register (Survivior)
class SurAdmin(ModelAdmin):
    list_display = [
        'user',
        'points',
    ]
    filter_horizontal = ['inventory']

@register (Island)
class IslandAdmin(ModelAdmin):
    list_display = [
        'owner',
        'lat',
        'long'
    ]

@register (Bottle)
class BottleAdmin(ModelAdmin):
    list_display = [
        'sender',
        'reciver',
        'radius',
        'text'
    ]

@register (Shop)
class ShopAdmin(ModelAdmin):
    list_display=[
        'name',
        'cost',
        'max_length',
        'radius'
    ]