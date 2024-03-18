from django import forms
from .models import Listing, Category

class CommentForm(forms.Form):
    text = forms.CharField(widget=forms.Textarea(attrs={'rows': 4, 'placeholder': 'Write your comment here...'}))

class ListingForm(forms.ModelForm):
    class Meta:
        model = Listing
        fields = ['title', 'category']  # Add 'category' field to the form

    def __init__(self, *args, **kwargs):
        super(ListingForm, self).__init__(*args, **kwargs)
        self.fields['category'].queryset = Category.objects.all()  # 