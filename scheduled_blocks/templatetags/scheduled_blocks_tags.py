# coding=utf-8
import ast
import datetime
from django.conf import settings
from django.template import Context
from django.template.loader import render_to_string
from scheduled_blocks.models import ScheduledBlock, SCHEDULED_BLOCKS_TEMPLATE_EXTENSION

__author__ = 'pgcd'

from django import template

register = template.Library()

@register.simple_tag(takes_context=True)
def schedule_block(context, block_name):
    """
    :param context:
    :type Context
    :param block_name:
    :return: string
    :raise: template.TemplateSyntaxError

    This works pretty much like an inclusion tag - that is, it renders a template based on the current datetime.
    First, it looks for a ScheduledBlock with the given name that is scheduled to be displayed now. If the lookup doesn't
    yield a result, the fallback is the template with the same name as the block (plus the extension).
    If there is a ScheduledBlock, the template loader looks for the first template that matches:
    * (saved template_name)
    * (block name)_(event_name)
    * (block name)_(display_from datetime)_(display_to datetime)
    * (block name)_(display_from date)_(display_to date)
    * (block name)_(display_from datetime)
    * (block name)

    Datetime, here, means YYYYMMDDHHMM, while date means YYYYMMDD. template_name and event_name can be saved in the
    ScheduledBlock.
    """
    private_context = Context(context)
    testdate = None
    request = private_context.get('request')
    fallback_template = "scheduled_blocks/%s%s" % (block_name,SCHEDULED_BLOCKS_TEMPLATE_EXTENSION)
    if request and request.user.is_staff:
        # Otherwise we're not using a RequestContext and it's pointless to proceed
        # Also, non-staff shouldn't be able to see unpublished stuff, right?
        testdate = request.GET.get('testdate')

    try:
        block = ScheduledBlock.objects.currently_visible(testdate).filter(name=block_name).latest()
    except ScheduledBlock.DoesNotExist:
        try:
            #Since there's no scheduled block we try to see if there's a template with the right name to use as fallback
            return render_to_string(fallback_template, context_instance=private_context)
        except:
            pass
        raise template.TemplateSyntaxError(
            "No scheduled block with the name [%s] is scheduled to appear now and there's no fallback template." % block_name)
    if block.content:
        #If there's content, we'll just render this
        return template.loader.get_template_from_string(block.content, name=block_name).render(private_context)

    if block.extra_context:
        private_context.update(ast.literal_eval(block.extra_context))
    #No content in the block, so we select the template using this order:
    # - (saved template name)
    # - (block name)_(event name)
    # - (block name)_(display_from datetime)_(display_to datetime)
    # - (block name)_(display_from date)_(display_to date)
    # - (block name)_(display_from datetime)
    # - (block name)
    possible_templates = [block.template_name,]
    if block.event_name:
        possible_templates += ["%s_%s" % (block.name, block.event_name),]
    if block.display_from is not None:
        if block.display_to is not None:
            possible_templates += ["%s_%s_%s" % (block.name, block.display_from.strftime("%Y%m%d%H%M"),
                                        block.display_to.strftime("%Y%m%d%H%M")),
                          "%s_%s_%s" % (
                          block.name, block.display_from.strftime("%Y%m%d"), block.display_to.strftime("%Y%m%d")),]
        possible_templates += ["%s_%s" % (block.name, block.display_from.strftime("%Y%m%d%H%M")),]
    possible_templates = ['scheduled_blocks/%s%s' % (x, SCHEDULED_BLOCKS_TEMPLATE_EXTENSION) for x in
                          possible_templates if x != ''] #cleanup and name formatting
    return render_to_string(possible_templates+[fallback_template], context_instance=private_context)



