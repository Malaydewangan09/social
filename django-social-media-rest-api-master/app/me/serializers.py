from django.contrib.auth import get_user_model
from rest_framework import serializers

User = get_user_model()


class MeSerializer(serializers.ModelSerializer):
    username = serializers.CharField(
        required=False,
        allow_blank=False,
    )

    first_name = serializers.CharField(
        required=False,
        allow_blank=False,
    )

    @staticmethod
    def validate_username(username):
        try:
            User.objects.get(username=username)
            raise serializers.ValidationError('Username is already taken!')
        except User.DoesNotExist:
            return username

    @staticmethod
    def validate_first_name(first_name):
        if len(first_name) < 4:
            raise serializers.ValidationError("The name has to be at least 4 chars long!")
        return first_name

    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'first_name', 'last_name']
        read_only_fields = ['id']