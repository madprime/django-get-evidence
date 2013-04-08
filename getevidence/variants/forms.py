from .models import VariantReview
from django import forms
from bootstrap_toolkit.widgets import BootstrapDateInput, BootstrapTextInput, BootstrapUneditableInput

class VariantReviewForm(forms.ModelForm):
    class Meta:
        model = VariantReview
