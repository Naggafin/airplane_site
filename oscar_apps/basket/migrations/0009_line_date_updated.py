# Generated by Django 3.0.3 on 2020-03-03 09:36

from django.db import migrations, models


class Migration(migrations.Migration):
	dependencies = [
		("basket", "0008_auto_20181115_1953"),
	]

	operations = [
		migrations.AddField(
			model_name="line",
			name="date_updated",
			field=models.DateTimeField(
				auto_now=True, db_index=True, verbose_name="Date Updated"
			),
		),
	]
