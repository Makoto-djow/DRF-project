from django_filters import rest_framework
from rest_framework import generics, filters


from users import models, serializers


class PaymentListAPIView(generics.ListAPIView):
    queryset = models.Payment.objects.all()
    serializer_class = serializers.PaymentSerializer

    filter_backends = [filters.OrderingFilter, rest_framework.DjangoFilterBackend]
    filterset_fields = ["method", "lesson", "course"]
    ordering_fields = ["payment_date"]
