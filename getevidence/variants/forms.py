from .models import VariantReview
from django import forms

class VariantReviewForm(forms.ModelForm):
    class Meta:
        model = VariantReview
