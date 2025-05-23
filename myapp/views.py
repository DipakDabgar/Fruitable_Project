from django.shortcuts import render,HttpResponse,redirect
from .models import*

# Create your views here.

def home(request):
    return HttpResponse("hello python")

def index(request):
    pid=Product.objects.all()[:8]
    wish_count=Add_to_wishlist.objects.all().count()
    cart_count=Add_to_cart.objects.all().count()
    con={"pid":pid,"wish_count":wish_count,"cart_count":cart_count}
    return render(request,"index.html",con)
    

def wishlist(request):
    wish_id=Add_to_wishlist.objects.all()
    wish_count=Add_to_wishlist.objects.all().count()
    cart_count=Add_to_cart.objects.all().count()
    con={"wish_id":wish_id,"wish_count":wish_count,"cart_count":cart_count}
    

    return render(request,"wishlist.html",con)

def add_wish(request,id):
    pid=Product.objects.get(id=id)
    wish_item=Add_to_wishlist.objects.filter(product_id=pid)

    if wish_item:
        wish_item.delete()
    else:
        Add_to_wishlist.objects.create(
            product_id=pid,
            price=pid.price,
            name=pid.name,
            image=pid.image,
            )
    return redirect("shop")
    
def delete_wishlist(request,id):
    dell=Add_to_wishlist.objects.get(id=id)
    dell.delete()
    return redirect("wishlist")


# def add_whishlist(request, id):
#     uid = User.objects.get(email=request.session['email'])
#     pp = product.objects.get(id=id)
#     w_id = Add_Whishlist.objects.filter(product_id=pp, user_id=uid).first()
    
#     if w_id:
#         w_id.delete()
#         messages.info(request, "Item Removed From Your Wishlist")
#     else:
#         Add_Whishlist.objects.create(
#             user_id=uid,
#             product_id=pp,
#             price=pp.price,
#             name=pp.name,
#             image=pp.img)
#         messages.info(request, "Item Saved In Your Wishlist")
        
#     return redirect("shop")


def cart(request):
    cate_id=Add_to_cart.objects.all()
    wish_count=Add_to_wishlist.objects.all().count()
    cart_count=Add_to_cart.objects.all().count()

    total_price=0
    for i in cate_id:
        total_price += i.product_id.price * i.quantity


    shipping_charge=50

    if total_price==0:
        shipping_charge=0
    else:
        shipping_charge=50

    
    grand_total= total_price + shipping_charge

    con={"cate_id":cate_id,"wish_count":wish_count,"cart_count":cart_count,"total_price":total_price,"grand_total":grand_total,"shipping_charge":shipping_charge}


    return render(request,"cart.html",con)

def add_cart(request,id):
    pid=Product.objects.get(id=id)

    cart_item=Add_to_cart.objects.filter(product_id=pid).first()

    if cart_item :

        cart_item.quantity += 1
        cart_item.total_price = cart_item.quantity * cart_item.price
        cart_item.save()

    else:
        Add_to_cart.objects.create(
            product_id=pid,
            price=pid.price,
            name=pid.name,
            quantity=1,
            image=pid.image,
            total_price=pid.price
                                   
        )

    return redirect("shop")

def quantity_plus(request,id):
    cart_item=Add_to_cart.objects.get(id=id)
    if cart_item :
        cart_item.quantity += 1
        cart_item.total_price=cart_item.quantity * cart_item.price
        cart_item.save()

        return redirect("cart")
    else :
        return redirect("cart")
    

def quantity_minus(request,id):
    cart_item=Add_to_cart.objects.get(id=id)
    
    if cart_item :
        if (cart_item.quantity==1):
            Add_to_cart.objects.get(id=id).delete()
        else:
            cart_item.quantity -= 1
            cart_item.total_price=cart_item.quantity * cart_item.price
            cart_item.save()
            return redirect("cart")

        return redirect("cart")
    else :
        return redirect("cart")


def delete_item(request,id):
    dell=Add_to_cart.objects.filter(id=id)
    dell.delete()
    return redirect("cart")

   

def checkout(request):
    wish_count=Add_to_wishlist.objects.all().count()
    cart_count=Add_to_cart.objects.all().count()
    check_id=Add_to_cart.objects.all()

    total_price=0
    for i in check_id:
        total_price += i.product_id.price * i.quantity

    con={"wish_count":wish_count,"cart_count":cart_count,"check_id":check_id,"total_price":total_price,"billing_add":billing_add}
    return render(request,"checkout.html",con)


def billing_add(request):

    if request.POST:
        first_name=request.POST["first_name"]
        last_name=request.POST["last_name"]
        company_name=request.POST["company_name"]
        address=request.POST["address"]
        city=request.POST["city"]
        country=request.POST["country"]
        pincode=request.POST["pincode"]
        mobile=request.POST["mobile"]
        email=request.POST["email"]
        note=request.POST["note"]

        if first_name and last_name and company_name and address and city and country and pincode and mobile and email and note:
            
            Billing_details.objects.create(first_name=first_name,
                                   last_name=last_name,
                                   company_name=company_name,
                                   address=address,
                                   city=city,
                                   country=country,
                                   pincode=pincode,
                                   mobile=mobile,
                                   email=email,
                                   note=note)
            return redirect("checkout")
        return render(request,"checkout.html")
        
    else:
        return render(request,"checkout.html")



