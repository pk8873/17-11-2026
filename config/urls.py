from django.contrib import admin
from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from portal import views
urlpatterns=[path('admin/',admin.site.urls),path('',views.home,name='home'),path('vacancies/',views.vacancies,name='vacancies'),path('apply/<int:vacancy_id>/',views.apply,name='apply'),path('application/<str:reference>/',views.confirmation,name='confirmation'),path('application/<str:reference>/receipt.pdf',views.receipt_pdf,name='receipt_pdf')]
if settings.DEBUG: urlpatterns += static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT)
