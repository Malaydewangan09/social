from django.contrib.auth import get_user_model
from django.core.mail import EmailMessage
from rest_framework import serializers

User = get_user_model()


class RegistrationSerializer(serializers.Serializer):
    email = serializers.EmailField(
        label='Registration E-Mail Address'
    )

    def validate_email(self, email):
        try:
            User.objects.get(email=email)
            raise serializers.ValidationError('Mail already exist!')
        except User.DoesNotExist:
            return email

    @staticmethod
    def send_registration_email(email, code):
        message = EmailMessage(
            subject='Social feed registration',
            body=f'This is your registration code ==>  {code}',
            to=[email],
        )
        message.send()

    def save(self, validated_data):
        email = validated_data.get('email')
        new_user = User.objects.create_user(
            username=email,
            email=email,
            is_active=False,
        )
        self.send_registration_email(
            email=email,
            code=new_user.user_profile.code,
        )
        return new_user


class RegistrationValidationSerializer(RegistrationSerializer):
    code = serializers.CharField(
        label='Validation code',
        write_only=True,
    )
    password = serializers.CharField(
        label='password',
        write_only=True,
    )
    password_repeat = serializers.CharField(
        label='password',
        write_only=True,
    )
    first_name = serializers.CharField(
        label='First name'
    )
    last_name = serializers.CharField(
        label='Last name'
    )

    def validate_email(self, email):
        try:
            return User.objects.get(email=email)
        except User.DoesNotExist:
            raise serializers.ValidationError('User does not exist!')

    def validate(self, data):
        user = data.get('email')
        if data.get('password') != data.get('password_repeat'):
            raise serializers.ValidationError({
                'password_repeat': 'Passwords do not match!'
            })
        if data.get('code') != user.user_profile.code or user.is_active:
            raise serializers.ValidationError({
                'code': 'Wrong validation code or already validated!'
            })
        return data

    def save(self, validated_data):
        user = validated_data.get('email')
        user.first_name = validated_data.get('first_name')
        user.last_name = validated_data.get('last_name')
        user.is_active = True
        user.set_password(validated_data.get('password'))
        user.save()
        return user
