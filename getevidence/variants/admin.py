from django.contrib import admin
from .models import Variant, VariantReview

class VariantReviewInline(admin.StackedInline):
    model = VariantReview

class VariantInline(admin.ModelAdmin):
    inlines = [VariantReviewInline]

admin.site.register(Variant, VariantInline)

