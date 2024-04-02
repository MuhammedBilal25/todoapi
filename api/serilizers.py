from rest_framework import serializers
from django.contrib.auth.models import User

from api.models import Todo

class UserSerializers(serializers.ModelSerializer):

    class Meta:

        model=User
        fields=["id","username","email","password"]
        read_only_fields=["id"]

    def create(self, validated_data):
        return User.objects.create_user(**validated_data)
    
class TodoSerilizer(serializers.ModelSerializer):
     
    user_object=serializers.StringRelatedField()

    class Meta:

        model=Todo
        fields="__all__"
        read_only_fields=["id","user_object","created_date"]