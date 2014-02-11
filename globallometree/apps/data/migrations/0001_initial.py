# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'Country'
        db.create_table(u'data_country', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('common_name', self.gf('django.db.models.fields.CharField')(max_length=159, blank=True)),
            ('formal_name', self.gf('django.db.models.fields.CharField')(max_length=159, blank=True)),
            ('type', self.gf('django.db.models.fields.CharField')(max_length=69, blank=True)),
            ('sub_type', self.gf('django.db.models.fields.CharField')(max_length=102, blank=True)),
            ('sovereignty', self.gf('django.db.models.fields.CharField')(max_length=72, blank=True)),
            ('capital', self.gf('django.db.models.fields.CharField')(max_length=234, blank=True)),
            ('iso_4217_currency_code', self.gf('django.db.models.fields.CharField')(max_length=33, blank=True)),
            ('iso_4217_currency_name', self.gf('django.db.models.fields.CharField')(max_length=42, blank=True)),
            ('telephone_code', self.gf('django.db.models.fields.CharField')(max_length=48, blank=True)),
            ('iso_3166_1_2_letter_code', self.gf('django.db.models.fields.CharField')(max_length=6, blank=True)),
            ('iso_3166_1_3_letter_code', self.gf('django.db.models.fields.CharField')(max_length=9, blank=True)),
            ('iso_3166_1_number', self.gf('django.db.models.fields.IntegerField')(null=True, blank=True)),
            ('iana_country_code_tld', self.gf('django.db.models.fields.CharField')(max_length=33, blank=True)),
        ))
        db.send_create_signal(u'data', ['Country'])

        # Adding model 'DataSubmission'
        db.create_table(u'data_datasubmission', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('submitted_file', self.gf('django.db.models.fields.files.FileField')(max_length=100)),
            ('submitted_notes', self.gf('django.db.models.fields.TextField')(null=True, blank=True)),
            ('date_uploaded', self.gf('django.db.models.fields.DateField')(auto_now_add=True, blank=True)),
            ('user', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['auth.User'])),
            ('imported', self.gf('django.db.models.fields.BooleanField')()),
        ))
        db.send_create_signal(u'data', ['DataSubmission'])

        # Adding model 'TreeEquation'
        db.create_table(u'data_treeequation', (
            ('ID', self.gf('django.db.models.fields.IntegerField')(primary_key=True)),
            ('data_submission', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['data.DataSubmission'], null=True, blank=True)),
            ('IDequation', self.gf('django.db.models.fields.IntegerField')(null=True, blank=True)),
            ('Population', self.gf('django.db.models.fields.CharField')(max_length=255, null=True, blank=True)),
            ('Ecosystem', self.gf('django.db.models.fields.CharField')(max_length=255, null=True, blank=True)),
            ('Continent', self.gf('django.db.models.fields.CharField')(max_length=100, null=True, blank=True)),
            ('Country', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['data.Country'], null=True, blank=True)),
            ('ID_Location', self.gf('django.db.models.fields.IntegerField')(null=True, blank=True)),
            ('Group_Location', self.gf('django.db.models.fields.IntegerField')(null=True, blank=True)),
            ('Location', self.gf('django.db.models.fields.CharField')(max_length=255, null=True, blank=True)),
            ('Latitude', self.gf('django.db.models.fields.DecimalField')(null=True, max_digits=12, decimal_places=9, blank=True)),
            ('Longitude', self.gf('django.db.models.fields.DecimalField')(null=True, max_digits=12, decimal_places=9, blank=True)),
            ('Biome_FAO', self.gf('django.db.models.fields.CharField')(max_length=200, null=True, blank=True)),
            ('Biome_UDVARDY', self.gf('django.db.models.fields.CharField')(max_length=200, null=True, blank=True)),
            ('Biome_WWF', self.gf('django.db.models.fields.CharField')(max_length=200, null=True, blank=True)),
            ('Division_BAILEY', self.gf('django.db.models.fields.CharField')(max_length=200, null=True, blank=True)),
            ('Biome_HOLDRIDGE', self.gf('django.db.models.fields.CharField')(max_length=200, null=True, blank=True)),
            ('X', self.gf('django.db.models.fields.CharField')(max_length=20, null=True, blank=True)),
            ('Unit_X', self.gf('django.db.models.fields.CharField')(max_length=20, null=True, blank=True)),
            ('Z', self.gf('django.db.models.fields.CharField')(max_length=20, null=True, blank=True)),
            ('Unit_Z', self.gf('django.db.models.fields.CharField')(max_length=20, null=True, blank=True)),
            ('W', self.gf('django.db.models.fields.CharField')(max_length=20, null=True, blank=True)),
            ('Unit_W', self.gf('django.db.models.fields.CharField')(max_length=20, null=True, blank=True)),
            ('U', self.gf('django.db.models.fields.CharField')(max_length=20, null=True, blank=True)),
            ('Unit_U', self.gf('django.db.models.fields.CharField')(max_length=20, null=True, blank=True)),
            ('V', self.gf('django.db.models.fields.CharField')(max_length=20, null=True, blank=True)),
            ('Unit_V', self.gf('django.db.models.fields.CharField')(max_length=20, blank=True)),
            ('Min_X', self.gf('django.db.models.fields.DecimalField')(null=True, max_digits=16, decimal_places=10, blank=True)),
            ('Max_X', self.gf('django.db.models.fields.DecimalField')(null=True, max_digits=16, decimal_places=10, blank=True)),
            ('Min_Z', self.gf('django.db.models.fields.DecimalField')(null=True, max_digits=16, decimal_places=10, blank=True)),
            ('Max_Z', self.gf('django.db.models.fields.DecimalField')(null=True, max_digits=16, decimal_places=10, blank=True)),
            ('Output', self.gf('django.db.models.fields.CharField')(max_length=30, null=True, blank=True)),
            ('Output_TR', self.gf('django.db.models.fields.CharField')(max_length=30, null=True, blank=True)),
            ('Unit_Y', self.gf('django.db.models.fields.CharField')(max_length=50, null=True, blank=True)),
            ('Age', self.gf('django.db.models.fields.CharField')(max_length=50, null=True, blank=True)),
            ('Veg_Component', self.gf('django.db.models.fields.CharField')(max_length=150, null=True, blank=True)),
            ('B', self.gf('django.db.models.fields.NullBooleanField')(null=True, blank=True)),
            ('Bd', self.gf('django.db.models.fields.NullBooleanField')(null=True, blank=True)),
            ('Bg', self.gf('django.db.models.fields.NullBooleanField')(null=True, blank=True)),
            ('Bt', self.gf('django.db.models.fields.NullBooleanField')(null=True, blank=True)),
            ('L', self.gf('django.db.models.fields.NullBooleanField')(null=True, blank=True)),
            ('Rb', self.gf('django.db.models.fields.NullBooleanField')(null=True, blank=True)),
            ('Rf', self.gf('django.db.models.fields.NullBooleanField')(null=True, blank=True)),
            ('Rm', self.gf('django.db.models.fields.NullBooleanField')(null=True, blank=True)),
            ('S', self.gf('django.db.models.fields.NullBooleanField')(null=True, blank=True)),
            ('T', self.gf('django.db.models.fields.NullBooleanField')(null=True, blank=True)),
            ('F', self.gf('django.db.models.fields.NullBooleanField')(null=True, blank=True)),
            ('ID_Species', self.gf('django.db.models.fields.IntegerField')(null=True, blank=True)),
            ('Family', self.gf('django.db.models.fields.CharField')(max_length=80, null=True, blank=True)),
            ('Genus', self.gf('django.db.models.fields.CharField')(max_length=80, null=True, blank=True)),
            ('Species', self.gf('django.db.models.fields.CharField')(max_length=80, null=True, blank=True)),
            ('Group_Species', self.gf('django.db.models.fields.IntegerField')(null=True, blank=True)),
            ('ID_Group', self.gf('django.db.models.fields.IntegerField')(null=True, blank=True)),
            ('Equation', self.gf('django.db.models.fields.CharField')(max_length=500, null=True, blank=True)),
            ('Substitute_equation', self.gf('django.db.models.fields.CharField')(max_length=500, null=True, blank=True)),
            ('Top_dob', self.gf('django.db.models.fields.DecimalField')(null=True, max_digits=16, decimal_places=10, blank=True)),
            ('Stump_height', self.gf('django.db.models.fields.DecimalField')(null=True, max_digits=16, decimal_places=10, blank=True)),
            ('ID_REF', self.gf('django.db.models.fields.IntegerField')(null=True, blank=True)),
            ('Label', self.gf('django.db.models.fields.CharField')(max_length=20, null=True, blank=True)),
            ('Author', self.gf('django.db.models.fields.CharField')(max_length=200, null=True, blank=True)),
            ('Year', self.gf('django.db.models.fields.CharField')(max_length=12, null=True, blank=True)),
            ('Reference', self.gf('django.db.models.fields.TextField')(null=True, blank=True)),
            ('R2', self.gf('django.db.models.fields.DecimalField')(null=True, max_digits=16, decimal_places=10, blank=True)),
            ('R2_Adjusted', self.gf('django.db.models.fields.DecimalField')(null=True, max_digits=16, decimal_places=10, blank=True)),
            ('RMSE', self.gf('django.db.models.fields.DecimalField')(null=True, max_digits=16, decimal_places=10, blank=True)),
            ('SEE', self.gf('django.db.models.fields.DecimalField')(null=True, max_digits=16, decimal_places=10, blank=True)),
            ('Corrected_for_bias', self.gf('django.db.models.fields.NullBooleanField')(null=True, blank=True)),
            ('Bias_correction', self.gf('django.db.models.fields.DecimalField')(null=True, max_digits=16, decimal_places=10, blank=True)),
            ('Ratio_equation', self.gf('django.db.models.fields.NullBooleanField')(null=True, blank=True)),
            ('Segmented_equation', self.gf('django.db.models.fields.NullBooleanField')(null=True, blank=True)),
            ('Sample_size', self.gf('django.db.models.fields.CharField')(max_length=150, null=True, blank=True)),
            ('Contributor', self.gf('django.db.models.fields.CharField')(max_length=150, null=True, blank=True)),
            ('Name_operator', self.gf('django.db.models.fields.CharField')(max_length=150, null=True, blank=True)),
        ))
        db.send_create_signal(u'data', ['TreeEquation'])


    def backwards(self, orm):
        # Deleting model 'Country'
        db.delete_table(u'data_country')

        # Deleting model 'DataSubmission'
        db.delete_table(u'data_datasubmission')

        # Deleting model 'TreeEquation'
        db.delete_table(u'data_treeequation')


    models = {
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
        u'data.country': {
            'Meta': {'object_name': 'Country'},
            'capital': ('django.db.models.fields.CharField', [], {'max_length': '234', 'blank': 'True'}),
            'common_name': ('django.db.models.fields.CharField', [], {'max_length': '159', 'blank': 'True'}),
            'formal_name': ('django.db.models.fields.CharField', [], {'max_length': '159', 'blank': 'True'}),
            'iana_country_code_tld': ('django.db.models.fields.CharField', [], {'max_length': '33', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'iso_3166_1_2_letter_code': ('django.db.models.fields.CharField', [], {'max_length': '6', 'blank': 'True'}),
            'iso_3166_1_3_letter_code': ('django.db.models.fields.CharField', [], {'max_length': '9', 'blank': 'True'}),
            'iso_3166_1_number': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'iso_4217_currency_code': ('django.db.models.fields.CharField', [], {'max_length': '33', 'blank': 'True'}),
            'iso_4217_currency_name': ('django.db.models.fields.CharField', [], {'max_length': '42', 'blank': 'True'}),
            'sovereignty': ('django.db.models.fields.CharField', [], {'max_length': '72', 'blank': 'True'}),
            'sub_type': ('django.db.models.fields.CharField', [], {'max_length': '102', 'blank': 'True'}),
            'telephone_code': ('django.db.models.fields.CharField', [], {'max_length': '48', 'blank': 'True'}),
            'type': ('django.db.models.fields.CharField', [], {'max_length': '69', 'blank': 'True'})
        },
        u'data.datasubmission': {
            'Meta': {'object_name': 'DataSubmission'},
            'date_uploaded': ('django.db.models.fields.DateField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'imported': ('django.db.models.fields.BooleanField', [], {}),
            'submitted_file': ('django.db.models.fields.files.FileField', [], {'max_length': '100'}),
            'submitted_notes': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['auth.User']"})
        },
        u'data.treeequation': {
            'Age': ('django.db.models.fields.CharField', [], {'max_length': '50', 'null': 'True', 'blank': 'True'}),
            'Author': ('django.db.models.fields.CharField', [], {'max_length': '200', 'null': 'True', 'blank': 'True'}),
            'B': ('django.db.models.fields.NullBooleanField', [], {'null': 'True', 'blank': 'True'}),
            'Bd': ('django.db.models.fields.NullBooleanField', [], {'null': 'True', 'blank': 'True'}),
            'Bg': ('django.db.models.fields.NullBooleanField', [], {'null': 'True', 'blank': 'True'}),
            'Bias_correction': ('django.db.models.fields.DecimalField', [], {'null': 'True', 'max_digits': '16', 'decimal_places': '10', 'blank': 'True'}),
            'Biome_FAO': ('django.db.models.fields.CharField', [], {'max_length': '200', 'null': 'True', 'blank': 'True'}),
            'Biome_HOLDRIDGE': ('django.db.models.fields.CharField', [], {'max_length': '200', 'null': 'True', 'blank': 'True'}),
            'Biome_UDVARDY': ('django.db.models.fields.CharField', [], {'max_length': '200', 'null': 'True', 'blank': 'True'}),
            'Biome_WWF': ('django.db.models.fields.CharField', [], {'max_length': '200', 'null': 'True', 'blank': 'True'}),
            'Bt': ('django.db.models.fields.NullBooleanField', [], {'null': 'True', 'blank': 'True'}),
            'Continent': ('django.db.models.fields.CharField', [], {'max_length': '100', 'null': 'True', 'blank': 'True'}),
            'Contributor': ('django.db.models.fields.CharField', [], {'max_length': '150', 'null': 'True', 'blank': 'True'}),
            'Corrected_for_bias': ('django.db.models.fields.NullBooleanField', [], {'null': 'True', 'blank': 'True'}),
            'Country': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['data.Country']", 'null': 'True', 'blank': 'True'}),
            'Division_BAILEY': ('django.db.models.fields.CharField', [], {'max_length': '200', 'null': 'True', 'blank': 'True'}),
            'Ecosystem': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'Equation': ('django.db.models.fields.CharField', [], {'max_length': '500', 'null': 'True', 'blank': 'True'}),
            'F': ('django.db.models.fields.NullBooleanField', [], {'null': 'True', 'blank': 'True'}),
            'Family': ('django.db.models.fields.CharField', [], {'max_length': '80', 'null': 'True', 'blank': 'True'}),
            'Genus': ('django.db.models.fields.CharField', [], {'max_length': '80', 'null': 'True', 'blank': 'True'}),
            'Group_Location': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'Group_Species': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'ID': ('django.db.models.fields.IntegerField', [], {'primary_key': 'True'}),
            'ID_Group': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'ID_Location': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'ID_REF': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'ID_Species': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'IDequation': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'L': ('django.db.models.fields.NullBooleanField', [], {'null': 'True', 'blank': 'True'}),
            'Label': ('django.db.models.fields.CharField', [], {'max_length': '20', 'null': 'True', 'blank': 'True'}),
            'Latitude': ('django.db.models.fields.DecimalField', [], {'null': 'True', 'max_digits': '12', 'decimal_places': '9', 'blank': 'True'}),
            'Location': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'Longitude': ('django.db.models.fields.DecimalField', [], {'null': 'True', 'max_digits': '12', 'decimal_places': '9', 'blank': 'True'}),
            'Max_X': ('django.db.models.fields.DecimalField', [], {'null': 'True', 'max_digits': '16', 'decimal_places': '10', 'blank': 'True'}),
            'Max_Z': ('django.db.models.fields.DecimalField', [], {'null': 'True', 'max_digits': '16', 'decimal_places': '10', 'blank': 'True'}),
            'Meta': {'object_name': 'TreeEquation'},
            'Min_X': ('django.db.models.fields.DecimalField', [], {'null': 'True', 'max_digits': '16', 'decimal_places': '10', 'blank': 'True'}),
            'Min_Z': ('django.db.models.fields.DecimalField', [], {'null': 'True', 'max_digits': '16', 'decimal_places': '10', 'blank': 'True'}),
            'Name_operator': ('django.db.models.fields.CharField', [], {'max_length': '150', 'null': 'True', 'blank': 'True'}),
            'Output': ('django.db.models.fields.CharField', [], {'max_length': '30', 'null': 'True', 'blank': 'True'}),
            'Output_TR': ('django.db.models.fields.CharField', [], {'max_length': '30', 'null': 'True', 'blank': 'True'}),
            'Population': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'R2': ('django.db.models.fields.DecimalField', [], {'null': 'True', 'max_digits': '16', 'decimal_places': '10', 'blank': 'True'}),
            'R2_Adjusted': ('django.db.models.fields.DecimalField', [], {'null': 'True', 'max_digits': '16', 'decimal_places': '10', 'blank': 'True'}),
            'RMSE': ('django.db.models.fields.DecimalField', [], {'null': 'True', 'max_digits': '16', 'decimal_places': '10', 'blank': 'True'}),
            'Ratio_equation': ('django.db.models.fields.NullBooleanField', [], {'null': 'True', 'blank': 'True'}),
            'Rb': ('django.db.models.fields.NullBooleanField', [], {'null': 'True', 'blank': 'True'}),
            'Reference': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'Rf': ('django.db.models.fields.NullBooleanField', [], {'null': 'True', 'blank': 'True'}),
            'Rm': ('django.db.models.fields.NullBooleanField', [], {'null': 'True', 'blank': 'True'}),
            'S': ('django.db.models.fields.NullBooleanField', [], {'null': 'True', 'blank': 'True'}),
            'SEE': ('django.db.models.fields.DecimalField', [], {'null': 'True', 'max_digits': '16', 'decimal_places': '10', 'blank': 'True'}),
            'Sample_size': ('django.db.models.fields.CharField', [], {'max_length': '150', 'null': 'True', 'blank': 'True'}),
            'Segmented_equation': ('django.db.models.fields.NullBooleanField', [], {'null': 'True', 'blank': 'True'}),
            'Species': ('django.db.models.fields.CharField', [], {'max_length': '80', 'null': 'True', 'blank': 'True'}),
            'Stump_height': ('django.db.models.fields.DecimalField', [], {'null': 'True', 'max_digits': '16', 'decimal_places': '10', 'blank': 'True'}),
            'Substitute_equation': ('django.db.models.fields.CharField', [], {'max_length': '500', 'null': 'True', 'blank': 'True'}),
            'T': ('django.db.models.fields.NullBooleanField', [], {'null': 'True', 'blank': 'True'}),
            'Top_dob': ('django.db.models.fields.DecimalField', [], {'null': 'True', 'max_digits': '16', 'decimal_places': '10', 'blank': 'True'}),
            'U': ('django.db.models.fields.CharField', [], {'max_length': '20', 'null': 'True', 'blank': 'True'}),
            'Unit_U': ('django.db.models.fields.CharField', [], {'max_length': '20', 'null': 'True', 'blank': 'True'}),
            'Unit_V': ('django.db.models.fields.CharField', [], {'max_length': '20', 'blank': 'True'}),
            'Unit_W': ('django.db.models.fields.CharField', [], {'max_length': '20', 'null': 'True', 'blank': 'True'}),
            'Unit_X': ('django.db.models.fields.CharField', [], {'max_length': '20', 'null': 'True', 'blank': 'True'}),
            'Unit_Y': ('django.db.models.fields.CharField', [], {'max_length': '50', 'null': 'True', 'blank': 'True'}),
            'Unit_Z': ('django.db.models.fields.CharField', [], {'max_length': '20', 'null': 'True', 'blank': 'True'}),
            'V': ('django.db.models.fields.CharField', [], {'max_length': '20', 'null': 'True', 'blank': 'True'}),
            'Veg_Component': ('django.db.models.fields.CharField', [], {'max_length': '150', 'null': 'True', 'blank': 'True'}),
            'W': ('django.db.models.fields.CharField', [], {'max_length': '20', 'null': 'True', 'blank': 'True'}),
            'X': ('django.db.models.fields.CharField', [], {'max_length': '20', 'null': 'True', 'blank': 'True'}),
            'Year': ('django.db.models.fields.CharField', [], {'max_length': '12', 'null': 'True', 'blank': 'True'}),
            'Z': ('django.db.models.fields.CharField', [], {'max_length': '20', 'null': 'True', 'blank': 'True'}),
            'data_submission': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['data.DataSubmission']", 'null': 'True', 'blank': 'True'})
        }
    }

    complete_apps = ['data']