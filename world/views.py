from rest_framework import generics
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.views import TokenObtainPairView
from .models import Bottle , Island , Survivior , User ,Shop 
from django.db.models import Q
from rest_framework.filters import OrderingFilter
from .serializer import  BottleSerializer ,ShopSerializer ,BottleSerializer2 ,SurSerializer
from rest_framework.permissions import IsAuthenticated ,AllowAny
from rest_framework.exceptions import ValidationError
from random import randint




class Login(TokenObtainPairView):
    pass

class Register(APIView):
    def post(self , request):
        username = request.data.get("username")
        password = request.data.get("password")
        if not username and not password:
            raise ValidationError("username and password are required")
        register_inventory = Shop.objects.all()
        my_user = User.objects.create(username = username , password = password)
        my_survivor = Survivior(user = my_user , points = 100 )
        my_survivor.save()
        my_survivor.inventory.set(register_inventory)
        my_survivor.save()
        my_island = Island.objects.create(lat = randint(-1000,1000), long = randint(-1000,1000) ,owner = my_survivor)
        return Response("you registered successfuly")

class SendBottle(APIView):
    permission_classes = [IsAuthenticated]
    def post(self , request):
        text = request.data.get("text")
        bottle_type = request.data.get("bottle_type")
        if not text or not bottle_type:
            raise ValidationError("required text and bottle type")
        
        my_sur = Survivior.objects.get(user = self.request.user)
        for shop in my_sur.inventory.all():
            if shop.name == bottle_type:
                my_sur.inventory.remove(shop)
                break
        else:
            return Response("not enough bottles")
        
        my_shop = Shop.objects.get(name = bottle_type)
        if my_shop.max_length < len(text):
            return Response("max length exceeded")
        my_island = Island.objects.get(owner = my_sur)
        bot_range = my_shop.radius
        neighbors = Island.objects.filter(Q(lat__gte = my_island.lat - bot_range) & Q(lat__lte = my_island.lat + bot_range) & Q(long__gte = my_island.long - bot_range) & Q(long__lte = my_island.long + bot_range))
        my_bottle = Bottle.objects.create(sender = my_sur, radius = my_shop.radius,  text=text)
        my_bottle.potensial_recivers.set(neighbors)
        return Response("your bottle is in the water")



class GetBottle(APIView):
    permission_classes = [IsAuthenticated]
    def get(self,request):
        my_sur = Survivior.objects.get(user = self.request.user)
        for items in my_sur.inventory.all():
            if items.name == "bottle catcher":
                my_sur.inventory.remove(items)
                break
        else:
            return Response("not enough bottle catchers")

        my_island = Island.objects.get(owner = my_sur)

        for bot in Bottle.objects.filter(reciver = None):
            for reciver in bot.potensial_recivers.all():
                if reciver == my_island:
                    bot.reciver = my_sur
                    bot.potensial_recivers.set([])
                    my_sur.points += 50
                    my_sur.save()
                    bot.save()
                    return Response(f"you found a bottle!!!   text:{bot.text}")
        return Response("no bottle available!!!")
    

class ShopView(APIView):
    def get_permissions(self):
        if self.request.method == 'GET':
            return [AllowAny()]  
        elif self.request.method == 'POST':
            return [IsAuthenticated()] 
        return super().get_permissions()

    def post(self,request):

        bottle_name = request.data.get("bottle_name")
        if not bottle_name:
            raise ValidationError("bottle_name is needed")
        my_sur = Survivior.objects.get(user = self.request.user)
        my_bottle = Shop.objects.get(name = bottle_name)
        if my_sur.points < my_bottle.cost :
            raise ValidationError("not enough points")
        my_sur.points -= my_bottle.cost
        my_sur.inventory.add(my_bottle)
        my_sur.save()
        return Response("item is added to your inventory")

    def get(self, request, *args, **kwargs):

        queryset = Shop.objects.all()
        serializer = ShopSerializer(queryset, many=True)
        return Response(serializer.data)


class MyProfile(APIView):
    permission_classes = [IsAuthenticated]
    def get(self,request):
        my_sur = Survivior.objects.get(user = self.request.user)
        my_island = Island.objects.get(owner = my_sur)
        my_inventory = my_sur.inventory.all()
        inventory = []
        for items in my_inventory:
            inventory.append(items.name)
        profile = {"name":my_sur.user.username , "points":my_sur.points  ,"island_X":my_island.lat , "island_Y":my_island.long ,"inventory":inventory}
        return Response(profile)
    
    
class ResponseToBottle(APIView):
    permission_classes = [IsAuthenticated]
    def post(self,request):


        text = request.data.get("text")
        bottle_id = request.data.get("bottle_id")
        if not text or not bottle_id:
            raise ValidationError("required text and bottle_id")
        
        my_sur = Survivior.objects.get(user = self.request.user)
        for items in my_sur.inventory.all():
            if items.name == "responce bottle":
                my_sur.inventory.remove(items)
                break
        else:
            raise ValidationError("not enough responce bottles")

        target_bottle = Bottle.objects.get(id = bottle_id)
        if target_bottle.reciver != my_sur:
            raise ValidationError("this bottle is not yours")
        target_sur = target_bottle.sender
        my_bottle = Bottle.objects.create(sender = my_sur, reciver = target_sur ,text = text)
        return Response("your bottle was sent")



class BottleInbox(generics.ListAPIView):
    queryset = Bottle.objects.all()
    serializer_class = BottleSerializer2
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        my_sur = Survivior.objects.get(user = self.request.user)
        return Bottle.objects.filter(reciver = my_sur)
    

    
class BottleSent(generics.ListAPIView):
    queryset = Bottle.objects.all()
    serializer_class = BottleSerializer2
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        my_sur = Survivior.objects.get(user = self.request.user)
        return Bottle.objects.filter(sender = my_sur)

                
class LeaderBoard(generics.ListAPIView):
    queryset = Survivior.objects.all()
    serializer_class = SurSerializer
    filter_backends = [OrderingFilter]
    ordering_fields = ['points']
    ordering = ['-points']



    
