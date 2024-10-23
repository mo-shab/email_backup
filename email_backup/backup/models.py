from django.db import models

# Create your models here.

class EmailConfig(models.Model):
    email = models.EmailField()
    server = models.CharField(max_length=100)
    port = models.IntegerField()
    username = models.CharField(max_length=100)
    password = models.CharField(max_length=100)
    protocol = models.CharField(max_length=10, choices=[('IMAP', 'IMAP'), ('POP3', 'POP3')])

    def __str__(self):
        return self.email


class Email(models.Model):
    subject = models.CharField(max_length=255)
    sender = models.CharField(max_length=255)
    body = models.TextField()
    date_received = models.DateTimeField()
    eml_file = models.FileField(upload_to='emails/')

    def __str__(self):
        return self.subject
