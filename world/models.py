from django.db import models
from django.contrib.auth.models import User



class Shop(models.Model):
    name = models.CharField(max_length=20)
    cost = models.IntegerField()
    max_length = models.IntegerField(blank=True , null=True)
    radius = models.IntegerField(blank=True , null=True)

    def __str__(self) -> str:
        return self.name



class Survivior(models.Model):
    user = models.OneToOneField(User , on_delete=models.CASCADE)
    points = models.IntegerField()
    inventory = models.ManyToManyField(Shop, blank=True)

    def __str__(self) -> str:
        return self.user.username



class Island(models.Model):
    lat = models.IntegerField()
    long = models.IntegerField()
    owner = models.OneToOneField(Survivior , on_delete=models.CASCADE)

    def __str__(self) -> str:
        return f"{self.owner} island"


class Bottle(models.Model):
    sender = models.ForeignKey(Survivior , on_delete=models.CASCADE , related_name="sender")
    radius = models.IntegerField(blank=True ,null=True)
    reciver = models.ForeignKey(Survivior , on_delete=models.CASCADE , related_name="reciver" , blank=True , null= True)
    text = models.TextField(max_length=500 ,blank=True , null=True)
    potensial_recivers = models.ManyToManyField(Island , related_name="poten")



    
    
