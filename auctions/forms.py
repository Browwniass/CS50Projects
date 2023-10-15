from .models import Categories
from django import forms


class NewListingForm(forms.Form):
    title = forms.CharField(max_length=100, label="",
                            widget= forms.TextInput
                            (attrs={'class':'form-control', 
                            'placeholder': 'Title'}))
    bid = forms.IntegerField(min_value=0, label="",
                           widget= forms.NumberInput
                           (attrs={'class':'form-control',
                            'placeholder': 'Bid'}))
    description = forms.CharField(max_length=1000, label="",
                           widget= forms.Textarea
                           (attrs={'class':'form-control',
                            'placeholder': 'Description'}))
    photo = forms.CharField(max_length=150, label="",
                           widget= forms.URLInput
                           (attrs={'class':'form-control',
                            'placeholder': 'Photo URL'}), required=False)
    categories = forms.ChoiceField(choices=[
                            (choice.pk, choice.title) for choice in Categories.objects.all()],
                            required=False , label="",
                           widget= forms.Select
                           (attrs={'class':'form-control',
                            'placeholder': 'Category[Optional]'})) 
    
    """forms.CharField(max_length=60, label="",
                           widget= forms.TextInput
                           (attrs={'class':'form-control',
                            'placeholder': 'Category'}))"""


class NewBidForm(forms.Form):
    bid = forms.IntegerField(min_value=0, label="",
                            required=False, widget= forms.NumberInput
                           (attrs={'class':'form-control',
                            'placeholder': 'Bid'}))