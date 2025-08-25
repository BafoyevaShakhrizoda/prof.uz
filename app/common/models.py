from django.contrib.auth.models import AbstractUser
from django.db import models
from django.core.validators import RegexValidator 


class BaseModel(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True 

class CustomUser(AbstractUser):
    first_name = models.CharField(max_length=30, verbose_name='Ism')
    last_name = models.CharField(max_length=30, verbose_name='Familiya')
    region = models.CharField(max_length=50, verbose_name ='Viloyat')
    district = models.CharField(max_length=50, verbose_name='Tuman')
    classes = models.IntegerField(verbose_name='Sinf')
    letter =  models.CharField(max_length=1, verbose_name='Aa')
    email = models.EmailField(unique=True)
    password_validator = RegexValidator(
        regex = r'^(?=.*[A-Za-z])(?=.*\d)[A-Za-z\d]{8,}$',
        message = 
        """Parol kamida 8 ta belgidan iborat bo'lishi kerak :
            - kamida 1 ta katta harf 
            - kamida 1 ta kichik hark
            - kamida 1 ta raqam
            - maxsus belgilar rossat etilmaydi.
        """  
    )
    password = models.CharField(max_length= 128, validators = [password_validator], verbose_name='parol')
    
    
    class Meta:
        erbose_name='Foydalanuvchi'
        verbose_name_plural='Foydalanuvchilar'
        
    
    def __str__(self):
        return self.first_name + ' ' + self.last_name



    

