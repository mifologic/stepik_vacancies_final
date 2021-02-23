import os
import django

os.environ["DJANGO_SETTINGS_MODULE"] = 'stepik_vacancies.settings'
django.setup()


if __name__ == '__main__':

    from vacancies.data import jobs, companies, specialties
    from vacancies.models import Company, Specialty, Vacancy

    Specialty.objects.all().delete()
    Vacancy.objects.all().delete()
    Company.objects.all().delete()

    for special in specialties:
        Specialty.objects.create(
            code=special['code'],
            title=special['title'],
        )

    for company in companies:
        Company.objects.create(
            name=company['title'],
            location=company['location'],
            description=company['description'],
            employee_count=company['employee_count'],
                               )

    for job in jobs:
        company = Company.objects.get(pk=job['company'])
        specialty = Specialty.objects.get(code=job['specialty'])
        Vacancy.objects.create(
            title=job['title'],
            specialty=specialty,
            company=company,
            skills=job['skills'],
            description=job['description'],
            salary_min=job['salary_from'],
            salary_max=job['salary_to'],
            published_at=job['posted'],
        )

Company.objects.filter(pk=8).update(owner=8)
