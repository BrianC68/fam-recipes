# Generated by Django 3.1.1 on 2020-09-30 15:15

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('meal_menu', '0005_auto_20200930_1012'),
    ]

    operations = [
        migrations.AlterField(
            model_name='shoppinglist',
            name='department',
            field=models.ForeignKey(blank=True, help_text='Used to group shopping list items. (Not Required)', null=True, on_delete=django.db.models.deletion.SET_NULL, to='meal_menu.storedepartment'),
        ),
    ]
