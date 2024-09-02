
from rest_framework import serializers
from django.contrib.auth.models import User
from django.contrib.auth import authenticate
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.authtoken.models import Token



# Users details Serializers

class users(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = '__all__'
        
# Users Register Serializers

class UserRegister(serializers.Serializer):
    first_name = serializers.CharField()
    last_name = serializers.CharField()
    username = serializers.CharField()
    password = serializers.CharField()
    
    # Validtaions
    
    def validate(self, data):
        if User.objects.filter(username = data['username']).exists():
            raise serializers.ValidationError("This username are already exists")
        
        special_char = '!@#$%^&*()_+<>?'
        if any(char in special_char for char in data['first_name']):
            raise serializers.ValidationError('First name doesnt take Special characters')
        
        if any(char in special_char for char in data['last_name']):
            raise serializers.ValidationError('Last name doesnt take Special characters')
        
        if len(data['password']) < 5:
            raise serializers.ValidationError("password should be a atleast 5 Characters")
        
        return data
    
    # Create Users
        
    def create(self, data):
        user = User.objects.create(
            first_name = data['first_name'],
            last_name = data['last_name'],
            username = data['username']
        )
        user.set_password(data['password'])
        user.save()       
        return data
    
            
            


        

# Users Register Serializers

class LoginUser(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField()
    
    def validate(self, data):  
        if not User.objects.filter(username = data['username']).exists():
            raise serializers.ValidationError('user not found in this credientials')
        
        return data

    # Auth Tokens Created
        
    def get_token(self, data):
         
        user = authenticate(username = data['username'], password =  data['password'])
        
        if not user:
            return {'message' : 'Invalid credientials ', 'success' : False}
        
        token, _ = Token.objects.get_or_create(user = user)
        
        return {
            'success' : True,
            'token' : str(token.key)
        }
        
    
