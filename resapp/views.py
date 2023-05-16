from bson.objectid import ObjectId
from django.shortcuts import render,redirect
from django.http import HttpResponse
# Create your views here.
from django.core.mail import send_mail
from django.urls import reverse
from geoip2.database import Reader
import requests
from django.shortcuts import render, redirect
from django.conf import settings
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponse

import stripe
import time
import requests



from django.conf import settings # new
from django.http.response import JsonResponse # new
from django.views.decorators.csrf import csrf_exempt # new
from django.views.generic.base import TemplateView

import pymongo
from django.shortcuts import render
import os
import datetime
#from flask_mail import Mail, Message




from django.shortcuts import render




stripe.api_key=settings.STRIPE_SECRET_KEY
#@app.route('/')
def home(request):
    return render(request,'sandy.html')


#@app.route('/prop')
def index(request):
    client = pymongo.MongoClient(
        'mongodb+srv://2100032245:2100032245@cluster0.iejagan.mongodb.net/?retryWrites=true&w=majority')
    db = client['properties_db']
    collection = db['properties']
    properties = collection.find()
    return render(request,'index2.html', {"properties":properties})


#@app.route('/buy')
def buy(request):
    client = pymongo.MongoClient(
        'mongodb+srv://2100032245:2100032245@cluster0.iejagan.mongodb.net/?retryWrites=true&w=majority')
    db = client['properties_db']
    collection = db['properties']
    properties = collection.find()
    return render(request,'buy.html', {"properties":properties})


#@app.route('/book', methods=['POST'])
def bookings(request):
    if request.method=="POST":
        id = request.POST.get("id")

        client = pymongo.MongoClient(
            'mongodb+srv://2100032245:2100032245@cluster0.iejagan.mongodb.net/?retryWrites=true&w=majority')

        db = client['properties_db']
        properties_collection = db['properties']
        dashboard_collection = db['dash']
        user = {"prop_id": id}
        result = properties_collection.find_one(user)
        if result is not None:
            ename = request.session['username']

            created_date = datetime.datetime.now()
            g = {"prop_"
                 "id": id, "created_date": created_date, "bookedby": ename}
            dashboard_collection.insert_one(g)
            return redirect('dashboard2')
        else:
            return HttpResponse("<h1><center>Please check property ID</center></h1>")


#@app.route('/dashboard2')
def dashboard2(request):
    client = pymongo.MongoClient(
        'mongodb+srv://2100032245:2100032245@cluster0.iejagan.mongodb.net/?retryWrites=true&w=majority')
    db = client['properties_db']
    collection = db['dash']
    # Get all the bookings from MongoDB and display them in the dashboard
    ename = request.session['username']
    intrested = list(collection.find({'bookedby': ename}))
    if intrested:

        return render(request,'dashboard2.html', {"intr":intrested})

    else:
        return HttpResponse("not found")


#@app.route('/dashboard')
from django.shortcuts import redirect

def dashboard(request):
    client = pymongo.MongoClient(
        'mongodb+srv://2100032245:2100032245@cluster0.iejagan.mongodb.net/?retryWrites=true&w=majority')
    db = client['properties_db']
    collection = db['properties']
    # Get all the bookings from MongoDB and display them in the dashboard
    ename = request.session['username']
    bookings = list(collection.find({'seller': ename}))
    if bookings:
        if request.method == 'POST' and 'booking_id' in request.POST:
            # Get the booking ID from the form submission
            booking_id = request.POST['booking_id']
            # Delete the booking from the database
            collection.delete_one({'_id': ObjectId(booking_id)})
            # Redirect back to the dashboard
            return redirect('dashboard')
        else:
            # Render the dashboard template with the bookings data
            return render(request,'dashboard.html', {"bookings":bookings})
    else:
        return HttpResponse("not found")


