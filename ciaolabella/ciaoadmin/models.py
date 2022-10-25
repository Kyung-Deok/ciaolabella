from django.db import models


class ADMIN(models.Model):
    row_id = models.AutoField(primary_key=True, db_column = 'row_id' ,null=False)
    admin_id = models.CharField(max_length=100, db_column = 'admin_id',null=False)
    admin_pw = models.CharField(max_length=100, db_column = 'admin_pw',null=False)

    class Meta:
        db_table = 'ADMIN'