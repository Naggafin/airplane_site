# Generated by Django 3.2.9 on 2022-01-25 20:17

from django.db import migrations


class Migration(migrations.Migration):
	dependencies = [
		("catalogue", "0024_remove_duplicate_attributes"),
	]

	operations = [
		migrations.AlterUniqueTogether(
			name="productattribute",
			unique_together={("code", "product_class")},
		),
	]
