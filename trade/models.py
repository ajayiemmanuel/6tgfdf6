from django.db import models
from django.contrib.auth.models import User
from django.dispatch import receiver
from django.db.models.signals import pre_save, post_save
from django.db import models

class Customer (models.Model):
    user = models.OneToOneField (User, null = True, blank = True, on_delete = models.CASCADE)
    name = models.CharField (max_length = 200,  null = True)
    first_name = models.CharField (max_length = 200,  null = True)
    last_name = models.CharField (max_length = 200,  null = True)
    email = models.CharField (max_length = 200, null = True)
    phone_number = models.CharField (max_length = 200, null = True)
    address = models.CharField (max_length = 200, null = True)
    country = models.CharField (max_length = 200, null = True)
    gender = models.CharField (max_length = 200, null = True)
    profile_pic = models.ImageField (default = "avater.png", null = True, blank = True)
    bio = models.TextField (max_length = 200, null = True)

    def __str__(self):
        return str(self.name)

class Deposit (models.Model):
    user = models.OneToOneField (User, null = True, blank = True, on_delete = models.CASCADE)
    name = models.CharField (max_length = 200,  null = True)
    deposit_wallet_balance = models.CharField (max_length = 200,  null = True, default = "10")
    total_deposit_balance = models.CharField (max_length = 200,  null = True, default = "0")
    interest_balance = models.CharField (max_length = 200, null = True, default = "0")
    total_withdraw = models.CharField (max_length = 200, null = True, default = "0")
    time = models.DateField(auto_now=True)
    trnsaction_id = models.CharField (max_length = 200, null = True, default = "GHGSH4748HDH")


    def __str__(self):
        return str(self.name)

class Ticket (models.Model):
    user = models.ForeignKey(
        User, on_delete=models.SET_NULL, null=True, blank=True)
    name = models.CharField (max_length = 200,  null = True)
    email = models.EmailField (max_length = 200,  null = True)
    subject = models.CharField (max_length = 200,  null = True)
    message = models.TextField (max_length = 200, null = True)
    picture = models.ImageField (max_length = 200, null = True)
    status = models.CharField (max_length = 200, null = True)

    def __str__(self):
        return str(self.name)

level = (
    ('Pending...', 'Pending...'),
    ('Approved', 'Approved'),
    ('Declined', 'Declined'),

    )


class Bitcoin (models.Model):
    user = models.ForeignKey(
        User, on_delete=models.SET_NULL, null=True, blank=True)
    name = models.CharField (max_length = 200,  null = True)   
    wallet = models.CharField (max_length = 200,  null = True)
    address = models.CharField (max_length = 200,  null = True)
    amount = models.CharField (max_length = 200,  null = True)
    purpose = models.TextField (max_length = 200, null = True)
    time = models.DateField (auto_now=True)
    transactionid = models.CharField (max_length = 200, null = True, default='FDG637GDJYU**')
    status = models.CharField (max_length = 200, choices=level, default='Pending...' )
    rate = models.CharField (max_length = 200, null = True)

    def __str__(self):
        return str(self.name)


status = (
    ('Pending...', 'Pending...'),
    ('Approved', 'Approved'),
    ('Declined', 'Declined'),

    )


class Banktransfer (models.Model):
    user = models.ForeignKey(
        User, on_delete=models.SET_NULL, null=True, blank=True)
    name = models.CharField (max_length = 200,  null = True)   
    wallet = models.CharField (max_length = 200,  null = True)
    bank = models.CharField (max_length = 200,  null = True)
    accountnumber = models.CharField (max_length = 200,  null = True)
    swift = models.CharField (max_length = 200,  null = True)
    amount = models.CharField (max_length = 200,  null = True)
    purpose = models.TextField (max_length = 200, null = True)
    time = models.DateField (auto_now=True)
    transactionid = models.CharField (max_length = 200, null = True, default='FDG637GDJYU**')
    status = models.CharField (max_length = 200, choices=status, default='Pending...' )
    purpose = models.TextField (max_length = 200, null = True)
    rate = models.CharField (max_length = 200, null = True)



    def __str__(self):
        return str(self.name)

class Transfer (models.Model):
    user = models.ForeignKey(
        User, on_delete=models.SET_NULL, null=True, blank=True)
    wallet = models.CharField (max_length = 200,  null = True)
    name = models.CharField (max_length = 200,  null = True)   
    amount = models.CharField (max_length = 200,  null = True)
    time = models.DateField (auto_now=True)
    transactionid = models.CharField (max_length = 200, null = True, default='FDG637GDJYU**')
    status = models.CharField (max_length = 200, choices=status, default='Pending...' )
    rate = models.CharField (max_length = 200, null = True)

    def __str__(self):
        return str(self.name)


class Depositlist (models.Model):
    user = models.OneToOneField (User, null = True, blank = True, on_delete = models.CASCADE)
    name = models.CharField (max_length = 200,  null = True)
    amount = models.CharField (max_length = 200,  null = True)
    time = models.DateField (auto_now=True)
    transactionid = models.CharField (max_length = 200, null = True, default='FDG637GDJYU**')
    status = models.CharField (max_length = 200, choices=status, default='Pending...' )
    rate = models.CharField (max_length = 200, null = True, default='4')

    def __str__(self):
        return str(self.name)

class Depositlistimage (models.Model):
    user = models.OneToOneField (User, null = True, blank = True, on_delete = models.CASCADE)
    name = models.CharField (max_length = 200,  null = True)
    slip = models.ImageField (max_length = 200,  null = True)

    def __str__(self):
        return str(self.name)


class Wallet (models.Model):
    user = models.OneToOneField (User, null = True, blank = True, on_delete = models.CASCADE)
    name = models.CharField (max_length = 200,  null = True)
    wallet = models.CharField (max_length = 200,  null = True)

    def __str__(self):
        return str(self.name)

class Pin (models.Model):
    user = models.OneToOneField (User, null = True, blank = True, on_delete = models.CASCADE)
    name = models.CharField (max_length = 200,  null = True)
    pin = models.CharField (max_length = 200,  null = True, default='0000')

    def __str__(self):
        return str(self.name)