from django.http import HttpResponse, JsonResponse
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
import json
from firebase_admin.auth import UserNotFoundError
from firebase_admin import firestore

from backend.settings import get_user, db, es
from core.models import UserDetails
from balaji.filters import getESQueryFromFilters, ParseFilterExcpetion
from balaji.utils import create_api_user_access_tokens
import datetime
from balaji.indexusers import index_users, index_users_fast
from balaji.campaign import run_campaign
from balaji.utils import send_email_alert
from balaji.config import STRIPE_API_KEY_TEST
import stripe
stripe.api_key = STRIPE_API_KEY_TEST
# Create your views here.


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
        # print(request.body)
        js = json.loads(request.body.decode('utf-8'))
        # print(js)
        print("########################")
        print(js['data']['twitterUser']['additionalUserInfo']['isNewUser'])
        try:
            u = get_user(js['uid'])
            db.collection(u'userdetails').document(
                js['uid']).set(js['data'], merge=True)
            if 'twitterUser' in js['data'] and js['data']['twitterUser']['additionalUserInfo']['isNewUser']:
                message = "New User SignUp %s" % js['data']['twitterUser']['additionalUserInfo']['username']
                send_email_alert(message, message)
            return JsonResponse({"status": 200, "message": "User Data Updated", "userdetails": js['data']})
        except UserNotFoundError:
            return JsonResponse({"status": 400, "message": "User Not Authenticated"})
        except:
            return JsonResponse({"status": 500, "message": "Server Error"})
    elif request.method == 'OPTIONS':
        # print("in options")
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
            es_query = getESQueryFromFilters(
                js['filters'], id_str, js['size'])
        except ParseFilterExcpetion:
            return JsonResponse({"status": 400, "message": "Improper Filter"})
        print(es_query)
        es_response = es.search(body=es_query, index="followers")
        return JsonResponse({"status": 200, "message": "Users Returned", "es_response": es_response})


@csrf_exempt
def send_test_dm(request):
    if request.method == 'POST':
        js = json.loads(request.body.decode('utf-8'))
        twitterHandle = js['twitterHandle']
        dm = js['dm']
        escher_account = js['id_str']
        try:
            u = get_user(js['uid'])
        except UserNotFoundError:
            return JsonResponse({"status": 400, "message": "User Not Authenticated"})
        user_details = db.collection(u'userdetails').document(
            js['uid']).get().to_dict()
        # print(user_details)
        api = create_api_user_access_tokens(user_details)
        twitterUser = api.get_user(screen_name=twitterHandle)
        api.send_direct_message(twitterUser.id, dm)
        es.index('dms', body={
                 'dm': dm, 'escher_account': escher_account, 'twitterHandle': twitterHandle, 't': datetime.datetime.now()})
        return JsonResponse({"status": 200, "message": "dm sent successfully"})


@csrf_exempt
def start_campaign(request):
    if request.method == 'POST':
        js = json.loads(request.body.decode('utf-8'))
        # campaignName = js['campaignName']
        # dm = js['dm']
        # text = js['text']
        # url = js['url']
        # linkCheck = js['linkCheck']
        # filters = js['filters']
        uid = js['uid']
        try:
            u = get_user(js['uid'])
        except UserNotFoundError:
            return JsonResponse({"status": 400, "message": "User Not Authenticated"})
        campaignRef = db.collection(u'campaigns').document()
        campaignId = campaignRef.id
        js['created_at'] = datetime.datetime.now()
        try:
            print(js['data'])
            campaignRef.set(js)
            run_campaign.send(campaignId)
            js['cid'] = campaignId
            message = "Campaign Start: cid - %s uid %s" % (campaignId, uid)
            send_email_alert(message, message)
            return JsonResponse({"status": 200, "message": "Campaign Started", "campaign": js})
        except:
            return JsonResponse({"status": 400, "message": "Creating campaign failed"})


@csrf_exempt
def execute_es_search_query(request):
    if request.method == 'POST':
        js = json.loads(request.body.decode('utf-8'))
        uid = js['uid']
        try:
            u = get_user(uid)
        except UserNotFoundError:
            return JsonResponse({"status": 400, "message": "User Not Authenticated"})
        query = js['query']
        index = js['index']
        print(query)
        print(index)
        es_response = es.search(index=index, body=query)
        return JsonResponse({"status": 200, "message": "search query success", "es_response": es_response})


@csrf_exempt
def click_track(request):
    if request.method == 'POST':
        js = json.loads(request.body.decode('utf-8'))
        js['t'] = datetime.datetime.now()
        print(js)
        es.index('clicks', body=js)
        print('indexed click')
        return JsonResponse({"status": 200})


@csrf_exempt
def subscribe_conversion(request):
    if request.method == 'POST':
        js = json.loads(request.body.decode('utf-8'))
        js['t'] = datetime.datetime.now()
        print(js)
        es.index('conversions', body=js)
        return JsonResponse({"status": 200})


@csrf_exempt
def start_index_users(request):
    if request.method == 'POST':
        js = json.loads(request.body.decode('utf-8'))
        try:
            u = get_user(js['uid'])
        except UserNotFoundError:
            return JsonResponse({"status": 400, "message": "User not authenticated"})
        user_details = db.collection(u'userdetails').document(
            js['uid']
        ).get().to_dict()
        if 'index_status' in user_details and 'indexing' in user_details['index_status']:
            return JsonResponse({"status": 200, "message": "Indexing already started"})
            # do a api.me call here and if it fails send a message creds are wrong
        else:
            index_users_fast.send(js['uid'])
            message = "New indexing job for %s" % (js['uid'])
            send_email_alert(message, message)
            return JsonResponse({"status": 200, "message": "Indexing Started"})


def campaign_dict(c):
    campaign = c.to_dict()
    id_dict = {'cid': c.id}
    return {**campaign, **id_dict}


@csrf_exempt
def get_latest_campaigns(request):
    if request.method == 'POST':
        js = json.loads(request.body.decode('utf-8'))
        try:
            u = get_user(js['uid'])
        except UserNotFoundError:
            return JsonResponse({'status': 400, "message": "User not authenticated"})
        campaigns = db.collection('campaigns').where('uid', '==', js['uid']).order_by(
            'created_at', direction=firestore.Query.DESCENDING).limit(10).stream()

        campaigns_response = list(map(campaign_dict, campaigns))
        return JsonResponse({"status": 200, "message": "campaign query succeeded", "campaigns": campaigns_response})


@csrf_exempt
def create_payment_intent(request):
    if request.method == 'POST':
        js = json.loads(request.body.decode('utf-8'))
        try:
            u = get_user(js['uid'])
        except UserNotFoundError:
            return JsonResponse({'status': 400, "message": "User not authenticated"})
        amount = js['amount']
        intent = stripe.PaymentIntent.create(
            amount=amount,
            currency='inr'
        )
        print(intent)
        return JsonResponse({"status": 200, "message": "payment intent created", "clientSecret": intent['client_secret']})
