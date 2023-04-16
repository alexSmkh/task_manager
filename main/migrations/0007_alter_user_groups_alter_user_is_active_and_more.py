# Generated by Django 4.1.6 on 2023-04-11 21:25

import django.contrib.auth.validators
from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ('auth', '0012_alter_user_first_name_max_length'),
        ('main', '0006_task_assigned_task_author'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='groups',
            field=models.ManyToManyField(
                blank=True,
                help_text='The groups this user belongs to. A user will get all permissions\
                 granted to each of their groups.',
                related_name='user_set',
                related_query_name='user',
                to='auth.group',
                verbose_name='groups',
            ),
        ),
        migrations.AlterField(
            model_name='user',
            name='is_active',
            field=models.BooleanField(
                default=True,
                help_text='Designates whether this user should be treated as active. Unselect this\
                 instead of deleting accounts.',
                verbose_name='active',
            ),
        ),
        migrations.AlterField(
            model_name='user',
            name='is_superuser',
            field=models.BooleanField(
                default=False,
                help_text='Designates that this user has all permissions without explicitly\
                 assigning them.',
                verbose_name='superuser status',
            ),
        ),
        migrations.AlterField(
            model_name='user',
            name='username',
            field=models.CharField(
                error_messages={'unique': 'A user with that username already exists.'},
                help_text='Required. 150 characters or fewer. Letters, digits and @/./+/-/_ only.',
                max_length=150,
                unique=True,
                validators=[django.contrib.auth.validators.UnicodeUsernameValidator()],
                verbose_name='username',
            ),
        ),
    ]
