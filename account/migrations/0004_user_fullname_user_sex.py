# Generated by Django 4.0.4 on 2022-04-23 16:41

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0003_alter_user_birthday'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='fullname',
            field=models.CharField(default='Админ Админов Админыч', max_length=255),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='user',
            name='sex',
            field=models.CharField(choices=[('М', 'Мужской'), ('Ж', 'Женский')], default='Админ Админов Админыч', max_length=9),
            preserve_default=False,
        ),
    ]