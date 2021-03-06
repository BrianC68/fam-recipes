# Generated by Django 3.1.1 on 2020-09-25 18:51

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('recipes', '0018_auto_20200925_1045'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('meal_menu', '0001_initial'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='shoppinglist',
            options={'verbose_name_plural': 'Shopping Lists'},
        ),
        migrations.AddField(
            model_name='shoppinglist',
            name='recipe',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='recipes.recipe'),
        ),
        migrations.AlterField(
            model_name='shoppinglist',
            name='list_item',
            field=models.CharField(max_length=255),
        ),
        migrations.AlterUniqueTogether(
            name='mealmenurecipe',
            unique_together={('recipe', 'user')},
        ),
    ]
