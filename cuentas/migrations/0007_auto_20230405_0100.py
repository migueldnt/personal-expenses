# Generated by Django 3.2.5 on 2023-04-05 07:00

from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('cuentas', '0006_account_comments'),
    ]

    operations = [
        migrations.CreateModel(
            name='AccountMetadata',
            fields=[
                ('id', models.BigAutoField(primary_key=True, serialize=False)),
                ('creditcard_default_cutoffdate', models.SmallIntegerField(default=1)),
                ('creditcard_default_paydeadlinedays', models.SmallIntegerField(default=20)),
            ],
        ),
        migrations.AlterField(
            model_name='account',
            name='type_account',
            field=models.CharField(choices=[('normal', 'Normal'), ('debt', 'Debt'), ('creditcard', 'Credit Card'), ('debitcard', 'Debit Card')], default='normal', max_length=20),
        ),
        migrations.CreateModel(
            name='CreditCardArbitrayDates',
            fields=[
                ('id', models.BigAutoField(primary_key=True, serialize=False)),
                ('cutoffdate', models.DateField()),
                ('paydeadlinedays', models.DateField()),
                ('accountMetadata', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, related_name='creditcard_arbitraydates', to='cuentas.accountmetadata')),
            ],
        ),
        migrations.AddField(
            model_name='accountmetadata',
            name='account',
            field=models.OneToOneField(on_delete=django.db.models.deletion.DO_NOTHING, related_name='metadata', to='cuentas.account'),
        ),
        migrations.CreateModel(
            name='AccountMarkers',
            fields=[
                ('id', models.BigAutoField(primary_key=True, serialize=False)),
                ('date', models.DateTimeField()),
                ('name', models.CharField(default='', max_length=250)),
                ('created', models.DateTimeField(default=django.utils.timezone.now)),
                ('account', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, related_name='markers', to='cuentas.account')),
            ],
        ),
    ]