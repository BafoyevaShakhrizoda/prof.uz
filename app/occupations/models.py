from django.db import models
from app.common.models import BaseModel
from django.contrib.auth import get_user_model

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
    
    name = models.CharFiled(max_length=50, unique=True)
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


class Test(BaseModel):
    name = models.CharField(max_length=100)
    questions_number  = models.PositiveInteegerField(verbose_name = 'Savollar soni')
    max_score = models.PositiveInteegerField(verbose_name =' Maksimal ball')
    time_limit  = models.PositiveInteegerField(verbose_name = 'Vaqt cheklovi (daqiqa)', help_text="0 bo'lsa cheklov yo'q")
    is_active = models.BooleanField(default=True, verbose_name='Faol')
    
    class Meta:
        verbose_name = 'Test'
        verbose_name_plural = 'Testlar'
        ordering = ['-created_at']
    
    def __str__(self):
        return self.name


class Question(BaseModel):
    test = models.ForeignKey(Test, on_delete=models.CASCADE, related_name='savollar')
    text = models.TextField(verbose_name="Savol matni")
    image = models.ImageField(upload_to='savol_rasmlari/', blank=True, null=True, verbose_name="Savol rasmi")
    order = models.PositiveIntegerField(verbose_name="Tartib raqami")
    
    class Meta:
        verbose_name = "Savol"
        verbose_name_plural = "Savollar"
        ordering = ['order']
    
    def __str__(self):
        return f"{self.test.name} - {self.order}"

class Option(BaseModel):
    questions = models.ForeignKey(Savol, on_delete=models.CASCADE, related_name='variantlar')
    text = models.CharField(max_length=500, verbose_name="Variant matni")
    true = models.BooleanField(default=False, verbose_name="To'g'ri javob")
    
    class Meta:
        verbose_name = "Variant"
        verbose_name_plural = "Variantlar"
    
    def __str__(self):
        return f"{self.questions.order} - {self.text}"

class Result(BaseModel):
    username = models.ForeignKey(User, on_delete=models.CASCADE, related_name='test_natijalari')
    test = models.ForeignKey(Test, on_delete=models.CASCADE, related_name='natijalar')
    score = models.PositiveIntegerField(verbose_name="Topilgan ball")
    percentage = models.FloatField(verbose_name="Foizda natija")
    finished_time= models.DateTimeField(auto_now_add=True, verbose_name="Tugatilgan vaqt")
    answers = models.JSONField(verbose_name="Foydalanuvchi javoblari", default=dict)
    
    class Meta:
        verbose_name = "Test natijasi"
        verbose_name_plural = "Test natijalari"
        ordering = ['-finished_time']
    
    def __str__(self):
        return f"{self.username.username} - {self.test.name} - {self.percentage}%"
    
    def save(self, *args, **kwargs):
        self.foiz = (self.score / self.test.max_score) * 100
        super().save(*args, **kwargs)



class Videos(BaseModel):
    title = models.CharField(max_length=200)
    duration = models.DurationField()
    video_url = models.URLField()
    description = models.TextField(null=True, blank=True)
    order = models.PositiveIntegerField(verbose_name="Tartib raqami")


class Resume(BaseModel):
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    email = models.EmailField()
    phone = models.CharField(max_length=20)
    birth_date = models.DateField()
    gender = models.CharField(max_length=10, choices=[('Male', 'Male'), ('Female', 'Female'), ('Other', 'Other')])
    nationality = models.CharField(max_length=50)
    address = models.TextField()
    education = models.TextField()
    experience = models.TextField()
    skills = models.TextField()

    def __str__(self):
        return f"{self.first_name} {self.last_name} - Resume"

class Profile(BaseModel):
    user = models.OneToOneField('auth.User', on_delete=models.CASCADE)
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    email = models.EmailField()
    phone = models.CharField(max_length=20)
    gender = models.CharField(max_length=10, choices=[('Male', 'Male'), ('Female', 'Female'), ('Other', 'Other')])
    nationality = models.CharField(max_length=50)
    address = models.TextField()
    profession = models.CharField(max_length=100)
    resume = models.ForeignKey(Resume, on_delete=models.SET_NULL, null=True, blank=True)

    def __str__(self):
        return f"{self.first_name} {self.last_name} - Profile"
    

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
    
    
    

