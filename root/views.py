from django.shortcuts import render
from .models import *
from .forms import ContactForm, NewsLetterForm
from django.contrib import messages
from django.views.generic import CreateView
from django.shortcuts import redirect
from django.views.generic import TemplateView



class IndexView(TemplateView):
    template_name = "root/index.html" 
    def get_context_data(self, **kwargs):
        # دریافت context پیش‌فرض
        context = super().get_context_data(**kwargs)
        
        # اضافه کردن داده‌های مدل‌ها به context
        context['gallery'] = Gallery.objects.filter(status=True)[:8]  # دریافت 10 محصول اول
        
        
        return context
class AboutView(TemplateView):
    template_name = "root/about.html"

class ContactView(TemplateView):
    template_name = "root/contact-us.html"

class SendContactView(CreateView):
    """
    a class based view to show index page
    """
    http_method_names = ['post']
    form_class = ContactForm

    def form_valid(self, form):
        form.save()
        messages.success(
            self.request, 'تیکت شما با موفقیت ثبت شد و در اسرع وقت با شما تماس حاصل خواهد شد')
        return super().form_valid(form)

    def form_invalid(self, form):
        # handle unsuccessful form submission
        messages.error(
            self.request, 'مشکلی در ارسال فرم شما پیش آمد لطفا ورودی ها رو بررسی کنین و مجدد ارسال نمایید')
        return redirect(self.request.META.get('HTTP_REFERER'))

    def get_success_url(self):
        return self.request.META.get('HTTP_REFERER')
    
class NewsletterView(CreateView):
    http_method_names = ['post']
    form_class = NewsLetterForm
    success_url = '/'

    def form_valid(self, form):
        # handle successful form submission
        messages.success(
            self.request, 'از ثبت نام شما ممنونم، اخبار جدید رو براتون ارسال می کنم 😊👍')
        return super().form_valid(form)

    def form_invalid(self, form):
        # handle unsuccessful form submission
        messages.error(
            self.request, 'مشکلی در ارسال فرم شما وجود داشت که می دونم برا چی بود!! چون ربات هستید!')
        return redirect('website:index')