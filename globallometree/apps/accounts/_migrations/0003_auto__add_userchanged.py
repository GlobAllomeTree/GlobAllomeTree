# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'UserChanged'
        db.create_table(u'accounts_userchanged', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('user', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['auth.User'])),
        ))
        db.send_create_signal(u'accounts', ['UserChanged'])


    def backwards(self, orm):
        # Deleting model 'UserChanged'
        db.delete_table(u'accounts_userchanged')


    models = {
        u'accounts.userchanged': {
            'Meta': {'object_name': 'UserChanged'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['auth.User']"})
        },
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
            'Code': ('django.db.models.fields.CharField', [], {'max_length': '2'}),
            'Continent_ID': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'Created': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'Meta': {'object_name': 'Continent', 'db_table': "'Continent'"},
            'Modified': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'}),
            'Name': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        },
        u'locations.country': {
            'Centroid_latitude': ('django.db.models.fields.DecimalField', [], {'null': 'True', 'max_digits': '5', 'decimal_places': '2', 'blank': 'True'}),
            'Centroid_longitude': ('django.db.models.fields.DecimalField', [], {'null': 'True', 'max_digits': '5', 'decimal_places': '2', 'blank': 'True'}),
            'Common_name': ('django.db.models.fields.CharField', [], {'max_length': '159', 'blank': 'True'}),
            'Common_name_fr': ('django.db.models.fields.CharField', [], {'max_length': '159', 'blank': 'True'}),
            'Continent': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['locations.Continent']", 'null': 'True', 'db_column': "'Continent_ID'", 'blank': 'True'}),
            'Country_ID': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'Created': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'Formal_name': ('django.db.models.fields.CharField', [], {'max_length': '159', 'blank': 'True'}),
            'Formal_name_fr': ('django.db.models.fields.CharField', [], {'max_length': '159', 'blank': 'True'}),
            'Iso3166a2': ('django.db.models.fields.CharField', [], {'max_length': '6', 'blank': 'True'}),
            'Iso3166a3': ('django.db.models.fields.CharField', [], {'max_length': '9', 'blank': 'True'}),
            'Iso3166n3': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'Meta': {'ordering': "('Common_name',)", 'object_name': 'Country', 'db_table': "'Country'"},
            'Modified': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'})
        }
    }

    complete_apps = ['accounts']