#@app.route('/l', methods=['POST'])
def login(request):
    if request.method == "POST":
        ename = request.POST.get("username")
        epass = request.POST.get("password")
        client = pymongo.MongoClient(
            'mongodb+srv://2100032245:2100032245@cluster0.iejagan.mongodb.net/?retryWrites=true&w=majority')
        if ename == "admin" and epass == "123":
            return redirect('review')
        else:
            db = client["Pfsd"]
            collection = db["sdp4"]
            user = {"username": ename, "password": epass}
            result = collection.find_one(user)
            if result is not None:
                ip = request.META.get('HTTP_X_FORWARDED_FOR', '') or request.META.get('REMOTE_ADDR', '')
                response = requests.get(f'https://api.ipdata.co/{ip}?api-key=ef82679de52de91914ddd943d26389e549815579a9148d3245c0a42a')
                if response.status_code == 200:
                    data = response.json()
                    city = data.get('city', 'Unknown')
                else:
                    city = 'Unknown'
                email = result.get('email', '')

                request.session['username'] = ename
                subject = 'Loggin Notification'
                message = f"Dear {ename},\n\nThank you for logging in to our website. We hope you enjoy your experience here! \n\nBest regards,\nThe Website Team\n\nYou are visiting from: {ip} address"
                from_email = 'sandeepnaga763@gmail.com'
                recipient_list = [email]
                send_mail(subject, message, from_email, recipient_list, fail_silently=False)

                #request.session.permanent = True

                return render(request, "index.html", {"name": ename})
            else:
                return HttpResponse("<h1><center>fail</center></h1>")



#@app.route('/booki')
def register(request):
    return render(request,'buy.html')


#@app.route('/lr', methods=['POST', 'GET'])
def hlr(request):
    if request.method=="POST":
        ename = request.POST.get("username")
        email = request.POST.get("email")
        epass = request.POST.get("password")

        client = pymongo.MongoClient(
            'mongodb+srv://2100032245:2100032245@cluster0.iejagan.mongodb.net/?retryWrites=true&w=majority')

        db = client["Pfsd"]
        collection = db["sdp4"]
        user = {"username": ename, "email": email, "password": epass}
        result = collection.insert_one(user)
        if result != None:

            # send welcome email to new user
            subject = 'Welcome to our website!'
            message = f"Dear {ename},\n\nThank you for registering with our website. We hope you enjoy your experience here!\n\nBest regards,\nThe Website Team"
            from_email = 'sandeepnaga763@gmail.com'
            recipient_list = [email]
            send_mail(subject, message, from_email, recipient_list, fail_silently=False)

            return render(request, 'sandy.html', {'new_user': True})
        else:
            return HttpResponse("<h1><center>invalid</center></h1>")
    else:
        return render(request, 'sandy.html')


#@app.route('/send-email', methods=['POST'])
# def send_email():
#     name = request.form['name']
#     email = request.form['email']
#     subject = request.form['subject']
#     message = request.form['message']
#
#     msg = Message(subject, sender=email, recipients=['sandeepnaga763@gmail.com'])
#     msg.body = f"Name: {name}\nEmail: {email}\nMessage: {message}"
#
#     mail.send(msg)
#
#     return 'Email sent successfully!'


#@app.route('/sell', methods=['GET', 'POST'])
from django.core.mail import send_mail

def sell(request):
    if request.method == "POST":
        client = pymongo.MongoClient(
            'mongodb+srv://2100032245:2100032245@cluster0.iejagan.mongodb.net/?retryWrites=true&w=majority')
        db = client['properties_db']
        collection = db['properties_tm']
        ename = request.session['username']

        property = {
            'seller': ename,
            'name': request.POST['name'],
            'image': request.POST['image'],
            'price': request.POST['price'],
            'type': request.POST['type'],
            'prop_id': request.POST['prop_id'],
            'Location': request.POST['Location'],
            'contact': request.POST['contact'],
            'size': request.POST['size'],
            'category': request.POST['category'],
        }

        if int(property['size']) < 50:
            return render(request, 'sell.html', {'error': 'Land size cannot be less than 50 sqft.'})
        else:
            collection.insert_one(property)

            # Send notification email to admin
            subject = 'New Property Added'
            message = f"A new property has been added to the website by {ename}.\n\nProperty details:\n\nName: {property['name']}\nPrice: {property['price']}\nLocation: {property['Location']}\nSize: {property['size']} sqft\nContact: {property['contact']}\n\nYou can view the property on the website."
            from_email = 'yourwebsite@example.com'
            recipient_list = ['sandeepnaga763@gmail.com']
            send_mail(subject, message, from_email, recipient_list, fail_silently=False)

            return redirect('sell')
    else:
        return render(request, 'sell.html')

