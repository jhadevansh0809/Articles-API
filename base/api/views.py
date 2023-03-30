from rest_framework.response import Response
from .serializers import ArticleSerializer
from base.models import Article

from rest_framework.decorators import api_view

from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework_simplejwt.views import TokenObtainPairView

from django.contrib.auth.models import User
from rest_framework import viewsets

import re

from email_validator import validate_email, EmailNotValidError


class MyTokenObtainPairSerializer(TokenObtainPairSerializer):
    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)

        # Add custom claims
        token['username'] = user.username
        # ...

        return token
    
class MyTokenObtainPairView(TokenObtainPairView):
    serializer_class =  MyTokenObtainPairSerializer



class ArticleViewSet(viewsets.ModelViewSet):
    queryset = Article.objects.all()
    serializer_class = ArticleSerializer
    


@api_view(['GET','PUT'])
def getUserArticles(request,username):
     articles =  Article.objects.filter(author=username)
     serializer = ArticleSerializer(articles,many=True)
     return Response(serializer.data)


def strongpasswordchecker(password):
    while True:
        if (len(password)<=8):
            return False
        elif not re.search("[a-z]", password):
            return False
        elif not re.search("[A-Z]", password):
            return False
        elif not re.search("[0-9]", password):
            return False
        elif not re.search("[_@$]" , password):
            return False
        elif re.search("\s" , password):
            return False
        else:
            return True
        
def validemailchecker(email):
    try:
        v = validate_email(email)
        email = v["email"] 
        return True
    except EmailNotValidError as e:
        return False


@api_view(['POST'])
def getUser(request):
        data = request.data
        firstname=data['firstname']
        lastname=data['lastname']
        username=data['username']
        email=data['email']
        password=data['password1']
        confirm_password=data['password2']
        if(username.find(' ')==-1): 
            if(validemailchecker(email)): 
                if password == confirm_password:
                    if(strongpasswordchecker(password)):
                        if User.objects.filter(username=username).exists():
                                return Response (
                                {
                                "message":"Username already exists!",
                                "status" : False,
                                }
                                )
                        else:
                            if User.objects.filter(email=email).exists():
                                return Response (
                                {
                                "message":"Email already exists!",
                                "status" : False,
                                }
                                )
                            else:
                                user=User.objects.create_user(first_name=firstname,last_name=lastname,username=username,email=email,password=password)
                                user.save()
                                return Response (
                                {
                                "message":"User created successfully!",
                                "status" : True,
                                }
                                )
                        
                    else:
                        return Response (
                            {
                            "message":" Passwords is not strong! \n Primary conditions for password validation: \n 1.Minimum 8 characters. \n 2.The alphabet must be between [a-z]. \n 3.At least one alphabet should be of Upper Case [A-Z]. \n 4.At least 1 number or digit between [0-9]. \n 5.At least 1 character from [ _ or @ or $ ].",
                            "status" : False,
                            }
                            )
                        
                else:
                    return Response (
                        {
                        "message":"Passwords didn't match!",
                        "status" : False,
                        }
                        )
            else:
                  return Response (
                        {
                        "message":"Enter valid email!",
                        "status" : False,
                        }
                        )
                      
        else:
            return Response (
                {
                "message":"Username should contain one word only!",
                "status" : False,
                }
                )
             

