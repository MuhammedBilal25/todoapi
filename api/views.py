from django.shortcuts import render
from rest_framework.viewsets import ViewSet
from rest_framework.views import APIView
from  rest_framework.response import Response
from rest_framework import status
from api.serilizers import UserSerializers,TodoSerilizer
from api.models import Todo
from rest_framework import authentication,permissions
from rest_framework import serializers

# Create your views here.
class UserCreatioView(APIView):

    def post(self,request,*args,**kwargs):

        data=request.data
        serilizer_instance=UserSerializers(data=data)
        if serilizer_instance.is_valid():
            serilizer_instance.save()
            return Response(data=serilizer_instance.data,status=status.HTTP_201_CREATED)
        return Response(data=serilizer_instance.errors,status=status.HTTP_400_BAD_REQUEST)
    
class ToDoSetView(ViewSet):

    authentication_classes=[authentication.BasicAuthentication]

    permission_classes=[permissions.IsAuthenticated]

    def list(self,request,*args,**kwargs):
        qs=Todo.objects.filter(user_object=request.user)
        serilizer_instance=TodoSerilizer(qs,many=True)
        return Response(data=serilizer_instance.data,status=status.HTTP_200_OK)
    
    def create(self,request,*args,**kwargs):
        data=request.data
        serilizer_instance=TodoSerilizer(data=data)
        if serilizer_instance.is_valid():
            serilizer_instance.save(user_object=request.user)
            return Response(data=serilizer_instance.data,status=status.HTTP_201_CREATED)
        return Response(data=serilizer_instance.errors,status=status.HTTP_400_BAD_REQUEST)

    def retrieve(self,request,*args,**kwargs):

        id=kwargs.get("pk")
        qs=Todo.objects.get(id=id)
        if request.user!=qs.user_object:
            raise serializers.ValidationError("permission  denied")
        serilizer_instance=TodoSerilizer(qs)
        return Response(data=serilizer_instance.data,status=status.HTTP_200_OK)
    
    def update(self,request,*args,**kwargs):

        id=kwargs.get("pk")
        qs=Todo.objects.get(id=id)
        if request.user!=qs.user_object:
            raise serializers.ValidationError("permission required")
        serilizer_instance=TodoSerilizer(data=request.data,instance=qs)
        if serilizer_instance.is_valid():
            serilizer_instance.save()
            return Response(data=serilizer_instance.data,status=status.HTTP_205_RESET_CONTENT)
        return Response(data=serilizer_instance.errors,status=status.HTTP_400_BAD_REQUEST)
    
    def destroy(self,request,*args,**kwargs):

        id=kwargs.get("pk")
        todo_object=Todo.objects.get(id=id)
        if request.user!=todo_object.user_object:
            raise serializers.ValidationError("permission denied")
        Todo.objects.get(id=id).delete()
        return Response(data={"message":"item deleted"},status=status.HTTP_200_OK)