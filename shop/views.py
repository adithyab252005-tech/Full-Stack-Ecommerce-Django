from django.http import  JsonResponse
from django.shortcuts import redirect, render,get_object_or_404
from shop.form import CustomUserForm,ProfileForm
from . models import *
from django.contrib import messages
from django.contrib.auth import authenticate,login,logout
import json
from django.templatetags.static import static
from django.template.loader import select_template
from .models import Catagory, Product
from django.contrib.auth.decorators import login_required
def home(request):
  products = Product.objects.filter(trending=1)
    
    # Find which template Django actually loads
  template = select_template(["shop/index.html"])
  print(">>> Django is using template:", template.origin.name)  
  return render(request, "shop/index.html", {"products": products})
def favviewpage(request):
  if request.user.is_authenticated:
    fav=Favourite.objects.filter(user=request.user)
    return render(request,"shop/fav.html",{"fav":fav})
  else:
    return redirect("/")
 
def remove_fav(request,fid):
  item=Favourite.objects.get(id=fid)
  item.delete()
  return redirect("/favviewpage")
 
def cart_page(request):
  if request.user.is_authenticated:
    cart=Cart.objects.filter(user=request.user)
    return render(request,"shop/cart.html",{"cart":cart})
  else:
    return redirect("/")
 
def remove_cart(request,cid):
  cartitem=Cart.objects.get(id=cid)
  cartitem.delete()
  return redirect("/cart")

def fav_page(request):
   if request.headers.get('x-requested-with')=='XMLHttpRequest':
    if request.user.is_authenticated:
      data=json.load(request)
      product_id=data['pid']
      product_status=Product.objects.get(id=product_id)
      if product_status:
         if Favourite.objects.filter(user=request.user.id,product_id=product_id):
          return JsonResponse({'status':'Product Already in Favourite'}, status=200)
         else:
          Favourite.objects.create(user=request.user,product_id=product_id)
          return JsonResponse({'status':'Product Added to Favourite'}, status=200)
    else:
      return JsonResponse({'status':'Login to Add Favourite'}, status=200)
   else:
    return JsonResponse({'status':'Invalid Access'}, status=200)

def add_to_cart(request):
   if request.headers.get('x-requested-with')=='XMLHttpRequest':
    if request.user.is_authenticated:
      data=json.load(request)
      product_qty=data['product_qty']
      product_id=data['pid']
      #print(request.user.id)
      product_status=Product.objects.get(id=product_id)
      if product_status:
        if Cart.objects.filter(user=request.user.id,product_id=product_id):
          return JsonResponse({'status':'Product Already in Cart'}, status=200)
        else:
          if product_status.quantity>=product_qty:
            Cart.objects.create(user=request.user,product_id=product_id,product_qty=product_qty)
            return JsonResponse({'status':'Product Added to Cart'}, status=200)
          else:
            return JsonResponse({'status':'Product Stock Not Available'}, status=200)
    else:
      return JsonResponse({'status':'Login to Add Cart'}, status=200)
   else:
    return JsonResponse({'status':'Invalid Access'}, status=200)
 
def logout_page(request):
  if request.user.is_authenticated:
    logout(request)
    messages.success(request,"Logged out Successfully")
  return redirect("/")
 
def login_page(request):
  if request.user.is_authenticated:
    return redirect("/")
  else:
    if request.method=='POST':
      name=request.POST.get('username')
      pwd=request.POST.get('password')
      user=authenticate(request,username=name,password=pwd)
      if user is not None:
        login(request,user)
        messages.success(request,"Logged in Successfully")
        return redirect("/")
      else:
        messages.error(request,"Invalid User Name or Password")
        return redirect("/login")
    return render(request,"shop/login.html")
 
def register(request):
  form=CustomUserForm()
  if request.method=='POST':
    form=CustomUserForm(request.POST)
    if form.is_valid():
      form.save()
      messages.success(request,"Registration Success You can Login Now..!")
      return redirect('/login')
  return render(request,"shop/register.html",{'form':form})
 
def collections(request):
  categories = Catagory.objects.all()  # fetch all categories
  context = {
        'catagory': categories,  # must match template variable
    }
  return render(request, 'shop/collections.html', context)
 
def collections_view(request, category_slug):
    category = get_object_or_404(Catagory, slug=category_slug, status=True)
    products = Product.objects.filter(category=category)
    for product in products:
        product.product_image_url = product.product_image.url if product.product_image else static('uploads/default.png')
    return render(request, "shop/products/index.html", {
        "products": products,
        "category_name": category.name
    })


# Make sure 'collections' URL exists
def product_details(request, category_slug, product_slug):
    category = get_object_or_404(Catagory, slug=category_slug, status=True)
    product = get_object_or_404(Product, category=category, slug=product_slug, status=True)
    return render(request, "shop/products/product_details.html", {"product": product})

@login_required(login_url='login')
def edit_profile(request):
    profile = request.user.profile
    if request.method == 'POST':
        form = ProfileForm(request.POST, instance=profile)
        if form.is_valid():
            form.save()
            messages.success(request, "Address updated successfully.")
            return redirect('edit_profile')
    else:
        form = ProfileForm(instance=profile)

    return render(request, 'shop/profile_edit.html', {'form': form})