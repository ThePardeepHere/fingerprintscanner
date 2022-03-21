from django.shortcuts import render, HttpResponse, redirect
from .models import content,userprofile
from django.contrib.auth.models import User, auth
from django.contrib.auth import authenticate, login, logout
from django.http import JsonResponse, request
from django.views.decorators.csrf import csrf_exempt
from django.core.files.base import ContentFile
import base64
from django.core.files.base import ContentFile
import datetime
from django.contrib.auth.decorators import login_required
import os
import zipfile
from io import StringIO ,BytesIO
from fingerprintscanner.settings import BASE_DIR
from django.contrib import messages



from .models import userprofile, adminUser

# Create your views here.

def test(request):
    return render(request, 'FPS/newTest.html')


@csrf_exempt
def testupload(request):
    print(request.POST.get('iname'))
    iname =request.POST.get('iname')
    user = request.user
    userpro = userprofile.objects.get(user=user)
    con = content()
    # # print(request.is_ajax)
    # print(request.FILES)
    if request.method == "POST":
        img = request.FILES['file']

        con.name = iname
        con.thumbnail = img
        con.addedby = userpro
        con.save()
        return JsonResponse({'data': con.thumbnail.__str__()})

def index(request):
    return render(request, 'FPS/index.html')





# def useradmin(request):
#     return render(request, 'FPS/admin_index.html')




def TnC(request):
    return render(request, 'FPS/agree.html')


def create(request):
    if(request.method == "POST"):
        c = content()
        c.thumbnail = request.FILES.get('myfile')
        c.save()
    return render(request, 'FPS/some.html')

@login_required(login_url='login_form')
def scanner(request,fno):
    fname=""
    # Left Angle Center Angle Right Angle-
    names = ["Left Thumb Left Angle","Left Thumb Center Angle","Left Thumb Right Angle",
                "Left Index Left Angle","Left Index Center Angle","Left Index Right Angle",
                "Left Middle Left Angle","Left Middle Center Angle","Left Middle Right Angle",
                "Left Ring Left Angle","Left Ring Center Angle","Left Ring Right Angle",
                "Left Pinky Left Angle","Left Pinky Center Angle","Left Pinky Right Angle",
                "Right Thumb Left Angle","Right Thumb Center Angle","Right Thumb Right Angle",
                "Right Index Left Angle","Right Index Center Angle","Right Index Right Angle",
                "Right Middle Left Angle","Right Middle Center Angle","Right Middle Right Angle",
                "Right Ring Left Angle","Right Ring Center Angle","Right Ring Right Angle",
                "Right Pinky Left Angle","Right Pinky Center Angle","Right Pinky Right Angle",
    ]
    if fno<30:
        fname = names[fno]
    else:
        return redirect('thanks')
    return render(request, 'FPS/newTest.html',{'fno':fno,'fname':fname})


def forgetpass(request):
    return render(request, 'FPS/forgotpassword.html')


def emailprotection(request):
    return render(request, 'FPS/emailprotection.html')


def login_user(request):

    if request.method == 'POST':

        name = request.POST.get('username')
        passw = request.POST.get('password')
        try:
            user = auth.authenticate(username=name, password=passw)

            print("--------login view-----------")
            print(user)
            return render(request, 'FPS/scanner.html')

        except:

            return redirect('useradmin')

    else:

        return redirect('useradmin')




@csrf_exempt
def cropimg(request):
    print(request.POST.get('iname'))
    iname =request.POST.get('iname')
    user = request.user
    userpro = userprofile.objects.get(user=user)
    con = content()
    # # print(request.is_ajax)
    # print(request.FILES)
    if request.method == "POST":
        img = request.FILES['file']

        con.name = iname
        con.thumbnail = img
        con.addedby = userpro
        con.save()
        return JsonResponse({'data': con.thumbnail.__str__()})


    # user = request.user
    # userpro = userprofile.objects.get(user=user)
    # con = content()
    # # # print(request.is_ajax)
    # # print(request.FILES)
    # if request.method == "POST":
    #     img = request.POST.get("raw_image")
    #     iname = request.POST.get("iname")
    #     format, imgstr = img.split(';base64,')
    #     ext = format.split('/')[-1]

    #     # You can save this as file instance.
    #     data = ContentFile(base64.b64decode(imgstr),
    #                        name=f'{iname}-{datetime.datetime.today().strftime("%Y-%m-%d-%H:%M:%S")}.' + ext)

    #     # print("00------------------00")
    #     # print(img)
    #     # print(type(img))
    #     # print("00------------------00")
    #     con.name = iname
    #     con.thumbnail = data
    #     con.addedby = userpro
    #     con.save()
    #     return JsonResponse({'data': con.thumbnail.__str__()})


