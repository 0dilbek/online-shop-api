from rest_framework import serializers
from .models import Customer


class CustomerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Customer
        fields = ['id', 'full_name', 'phone', 'default_address']


class CustomerCreateSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)

    class Meta:
        model = Customer
        fields = ['full_name', 'phone', 'default_address', 'password']

    def validate_phone(self, value):
        if Customer.objects.filter(phone=value).exists():
            raise serializers.ValidationError("Customer with this phone already exists")
        return value

    def create(self, validated_data):
        password = validated_data.pop('password')
        customer = Customer(**validated_data)
        customer.set_password(password)
        customer.save()
        return customer


class CustomerUpdateSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, required=False)

    class Meta:
        model = Customer
        fields = ['full_name', 'phone', 'default_address', 'password']
        extra_kwargs = {
            'full_name': {'required': False},
            'phone': {'required': False},
            'default_address': {'required': False},
        }

    def validate_phone(self, value):
        customer = self.instance
        if Customer.objects.filter(phone=value).exclude(pk=customer.pk).exists():
            raise serializers.ValidationError("Another customer already has this phone number")
        return value

    def update(self, instance, validated_data):
        password = validated_data.pop('password', None)
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        if password:
            instance.set_password(password)
        instance.save()
        return instance


class CustomerLoginSerializer(serializers.Serializer):
    phone = serializers.CharField()
    password = serializers.CharField()
