from django import forms
from .models import CommunityPost,Category, Property, Bidding



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

class BidForm(forms.ModelForm):
    class Meta:
        model = Bidding
        fields = ['property', 'bidding_amount']