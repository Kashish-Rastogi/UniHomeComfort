from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseForbidden
from .forms import CommunityPostForm, ContactForm, PropertyForm, PropertyTypeForm,BidForm, CustomUserCreationForm, LoginForm
from .models import Property, CommunityPost, Category, Bidding, AppUser
from django.core.mail import send_mail
from django.conf import settings
from django.contrib.auth.forms import UserCreationForm
from .forms import PropertyOwnerRegistrationForm
from .models import Property
from django.db.models import Max
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib import messages  # Import Django's messaging framework
from datetime import timezone
from django.shortcuts import render, redirect
from django.contrib.auth import get_user_mode
from .forms import ForgetPasswordForm


def user_login(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('home')  # Redirect to the home page after login
        else:
            # Handle invalid login credentials
            return render(request, 'login.html', {'error_message': 'Invalid username or password'})
    else:
        return render(request, 'login.html')

# def user_register(request):
#     if request.method == 'POST':
#         form = UserCreationForm(request.POST)
#         if form.is_valid():
#             form.save()
#             return redirect('login')  # Redirect to the login page after registration
#     else:
#         form = UserCreationForm()
#     return render(request, 'register.html', {'form': form})

def loginpage(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            print(username, password)
            user = authenticate(request,username=username, password=password)
            if user is not None:
                login(request, user)
                messages.success(request, 'You have been successfully logged in.')
                return redirect('owner-dashboard')
            else:
                messages.error(request, 'Invalid username or password.')
    else:
        form = LoginForm()
    return render(request, 'mainapp/login.html', {'form': form})

def register_student_user(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            # login(request, user)
            messages.success(request, 'Registration successful. You are now logged in.')
            return redirect('login-page')
        else:
            for field, errors in form.errors.items():
                for error in errors:
                    messages.error(request, f"{field}: {error}")
    else:
        form = CustomUserCreationForm()
    return render(request, 'mainapp/register-student-user.html', {'form': form})


def property_owner_register(request):
    if request.method == 'POST':
        form = PropertyOwnerRegistrationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('login')  # Redirect to the login page after registration
    else:
        form = PropertyOwnerRegistrationForm()
    return render(request, 'mainapp/register.html', {'form': form})


def property_listing(request):
    # Retrieve all properties from the database
    properties = Property.objects.all()

    # Pass the properties to the template context
    context = {
        'properties': properties
    }

    # Render the template with the list of properties
def landingpage(request):
    ouser = AppUser.objects.all()
    context = {'ouser': ouser}

    if request.method == 'POST':
        contact_form = ContactForm(request.POST)
        if contact_form.is_valid():
            name = contact_form.cleaned_data['first_name'] + " " + contact_form.cleaned_data['last_name']
            email = contact_form.cleaned_data['email']
            message = contact_form.cleaned_data['message']
            user_type = contact_form.cleaned_data['user_type']

            email_subject = f"New contact form submission from {name}"
            email_message = f"User Type: {user_type}\nEmail: {email}\n\nMessage:\n{message}"

            send_mail(
                subject=email_subject,
                message=email_message,
                from_email=settings.EMAIL_HOST_USER,
                recipient_list=[settings.EMAIL_HOST_USER],
                fail_silently=False,
            )

            context['success_message'] = "Thank you for contacting us! We will get back to you soon."
            return render(request, 'mainapp/landing-page.html', {**context, 'contact_form': ContactForm()})  # Provides a new blank form
    else:
        contact_form = ContactForm()

    context['contact_form'] = contact_form
    return render(request, 'mainapp/landing-page.html', context)





@login_required(login_url='mainapp/login-page')
def ownerdashboard(request):
    print(request.user)
    property_type_form = PropertyTypeForm()
    property = Property.objects.all()
    return render(request, 'mainapp/owner-dashboard.html', {'property_type_form': property_type_form,
                                                            'property': property})

def bidding(request, property_id):
    property_data = get_object_or_404(Property, pk=property_id)
    max_bidding_amount= Bidding.objects.filter(property_id=property_id).aggregate(max_bidding_amount=Max('bidding_amount'))[
        'max_bidding_amount']

    # print(property_data.prop_image1)
    if request.method == "POST":
        form = BidForm(request.POST)
        if form.is_valid():
            form = form.save(commit=False)
            form.bidding_status = 'accepted'
            form.bidding_amount = form.cleaned_data['bidding_amount']
            form.save()
    else:
        form = BidForm(initial={'bidding_amount': max_bidding_amount or 2000})  # Example current bid
    return render(request, 'mainapp/bidding.html',{'form': form, 'property_data': property_data,'max_bidding_amount': max_bidding_amount})



def viewbiddedproperties(request):
    return render (request, 'mainapp/view-bidded-properties.html')

def studentallproperties(request, student_id):
    # student = get_object_or_404(StudentUser, id=student_id)

    return render (request, 'mainapp/student-all-properties.html')


def community_posts_list(request):
    category_id = request.GET.get('category_id', '')
    categories = Category.objects.all()  # Fetch all categories from database
    form = CommunityPostForm()  # Initialize the form

    if category_id and category_id != 'all':
        posts = CommunityPost.objects.filter(category__id=category_id).order_by('-created_at')
    else:
        posts = CommunityPost.objects.all().order_by('-created_at')

    return render(request, 'mainapp/community-post-list.html', {
        'posts': posts,
        'categories': categories,
        'selected_category_id': category_id
    })

# @login_required
def create_community_post(request):
    categories = Category.objects.all()  # Fetch categories once

    if request.method == 'POST':
        form = CommunityPostForm(request.POST)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.category = form.cleaned_data['category']
            post.save()
            return redirect('community_posts_list')
    else:
        form = CommunityPostForm()

    return render(request, 'mainapp/create-community-post.html', {'form': form, 'categories': categories})


# @login_required
def update_community_post(request, pk):
    post = get_object_or_404(CommunityPost, pk=pk)
    if request.user != post.author and not request.user.is_superuser:
        return HttpResponseForbidden()

    if request.method == 'POST':
        form = CommunityPostForm(request.POST, instance=post)
        if form.is_valid():
            updated_post = form.save(commit=False)
            updated_post.category = form.cleaned_data['category']  # Ensure category is correctly assigned
            updated_post.save()
            return redirect('community_posts_list')
    else:
        form = CommunityPostForm(instance=post)

    categories = Category.objects.all()  # Fetch categories for dropdown
    return render(request, 'mainapp/edit-community-post.html', {
        'form': form,
        'post': post,
        'categories': categories  # Pass categories to the template for the dropdown
    })


# @login_required
def delete_community_post(request, pk):
    post = get_object_or_404(CommunityPost, pk=pk)
    if request.user != post.author and not request.user.is_superuser:
        return HttpResponseForbidden()
    post.delete()
    return redirect('community_posts_list')



def property_detail(request, property_id):
    try:
        property = Property.objects.get(pk=property_id)
    except Property.DoesNotExist:
        return render(request, '', status=404)
    context = {
        'property': property,
    }
    return render(request, 'mainapp/property-details.html', context)


def add_property(request):
	property_form = PropertyForm()
	return render(request, 'mainapp/owner-add-property.html', {'property_form':property_form})


@login_required(login_url='mainapp/login-page')  # Ensure that only authenticated users can access this view
def ownerdashboard(request):
    current_time = timezone.now()  # Get the current time
    """
            Get properties where bidding has expired
    """
    expired_properties = Property.objects.filter(
        bidding__time__lt=current_time,  # Filter properties where bidding time is less than the current time
        bidding__bidding_status='pending'  # Filter properties with pending bidding status
    ).distinct()  # Get distinct properties
    """
            # Update bidding status and send payment requests for expired properties
    """
    
    for property in expired_properties:  # Iterate over expired properties
        highest_bid = property.bidding_set.filter(bidding_status='pending').order_by('-bidding_amount').first()  # Get the highest bid for the property
        if highest_bid:  # Check if there is a highest bid
            highest_bid.bidding_status = 'accepted'  # Update bidding status to 'accepted'
            highest_bid.save()  # Save the changes
            
            # Display a notification to the owner on the web interface
            messages.info(request, f"Payment request sent to {highest_bid.student.username} for property '{property.title}'.")
            
    # Retrieve all properties for display
    properties = Property.objects.all()  # Get all properties from the database
    property_type_form = PropertyTypeForm()  # Create an instance of the PropertyTypeForm
    
    # Render the owner dashboard template with properties, property type form, and expired properties
    return render(request, 'mainapp/owner-dashboard.html', {
        'properties': properties,  # Pass properties to the template
        'property_type_form': property_type_form,  # Pass property type form to the template
        'expired_properties': expired_properties  # Pass expired properties to the template
    })


from django.shortcuts import render, redirect
from django.contrib.auth import get_user_model

from .forms import ForgetPasswordForm

User = get_user_model()

def forget_password(request):
    if request.method == 'POST':
        form = ForgetPasswordForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            new_password = form.cleaned_data['new_password']
            user = User.objects.filter(username=username).first()
            if user:
                user.set_password(new_password)
                user.save()
                return redirect('password_reset_done')
    else:
        form = ForgetPasswordForm()
    return render(request, 'webPages/forget.html', {'form': form})
