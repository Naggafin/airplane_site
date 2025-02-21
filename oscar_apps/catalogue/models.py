from functools import partial

import auto_prefetch
from cachetools import LRUCache, cachedmethod
from cachetools.keys import hashkey
from django.contrib.contenttypes.models import ContentType
from django.db import models
from django.utils.translation import gettext_lazy as _
from oscar.apps.catalogue.abstract_models import (
	AbstractAttributeOption,
	AbstractAttributeOptionGroup,
	AbstractCategory,
	AbstractOption,
	AbstractProduct,
	AbstractProductAttribute,
	AbstractProductAttributeValue,
	AbstractProductCategory,
	AbstractProductClass,
	AbstractProductImage,
	AbstractProductRecommendation,
)
from taggit.managers import TaggableManager

from .managers import CategoryQuerySet, ProductQuerySet


class ProductClass(auto_prefetch.Model, AbstractProductClass):
	class Meta(auto_prefetch.Model.Meta, AbstractProductClass.Meta):
		pass


class Category(auto_prefetch.Model, AbstractCategory):
	objects = CategoryQuerySet.as_manager()

	def __init__(self, *args, **kwargs):
		super().__init__(*args, **kwargs)
		self._cache = LRUCache(maxsize=128)

	@cachedmethod(
		lambda self: self._cache, key=partial(hashkey, "get_ancestors_and_self")
	)
	def get_ancestors_and_self(self):
		return super().get_ancestors_and_self()

	@cachedmethod(
		lambda self: self._cache, key=partial(hashkey, "get_descendants_and_self")
	)
	def get_descendants_and_self(self):
		return super().get_descendants_and_self()

	class Meta(auto_prefetch.Model.Meta, AbstractCategory.Meta):
		pass


class ProductCategory(auto_prefetch.Model, AbstractProductCategory):
	product = auto_prefetch.ForeignKey(
		"catalogue.Product", on_delete=models.CASCADE, verbose_name=_("Product")
	)
	category = auto_prefetch.ForeignKey(
		"catalogue.Category", on_delete=models.CASCADE, verbose_name=_("Category")
	)

	class Meta(auto_prefetch.Model.Meta, AbstractProductCategory.Meta):
		pass


class Product(auto_prefetch.Model, AbstractProduct):
	parent = auto_prefetch.ForeignKey(
		"self",
		blank=True,
		null=True,
		on_delete=models.CASCADE,
		related_name="children",
		verbose_name=_("Parent product"),
		help_text=_(
			"Only choose a parent product if you're creating a child "
			"product.  For example if this is a size "
			"4 of a particular t-shirt.  Leave blank if this is a "
			"stand-alone product (i.e. there is only one version of"
			" this product)."
		),
	)
	product_class = auto_prefetch.ForeignKey(
		"catalogue.ProductClass",
		null=True,
		blank=True,
		on_delete=models.PROTECT,
		verbose_name=_("Product type"),
		related_name="products",
		help_text=_("Choose what type of product this is"),
	)

	video_url = models.URLField(_("video URL"), null=True)

	tags = TaggableManager()

	objects = ProductQuerySet.as_manager()

	class Meta(auto_prefetch.Model.Meta, AbstractProduct.Meta):
		pass


class ProductRecommendation(auto_prefetch.Model, AbstractProductRecommendation):
	primary = auto_prefetch.ForeignKey(
		"catalogue.Product",
		on_delete=models.CASCADE,
		related_name="primary_recommendations",
		verbose_name=_("Primary product"),
	)
	recommendation = auto_prefetch.ForeignKey(
		"catalogue.Product",
		on_delete=models.CASCADE,
		verbose_name=_("Recommended product"),
	)

	class Meta(auto_prefetch.Model.Meta, AbstractProductRecommendation.Meta):
		pass


class ProductAttribute(auto_prefetch.Model, AbstractProductAttribute):
	product_class = auto_prefetch.ForeignKey(
		"catalogue.ProductClass",
		blank=True,
		on_delete=models.CASCADE,
		related_name="attributes",
		null=True,
		verbose_name=_("Product type"),
	)
	option_group = auto_prefetch.ForeignKey(
		"catalogue.AttributeOptionGroup",
		blank=True,
		null=True,
		on_delete=models.CASCADE,
		related_name="product_attributes",
		verbose_name=_("Option Group"),
		help_text=_('Select an option group if using type "Option" or "Multi Option"'),
	)

	class Meta(auto_prefetch.Model.Meta, AbstractProductAttribute.Meta):
		pass


class ProductAttributeValue(auto_prefetch.Model, AbstractProductAttributeValue):
	attribute = auto_prefetch.ForeignKey(
		"catalogue.ProductAttribute",
		on_delete=models.CASCADE,
		verbose_name=_("Attribute"),
	)
	product = auto_prefetch.ForeignKey(
		"catalogue.Product",
		on_delete=models.CASCADE,
		related_name="attribute_values",
		verbose_name=_("Product"),
	)
	value_option = auto_prefetch.ForeignKey(
		"catalogue.AttributeOption",
		blank=True,
		null=True,
		on_delete=models.CASCADE,
		verbose_name=_("Value option"),
	)
	entity_content_type = auto_prefetch.ForeignKey(
		ContentType, blank=True, editable=False, on_delete=models.CASCADE, null=True
	)

	class Meta(auto_prefetch.Model.Meta, AbstractProductAttributeValue.Meta):
		pass


class AttributeOptionGroup(auto_prefetch.Model, AbstractAttributeOptionGroup):
	class Meta(auto_prefetch.Model.Meta, AbstractAttributeOptionGroup.Meta):
		pass


class AttributeOption(auto_prefetch.Model, AbstractAttributeOption):
	group = auto_prefetch.ForeignKey(
		"catalogue.AttributeOptionGroup",
		on_delete=models.CASCADE,
		related_name="options",
		verbose_name=_("Group"),
	)

	class Meta(auto_prefetch.Model.Meta, AbstractAttributeOption.Meta):
		pass


class Option(auto_prefetch.Model, AbstractOption):
	option_group = auto_prefetch.ForeignKey(
		"catalogue.AttributeOptionGroup",
		blank=True,
		null=True,
		on_delete=models.CASCADE,
		related_name="product_options",
		verbose_name=_("Option Group"),
		help_text=_('Select an option group if using type "Option" or "Multi Option"'),
	)

	class Meta(auto_prefetch.Model.Meta, AbstractOption.Meta):
		pass


class ProductImage(auto_prefetch.Model, AbstractProductImage):
	product = auto_prefetch.ForeignKey(
		"catalogue.Product",
		on_delete=models.CASCADE,
		related_name="images",
		verbose_name=_("Product"),
	)

	class Meta(auto_prefetch.Model.Meta, AbstractProductImage.Meta):
		pass
