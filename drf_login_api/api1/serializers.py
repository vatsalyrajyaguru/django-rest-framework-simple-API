from rest_framework import serializers
from .models import User, Customer, Address
from django.contrib.auth.hashers import make_password

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['email', 'password']
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        validated_data['password'] = make_password(validated_data['password'])
        return super().create(validated_data)

class AddressSerializer(serializers.ModelSerializer):
    class Meta:
        model = Address
        fields = '__all__'

class CustomerSerializer(serializers.ModelSerializer):
    addresses = AddressSerializer(many=True)

    class Meta:
        model = Customer
        fields = '__all__'
        extra_kwargs = {
            'created_by': {'required': False}  # Exclude 'created_by' from being required
        }

    def create(self, validated_data):
        addresses_data = validated_data.pop('addresses')
        customer = Customer.objects.create(**validated_data)
        for address_data in addresses_data:
            address = Address.objects.create(**address_data)
            customer.addresses.add(address)
        return customer

    def update(self, instance, validated_data):
        addresses_data = validated_data.pop('addresses')
        instance.full_name = validated_data.get('full_name', instance.full_name)
        instance.mobile_number = validated_data.get('mobile_number', instance.mobile_number)
        instance.birthdate = validated_data.get('birthdate', instance.birthdate)
        instance.gender = validated_data.get('gender', instance.gender)
        instance.save()

        instance.addresses.clear()
        for address_data in addresses_data:
            address = Address.objects.create(**address_data)
            instance.addresses.add(address)
        return instance
