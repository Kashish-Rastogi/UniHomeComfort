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
from django.db.models import Max, Count
from datetime import timezone



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


@login_required(login_url='/login/')
def viewbiddedproperties(request):
    property_type = request.GET.get('property_type', '')
    bidding_status = request.GET.get('bidding_status', '')
    types = PropertyType.objects.all()  # Fetch all categories from database
    bidding_grouped_by_property = Bidding.objects.filter(student=request.user) \
        .values('property_id') \
        .annotate(max_bid_amount=Max('bidding_amount'))

    # Extract the IDs of the highest bid for each property
    highest_bid_ids = []
    for entry in bidding_grouped_by_property:
        property_id = entry['property_id']
        max_bid_amount = entry['max_bid_amount']
        highest_bid = Bidding.objects.filter(property_id=property_id, bidding_amount=max_bid_amount).first()
        if highest_bid:
            highest_bid_ids.append(highest_bid.id)

    highest_bid_from_all_users = Bidding.objects.values('property_id') \
        .annotate(max_bid_amount=Max('bidding_amount'))

    # Extract the IDs of the highest bid for each property
    highest_bid_from_all_users_ids = []
    for entry in highest_bid_from_all_users:
        property_id = entry['property_id']
        max_bid_amount = entry['max_bid_amount']
        highest_bid = Bidding.objects.filter(property_id=property_id, bidding_amount=max_bid_amount).first()
        if highest_bid:
            highest_bid_from_all_users_ids.append(highest_bid.id)

    # Print the IDs of the highest bid for each property
    print("IDs of the highest bid for each property:")
    print(highest_bid_ids,highest_bid_from_all_users_ids)

    bidded_properties_ids = Bidding.objects.filter(student=request.user) \
        .values('student_id') \
        .annotate(max_bid_amount=Max('bidding_amount')) \
        .values_list('property_id', flat=True)
    # print(highest_biddin_ids)
    if property_type and property_type != 'all':
        properties = (Property.objects.filter(id__in=bidded_properties_ids).filter(property_type=property_type.lower()))
        print(Property.objects.filter(id__in=bidded_properties_ids).values_list('property_type',flat=True))
    else:
        properties = Property.objects.filter(id__in=bidded_properties_ids)

    property_bidding_statuses = {}
    property_bidding_highest_price = {}
    property_highest_bidding = {}
    for property_id in bidded_properties_ids:
        try:
            bidding = Bidding.objects.get(property_id=property_id, student=request.user, id__in=highest_bid_ids)
            highest_bidding = Bidding.objects.get(property_id=property_id, id__in=highest_bid_from_all_users_ids)
            property_bidding_statuses[property_id] = bidding.bidding_status
            property_bidding_highest_price[property_id] = bidding.bidding_amount
            property_highest_bidding[property_id] = highest_bidding.bidding_amount
        except Bidding.DoesNotExist:
            property_bidding_statuses[property_id] = None


    for prop in properties:
        prop.bidding_status = property_bidding_statuses.get(prop.id)
        prop.user_bid = property_bidding_highest_price.get(prop.id)
        prop.bidding_highest_price = property_highest_bidding.get(prop.id)

    if bidding_status and bidding_status != 'all':
        properties = [prop for prop in properties if prop.bidding_status == bidding_status]

    return render(request, 'mainapp/view-bidded-properties.html', {
        'properties': properties,
        'types': types,
        'bidding_statuses':['pending','accepted', 'rejected'],
        'bidding_status':bidding_status,
        'selected_property_type': property_type
    })



def studentallproperties(request):
    # student = get_object_or_404(StudentUser, id=student_id)

    return render(request, 'mainapp/student-all-properties.html')


# ################# Jainam #################

from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseForbidden
from .forms import CommunityPostForm, ContactForm, PropertyForm, PropertyTypeForm, BidForm, CustomUserCreationForm, LoginForm, StudentSettingsForm
from .models import Property, CommunityPost, Category, Bidding, AppUser, PropertyType
from django.core.mail import send_mail
from django.conf import settings
from django.contrib.auth.forms import UserCreationForm, PasswordChangeForm
from .forms import PropertyOwnerRegistrationForm
from .models import Property
from django.db.models import Max
from django.contrib.auth import authenticate, login, logout, update_session_auth_hash
from django.contrib import messages
from django.db.models import Max, Count

