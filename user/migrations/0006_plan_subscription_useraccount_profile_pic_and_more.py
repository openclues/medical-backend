# Generated by Django 4.2 on 2023-04-04 21:54

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0005_address_url'),
    ]

    operations = [
        migrations.CreateModel(
            name='Plan',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255)),
                ('description', models.TextField()),
                ('price', models.DecimalField(decimal_places=2, max_digits=7)),
                ('billing_interval', models.CharField(max_length=255)),
                ('billing_frequency', models.IntegerField()),
            ],
        ),
        migrations.CreateModel(
            name='Subscription',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('start_date', models.DateTimeField(auto_now_add=True)),
                ('end_date', models.DateTimeField(blank=True, null=True)),
                ('payment_id', models.CharField(blank=True, max_length=255, null=True)),
                ('is_active', models.BooleanField(default=True)),
                ('trial_period', models.IntegerField(default=0)),
                ('plan', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='user.plan')),
            ],
        ),
        migrations.AddField(
            model_name='useraccount',
            name='profile_pic',
            field=models.FileField(blank=True, null=True, upload_to='pics'),
        ),
        migrations.CreateModel(
            name='Transaction',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('amount', models.DecimalField(decimal_places=2, max_digits=7)),
                ('date', models.DateTimeField(auto_now_add=True)),
                ('success', models.BooleanField(default=False)),
                ('payment_id', models.CharField(blank=True, max_length=255, null=True)),
                ('subscription', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='transactions', to='user.subscription')),
            ],
        ),
        migrations.AddField(
            model_name='subscription',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='subscriptions', to=settings.AUTH_USER_MODEL),
        ),
        migrations.CreateModel(
            name='Interest',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('specialties', models.ManyToManyField(related_name='interested_users', to='user.specialty')),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='interests', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Doctor',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255)),
                ('image', models.ImageField(blank=True, null=True, upload_to='doctors')),
                ('specialist', models.CharField(max_length=255)),
                ('medical_center', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='doctors', to='user.medicalcenter')),
            ],
        ),
        migrations.CreateModel(
            name='CustomField',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255)),
                ('field_type', models.CharField(choices=[('text', 'Text'), ('image', 'Image')], max_length=10)),
                ('text_value', models.TextField(blank=True, null=True)),
                ('image_value', models.ImageField(blank=True, null=True, upload_to='custom_fields')),
                ('medical_center', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='custom_fields', to='user.medicalcenter')),
            ],
        ),
    ]
