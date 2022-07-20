# Generated by Django 4.0.3 on 2022-07-07 11:42

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('cards', '0001_initial'),
        ('doctors', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='SerialTracker',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('cur_date', models.DateField()),
                ('serial_no', models.IntegerField()),
            ],
        ),
        migrations.CreateModel(
            name='Appointment',
            fields=[
                ('id', models.BigIntegerField(primary_key=True, serialize=False)),
                ('serial_no', models.IntegerField()),
                ('patient_name', models.CharField(max_length=100)),
                ('gender', models.CharField(choices=[('F', 'Female'), ('M', 'Male')], default='M', max_length=2)),
                ('age', models.PositiveIntegerField(blank=True, null=True)),
                ('blood_group', models.CharField(blank=True, max_length=3, null=True)),
                ('location', models.CharField(blank=True, max_length=100, null=True)),
                ('contact_no', models.CharField(blank=True, max_length=15, null=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('doctor_fee', models.PositiveIntegerField()),
                ('lab_fee', models.PositiveIntegerField()),
                ('is_doctor_fee_paid', models.BooleanField(default=False)),
                ('is_lab_fee_paid', models.BooleanField(default=False)),
                ('card', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='patients', to='cards.cardperson')),
                ('doctor', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='appointments', to='doctors.doctor')),
            ],
        ),
    ]