# ################# Tanvi #################
def property_owner_register(request):
    if request.method == 'POST':
        form = PropertyOwnerRegistrationForm(request.POST, request.FILES)  # Ensure to handle FILES if your form includes file uploads
        if form.is_valid():
            owner_form = form.save(commit=False)
            owner_form.is_owner = True
            owner_form.is_student = False
            owner_form.save()
            return redirect('login-page')  # Redirect to the login page after registration
        else:
            for field, errors in form.errors.items():
                for error in errors:
                    messages.error(request, f"{field}: {error}")
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
    return render(request, 'mainapp/property_listing.html', context)

@login_required
def student_settings(request):
    user = AppUser.objects.get(username=request.user.username)
    if request.method == 'POST':
        user_form = StudentSettingsForm(request.POST, instance=user)
        password_form = PasswordChangeForm(request.user, request.POST)
        if user_form.is_valid() and (not password_form.is_bound or password_form.is_valid()):
            user_form.save()
            if password_form.is_valid():
                password_form.save()
                update_session_auth_hash(request, password_form.user)  # Important for keeping the user logged in
                messages.success(request, 'Password has been updated.')
            messages.success(request, 'Your settings have been updated.')
            return redirect('student_settings')
    else:
        user_form = StudentSettingsForm(instance=user)
        password_form = PasswordChangeForm(request.user)
    return render(request, 'mainapp/student_settings.html', {
        'form': user_form,
        'password_form': password_form
    })
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
def owner_view_all_properties(request):
    property_type = request.GET.get('property_type', '')
    types = PropertyType.objects.all()  # Fetch all categories from database
    print(types)
    if property_type and property_type != 'all':
        properties = (Property.objects.filter(owner=request.user).filter(property_type=property_type.lower()))
    else:
        properties = Property.objects.filter(owner=request.user)

    return render(request, 'mainapp/owner-view-all-properties.html', {
        'properties': properties,
        'types': types,
        'selected_property_type': property_type
    })

@login_required(login_url='/login/')
def owner_add_property(request):
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

@login_required(login_url='/login/')
def owner_edit_property(request, property_id):
    property = get_object_or_404(Property, id=property_id, owner=request.user)
    if request.method == 'POST':
        form = PropertyForm(request.POST, request.FILES, instance=property)
        if form.is_valid():
            form.save()
            messages.success(request, "Property updated successfully.")
            return redirect('owner-view-all-properties')  # Redirect to the property listing
        else:
            for field, errors in form.errors.items():
                for error in errors:
                    messages.error(request, f"{field}: {error}")
    else:
        form = PropertyForm(instance=property)

    return render(request, 'mainapp/owner-edit-property.html', {
        'property_form': form,
        'property': property
    })

def owner_delete_property(request, property_id):
    property_instance = get_object_or_404(Property, id=property_id)
    property_instance.delete()
    return redirect('owner-view-all-properties')

def property_detail(request, property_id):
    property = get_object_or_404(Property,id=property_id)
    if request.user.is_authenticated:
        if 'visited_properties' not in request.session:
            request.session['visited_properties'] = []
        visited_properties = request.session['visited_properties']

        if property_id not in visited_properties:
            visited_properties.append(property_id)
            request.session['visited_properties'] = visited_properties
    return render(request, 'mainapp/property-details.html', {'property': property})

def owner_property_bids(request):
    property_type = request.GET.get('property_type', '')
    selected_property = request.GET.get('selected_property', '')
    types = PropertyType.objects.all()  # Assuming this is for display purposes in the template
    owner_properties = Property.objects.filter(owner=request.user)  # Assuming this is for display purposes in the template

    if property_type and property_type != 'all':
        # Filter properties directly by property_type value, not by property_type__id
        properties = Property.objects.filter(owner=request.user, property_type=property_type.lower())
    else:
        # Fetch all properties for this owner if no specific type is requested or 'all' is specified
        properties = Property.objects.filter(owner=request.user)

    if selected_property and selected_property != 'all':
        properties = properties.filter(id=selected_property)

    properties = properties.values_list('id',flat=True)
    # Filter bids where property_id is in the list of properties' ids
    bids = Bidding.objects.filter(property__id__in=list(properties)).order_by('-time')

    return render(request, 'mainapp/owner-property-bids.html', {
        'bids': bids,
        'types': types,
        'selected_property_type': property_type,
        'owner_properties':owner_properties,
        'selected_property':selected_property
    })

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



###################  Haseeb #################


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

    return render(request, 'mainapp/forgot_password.html')




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



