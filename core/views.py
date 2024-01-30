import requests
from rest_framework import status
from rest_framework.response import Response
from rest_framework import serializers
from rest_framework.generics import ListCreateAPIView, CreateAPIView, RetrieveUpdateDestroyAPIView
from rest_framework.views import APIView
from .models import CustomUser as User, Bank
from .serializers import UserSerializer, BankSerializer
from django.core.exceptions import ObjectDoesNotExist
from rest_framework.exceptions import APIException

class UserListCreateAPIView(ListCreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer

class UserRetriveUpdateDestroyAPIView(RetrieveUpdateDestroyAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer

class UserRandomCreateView(CreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer

    def post(self, request, *args, **kwargs):
        res = requests.get("https://random-data-api.com/api/v2/users")
        data = res.json()
        required_fields = ['first_name', 'last_name', 'email', 'password']
        if not all(field in data for field in required_fields):
            raise serializers.ValidationError("Invalid data received from the random data API")
        
        serializer = self.get_serializer(data=data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    
class BankListCreateAPIView(ListCreateAPIView):
    queryset = Bank.objects.all()
    serializer_class = BankSerializer

class BankRetriveUpdateDestroyAPIView(RetrieveUpdateDestroyAPIView):
    queryset = Bank.objects.all()
    serializer_class = BankSerializer

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        if instance.customuser_set.exists():
            raise APIException("Cannot delete the bank because it is associated with one or more users.")
        self.perform_destroy(instance)
        return Response(status=status.HTTP_204_NO_CONTENT)

class BankRandomCreateView(CreateAPIView):
    queryset = Bank.objects.all()
    serializer_class = BankSerializer

    def post(self, request, *args, **kwargs):
        res = requests.get("https://random-data-api.com/api/v2/banks")
        data = res.json()
        required_fields = ['bank_name', 'routing_number', 'swift_bic']
        if not all(field in data for field in required_fields):
            raise serializers.ValidationError("Invalid data received from the random data API")
        
        serializer = self.get_serializer(data=data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    
class UserBankView(APIView):
    def get_user(self, user_id):
        try:
            return User.objects.get(id=user_id)
        except ObjectDoesNotExist:
            return None

    def get_bank(self, bank_id):
        try:
            return Bank.objects.get(id=bank_id)
        except ObjectDoesNotExist:
            return None

    def add_bank_to_user(self, user, bank):
        user.banks.add(bank)
        return Response({"message": "Bank added to user"}, status=status.HTTP_200_OK)

    def remove_bank_from_user(self, user, bank):
        user.banks.remove(bank)
        return Response({"message": "Bank removed from user"}, status=status.HTTP_200_OK)

    def check_user_has_bank(self, user, bank):
        if bank in user.banks.all():
            return Response({"message": "User has bank"}, status=status.HTTP_200_OK)
        else:
            return Response({"message": "User does not have bank"}, status=status.HTTP_404_NOT_FOUND)

    def post(self, request, *args, **kwargs):
        user_id = kwargs.get('user_id')
        bank_id = kwargs.get('bank_id')

        user = self.get_user(user_id)
        bank = self.get_bank(bank_id)

        if user is None:
            return Response({"message": "User does not exist"}, status=status.HTTP_404_NOT_FOUND)

        if bank is None:
            return Response({"message": "Bank does not exist"}, status=status.HTTP_404_NOT_FOUND)

        return self.add_bank_to_user(user, bank)

    def delete(self, request, *args, **kwargs):
        user_id = kwargs.get('user_id')
        bank_id = kwargs.get('bank_id')

        user = self.get_user(user_id)
        bank = self.get_bank(bank_id)

        if user is None:
            return Response({"message": "User does not exist"}, status=status.HTTP_404_NOT_FOUND)

        if bank is None:
            return Response({"message": "Bank does not exist"}, status=status.HTTP_404_NOT_FOUND)

        return self.remove_bank_from_user(user, bank)

    def put(self, request, *args, **kwargs):
        user_id = kwargs.get('user_id')
        bank_id = kwargs.get('bank_id')

        user = self.get_user(user_id)
        bank = self.get_bank(bank_id)

        if user is None:
            return Response({"message": "User does not exist"}, status=status.HTTP_404_NOT_FOUND)

        if bank is None:
            return Response({"message": "Bank does not exist"}, status=status.HTTP_404_NOT_FOUND)

        return self.add_bank_to_user(user, bank)

    def get(self, request, *args, **kwargs):
        user_id = kwargs.get('user_id')
        bank_id = kwargs.get('bank_id')

        user = self.get_user(user_id)
        bank = self.get_bank(bank_id)

        if user is None:
            return Response({"message": "User does not exist"}, status=status.HTTP_404_NOT_FOUND)

        if bank is None:
            return Response({"message": "Bank does not exist"}, status=status.HTTP_404_NOT_FOUND)

        return self.check_user_has_bank(user, bank)