from django.contrib.auth.hashers import make_password
from rest_framework import serializers
from .models import Bank, CustomUser as User

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'first_name', 'last_name',  'email', 'password', 'banks']
        extra_kwargs = {
            'password': {'write_only': True, "min_length": 8},
            'banks': {'required': False}
        }
    def create(self, validated_data):
        validated_data['password'] = make_password(validated_data['password'])
        return super(UserSerializer, self).create(validated_data)
    
class BankSerializer(serializers.ModelSerializer):
    class Meta:
        model = Bank
        fields = ['id', 'bank_name', 'routing_number', 'swift_bic']
