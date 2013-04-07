"""
=============
Variant views
=============

Views
=====

submit_edit: update Variant based on POST data
submit_new:  create Variant based on POST data
index:       view to list Variants
new:         view to create new Variant
edit:        view to edit Variant
detail:      view to display Variant

"""

from django.http import HttpResponse, HttpResponseRedirect
from django.db import IntegrityError
from django.shortcuts import render
from django.core.urlresolvers import reverse
from genes.models import gene_lookup, Gene
from .models import parse_variant, variant_lookup, Variant, VariantReview


def index(request):
    """Lists Variants."""
    variant_list = Variant.objects.order_by('gene__hgnc_name')
    return render(request, 'variants/index.html', {'variant_list': variant_list})


def submit_edit(request, variant_pattern):
    """Edits Variant based on POST data."""
    try:
        variant = variant_lookup(variant_pattern)
        variant.variantreview.review_long = request.POST['variant_review_long']
        variant.variantreview.save()
        return HttpResponseRedirect(reverse('variants:detail', 
                                            args=(variant_pattern,)))
    except AssertionError:
        return HttpResponse("Submit edit - Badly formatted variant? " + 
                            variant_pattern)
    except Variant.DoesNotExist:
        return HttpResponse("Submit edit - No variant found? " + 
                            variant_pattern)


def submit_new(request):
    """Creates new Variant based on POST data."""

    gene_name = aa_ref = aa_pos = aa_var = None

    # If parse_variant works: create gene, variant, and variantreview.
    try:
        gene_name = request.POST['gene']
        aa_ref = request.POST['aa_reference']
        aa_pos = int(request.POST['aa_position'])
        aa_var = request.POST['aa_variant']

        # Test that combined string is parseable.
        variant_string = gene_name + '-' + aa_ref + str(aa_pos) + aa_var
        parse_variant(variant_string)
    except (AssertionError, ValueError):
        return HttpResponse("Sorry, your variant data looks poorly formatted.")

    # Check if gene already exists, otherwise create and save.
    try:
        gene = gene_lookup(request.POST['gene'])
    except Gene.DoesNotExist:
        gene = Gene(hgnc_name=request.POST['gene'])
        gene.save()

    variant = Variant(gene = gene,
                      aa_reference = aa_ref,
                      aa_position = aa_pos,
                      aa_variant = aa_var)
    try:
        variant.save()
    except IntegrityError:
        return HttpResponse("Sorry, this variant already exists.)")
    variantreview = VariantReview(variant = variant, review_long = '')
    variantreview.save()
    return HttpResponseRedirect(reverse('variants:index'))


def new(request, error=None):
    """Requests data to create new Variant."""
    return render(request, 'variants/new.html', {'error': error})


def detail(request, variant_pattern, template='variants/detail.html'):
    """Display Variant and VariantReview data for viewing or editing.

    Default template displays for viewing. Another template may be used 
    to provide forms for editing.

    """
    try:
        variant = variant_lookup(variant_pattern)
        return render(request, template,
                      {'variant': variant,
                       'variant_review': variant.variantreview,
                       'dbsnps': variant.dbsnps.all(),
                       })
    except AssertionError:
        return HttpResponse("Badly formatted variant? " + variant_pattern)
    except Variant.DoesNotExist:
        return HttpResponse("No variant found? " + variant_pattern)
