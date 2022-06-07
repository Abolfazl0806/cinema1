# Generated by Django 3.2.9 on 2022-05-08 19:11

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0001_initial'),
        ('ticketing', '0005_alter_cinema_image'),
    ]

    operations = [
        migrations.CreateModel(
            name='Ticket',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('seat_count', models.IntegerField(verbose_name='تعداد صندلی')),
                ('order_time', models.DateTimeField(auto_now_add=True, verbose_name='زمان خرید')),
                ('customer', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='accounts.profile', verbose_name='خریدار')),
                ('showtime', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='ticketing.showtime', verbose_name='سانس')),
            ],
            options={
                'verbose_name': 'بلیت',
                'verbose_name_plural': 'بلیت',
            },
        ),
    ]
