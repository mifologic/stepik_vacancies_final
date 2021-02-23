from django.db.models import Count
from django.shortcuts import render, redirect, get_object_or_404
from django.views import View

from vacancies.check_user_status import get_current_user
from vacancies.forms import EditMyCompanyForm, EditMyVacancyForm
from vacancies.models import Company, Vacancy, Application


class UserCompanyStart(View):

    def get(self, request):
        return render(request, 'vacancies/company-create.html')


class UserCompanyCreate(View):

    def get(self, request):
        form = EditMyCompanyForm
        user = get_current_user(request)
        context = {'user': user, 'form': form}
        return render(request, 'vacancies/company-edit.html', context=context)

    def post(self, request):
        user = get_current_user(request)
        form = EditMyCompanyForm(request.POST, request.FILES)
        if form.is_valid():
            post_form = form.save(commit=False)
            post_form.owner = user
            post_form.save()
            return redirect('my_company')
        else:
            form = EditMyCompanyForm()
        context = {'form': form}
        return render(request, 'vacancies/company-edit.html', context=context)


class UserCompany(View):
    company_modify = False

    def get(self, request):
        user = get_current_user(request)
        if user is None:
            return redirect('login')
        user_company = Company.objects.filter(owner=user.id).first()
        if user_company is None:
            return redirect('my_company_start')
        else:
            form = EditMyCompanyForm(instance=user_company)
            context = {'user': user, 'form': form}
            return render(request, 'vacancies/company-edit.html', context=context)

    def post(self, request):
        user = get_current_user(request)
        instance = Company.objects.filter(owner=user.id).first()
        form = EditMyCompanyForm(request.POST, request.FILES, instance=instance)
        if form.is_valid():
            post_form = form.save(commit=False)
            post_form.owner = user
            post_form.save()
            self.company_modify = True
        context = {
            'form': form,
            'company_modify': self.company_modify}
        return render(request, 'vacancies/company-edit.html', context=context)


class UserVacancyCreate(View):

    def get(self, request):
        form = EditMyVacancyForm
        context = {'form': form}
        return render(request, 'vacancies/vacancy-edit.html', context=context)

    def post(self, request):
        form = EditMyVacancyForm(request.POST)
        user = get_current_user(request)
        company = get_object_or_404(Company, owner=user)
        if form.is_valid():
            vacancy_form = form.save(commit=False)
            vacancy_form.company = company
            vacancy = form.save()
            return redirect('my_company_vacancy', vacancy_id=vacancy.pk)
        else:
            form = EditMyCompanyForm()
        context = {'form': form}
        return render(request, 'vacancies/vacancy-edit.html', context=context)


class UserCompanyVacancy(View):
    vacancy_modify = False

    def get(self, request, vacancy_id):
        user = get_current_user(request)
        vacancy = Vacancy.objects.annotate(applications_count=Count('applications__vacancy'))\
            .filter(id=vacancy_id).first()
        applications = Application.objects.filter(vacancy=vacancy_id)
        if user is None:
            return redirect('login')
        form = EditMyVacancyForm(instance=vacancy)
        context = {
            'form': form,
            'vacancy': vacancy,
            'applications': applications,
        }
        return render(request, 'vacancies/vacancy-edit.html', context=context)

    def post(self, request, vacancy_id):
        vacancy = Vacancy.objects.annotate(applications_count=Count('applications__vacancy'))\
            .filter(id=vacancy_id).first()
        applications = Application.objects.filter(vacancy=vacancy_id)
        form = EditMyVacancyForm(request.POST, instance=vacancy)
        if form.is_valid():
            post_form = form.save(commit=False)
            post_form.company = vacancy.company
            post_form.save()
            self.vacancy_modify = True
        context = {
            'form': form,
            'vacancy': vacancy,
            'applications': applications,
            'vacancy_modify': self.vacancy_modify,
        }
        return render(request, 'vacancies/vacancy-edit.html', context=context)


class UserCompanyVacancies(View):

    def get(self, request):
        user = get_current_user(request)
        if user is None:
            return redirect('login')
        company = Company.objects.filter(owner=user.id).first()
        vacancies = Vacancy.objects.filter(company=company.id).annotate(
            applications_count=Count('applications__vacancy'))
        if company is None:
            return redirect('my_company_start')
        if len(vacancies) == 0:
            return redirect('my_company_vacancy_create')
        context = {
            'vacancies': vacancies,
            'user': user,
        }
        return render(request, 'vacancies/vacancy-list.html', context=context)
