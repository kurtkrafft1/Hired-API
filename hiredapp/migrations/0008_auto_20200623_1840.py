# Generated by Django 3.0.7 on 2020-06-23 18:40

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('hiredapp', '0007_auto_20200623_1422'),
    ]

    operations = [
        migrations.AlterField(
            model_name='job',
            name='employee_profile',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='hiredapp.EmployeeProfile'),
        ),
    ]
