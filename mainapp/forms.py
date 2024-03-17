from django import forms
from .models import CommunityPost,Category, Property



class CommunityPostForm(forms.ModelForm):
    class Meta:
        model = CommunityPost
        fields = ['title', 'content', 'category']
        widgets = {
            'title': forms.TextInput(attrs={'class': 'w-full px-4 py-2 mt-2 border rounded-md focus:outline-none focus:ring-1 focus:ring-blue-600', 'placeholder': 'Title'}),
            'content': forms.Textarea(attrs={'class': 'w-full px-4 py-2 mt-2 border rounded-md focus:outline-none focus:ring-1 focus:ring-blue-600', 'placeholder': 'Content', 'rows': '4'}),
            'category': forms.Select(  # Change TextInput to Select
                choices=(),  # Initialize with empty choices
            )
        }

    def __init__(self, *args, **kwargs):
        super(CommunityPostForm, self).__init__(*args, **kwargs)
        # Dynamically populate category choices
        self.fields['category'].choices = [(category.id, category.name) for category in Category.objects.all()]



class ContactForm(forms.Form):
    first_name = forms.CharField(max_length=100, widget=forms.TextInput(attrs={'class': 'w-full rounded-md py-3 px-4 bg-gray-100 text-sm outline-[#007bff]', 'placeholder': 'First Name'}))
    last_name = forms.CharField(max_length=100, widget=forms.TextInput(attrs={'class': 'w-full rounded-md py-3 px-4 bg-gray-100 text-sm outline-[#007bff]', 'placeholder': 'Last Name'}))
    email = forms.EmailField(widget=forms.EmailInput(attrs={'class': 'w-full rounded-md py-3 px-4 bg-gray-100 text-sm outline-[#007bff]', 'placeholder': 'Email'}))
    user_type = forms.ChoiceField(choices=[('owner', 'Owner'), ('student', 'Student')], widget=forms.Select(attrs={'class': 'inline-flex w-full justify-center gap-x-1.5 rounded-md bg-white px-3 py-2 text-sm font-semibold text-gray-900 shadow-sm ring-1 ring-inset ring-gray-300 hover:bg-gray-50'}))
    message = forms.CharField(widget=forms.Textarea(attrs={'class': 'w-full rounded-md px-4 bg-gray-100 text-sm py-3 mt-4 outline-[#007bff]', 'placeholder': 'Message', 'rows': '6'}))


class PropertyForm(forms.ModelForm):
    class Meta:
        model = Property
        fields = ['title', 'address']


class PropertyTypeForm(forms.ModelForm):
    class Meta:
        model = Property
        fields = ['property_type']
        widgets = {
            'property_type': forms.Select(attrs={'class': 'flex-1 border border-gray-300 rounded-lg py-2 px-4'},
                                          choices=Property.property_type)
        }
        labels = {
            'property_type': ''
        }

class PropertyForm(forms.ModelForm):
    class Meta:
        model = Property
        exclude = ['owner','created_at', 'expire', 'lease_required']
        labels = {
            'number_of_bedrooms': 'No. Bedrooms:',
            'number_of_bathrooms': 'No. Bathrooms:'
        }
        widgets = {
            'title': forms.TextInput(attrs={'class': 'common-input w-full'}),
            'address': forms.TextInput(attrs={'class': 'common-input w-full'}),
            'city': forms.TextInput(attrs={'class': 'common-input w-full'}),
            'zipcode': forms.TextInput(attrs={'class': 'common-input w-full'}),
            'property_type': forms.Select(attrs={'class': 'common-input w-full'}),
            'number_of_bedrooms': forms.NumberInput(attrs={'class': 'common-input w-full'}),
            'number_of_bathrooms': forms.NumberInput(attrs={'class': 'common-input w-full'}),
            'amenities': forms.Textarea(attrs={'class': 'common-input w-full h-20'}),
            'price': forms.NumberInput(attrs={'class': 'common-input w-full'}),
            'availability_status': forms.Select(attrs={'class': 'common-input w-full'}),
            'available_from': forms.DateTimeInput(attrs={'class': 'common-input w-full'}),
            'available_to': forms.DateTimeInput(attrs={'class': 'common-input w-full'}),
            'is_biddable': forms.CheckboxInput(attrs={'class': 'common-checkbox w-full'}),
            'bidding_min_limit': forms.NumberInput(attrs={'class': 'common-input w-full'}),
            'lease_duration': forms.NumberInput(attrs={'class': 'common-input'}),
            'allowed_lease_people': forms.NumberInput(attrs={'class': 'common-input'}),
            'rules': forms.Textarea(attrs={'class': 'common-input w-full h-20'}),
            'prop_image1': forms.FileInput(attrs={'class': 'common-input w-full '}),
            'prop_image2': forms.FileInput(attrs={'class': 'common-input w-full '}),
            'prop_image3': forms.FileInput(attrs={'class': 'common-input w-full '}),
            'prop_image4': forms.FileInput(attrs={'class': 'common-input'}),
            'prop_image5': forms.FileInput(attrs={'class': 'common-input'}),
            'house_build_date': forms.DateInput(attrs={'class': 'common-input'}),
        }
