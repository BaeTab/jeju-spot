# Generated by Django 5.1.3 on 2024-12-15 07:28

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('spots', '0002_remove_spotimage_uploaded_at_spot_likes_count_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='spot',
            name='category',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='spots.spotcategory'),
        ),
        migrations.AlterField(
            model_name='spotcategory',
            name='name',
            field=models.CharField(max_length=50, unique=True),
        ),
    ]
