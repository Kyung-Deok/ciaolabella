# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey and OneToOneField has `on_delete` set to the desired behavior
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
from django.db import models


class ECOPOINT(models.Model):
    row_id = models.BigAutoField(primary_key=True)
    user_nb = models.BigIntegerField()
    save_tm = models.DateTimeField()
    point_amt = models.BigIntegerField()

    class Meta:
        managed = False
        db_table = 'ECOPOINT'


class MEMBER(models.Model):
    id = models.BigAutoField(primary_key=True)
    user_id = models.CharField(max_length=100)
    user_pw = models.CharField(max_length=100)
    user_nm = models.CharField(max_length=50)
    birth_nb = models.CharField(max_length=20)
    gender_kb = models.CharField(max_length=20)
    email_txt = models.CharField(max_length=150)
    phone_nb = models.CharField(max_length=150)
    region_kb = models.CharField(max_length=100)
    reg_date = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'MEMBER'
