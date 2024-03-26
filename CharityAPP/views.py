from django.contrib.auth.models import User
from django.core.paginator import Paginator
import json
from django.db.models import Sum
from django.http import JsonResponse
from django.shortcuts import render, redirect
from django.views import View

from CharityAPP.forms import DonationForm
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
        institutions = Institution.objects.all()
        institution_categories = {inst.id: [cat.name for cat in inst.categories.all()] for inst in institutions}
        form = DonationForm()
        return render(request, 'form.html', {
            'categories': categories,
            'institution_categories': institution_categories,
            'institutions': institutions,
            'form': form
        })

    def post(self, request):
        data = json.loads(request.body)
        quantity = data.get('quantity')
        category_names = data.get('categories')  # Otrzymujemy listę nazw kategorii
        institution_name = data.get('institution')
        address = data.get('address')
        phone_number = data.get('phone_number')
        city = data.get('city')
        zip_code = data.get('zip_code')
        pick_up_date = data.get('pick_up_date')
        pick_up_time = data.get('pick_up_time')
        pick_up_comment = data.get('pick_up_comment')
        user_id = request.user.id

        valid_categories = []
        for category_name in category_names:
            try:
                category = Category.objects.get(name=category_name)
                valid_categories.append(category)
            except Category.DoesNotExist:
                pass


        institution = Institution.objects.get(name=institution_name)
        donation = Donation.objects.create(
            quantity=quantity,
            institution=institution,
            address=address,
            phone_number=phone_number,
            city=city,
            zip_code=zip_code,
            pick_up_date=pick_up_date,
            pick_up_time=pick_up_time,
            pick_up_comment=pick_up_comment,
            user_id=user_id
        )
        donation.categories.set(valid_categories)

        response_data = {'message': 'Dane zostały pomyślnie zapisane.', 'redirect_url': '/form-confirmation/'}
        return JsonResponse(response_data)


class Confirmation(View):
    def get(self, request):
        return render(request, 'form-confirmation.html')


class UserProfile(View):
    def get(self, request):
        user = request.user
        donations = Donation.objects.filter(user=user)
        return render(request, 'user-profile.html', {'user': user,
                                                     'donations': donations})


class TakeDonation(View):
    def post(self, request, donation_id):
        donation = Donation.objects.get(id=donation_id)
        donation.is_taken = not donation.is_taken
        donation.save()
        return redirect('profile')