from django import forms
from django.core.validators import FileExtensionValidator
from .models import Application
class ApplicationForm(forms.ModelForm):
    photo=forms.ImageField(required=False,validators=[FileExtensionValidator(['jpg','jpeg','png','webp'])])
    supporting_document=forms.FileField(required=False,validators=[FileExtensionValidator(['pdf','jpg','jpeg','png','webp'])])
    class Meta:
        model=Application
        fields=['full_name','date_of_birth','gender','city','state','postal_code','country','email','phone','qualification','institution','passing_year','grade','employment_status','experience','organization','skills','photo','supporting_document','demo_acknowledged']
        widgets={'date_of_birth':forms.DateInput(attrs={'type':'date'}),'skills':forms.Textarea(attrs={'rows':3}),'demo_acknowledged':forms.CheckboxInput()}
    def clean(self):
        cleaned=super().clean()
        if not cleaned.get('demo_acknowledged'): self.add_error('demo_acknowledged','Please confirm this is a demo application.')
        return cleaned
    def clean_photo(self):
        f=self.cleaned_data.get('photo')
        if f and f.size>3*1024*1024: raise forms.ValidationError('Photo must be 3 MB or smaller.')
        return f
    def clean_supporting_document(self):
        f=self.cleaned_data.get('supporting_document')
        if f and f.size>5*1024*1024: raise forms.ValidationError('Document must be 5 MB or smaller.')
        return f
