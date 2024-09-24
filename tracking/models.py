from django.db import models
from django.utils import timezone

class SerialNumber(models.Model):
    serial_number = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.serial_number

class Stage(models.Model):
    STAGE_CHOICES = [
        ('Qr1', 'QR1'),
        ('Qr2', 'QR2'),
        ('Qr3', 'QR3'),
    ]

    serial_number = models.ForeignKey(SerialNumber, on_delete=models.CASCADE)
    stage = models.CharField(max_length=3, choices=STAGE_CHOICES)
    completed = models.BooleanField(default=False)
    time = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return f'{self.serial_number} - {self.stage}'

class StageCompletion(models.Model):
    serial_number = models.ForeignKey(SerialNumber, on_delete=models.CASCADE)
    qr1_completed = models.BooleanField(default=False)
    qr1_completed_time = models.DateTimeField(null=True, blank=True)
    
    qr2_completed = models.BooleanField(default=False)
    qr2_completed_time = models.DateTimeField(null=True, blank=True)
    
    qr3_completed = models.BooleanField(default=False)
    qr3_completed_time = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return (f'{self.serial_number} - QR1: {"Completed" if self.qr1_completed else "Not Completed"}, '
                f'QR2: {"Completed" if self.qr2_completed else "Not Completed"}, '
                f'QR3: {"Completed" if self.qr3_completed else "Not Completed"}')
