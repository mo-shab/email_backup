# Create your views here.
from django.shortcuts import render, redirect
from .forms import EmailConfigForm, EmailConfig
from .email_utils import fetch_emails
from .models import Email

def configure_email(request):
    if request.method == 'POST':
        form = EmailConfigForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('success')
    else:
        form = EmailConfigForm()

    return render(request, 'configure_email.html', {'form': form})

def success(request):
    return render(request, 'success.html')


def fetch_emails_view(request):
    email_configs = EmailConfig.objects.all()
    if email_configs.exists():
        email_config = email_configs.first()
        fetch_emails(email_config)
        return render(request, 'fetch_emails.html', {'message': 'Emails fetched successfully.'})
    else:
        return render(request, 'fetch_emails.html', {'message': 'No email configuration found.'})

def email_list(request):
    emails = Email.objects.all().order_by('-date_received')
    return render(request, 'email_list.html', {'emails': emails})

def email_detail(request, email_id):
    email_obj = Email.objects.get(id=email_id)
    # Parse the .eml file to get the content
    import email as email_module
    with email_obj.eml_file.open('rb') as f:
        msg = email_module.message_from_binary_file(f)
    # Get the email body
    body = ""
    if msg.is_multipart():
        for part in msg.walk():
            ctype = part.get_content_type()
            cdispo = str(part.get('Content-Disposition'))
            # Skip attachments
            if ctype == 'text/plain' and 'attachment' not in cdispo:
                body = part.get_payload(decode=True).decode()
                break
    else:
        body = msg.get_payload(decode=True).decode()

    return render(request, 'email_detail.html', {'email': email_obj, 'body': body})
