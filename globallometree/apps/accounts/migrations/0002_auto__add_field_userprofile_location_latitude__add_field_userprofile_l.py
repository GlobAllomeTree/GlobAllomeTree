# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding field 'UserProfile.location_latitude'
        db.add_column(u'accounts_userprofile', 'location_latitude',
                      self.gf('django.db.models.fields.DecimalField')(null=True, max_digits=8, decimal_places=5, blank=True),
                      keep_default=False)

        # Adding field 'UserProfile.location_longitude'
        db.add_column(u'accounts_userprofile', 'location_longitude',
                      self.gf('django.db.models.fields.DecimalField')(null=True, max_digits=8, decimal_places=5, blank=True),
                      keep_default=False)

        # Adding field 'UserProfile.location_country'
        db.add_column(u'accounts_userprofile', 'location_country',
                      self.gf('django.db.models.fields.related.ForeignKey')(to=orm['locations.Country'], null=True, blank=True),
                      keep_default=False)

        # Adding field 'UserProfile.privacy'
        db.add_column(u'accounts_userprofile', 'privacy',
                      self.gf('django.db.models.fields.CharField')(default='anonymous', max_length=20),
                      keep_default=False)


    def backwards(self, orm):
        # Deleting field 'UserProfile.location_latitude'
        db.delete_column(u'accounts_userprofile', 'location_latitude')

        # Deleting field 'UserProfile.location_longitude'
        db.delete_column(u'accounts_userprofile', 'location_longitude')

        # Deleting field 'UserProfile.location_country'
        db.delete_column(u'accounts_userprofile', 'location_country_id')

        # Deleting field 'UserProfile.privacy'
        db.delete_column(u'accounts_userprofile', 'privacy')


    models = {
        u'accounts.userprofile': {
            'Meta': {'object_name': 'UserProfile'},
            'address': ('django.db.models.fields.CharField', [], {'max_length': '200'}),
            'country': ('django.db.models.fields.CharField', [], {'max_length': '80', 'blank': 'True'}),
            'data_may_provide': ('django.db.models.fields.CharField', [], {'max_length': '40', 'blank': 'True'}),
            'education': ('django.db.models.fields.CharField', [], {'max_length': '300', 'blank': 'True'}),
            'field_subject': ('django.db.models.fields.CharField', [], {'max_length': '60', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'institution_address': ('django.db.models.fields.CharField', [], {'max_length': '200', 'blank': 'True'}),
            'institution_fax': ('django.db.models.fields.CharField', [], {'max_length': '60', 'blank': 'True'}),
            'institution_name': ('django.db.models.fields.CharField', [], {'max_length': '200', 'blank': 'True'}),
            'institution_phone': ('django.db.models.fields.CharField', [], {'max_length': '60', 'blank': 'True'}),
            'location_country': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['locations.Country']", 'null': 'True', 'blank': 'True'}),
            'location_latitude': ('django.db.models.fields.DecimalField', [], {'null': 'True', 'max_digits': '8', 'decimal_places': '5', 'blank': 'True'}),
            'location_longitude': ('django.db.models.fields.DecimalField', [], {'null': 'True', 'max_digits': '8', 'decimal_places': '5', 'blank': 'True'}),
            'privacy': ('django.db.models.fields.CharField', [], {'default': "'anonymous'", 'max_length': '20'}),
            'region': ('django.db.models.fields.CharField', [], {'max_length': '80', 'blank': 'True'}),
            'subregion': ('django.db.models.fields.CharField', [], {'max_length': '80', 'blank': 'True'}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['auth.User']"})
        },
        u'auth.group': {
            'Meta': {'object_name': 'Group'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '80'}),
            'permissions': ('django.db.models.fields.related.ManyToManyField', [], {'to': u"orm['auth.Permission']", 'symmetrical': 'False', 'blank': 'True'})
        },
        u'auth.permission': {
            'Meta': {'ordering': "(u'content_type__app_label', u'content_type__model', u'codename')", 'unique_together': "((u'content_type', u'codename'),)", 'object_name': 'Permission'},
            'codename': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'content_type': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['contenttypes.ContentType']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '50'})
        },
        u'auth.user': {
            'Meta': {'object_name': 'User'},
            'date_joined': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'email': ('django.db.models.fields.EmailField', [], {'max_length': '75', 'blank': 'True'}),
            'first_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'groups': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'related_name': "u'user_set'", 'blank': 'True', 'to': u"orm['auth.Group']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_active': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'is_staff': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'is_superuser': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'last_login': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'last_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'password': ('django.db.models.fields.CharField', [], {'max_length': '128'}),
            'user_permissions': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'related_name': "u'user_set'", 'blank': 'True', 'to': u"orm['auth.Permission']"}),
            'username': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '30'})
        },
        u'contenttypes.contenttype': {
            'Meta': {'ordering': "('name',)", 'unique_together': "(('app_label', 'model'),)", 'object_name': 'ContentType', 'db_table': "'django_content_type'"},
            'app_label': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'model': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        },
        u'locations.continent': {
            'Meta': {'object_name': 'Continent'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100', 'null': 'True', 'blank': 'True'})
        },
        u'locations.country': {
            'Meta': {'ordering': "('common_name',)", 'object_name': 'Country'},
            'centroid_latitude': ('django.db.models.fields.DecimalField', [], {'null': 'True', 'max_digits': '5', 'decimal_places': '2', 'blank': 'True'}),
            'centroid_longitude': ('django.db.models.fields.DecimalField', [], {'null': 'True', 'max_digits': '5', 'decimal_places': '2', 'blank': 'True'}),
            'common_name': ('django.db.models.fields.CharField', [], {'max_length': '159', 'blank': 'True'}),
            'continent': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['locations.Continent']", 'null': 'True', 'blank': 'True'}),
            'formal_name': ('django.db.models.fields.CharField', [], {'max_length': '159', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'iso_3166_1_2_letter_code': ('django.db.models.fields.CharField', [], {'max_length': '6', 'blank': 'True'}),
            'iso_3166_1_3_letter_code': ('django.db.models.fields.CharField', [], {'max_length': '9', 'blank': 'True'}),
            'iso_3166_1_number': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'})
        }
    }

    complete_apps = ['accounts']