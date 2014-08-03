# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'Person'
        db.create_table('core_person', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('user', self.gf('django.db.models.fields.related.ForeignKey')(default=None, to=orm['auth.User'], null=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('description', self.gf('django.db.models.fields.TextField')(default='')),
            ('phone', self.gf('django.db.models.fields.CharField')(default='', max_length=32)),
            ('email', self.gf('django.db.models.fields.CharField')(default='', max_length=255)),
            ('verified', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('lat', self.gf('django.db.models.fields.DecimalField')(default=0, max_digits=14, decimal_places=10)),
            ('lng', self.gf('django.db.models.fields.DecimalField')(default=0, max_digits=14, decimal_places=10)),
            ('address', self.gf('django.db.models.fields.CharField')(default='', max_length=512)),
            ('ok_contact', self.gf('django.db.models.fields.IntegerField')(default=1)),
            ('beer', self.gf('django.db.models.fields.CharField')(default='', max_length=255)),
        ))
        db.send_create_signal('core', ['Person'])

        # Adding M2M table for field services on 'Person'
        db.create_table('core_person_services', (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('person', models.ForeignKey(orm['core.person'], null=False)),
            ('service', models.ForeignKey(orm['core.service'], null=False))
        ))
        db.create_unique('core_person_services', ['person_id', 'service_id'])

        # Adding model 'Service'
        db.create_table('core_service', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(default='', max_length=512)),
        ))
        db.send_create_signal('core', ['Service'])

        # Adding model 'Activation'
        db.create_table('core_activation', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('key', self.gf('django.db.models.fields.CharField')(max_length=512)),
            ('person', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['core.Person'])),
        ))
        db.send_create_signal('core', ['Activation'])

        # Adding model 'Karma'
        db.create_table('core_karma', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('description', self.gf('django.db.models.fields.TextField')(default='')),
            ('person', self.gf('django.db.models.fields.related.ForeignKey')(related_name='karma_person', to=orm['core.Person'])),
            ('creator', self.gf('django.db.models.fields.related.ForeignKey')(related_name='karma_creator', to=orm['core.Person'])),
        ))
        db.send_create_signal('core', ['Karma'])

        # Adding model 'Flag'
        db.create_table('core_flag', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('description', self.gf('django.db.models.fields.TextField')(default='')),
            ('person', self.gf('django.db.models.fields.related.ForeignKey')(related_name='flag_person', to=orm['core.Person'])),
            ('creator', self.gf('django.db.models.fields.related.ForeignKey')(related_name='flag_creator', to=orm['core.Person'])),
        ))
        db.send_create_signal('core', ['Flag'])

    def backwards(self, orm):
        # Deleting model 'Person'
        db.delete_table('core_person')

        # Removing M2M table for field services on 'Person'
        db.delete_table('core_person_services')

        # Deleting model 'Service'
        db.delete_table('core_service')

        # Deleting model 'Activation'
        db.delete_table('core_activation')

        # Deleting model 'Karma'
        db.delete_table('core_karma')

        # Deleting model 'Flag'
        db.delete_table('core_flag')

    models = {
        'auth.group': {
            'Meta': {'object_name': 'Group'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '80'}),
            'permissions': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['auth.Permission']", 'symmetrical': 'False', 'blank': 'True'})
        },
        'auth.permission': {
            'Meta': {'ordering': "('content_type__app_label', 'content_type__model', 'codename')", 'unique_together': "(('content_type', 'codename'),)", 'object_name': 'Permission'},
            'codename': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'content_type': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['contenttypes.ContentType']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '50'})
        },
        'auth.user': {
            'Meta': {'object_name': 'User'},
            'date_joined': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'email': ('django.db.models.fields.EmailField', [], {'max_length': '75', 'blank': 'True'}),
            'first_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'groups': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['auth.Group']", 'symmetrical': 'False', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_active': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'is_staff': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'is_superuser': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'last_login': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'last_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'password': ('django.db.models.fields.CharField', [], {'max_length': '128'}),
            'user_permissions': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['auth.Permission']", 'symmetrical': 'False', 'blank': 'True'}),
            'username': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '30'})
        },
        'contenttypes.contenttype': {
            'Meta': {'ordering': "('name',)", 'unique_together': "(('app_label', 'model'),)", 'object_name': 'ContentType', 'db_table': "'django_content_type'"},
            'app_label': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'model': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        },
        'core.activation': {
            'Meta': {'object_name': 'Activation'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'key': ('django.db.models.fields.CharField', [], {'max_length': '512'}),
            'person': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['core.Person']"})
        },
        'core.flag': {
            'Meta': {'object_name': 'Flag'},
            'creator': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'flag_creator'", 'to': "orm['core.Person']"}),
            'description': ('django.db.models.fields.TextField', [], {'default': "''"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'person': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'flag_person'", 'to': "orm['core.Person']"})
        },
        'core.karma': {
            'Meta': {'object_name': 'Karma'},
            'creator': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'karma_creator'", 'to': "orm['core.Person']"}),
            'description': ('django.db.models.fields.TextField', [], {'default': "''"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'person': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'karma_person'", 'to': "orm['core.Person']"})
        },
        'core.person': {
            'Meta': {'object_name': 'Person'},
            'address': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '512'}),
            'beer': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '255'}),
            'description': ('django.db.models.fields.TextField', [], {'default': "''"}),
            'email': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '255'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'lat': ('django.db.models.fields.DecimalField', [], {'default': '0', 'max_digits': '14', 'decimal_places': '10'}),
            'lng': ('django.db.models.fields.DecimalField', [], {'default': '0', 'max_digits': '14', 'decimal_places': '10'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'ok_contact': ('django.db.models.fields.IntegerField', [], {'default': '1'}),
            'phone': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '32'}),
            'services': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['core.Service']", 'symmetrical': 'False'}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'default': 'None', 'to': "orm['auth.User']", 'null': 'True'}),
            'verified': ('django.db.models.fields.BooleanField', [], {'default': 'False'})
        },
        'core.service': {
            'Meta': {'object_name': 'Service'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '512'})
        }
    }

    complete_apps = ['core']