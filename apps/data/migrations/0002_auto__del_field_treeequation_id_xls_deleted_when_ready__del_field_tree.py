# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Deleting field 'TreeEquation.id_xls_deleted_when_ready'
        db.delete_column('data_treeequation', 'id_xls_deleted_when_ready')

        # Deleting field 'TreeEquation.id_article'
        db.delete_column('data_treeequation', 'id_article')

        # Adding field 'TreeEquation.contributor'
        db.add_column('data_treeequation', 'contributor',
                      self.gf('django.db.models.fields.CharField')(max_length=100, null=True, blank=True),
                      keep_default=False)

        # Adding field 'TreeEquation.name_operator'
        db.add_column('data_treeequation', 'name_operator',
                      self.gf('django.db.models.fields.CharField')(max_length=100, null=True, blank=True),
                      keep_default=False)


    def backwards(self, orm):
        # Adding field 'TreeEquation.id_xls_deleted_when_ready'
        db.add_column('data_treeequation', 'id_xls_deleted_when_ready',
                      self.gf('django.db.models.fields.IntegerField')(null=True, blank=True),
                      keep_default=False)

        # Adding field 'TreeEquation.id_article'
        db.add_column('data_treeequation', 'id_article',
                      self.gf('django.db.models.fields.IntegerField')(null=True, blank=True),
                      keep_default=False)

        # Deleting field 'TreeEquation.contributor'
        db.delete_column('data_treeequation', 'contributor')

        # Deleting field 'TreeEquation.name_operator'
        db.delete_column('data_treeequation', 'name_operator')


    models = {
        'data.country': {
            'Meta': {'object_name': 'Country'},
            'capital': ('django.db.models.fields.CharField', [], {'max_length': '234', 'blank': 'True'}),
            'common_name': ('django.db.models.fields.CharField', [], {'max_length': '159', 'blank': 'True'}),
            'formal_name': ('django.db.models.fields.CharField', [], {'max_length': '159', 'blank': 'True'}),
            'iana_country_code_tld': ('django.db.models.fields.CharField', [], {'max_length': '33', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
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
        'data.treeequation': {
            'B': ('django.db.models.fields.NullBooleanField', [], {'null': 'True', 'blank': 'True'}),
            'Bd': ('django.db.models.fields.NullBooleanField', [], {'null': 'True', 'blank': 'True'}),
            'Bg': ('django.db.models.fields.NullBooleanField', [], {'null': 'True', 'blank': 'True'}),
            'Bt': ('django.db.models.fields.NullBooleanField', [], {'null': 'True', 'blank': 'True'}),
            'F': ('django.db.models.fields.NullBooleanField', [], {'null': 'True', 'blank': 'True'}),
            'L': ('django.db.models.fields.NullBooleanField', [], {'null': 'True', 'blank': 'True'}),
            'Meta': {'object_name': 'TreeEquation'},
            'Rb': ('django.db.models.fields.NullBooleanField', [], {'null': 'True', 'blank': 'True'}),
            'Rf': ('django.db.models.fields.NullBooleanField', [], {'null': 'True', 'blank': 'True'}),
            'Rm': ('django.db.models.fields.NullBooleanField', [], {'null': 'True', 'blank': 'True'}),
            'S': ('django.db.models.fields.NullBooleanField', [], {'null': 'True', 'blank': 'True'}),
            'T': ('django.db.models.fields.NullBooleanField', [], {'null': 'True', 'blank': 'True'}),
            'U': ('django.db.models.fields.CharField', [], {'max_length': '10', 'null': 'True', 'blank': 'True'}),
            'V': ('django.db.models.fields.CharField', [], {'max_length': '10', 'null': 'True', 'blank': 'True'}),
            'W': ('django.db.models.fields.CharField', [], {'max_length': '10', 'null': 'True', 'blank': 'True'}),
            'X': ('django.db.models.fields.CharField', [], {'max_length': '10', 'null': 'True', 'blank': 'True'}),
            'Z': ('django.db.models.fields.CharField', [], {'max_length': '10', 'null': 'True', 'blank': 'True'}),
            'age': ('django.db.models.fields.CharField', [], {'max_length': '20', 'null': 'True', 'blank': 'True'}),
            'author': ('django.db.models.fields.CharField', [], {'max_length': '100', 'null': 'True', 'blank': 'True'}),
            'bias_correction_cf': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'biome_FAO': ('django.db.models.fields.CharField', [], {'max_length': '50', 'null': 'True', 'blank': 'True'}),
            'biome_HOLDRIDGE': ('django.db.models.fields.CharField', [], {'max_length': '50', 'null': 'True', 'blank': 'True'}),
            'biome_UDVARDY': ('django.db.models.fields.CharField', [], {'max_length': '50', 'null': 'True', 'blank': 'True'}),
            'biome_WWF': ('django.db.models.fields.CharField', [], {'max_length': '50', 'null': 'True', 'blank': 'True'}),
            'contributor': ('django.db.models.fields.CharField', [], {'max_length': '100', 'null': 'True', 'blank': 'True'}),
            'corrected_for_bias': ('django.db.models.fields.NullBooleanField', [], {'null': 'True', 'blank': 'True'}),
            'country': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['data.Country']", 'null': 'True', 'blank': 'True'}),
            'division_BAILEY': ('django.db.models.fields.CharField', [], {'max_length': '50', 'null': 'True', 'blank': 'True'}),
            'ecosystem': ('django.db.models.fields.CharField', [], {'max_length': '50', 'null': 'True', 'blank': 'True'}),
            'equation_y': ('django.db.models.fields.CharField', [], {'max_length': '100', 'null': 'True', 'blank': 'True'}),
            'genus': ('django.db.models.fields.CharField', [], {'max_length': '25', 'null': 'True', 'blank': 'True'}),
            'group_location': ('django.db.models.fields.NullBooleanField', [], {'null': 'True', 'blank': 'True'}),
            'group_species': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'id_group': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'id_location': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'id_ref': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'id_species': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'label': ('django.db.models.fields.CharField', [], {'max_length': '10', 'null': 'True', 'blank': 'True'}),
            'latitude': ('django.db.models.fields.DecimalField', [], {'null': 'True', 'max_digits': '8', 'decimal_places': '6', 'blank': 'True'}),
            'location': ('django.db.models.fields.CharField', [], {'max_length': '50', 'null': 'True', 'blank': 'True'}),
            'longitude': ('django.db.models.fields.DecimalField', [], {'null': 'True', 'max_digits': '8', 'decimal_places': '6', 'blank': 'True'}),
            'max_H': ('django.db.models.fields.DecimalField', [], {'null': 'True', 'max_digits': '10', 'decimal_places': '8', 'blank': 'True'}),
            'max_X': ('django.db.models.fields.DecimalField', [], {'null': 'True', 'max_digits': '10', 'decimal_places': '8', 'blank': 'True'}),
            'min_H': ('django.db.models.fields.DecimalField', [], {'null': 'True', 'max_digits': '10', 'decimal_places': '8', 'blank': 'True'}),
            'min_X': ('django.db.models.fields.DecimalField', [], {'null': 'True', 'max_digits': '10', 'decimal_places': '8', 'blank': 'True'}),
            'n': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'name_operator': ('django.db.models.fields.CharField', [], {'max_length': '100', 'null': 'True', 'blank': 'True'}),
            'output': ('django.db.models.fields.CharField', [], {'max_length': '20', 'null': 'True', 'blank': 'True'}),
            'output_TR': ('django.db.models.fields.CharField', [], {'max_length': '20', 'null': 'True', 'blank': 'True'}),
            'population': ('django.db.models.fields.CharField', [], {'max_length': '50', 'null': 'True', 'blank': 'True'}),
            'potential_evapotranspiration': ('django.db.models.fields.DecimalField', [], {'null': 'True', 'max_digits': '10', 'decimal_places': '8', 'blank': 'True'}),
            'precipitation': ('django.db.models.fields.DecimalField', [], {'null': 'True', 'max_digits': '10', 'decimal_places': '8', 'blank': 'True'}),
            'r2': ('django.db.models.fields.DecimalField', [], {'null': 'True', 'max_digits': '6', 'decimal_places': '5', 'blank': 'True'}),
            'r_adjusted': ('django.db.models.fields.DecimalField', [], {'null': 'True', 'max_digits': '6', 'decimal_places': '5', 'blank': 'True'}),
            'ratio_equation': ('django.db.models.fields.NullBooleanField', [], {'null': 'True', 'blank': 'True'}),
            'reference': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'rms': ('django.db.models.fields.DecimalField', [], {'null': 'True', 'max_digits': '10', 'decimal_places': '9', 'blank': 'True'}),
            'rmse': ('django.db.models.fields.DecimalField', [], {'null': 'True', 'max_digits': '10', 'decimal_places': '9', 'blank': 'True'}),
            'see': ('django.db.models.fields.DecimalField', [], {'null': 'True', 'max_digits': '10', 'decimal_places': '9', 'blank': 'True'}),
            'segmented_equation': ('django.db.models.fields.NullBooleanField', [], {'null': 'True', 'blank': 'True'}),
            'species': ('django.db.models.fields.CharField', [], {'max_length': '25', 'null': 'True', 'blank': 'True'}),
            'stump_height': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'sunshine_fraction': ('django.db.models.fields.DecimalField', [], {'null': 'True', 'max_digits': '10', 'decimal_places': '8', 'blank': 'True'}),
            'temp_MAX': ('django.db.models.fields.DecimalField', [], {'null': 'True', 'max_digits': '10', 'decimal_places': '8', 'blank': 'True'}),
            'temp_MIN': ('django.db.models.fields.DecimalField', [], {'null': 'True', 'max_digits': '10', 'decimal_places': '8', 'blank': 'True'}),
            'temperature': ('django.db.models.fields.DecimalField', [], {'null': 'True', 'max_digits': '10', 'decimal_places': '8', 'blank': 'True'}),
            'top_dob': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'unit_U': ('django.db.models.fields.CharField', [], {'max_length': '10', 'null': 'True', 'blank': 'True'}),
            'unit_V': ('django.db.models.fields.CharField', [], {'max_length': '10', 'blank': 'True'}),
            'unit_W': ('django.db.models.fields.CharField', [], {'max_length': '10', 'null': 'True', 'blank': 'True'}),
            'unit_X': ('django.db.models.fields.CharField', [], {'max_length': '10', 'null': 'True', 'blank': 'True'}),
            'unit_Y': ('django.db.models.fields.CharField', [], {'max_length': '20', 'null': 'True', 'blank': 'True'}),
            'unit_Z': ('django.db.models.fields.CharField', [], {'max_length': '10', 'null': 'True', 'blank': 'True'}),
            'veg_component': ('django.db.models.fields.CharField', [], {'max_length': '20', 'null': 'True', 'blank': 'True'}),
            'water_vapor_pressure': ('django.db.models.fields.DecimalField', [], {'null': 'True', 'max_digits': '10', 'decimal_places': '8', 'blank': 'True'}),
            'wind': ('django.db.models.fields.DecimalField', [], {'null': 'True', 'max_digits': '10', 'decimal_places': '8', 'blank': 'True'}),
            'year': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'})
        }
    }

    complete_apps = ['data']