def login_form(request):
    if request.method == "POST":
        username = request.POST.get("username")
        passw = request.POST.get("password")
        try:
            user = authenticate(username=username, password=passw)
            print(user)
            if user is not None:
                try:
                    userpro = userprofile.objects.get(user=user)
                    print(userpro)
                    if userpro is not None:
                        login(request, user)
                        # return render(request,"FPS/userlist.html")
                        return redirect('TnC')
                    else:
                        return render(request, "FPS/login_form.html",{'msg':"please check the username and password entered"})
                except:
                    return render(request, "FPS/login_form.html",{'msg':"please check the username and password entered"})
            else:
                return render(request, "FPS/login_form.html",{'msg':"please check the username and password entered"})
        except:
            return render(request, "FPS/login_form.html",{'msg':"please check the username and password entered"})

    return render(request, 'FPS/login_form.html')

@login_required(login_url='franchiselogin')
def user_details(request,idi):
    user = User.objects.get(id=idi)
    userpro = userprofile.objects.get(user=user)
    userimg = content.objects.filter(addedby=userpro)
    return render(request, 'FPS/user_details.html',{'user':userpro,"userimg":userimg})


def register(request):
    if request.method == "POST":
        adcode = request.POST.get('admincode')
        adminuser = adminUser.objects.get(uniqueCode=adcode)

        if adminuser.userLimit <10:
            try:
                username = request.POST.get('username')
                email = request.POST.get('email')
                adcode = request.POST.get('admincode')
                phone = request.POST.get('phone')
                passw = request.POST.get('pass')
                repass = request.POST.get('repass')
                admin = adminUser.objects.get(uniqueCode=adcode)
                userlist = userprofile.objects.filter(admin=admin)
                print(userlist.__len__())
                if userlist.__len__()>=10:
                    return render(request, 'FPS/signup.html',{'msg':"Opps!! ,User Limit For Franchise Exceeded"})
                print(request.POST)
                if(passw!=repass):
                    return render(request, 'FPS/signup.html',{'msg':"Password Does Not Match"})
                try:
                    user = User.objects.create_user(username=username, email=email, password=passw)
                    user.save()
                    admin = adminUser.objects.get(uniqueCode=adcode)
                    userpro = userprofile()
                    userpro.admin = admin
                    userpro.mobile = phone
                    userpro.user = user
                    userpro.save()
                    print("Success")
                    usercnt = admin.userLimit
                    admin.userLimit = usercnt+1
                    admin.save()
                    # messages.add_message(request,messages.SUCCESS,"Your Account Has Been Created !")
                    return render(request, 'FPS/login_form.html',{"msg":"User Created Successfully please login"})
                except Exception as e:
                    print("Not POST"+str(e))
                    return render(request, 'FPS/signup.html',{'msg':"Something Went Wrong Please Enter Valid Credentials"})
            except Exception as e:
                print("Not POSt "+str(e))
                return render(request, 'FPS/signup.html',{'msg':"Something Went Wrong Please Enter Valid Credentials"})
        else:
            return render(request, 'FPS/signup.html',{'msg':"Max Limit Exceeded! Please Create New Franchise"})
    return render(request, 'FPS/signup.html')

def createFranchise(request):
    if request.method == "POST":
        try:
            username = request.POST.get('username')
            email = request.POST.get('email')
            adcode = request.POST.get('admincode')
            phone = request.POST.get('phone')
            passw = request.POST.get('pass')
            repass=request.POST.get('repass')
            if(passw!=repass):
                return render(request, 'FPS/createfranchise.html',{'msg':"Password does not match"})
            print(request.POST)
            try:
                user = User.objects.create_user(username, email, passw)
                user.save()
                # admin = adminUser.objects.get(uniqueCode=adcode)
                admin = adminUser()
                admin.userid = user
                admin.uniqueCode = adcode
                admin.save()
                return render(request, 'FPS/createfranchise.html',{'msg':"Franchise created"})
            except Exception as r:

                return render(request, 'FPS/createfranchise.html',{'msg':"something went wrong ,Please try with a different username"+str(r)})
        except:
            return render(request, 'FPS/createfranchise.html',{'msg':"something went wrong"})
    return render(request, 'FPS/createfranchise.html')


