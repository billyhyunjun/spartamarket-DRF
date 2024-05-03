from rest_framework import serializers
from .models import User

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        exclude = ["following"]
        
    def create(self, validated_data): 
        user = super().create(validated_data) 
        user.set_password(validated_data['password']) 
        user.save() 
        return user
    
    def to_representation(self, value): 
        ret = super().to_representation(value) 
        ret['following'] = [following_user.username for following_user in value.following.all()]
        return ret
