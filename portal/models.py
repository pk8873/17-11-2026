import uuid
from django.db import models
from django.utils import timezone
class BankProfile(models.Model):
    name=models.CharField(max_length=120,unique=True)
    short_name=models.CharField(max_length=24,blank=True)
    logo=models.ImageField(upload_to='bank_logos/',blank=True,null=True)
    primary_color=models.CharField(max_length=7,default='#12345b')
    accent_color=models.CharField(max_length=7,default='#c49a52')
    description=models.CharField(max_length=240,blank=True)
    footer_text=models.CharField(max_length=240,blank=True)
    active=models.BooleanField(default=True)
    created_at=models.DateTimeField(auto_now_add=True)
    class Meta: ordering=['name']
    def __str__(self): return self.name
class Vacancy(models.Model):
    bank=models.ForeignKey(BankProfile,on_delete=models.PROTECT,related_name='vacancies')
    title=models.CharField(max_length=150)
    department=models.CharField(max_length=100,default='General Banking')
    openings=models.PositiveIntegerField(default=1)
    qualification=models.CharField(max_length=240,default='Graduation in any discipline')
    age_criteria=models.CharField(max_length=120,default='18–30 years (demo criteria)')
    description=models.TextField()
    selection_process=models.CharField(max_length=240,default='Written test · Interview (demo)')
    opening_date=models.DateField(default=timezone.localdate)
    closing_date=models.DateField()
    active=models.BooleanField(default=True)
    created_at=models.DateTimeField(auto_now_add=True)
    class Meta: ordering=['closing_date','title']
    def __str__(self): return f'{self.title} — {self.bank.name}'
class Application(models.Model):
    reference=models.UUIDField(default=uuid.uuid4,unique=True,editable=False)
    vacancy=models.ForeignKey(Vacancy,on_delete=models.PROTECT,related_name='applications')
    full_name=models.CharField(max_length=140)
    date_of_birth=models.DateField()
    gender=models.CharField(max_length=30)
    city=models.CharField(max_length=80); state=models.CharField(max_length=80)
    postal_code=models.CharField(max_length=12); country=models.CharField(max_length=60,default='India')
    email=models.EmailField(blank=True); phone=models.CharField(max_length=20,blank=True)
    qualification=models.CharField(max_length=120); institution=models.CharField(max_length=160)
    passing_year=models.PositiveIntegerField(); grade=models.CharField(max_length=30,blank=True)
    employment_status=models.CharField(max_length=40); experience=models.CharField(max_length=80,blank=True)
    organization=models.CharField(max_length=140,blank=True); skills=models.TextField(blank=True)
    photo=models.ImageField(upload_to='applicants/photos/',blank=True,null=True)
    supporting_document=models.FileField(upload_to='applicants/documents/',blank=True,null=True)
    submitted_at=models.DateTimeField(auto_now_add=True); demo_acknowledged=models.BooleanField(default=False)
    class Meta: ordering=['-submitted_at']
    def __str__(self): return f'{self.full_name} — {self.reference}'
