# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey has `on_delete` set to the desired behavior.
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
from __future__ import unicode_literals

from django.db import models


class Comment(models.Model):
    id = models.CharField(max_length=40, primary_key=True)
    user = models.ForeignKey('users.user', db_column='user_id', on_delete=models.CASCADE)
    video = models.ForeignKey('videos.video', on_delete=models.CASCADE)
    text = models.CharField(max_length=8192, blank=True, null=True)
    likes = models.IntegerField(blank=True, null=True)
    reply_to = models.CharField(max_length=40, blank=True, null=True)
    replies = models.IntegerField(blank=True, null=True)
    published_time_display = models.CharField(max_length=256, blank=True, null=True)
    scrape_date = models.DateTimeField(blank=True, null=True)
    published_time_calculated = models.DateTimeField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'comment'

    def __unicode__(self):
        return str(self.id)

    def __str__(self):
        string = "{0}: {1}".format(self.user.name, self.text[0:50])
        if len(self.text) > 50:
            string += "..."
        return string


class DjangoMigrations(models.Model):
    app = models.CharField(max_length=255)
    name = models.CharField(max_length=255)
    applied = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'django_migrations'
