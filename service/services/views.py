from django.db.models import Prefetch
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
                'service',
    )
    serializer_class = SubscriptionSerializer
