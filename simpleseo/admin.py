# -*- coding: utf-8 -*-

from django.contrib.contenttypes import generic
from simpleseo.models import BasicMetadata


class MetadataFormset(generic.BaseGenericInlineFormSet):
    def _construct_form(self, i, **kwargs):
        form = super(MetadataFormset, self)._construct_form(i, **kwargs)

        form.empty_permitted = False
        form.has_changed = lambda: True

        if self.instance:
            self.instance.__seo_metadata_handled = True

        return form


def seo_inline():
    attrs = {
        'max_num': 1,
        'extra': 1,
        'model': BasicMetadata,
        'ct_field': "item_model",
        'ct_fk_field': "item_id",
        'formset': MetadataFormset,
        }
    return type('MetadataInline', (generic.GenericStackedInline,), attrs)
