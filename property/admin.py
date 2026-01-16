from django.contrib import admin
from .models import Flat, Complain, Owner


class OwnershipInline(admin.TabularInline):
    model = Flat.owned_by.through
    raw_id_fields = ('owner',)


@admin.register(Flat)
class FlatAdmin(admin.ModelAdmin):
    search_fields = ('town', 'town_district', 'address', 'owner')
    readonly_fields = ('created_at',)
    list_display = ('address', 'price', 'new_building', 'construction_year')
    list_editable = ('new_building',)
    list_filter = ('new_building', 'rooms_number', 'has_balcony')
    raw_id_fields = ('likes',)
    inlines = (OwnershipInline,)


@admin.register(Complain)
class ComplainAdmin(admin.ModelAdmin):
    raw_id_fields = ('user', 'flat')


@admin.register(Owner)
class OwnerAdmin(admin.ModelAdmin):
    search_fields = ('name', 'pure_phone_number')
    readonly_fields = ('pure_phonenumber',)
    list_display = ('name', 'phonenumber', 'pure_phonenumber')
    raw_id_fields = ('flats',)
