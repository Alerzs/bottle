from rest_framework.serializers import ModelSerializer
from .models import Survivior , Bottle , Island , Shop ,User

class UserSerializer(ModelSerializer):
    class Meta:
        model = User
        fields = ["username"]


class SurSerializer(ModelSerializer):

    user = UserSerializer(read_only = True)

    class Meta:
        model = Survivior
        fields = ["user","points"]


class BottleSerializer(ModelSerializer):
    class Meta:
        model = Bottle
        fields = '__all__'


class BottleSerializer2(ModelSerializer):
    class Meta:
        model = Bottle
        fields = ["text" ,"id"]


class IslandSerializer(ModelSerializer):
    class Meta:
        model = Island
        fields = '__all__'

class ShopSerializer(ModelSerializer):
    class Meta:
        model = Shop
        exclude = ['id']

