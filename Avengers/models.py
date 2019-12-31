from django.db import models
# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey has `on_delete` set to the desired behavior.
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.


class Myinfo(models.Model):
    email = models.CharField(max_length=50)
    pwd = models.CharField(max_length=50)

    class Meta:
        managed = False
        db_table = 'myinfo'


class Schedule(models.Model):
    no = models.AutoField(primary_key=True)
    memid = models.ForeignKey(Myinfo, models.DO_NOTHING, db_column='memid')
    title = models.CharField(max_length=50)
    content = models.CharField(max_length=500)
    date = models.DateTimeField(blank=True, null=True)
    star = models.CharField(max_length=10)

    class Meta:
        managed = False
        db_table = 'schedule'
