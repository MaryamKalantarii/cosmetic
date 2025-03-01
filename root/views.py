from django.shortcuts import render
from django.views.generic import TemplateView



class IndexView(TemplateView):
    template_name = "root/index.html" 

class AboutView(TemplateView):
    template_name = "root/about.html"

 