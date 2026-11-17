import io
from django.contrib import messages
from django.http import Http404,HttpResponse
from django.shortcuts import get_object_or_404,redirect,render
from django.utils import timezone
from reportlab.lib import colors
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import getSampleStyleSheet,ParagraphStyle
from reportlab.lib.units import mm
from reportlab.platypus import SimpleDocTemplate,Paragraph,Spacer,Table,TableStyle
from .models import BankProfile,Vacancy,Application
from .forms import ApplicationForm
def seed_demo_data():
    if not BankProfile.objects.exists():
        bank=BankProfile.objects.create(name='National Finance Demo Bank',short_name='NFDB',description='A fictional institution for recruitment workflow testing.',footer_text='Independent software demonstration · No real recruitment')
        Vacancy.objects.create(bank=bank,title='Junior Banking Associate (Demo)',department='Branch Operations',openings=12,qualification='Graduation in any discipline (sample criteria)',age_criteria='18–30 years (sample only)',description='A fictional vacancy used to test the recruitment application workflow.',closing_date=timezone.localdate()+timezone.timedelta(days=45))
def home(request):
    seed_demo_data(); banks=BankProfile.objects.filter(active=True); latest=Vacancy.objects.filter(active=True,bank__active=True).select_related('bank')[:3]
    return render(request,'portal/home.html',{'banks':banks,'vacancies':latest})
def vacancies(request):
    seed_demo_data(); qs=Vacancy.objects.filter(active=True,bank__active=True).select_related('bank'); bank_id=request.GET.get('bank'); q=request.GET.get('q','').strip()
    if bank_id and bank_id.isdigit(): qs=qs.filter(bank_id=bank_id)
    if q: qs=qs.filter(title__icontains=q)
    return render(request,'portal/vacancies.html',{'vacancies':qs,'banks':BankProfile.objects.filter(active=True),'selected_bank':bank_id or '','query':q})
def apply(request,vacancy_id):
    vacancy=get_object_or_404(Vacancy,pk=vacancy_id,active=True,bank__active=True)
    if request.method=='POST':
        form=ApplicationForm(request.POST,request.FILES)
        if form.is_valid():
            application=form.save(commit=False); application.vacancy=vacancy; application.save(); messages.success(request,'Your demo application has been recorded.'); return redirect('confirmation',reference=application.reference)
    else: form=ApplicationForm()
    return render(request,'portal/apply.html',{'form':form,'vacancy':vacancy})
def get_application(reference):
    try: return Application.objects.select_related('vacancy__bank').get(reference=reference)
    except (Application.DoesNotExist,ValueError): raise Http404('Demo application not found.')
def confirmation(request,reference): return render(request,'portal/confirmation.html',{'application':get_application(reference)})
def receipt_pdf(request,reference):
    app=get_application(reference); buffer=io.BytesIO(); doc=SimpleDocTemplate(buffer,pagesize=A4,rightMargin=18*mm,leftMargin=18*mm,topMargin=18*mm,bottomMargin=18*mm)
    styles=getSampleStyleSheet(); title=ParagraphStyle('DemoTitle',parent=styles['Title'],textColor=colors.HexColor('#12345b'),fontSize=18,spaceAfter=8); small=ParagraphStyle('SmallDemo',parent=styles['Normal'],textColor=colors.HexColor('#9b2c2c'),fontSize=9,alignment=1)
    story=[Paragraph('DEMO RECRUITMENT PORTAL',title),Paragraph('NOT AN OFFICIAL BANK WEBSITE · TEST RECEIPT ONLY',small),Spacer(1,8*mm),Paragraph(app.vacancy.bank.name,styles['Heading2']),Paragraph('Application receipt',styles['Heading1']),Paragraph(f'<b>Reference:</b> {app.reference}',styles['Normal']),Paragraph(f'<b>Submitted:</b> {timezone.localtime(app.submitted_at).strftime("%d %B %Y, %I:%M %p")}',styles['Normal']),Spacer(1,5*mm)]
    rows=[['Field','Submitted demo information'],['Applicant',app.full_name],['Date of birth',app.date_of_birth.strftime('%d-%m-%Y')],['Gender',app.gender],['Location',f'{app.city}, {app.state}, {app.postal_code}, {app.country}'],['Email / Phone',f'{app.email or "Not provided"} / {app.phone or "Not provided"}'],['Qualification',f'{app.qualification} — {app.institution} ({app.passing_year})'],['Grade',app.grade or 'Not provided'],['Employment',f'{app.employment_status} — {app.experience or "Not specified"}'],['Organization',app.organization or 'Not provided'],['Skills',app.skills or 'Not provided'],['Recruitment',app.vacancy.title],['Department',app.vacancy.department],['Status','DEMO SUBMISSION RECORDED']]
    table=Table(rows,colWidths=[42*mm,125*mm],repeatRows=1); table.setStyle(TableStyle([('BACKGROUND',(0,0),(-1,0),colors.HexColor('#12345b')),('TEXTCOLOR',(0,0),(-1,0),colors.white),('GRID',(0,0),(-1,-1),.4,colors.HexColor('#d7dee8')),('VALIGN',(0,0),(-1,-1),'TOP'),('BACKGROUND',(0,1),(0,-1),colors.HexColor('#f1f4f8')),('FONTNAME',(0,0),(-1,0),'Helvetica-Bold'),('FONTSIZE',(0,0),(-1,-1),9),('LEFTPADDING',(0,0),(-1,-1),7),('RIGHTPADDING',(0,0),(-1,-1),7),('TOPPADDING',(0,0),(-1,-1),7),('BOTTOMPADDING',(0,0),(-1,-1),7)]))
    story.extend([table,Spacer(1,8*mm),Paragraph('<b>DEMO NOTICE:</b> This is a demonstration application only. It has not been submitted to any actual bank, employer, or recruitment authority. No selection, approval, verification, or employment is implied.',styles['BodyText'])]); doc.build(story)
    response=HttpResponse(buffer.getvalue(),content_type='application/pdf'); response['Content-Disposition']=f'attachment; filename="demo-application-{str(app.reference)[:8]}.pdf"'; return response
