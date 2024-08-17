from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.contrib.auth.decorators import login_required
from django.views.generic import CreateView, UpdateView
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django_extensions.auth.mixins import ModelUserFieldPermissionMixin
from .forms import ProductForm
from .models import Product, Review


class ProductCreateView(LoginRequiredMixin, CreateView):
	model = Product
	form_class = ProductForm
	success_url = reverse_lazy('dashboard:home')
	
	def form_valid(self, form):
		product = form.save(commit=False)
		product.listed_by = self.request.user
		product.save()
		return super(ModelFormMixin, self).form_valid(form)


class ProductUpdateView(LoginRequiredMixin, PermissionRequiredMixin, UpdateView):
	model = Product
	permission_required = "update"
	form_class = ProductForm
	success_url = reverse_lazy('dashboard:home')


class ReviewCreateView(LoginRequiredMixin, CreateView):
	model = Product
	form_class = ReviewForm
	
	def get(self, *args, **kwargs):
		self.product = self.get_object()
		return redirect('catalogue:product_detail', product_id=self.product.pk)
	
	def post(self, *args, **kwargs):
		self.product = self.get_object()
		return super().post(*args,**kwargs)
	
	def get_success_url(self):
		return reverse_lazy('catalogue:product_detail', product_id=self.product.pk)
	
	def form_valid(self, form):
		review = form.save(commit=False)
		review.user = self.request.user
		review.product = self.product
		review.save()
		return super(ModelFormMixin, self).form_valid(form)


class ReviewUpdateView(LoginRequiredMixin, PermissionRequiredMixin, UpdateView):
	model = Review
	queryset = model.objects.select_related('product').all()
	permission_required = "update"
	form_class = ReviewForm
	
	def get_success_url(self):
		return reverse_lazy('catalogue:product_detail', product_id=self.object.product_id)
