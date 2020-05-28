from rest_framework import serializers
from .models import User


class UserSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'email', 'username', 'gender', 'birth_date', 'mobile', 'created_at',
                  'updated_at', 'password']

    def to_representation(self, instance):
        return {
            'id': instance.id,
            'username': instance.username,
            'first_name': instance.first_name,
            'last_name': instance.last_name,
            'email': instance.email,
            'gender': instance.gender,
            'mobile': instance.mobile,
            'birth_date': instance.birth_date,
            'created_at': instance.created_at,
            'updated_at': instance.updated_at
        }

    def update(self, instance, validated_data):
        print(validated_data)
        instance.first_name = validated_data.get('first_name', instance.first_name)
        instance.last_name = validated_data.get('last_name', instance.last_name)
        instance.gender = validated_data.get('gender', instance.gender)
        instance.save()
        return instance
