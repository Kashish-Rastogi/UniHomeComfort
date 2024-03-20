from django.shortcuts import render
from django.contrib import messages
from django.core.mail import send_mail
from django.conf import settings
from django.utils.http import urlsafe_base64_encode
from django.utils.encoding import force_bytes

def forgot_password(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        new_password = request.POST.get('newPassword')
        confirm_password = request.POST.get('confirmPassword')
        if new_password != confirm_password:      # Check if passwords match
            messages.error(request, "Passwords do not match.")
            return render(request, 'forgot_password.html')

        token = urlsafe_base64_encode(force_bytes(email))    # For demonstration purposes, we're encoding the email address in base64 
 	# Django's token generator or any other secure method to generate the token
        
        reset_link = request.build_absolute_uri(f'/reset-password/{token}/') # Construct the password reset link

       
        subject = 'Password Reset Request'       # Send the password reset link to the user's email
        message = f'Hello,\n\nPlease click the following link to reset your password:\n{reset_link}'
        from_email = settings.EMAIL_HOST_USER
        to_email = [email]
        send_mail(subject, message, from_email, to_email, fail_silently=False)

        messages.success(request, "Password reset link sent to your email. Check your inbox.")
        return render(request, 'forgot_password.html')

    return render(request, 'forgot_password.html')
