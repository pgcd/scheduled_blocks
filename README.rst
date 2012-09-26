scheduled_blocks
========================

Welcome to the documentation for django-scheduled_blocks v0.0.1!

The purpose of this app is to schedule content in a Django template.

BASIC USAGE:
____________
* Add ``'scheduled_blocks'`` to your ``INSTALLED_APPS``.
* Run 'python manage.py migrate scheduled_blocks' to create the required table.
* Add a block in the admin panel - you can begin by simply entering the name of the block and something in the ``content`` field.
* In the template where you need to schedule some content, add ``{% load scheduled_blocks_tags %}`` at the beginning, then
  add ``{% schedule_block <blockname> %}`` where you want the content to appear.
* That's it - the content will appear where required.

MORE USEFUL USAGE:
__________________
* Define a second block (with the same name - you can have any number of blocks with the same name) with different content
  and set its ``display_from`` field to be some time in the future. You can test the result by appending ``?testdate=YYYY-MM-DD``
  (substitute the actual values here) to the URL of the relevant page.
* You can (you should) use actual templates for your content, either by specifying the template name (no extension) in
  your ScheduledBlock  object or by naming the template so that the loader will find it. The name resolution rules are:
  1. scheduled_blocks/(saved template_name)
  2. scheduled_blocks/(block name)_(event_name)
  3. scheduled_blocks/(block name)_(display_from datetime)_(display_to datetime)
  4. scheduled_blocks/(block name)_(display_from date)_(display_to date)
  5. scheduled_blocks/(block name)_(display_from datetime)
  6. scheduled_blocks/(block name)
  Datetime, here, means YYYYMMDDHHMM, while date means YYYYMMDD.
* You can pass extra context to your scheduled block, by specifying it in the ScheduledBlock object as a dict.