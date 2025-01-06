# Generated by Django 5.1.3 on 2025-01-05 22:54

import auto_prefetch
import django.db.models.deletion
import django.db.models.manager
from django.conf import settings
from django.db import migrations


class Migration(migrations.Migration):
	dependencies = [
		("catalogue", "0031_alter_attributeoption_options_and_more"),
		("wishlists", "0004_auto_20220328_0939"),
		migrations.swappable_dependency(settings.AUTH_USER_MODEL),
	]

	operations = [
		migrations.AlterModelOptions(
			name="line",
			options={
				"base_manager_name": "prefetch_manager",
				"ordering": ["pk"],
				"verbose_name": "Wish list line",
			},
		),
		migrations.AlterModelOptions(
			name="wishlist",
			options={
				"base_manager_name": "prefetch_manager",
				"ordering": ("owner", "date_created"),
				"verbose_name": "Wish List",
			},
		),
		migrations.AlterModelManagers(
			name="line",
			managers=[
				("objects", django.db.models.manager.Manager()),
				("prefetch_manager", django.db.models.manager.Manager()),
			],
		),
		migrations.AlterModelManagers(
			name="wishlist",
			managers=[
				("objects", django.db.models.manager.Manager()),
				("prefetch_manager", django.db.models.manager.Manager()),
			],
		),
		migrations.AlterField(
			model_name="line",
			name="product",
			field=auto_prefetch.ForeignKey(
				blank=True,
				null=True,
				on_delete=django.db.models.deletion.SET_NULL,
				related_name="wishlists_lines",
				to="catalogue.product",
				verbose_name="Product",
			),
		),
		migrations.AlterField(
			model_name="line",
			name="wishlist",
			field=auto_prefetch.ForeignKey(
				on_delete=django.db.models.deletion.CASCADE,
				related_name="lines",
				to="wishlists.wishlist",
				verbose_name="Wish List",
			),
		),
		migrations.AlterField(
			model_name="wishlist",
			name="owner",
			field=auto_prefetch.ForeignKey(
				on_delete=django.db.models.deletion.CASCADE,
				related_name="wishlists",
				to=settings.AUTH_USER_MODEL,
				verbose_name="Owner",
			),
		),
	]
