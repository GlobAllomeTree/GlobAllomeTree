# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):

        # Changing field 'TreeEquation.division_BAILEY'
        db.alter_column('data_treeequation', 'division_BAILEY', self.gf('django.db.models.fields.CharField')(max_length=200, null=True))

        # Changing field 'TreeEquation.contributor'
        db.alter_column('data_treeequation', 'contributor', self.gf('django.db.models.fields.CharField')(max_length=150, null=True))

        # Changing field 'TreeEquation.author'
        db.alter_column('data_treeequation', 'author', self.gf('django.db.models.fields.CharField')(max_length=200, null=True))

        # Changing field 'TreeEquation.label'
        db.alter_column('data_treeequation', 'label', self.gf('django.db.models.fields.CharField')(max_length=20, null=True))

        # Changing field 'TreeEquation.location'
        db.alter_column('data_treeequation', 'location', self.gf('django.db.models.fields.CharField')(max_length=255, null=True))

        # Changing field 'TreeEquation.biome_WWF'
        db.alter_column('data_treeequation', 'biome_WWF', self.gf('django.db.models.fields.CharField')(max_length=200, null=True))

        # Changing field 'TreeEquation.biome_FAO'
        db.alter_column('data_treeequation', 'biome_FAO', self.gf('django.db.models.fields.CharField')(max_length=200, null=True))

        # Changing field 'TreeEquation.equation_y'
        db.alter_column('data_treeequation', 'equation_y', self.gf('django.db.models.fields.CharField')(max_length=255, null=True))

        # Changing field 'TreeEquation.population'
        db.alter_column('data_treeequation', 'population', self.gf('django.db.models.fields.CharField')(max_length=255, null=True))

        # Changing field 'TreeEquation.name_operator'
        db.alter_column('data_treeequation', 'name_operator', self.gf('django.db.models.fields.CharField')(max_length=150, null=True))

        # Changing field 'TreeEquation.ecosystem'
        db.alter_column('data_treeequation', 'ecosystem', self.gf('django.db.models.fields.CharField')(max_length=255, null=True))

        # Changing field 'TreeEquation.biome_UDVARDY'
        db.alter_column('data_treeequation', 'biome_UDVARDY', self.gf('django.db.models.fields.CharField')(max_length=200, null=True))

        # Changing field 'TreeEquation.biome_HOLDRIDGE'
        db.alter_column('data_treeequation', 'biome_HOLDRIDGE', self.gf('django.db.models.fields.CharField')(max_length=200, null=True))

    def backwards(self, orm):

        # Changing field 'TreeEquation.division_BAILEY'
        db.alter_column('data_treeequation', 'division_BAILEY', self.gf('django.db.models.fields.CharField')(max_length=150, null=True))

        # Changing field 'TreeEquation.contributor'
        db.alter_column('data_treeequation', 'contributor', self.gf('django.db.models.fields.CharField')(max_length=100, null=True))

        # Changing field 'TreeEquation.author'
        db.alter_column('data_treeequation', 'author', self.gf('django.db.models.fields.CharField')(max_length=100, null=True))

        # Changing field 'TreeEquation.label'
        db.alter_column('data_treeequation', 'label', self.gf('django.db.models.fields.CharField')(max_length=10, null=True))

        # Changing field 'TreeEquation.location'
        db.alter_column('data_treeequation', 'location', self.gf('django.db.models.fields.CharField')(max_length=150, null=True))

        # Changing field 'TreeEquation.biome_WWF'
        db.alter_column('data_treeequation', 'biome_WWF', self.gf('django.db.models.fields.CharField')(max_length=150, null=True))

        # Changing field 'TreeEquation.biome_FAO'
        db.alter_column('data_treeequation', 'biome_FAO', self.gf('django.db.models.fields.CharField')(max_length=150, null=True))

        # Changing field 'TreeEquation.equation_y'
        db.alter_column('data_treeequation', 'equation_y', self.gf('django.db.models.fields.CharField')(max_length=100, null=True))

        # Changing field 'TreeEquation.population'
        db.alter_column('data_treeequation', 'population', self.gf('django.db.models.fields.CharField')(max_length=100, null=True))

        # Changing field 'TreeEquation.name_operator'
        db.alter_column('data_treeequation', 'name_operator', self.gf('django.db.models.fields.CharField')(max_length=100, null=True))

        # Changing field 'TreeEquation.ecosystem'
        db.alter_column('data_treeequation', 'ecosystem', self.gf('django.db.models.fields.CharField')(max_length=100, null=True))

        # Changing field 'TreeEquation.biome_UDVARDY'
        db.alter_column('data_treeequation', 'biome_UDVARDY', self.gf('django.db.models.fields.CharField')(max_length=150, null=True))

        # Changing field 'TreeEquation.biome_HOLDRIDGE'
        db.alter_column('data_treeequation', 'biome_HOLDRIDGE', self.gf('django.db.models.fields.CharField')(max_length=150, null=True))

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
            'U': ('django.db.models.fields.CharField', [], {'max_length': '20', 'null': 'True', 'blank': 'True'}),
            'V': ('django.db.models.fields.CharField', [], {'max_length': '20', 'null': 'True', 'blank': 'True'}),
            'W': ('django.db.models.fields.CharField', [], {'max_length': '20', 'null': 'True', 'blank': 'True'}),
            'X': ('django.db.models.fields.CharField', [], {'max_length': '20', 'null': 'True', 'blank': 'True'}),
            'Z': ('django.db.models.fields.CharField', [], {'max_length': '20', 'null': 'True', 'blank': 'True'}),
            'age': ('django.db.models.fields.CharField', [], {'max_length': '50', 'null': 'True', 'blank': 'True'}),
            'author': ('django.db.models.fields.CharField', [], {'max_length': '200', 'null': 'True', 'blank': 'True'}),
            'bias_correction_cf': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'biome_FAO': ('django.db.models.fields.CharField', [], {'max_length': '200', 'null': 'True', 'blank': 'True'}),
            'biome_HOLDRIDGE': ('django.db.models.fields.CharField', [], {'max_length': '200', 'null': 'True', 'blank': 'True'}),
            'biome_UDVARDY': ('django.db.models.fields.CharField', [], {'max_length': '200', 'null': 'True', 'blank': 'True'}),
            'biome_WWF': ('django.db.models.fields.CharField', [], {'max_length': '200', 'null': 'True', 'blank': 'True'}),
            'contributor': ('django.db.models.fields.CharField', [], {'max_length': '150', 'null': 'True', 'blank': 'True'}),
            'corrected_for_bias': ('django.db.models.fields.NullBooleanField', [], {'null': 'True', 'blank': 'True'}),
            'country': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['data.Country']", 'null': 'True', 'blank': 'True'}),
            'division_BAILEY': ('django.db.models.fields.CharField', [], {'max_length': '200', 'null': 'True', 'blank': 'True'}),
            'ecosystem': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'equation_y': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'family': ('django.db.models.fields.CharField', [], {'max_length': '80', 'null': 'True', 'blank': 'True'}),
            'genus': ('django.db.models.fields.CharField', [], {'max_length': '80', 'null': 'True', 'blank': 'True'}),
            'group_location': ('django.db.models.fields.NullBooleanField', [], {'null': 'True', 'blank': 'True'}),
            'group_species': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'id_group': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'id_location': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'id_ref': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'id_species': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'label': ('django.db.models.fields.CharField', [], {'max_length': '20', 'null': 'True', 'blank': 'True'}),
            'latitude': ('django.db.models.fields.DecimalField', [], {'null': 'True', 'max_digits': '8', 'decimal_places': '6', 'blank': 'True'}),
            'location': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'longitude': ('django.db.models.fields.DecimalField', [], {'null': 'True', 'max_digits': '8', 'decimal_places': '6', 'blank': 'True'}),
            'max_H': ('django.db.models.fields.DecimalField', [], {'null': 'True', 'max_digits': '10', 'decimal_places': '8', 'blank': 'True'}),
            'max_X': ('django.db.models.fields.DecimalField', [], {'null': 'True', 'max_digits': '10', 'decimal_places': '8', 'blank': 'True'}),
            'max_Z': ('django.db.models.fields.DecimalField', [], {'null': 'True', 'max_digits': '10', 'decimal_places': '8', 'blank': 'True'}),
            'min_H': ('django.db.models.fields.DecimalField', [], {'null': 'True', 'max_digits': '10', 'decimal_places': '8', 'blank': 'True'}),
            'min_X': ('django.db.models.fields.DecimalField', [], {'null': 'True', 'max_digits': '10', 'decimal_places': '8', 'blank': 'True'}),
            'min_Z': ('django.db.models.fields.DecimalField', [], {'null': 'True', 'max_digits': '10', 'decimal_places': '8', 'blank': 'True'}),
            'n': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'name_operator': ('django.db.models.fields.CharField', [], {'max_length': '150', 'null': 'True', 'blank': 'True'}),
            'output': ('django.db.models.fields.CharField', [], {'max_length': '30', 'null': 'True', 'blank': 'True'}),
            'output_TR': ('django.db.models.fields.CharField', [], {'max_length': '30', 'null': 'True', 'blank': 'True'}),
            'population': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'potential_evapotranspiration': ('django.db.models.fields.DecimalField', [], {'null': 'True', 'max_digits': '10', 'decimal_places': '8', 'blank': 'True'}),
            'precipitation': ('django.db.models.fields.DecimalField', [], {'null': 'True', 'max_digits': '10', 'decimal_places': '8', 'blank': 'True'}),
            'r2': ('django.db.models.fields.DecimalField', [], {'null': 'True', 'max_digits': '6', 'decimal_places': '5', 'blank': 'True'}),
            'r2_adjusted': ('django.db.models.fields.DecimalField', [], {'null': 'True', 'max_digits': '6', 'decimal_places': '5', 'blank': 'True'}),
            'ratio_equation': ('django.db.models.fields.NullBooleanField', [], {'null': 'True', 'blank': 'True'}),
            'reference': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'rms': ('django.db.models.fields.DecimalField', [], {'null': 'True', 'max_digits': '10', 'decimal_places': '9', 'blank': 'True'}),
            'rmse': ('django.db.models.fields.DecimalField', [], {'null': 'True', 'max_digits': '10', 'decimal_places': '9', 'blank': 'True'}),
            'sample_size': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'see': ('django.db.models.fields.DecimalField', [], {'null': 'True', 'max_digits': '10', 'decimal_places': '9', 'blank': 'True'}),
            'segmented_equation': ('django.db.models.fields.NullBooleanField', [], {'null': 'True', 'blank': 'True'}),
            'species': ('django.db.models.fields.CharField', [], {'max_length': '80', 'null': 'True', 'blank': 'True'}),
            'stump_height': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'sunshine_fraction': ('django.db.models.fields.DecimalField', [], {'null': 'True', 'max_digits': '10', 'decimal_places': '8', 'blank': 'True'}),
            'temp_MAX': ('django.db.models.fields.DecimalField', [], {'null': 'True', 'max_digits': '10', 'decimal_places': '8', 'blank': 'True'}),
            'temp_MIN': ('django.db.models.fields.DecimalField', [], {'null': 'True', 'max_digits': '10', 'decimal_places': '8', 'blank': 'True'}),
            'temperature': ('django.db.models.fields.DecimalField', [], {'null': 'True', 'max_digits': '10', 'decimal_places': '8', 'blank': 'True'}),
            'top_dob': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'unit_U': ('django.db.models.fields.CharField', [], {'max_length': '20', 'null': 'True', 'blank': 'True'}),
            'unit_V': ('django.db.models.fields.CharField', [], {'max_length': '20', 'blank': 'True'}),
            'unit_W': ('django.db.models.fields.CharField', [], {'max_length': '20', 'null': 'True', 'blank': 'True'}),
            'unit_X': ('django.db.models.fields.CharField', [], {'max_length': '20', 'null': 'True', 'blank': 'True'}),
            'unit_Y': ('django.db.models.fields.CharField', [], {'max_length': '50', 'null': 'True', 'blank': 'True'}),
            'unit_Z': ('django.db.models.fields.CharField', [], {'max_length': '20', 'null': 'True', 'blank': 'True'}),
            'veg_component': ('django.db.models.fields.CharField', [], {'max_length': '150', 'null': 'True', 'blank': 'True'}),
            'water_vapor_pressure': ('django.db.models.fields.DecimalField', [], {'null': 'True', 'max_digits': '10', 'decimal_places': '8', 'blank': 'True'}),
            'wind': ('django.db.models.fields.DecimalField', [], {'null': 'True', 'max_digits': '10', 'decimal_places': '8', 'blank': 'True'}),
            'year': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'})
        }
    }

    complete_apps = ['data']