# encoding: utf-8
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models

class Migration(SchemaMigration):

    def forwards(self, orm):
        
        # Adding model 'ScheduledBlock'
        db.create_table('scheduled_blocks_scheduledblock', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=120, db_index=True)),
            ('created', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
            ('display_from', self.gf('django.db.models.fields.DateTimeField')(null=True, blank=True)),
            ('display_to', self.gf('django.db.models.fields.DateTimeField')(null=True, blank=True)),
            ('content', self.gf('django.db.models.fields.TextField')(blank=True)),
            ('template_name', self.gf('django.db.models.fields.CharField')(max_length=120, blank=True)),
            ('event_name', self.gf('django.db.models.fields.CharField')(max_length=120, blank=True)),
            ('extra_context', self.gf('django.db.models.fields.TextField')(blank=True)),
        ))
        db.send_create_signal('scheduled_blocks', ['ScheduledBlock'])


    def backwards(self, orm):
        
        # Deleting model 'ScheduledBlock'
        db.delete_table('scheduled_blocks_scheduledblock')


    models = {
        'scheduled_blocks.scheduledblock': {
            'Meta': {'ordering': "['display_from', 'display_to']", 'object_name': 'ScheduledBlock'},
            'content': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'created': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'display_from': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'}),
            'display_to': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'}),
            'event_name': ('django.db.models.fields.CharField', [], {'max_length': '120', 'blank': 'True'}),
            'extra_context': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '120', 'db_index': 'True'}),
            'template_name': ('django.db.models.fields.CharField', [], {'max_length': '120', 'blank': 'True'})
        }
    }

    complete_apps = ['scheduled_blocks']
