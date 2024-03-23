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
        institutions = Institution.objects.all()
        return render(request, 'index.html', {'bags_count': bags_count, 'organizations_count':
            organizations_count, 'categories': categories, 'institutions': institutions})


class AddDonation(View):
    def get(self, request):
        return render(request, 'form.html')
