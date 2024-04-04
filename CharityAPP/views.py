from django.contrib.auth import update_session_auth_hash
from django.contrib.auth.decorators import login_required
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
            organizations_count, 'categories': categories,
            'fundacje_page_obj': fundacje_page_obj,
            'organizacje_page_obj': organizacje_page_obj,
            'zbiorki_page_obj': zbiorki_page_obj,
            })


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
        category_names = data.get('categories')
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


@login_required
def settings(request):
    if request.method == 'POST':
        # Pobierz dane z formularza
        name = request.POST.get('name')
        surname = request.POST.get('surname')
        email = request.POST.get('email')
        confirm_password = request.POST.get('confirm_password')

        # Sprawdź poprawność hasła
        if not request.user.check_password(confirm_password):
            return render(request, 'user_management/settings.html',
                          {'user_data': request.user, 'error': 'Niepoprawne hasło'})

        # Zaktualizuj dane użytkownika
        request.user.first_name = name
        request.user.last_name = surname
        request.user.email = email
        request.user.save()

        # Przekieruj użytkownika gdziekolwiek po pomyślnym zapisie
        return redirect('settings')

    user_data = {
        'first_name': request.user.first_name,
        'last_name': request.user.last_name,
        'email': request.user.email,
    }
    return render(request, 'user_management/settings.html', {'user_data': user_data, 'error': None})


@login_required
def change_password(request):
    if request.method == 'POST':
        old_password = request.POST.get('old_password')
        new_password1 = request.POST.get('new_password1')
        new_password2 = request.POST.get('new_password2')

        if not request.user.check_password(old_password):
            return render(request, 'user_management/change_password.html',
                          {'error': 'Niepoprawne stare hasło.'})

        if new_password1 != new_password2:
            return render(request, 'user_management/change_password.html',
                          {'error': 'Nowe hasła nie pasują do siebie.'})

        request.user.set_password(new_password1)
        request.user.save()
        update_session_auth_hash(request, request.user)
        return redirect('settings')
    else:
        return render(request, 'user_management/change_password.html')
