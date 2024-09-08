from django_filters import rest_framework
from rest_framework import generics, filters
from django.contrib.auth.hashers import make_password
from rest_framework.permissions import IsAuthenticated


from users import models, serializers
from users.models import Payment
from users.services import convert_rub_to_dollars, create_stripe_session, create_stripe_price


class UserCreateAPIView(generics.CreateAPIView):
    serializer_class = serializers.UserSerializer

    permission_classes = [~IsAuthenticated]

    def perform_create(self, serializer):
        raw_password = serializer.validated_data.get('password')
        password = make_password(raw_password)
        serializer.save(password=password)


class PaymentCreateAPIView(generics.CreateAPIView):
    serializer_class = serializers.PaymentSerializer
    queryset = Payment.objects.all()

    def perform_create(self, serializer):
        payment = serializer.save(user=self.request.user)
        amount_in_dollars = convert_rub_to_dollars(payment.amount)
        price = create_stripe_price(amount_in_dollars)
        session_id, payment_link = create_stripe_session(price)
        payment.session_id = session_id
        payment_link = payment_link
        payment.save()


class UserListAPIView(generics.ListAPIView):
    serializer_class = serializers.UserSerializer
    queryset = models.User.objects.all()
    permission_classes = [IsAuthenticated]


class UserRetrieveAPIView(generics.RetrieveAPIView):
    serializer_class = serializers.UserSerializer
    queryset = models.User.objects.all()
    permission_classes = [IsAuthenticated]


class UserUpdateAPIView(generics.UpdateAPIView):
    serializer_class = serializers.UserSerializer
    queryset = models.User.objects.all()
    permission_classes = [IsAuthenticated]


class UserDestroyAPIView(generics.DestroyAPIView):
    queryset = models.User.objects.all()
    permission_classes = [IsAuthenticated]
