from django.contrib.auth import views as auth_views
from accounts.forms import AuthenticationForm
from django.shortcuts import redirect
from accounts.forms import CustomUserCreationForm
from django.contrib.auth import login,authenticate,logout
from django.views.generic import CreateView

from django.contrib import messages
class LoginView(auth_views.LoginView):
    template_name = "accounts/login.html"
    form_class = AuthenticationForm
    redirect_authenticated_user = True
    
    
class LogoutView(auth_views.LogoutView):
    
    def dispatch(self, request, *args, **kwargs):
        # قبول کردن متد GET برای لاگ‌اوت
        if request.method == 'GET':
            # انجام لاگ‌اوت
            logout(request)
            # هدایت به صفحه مورد نظر
            return redirect('/')  
        
        return super().dispatch(request, *args, **kwargs)

class RegistrationView(CreateView):
    template_name = "accounts/registration.html"
    form_class = CustomUserCreationForm
    success_url = "/"  

    def form_valid(self, form):
        user = form.save()  # ذخیره فرم و دریافت کاربر
        email = form.cleaned_data.get("email")
        password = form.cleaned_data.get("password1")
        user = authenticate(self.request, email=email, password=password)

        if user is not None:
            login(self.request, user)
            return redirect(self.success_url)
        else:
            messages.error(self.request, "خطا در ورود پس از ثبت‌نام")
            return redirect("login")  # یا هر صفحه‌ای که مناسب باشد

    def form_invalid(self, form):
        messages.error(self.request, "ایمیل یا رمزعبور نامعتبر است")
        return super().form_invalid(form)