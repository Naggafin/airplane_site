import logging
from http import HTTPStatus

from crypto.exceptions import InsufficientBalance
from crypto.models import Coin, CryptoTransaction
from crypto.types import get_crypto_type
from debug_toolbar.middleware import show_toolbar
from django.conf import settings
from django.contrib import messages
from django.contrib.auth.middleware import get_user
from django.http import HttpResponse
from django.shortcuts import redirect
from django.utils.deprecation import MiddlewareMixin
from django.utils.translation import gettext_lazy as _
from django_htmx.http import trigger_client_event
from rest_framework import status
from rest_framework.response import Response


def show_toolbar_superuser(request):
	user = get_user(request)
	return show_toolbar(request) or user.is_superuser
