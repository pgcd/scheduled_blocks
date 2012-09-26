import datetime
from django.conf import settings
from django.db import models
from django.db.models import Q

SCHEDULED_BLOCKS_TEMPLATE_EXTENSION = getattr(settings,'SCHEDULED_BLOCKS_TEMPLATE_EXTENSION', '.html')
class ScheduledBlockManager(models.Manager):
    def currently_visible(self, when=None):
        when = when or datetime.datetime.today()
        return super(ScheduledBlockManager, self).get_query_set()\
            .filter(Q(display_from__lte=when)|Q(display_from__isnull=True))\
            .filter(Q(display_to__gte=when)|Q(display_to__isnull=True))

class ScheduledBlock(models.Model):
    name = models.CharField(max_length=120, db_index=True)
    created =models.DateTimeField(auto_now_add=True)
    display_from = models.DateTimeField(blank=True, null=True)
    display_to = models.DateTimeField(blank=True, null=True)
    content = models.TextField(blank=True, help_text="If present, the block's output will be this, rendered as a template.")
    template_name = models.CharField(max_length=120, blank=True, help_text="The name of the template to be "
                                                                           "rendered (the template has to exist in "
                                                                           "the 'scheduled_blocks' folder). No extension.")
    event_name = models.CharField(max_length=120, blank=True, help_text="If present, the loader will also attempt to "
                                                                        "load the %(name)s_%(event_name)s template.")
    extra_context = models.TextField(blank=True, help_text="You can use this to pass an extra dict to the template")
    objects = ScheduledBlockManager()

    def __unicode__(self):
        return self.name

    class Meta:
        ordering = ['display_from','display_to']
        get_latest_by = 'display_from'