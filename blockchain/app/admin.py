from django.contrib import admin
from django.contrib.auth import get_user_model
from django.contrib.auth.admin import UserAdmin
from .models import (
    User,
    UserKyc,
    Currencies,
    Wallet,
    Proposals,
    Tutorials,
    WatchList,
    SellOrder,
    Transactions
)

User = get_user_model()
# Register your models here.



admin.site.site_title = "Crypto Currency"
admin.site.site_header = "Crypto Currency"
admin.site.index_title = "Crypto Currency"


class UserAdmin(UserAdmin):
    model = User
    list_display = ('email', 'is_staff', 'is_superuser', 'is_active',)
    list_filter = ('email', 'is_staff', 'is_active',)
    fieldsets = (
        (None, {'fields': ('email', 'password')}),
        ('User Info', {
            'classes': ('wide',),
            'fields': ('first_name', 'last_name', 'profile_image')
        }),
        ('Permissions', {'fields': ('is_staff', 'is_superuser', 'is_active')}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'password1', 'password2')}),
        ('User Info', {
            'classes': ('wide',),
            'fields': ('first_name', 'last_name', 'profile_image')
        }),
        ('Permissions', {
            'fields': ('is_staff', 'is_active')
        })
    )
    search_fields = ('email',)
    ordering = ('email',)


admin.site.register(User, UserAdmin)


@admin.register(UserKyc)
class KycAdmin(admin.ModelAdmin):
    list_display = [field.name for field in UserKyc._meta.get_fields()]
    search_fields = ('user__username',)



@admin.register(Wallet)
class WalletAdmin(admin.ModelAdmin):
    list_display = [field.name for field in Wallet._meta.get_fields()]
    search_fields = ('user__username',)


@admin.register(Currencies)
class CurriencyAdmin(admin.ModelAdmin):
    list_display = [field.name for field in Currencies._meta.get_fields()]
    search_fields = ('user__username',)



@admin.register(Proposals)
class ProposalAdmin(admin.ModelAdmin):
    list_display = [field.name for field in Proposals._meta.get_fields()]
    search_fields = ('user__username',)



@admin.register(Tutorials)
class TutorialsAdmin(admin.ModelAdmin):
    list_display = [field.name for field in Tutorials._meta.get_fields()]
    search_fields = ('user__username',)




@admin.register(WatchList)
class WatchListAdmin(admin.ModelAdmin):
    list_display = [field.name for field in WatchList._meta.get_fields()]
    search_fields = ('user__username',)




@admin.register(SellOrder)
class SellOrderAdmin(admin.ModelAdmin):
    list_display = [field.name for field in SellOrder._meta.get_fields()]
    search_fields = ('user__username',)



@admin.register(Transactions)
class TransactionsAdmin(admin.ModelAdmin):
    list_display = [field.name for field in Transactions._meta.get_fields()]
    search_fields = ('user__username',)

