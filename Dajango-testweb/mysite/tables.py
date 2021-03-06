# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey has `on_delete` set to the desired behavior.
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
from __future__ import unicode_literals

from django.db import models


class DailySurveillance(models.Model):
    flarm_id = models.CharField(db_column='Flarm_ID', primary_key=True, max_length=12)  # Field name made lowercase.
    logged_date = models.DateField(db_column='Logged_Date')  # Field name made lowercase.
    note = models.CharField(db_column='Note', max_length=150, blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'Daily_Surveillance'
        unique_together = (('flarm_id', 'logged_date'),)


class Flew(models.Model):
    flight_no = models.ForeignKey('FlightData', models.DO_NOTHING, db_column='Flight_No', primary_key=True)  # Field name made lowercase.
    pilot = models.ForeignKey('Pilot', models.DO_NOTHING, db_column='Pilot_ID')  # Field name made lowercase.
    flight_type = models.CharField(db_column='Flight_Type', max_length=150)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'Flew'
        unique_together = (('flight_no', 'pilot'),)


class FlightData(models.Model):
    flight_no = models.AutoField(db_column='Flight_No', primary_key=True)  # Field name made lowercase.
    takeoff = models.TimeField(db_column='Takeoff', blank=True, null=True)  # Field name made lowercase.
    glider_landing = models.TimeField(db_column='Glider_Landing', blank=True, null=True)  # Field name made lowercase.
    max_height = models.IntegerField(db_column='Max_Height', blank=True, null=True)  # Field name made lowercase.
    logged_date = models.DateField(db_column='Logged_Date', blank=True, null=True)  # Field name made lowercase.
    flight_type = models.CharField(db_column='Flight_Type', max_length=10, blank=True, null=True)  # Field name made lowercase.
    glider = models.ForeignKey('Glider', models.DO_NOTHING, db_column='Glider_id', blank=True, null=True)  # Field name made lowercase.
    towing = models.ForeignKey('TowPlane', models.DO_NOTHING, db_column='Towing_id', blank=True, null=True)  # Field name made lowercase.
    towing_height = models.IntegerField(db_column='Towing_Height', blank=True, null=True)  # Field name made lowercase.
    towing_landing = models.TimeField(db_column='Towing_Landing', blank=True, null=True)  # Field name made lowercase.
    flight_status = models.CharField(db_column='Flight_Status', max_length=20, blank=True, null=True)  # Field name made lowercase.
    notes = models.CharField(db_column='Notes', max_length=150, blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'Flight_Data'


class Glider(models.Model):
    glider_id = models.CharField(db_column='Glider_ID', max_length=12)  # Field name made lowercase.
    flarm_id = models.CharField(db_column='Flarm_ID', primary_key=True, max_length=12)  # Field name made lowercase.
    daily_surveillance_performed = models.CharField(db_column='Daily_Surveillance_Performed', max_length=150, blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'Glider'


class Pilot(models.Model):
    pilot_id = models.IntegerField(db_column='Pilot_ID', primary_key=True)  # Field name made lowercase.
    name = models.CharField(db_column='Name', max_length=150, blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'Pilot'


class Surveilled(models.Model):
    flarm = models.ForeignKey(DailySurveillance, models.DO_NOTHING, db_column='Flarm_ID', primary_key=True)  # Field name made lowercase.
    logged_date = models.ForeignKey(DailySurveillance, models.DO_NOTHING, db_column='Logged_Date')  # Field name made lowercase.
    pilot = models.ForeignKey(Pilot, models.DO_NOTHING, db_column='Pilot_ID', blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'Surveilled'
        unique_together = (('flarm', 'logged_date'),)


class TowPlane(models.Model):
    towing_id = models.CharField(db_column='Towing_ID', max_length=12)  # Field name made lowercase.
    flarm_id = models.CharField(db_column='Flarm_ID', primary_key=True, max_length=12)  # Field name made lowercase.
    daily_surveillance_performed = models.CharField(db_column='Daily_Surveillance_Performed', max_length=150, blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'Tow_Plane'
