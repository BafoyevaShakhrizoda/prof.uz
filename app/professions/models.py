from django.db import models
from app.users.models import BaseModel
from django.contrib.auth import get_user_model
from django.conf import settings


User = get_user_model()


class Occupations(BaseModel):
    name = models.CharField(max_length=100)
    descriptions = models.TextField()
    image = models.ImageField(upload_to='occupations_images/', null = True, blank = True)
    categories = models.CharField(max_length=50, null = True, blank = True)
    about = models.TextField(null = True, blank = True)
    abilities = models.TextField(null = True, blank = True)
    video = models.URLField(null = True, blank = True )
    salary = models.IntegerField(null = True, blank = True)
    job_places = models.TextField(null = True, blank = True)
    similar_to = models.TextField(null = True, blank = True)
    viewed = models.PositiveIntegerField(default=0)
    
    
    class Meta:
        verbose_name = 'Kasb'
        verbose_name_plural = 'Kasblar'
        ordering = ['-viewed']
    
    def __str__(self):
        return f"{self.name}  {self.image}"



class Experts(BaseModel):
    name = models.CharField(max_length= 75)
    image = models.ImageField(upload_to = 'experts_images/', null=True, blank=True)
    profession = models.CharField(max_length=100)
    description = models.TextField()
    intagram = models.URLField(null=True, blank=True)
    linkedin = models.URLField(null=True, blank=True)
    facebook = models.URLField(null=True, blank=True)
    
    class Meta:
        verbose_name = 'Mutaxasis'
        verbose_name_plural = 'Mutaxasislar'
    
    def __str__(self):
        return f"{self.name} - {self.profession} {self.image}"


class Categories(BaseModel):
    FIELD_CHOICES = [
        ('texnologiya', 'Texnologiya'),
        ('sogliq', 'Sog‘liqni saqlash'),
        ('moliya', 'Moliya'),
        ('talim', 'Ta’lim'),
        ('qurilish', 'Qurilish'),
        ('dizayn', 'Dizayn'),
        ('marketing', 'Marketing'),
        ('boshqaruv', 'Boshqaruv'),
    ]
    
    REGION_CHOICES = [
        ('toshkent', 'Toshkent'),
        ('samarqand', 'Samarqand'),
        ('buxoro', 'Buxoro'),
        ('xorazm', 'Xorazm'),
        ('qashqadaryo', 'Qashqadaryo'),
        ('surxondaryo', 'Surxondaryo'),
        ('jizzax', 'Jizzax'),
        ('sirdaryo', 'Sirdaryo'),
        ('namangan', 'Namangan'),
        ('fargona', 'Farg‘ona'),
        ('andijon', 'Andijon'),
        ('qoraqalpogiston', 'Qoraqalpog‘iston'),
        ('navoiy', 'Navoiy'),
        ('barcha hududlar', 'barcha hududlar'),
    ]
    
    SORT_CHOICES = [
        ("talablar yuqori bo'lgan kasblar", "Talablar yuqori bo'lgan kasblar"),
        ('yuqori maoshli kasblar', 'Yuqori maoshli kasblar'),
        ('kam maoshli kasblar', 'Kam maoshli kasblar'),
        ('alifbo tartibida', 'Alifbo tartibida'),
         
    ]
    
    name = models.CharField(max_length=50, unique=True)
    field = models.CharField(max_length=50, choices=FIELD_CHOICES)
    region = models.CharField(max_length=50, choices=REGION_CHOICES)
    sort_by = models.CharField(max_length=100, choices=SORT_CHOICES)
    image = models.ImageField(upload_to='categories_images/', null=True, blank=True)
    salary = models.PositiveIntegerField(null=True, blank=True, verbose_name="O'rtacha maosh (so'mda)")
    description = models.TextField(null=True, blank=True)
    
    class Meta :
        verbose_name = "Kategoriya"
        verbose_name_plural = "Kategoriyalar"
        ordering = ['name']
        
    def __str__(self):
        return self.name


class Videos(BaseModel):
    title = models.CharField(max_length=200)
    duration = models.DurationField()
    video_url = models.URLField()
    description = models.TextField(null=True, blank=True)
    order = models.PositiveIntegerField(verbose_name="Tartib raqami")
    category = models.ForeignKey(Categories, on_delete=models.CASCADE, related_name='videos')
    
    class Meta:
        verbose_name = "Video"
        verbose_name_plural = "Videolar"
        ordering = ['order']
        
    def __str__(self):
        return self.title
  

class StudentSubject(models.Model):
    SUBJECTS = [
        ('Fizika', 'Fizika'), ('Astronomiya', 'Astronomiya'), ('Jismoniy tarbiya', 'Jismoniy tarbiya'),
        ('Musiquiya', 'Musiquiya'), ('Adabiyot', 'Adabiyot'), ('Tasviriy san\'at', 'Tasviriy san\'at'),
        ('Geometriya', 'Geometriya'), ('Matematika', 'Matematika'), ('Ximiya', 'Ximiya'),
        ('Botanika', 'Botanika'), ('Tarix', 'Tarix'), ('Informatica', 'Informatica')
    ]
    student_name = models.CharField(max_length=100)
    subjects = models.JSONField()  

    def __str__(self):
        return f"{self.student_name} - Subjects"

class Profession(models.Model):
    name = models.CharField(max_length=100)
    salary_range = models.CharField(max_length=100)  
    subject_weights = models.JSONField()  
    description = models.TextField(blank=True)

    def __str__(self):
        return self.name

class StudentProfessionMatch(models.Model):
    student = models.ForeignKey(StudentSubject, on_delete=models.CASCADE)
    profession = models.ForeignKey(Profession, on_delete=models.CASCADE)
    match_percentage = models.FloatField() 
    def __str__(self):
        return f"{self.student.student_name} - {self.profession.name} ({self.match_percentage}%)"
    
    
    

