from .models import VariantReview
from django import forms

class VariantReviewForm(forms.ModelForm):
    class Meta:
        model = VariantReview
        fields = ('review_summary',
                  'review_long',
                  'impact',
                  'inheritance',
                  'evidence_computational',
                  'evidence_functional',
                  'evidence_casecontrol',
                  'evidence_familial',
                  'clinical_severity',
                  'clinical_treatability',
                  'clinical_penetrance',
                  )

        widgets = {
            'review_summary': forms.Textarea(attrs={'class': 'span10 lead',
                                                    'rows': 3}),
            'review_long': forms.Textarea(attrs={'class': 'span10',
                                                 'rows': 8})
            }
