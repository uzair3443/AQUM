from django.shortcuts import render
from django.shortcuts import redirect
from django.core.mail import send_mail
from django.http import HttpResponse
import firebase_admin
from firebase_admin import credentials
from firebase_admin import db
from django.contrib import messages
from twilio.rest import Client
from django.conf import settings
from django.db import connection
import pyrebase
config = {
  "apiKey": "AIzaSyBE8Anlbx_nRK-fn8IJIqbSFjS1_tBFuBg",
  "authDomain": "ahsan-2035d.firebaseapp.com",
  "databaseURL": "https://ahsan-2035d-default-rtdb.firebaseio.com",
  "projectId": "ahsan-2035d",
  "storageBucket": "ahsan-2035d.appspot.com",
  "messagingSenderId": "487624841307",
  "appId": "1:487624841307:web:4b8161f35b23bed246c77e",
  "measurementId": "G-Y24PMRNN5P"
}
# Initialising database,auth and firebase for further use
firebase=pyrebase.initialize_app(config)
authe = firebase.auth()
database=firebase.database()

#app databse credential
cred = credentials.Certificate('C:/Users/DELL/Desktop/key/aq.json')
firebase_admin.initialize_app(cred, {
    'databaseURL': 'https://my-project-191388-default-rtdb.firebaseio.com'
})
ref = db.reference('/Users')

def index(request):
    if request.method == 'POST':
        name = request.POST.get('full-name')
        email = request.POST.get('email')
        subject = request.POST.get('subject')
        message = request.POST.get('message')

        data = {
            'name': name,
            'email': email,
            'subject': subject,
            'message':message,
        }
        
        message= '''
        New message: {}

        From: {}
        '''.format(data['message'],data['email'])
        send_mail(data['subject'],message,'',['191396@students.au.edu.pk'])
        
        
    return render(request,'index.html')

def signIn(request):
    return render(request,"signin.html")
def home(request):
    return render(request,"Home.html")
 
def postSignIn(request):
    email = request.POST.get('email')
    passw = request.POST.get('pass')
    try:
        user = authe.sign_in_with_email_and_password(email, passw)
    except:
        message = 'inavlid credentials'
        return render(request, 'signIn.html', {"messg":message})
    print(user['idToken'])
    session_id = user['idToken']
    request.session['uid'] = str(session_id)

    idtoken = request.session['uid']
    print("id" +" " + ' : ' + str(idtoken))
    a = authe.get_account_info(idtoken)
    print(a)
    a = a['users']
    a = a[0]
    a = a['localId']
    name = database.child('users').child('idToken').child('details').child('name').get().val()


    request.session['name'] = name

    return redirect('dashboard')
 


 
def signUp(request):
    return render(request,"register.html")
 
def postsignup(request):
     username= request.POST.get('username')
     email = request.POST.get('email')
     passw = request.POST.get('password1')
     cpass = request.POST.get('password2')
     firstname = request.POST.get('firstname')
     lastname = request.POST.get('lastname')
     name =f"{firstname},{lastname}"
     country = request.POST.get('country')
     province = request.POST.get('province')
     City = request.POST.get('city')
     Address1 = request.POST.get('Address1')
     Address2 = request.POST.get('Address2')
     Address= f"{Address1}, {Address2}"
     Society = request.POST.get('Society')

     try:
        user = authe.create_user_with_email_and_password(email, passw)
     except:
        message = 'unable to create account try again'
        return render(request, 'signUp.html', {"messg":message})
    
     
        # creating a user with the given email and passw
     uid = user['localId']
     data = {"name":name,"username":username,"country":country,"province":province,"City":City,"Address":Address,"Society":Society}
     database.child("users").child(uid).child("details").set(data)   
     return render(request,"signin.html")

def reset(request):
    return render(request, "Reset.html")
 
def postReset(request):
    email = request.POST.get('email')
    try:
        authe.send_password_reset_email(email)
        message  = "A email to reset password is successfully sent"
        return render(request, "Reset.html", {"msg":message})
    except:
        message  = "Something went wrong, Please check the email you provided is registered or not"
        return render(request, "Reset.html", {"msg":message})


def logout(request):
    request.session.get('uid', None)
    del request.session['uid']
    return redirect('signin')  # Replace 'home' with the name of your desired homepage URL
    
     

def dashboard(request):
    uid = request.session.get('uid')
    if not uid:
        return redirect('signin')  # Redirect to the sign-in page if user is not authenticated
    
    users_snapshot = ref.get()

    users_data = []
    for user_id, user_data in users_snapshot.items(): # type: ignore
        address = user_data.get('Address')
        email = user_data.get('Email')
        name = user_data.get('Name')
        phone_number = user_data.get('PhoneNumber')

        data = user_data.get('data')
        latest_entry = None
        if data:
            # Get the latest entry from the data
            latest_entry_id = max(data.keys())
            latest_entry = data.get(latest_entry_id)

        user_entry = {
            'id': user_id,
            'address': address,
            'email': email,
            'name': name,
            'phone_number': phone_number,
            'latest_entry': latest_entry
        }
        users_data.append(user_entry)

    context = {
        'users': users_data
    }
    return render(request, "dashboard.html", context)
def notification(request):
    uid = request.session.get('uid')
    if not uid:
        return redirect('signin') 

    if request.method == 'POST':
        user_name = request.POST.get('user_name')
        message = request.POST.get('message')
        
        # Retrieve user's phone number from Firebase based on the user name
         # Initialize the Firebase app
        
         # Assuming '/users' is the reference to the user data in Firebase Realtime Database
        user_data = ref.order_by_child('Name').equal_to(user_name).get()  # Retrieve the user data from the database
        
        if user_data:
            for user_id, user_info in user_data.items(): # type: ignore
                user_phone_number = user_info['PhoneNumber']
                
                try:
                    # Ensure the phone number is in a valid format
                    formatted_phone_number = "+92" + user_phone_number  # Assuming the phone numbers are from Pakistan (+92)
                    
                    client = Client(settings.TWILIO_ACCOUNT_SID, settings.TWILIO_AUTH_TOKEN)
                    
                    message = client.messages.create(
                        body=message,
                        from_=settings.TWILIO_PHONE_NUMBER,
                        to=formatted_phone_number
                    )
                    
                    success_message = f"SMS sent to user '{user_name}' successfully."
                    return render(request, 'send_sms.html', {'success_message': success_message})
                except Exception as e:
                    error_message = f"Error occurred while sending SMS: {str(e)}"
                    return render(request, 'send_sms.html', {'error_message': error_message})
        else:
            error_message = f"No user found with name '{user_name}'"
            return render(request, 'send_sms.html', {'error_message': error_message})
    else:
        return render(request, 'send_sms.html')
