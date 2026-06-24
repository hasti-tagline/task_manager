from rest_framework import serializers
from rest_framework.serializers import ModelSerializer
from .models import User
from rest_framework_simplejwt.serializers import (TokenObtainPairSerializer)
from tasks.models import Task
import secrets
from .utils import decrypt_api_key
    
from cryptography.fernet import InvalidToken





# Register Serializer

class RegisterSerializer(ModelSerializer):
    class Meta:
        model = User
        fields = [
            "username",
            "email",
            "password"
        ]
        extra_kwargs = {
            "password": {"write_only": True}
        }

    def validate_username(self, value):
        if len(value) < 3:
            raise serializers.ValidationError(
                "Username must be at least 3 characters"
            )
        if User.objects.filter(username=value).exists():
            raise serializers.ValidationError(
                "Username already exists"
            )
        return value

  
    def validate_email(self, value):
        if User.objects.filter(email=value).exists():
            raise serializers.ValidationError(
                "Email already exists"
            )
        return value

    
    def validate_password(self, value):
        if len(value) < 6:
            raise serializers.ValidationError(
                "Password must be at least 6 characters"
            )
        return value


    def create(self, validated_data):
        user = User.objects.create_user(
            username=validated_data["username"],
            email=validated_data["email"],
            password=validated_data["password"],
            role="employee"
        )
        return user
    


# Login Serializer
class CustomLoginSerializer(TokenObtainPairSerializer):

    @classmethod
    def get_token(cls,user):
        token = super().get_token(user)
        token["role"] = user.role
        return token

    def validate(self, attrs):
        data = super().validate(attrs)
        
        if self.user.is_superuser:
            data["role"] = "admin"
        else:
            data["role"] = self.user.role

        data["username"] = self.user.username
        return data
  


# User Serializer 
class UserListSerializer(serializers.ModelSerializer):

    total_tasks = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = [
            "id",
            "username",
            "email",
            "role",
            "total_tasks",    
        ]

    def get_total_tasks(self, obj):
        return Task.objects.filter(assigned_to=obj).count()
    

    

# User Detail Serializer
class UserDetailSerializer(serializers.ModelSerializer):

    total_tasks = serializers.SerializerMethodField()

    api_key = serializers.SerializerMethodField()
    class Meta:
        model = User
        fields = [
            "id",
            "username",
            "email",
            "role",
            "api_key",
            "total_tasks",    
        ]

    def get_total_tasks(self, obj):
        return Task.objects.filter(assigned_to=obj).count()



    def get_api_key(self, obj):

        request = self.context.get("request")

        if request.user.id == obj.id or request.user.role == "manager" or request.user.role == "admin":

            try:
                return decrypt_api_key(obj.api_key)
            except InvalidToken:
                return obj.api_key

        return None
    

    