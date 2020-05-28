from rest_framework import serializers

def validate_password(value):
    """
        check password length
    :param value:
    :return:value
    """
    if len(value) >= 8 and len(value) <= 15:
        return value
    raise serializers.ValidationError("Password length should be minimum 8 and maximum 15 character long. ")