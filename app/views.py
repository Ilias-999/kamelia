from django.shortcuts import render, redirect
from django.http import JsonResponse, HttpResponse
from .models import Appointment, Client, Service
from django.shortcuts import get_object_or_404
from django.utils import timezone
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login


from django.urls import reverse


def appointments_view(request):
    services = Service.objects.all()
    return render(request, 'appointments.html', {'services': services})


def appointments_form_view(request):
    if request.method == 'POST':
        selected_date = request.POST.get('date')
        selected_service_id = request.POST.get('service_id')
        service = get_object_or_404(Service, pk=selected_service_id)
        appointments = Appointment.objects.filter(appointment_date_time__date=selected_date)
        appointment_times_and_timing = [{'appointment_time': appointment.appointment_date_time.time().strftime('%H:%M'),
                                         'appointment_timing': appointment.service.timing}
                                        for appointment in appointments]

        return JsonResponse({'appointment_times_and_timing': appointment_times_and_timing,
                             'appointment_date': selected_date, 'selected_service_id': selected_service_id,
                             'service_timing': service.timing})
    # If the request method is not POST, render the form template
    return render(request, 'appointments.html')


def create_appointment_client(request):
    if request.method == 'POST':
        client_name = request.POST.get('name')
        client_email = request.POST.get('email')
        client_phone = request.POST.get('telephone')
        clicked_time = request.POST.get('clickedTime')  # Get clickedTime from the request
        chosen_date = request.POST.get('chosenDate')  # Get chosenDate from the request
        service_id = request.POST.get('service_id')
        new_client = Client(name=client_name, email=client_email, phone_number=client_phone)
        new_client.save()
        service = get_object_or_404(Service, pk=service_id)
        appointment_date_time = f"{chosen_date} {clicked_time}"
        new_appointment = Appointment(client=new_client, appointment_date_time=appointment_date_time,
                                      service=service)
        new_appointment.save()

        return redirect('/thank_you_page_view/')
    else:
        return HttpResponse('Invalid data')


def thank_you_page_view(request):
    return render(request, 'tank_you_page.html')


@login_required
def appointment_list_view(request):
    today = timezone.now().date()  # Get today's date
    upcoming_appointments = Appointment.objects.filter(appointment_date_time__date__gte=today).order_by('appointment_date_time')
    return render(request, 'list_appointments.html', {'upcoming_appointments': upcoming_appointments})


@login_required
def delete_appointment(request, appointment_id):
    appointment = get_object_or_404(Appointment, id=appointment_id)
    appointment.delete()
    return redirect('/management/')


def custom_login_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('/management/')  # Redirect to the desired page after successful login
        else:
            # Authentication failed, handle the error
            error_message = "Invalid credentials. Please try again."
    else:
        error_message = None

    return render(request, 'login_form.html', {'error_message': error_message})