from django.db import models
from django.contrib.auth.models import AbstractBaseUser,UserManager,PermissionsMixin


class MYAccountManager(UserManager):
    def _create_user(self,first_name,username,last_name,email,phone_number,role,password=None,**extra):
        if not email:
            raise ValueError("Email is not provided")
        if not username:
            raise ValueError("Username is not provided")
        if not role:
            raise ValueError("You have to select the role")
        user=self.model(
            email=self.normalize_email(email),
            username=username,
            first_name=first_name,
            last_name=last_name,
            phone_number=phone_number,
            role=role,
        )
        user.set_password(password) #inbuild 
        user.save(using=self._db)
        return user
    
    def create_superuser(self, first_name, username, last_name, email, password,phone_number,role):
        user = self._create_user(
            first_name=first_name,
            username=username,
            last_name=last_name,
            email=self.normalize_email(email),
            password=password,
            phone_number=phone_number,
            role=role

        )
        user.is_admin = True
        user.is_staff=True
        user.is_active = True
        user.is_superadmin = True
        user.save(using=self._db)
        return user
    
    def create_user(self,first_name,username,last_name,email,phone_number,role,password=None,**extra):
        user=self._create_user(first_name,username,last_name,email,phone_number,role,password,**extra)
        user.is_staff=True
        user.is_active=True
        user.save(using=self._db)
        return user


class Account(AbstractBaseUser,PermissionsMixin):
    profile_pictue=models.ImageField(upload_to='photos/accounts',null=True,blank=True)
    first_name=models.CharField(max_length=50)
    last_name=models.CharField(max_length=50)
    username=models.CharField(max_length=100,unique=True)
    email=models.EmailField(max_length=100,unique=True)
    phone_number=models.IntegerField(null=True,blank=True)
    role = models.CharField(max_length=10, choices=[('vendor', 'Vendor'), ('customer', 'Customer')])
    date_joined=models.DateTimeField(auto_now_add=True)
    last_login=models.DateTimeField(auto_now=True)
    is_admin=models.BooleanField(default=False)
    is_superadmin=models.BooleanField(default=False)
    is_staff=models.BooleanField(default=False)
    is_active=models.BooleanField(default=False)
    USERNAME_FIELD='email'
    REQUIRED_FIELDS=['username','first_name','last_name','phone_number','role']

    def __str__(self):
        return self.email

    
    def has_perm(self,perm,obj=None):
        return self.is_admin or super().has_perm(perm, obj)     

    def has_module_perms(self,add_label):
        return True
    objects=MYAccountManager()

