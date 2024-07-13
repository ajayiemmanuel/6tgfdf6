from django.contrib import admin

# Register your models here.
from .models import *

admin.site.register (Customer)
admin.site.register(Deposit)
admin.site.register(Ticket)
admin.site.register(Bitcoin)
admin.site.register(Banktransfer)
admin.site.register(Transfer)
admin.site.register(Depositlist)
admin.site.register(Depositlistimage)
admin.site.register(Wallet)
admin.site.register(Pin)