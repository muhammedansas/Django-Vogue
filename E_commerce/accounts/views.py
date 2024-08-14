from django.shortcuts import render,redirect,get_object_or_404
from . forms import RegistrationForm,Userform,Userprofileform
from . models import Account,Userprofile
from cart.models import Cart,Cartitem
from django.contrib import messages,auth
from django.contrib.auth.decorators import login_required
from cart.views import _cart_id
from django.http import HttpResponse

#verification email
from django.contrib.sites.shortcuts import get_current_site
from django.template.loader import render_to_string
from django.utils.http import urlsafe_base64_encode,urlsafe_base64_decode
from django.utils.encoding import force_bytes
from django.contrib.auth.tokens import default_token_generator
from django.core.mail import EmailMessage

# Create your views here.



def register(request):
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            first_name = form.cleaned_data['first_name']
            last_name = form.cleaned_data['last_name']
            phone_number = form.cleaned_data['phone_number']
            email = form.cleaned_data['email']
            password = form.cleaned_data['password']
            username = email.split("@")[0]
            user = Account.objects.create_user(
                first_name=first_name,
                last_name=last_name,
                email=email,
                password=password,
                username=username
            )
            user.phone_number = phone_number
            user.save()
            
            # User activation
            try:
                current_site = get_current_site(request)
                mail_subject = "Please activate your account"
                message = render_to_string('accounts/verification_email.html', {
                    'user': user,
                    'domain': current_site.domain,
                    'uid': urlsafe_base64_encode(force_bytes(user.pk)),
                    'token': default_token_generator.make_token(user),
                })
                to_email = email
                send_email = EmailMessage(mail_subject, message, to=[to_email])
                send_email.send()
                messages.success(request, "Registration successful. Please check your email to activate your account.")
                return redirect("register")
            except Exception as e:
                print(f"Error sending email: {e}")
                messages.error(request, "There was an error sending the activation email. Please try again.")
    
    else:
        form = RegistrationForm()
    
    context = {
        'form': form
    }
    return render(request, "accounts/register.html", context)

def login(request):
    if request.method == "POST":
        email = request.POST["email"]
        password = request.POST["password"]
        print(email,password)
        user = auth.authenticate(request,email=email,password=password)
        print(user)
        if user is not None:
            try:
                if user.is_blocked:
                    messages.error(request,"This user is blocked please unblock")
                    return redirect('login')
                cart = Cart.objects.get(cart_id=_cart_id(request))
                cartitem_exists = Cartitem.objects.filter(cart=cart).exists()
                if cartitem_exists:
                    cart_item = Cartitem.objects.filter(cart=cart)
                    for item in cart_item:
                        item.user = user
                        item.save()
            except:
                pass    
            auth.login(request,user)
            if user.is_admin:
                return redirect("admin_panel")
            else:
                return redirect('home')
        else:
            messages.error(request,"Invalid login")
            return redirect("login")
    return render(request,"accounts/login.html")

@login_required(login_url='login')
def logout(request):
    auth.logout(request)
    messages.success(request, 'You are logged out')
    return redirect('login')

def activate(request,uidb64,token):
    try:
        uid = urlsafe_base64_decode(uidb64).decode()
        user = Account._default_manager.get(pk=uid)
    except(TypeError,ValueError,OverflowError,Account.DoesNotExist):
        user =None    
    
    if user is not None and default_token_generator.check_token(user,token):
        user.is_active = True
        user.save()
        messages.success(request,'Congragulations your account is activated.')
        return redirect('login')
    else:
        messages.error(request,"Invalid activation link")
        return redirect('register')
    

@login_required(login_url='login')
def edit_profile(request):
    try:
        user_profile = Userprofile.objects.get(user=request.user)
    except Userprofile.DoesNotExist:
        user_profile = None
    
    if request.method == "POST":
        user_form = Userform(request.POST,instance=request.user)
        profile_form = Userprofileform(request.POST,request.FILES,instance=user_profile)
        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()
            messages.success(request,'Your profile has been updated')
            return redirect('edit_profile')
        else:
            return redirect("home")
    else:
        user_form = Userform(instance=request.user)
        profile_form = Userprofileform(instance=user_profile)

    context = {
        'user_form':user_form,
        'profile_form':profile_form,
        'user_profile':user_profile
    }    
    return render(request,'accounts/edit_profile.html',context)


def forgotpassword(request):
    if request.method == 'POST':
        email = request.POST['email']
        if Account.objects.filter(email=email).exists():
            user = Account.objects.get(email__exact=email)

            # Reset password
            current_site = get_current_site(request)
            mail_subject = "Reset your password"
            message = render_to_string('accounts/reset_password_email.html',{
                'user':user,
                'domain':current_site,
                'uid':urlsafe_base64_encode(force_bytes(user.pk)),
                'token':default_token_generator.make_token(user),
            })
            to_email = email
            send_email = EmailMessage(mail_subject,message,to=[to_email])
            send_email.send()

            messages.success(request,'Password reset email has been sent to your email address')
            return redirect('login')
        else:
            messages.error(request,"Account does not exist")  
            return redirect('forgotpassword')  
    return render(request,'accounts/forgotpassword.html')

def resetpassword_validate(request,uidb64,token):
    try:
        uid = urlsafe_base64_decode(uidb64).decode()
        user = Account._default_manager.get(pk=uid)
    except(TypeError,ValueError,OverflowError,Account.DoesNotExist):
        user =None    

    if user is not None and default_token_generator.check_token(user,token):
        request.session['uid'] = uid
        messages.success(request,'Please reset your password')
        return redirect('resetpassword')
    else:
        messages.error(request,"This link is expired")  
        return redirect('login')  
    

def resetpassword(request):
    if request.method == "POST":
        new_password = request.POST['new_password']
        confirm_password = request.POST['confirm_password']
        
        if new_password == confirm_password:
            uid = request.session.get('uid')
            user = Account.objects.get(pk=uid)
            user.set_password(new_password)
            user.save()
            messages.success(request,'Password successfully reset')
            return redirect('login')
        else:
            messages.error(request,'Password does not match') 
            return redirect('resetpassword')
    
    return render(request,'accounts/resetpassword.html')    