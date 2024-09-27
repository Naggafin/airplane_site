# Generated by Django 2.2.10 on 2020-07-24 08:09

from django.db import migrations, models


class Migration(migrations.Migration):
	dependencies = [
		("partner", "0005_auto_20181115_1953"),
	]

	operations = [
		migrations.RemoveField(
			model_name="stockrecord",
			name="cost_price",
		),
		migrations.RemoveField(
			model_name="stockrecord",
			name="price_retail",
		),
		migrations.AlterField(
			model_name="stockrecord",
			name="price_excl_tax",
			field=models.DecimalField(
				blank=True,
				decimal_places=2,
				max_digits=12,
				null=True,
				verbose_name="Price",
			),
		),
		migrations.RenameField(
			model_name="stockrecord",
			old_name="price_excl_tax",
			new_name="price",
		),
	]
