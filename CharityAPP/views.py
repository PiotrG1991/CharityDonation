from django.db.models import Sum
from django.shortcuts import render
from django.views import View

from CharityAPP.models import Institution, Donation


# Create your views here.
class LandingPage(View):
    bags_count =  Donation.objects.aggregate(total_quantity=Sum('quantity'))['total_quantity'] or 0
    organizations_count = Donation.objects.count()
    def get(self, request):
        return render(request, 'index.html', {'bags_count': self.bags_count, 'organizations_count': self.organizations_count})


class AddDonation(View):
    def get(self, request):
        return render(request, 'form.html')
