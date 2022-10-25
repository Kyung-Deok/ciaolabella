from django.db import models


class MEMBER(models.Model):

    user_nm = models.CharField(db_column='user_nm', max_length=50, null=False)
    user_id = models.CharField(db_column='user_id', max_length=100, null=False)
    user_pw = models.CharField(db_column='user_pw', max_length=100)
    age_nb = models.IntegerField(db_column='age_nb', null=False)
    gender_kb = models.CharField(db_column='gender_kb', max_length=20, null=False)
    email_txt = models.EmailField(db_column='email_txt', max_length=150)
    phone_nb = models.CharField(db_column='phone_nb', max_length=150)
    region_kb = models.CharField(db_column='region_kb', max_length=100, null=False)
    reg_date = models.DateTimeField(db_column='reg_date', auto_now_add=True)

    class Meta:
        db_table = 'MEMBER'

class ECOPOINT(models.Model):
    row_id = models.BigAutoField(primary_key=True, null=False)
    user_nb = models.ForeignKey('Member', models.DO_NOTHING, db_column='user_nb', null=False)
    save_tm = models.DateTimeField(db_column='save_tm', auto_now_add=True, null=False)
    point_amt = models.BigIntegerField(db_column='point_amt', null=False)

    class Meta:
        db_table = 'ECOPOINT'