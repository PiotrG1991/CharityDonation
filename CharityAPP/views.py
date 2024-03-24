from django.core.paginator import Paginator
from django.db.models import Sum
from django.shortcuts import render
from django.views import View

from CharityAPP.models import Institution, Donation, Category


# Create your views here.
class LandingPage(View):
    def get(self, request):
        bags_count = Donation.objects.aggregate(total_quantity=Sum('quantity'))['total_quantity'] or 0
        organizations_count = Institution.objects.count()
        categories = Category.objects.all()

        fundacje_page_number = request.GET.get('fundacje_page', 1)
        institutions_fundacje = Institution.objects.filter(type='fundacja').order_by('name')
        paginator_fundacje = Paginator(institutions_fundacje, 5)
        fundacje_page_obj = paginator_fundacje.get_page(fundacje_page_number)

        organizacje_page_number = request.GET.get('organizacje_page', 1)
        institutions_organizacje = Institution.objects.filter(type='organizacja').order_by('name')
        paginator_organizacje = Paginator(institutions_organizacje, 5)
        organizacje_page_obj = paginator_organizacje.get_page(organizacje_page_number)

        zbiorki_page_number = request.GET.get('zbiorki_page', 1)
        institutions_zbiorki = Institution.objects.filter(type='zbiórka_lokalna').order_by('name')
        paginator_zbiorki = Paginator(institutions_zbiorki, 5)
        zbiorki_page_obj = paginator_zbiorki.get_page(zbiorki_page_number)

        return render(request, 'index.html', {'bags_count': bags_count, 'organizations_count':
            organizations_count, 'categories': categories, 'fundacje_page_obj': fundacje_page_obj,
                                              'organizacje_page_obj': organizacje_page_obj,
                                              'zbiorki_page_obj': zbiorki_page_obj})


class AddDonation(View):
    def get(self, request):
        categories = Category.objects.all()
        return render(request, 'form.html', {'categories': categories})
