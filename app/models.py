from django.db import models


class Client(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField()
    phone_number = models.CharField(max_length=20)

    def __str__(self):
        return self.name


class Service(models.Model):
    TIMING_CHOICES = [
        (30, '30 Minutes'),
        (60, '1 Hour'),
        (90, '1 Hour 30 Minutes'),
        (120, '2 Hours'),
        (150, '2 Hours 30 Minutes'),
        (180, '3 Hours'),
    ]

    name = models.CharField(max_length=100)
    timing = models.IntegerField(choices=TIMING_CHOICES)

    def __str__(self):
        return self.name

class Appointment(models.Model):
    client = models.ForeignKey(Client, on_delete=models.CASCADE)
    appointment_date_time = models.DateTimeField()
    service = models.ForeignKey(Service, on_delete=models.CASCADE, default=None)

    def __str__(self):
        return f"{self.appointment_date_time} - {self.client.name}"