def franchiselogin(request):
    if request.method == "POST":
        username = request.POST.get('username')
        passw = request.POST.get('pass')
        user = authenticate(username=username, password=passw)
        print("------franchise")
        if user is not None:
            try:
                franchise = adminUser.objects.get(userid=user)
                if franchise is not None:
                    login(request, user)
                    # return render(request,"FPS/userlist.html")
                    return redirect('userlist')
            except Exception as e:
                print(e)
                return render(request, "FPS/franchiseLogin.html",{'msg':"please check the username and password entered"})
        else:
            return render(request, "FPS/franchiseLogin.html",{'msg':"please check the username and password entered"})
    return render(request, "FPS/franchiseLogin.html")


@login_required(login_url='franchiselogin')
def userlist(request):
    user = request.user
    franchise = adminUser.objects.get(userid=user)
    print(franchise)
    userlist = userprofile.objects.filter(admin=franchise)
    print(userlist)
    return render(request, "FPS/userlist.html", {'userlist': userlist})
def thanks(request):
    return render(request,"FPS/thankyou.html")
def instruction(request):
    return render(request,"FPS/instruction.html")
def nextToscan(request):
    return redirect('scanner',fno=0)






def getfiles(request,un):
    """
        This function is used to get all the images of the selected user,
        and adds a file containing his/her details.
    """
    print(BASE_DIR)

    uid = User.objects.get(username=un)
    useracc = userprofile.objects.get(user=uid)
    contentu = content.objects.filter(addedby=useracc )
    f = open(f"{useracc}details.txt","w")

    f.write(f"Username:{useracc.user.username}\nContact No.:{useracc.mobile}\nE-mail:{useracc.user.email}\nAccess code:{useracc.admin.uniqueCode}")
    f.close()

    fn = []
    processed = []
    for u in contentu:
        if ".jpg" or ".bmp" in u.thumbnail.path:

            fn.append(u.thumbnail.path)

    filenames = fn+processed
    print(filenames)
    # print(os.path.abspath(f"{useracc}details.txt"))
    filenames.append(os.path.abspath(f"{useracc}details.txt"))

    zip_subdir = str(useracc.user.username)
    zip_filename = "%s.zip" % zip_subdir

    # Open StringIO to grab in-memory ZIP contents
    s = BytesIO()

    # The zip compressor
    zf = zipfile.ZipFile(s, "w")

    for fpath in filenames:
        # Calculate path for file in zip

        fdir, fname = os.path.split(fpath)
        if fpath in fn:
            fname = f'RAW/{fname}'
        if fpath in processed:
            fname = f'PROCESSED/{fname}'
        zip_path = os.path.join(zip_subdir, fname)

        # Add file, at correct path
        zf.write(fpath, zip_path)

    # Must close zip for all contents to be written
    zf.close()

    # Grab ZIP file from in-memory, make response with correct MIME-type
    resp = HttpResponse(s.getvalue(), content_type = "application/x-zip-compressed")
    # ..and correct content-disposition
    resp['Content-Disposition'] = 'attachment; filename=%s' % zip_filename

    return resp




def delimg(request):
    u = User.objects.get(username='nil')
    user = userprofile.objects.get(user=u)
    con = content.objects.filter(addedby=user)
    for c in con:
        c.delete()
def adminlogin(request):
    return render(request, 'FPS/admin_index.html')
def checkadmin(request):
    if request.method == "POST":

        username = request.POST.get('a_username')
        passw = request.POST.get('a_password')
        user = authenticate(username=username, password=passw)
        print(user)
        print("------Admin")
        if user is not None:
            try:
                if user.is_superuser:
                    login(request, user)
                    return redirect("franchiselist")
                else:
                    return render(request,"FPS/admin_index.html",{'msg':"please check the username and password entered"})
            except Exception as e:
                print(e)
                return render(request, "FPS/admin_index.html",{'msg':"please check the username and password entered"})
        else:
            return render(request, "FPS/admin_index.html",{'msg':"please check the username and password entered"})
    # return render(request, "FPS/admin_index.html")

    # return redirect("adminlogin")
@login_required(login_url='adminlogin')
def franchiselist(request):
    # user = request.user
    # franchise = adminUser.objects.get(userid=user)
    # print(franchise)

    franchise_list = adminUser.objects.all()
    print(franchise_list)
    return render(request, "FPS/franchise_list.html", {'franchise_list': franchise_list})
def del_f(request,fid):
    user=User.objects.get(id=fid)
    user.delete()
    return redirect("franchiselist")
def del_u(request,idi):
    # return HttpResponse("hello")
    user = User.objects.get(id=idi)
    user.delete()
    return redirect("userlist")