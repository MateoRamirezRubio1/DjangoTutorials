from django.shortcuts import render, redirect
from django.views.generic import TemplateView
from django.views import View
from django import forms

class HomePageView(TemplateView):
    template_name = 'pages/home.html'

class AboutPageView(TemplateView):
    template_name = 'pages/about.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update({
            "title": "About us - Online Store",
            "subtitle": "About us",
            "description": "This is an about page ...",
            "author": "Developed by: Mateo Ramirez Rubio",
        })
        
        return context
    
class ContactPageView(TemplateView):
    template_name = 'pages/contact.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update({
            "title": "Contact - Online Store",
            "subtitle": "Contact",
            "email": "mramirezr4@eafit.edu.co",
            "address": "calle 47 Medellín",
            "phone": 123456789,
            "description": "This is an contact page ...",
            "author": "Developed by: Mateo Ramirez Rubio",
        })
        
        return context
    
class Product:
    products = [
        {"id":"1", "name":"TV", "description":"Best TV", "price": 100},
        {"id":"2", "name":"iPhone", "description":"Best iPhone", "price": 102},
        {"id":"3", "name":"Chromecast", "description":"Best Chromecast", "price": 8},
        {"id":"4", "name":"Glasses", "description":"Best Glasses", "price": 200}
    ]

class ProductIndexView(View):
    template_name = 'products/index.html'

    def get(self, request):
        viewData = {}
        viewData["title"] = "Products - Online Store"
        viewData["subtitle"] = "List of products"
        viewData["products"] = Product.products

        return render(request, self.template_name, viewData)

class ProductShowView(View):
    template_name = 'products/show.html'

    def get(self, request, id):
        viewData = {}

        if int(id) > len(Product.products) or int(id) < 1:
            return redirect('home')
        
        product = Product.products[int(id)-1]

        viewData["title"] = product["name"] + " - Online Store"
        viewData["subtitle"] = product["name"] + " - Product information"
        viewData["product"] = product

        return render(request, self.template_name, viewData)
    
class ProductForm(forms.Form):
    name = forms.CharField(required=True)
    price = forms.FloatField(required=True)

    def clean_price(self):
        data = self.cleaned_data['price']

        if data < 1:
            raise forms.ValidationError("Price must be greater than zero")
        
        return data

class ProductCreateView(View):
    template_name = 'products/create.html'

    def get(self, request):
        form = ProductForm()
        viewData = {}
        viewData["title"] = "Create product"
        viewData["form"] = form

        return render(request, self.template_name, viewData)
    
    def post(self, request):
        form = ProductForm(request.POST)
        if form.is_valid():
            return render(request, 'products/createConfirmation.html')
        else:
            viewData = {}
            viewData["title"] = "Create product"
            viewData["form"] = form

            return render(request, self.template_name, viewData)