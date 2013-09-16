import re
from django import forms
from .models import Gene, Variant, VariantReview, VariantPublicationReview

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


class AddVarPubReviewForm(forms.Form):
    pmid = forms.IntegerField(min_value=1)


class NewVariantForm(forms.Form):
    gene = forms.CharField()
    aa_reference = forms.CharField()
    aa_position = forms.IntegerField(min_value=1)
    aa_variant = forms.CharField()

    def clean_gene(self):
        try:
            gene = Gene.objects.get(hgnc_symbol=self.cleaned_data['gene'])
            return self.cleaned_data['gene']
        except Gene.DoesNotExist:
            raise forms.ValidationError('No gene in database with gene symbol "' +
                                        self.cleaned_data['gene'] + '".')

    def clean_aa_reference(self):
        single_letter = '[ACDEFGHIKLMNPQRSTVWY]'
        if re.match('^(' + single_letter + '+|[X\*])$', self.cleaned_data['aa_reference']):
            return self.cleaned_data['aa_reference']
        else:
            raise forms.ValidationError('aa_reference ("' +
                                        self.cleaned_data['aa_reference'] +
                                        '") must be a string consisting of ' +
                                        'one or more amino acids, in single letter code.')

    def clean_aa_variant(self):
        single_letter = '[ACDEFGHIKLMNPQRSTVWY]'
        if re.match('^(' + single_letter + '+|[X\*])$', self.cleaned_data['aa_variant']):
            return self.cleaned_data['aa_variant']
        else:
            raise forms.ValidationError('aa_variant ("' +
                                        self.cleaned_data['aa_variant'] +
                                        '") must be a string consisting of ' +
                                        'one or more amino acids, in single letter code.')
