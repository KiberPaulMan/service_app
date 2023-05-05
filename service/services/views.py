from django.db.models import Prefetch, F
from django.http import HttpResponse
from django.shortcuts import render
from rest_framework.viewsets import ReadOnlyModelViewSet

from clients.models import Client
from services.models import Subscription, Plan, Service
from services.serializers import SubscriptionSerializer


class SubscriptionView(ReadOnlyModelViewSet):
    queryset = Subscription.objects.all().prefetch_related(
                Prefetch('client',
                         queryset=Client.objects.all().select_related('user').only('company_name',
                                                                                   'user__email')),
                Prefetch('plan',
                         queryset=Plan.objects.all().only('plan_type', 'discount_percent')),
    ).annotate(price=F('service__full_price') * (1 - F('plan__discount_percent') / 100.00))
    serializer_class = SubscriptionSerializer

    def list(self, request, *args, **kwargs):
        response = super().list(request, *args, **kwargs)
        response_data = {'result': response.data}
        response.data = response_data
        return response
