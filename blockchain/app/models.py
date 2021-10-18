from django.db import models  # noqa: F401
from django.contrib.auth.base_user import BaseUserManager
from django.contrib.auth.models import AbstractUser
from django.db.models.base import Model


class CustomUserManager(BaseUserManager):
    """
    Custom user model manager where email is the unique identifiers
    for authentication instead of usernames.
    """
    def create_user(self, email, password, **extra_fields):
        """
        Create and save a User with the given email and password.
        """
        if not email:
            raise ValueError('The Email must be set')
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save()
        return user

    def create_superuser(self, email, password, **extra_fields):
        """
        Create and save a SuperUser with the given email and password.
        """
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('is_active', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')
        return self.create_user(email, password, **extra_fields)


def upload_profile(instance, filename):
    return "Profiles/{user}/{filename}".format(user='{0}_{1}'.format(instance.first_name, instance.last_name),
                                               filename=filename)

GENDER = [('Male', 'Male'), ('Female', "Female")]
 

class User(AbstractUser):
    # username 
    # first_name
    # last_name
    # password
    # password2
    id = models.BigAutoField(primary_key=True)
    email = models.EmailField(unique=True)
    date_of_birth = models.DateField(blank=True, null=True)
    phone_no = models.CharField(max_length=14)
    age = models.PositiveIntegerField(default=18)
    gender = models.CharField(max_length=15, choices=GENDER, verbose_name='Gender')
    address = models.CharField(max_length=150, null=True, blank=True)
    creadit_card = models.CharField(max_length=15, null=True, blank=True)
    profile_image = models.ImageField(
                        upload_to=upload_profile,
                        default='Profiles/user/user.png',
                        null=True, blank=True
    )

    is_verified = models.BooleanField(default=False)
    created_date = models.DateTimeField(auto_now_add=True)
    updated_date = models.DateTimeField(auto_now=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    objects = CustomUserManager()


    def __str__(self):
        return self.email




class UserKyc(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='user_kyc', verbose_name='User')
    kyc_documents = models.FileField(upload_to='uploads/KYC/%Y/%m/%d/')
    is_approved = models.BooleanField(default=False)
    remarks = models.CharField(max_length=500, null=True, blank=True)

    created_date = models.DateTimeField(auto_now_add=True)
    updated_date = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = 'KYC Documents'

    def __str__(self) -> str:
        return self.user.username


class Currencies(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    currency = models.CharField(max_length=4, unique=True)
    total_amount = models.PositiveBigIntegerField(default=100000000)
    remaining_amount = models.PositiveBigIntegerField()

    created_date = models.DateTimeField(auto_now_add=True)
    updated_date = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = 'Wallet'
    
    def __str__(self) -> str:
        return 
    



class Wallet(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='wallet', verbose_name='User')
    currency = models.ForeignKey(Currencies, on_delete=models.CASCADE, related_name='wallet_currency', verbose_name='Currency')
    balance = models.PositiveBigIntegerField(default=0)

    created_date = models.DateTimeField(auto_now_add=True)
    updated_date = models.DateTimeField(auto_now=True)


    class Meta:
        verbose_name = 'Wallet'
        unique_together = ('user', 'currency',)

    def __str__(self) -> str:
        return '{} Wallet'.format(self.user.username)