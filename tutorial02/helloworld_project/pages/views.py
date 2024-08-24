from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic import TemplateView, ListView
from django.views import View
from django.http import HttpResponseRedirect
from django.urls import reverse
from django import forms
from .models import Product


class HomePageView(TemplateView):
    template_name = "pages/home.html"


class AboutPageView(TemplateView):
    template_name = "pages/about.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update(
            {
                "title": "About us - Online Store",
                "subtitle": "About us",
                "description": "This is an about page ...",
                "author": "Developed by: Mateo Ramirez Rubio",
            }
        )

        return context


class ContactPageView(TemplateView):
    template_name = "pages/contact.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update(
            {
                "title": "Contact - Online Store",
                "subtitle": "Contact",
                "email": "mramirezr4@eafit.edu.co",
                "address": "calle 47 Medellín",
                "phone": 123456789,
                "description": "This is an contact page ...",
                "author": "Developed by: Mateo Ramirez Rubio",
            }
        )

        return context


"""
class Product:
    products = [
        {"id":"1", "name":"TV", "description":"Best TV", "price": 100},
        {"id":"2", "name":"iPhone", "description":"Best iPhone", "price": 102},
        {"id":"3", "name":"Chromecast", "description":"Best Chromecast", "price": 8},
        {"id":"4", "name":"Glasses", "description":"Best Glasses", "price": 200}
    ]
"""


class ProductIndexView(View):
    template_name = "products/index.html"

    def get(self, request):
        viewData = {}
        viewData["title"] = "Products - Online Store"
        viewData["subtitle"] = "List of products"
        viewData["products"] = Product.objects.all()

        return render(request, self.template_name, viewData)


class ProductShowView(View):
    template_name = "products/show.html"

    def get(self, request, id):

        # Check if product id is valid
        try:
            product_id = int(id)
            if product_id < 1:
                raise ValueError("Product id must be 1 or greater")
            product = get_object_or_404(Product, pk=product_id)
        except (ValueError, IndexError):
            # If the product id is not valid, redirect to the home page
            return HttpResponseRedirect(reverse("home"))

        viewData = {}
        viewData["title"] = product.name + " - Online Store"
        viewData["subtitle"] = product.name + " - Product information"
        viewData["product"] = product

        return render(request, self.template_name, viewData)


class ProductListView(ListView):
    model = Product
    template_name = "product_list.html"
    context_object_name = (
        "products"  # This will allow you to loop through 'products' in your template
    )

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = "Products - Online Store"
        context["subtitle"] = "List of products"
        return context


class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = ["name", "price"]

    def clean_price(self):
        price = self.cleaned_data["price"]

        if price is not None and price <= 0:
            raise forms.ValidationError("Price must be greater than zero")

        return price


class ProductCreateView(View):
    template_name = "products/create.html"

    def get(self, request):
        form = ProductForm()
        viewData = {}
        viewData["title"] = "Create product"
        viewData["form"] = form

        return render(request, self.template_name, viewData)

    def post(self, request):
        form = ProductForm(request.POST)
        if form.is_valid():
            form.save()
            return render(request, "products/createConfirmation.html")
        else:
            viewData = {}
            viewData["title"] = "Create product"
            viewData["form"] = form

            return render(request, self.template_name, viewData)
