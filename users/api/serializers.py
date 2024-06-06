from rest_framework import serializers

from users.api.validators import check_phone_number
from users.models import User


class UserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ('id', 'phone_number', 'first_name', 'type', 'password')

    def create(self, validated_data):
        if not check_phone_number(validated_data['phone_number']):
            raise serializers.ValidationError({"message": "Invalid phone number"})
        user = User.objects.create_user(**validated_data)
        return user
