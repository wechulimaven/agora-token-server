from django.shortcuts import render
import requests

from rest_framework.views import APIView
from rest_framework.response import Response
from django.http import HttpResponse, JsonResponse

from .access_token import *

from django.conf import settings

import json

from django.views.decorators.csrf import csrf_exempt


# Create your views here.

Role_Attendee = 0 # depreated, same as publisher
Role_Publisher = 1 # for live broadcaster
Role_Subscriber = 2 # default, for live audience
Role_Admin = 101

class GenerateToken(APIView):

    def post(self, request, *args, **kwargs):


        requestData = request.data

        appId = requestData["appId"]
        appCertificate = requestData["appCertificate"]
        channelName = requestData["channelName"]
        account = requestData["account"]
        uid = requestData["uid"]
        role = requestData["role"]
        # privilegeExpiredTs = requestData["privilegeExpiredTs"]

        expireTimeInSeconds = 3600
        currentTimestamp = int(time.time())
        privilegeExpired = currentTimestamp + expireTimeInSeconds

        token = AccessToken(appId, appCertificate, channelName, account) 
        token.addPrivilege(kJoinChannel, privilegeExpired)
        if (role == Role_Attendee) | (role == Role_Admin) | (role == Role_Publisher):
            token.addPrivilege(kPublishVideoStream, privilegeExpired)
            token.addPrivilege(kPublishAudioStream, privilegeExpired)
            token.addPrivilege(kPublishDataStream, privilegeExpired)


        return Response(token.build())



# {
#        "appId": "22e79556998b4be090f91226b06d8024",
#         "appCertificate": "9442787e54444105994dfcf28eeae09d",
#        "channelName": "testagora",
#        "account": "314137",
#         "uid": "requestData",
#         "role": "Role_Publisher"
# }