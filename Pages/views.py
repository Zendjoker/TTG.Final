import json
from django.shortcuts import get_object_or_404, redirect, render


import logging

# Disable logging for requests module
logging.getLogger("urllib3").setLevel(logging.CRITICAL)
logging.getLogger('http.server').setLevel(logging.CRITICAL)
logging.basicConfig(level=logging.WARNING)


import pandas as pd
import datetime as dt
import time as t
import plotly.graph_objects as go
from plotly.offline import plot
from pycoingecko import CoinGeckoAPI
import json
import sys



from django.core.exceptions import ObjectDoesNotExist
from Pages.models import OptIn

from django.utils import timezone
from django.contrib.auth.models import User
from Chat.views import get_online_users
from datetime import time, timedelta
from Carts.models import Cart, CartItem
from Chat.models import Room, Message, Section
from Orders.models import Order, OrderItem
from Pages.models import Home
from PrivateSessions.forms import PrivateSessionForm
from Products.models import Cupon, Product, Deal
from django.urls import reverse
import requests
from Users.forms import TransactionForm
from Users.models import Badge, Transaction
from .forms import LogInForm, SignUpForm
from django.contrib.auth import authenticate, login, logout
from Courses.models import Course, CourseProgression, Level, LevelProgression, Module, UserCourseProgress, Video
from django.contrib import messages
from django.http import HttpResponse, JsonResponse
from django.contrib.auth.forms import PasswordResetForm, SetPasswordForm
from .models import Dashboard, Quest, UserQuestProgress
from django.core.serializers import serialize
from Users.models import CustomUser
from django.shortcuts import render
from django.contrib.auth import logout
from django.shortcuts import redirect
from Pages.models import Feedback, Podcast, FeaturedYoutubeVideo

def homeView(request, *args, **kwargs):
    courses = request.user.customuser.enrolled_courses.all()
    home_obj = Home.objects.all().first()
    featured_course = home_obj.featured_course if home_obj else None
    podcasts = Podcast.objects.all()
    next_points_goal = 500
    quests = Quest.objects.all()
    quests_and_progress = []

    for quest in quests:
        uqp, created = UserQuestProgress.objects.get_or_create(user=request.user.customuser, quest=quest)
        quests_and_progress.append((quest, uqp))

    return render(request, 'home.html', 
                  {
                      "courses": courses, 
                      "next_points_goal": next_points_goal,
                      "feedback_options": Feedback.FEEDBACKS, 
                      "featured_course": featured_course,
                      "podcasts": podcasts, 
                      "quests_and_progress": quests_and_progress
                  })


def shopView(request, *args, **kwargs):
    products = Product.objects.all()
    deals = Deal.objects.all()
    return render(request, 'shop.html', {"products": products, "deals": deals})

def coursesView(request, *args, **kwargs):
    courses = Course.objects.all()


    return render(request, 'courses.html', {"courses": courses})


def userProfileView(request, *args, **kwargs):  
    user = CustomUser.objects.get(user=User.objects.get(username=kwargs.get('username')))
    return render(request, 'user_profile.html', {"user": user})

def levelsView(request, *args, **kwargs):
    course_id = kwargs.get('course_id')
    course = Course.objects.get(id=course_id)
    levels = Level.objects.filter(course=course)  # Filter levels by the course
    return render(request, 'levels.html', {"levels": levels})

def videoCourseView(request, level_id):
    level = Level.objects.get(id=level_id)
    course = Course.objects.get(id=level.course.id)
    user_progress, created = UserCourseProgress.objects.get_or_create(user=request.user.customuser, course=course)
    first_module = level.modules.first()  # Get the first module in the level
    if first_module:
        first_video = first_module.videos.first()  # Get the first video in the first module
    else:
        first_video = None
    return render(request, 'video-course.html', {"modules": level.modules.all(), "level": level, "video": first_video})

def notesCourseView(request, level_id):
    level = Level.objects.get(id=level_id)
    return render(request, 'notes-course.html', {"modules": level.module_set.all()})

def imgQuizzCourseView(request, level_id):
    level = Level.objects.get(id=level_id)
    return render(request, 'imgQuizz-course.html', {"modules": level.module_set.all()})

def textQuizzCourseView(request, level_id):
    level = Level.objects.get(id=level_id)
    return render(request, 'textQuizz-course.html', {"modules": level.module_set.all()})

def lessonCompletedView(request, level_id):
    level = Level.objects.get(id=level_id)
    return render(request, 'lessonComplete.html', {"modules": level.module_set.all()})


def registerView(request, *args, **kwargs):
    SignupForm = SignUpForm()
    return render(request, 'register.html', {"SignupForm": SignupForm})

def registerf(request, *args, **kwargs):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            form.save()
            first_name = form.cleaned_data['first_name']
            last_name = form.cleaned_data['last_name']
            username = form.cleaned_data['username']
            email = form.cleaned_data['email']
            password1 = form.cleaned_data['password1']
            password2 = form.cleaned_data['password2']
            """ login """
            user = authenticate(firstName=first_name, lastName=last_name, username=username, email=email, password1=password1, password2=password2)
            login(request, user)
            messages.success(request, "registred and logged in successfully.")
            return JsonResponse({'success': True})  # Return success response
        else:
            errors = form.errors.as_json()
            return JsonResponse({'success': False, 'errors': errors})  # Return error response
    else:
        return redirect('register')

def loginView(request, *args, **kwargs):
    if request.user.is_authenticated:
        return redirect('home')  # Redirect to the home page if the user is already authenticated

    LoginForm = LogInForm()
    return render(request, 'login.html', {"LoginForm": LoginForm})