def contact(request):
    name=request.POST.get("name")
    email=request.POST.get("email")
    message=request.POST.get("message")
    wish_count=Add_to_wishlist.objects.all().count()
    cart_count=Add_to_cart.objects.all().count()
    con={"wish_count":wish_count,"cart_count":cart_count}

    if name and email and message:
        Contact.objects.create(name=name,email=email,message=message)
        return redirect("index")
    
    return render(request,"contact.html",con)

def error(request):
    wish_count=Add_to_wishlist.objects.all().count()
    cart_count=Add_to_cart.objects.all().count()
    con={"wish_count":wish_count,"cart_count":cart_count}
    return render(request,"error.html",con)

def login(request):
    if request.POST:       
        email=request.POST["email"]
        password=request.POST["password"]

        if email and password:
            try:
                User.objects.get(email=email,password=password)
                return redirect("index")
            except:
                er={"e_msg":"Invalid Email or Password"}
                return render(request,"login.html",er)
    return render(request,"login.html")
        
 
     

def register(request):
    if request.POST:
        name=request.POST["name"]
        email=request.POST["email"]
        password=request.POST["password"]
        confirm_password=request.POST["confirm_password"]

        if password!=confirm_password:
           er={"e_msg":"Password do not match"}
           return render(request,"register.html",er)
        
        else:
            User.objects.create(name=name,email=email,password=password)
            return redirect("login")
    return render(request,"register.html")
    
        



def shop_detail(request):
    return render(request,"shop_detail.html")

def shop_detail1(request,id):
    pid=Product.objects.get(id=id)
    con={"pid":pid}

    return render(request,"shop_detail.html",con)

def price_filter(request):
    if request.POST:
        max1=request.POST["max1"]
        pid=Product.objects.filter(price__lte=max1)
        con={"pid":pid,"max1":max1}

    return render(request,"shop.html",con)

def shop(request):
    cid=Category.objects.all()
    cat=request.GET.get("cat")
    pid=Product.objects.all().order_by("-id")
    wish_count=Add_to_wishlist.objects.all().count()
    cart_count=Add_to_cart.objects.all().count()
    sort_by=request.GET.get('sort_by')
    wishlist_product=Add_to_wishlist.objects.all()
    l1=[]
    for i in wishlist_product:
        l1.append(i.product_id.id)

    if cat:
        pid=Product.objects.filter(cate_id=cat)
    elif sort_by == 'price_lth':
        pid = Product.objects.all().order_by('price')  
    elif sort_by == 'price_htl':
        pid = Product.objects.all().order_by('-price')  
    elif sort_by == 'name_atz':
        pid = Product.objects.all().order_by('name')  
    elif sort_by == 'name_zta':
        pid = Product.objects.all().order_by('-name') 
    else:
        pid=Product.objects.all().order_by("-id")

    con={"cid":cid,"pid":pid,"cat":cat,"wish_count":wish_count,"cart_count":cart_count,"l1":l1,"sort_by":sort_by}
    return render(request,"shop.html",con)
    
  


def testimonial(request):
    wish_count=Add_to_wishlist.objects.all().count()
    cart_count=Add_to_cart.objects.all().count()
    con={"wish_count":wish_count,"cart_count":cart_count}
    return render(request,"testimonial.html",con)


import random
from django.core.mail import send_mail

def forgot_password(request):
    if request.POST:
        email=request.POST['email']
        otp1=random.randint(1000,9999)
        try:
            uid=User.objects.get(email=email)
            uid.otp=otp1
            uid.save()
            send_mail("demo",f"your otp is - {otp1}",'dipakdabgar76@gmail.com',[email])
            contaxt={
                "email":email
            }
            return render(request,"confirm_password.html",contaxt)
        except:
            print("Invalid Email")       
            return render(request,"forgot_password.html") 
    else:
        return render(request,"forgot_password.html")
    


def confirm_password(request):
    if request.POST:
        email=request.POST['email']
        otp=request.POST['otp']
        new_password=request.POST['new_password']
        confirm_password=request.POST['confirm_password']
        
        try:
            uid=User.objects.get(email=email)
            if str(uid.otp) == otp:
                er={'msg':"Valid OTP"}
                
                if new_password==confirm_password:
                    uid.password=new_password
                    uid.save()
                    er={'msg':"Password Updated"}
                    return redirect("login")
                
                else :
                    er={"msg":"New Password and Confirm Password don't match"}
                    return render(request,"confirm_password.html",er)
                              
            elif str(uid.otp) != otp: 
                er = {"msg":"invalid otp"}
                return render(request,"confirm_password.html",er)
            
        except:
            except1 = {"except msg":"except block"}
            return render(request,"confirm_password.html",except1)
                    
        
    return render(request,"confirm_password.html")

  