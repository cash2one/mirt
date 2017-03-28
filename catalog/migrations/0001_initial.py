# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'Accessories'
        db.create_table(u'catalog_accessories', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=255)),
        ))
        db.send_create_signal(u'catalog', ['Accessories'])

        # Adding model 'Directory'
        db.create_table(u'catalog_directory', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('singular_name', self.gf('django.db.models.fields.CharField')(max_length=255, null=True, blank=True)),
            ('directory', self.gf('mptt.fields.TreeForeignKey')(blank=True, related_name='subdirectory', null=True, to=orm['catalog.Directory'])),
            ('image', self.gf('django.db.models.fields.files.ImageField')(max_length=100, null=True, blank=True)),
            ('is_visible', self.gf('django.db.models.fields.BooleanField')(default=True)),
            ('show_in_bottom_menu', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('order', self.gf('django.db.models.fields.SmallIntegerField')(default=0)),
            ('slug', self.gf('django.db.models.fields.SlugField')(max_length=100, blank=True)),
            ('top_description', self.gf('django.db.models.fields.TextField')(null=True, blank=True)),
            ('bottom_description', self.gf('django.db.models.fields.TextField')(null=True, blank=True)),
            ('seo_title', self.gf('django.db.models.fields.TextField')(null=True, blank=True)),
            ('seo_description', self.gf('django.db.models.fields.TextField')(null=True, blank=True)),
            ('seo_keywords', self.gf('django.db.models.fields.TextField')(null=True, blank=True)),
            ('onec', self.gf('django.db.models.fields.CharField')(max_length=255, null=True, blank=True)),
            (u'lft', self.gf('django.db.models.fields.PositiveIntegerField')(db_index=True)),
            (u'rght', self.gf('django.db.models.fields.PositiveIntegerField')(db_index=True)),
            (u'tree_id', self.gf('django.db.models.fields.PositiveIntegerField')(db_index=True)),
            (u'level', self.gf('django.db.models.fields.PositiveIntegerField')(db_index=True)),
        ))
        db.send_create_signal(u'catalog', ['Directory'])

        # Adding M2M table for field accessory on 'Directory'
        m2m_table_name = db.shorten_name(u'catalog_directory_accessory')
        db.create_table(m2m_table_name, (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('directory', models.ForeignKey(orm[u'catalog.directory'], null=False)),
            ('accessories', models.ForeignKey(orm[u'catalog.accessories'], null=False))
        ))
        db.create_unique(m2m_table_name, ['directory_id', 'accessories_id'])

        # Adding M2M table for field dir_accessory on 'Directory'
        m2m_table_name = db.shorten_name(u'catalog_directory_dir_accessory')
        db.create_table(m2m_table_name, (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('from_directory', models.ForeignKey(orm[u'catalog.directory'], null=False)),
            ('to_directory', models.ForeignKey(orm[u'catalog.directory'], null=False))
        ))
        db.create_unique(m2m_table_name, ['from_directory_id', 'to_directory_id'])

        # Adding model 'Brand'
        db.create_table(u'catalog_brand', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('image', self.gf('django.db.models.fields.files.ImageField')(max_length=100, null=True, blank=True)),
            ('onec', self.gf('django.db.models.fields.CharField')(default=True, max_length=255, blank=True)),
        ))
        db.send_create_signal(u'catalog', ['Brand'])

        # Adding model 'Product'
        db.create_table(u'catalog_product', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('created_at', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('articul', self.gf('django.db.models.fields.CharField')(max_length=255, null=True, blank=True)),
            ('onec', self.gf('django.db.models.fields.CharField')(max_length=255, null=True, blank=True)),
            ('onecdir', self.gf('django.db.models.fields.CharField')(max_length=255, null=True, blank=True)),
            ('searchfield', self.gf('django.db.models.fields.CharField')(max_length=255, null=True, blank=True)),
            ('directory', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['catalog.Directory'])),
            ('brand', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['catalog.Brand'], null=True, blank=True)),
            ('price', self.gf('django.db.models.fields.DecimalField')(default=0, max_digits=10, decimal_places=2)),
            ('description', self.gf('django.db.models.fields.TextField')(blank=True)),
            ('short_description', self.gf('django.db.models.fields.CharField')(max_length=255, null=True, blank=True)),
            ('is_visible', self.gf('django.db.models.fields.BooleanField')(default=True)),
            ('slug', self.gf('django.db.models.fields.SlugField')(max_length=255, blank=True)),
            ('show_on_main', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('accessory', self.gf('django.db.models.fields.related.ForeignKey')(blank=True, related_name='access_product', null=True, to=orm['catalog.Accessories'])),
        ))
        db.send_create_signal(u'catalog', ['Product'])

        # Adding model 'ProductAccessory'
        db.create_table(u'catalog_productaccessory', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('product', self.gf('django.db.models.fields.related.ForeignKey')(related_name='for_product', to=orm['catalog.Product'])),
            ('accessory', self.gf('django.db.models.fields.related.ForeignKey')(related_name='added_accessory', to=orm['catalog.Product'])),
        ))
        db.send_create_signal(u'catalog', ['ProductAccessory'])

        # Adding model 'Image'
        db.create_table(u'catalog_image', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('file', self.gf('django.db.models.fields.files.ImageField')(max_length=100, null=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=255, null=True, blank=True)),
            ('is_primary', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('content_type', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['contenttypes.ContentType'])),
            ('object_id', self.gf('django.db.models.fields.PositiveIntegerField')()),
        ))
        db.send_create_signal(u'catalog', ['Image'])

        # Adding model 'Promotion'
        db.create_table(u'catalog_promotion', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('product', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['catalog.Product'])),
            ('type', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('description', self.gf('django.db.models.fields.TextField')(blank=True)),
            ('start_at', self.gf('django.db.models.fields.DateField')(null=True, blank=True)),
            ('finish_at', self.gf('django.db.models.fields.DateField')(null=True, blank=True)),
        ))
        db.send_create_signal(u'catalog', ['Promotion'])

        # Adding model 'FeatureGroup'
        db.create_table(u'catalog_featuregroup', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('directory', self.gf('django.db.models.fields.related.ForeignKey')(related_name='group', to=orm['catalog.Directory'])),
        ))
        db.send_create_signal(u'catalog', ['FeatureGroup'])

        # Adding model 'Feature'
        db.create_table(u'catalog_feature', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('group', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['catalog.FeatureGroup'])),
            ('widget_type', self.gf('django.db.models.fields.CharField')(default='checkbox', max_length=255)),
            ('order', self.gf('django.db.models.fields.SmallIntegerField')(default=0)),
            ('is_primary', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('is_filter', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('onec', self.gf('django.db.models.fields.CharField')(default=True, max_length=255, blank=True)),
        ))
        db.send_create_signal(u'catalog', ['Feature'])

        # Adding model 'FeatureValueGroup'
        db.create_table(u'catalog_featurevaluegroup', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('feature', self.gf('django.db.models.fields.related.ForeignKey')(related_name='value_group', to=orm['catalog.Feature'])),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('regexp', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('order', self.gf('django.db.models.fields.SmallIntegerField')(default=0)),
        ))
        db.send_create_signal(u'catalog', ['FeatureValueGroup'])

        # Adding model 'FeatureValue'
        db.create_table(u'catalog_featurevalue', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('product', self.gf('django.db.models.fields.related.ForeignKey')(related_name='product_id_for_value', to=orm['catalog.Product'])),
            ('feature', self.gf('django.db.models.fields.related.ForeignKey')(related_name='value', to=orm['catalog.Feature'])),
            ('value', self.gf('django.db.models.fields.CharField')(max_length=100, null=True, blank=True)),
            ('order', self.gf('django.db.models.fields.SmallIntegerField')(default=0)),
            ('onec', self.gf('django.db.models.fields.CharField')(default=True, max_length=255, blank=True)),
        ))
        db.send_create_signal(u'catalog', ['FeatureValue'])

        # Adding model 'FeaturesOnec'
        db.create_table(u'catalog_featuresonec', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('onec', self.gf('django.db.models.fields.CharField')(default=True, max_length=255, blank=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=255, null=True, blank=True)),
        ))
        db.send_create_signal(u'catalog', ['FeaturesOnec'])

        # Adding model 'FeatureValueOnec'
        db.create_table(u'catalog_featurevalueonec', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('onec', self.gf('django.db.models.fields.CharField')(default=True, max_length=255, blank=True)),
            ('feature', self.gf('django.db.models.fields.related.ForeignKey')(related_name='value_onec', to=orm['catalog.FeaturesOnec'])),
            ('value', self.gf('django.db.models.fields.CharField')(max_length=100, null=True, blank=True)),
            ('brand', self.gf('django.db.models.fields.BooleanField')(default=False)),
        ))
        db.send_create_signal(u'catalog', ['FeatureValueOnec'])

        # Adding model 'WebStock'
        db.create_table(u'catalog_webstock', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('text', self.gf('django.db.models.fields.TextField')(max_length=5000, null=True, blank=True)),
        ))
        db.send_create_signal(u'catalog', ['WebStock'])

        # Adding model 'WebStockProduct'
        db.create_table(u'catalog_webstockproduct', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('webstock', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['catalog.WebStock'])),
            ('product', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['catalog.Product'])),
            ('count', self.gf('django.db.models.fields.FloatField')(default=0.0)),
        ))
        db.send_create_signal(u'catalog', ['WebStockProduct'])

        # Adding model 'OneCstock'
        db.create_table(u'catalog_onecstock', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('webstock', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['catalog.WebStock'])),
            ('onec', self.gf('django.db.models.fields.CharField')(max_length=255)),
        ))
        db.send_create_signal(u'catalog', ['OneCstock'])


    def backwards(self, orm):
        # Deleting model 'Accessories'
        db.delete_table(u'catalog_accessories')

        # Deleting model 'Directory'
        db.delete_table(u'catalog_directory')

        # Removing M2M table for field accessory on 'Directory'
        db.delete_table(db.shorten_name(u'catalog_directory_accessory'))

        # Removing M2M table for field dir_accessory on 'Directory'
        db.delete_table(db.shorten_name(u'catalog_directory_dir_accessory'))

        # Deleting model 'Brand'
        db.delete_table(u'catalog_brand')

        # Deleting model 'Product'
        db.delete_table(u'catalog_product')

        # Deleting model 'ProductAccessory'
        db.delete_table(u'catalog_productaccessory')

        # Deleting model 'Image'
        db.delete_table(u'catalog_image')

        # Deleting model 'Promotion'
        db.delete_table(u'catalog_promotion')

        # Deleting model 'FeatureGroup'
        db.delete_table(u'catalog_featuregroup')

        # Deleting model 'Feature'
        db.delete_table(u'catalog_feature')

        # Deleting model 'FeatureValueGroup'
        db.delete_table(u'catalog_featurevaluegroup')

        # Deleting model 'FeatureValue'
        db.delete_table(u'catalog_featurevalue')

        # Deleting model 'FeaturesOnec'
        db.delete_table(u'catalog_featuresonec')

        # Deleting model 'FeatureValueOnec'
        db.delete_table(u'catalog_featurevalueonec')

        # Deleting model 'WebStock'
        db.delete_table(u'catalog_webstock')

        # Deleting model 'WebStockProduct'
        db.delete_table(u'catalog_webstockproduct')

        # Deleting model 'OneCstock'
        db.delete_table(u'catalog_onecstock')


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
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
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