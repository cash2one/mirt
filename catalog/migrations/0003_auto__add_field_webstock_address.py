# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding field 'WebStock.address'
        db.add_column(u'catalog_webstock', 'address',
                      self.gf('django.db.models.fields.CharField')(max_length=500, null=True, blank=True),
                      keep_default=False)


    def backwards(self, orm):
        # Deleting field 'WebStock.address'
        db.delete_column(u'catalog_webstock', 'address')


    models = {
        u'catalog.accessories': {
            'Meta': {'object_name': 'Accessories'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '255'})
        },
        u'catalog.brand': {
            'Meta': {'object_name': 'Brand'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'image': ('django.db.models.fields.files.ImageField', [], {'max_length': '100', 'null': 'True', 'blank': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'onec': ('django.db.models.fields.CharField', [], {'default': 'True', 'max_length': '255', 'blank': 'True'})
        },
        u'catalog.directory': {
            'Meta': {'object_name': 'Directory'},
            'accessory': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'to': u"orm['catalog.Accessories']", 'null': 'True', 'blank': 'True'}),
            'bottom_description': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'dir_accessory': ('mptt.fields.TreeManyToManyField', [], {'blank': 'True', 'related_name': "'access_directories'", 'null': 'True', 'symmetrical': 'False', 'to': u"orm['catalog.Directory']"}),
            'directory': ('mptt.fields.TreeForeignKey', [], {'blank': 'True', 'related_name': "'subdirectory'", 'null': 'True', 'to': u"orm['catalog.Directory']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'image': ('django.db.models.fields.files.ImageField', [], {'max_length': '100', 'null': 'True', 'blank': 'True'}),
            'is_visible': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            u'level': ('django.db.models.fields.PositiveIntegerField', [], {'db_index': 'True'}),
            u'lft': ('django.db.models.fields.PositiveIntegerField', [], {'db_index': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'onec': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'order': ('django.db.models.fields.SmallIntegerField', [], {'default': '0'}),
            u'rght': ('django.db.models.fields.PositiveIntegerField', [], {'db_index': 'True'}),
            'seo_description': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'seo_keywords': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'seo_title': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'show_in_bottom_menu': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'singular_name': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'slug': ('django.db.models.fields.SlugField', [], {'max_length': '100', 'blank': 'True'}),
            'top_description': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            u'tree_id': ('django.db.models.fields.PositiveIntegerField', [], {'db_index': 'True'})
        },
        u'catalog.feature': {
            'Meta': {'object_name': 'Feature'},
            'group': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['catalog.FeatureGroup']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_filter': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'is_primary': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'onec': ('django.db.models.fields.CharField', [], {'default': 'True', 'max_length': '255', 'blank': 'True'}),
            'order': ('django.db.models.fields.SmallIntegerField', [], {'default': '0'}),
            'widget_type': ('django.db.models.fields.CharField', [], {'default': "'checkbox'", 'max_length': '255'})
        },
        u'catalog.featuregroup': {
            'Meta': {'ordering': "('name',)", 'object_name': 'FeatureGroup'},
            'directory': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'group'", 'to': u"orm['catalog.Directory']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '255'})
        },
        u'catalog.featuresonec': {
            'Meta': {'object_name': 'FeaturesOnec'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'onec': ('django.db.models.fields.CharField', [], {'default': 'True', 'max_length': '255', 'blank': 'True'})
        },
        u'catalog.featurevalue': {
            'Meta': {'ordering': "('feature__order', 'feature__name')", 'object_name': 'FeatureValue'},
            'feature': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'value'", 'to': u"orm['catalog.Feature']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'onec': ('django.db.models.fields.CharField', [], {'default': 'True', 'max_length': '255', 'blank': 'True'}),
            'order': ('django.db.models.fields.SmallIntegerField', [], {'default': '0'}),
            'product': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'product_id_for_value'", 'to': u"orm['catalog.Product']"}),
            'value': ('django.db.models.fields.CharField', [], {'max_length': '100', 'null': 'True', 'blank': 'True'})
        },
        u'catalog.featurevaluegroup': {
            'Meta': {'ordering': "('order',)", 'object_name': 'FeatureValueGroup'},
            'feature': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'value_group'", 'to': u"orm['catalog.Feature']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'order': ('django.db.models.fields.SmallIntegerField', [], {'default': '0'}),
            'regexp': ('django.db.models.fields.CharField', [], {'max_length': '255'})
        },
        u'catalog.featurevalueonec': {
            'Meta': {'object_name': 'FeatureValueOnec'},
            'brand': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'feature': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'value_onec'", 'to': u"orm['catalog.FeaturesOnec']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'onec': ('django.db.models.fields.CharField', [], {'default': 'True', 'max_length': '255', 'blank': 'True'}),
            'value': ('django.db.models.fields.CharField', [], {'max_length': '100', 'null': 'True', 'blank': 'True'})
        },
        u'catalog.image': {
            'Meta': {'object_name': 'Image'},
            'content_type': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['contenttypes.ContentType']"}),
            'file': ('django.db.models.fields.files.ImageField', [], {'max_length': '100', 'null': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_primary': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'object_id': ('django.db.models.fields.PositiveIntegerField', [], {})
        },
        u'catalog.onecstock': {
            'Meta': {'object_name': 'OneCstock'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'onec': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'webstock': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['catalog.WebStock']"})
        },
        u'catalog.product': {
            'Meta': {'ordering': "('price',)", 'object_name': 'Product'},
            'accessory': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'access_product'", 'null': 'True', 'to': u"orm['catalog.Accessories']"}),
            'articul': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'brand': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['catalog.Brand']", 'null': 'True', 'blank': 'True'}),
            'created_at': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'description': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'directory': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['catalog.Directory']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_visible': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'onec': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'onecdir': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'price': ('django.db.models.fields.DecimalField', [], {'default': '0', 'max_digits': '10', 'decimal_places': '2'}),
            'searchfield': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'short_description': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'show_on_main': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'slug': ('django.db.models.fields.SlugField', [], {'max_length': '255', 'blank': 'True'})
        },
        u'catalog.productaccessory': {
            'Meta': {'object_name': 'ProductAccessory'},
            'accessory': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'added_accessory'", 'to': u"orm['catalog.Product']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'product': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'for_product'", 'to': u"orm['catalog.Product']"})
        },
        u'catalog.promotion': {
            'Meta': {'object_name': 'Promotion'},
            'description': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'finish_at': ('django.db.models.fields.DateField', [], {'null': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'product': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['catalog.Product']"}),
            'start_at': ('django.db.models.fields.DateField', [], {'null': 'True', 'blank': 'True'}),
            'type': ('django.db.models.fields.CharField', [], {'max_length': '255'})
        },
        u'catalog.webstock': {
            'Meta': {'ordering': "('name',)", 'object_name': 'WebStock'},
            'address': ('django.db.models.fields.CharField', [], {'max_length': '500', 'null': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'lat': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'long': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'mode': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'phone': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'text': ('django.db.models.fields.TextField', [], {'max_length': '5000', 'null': 'True', 'blank': 'True'})
        },
        u'catalog.webstockproduct': {
            'Meta': {'object_name': 'WebStockProduct'},
            'count': ('django.db.models.fields.FloatField', [], {'default': '0.0'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'product': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['catalog.Product']"}),
            'webstock': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['catalog.WebStock']"})
        },
        u'contenttypes.contenttype': {
            'Meta': {'ordering': "('name',)", 'unique_together': "(('app_label', 'model'),)", 'object_name': 'ContentType', 'db_table': "'django_content_type'"},
            'app_label': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'model': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        }
    }

    complete_apps = ['catalog']