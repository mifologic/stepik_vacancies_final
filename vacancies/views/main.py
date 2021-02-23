from django.db.models import Count
from django.http import HttpResponseNotFound, HttpResponseServerError
from django.shortcuts import render, redirect, get_object_or_404
from django.views import View

from vacancies.check_user_status import get_current_user
from vacancies.forms import ApplicationForm
from vacancies.models import Specialty, Vacancy, Company


class MainView(View):

    def get(self, request):
        specialties = Specialty.objects.all().annotate(count=Count('vacancies'))
        company_vacancies = Company.objects.all().annotate(count=Count('vacancies'))
        context = {
            'specialties': specialties,
            'company_vacancies': company_vacancies,
        }
        return render(request, 'vacancies/index.html', context=context)


class VacanciesByCategory(View):

    def get(self, request, category):
        specialty = get_object_or_404(Specialty, code=category)
        vacancies = Vacancy.objects.prefetch_related('specialty')
        context = {
            'vacancies': vacancies,
            'specialty': specialty,
        }
        return render(request, 'vacancies/vacancies.html', context=context)


class VacanciesView(View):

    def get(self, request):
        vacancies = Vacancy.objects.prefetch_related('specialty')
        context = {
            'vacancies': vacancies,
        }
        return render(request, 'vacancies/vacancies.html', context=context)


class SendView(View):
    template_name = 'vacancies/send.html'

    def get(self, request, vacancy_id):
        vacancy = get_object_or_404(Vacancy, id=vacancy_id)
        return render(
            request, self.template_name,
            context={
                'vacancy': vacancy,
            },
        )


class VacancyView(View):

    def get(self, request, vacancy_id):
        vacancy = get_object_or_404(Vacancy, pk=vacancy_id)
        form = ApplicationForm
        context = {
            'vacancy': vacancy,
            'form': form,
        }
        return render(request, 'vacancies/vacancy.html', context=context)

    def post(self, request, vacancy_id):
        form = ApplicationForm(request.POST)
        user = get_current_user(request)
        if user is None:
            return redirect('login')
        vacancy = Vacancy.objects.filter(pk=vacancy_id).select_related('specialty')
        if form.is_valid():
            application = form.save(commit=False)
            application.user = user
            application.vacancy = vacancy
            application.save()
            return redirect('send', vacancy_id)
        return render(request, 'vacancies/vacancy.html', {'form': form})


class CompanyView(View):

    def get(self, request, company_id):
        company = get_object_or_404(Company, pk=company_id)
        vacancies = Vacancy.objects.filter(company=company.id).select_related('specialty')
        context = {
            'company': company,
            'vacancies': vacancies,
        }
        return render(request, 'vacancies/company.html', context=context)


def custom_handler404(request, exception):
    """
    :return: Возвращает сообщение, если запрашиваемая страница не найдена.
    """
    return HttpResponseNotFound('Страница не найдена. Зайдите попозже.')


def custom_handler500(request):
    """
    :return: Возвращает сообщение, если сервер недоступен.
    """
    return HttpResponseServerError('Сервер недоступен. Зайдите попозже.')
