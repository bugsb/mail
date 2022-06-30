from django.shortcuts import render,redirect
from django.contrib.auth.models import User,auth
from django.contrib import messages
from login.models import Security
from django.http import HttpResponse
# Create your views here.
def login(request):
   return render(request,'login.html')

def signup(request):
   if request.method == 'POST':
         first_name = request.POST['firstname']
         last_name = request.POST['lastname']
         email = request.POST['email']
         first_name = request.POST['firstname']
         passwd = request.POST['password']
         confirm_passwd = request.POST['confirm_password']
         qes = request.POST['qes']
         ans = request.POST['ans']
         if passwd == confirm_passwd:
               if User.objects.filter(email=email).exists():
                       messages.info(request,"Email Already exists !")
                       return redirect('/signup')
               elif ans == '':
                    messages.info(request,"Please provide security question details..")
                    return redirect('/signup')
               else:
                  user = User.objects.create_user(username = email,first_name=first_name,last_name=last_name,email=email,password=passwd)
                  security = Security(qes=qes,ans=ans,user=email)
                  user.save()
                  security.save()
                  print("User Added----------------------------------------------")
                  print("000000000000000000000\n",qes,ans)
                  auth.login(request,user)
                  return redirect('/app/')
         else:
               messages.info(request,"Password Do not Match !")
               return redirect('/signup')
   else:
      return render(request,'signup.html')

def login(request):
   if request.method == 'POST':
      email = request.POST['email']
      passwd = request.POST['passwd']

      user = auth.authenticate(username=email,password=passwd)
      
      if user is not None:
             auth.login(request,user)
             print("logrdIn----------------------------------------------")
             return redirect('/app/')
      else:
             messages.info(request,"Invalid credentials")
             print("not  logrdIn----------------------------------------------")
             return redirect('/')

   else:
      return render(request,'login.html')


def logout(request):
   auth.logout(request)
   return redirect('login')

def resetpass(request):
   if request.method == 'POST':
         email = request.POST['email']
         qes = request.POST['qes']
         ans = request.POST['ans']

         data = Security.objects.filter(user=email).first()
         print("-------------------",data)
         if data.qes == qes and data.ans == ans:
            return redirect("/pass/")
   else:
      return render(request,'resetpass.html')


def password(request):
   if request.method == 'POST':
      email = request.POST['email']
      password = request.POST['passwd']
     
      print("--------------------",password,email)
      user=User.objects.filter(email=email).first()
      user.set_password(password)
      user.save()
      return HttpResponse("Password Change Succes")

   else:
      return render(request,'pass.html')