def send_email(request):
    name = request.POST['name']
    email = request.POST['email']
    subject = request.POST['subject']
    message = request.POST['message']

    message_body = f"Name: {name}\nEmail: {email}\nMessage: {message}"

    send_mail(
        subject,
        message_body,
        email,
        ['sandeepnaga763@gmail.com'],
        fail_silently=False,
    )

    return HttpResponse('Email sent successfully!')
def review_properties(request):
    if request.method == "GET":

        client = pymongo.MongoClient(
            'mongodb+srv://2100032245:2100032245@cluster0.iejagan.mongodb.net/?retryWrites=true&w=majority')
        db = client['properties_db']
        temp_collection = db['properties_tm']


        properties = temp_collection.find()

        return render(request, 'rp.html', {'properties': properties})
    elif request.method == "POST":

        client = pymongo.MongoClient(
            'mongodb+srv://2100032245:2100032245@cluster0.iejagan.mongodb.net/?retryWrites=true&w=majority')
        db = client['properties_db']
        temp_collection = db['properties_tm']
        perm_collection = db['properties']


        approved = request.POST.getlist('approved')
        rejected = request.POST.getlist('rejected')

        for prop_id in approved:
            if prop_id:
                property = temp_collection.find_one({'prop_id': prop_id})

                property['status'] = 'approved'
                print(f'Inserting property {prop_id} into permanent collection')
                perm_collection.insert_one(property)
                print(f'Successfully inserted property {prop_id} into permanent collection')
                temp_collection.delete_one({'prop_id': prop_id})

        for prop_id in rejected:
            if prop_id:
                property = temp_collection.find_one({'prop_id': prop_id})
                if property:
                    temp_collection.delete_one({'prop_id': prop_id})
                else:
                    print(f"Error deleting property {prop_id}: property not found")
            else:
                print(f"Error deleting property {prop_id}: invalid property number")


        return redirect('review')
#@app.route('/logut')
def logout(request):
    # ...
    return redirect('home')
    # ...
def get_context_data(self, **kwargs):
    context = super().get_context_data(**kwargs)
    context['key'] = settings.STRIPE_PUBLISHABLE_KEY
    return context
def charge(request):
    if request.method == 'POST':
        stripe.api_key = settings.STRIPE_SECRET_KEY
        token = request.POST['stripeToken']
        try:
            charge = stripe.Charge.create(
                amount=10000,
                currency='inr',
                description='A Payement Gate charge',
                source=token,
            )
            return render(request, 'charge.html')
        except stripe.error.CardError as e:
            # Handle card errors
            pass
        except stripe.error.RateLimitError as e:
            # Handle rate limit errors
            pass
        except stripe.error.InvalidRequestError as e:
            # Handle invalid request errors
            pass
        except stripe.error.AuthenticationError as e:
            # Handle authentication errors
            pass
        except stripe.error.APIConnectionError as e:
            # Handle API connection errors
            pass
        except stripe.error.StripeError as e:
            # Handle all other Stripe errors
            pass
    else:
        context = {'key': settings.STRIPE_PUBLISHABLE_KEY}
        return render(request, 'charge.html', context)
def payment(request):
    return render(request,"payment.html")
from bson import ObjectId

from bson.objectid import ObjectId

def delete_booking(request):
    if request.method == 'POST':
        client = pymongo.MongoClient('mongodb+srv://2100032245:2100032245@cluster0.iejagan.mongodb.net/?retryWrites=true&w=majority')
        db = client['properties_db']
        collection = db['properties']

        # Get the booking number of the booking to be deleted from the request data
        booking_number = request.POST.get('prop_id')

        # Check that the booking_number is not empty
        if booking_number:
            # Delete the booking from MongoDB
            result = collection.delete_one({'prop_id': booking_number})

            if result.deleted_count == 1:
                return redirect('dashboard')
            else:
                return HttpResponse("Delete operation failed.")
        else:
            return HttpResponse("Invalid booking number.")
    else:
        return HttpResponse("Invalid request method.")

