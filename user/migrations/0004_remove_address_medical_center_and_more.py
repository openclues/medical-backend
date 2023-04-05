# Generated by Django 4.2 on 2023-04-04 16:12

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0003_remove_medicalcenter_address_address_medical_center_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='address',
            name='medical_center',
        ),
        migrations.RemoveField(
            model_name='specialty',
            name='medical_centers',
        ),
        migrations.AddField(
            model_name='medicalcenter',
            name='specialities',
            field=models.ManyToManyField(related_name='specialities_center', to='user.specialty'),
        ),
    ]
