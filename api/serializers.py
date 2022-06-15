
from rest_framework import serializers
from .models import Charm, ChatRoom, Chats, Event, Faq, Notice, Report, Review, User
from rest_framework.authtoken.models import Token
from django.contrib.auth.password_validation import validate_password


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = "__all__"
        extra_kwargs = {
            'password': {'write_only': True}
        }

    def create(self, validated_data):
        password = validated_data.pop('password', None)
        instance = self.Meta.model(**validated_data)
        if password is not None:
            instance.set_password(password)
            instance.save()
            Token.objects.create(user=instance)
            return instance


class ChangePasswordSerializer(serializers.ModelSerializer):
    password = serializers.CharField(
        write_only=True, required=True, validators=[validate_password])
    password2 = serializers.CharField(write_only=True, required=True)
    old_password = serializers.CharField(write_only=True, required=True)

    class Meta:
        model = User
        fields = ('old_password', 'password', 'password2')

    def validate(self, attrs):
        if attrs['password'] != attrs['password2']:
            raise serializers.ValidationError(
                {"password": "Password fields didn't match."})

        return attrs

    def validate_old_password(self, value):
        user = self.context['request'].user
        if not user.check_password(value):
            raise serializers.ValidationError(
                {"old_password": "Old password is not correct"})
        return value

    def update(self, instance, validated_data):

        instance.set_password(validated_data['password'])
        instance.save()

        return instance


class NoticeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Notice
        fields = "__all__"


class FaqSerializer(serializers.ModelSerializer):
    class Meta:
        model = Faq
        fields = "__all__"


class ReportSerializer(serializers.ModelSerializer):
    class Meta:
        model = Report
        fields = "__all__"


class ChatSerializer(serializers.ModelSerializer):
    class Meta:
        model = Chats
        fields = "__all__"

    def update(self, instance, validated_data):
        return super().update(instance, validated_data)


class ChatRoomsSerializer(serializers.ModelSerializer):
    chats = ChatSerializer(many=True, read_only=True)

    class Meta:
        model = ChatRoom
        fields = ("id", "participants", "lastAt", 'chats', 'creatorId')


class CharmSerializer(serializers.ModelSerializer):
    class Meta:
        model = Charm
        fields = "__all__"


class ReviewSerializer(serializers.ModelSerializer):
    class Meta:
        model = Review
        fields = "__all__"


class EventSerializer(serializers.ModelSerializer):
    class Meta:
        model = Event
        fields = "__all__"
