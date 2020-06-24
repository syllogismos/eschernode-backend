from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
import json
from firebase_admin.auth import UserNotFoundError

from backend.settings import get_user, db, es
from core.models import UserDetails
from balaji.filters import getESQueryFromFilters, ParseFilterExcpetion

# Create your views here.

from django.http import HttpResponse, JsonResponse


def index(request):
    return JsonResponse({"Status": 200, "Message": "Hello, world."})


@csrf_exempt
def get_user_details(request):
    if request.method == 'POST':
        print(request.body)
        js = json.loads(request.body.decode('utf-8'))
        try:
            u = get_user(js['uid'])
            user_details = db.collection(u'userdetails').document(
                js['uid']).get().to_dict()
            return JsonResponse({"status": 200, "message": "Data Queried", "userdetails": user_details})
        except UserNotFoundError:
            return JsonResponse({"status": 400, "message": "User Not Authenticated"})
        except:
            return JsonResponse({"status": 500, "message": "Server Error"})
    if request.method == 'GET':
        return JsonResponse({"status": 200, "message": "IN GET"})


@csrf_exempt
def update_user_details(request):
    print('in update user details')
    if request.method == 'POST':
        print(request.body)
        js = json.loads(request.body.decode('utf-8'))
        try:
            u = get_user(js['uid'])
            db.collection(u'userdetails').document(
                js['uid']).set(js['data'], merge=True)
            return JsonResponse({"status": 200, "message": "Data Updated", "userdetails": js['data']})
        except UserNotFoundError:
            return JsonResponse({"status": 400, "message": "User Not Authenticated"})
        except:
            return JsonResponse({"status": 500, "message": "Server Error"})
    elif request.method == 'OPTIONS':
        print("in options")
        return JsonResponse({'status': 200, 'message': 'in options'})


@csrf_exempt
def get_filtered_users(request):
    if request.method == 'POST':
        js = json.loads(request.body.decode('utf-8'))
        id_str = js['id_str']
        try:
            u = get_user(js['uid'])
        except UserNotFoundError:
            return JsonResponse({"status": 400, "message": "User Not Authenticated"})
        # print(js)
        try:
            es_query = getESQueryFromFilters(js['filters'], id_str, 30)
        except ParseFilterExcpetion:
            return JsonResponse({"status": 400, "message": "Improper Filter"})
        print(es_query)
        es_response = es.search(body=es_query)
        return JsonResponse({"status": 200, "message": "Users Returned", "es_response": es_response})
