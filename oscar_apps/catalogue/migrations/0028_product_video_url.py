# Generated by Django 4.2.13 on 2024-07-13 16:23

from django.db import migrations, models


class Migration(migrations.Migration):
	dependencies = [
		("catalogue", "0027_attributeoption_code_attributeoptiongroup_code_and_more"),
	]

	operations = [
		migrations.AddField(
			model_name="product",
			name="video_url",
			field=models.URLField(null=True, verbose_name="video URL"),
		),
	]
