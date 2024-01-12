from django.shortcuts import render
from django.shortcuts import render, redirect
from .forms import ContactForm
from django.contrib import messages
from users.views import get_ip
from users.models import GuestIP, get_total

from django.utils import timezone
from django.core.mail import send_mail
from django.conf import settings

def index(request):
    ip_address = get_ip(request)
    ip_user = request.user
    time = timezone.localtime(timezone.now())
     
    ### total unique test ###
    # total_unique = get_total(GuestIP)    
    # print(total_unique)
    GuestIP(user_id=ip_user, user_ip_address=ip_address, time=time).save()
    
    context = {
        'user': request.user,
    }
    return render(request, 'main/index.html', context)


def contact(request):
    user = request.user
    if request.method == 'POST':
        form = ContactForm(request.POST)
        if form.is_valid():
            # title = form.cleaned_data.get('title')
            # message = form.cleaned_data.get('message')
            # email = form.cleaned_data.get('email')
            form.save()
            messages.success(request, f'Your ticket has been created! we will contact you ASAP')
            name = form.cleaned_data.get('name')
            send_mail(
            subject='הפניה שלך לwebmarket.co.il התקלה',
            message=f'שלום {name}, קיבלנו את הפניה שלך, אנו נחזור אליך בהקדם האפשרי, תודה על הסבלנות.',
            from_email=settings.EMAIL_HOST_USER,
            recipient_list=[form.cleaned_data.get('email')])
            return redirect('ticket-created/')
    else:
        form = ContactForm()
    return render(request, 'main/contact.html', {'form': form})


def ticket_created(request):
    return render(request, 'main/ticket-created.html')

def support_price(request):
    return render(request, 'main/support_price.html')

def aboutus(request):
    return render(request, 'main/aboutus.html')

def faq(request):
    return render(request, 'main/faq.html')

def services(request):
    return render(request, 'main/services.html')