def loginf(request, *args, **kwargs):
    if request.method == 'POST':
        form = LogInForm(data=request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(request, username=username, password=password)
            if user:
                messages.success(request, 'Logged In succesfully')
                login(request, user)

                return  JsonResponse({'success': True, 'error': "User logged in"})
            else:
                return  JsonResponse({'success': False, 'error': "User not found"})
        else:
            errors = form.errors.as_json()
            return JsonResponse({'success': False, 'error': errors})


def logoutf(request):
    logout(request)
    # Redirect to a specific page after logout
    return redirect('')

def pageNotFoundView(request, *args, **kwargs):
    return render(request, '404.html', {})

def forgetPasswordView(request, *args, **kwargs):

    return render(request, 'forgetPassword.html', {})


def resetDoneView(request, *args, **kwargs):
    return render(request, 'resetDone.html', {})

def newPasswordView(request, *args, **kwargs):
    
    return render(request, 'newPassword.html', {})

def verificationView(request, *args, **kwargs):
    return render(request, 'verification.html', {})


def contact_us_view(request , *args, **kwargs):
    return render(request, 'contact-us.html' , {})

def dashboardView(request, *args, **kwargs):
    try:
        dashboard = Dashboard.objects.get(id=1)
    except ObjectDoesNotExist:
        error_message = "Dashboard data not found. Please contact the support team."
        messages.error(request, error_message)
        return render(request, '404.html', {
            "error_message": error_message,
            "page": "Dashboard"
        })

    transactionForm = TransactionForm()
    transactions = Transaction.objects.all().order_by('-date')[:4]  # Assuming 'date' is the field you want to order by
    reversed_transactions = reversed(transactions)

    top_users = CustomUser.objects.all()
    top_users = sorted(top_users, key=lambda user: user.calculate_balance(), reverse=True)[:5]

    top_user = sorted(top_users, key=lambda user: user.calculate_balance(), reverse=True)[:1][0]

    return render(request, 'dashboard.html', {
        "dashboard": dashboard, 
        "transactions": reversed_transactions, 
        "top_users": top_users,
        "top_user": top_user,
        "transactionForm": transactionForm
    })

def getCryptoDetails(request, *args, **kwargs):
    context = {
        'btc': get_crypto_price("BTC-USD"),
        'eth': get_crypto_price("ETH-USD"),
        'sol': get_crypto_price("SOL-USD"),
        'avax': get_crypto_price("AVAX-USD"),
    }
    return JsonResponse({"success": True, "crypto_details": context})

def getDashboard(request, *args, **kwargs):
    if request.method == "GET":
        dashboard = Dashboard.objects.get(id=1)
        dashboard_data = {
            'objectif': dashboard.objectif,
            'profits': dashboard.get_changes_today(),
            'losses': dashboard.get_changes_today(),
            'balance': dashboard.calculate_total_balance(),
            'profits_percentage': dashboard.calculate_change_percentage(),
            'losses_percentage': dashboard.calculate_change_percentage(),
            'btc': get_crypto_price("BTC-USD"),
            'eth': get_crypto_price("ETH-USD"),
            'sol': get_crypto_price("SOL-USD"),
            'avax': get_crypto_price("AVAX-USD"),
        }

        # Return the dictionary as JSON response
        return JsonResponse({"success": True, "dashboard": dashboard_data})
    else:
        return JsonResponse({"success": False, "error": "Bad request"})

def getTransactions(request, *args, **kwargs):
    if request.method == "GET":
        transactions = Transaction.objects.all().order_by('-date')[:5]
    
        # Prepare transaction data
        transactions_data = []
        for transaction in reversed(transactions):
            badges_list = []

            # Iterate through user's badges and create dictionaries
            for badge in transaction.user.badges.all():
                badge_dict = {
                    'title': badge.title,
                    'icon': badge.icon.url  # Assuming badge.icon is a FileField
                }
                badges_list.append(badge_dict)


            transaction_data = {
                'user': transaction.user.user.username,  # Assuming user has a related User model
                'pfp': transaction.user.pfp.url,
                'badges': badges_list,
                'type': transaction.type,
                'pair': transaction.pair,
                'amount': transaction.amount,
                'date': transaction.date.strftime('%Y-%m-%d %H:%M:%S'),  # Format the date as string
                # Add other fields as needed
            }
            transactions_data.append(transaction_data)

        # Return the transactions data as JSON response
        return JsonResponse({"success": True, "transactions": transactions_data})
    else:
        return JsonResponse({"success": False, "error": "Bad request"})

def getRanking(request, *args, **kwargs):
    if request.method == "GET":
        # Query all users and order them by calculated balance in descending order
        top_users = CustomUser.objects.all()
        top_users = sorted(top_users, key=lambda user: user.calculate_balance(), reverse=True)[:5]

        # Serialize user data into JSON serializable format
        serialized_users = []
        rankIco = 1
        for user in top_users:
            serialized_user = {
                'username': user.user.username,
                'pfp': user.pfp.url,
                'balance': user.calculate_balance(),
                'rankIco': rankIco,
                # Add other fields if necessary
            }
            rankIco += 1
            serialized_users.append(serialized_user)


        # Pass the serialized top 5 users to the JsonResponse
        return JsonResponse({"success": True, "top_users": serialized_users})
    else:
        return JsonResponse({"success": False, "error": "Bad request"})

def getTopUser(request, *args, **kwargs):
    if request.method == "GET":
        # Query all users and order them by calculated balance in descending order
        top_users = CustomUser.objects.all()
        top_user = sorted(top_users, key=lambda user: user.calculate_balance(), reverse=True)[:1][0]
        badges_list = []

        for badge in top_user.badges.all():
            badge_dict = {
                'title': badge.title,
                'icon': badge.icon.url  # Assuming badge.icon is a FileField
            }
            badges_list.append(badge_dict)

        # Extract the username from the top user
        top_user_username = top_user.user.username
        
        # Serialize the top user
        top_user_serialized = serialize('json', [top_user])
        
        # Pass the serialized top user to the JsonResponse along with the username
        return JsonResponse({"success": True, "top_user": top_user_serialized, "top_user_badgesList": badges_list, "top_user_username": top_user_username, 'top_user_pfp': top_user.pfp.url})
    else:
        return JsonResponse({"success": False, "error": "Bad request"})
    


def landingView (request, *args, **kwargs):
    return render(request, 'landing.html', {})



def course_progress(request, *args, **kwargs):
    user = request.user.customuser

    course_id = 1
    course = Course.objects.get(id=course_id)


    return JsonResponse({"success": True, "course_progression": course.calculate_progress_percentage(user=user)})

def getPoints(request, *args, **kwargs):
    user=request.user.customuser
    goal=1500
    return JsonResponse({"success": True, "goal": goal, "points": user.points})

def level_progress(request, *args, **kwargs):
    user = request.user.customuser

    level_id = 1
    level = Level.objects.get(id=level_id)

    return JsonResponse({"success": True, "level_progression": level.calculate_progress_percentage(user=user)})

def addPoints(request, *args, **kwargs):
    if request.method == 'POST':
        user = request.user.customuser
        
        # Check if the user has added points in the last 24 hours
        last_added_points_time = user.last_added_points_time
        if last_added_points_time is not None and timezone.now() - last_added_points_time < timedelta(hours=24):
            return JsonResponse({"success": False, "message": "Points can only be added once every 24 hours."})
        
        # Add points to the user
        points_to_add = 10
        user.points += points_to_add
        user.last_added_points_time = timezone.now()
        user.save()

        return JsonResponse({"success": True, "message": f"Points successfully added: {points_to_add}"})
    
    return JsonResponse({"success": False, "message": "Invalid request method."})


def addTransaction(request):
    if request.method == 'POST':
        form = TransactionForm(request.POST, request.FILES)
        if form.is_valid():
            # Save the transaction
            transaction = form.save(commit=False)
            transaction.user = request.user.customuser
            transaction.save()
            return JsonResponse({"success": True})
        else:
            return JsonResponse({"success": False, "errors": form.errors})
        


""" def privateSessionView(request, *args, **kwargs):
    form = PrivateSessionRequestForm()

    # Accessing the choices from the form field
    professor_choices = form.fields['selected_professor'].choices

    # Convert the choices to a list for easier manipulation
    professor_choices_list = list(professor_choices)

    # Exclude the first element in the list
    professor_choices_list = professor_choices_list[1:]

    # Accessing the choices for duration_hours
    session_time_choices = form.fields['duration_hours'].choices

    # Convert the choices to a list for easier manipulation
    session_time_choices_list = list(session_time_choices)

    # Exclude the first element in the list
    session_time_choices_list = session_time_choices_list[1:]

    # Now you can manipulate the choices
    separated_duration_choices = [session_time_choices_list[i:i+2] for i in range(0, len(session_time_choices_list), 2)]

    return render(request, 'privateSession.html', {'form': form, "professor_choices_list": professor_choices_list, "separated_duration_choices": separated_duration_choices})

def schedulePrivateSessionView(request):
    if request.method == 'POST':
        form = PrivateSessionRequestForm(request.POST)
        if form.is_valid():
            form.save()
            # Return a JSON response indicating success
            return JsonResponse({'success': True})
        else:
            # Return a JSON response with form errors
            return JsonResponse({'success': False, 'errors': form.errors})
    else:
        # Handle GET requests, assuming there's some logic for GET requests
        # You can return an HttpResponse or render a template here
        return HttpResponse("GET request handled") """

def privateSessionView(request, *args, **kwargs):
    if request.method == 'POST':
        return privateSessionSubmitView(request)
    else:
        form = PrivateSessionForm()
        return render(request, 'privateSession.html', {'form': form})

def privateSessionSubmitView(request):
    form = PrivateSessionForm(request.POST)
    if form.is_valid():
        form.save()
        # Redirect to a success page or do something else
        return JsonResponse({"success": True, "message": "form submitted successfully"})
    else:
        return JsonResponse({"success": False, "errors": form.errors})

def privateSessionScheduleDoneView(request, *args, **kwargs):

    return render(request, 'privateSessionScheduleDone.html', {})

def settingsView(request, *args, **kwargs):

    return render(request, 'settings.html', {})

def settingsResetPasswordView(request, *args, **kwargs):

    return render(request, 'settingsResetPassword.html', {})

def paymentView(request, *args, **kwargs):

    return render(request, 'payment.html', {})

def personalInfoView(request, *args, **kwargs):

    return render(request, 'personalInfo.html', {})

def checkoutView(request, *args, **kwargs):
    # Get or create the user's cart
    cart, created = Cart.objects.get_or_create(user=CustomUser.objects.get(user=request.user))
    # Check if the cart is empty
    if cart.cart_items.exists():
        return render(request, 'checkout.html', {"cartID": cart.id, "cart": cart})
    else:
        # If the cart is empty, redirect the user to some page indicating that the cart is empty
         return redirect(reverse('shop'))

def orderCompleteView(request, *args, **kwargs):

    return render(request, 'orderComplete.html', {})

def cartView(request, *args, **kwargs):
    cart=Cart.objects.get(user=request.user.customuser)
    cart.price = cart.calculate_total_price()
    return render(request, 'cart.html', {"cart": cart})

def delete_cart_item(request):
    if request.method == 'POST':
        item_id = request.POST.get('itemId')
        try:
            # Retrieve the cart item
            cart_item = CartItem.objects.get(pk=item_id)
            # Delete the cart item
            cart_item.delete()

            user_cart = None
            try:
                user_cart = Cart.objects.filter(user=CustomUser.objects.get(user=request.user))[0]
            except:
                print ("Cart does not exist")
            if user_cart:
                # Access the items related to the cart using the related name 'cart_items'
                items = user_cart.cart_items.all()
                total_price = user_cart.calculate_total_price()
                ultimate_total = total_price
                total_items = user_cart.cart_items.count()
            else:
                items = []

            return JsonResponse({'success': True, 'message': 'Item deleted successfully', "total_price": total_price, "ultimate_total":ultimate_total, "total_items": total_items})
        except CartItem.DoesNotExist:
            return JsonResponse({'error': 'Cart item not found'})
    else:
        return JsonResponse({'error': 'bad request'})
  

def createOrderView(request):
    if request.method == 'POST':
        # Retrieve data from request.POST
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        address = request.POST.get('address')
        city = request.POST.get('city')
        state = request.POST.get('state')
        zip_code = request.POST.get('zip_code')
        payment_method = request.POST.get('payment_method')
        
        cart_id = request.POST.get('cartId')

        # Retrieve the cart
        cart = Cart.objects.get(id=cart_id)

        # Create the order
        order = Order.objects.create(
            user=request.user.customuser,  # Assuming the user is authenticated
            first_name=first_name,
            last_name=last_name,
            address=address,
            city=city,
            state=state,
            zip_code=zip_code,
            shipping_method=1,  # You may adjust this as needed
            payment_method=1,
            price=cart.price,  # Ensure you have the correct price for the order
        )

        # Move items from cart to order
        for item in cart.cart_items.all():
            order_item = OrderItem.objects.create(
                order=order,
                product=item.product,
                quantity=item.quantity,
                color=item.color,
                size=item.size,
            )

        # Clear the cart after order creation
        cart.cart_items.all().delete()
        cart.price = 0
        cart.save()
        # Redirect to payment page or confirmation page based on payment method
        if payment_method == "credit-card":
            payment = initiate_payment(request, orderId=order.id, amount=order.price)
            url = payment["payUrl"]
        else:
            url = "/shop"  # Redirect to shop or confirmation page if payment method is not credit card

        return JsonResponse({'success': True, 'order_id': order.id, "url": url})
    else:
        return JsonResponse({'success': False, 'message': 'Invalid request method'})

    

def initiate_payment(request, orderId, amount):
    # Make sure to replace these values with your actual credentials and data
    api_key = '665ddd89ecb4e3b38d776b78a:5usETKkdz0MZwYpgWLMIQXg2gtyNgGp'
    konnect_wallet_id = '65ddd89ecb4e3b38d776b78e'

    url = "https://api.preprod.konnect.network/api/v2/payments/init-payment"
    headers = {
        "x-api-key": '65f0e6d5f85f11d7b8c06004:x3QEEv76q8kvnSxAXTqjMljIeYLz',
        "Content-Type": "application/json"
    }
    payload = {
      "receiverWalletId": '65f0e6d5f85f11d7b8c06008',
      "token": "TND",
      "amount": amount * 1000,
      "type": "immediate",
      "description": "payment description",
      "acceptedPaymentMethods": [
        "bank_card",
      ],
      "lifespan": 10,
      "checkoutForm": True,
      "addPaymentFeesToAmount": True,
      "firstName": request.user.first_name,
      "lastName": request.user.last_name,
      "phoneNumber": request.user.customuser.tel,
      "email": request.user.customuser.email,
      "orderId": orderId,
      "webhook": "http://127.0.0.1:8000/webhook",
      "silentWebhook": True,
      "successUrl": "http://127.0.0.1:8000/order_complete",
      "failUrl": "http://127.0.0.1:8000/payment-error",
      "theme": "dark"
    }

    response = requests.post(url, headers=headers, json=payload)
    if response.status_code == 200:
        data = response.json()
        return data
    else:
        error_message = "Failed to initiate payment"
        if response.status_code == 401:
            error_message = "Unauthorized: API key is invalid or missing"
        elif response.status_code == 403:
            error_message = "Forbidden: You do not have permission to access this resource"
        elif response.status_code == 404:
            error_message = "Not Found: The requested resource was not found"
        elif response.status_code == 422:
            error_message = "Unprocessable Entity: The request was well-formed but failed validation"
        
        return JsonResponse({"error": error_message}, status=response.status_code)

def webhook(request):
    payment_ref = request.GET.get("payment_ref")
    if payment_ref:
        # Query Konnect API to get payment details
        payment_status = get_payment_status(payment_ref)
        # Process payment status and update database or trigger actions
        # Example: Update database with payment status
        # payment.update(status=payment_status)
        return JsonResponse({"message": "Webhook received", "payment status": payment_status})
    else:
        return JsonResponse({"error": "Payment reference ID not provided"})

def get_payment_status(payment_ref):
    # Make a request to Konnect API to get payment details
    # Replace 'YOUR_KONNECT_API_KEY' with your actual API key
    api_key = '665ddd89ecb4e3b38d776b78a:5usETKkdz0MZwYpgWLMIQXg2gtyNgGp'
    url = f"https://api.preprod.konnect.network/api/v2/payments/{payment_ref}"
    headers = {"x-api-key": api_key}
    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        payment_data = response.json()
        payment_status = payment_data.get("payment", {}).get("status")
        return payment_status
    else:
        error_message = "Failed to get payment status"
        if response.status_code == 401:
            error_message = "Unauthorized: API key is invalid or missing"
        elif response.status_code == 403:
            error_message = "Forbidden: You do not have permission to access this resource"
        elif response.status_code == 404:
            error_message = "Not Found: The requested resource was not found"
        elif response.status_code == 422:
            error_message = "Unprocessable Entity: The request was well-formed but failed validation"
        elif response.status_code == 502:
            error_message = "Bad Gateway: The server was acting as a gateway or proxy and received an invalid response from the upstream server"
        
        return error_message



def finalCartCheckoutView(request):
    cartId = request.POST.get('cartId')
    price = request.POST.get('price')
    shippingMethod = request.POST.get('shippingMethod')
    shippingCost = request.POST.get('shippingCost')

    cart = Cart.objects.get(id=cartId)
    cart.price = price
    cart.shippingMethod = shippingMethod
    cart.shippingCost = shippingCost
    cart.save()
    return JsonResponse({'success': True})


def notificationView(request, *args, **kwargs):

    return render(request, 'settingsNotification.html', {})

from django.core.serializers.json import DjangoJSONEncoder


def serverChatView(request, room_name, *args, **kwargs):
    customuser_id = request.user.customuser.id
    room = get_object_or_404(Room, name=room_name)
    messages = Message.objects.filter(room=room).order_by('timestamp').values('user__user__username', 'content', 'user__pfp', 'timestamp')
    messages_list = list(messages)
    
    # Convert QuerySet to list of dictionaries
    messages_list = [dict(message) for message in messages_list]

    # Serialize the messages list to JSON
    messages_json = json.dumps(messages_list, cls=DjangoJSONEncoder)
    
    online_user_ids = get_online_users()
    online_users = CustomUser.objects.filter(user_id__in=online_user_ids)
    
    # Get offline users
    all_users = CustomUser.objects.all()
    offline_users = all_users.exclude(user_id__in=online_user_ids)
    
    all_badges = Badge.objects.filter(customusers__in=online_users).order_by('-index')
    sections = Section.objects.all().order_by('-index')

    return render(request, 'serverChat.html', {"room_name": room_name, "customuser_id": customuser_id, "messages_json": messages_json, "online_members": online_users, "offline_members": offline_users, "all_badges": all_badges, "sections": sections})

def search_members(request):
    if request.method == 'POST':
        query = request.POST.get('q')
        
        # Perform the search for members
        matched_users = CustomUser.objects.filter(user__username__icontains=query)
        
        # Get online user IDs
        online_user_ids = get_online_users()
        
        # Separate online and offline users
        online_users = matched_users.filter(user_id__in=online_user_ids)
        offline_users = matched_users.exclude(user_id__in=online_user_ids)
        
        # Serialize the online and offline users to JSON
        online_users_list = [{'id': user.id, 'username': user.user.username, 'pfp': user.pfp.url} for user in online_users]
        offline_users_list = [{'id': user.id, 'username': user.user.username, 'pfp': user.pfp.url} for user in offline_users]
        
        return JsonResponse({"success": True, 'online_members': online_users_list, 'offline_members': offline_users_list}) 

def privateChatView(request, *args, **kwargs):

    return render(request, 'privateChat.html', {})


    

def getVideoView(request, *args, **kwargs):
    if request.method == 'POST':
        videoId = request.POST.get("videoId")
        try:
            video = Video.objects.get(id=videoId)
            serialized_video = {
                "title": video.title,
                "video_file": video.video_file.url,
                "notes": video.notes,
                "summary": video.summary,
                'finished': video.finished,
                'quiz_id': video.quiz.id,
                'quiz_question': video.quiz.id,
                'quiz_options': video.quiz.options,
                'answer': video.quiz.answer,
            }
            return JsonResponse({'success': True, "video": serialized_video})
        except Video.DoesNotExist:
            return JsonResponse({'success': False, 'message': 'Video not found'}, status=404)
    else:
        return JsonResponse({'success': False, 'message': 'Invalid request method'}, status=405)
    
def getNextVideo(request, *args, **kwargs):
    video_id = request.POST.get('video_id')
    current_video = Video.objects.get(id=video_id)
    next_video = current_video.get_next_video()
    
    if not next_video:
        # Get the next module
        next_module = current_video.module.get_next_module()
        if next_module:
            # Get the first video in the next module
            next_video = next_module.videos.order_by('index').first()
    
    return JsonResponse({'success': True, "next_video": next_video.id if next_video else None})

def videoFinishedView(request, *args, **kwargs):
    videoId = request.POST.get("videoId")
    video = Video.objects.get(id=videoId)
    course=Course.objects.get(id=video.module.level.course.id)
    user_progress, created = UserCourseProgress.objects.get_or_create(user=request.user.customuser, course=course)
    user_progress.completed_videos.add(video)
    video.module.update_completion_status(request.user.customuser)
    
    return JsonResponse({'success': True, 'message':"video finished successfully"})

def add_liked_video(request):
    user = request.user.customuser
    video = get_object_or_404(Video, id=request.POST.get("video_id"))

    # Add the video to the user's liked videos
    user.liked_videos.add(video)

    # Return a success message
    return JsonResponse({'success': True})

def remove_liked_video(request):
    user = request.user.customuser
    video = get_object_or_404(Video, id=request.POST.get("video_id"))

    user.liked_videos.remove(video)

    return JsonResponse({'success': True})

def is_video_liked(request):

    user = request.user.customuser
    video_id = request.POST.get("video_id")

    if user.liked_videos:
        is_liked = user.liked_videos.filter(id=video_id).exists()
    else:
        is_liked = None
    return JsonResponse({'is_liked': is_liked})

def ProductView (request, product_id, *args, **kwargs):
    product = Product.objects.get(id=product_id)
    return render(request, 'product.html', {"product": product})

def logout_view(request):
    logout(request)
    next_page = request.GET.get('next', '/')  # Redirige vers  par défaut
    return redirect(next_page)




def add_to_cart(request):
    if request.method == 'POST':
        # Get the product ID and types from the POST data
        product_id = request.POST.get('product_id')
        color = request.POST.get('color')
        size = request.POST.get('size')
        if product_id:
            # Get the product object
            product = get_object_or_404(Product, id=product_id)

            # Get the user's cart or create one if it doesn't exist
            user_cart, created = Cart.objects.get_or_create(user=CustomUser.objects.get(user=request.user))

            # Check if the product is already in the cart
            # Parse the 'types' JSON string into a Python dictionary

            # Check if the item already exists in the cart with the same product and types
            cart_item, item_created = CartItem.objects.get_or_create(
                cart=user_cart,
                product=product,
                color=color,
                size=size,
            )

            if not item_created:
                # If the item already exists in the cart, increment its quantity
                cart_item.quantity += 1
                cart_item.save()

            # Set the created_at timestamp for the cart if it's newly created
            if created:
                user_cart.created_at = timezone.now()
                user_cart.save()

            # Return a JSON response indicating success
            return JsonResponse({'success': True})
        else:
            # Return a JSON response indicating failure
            return JsonResponse({'success': False, 'message': 'Product ID not provided'})
    else:
        # Return a JSON response indicating failure for non-POST requests
        return JsonResponse({'success': False, 'message': 'Invalid request method'})
    
def add_video_to_finished(request, video_id):
    if request.method == 'POST':
        user = request.user.customuser
        video = get_object_or_404(Video, id=video_id)
        
        # Add the video to the finished videos of the user
        user.finished_videos.add(video)
        user.save()
        
        return JsonResponse({'message': f'Video "{video.title}" added to finished videos for user {user.user.username}'})
    
    return JsonResponse({'error': 'Method not allowed'}, status=405)



def profileView(request, username, *args, **kwargs):
    profile_user = get_object_or_404(User, username=username)
    custom_profile_user = CustomUser.objects.get(user=profile_user)
    return render(request, 'profile.html', {"custom_profile_user": custom_profile_user})

def submitFeedbackView(request, *args, **kwargs):
    if request.method == 'POST':
        feedback_value = int(request.POST.get('feedback', -1))  # Get feedback value as an integer

        if feedback_value != -1:  # Check if feedback is provided
            # Check if the user has already submitted feedback
            existing_feedback = Feedback.objects.filter(user=request.user.customuser).exists()
            if not existing_feedback:
                # If user hasn't submitted feedback, create a new Feedback instance
                Feedback.objects.create(feedback_choice=feedback_value, user=request.user.customuser)

                # Update user's points and last_added_points_time
                user = request.user.customuser
                user.points += 20
                user.save()

                return JsonResponse({'success': True, 'message': "Feedback submitted and points added"})
            else:
                return JsonResponse({'success': False, 'message': "You have already submitted feedback"})
        else:
            return JsonResponse({'success': False, 'message': "Feedback value not provided"})
    else:
        return JsonResponse({'success': False, 'message': "Invalid request method"})

from requests import Request, Session
from requests.exceptions import ConnectionError, Timeout, TooManyRedirects
import json

# -*- coding: utf-8 -*-


from random import randint

from datetime import datetime, timedelta

import requests



class LiveCryptoData(object):
    """
    This class provides methods for obtaining live Cryptocurrency price data,
    including the Bid/Ask spread from the COinBase Pro API.

    :param: ticker: information for which the user would like to return. (str)
    :returns: response_data: a Pandas DataFrame which contains the requested cryptocurrency data. (pd.DataFrame)
    """
    def __init__(self,
                 ticker,
                 verbose=True):

        if verbose:
            pass
        if not isinstance(ticker, str):
            raise TypeError("The 'ticker' argument must be a string object.")
        if not isinstance(verbose, (bool, type(None))):
            raise TypeError("The 'verbose' argument must be a boolean or None type.")

        self.verbose = verbose
        self.ticker = ticker

    def _ticker_checker(self):
        """This helper function checks if the ticker is available on the CoinBase Pro API."""
        if self.verbose:
            pass
        tkr_response = requests.get("https://api.pro.coinbase.com/products")
        if tkr_response.status_code in [200, 201, 202, 203, 204]:
            if self.verbose:
                pass
            response_data = pd.json_normalize(json.loads(tkr_response.text))
            ticker_list = response_data["id"].tolist()

        elif tkr_response.status_code in [400, 401, 404]:
            if self.verbose:
                pass
            sys.exit()
        elif tkr_response.status_code in [403, 500, 501]:
            if self.verbose:
                pass
            sys.exit()
        else:
            if self.verbose:
                pass
            sys.exit()

        if self.ticker in ticker_list:
            if self.verbose:
                pass
        else:
            raise ValueError("""Ticker: '{}' not available through CoinBase Pro API. Please use the Cryptocurrencies 
            class to identify the correct ticker.""".format(self.ticker))

    def return_data(self):
        """This function returns the desired output."""
        if self.verbose:
            pass
        self._ticker_checker()
        response = requests.get("https://api.pro.coinbase.com/products/{}/ticker".format(self.ticker))

        if response.status_code in [200, 201, 202, 203, 204]:
            if self.verbose:
                pass
            response_data = pd.json_normalize(json.loads(response.text))
            response_data["time"] = pd.to_datetime(response_data["time"])
            response_data.set_index("time", drop=True, inplace=True)
            return response_data
        elif response.status_code in [400, 401, 404]:
            if self.verbose:
                pass
            sys.exit()
        elif response.status_code in [403, 500, 501]:
            if self.verbose:
                pass
            sys.exit()
        else:
            if self.verbose:
                pass
            sys.exit()


class HistoricalData(object):
    """
    This class provides methods for gathering historical price data of a specified
    Cryptocurrency between user specified time periods. The class utilises the CoinBase Pro
    API to extract historical data, providing a performant method of data extraction.
    
    Please Note that Historical Rate Data may be incomplete as data is not published when no 
    ticks are available (Coinbase Pro API Documentation).

    :param: ticker: a singular Cryptocurrency ticker. (str)
    :param: granularity: the price data frequency in seconds, one of: 60, 300, 900, 3600, 21600, 86400. (int)
    :param: start_date: a date string in the format YYYY-MM-DD-HH-MM. (str)
    :param: end_date: a date string in the format YYYY-MM-DD-HH-MM,  Default=Now. (str)
    :returns: data: a Pandas DataFrame which contains requested cryptocurrency data. (pd.DataFrame)
    """
    def __init__(self,
                 ticker,
                 granularity,
                 start_date,
                 end_date=None,
                 verbose=True):

        if verbose:
            pass
        if not all(isinstance(v, str) for v in [ticker, start_date]):
            raise TypeError("The 'ticker' and 'start_date' arguments must be strings or None types.")
        if not isinstance(end_date, (str, type(None))):
            raise TypeError("The 'end_date' argument must be a string or None type.")
        if not isinstance(verbose, bool):
            raise TypeError("The 'verbose' argument must be a boolean.")
        if isinstance(granularity, int) is False:
            raise TypeError("'granularity' must be an integer object.")
        if granularity not in [60, 300, 900, 3600, 21600, 86400]:
            raise ValueError("'granularity' argument must be one of 60, 300, 900, 3600, 21600, 86400 seconds.")

        if not end_date:
            end_date = datetime.today().strftime("%Y-%m-%d-%H-%M")
        else:
            end_date_datetime = datetime.strptime(end_date, '%Y-%m-%d-%H-%M')
            start_date_datetime = datetime.strptime(start_date, '%Y-%m-%d-%H-%M')
            while start_date_datetime >= end_date_datetime:
                raise ValueError("'end_date' argument cannot occur prior to the start_date argument.")

        self.ticker = ticker
        self.granularity = granularity
        self.start_date = start_date
        self.start_date_string = None
        self.end_date = end_date
        self.end_date_string = None
        self.verbose = verbose

    def _ticker_checker(self):
        """This helper function checks if the ticker is available on the CoinBase Pro API."""
        if self.verbose:
            pass

        tkr_response = requests.get("https://api.pro.coinbase.com/products")
        if tkr_response.status_code in [200, 201, 202, 203, 204]:
            if self.verbose:
                pass
            response_data = pd.json_normalize(json.loads(tkr_response.text))
            ticker_list = response_data["id"].tolist()

        elif tkr_response.status_code in [400, 401, 404]:
            if self.verbose:
                pass
            sys.exit()
        elif tkr_response.status_code in [403, 500, 501]:
            if self.verbose:
                pass
            sys.exit()
        else:
            if self.verbose:
                pass
            sys.exit()

        if self.ticker in ticker_list:
            if self.verbose:
                pass
        else:
            raise ValueError("""Ticker: '{}' not available through CoinBase Pro API. Please use the Cryptocurrencies 
            class to identify the correct ticker.""".format(self.ticker))

    def _date_cleaner(self, date_time: (datetime, str)):
        """This helper function presents the input as a datetime in the API required format."""
        if not isinstance(date_time, (datetime, str)):
            raise TypeError("The 'date_time' argument must be a datetime type.")
        if isinstance(date_time, str):
            output_date = datetime.strptime(date_time, '%Y-%m-%d-%H-%M').isoformat()
        else:
            output_date = date_time.strftime("%Y-%m-%d, %H:%M:%S")
            output_date = output_date[:10] + 'T' + output_date[12:]
        return output_date

    def retrieve_data(self):
        """This function returns the data."""
        if self.verbose:
            pass

        self._ticker_checker()
        self.start_date_string = self._date_cleaner(self.start_date)
        self.end_date_string = self._date_cleaner(self.end_date)
        start = datetime.strptime(self.start_date, "%Y-%m-%d-%H-%M")
        end = datetime.strptime(self.end_date, "%Y-%m-%d-%H-%M")
        request_volume = abs((end - start).total_seconds()) / self.granularity

        if request_volume <= 300:
            response = requests.get(
                "https://api.pro.coinbase.com/products/{0}/candles?start={1}&end={2}&granularity={3}".format(
                    self.ticker,
                    self.start_date_string,
                    self.end_date_string,
                    self.granularity))
            if response.status_code in [200, 201, 202, 203, 204]:
                if self.verbose:
                    pass
                data = pd.DataFrame(json.loads(response.text))
                data.columns = ["time", "low", "high", "open", "close", "volume"]
                data["time"] = pd.to_datetime(data["time"], unit='s')
                data = data[data['time'].between(start, end)]
                data.set_index("time", drop=True, inplace=True)
                data.sort_index(ascending=True, inplace=True)
                data.drop_duplicates(subset=None, keep='first', inplace=True)
                if self.verbose:
                    pass
                return data
            elif response.status_code in [400, 401, 404]:
                if self.verbose:
                    pass
                sys.exit()
            elif response.status_code in [403, 500, 501]:
                if self.verbose:
                    pass
                sys.exit()
            else:
                if self.verbose:
                    pass
                sys.exit()
        else:
            # The api limit:
            max_per_mssg = 300
            data = pd.DataFrame()
            for i in range(int(request_volume / max_per_mssg) + 1):
                provisional_start = start + timedelta(0, i * (self.granularity * max_per_mssg))
                provisional_start = self._date_cleaner(provisional_start)
                provisional_end = start + timedelta(0, (i + 1) * (self.granularity * max_per_mssg))
                provisional_end = self._date_cleaner(provisional_end)
            
                response = requests.get(
                    "https://api.pro.coinbase.com/products/{0}/candles?start={1}&end={2}&granularity={3}".format(
                        self.ticker,
                        provisional_start,
                        provisional_end,
                        self.granularity))
            
                if response.status_code in [200, 201, 202, 203, 204]:
                    if self.verbose:
                        pass
                    dataset = pd.DataFrame(json.loads(response.text))
                    if not dataset.empty:
                        if data.empty:
                            data = dataset
                        else:
                            data = pd.concat([data, dataset], ignore_index=True)
                        time.sleep(randint(0, 2))
                    else:
                        time.sleep(randint(0, 2))
                elif response.status_code in [400, 401, 404]:
                    if self.verbose:
                        pass
                    sys.exit()
                elif response.status_code in [403, 500, 501]:
                    if self.verbose:
                        pass
                    sys.exit()
                else:
                    if self.verbose:
                        pass
                    sys.exit()
            data.columns = ["time", "low", "high", "open", "close", "volume"]
            data["time"] = pd.to_datetime(data["time"], unit='s')
            data = data[data['time'].between(start, end)]
            data.set_index("time", drop=True, inplace=True)
            data.sort_index(ascending=True, inplace=True)
            data.drop_duplicates(subset=None, keep='first', inplace=True)
            return data


def get_crypto_price(pair):
    price_str = LiveCryptoData(pair).return_data()["price"]
    price_float = float(price_str.iloc[0])
    change = calculate_daily_change_percentage(pair)
    return [price_float, change]


def get_btc_price():

    price_str = LiveCryptoData('BTC-USD').return_data()["price"]
    price_float = float(price_str.iloc[0])
    change = calculate_daily_change_percentage('BTC-USD')
    return [price_float, change]

def get_eth_price():

    price_str = LiveCryptoData('ETH-USD').return_data()["price"]
    price_float = float(price_str.iloc[0])
    change = calculate_daily_change_percentage('ETH-USD')
    return [price_float, change]

def get_sol_price():

    price_str = LiveCryptoData('SOL-USD').return_data()["price"]
    price_float = float(price_str.iloc[0])
    change = calculate_daily_change_percentage('SOL-USD')
    return [price_float, change]

def get_avax_price():

    price_str = LiveCryptoData('AVAX-USD').return_data()["price"]
    price_float = float(price_str.iloc[0])
    change = calculate_daily_change_percentage('AVAX-USD')
    return [price_float, change]



def calculate_daily_change_percentage(ticker):
    # Step 1: Obtain the closing price of the cryptocurrency for the current day from the live data
    live_data = LiveCryptoData(ticker).return_data()
    current_price = pd.to_numeric(live_data.iloc[0]['price'])

    # Step 2: Retrieve the closing price of the cryptocurrency for the previous day from the historical data
    today = datetime.now().strftime('%Y-%m-%d') + "-00-00"
    yesterday = (datetime.now() - timedelta(days=1)).strftime('%Y-%m-%d') + "-00-00"

    historical_data = HistoricalData(ticker, granularity=86400, start_date=yesterday, end_date=today).retrieve_data()
    # Check if historical data retrieval is successful

    # Convert previous day's closing price to numeric
    previous_day_price = pd.to_numeric(historical_data.iloc[-1]['open'])

    # Step 3: Calculate the daily change percentage
    daily_change_percentage = ((current_price - previous_day_price) / previous_day_price) * 100

    return daily_change_percentage


def buyCourseView(request, *args, **kwargs):
    return render(request, 'buy-course.html', {})







def start_quest(request, quest_id):
    quest = get_object_or_404(Quest, pk=quest_id)
    user = request.user.customuser

    # Create or get UserQuestProgress instance for the user and quest
    user_quest_progress, created = UserQuestProgress.objects.get_or_create(user=user, quest=quest)

    # If it's a new instance, start from the first step
    if created:
        user_quest_progress.current_step = quest.steps.first()
        user_quest_progress.save()

    # Return JSON response indicating success
    return JsonResponse({'success': True})

def complete_step(request, quest_id):
    quest = get_object_or_404(Quest, pk=quest_id)
    user = request.user.customuser
    user_quest_progress = get_object_or_404(UserQuestProgress, user=user, quest=quest)

    # Call the complete_step method to mark the current step as completed
    user_quest_progress.complete_step()

    # Return JSON response indicating success
    return JsonResponse({'success': True})

def quest_detail(request, quest_id):
    quest = get_object_or_404(Quest, pk=quest_id)
    
    # Serialize the quest object into JSON format
    quest_json = serialize('json', [quest])

    # Return JSON response with quest details
    return JsonResponse({'quest': quest_json})

def user_quest_progression(request, quest_id):
    quest = get_object_or_404(Quest, pk=quest_id)
    user = request.user.customuser
    user_quest_progress = get_object_or_404(UserQuestProgress, user=user, quest=quest)

    # Serialize the user_quest_progress object into JSON format
    user_quest_progress_json = serialize('json', [user_quest_progress])

    # Return JSON response with user quest progress details
    return JsonResponse({'user_quest_progress': user_quest_progress_json})

def optIn(request, *args, **kwargs):
    email = request.POST.get('email')
    optIn, created = OptIn.objects.get_or_create(email=email)
    message = "you already subscribed"
    if created:
        message = "thanks for subscribing"
    return JsonResponse({"sucess": True, "message": message})

def add_liked_product(request):
    user = request.user.customuser
    product = get_object_or_404(Product, id=request.POST.get("product_id"))

    # Add the product to the user's liked products
    user.liked_products.add(product)

    # Return a success message
    return JsonResponse({'success': True})

def remove_liked_product(request):
    user = request.user.customuser
    product = get_object_or_404(Product, id=request.POST.get("product_id"))

    user.liked_products.remove(product)

    return JsonResponse({'success': True})

def is_product_liked(request):

    user = request.user.customuser
    product_id = request.POST.get("product_id")
    print(product_id)
    # Check if the product is liked by the user
    if user.liked_products:
        is_liked = user.liked_products.filter(id=product_id).exists()
    else:
        is_liked = None
    # Return a response indicating whether the video is liked or not
    return JsonResponse({'is_liked': is_liked})

def apply_coupon(request, *args, **kwargs):
    cupon_title = request.POST.get("cupon")  # Changed coupon to cupon
    print(cupon_title)
    try:
        cupon = get_object_or_404(Cupon, title=cupon_title)
    except Exception:
        cupon = None

    if cupon:
        cart = request.user.customuser.cart.get()
        cart.cupon = cupon

        # Serialize the cart object
        serialized_cart = serialize('json', [cart,])

        return JsonResponse({"success": True, "message": "Coupon added successfully", "cart": serialized_cart})  # Changed cupon to coupon and Cupon to Coupon
    else:
        return JsonResponse({"success": False, "message": "Coupon not found"})  # Adde