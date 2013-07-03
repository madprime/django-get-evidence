"""
=============
Variant views
=============

Views
=====
index:       view to list Variants
new:         view to create new Variant
edit:        view to edit Variant
detail:      view to display Variant

"""

from django.http import HttpResponse, HttpResponseRedirect
from django.db import IntegrityError
from django.shortcuts import render
from django.core.urlresolvers import reverse
from .models import Variant, VariantReview, VariantPublicationReview
from .forms import VariantReviewForm

def index(request):
    """Lists Variants."""
    variant_list = Variant.objects.order_by('gene__hgnc_name')
    return render(request, 'variants/index.html', {'variant_list': variant_list})


def edit(request, variant_pattern):
    """Edits VariantReview data for a Variant."""
    try:
        variant = Variant.variant_lookup(variant_pattern)
        if request.method == 'POST':
            form = VariantReviewForm(request.POST, instance=variant.variantreview)
            form.save()
            return HttpResponseRedirect(reverse('variants:detail',
                                                args=(variant_pattern,)))
        else:
            return render(request, 'variants/edit.html',
                      {'variant': variant,
                       'variant_review': variant.variantreview,
                       'dbsnps': variant.dbsnps.all(),
                       'form': VariantReviewForm(instance=variant.variantreview)
                       })
    except AssertionError:
        return HttpResponse("Submit edit - Badly formatted variant? " + 
                            variant_pattern)
    except Variant.DoesNotExist:
        return HttpResponse("Submit edit - No variant found? " + 
                            variant_pattern)


def add_pub(request, variant_pattern):
    """Add publication to variant."""
    try:
        variant = Variant.variant_lookup(variant_pattern)
        varpubreviews = VariantPublicationReview.objects.filter(
                            variantreview__id=variant.variantreview.id)
        if not request.method == 'POST':
            return render(request, 'variants/add_pub.html',
                          {'variant': variant,
                           'variant_review': variant.variantreview,
                           'dbsnps': variant.dbsnps.all(),
                           'varpubreviews': varpubreviews,
                           })
        else:
            varpubreview = VariantPublicationReview.create(
                               variantreview = variant.variantreview,
                               pmid = request.POST['pmid'])
            try:
                varpubreview.save()
            except IntegrityError:
                return HttpResponse("Sorry, this publication is already added.")
            return HttpResponseRedirect(reverse('variants:detail',
                                                args=(variant_pattern,)))

    except AssertionError:
        return HttpResponse("Add publication - Badly formatted variant? " +
                            variant_pattern)
    except Variant.DoesNotExist:
        return HttpResponse("Add publication - No variant found? " +
                            variant_pattern)


def new(request, error=None):
    """Create new Variant."""
    if not request.method == 'POST':
        return render(request, 'variants/new.html', {'error': error})
    else:
        variant_string = (request.POST['gene'] + '-' +
                          request.POST['aa_reference'] +
                          request.POST['aa_position'] +
                          request.POST['aa_variant'])
        try:
            Variant.parse_variant(variant_string)
        except (AssertionError, ValueError):
            return HttpResponse("Sorry, variant data looks poorly formatted.")
        try:
            Variant.variant_lookup(variant_string)
            return HttpResponse("Sorry, this variant already exists.")
        except Variant.DoesNotExist:
            # The Variant.create() classmethod also creates a VariantReview
            # and, if necessary, a Gene.
            Variant.create(gene_name = request.POST['gene'],
                           aa_ref = request.POST['aa_reference'],
                           aa_pos = request.POST['aa_position'],
                           aa_var = request.POST['aa_variant'])
            return HttpResponseRedirect(reverse('variants:index'))


def detail(request, variant_pattern):
    """Display Variant and VariantReview data for viewing or editing.

    Default template displays for viewing. Another template may be used 
    to provide forms for editing.

    """
    try:
        variant = Variant.variant_lookup(variant_pattern)
        varpubreviews = VariantPublicationReview.objects.filter(
                            variantreview__id=variant.variantreview.id)
        return render(request, 'variants/detail.html',
                      {'variant': variant,
                       'variant_review': variant.variantreview,
                       'dbsnps': variant.dbsnps.all(),
                       'varpubreviews': varpubreviews,
                       })
    except AssertionError:
        return HttpResponse("Badly formatted variant? " + variant_pattern)
    except Variant.DoesNotExist:
        return HttpResponse("No variant found? " + variant_pattern)
