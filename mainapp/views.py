from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseForbidden
from .forms import CommunityPostForm, ContactForm, PropertyForm, PropertyTypeForm, BidForm, CustomUserCreationForm, LoginForm
from .models import Property, CommunityPost, Category, Bidding, AppUser, PropertyType
from django.core.mail import send_mail
from django.conf import settings
from django.contrib.auth.forms import UserCreationForm
from .forms import PropertyOwnerRegistrationForm
from .models import Property
from django.db.models import Max
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages


# ################# Jainam #################
def loginpage(request):
    if request.user:
        logout(request)
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            userExists = AppUser.objects.filter(username=username)
            if userExists.count() == 0:
                messages.error(request, 'You are not registered, please sign up!')
            else:
                user = authenticate(request, username=username, password=password)
                if user is not None:
                    login(request, user)
                    messages.success(request, 'You have been successfully logged in.')
                    return redirect('owner-view-all-properties')
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


def viewbiddedproperties(request):
    return render(request, 'mainapp/view-bidded-properties.html')


def studentallproperties(request):
    # student = get_object_or_404(StudentUser, id=student_id)

    return render(request, 'mainapp/student-all-properties.html')


# ################# Jainam #################

# ################# Tanvi #################
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


# ################# Tanvi #################

# ################# Kashish + Hetansh #################
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
            user_email_subject = "Thank you for reaching out to us!"
            user_email_message = "Thank you for reaching out to us. We will contact you very soon via email."

            send_mail(
                subject=user_email_subject,
                message=user_email_message,
                from_email=settings.EMAIL_HOST_USER,
                recipient_list=[email],
                fail_silently=False,
            )
            context['success_message'] = "Thank you for contacting us! We will get back to you soon."
            return render(request, 'mainapp/landing-page.html',
                          {**context, 'contact_form': ContactForm()})
    else:
        contact_form = ContactForm()

    context['contact_form'] = contact_form
    return render(request, 'mainapp/landing-page.html', context)


# ################# Kashish + Hetansh #################


# ################# Kashish #################
@login_required(login_url='/login/')
def ownerviewallproperties(request):
    property_type = request.GET.get('property_type', '')
    types = PropertyType.objects.all()  # Fetch all categories from database
    print(types)
    if property_type and property_type != 'all':
        properties = (Property.objects.filter(owner=request.user).filter(property_type__id=property_type))
    else:
        properties = Property.objects.filter(owner=request.user)

    return render(request, 'mainapp/owner-view-all-properties.html', {
        'properties': properties,
        'types': types,
        'selected_property_type': property_type
    })

@login_required(login_url='/login/')
def owneraddproperty(request):
    if request.method == 'POST':
        form = PropertyForm(request.POST, request.FILES)
        if form.is_valid():
            # Associate current user as the owner of the property
            property = form.save(commit=False)
            owner = AppUser.objects.get(username=request.user.username)
            property.owner = owner  # Assuming user is logged in
            property.save()

            return redirect('owner-view-all-properties')
        else:
            for field, errors in form.errors.items():
                for error in errors:
                    messages.error(request, f"{field}: {error}")
    else:
        form = PropertyForm()
    return render(request, 'mainapp/owner-add-property.html', {'property_form': form})



def delete_property(request, property_id):
    property_instance = get_object_or_404(Property, id=property_id)
    property_instance.delete()
    return redirect('owner-view-all-properties')


def property_detail(request):
    # try:
    #     property = Property.objects.get(pk=property_id)
    # except Property.DoesNotExist:
    #     return render(request, '', status=404)
    # context = {
    #     'property': property,
    # }
     return render(request, 'mainapp/property-details.html')
    # , context)


# ################# Kashsih #################

# ################# Parth #################
def bidding(request, property_id):
    property_data = get_object_or_404(Property, pk=property_id)
    max_bidding_amount= Bidding.objects.filter(property_id=property_id).aggregate(max_bidding_amount=Max('bidding_amount'))[
        'max_bidding_amount']
    if max_bidding_amount is None:
        max_bidding_amount = property_data.bidding_min_limit

    # print(property_data.prop_image1)
    if request.method == "POST":
        form = BidForm(request.POST)
        if form.is_valid():
            form = form.save(commit=False)
            form.bidding_status = 'pending'
            form.property_id = property_id
            form.payment_status = 'pending'
            student = AppUser.objects.get(username=request.user.username)
            form.student = student
            # form.bidding_amount = form.cleaned_data['bidding_amount']
            form.save()
        else:
            for field, errors in form.errors.items():
                for error in errors:
                    messages.error(request, f"{field}: {error}")
    else:
        form = BidForm(initial={'bidding_amount': max_bidding_amount or 2000})  # Example current bid
    return render(request, 'mainapp/bidding.html',{'form': form, 'property_data': property_data,'max_bidding_amount': max_bidding_amount})

def aboutus(request):
    return render(request, 'mainapp/aboutus.html')

def settings_user(request):
    return render(request, 'mainapp/settings_user.html')

# ################# Parth #################

# ################# Hetansh #################
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
# ################# Hetansh #################
