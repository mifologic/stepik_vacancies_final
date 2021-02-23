"""stepik_vacancies URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
import debug_toolbar

from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

from vacancies.views import main, mycompany

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', main.MainView.as_view(), name='main'),
    path('vacancies/', main.VacanciesView.as_view(), name='vacancies'),
    path('vacancies/cat/<str:category>/', main.VacanciesByCategory.as_view(), name='vacancies_by_category'),
    path('companies/<int:company_id>/', main.CompanyView.as_view(), name='company'),
    path('vacancies/<int:vacancy_id>/', main.VacancyView.as_view(), name='vacancy'),
    path('vacancies/<int:vacancy_id>/send/', main.SendView.as_view(), name='send'),
    path('mycompany/start/', mycompany.UserCompanyStart.as_view(), name='my_company_start'),
    path('mycompany/create/', mycompany.UserCompanyCreate.as_view(), name='my_company_create'),
    path('mycompany/', mycompany.UserCompany.as_view(), name='my_company'),
    path('mycompany/vacancies/create/', mycompany.UserVacancyCreate.as_view(), name='my_company_vacancy_create'),
    path('mycompany/vacancies/<int:vacancy_id>/', mycompany.UserCompanyVacancy.as_view(), name='my_company_vacancy'),
    path('mycompany/vacancies/', mycompany.UserCompanyVacancies.as_view(), name='my_company_vacancies'),
    path('registration/', include('registration.urls')),
    path('__debug__/', include(debug_toolbar.urls)),
]

handler404 = main.custom_handler404
handler500 = main.custom_handler500

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL,
                          document_root=settings.MEDIA_ROOT)
