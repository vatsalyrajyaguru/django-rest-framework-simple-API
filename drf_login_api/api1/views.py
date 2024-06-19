from rest_framework import generics, status, serializers
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework.authtoken.models import Token
from rest_framework.authtoken.views import ObtainAuthToken
from .models import Customer, Address
from .serializers import CustomerSerializer, UserSerializer, AddressSerializer
import requests
from .models import User
from rest_framework.views import APIView

class CustomAuthToken(ObtainAuthToken):
    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data, context={'request': request})
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']
        token, created = Token.objects.get_or_create(user=user)
        return Response({
            'token': token.key,
            'user_id': user.pk,
            'email': user.email
        }, status=status.HTTP_200_OK)

class AddCustomerView(generics.CreateAPIView):
    serializer_class = CustomerSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        addresses_data = self.request.data.get('addresses')
        validated_addresses = []

        for address in addresses_data:
            pincode = address.get('pincode')
            response = requests.get(f'https://api.postalpincode.in/pincode/{pincode}')
            if response.status_code == 200 and response.json()[0]['Status'] == 'Success':
                post_office_data = response.json()[0]['PostOffice'][-1]
                address.update({
                    'post_office': post_office_data.get('Name'),
                    'district': post_office_data.get('District'),
                    'state': post_office_data.get('State'),
                    'country': post_office_data.get('Country')
                })
                validated_addresses.append(address)
            else:
                raise serializers.ValidationError({'pincode': f'Invalid pincode: {pincode}'})

        customer = serializer.save(created_by=self.request.user)
        for address_data in validated_addresses:
            address = Address.objects.create(**address_data)
            customer.addresses.add(address)

class GetCustomerView(generics.RetrieveAPIView):
    queryset = Customer.objects.all()
    serializer_class = CustomerSerializer
    permission_classes = [IsAuthenticated]
    lookup_field = 'id'

class EditCustomerView(generics.UpdateAPIView):
    queryset = Customer.objects.all()
    serializer_class = CustomerSerializer
    permission_classes = [IsAuthenticated]
    lookup_field = 'id'

    def perform_update(self, serializer):
        addresses_data = self.request.data.get('addresses')
        validated_addresses = []

        for address in addresses_data:
            pincode = address.get('pincode')
            response = requests.get(f'https://api.postalpincode.in/pincode/{pincode}')
            if response.status_code == 200 and response.json()[0]['Status'] == 'Success':
                post_office_data = response.json()[0]['PostOffice'][-1]
                address.update({
                    'post_office': post_office_data.get('Name'),
                    'district': post_office_data.get('District'),
                    'state': post_office_data.get('State'),
                    'country': post_office_data.get('Country')
                })
                validated_addresses.append(address)
            else:
                raise serializers.ValidationError({'pincode': f'Invalid pincode: {pincode}'})

        serializer.save(addresses=validated_addresses)

class ChangePasswordView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, *args, **kwargs):
        user = request.user
        old_password = request.data.get('old_password')
        new_password = request.data.get('new_password')

        if not user.check_password(old_password):
            return Response({'error': 'Old password is incorrect'}, status=status.HTTP_400_BAD_REQUEST)

        if len(new_password) < 8:
            return Response({'error': 'New password must be at least 8 characters long'}, status=status.HTTP_400_BAD_REQUEST)

        user.set_password(new_password)
        user.save()

        Token.objects.filter(user=user).delete()
        token, created = Token.objects.get_or_create(user=user)

        return Response({'token': token.key}, status=status.HTTP_200_OK)
