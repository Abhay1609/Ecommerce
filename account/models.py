from django.db import models
from django.urls import reverse
from django.contrib.auth.models import AbstractBaseUser,BaseUserManager
from django.utils import timezone
from rest_framework_simplejwt.tokens import RefreshToken
from django.core.validators import MinValueValidator, MaxValueValidator
from django.utils.translation import gettext_lazy as _





class UserManager(BaseUserManager):
    def create_user(self,email, full_name ,gender,mobile_number,password2,is_seller, password=None):
        """
        Creates and saves a User with the given email, name ,tc and password.
        """
        if not mobile_number:
            raise ValueError('Users must have a Mobile Number.')
        if not email:
            raise ValueError('Users must have a Email.')



        user = self.model(
             mobile_number=mobile_number,
            email=self.normalize_email(email),
            is_seller=is_seller,

            full_name=full_name,
            gender=gender,

            password2=password2
        )

        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, full_name,  gender, mobile_number, password2,password=None):
        """
        Creates and saves a superuser with the given email, name , tc and password.
        """
        if not mobile_number:
            raise ValueError('Users must have a Mobile number.')
        if not email:
            raise ValueError('Users must have a Email.')
        user = self.create_user(

            mobile_number=mobile_number,
            password=password,
            email=email,

            full_name=full_name,
            gender=gender,

            password2=password2

        )
        user.is_admin = True
        user.save(using=self._db)
        return user


class User(AbstractBaseUser):
    full_name=models.CharField(max_length=200,null=True)
    email=models.EmailField(unique=True)

    mobile_number=models.CharField(max_length=10,unique=True)
    gender=models.CharField(max_length=10,null=True)
    is_customer=models.BooleanField(default=True)
    is_seller=models.BooleanField(default=False)

    isverified=models.BooleanField(default=False)
    is_admin=models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    # is_superuser = models.BooleanField(default=False)
    password2=models.CharField(max_length=40)



    objects=UserManager()


    USERNAME_FIELD='mobile_number'
    REQUIRED_FIELDS= ['email','full_name','gender','password2','is_seller']

    def __str__(self):
        return self.full_name+  ' , ' +self.mobile_number

    def has_perm(self, perm, obj=None):
        "Does the user have a specific permission?"
        # Simplest possible answer: Yes, always
        return self.is_admin

    def has_module_perms(self, app_label):
        "Does the user have permissions to view the app `app_label`?"
        # Simplest possible answer: Yes, always
        return True

    @property
    def is_staff(self):
        "Is the user a member of staff?"
        # Simplest possible answer: All admins are staff
        return self.is_admin

    def tokens(self):
        refresh=RefreshToken.for_user(self)
        return{
            'refresh': str(refresh),
            'access':str(refresh.access_token)
        }
class Customer(models.Model):
    user=models.OneToOneField(User,on_delete=models.CASCADE)
    address=models.CharField(max_length=255)

class Seller(models.Model):
    user=models.OneToOneField(User,on_delete=models.CASCADE)
    gst=models.CharField(max_length=255)
    warehouse_location=models.CharField(max_length=255)

# Create your models here.
