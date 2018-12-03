
from django.shortcuts import render
from django.contrib.auth.models import User
from django.http import HttpResponse, HttpResponseRedirect
from django.http import JsonResponse
from django.contrib.auth import authenticate
from django.contrib.auth import login, get_user, logout
from django.contrib.admin.views.decorators import staff_member_required
from django.contrib.auth.decorators import login_required


def adminLogin(request):
    if request.method == 'POST':

        username = request.POST['username']
        password = request.POST['password']

        user = authenticate(username=username, password=password)

        if user:
            if user.is_active and user.is_staff:
                login(request, user)
                return HttpResponseRedirect('User/')
            else:
                # return render(request, 'admin/login.html', {'error': "Your count is not for admin Page."})
                login(request, user)
                return HttpResponseRedirect('User/')
        else:
            return render(request, 'admin/login.html', {'error': "Invalid login details supplied."})
    else:
        return render(request, 'admin/login.html', {})

def adminLogout(request):
    logout(request)
    return HttpResponseRedirect('/admin/logout')

@staff_member_required
def adminIndex(request):
    return render(request, 'admin/index.html')

def index(request):
    user = get_user(request)
    if user.is_staff:
        return HttpResponseRedirect('customer/')
    else:
        return render(request, 'admin/login.html')

@staff_member_required
def customerIndex(request):
    return render(request, 'admin/customer.html')

@staff_member_required
def customerEditPage(request, user_id):
    user = User.objects.get(pk=user_id)
    return render(request, 'admin/customerEdit.html', {'customer': user})

@staff_member_required
def customerEdit(request, user_id):
    username = request.POST['username']
    first_name = request.POST['firstName']
    last_name = request.POST['lastName']
    email = request.POST['email']
    adminUser = User.objects.filter(pk=user_id).update(
        username=username,
        first_name=first_name,
        last_name=last_name,
        email=email
    )
    return HttpResponseRedirect('/')

@login_required
def adminUserIndex(request, admin_id):
    adminUser = User.objects.get(pk=admin_id)
    return render(request, 'admin/adminUser.html', {'adminUser': adminUser})

@login_required()
def adminUserEdit(request):
    name = request.POST['username']
    first_name = request.POST['firstName']
    last_name = request.POST['lastName']
    email = request.POST['email']
    oldPassword = request.POST['old_password']
    newPassword = request.POST['new_password']
    confirmPassword = request.POST['confirm_password']

    user = get_user(request)

    if (oldPassword == '') and (newPassword == '') and (confirmPassword == ''):
        adminUser = User.objects.filter(pk=user.id).update(
            username=name,
            first_name=first_name,
            last_name=last_name,
            email=email
        )
        logout(request)
        return HttpResponseRedirect('/admin/logout')
    else:
        username = user.username

        Guser = authenticate(username=username, password=oldPassword)

        if Guser:
            if newPassword == confirmPassword:
                user.set_password(confirmPassword)
                user.save()

                User.objects.filter(pk=user.id).update(
                    username=name,
                    first_name=first_name,
                    last_name=last_name,
                    email=email
                )

                logout(request)
                return HttpResponseRedirect('/admin/logout')
            else:
                return render(request, 'admin/adminUser.html', {
                    'confirm_password_error': "Input the confirm password correctly.",
                    'old_password': oldPassword,
                    'new_password': newPassword,
                    'adminUser': user
                })
        else:
            return render(request, 'admin/adminUser.html',
                          {'old_password_error': "Invalid Old Password details supplied.",
                           'adminUser': user})

@staff_member_required
def AjaxTable(request):
    staff = request.GET['staff']
    customers = User.objects.filter(is_staff=staff).values('id', 'username', 'email', 'first_name', 'last_name', 'is_active')
    response_data = {}
    response_data['data'] = [customer for customer in customers]
    return JsonResponse(response_data)

@staff_member_required
def addNew(request):
    return render(request, 'admin/addNew.html')

@staff_member_required
def addUser(request):
    username = request.POST['username']
    first_name = request.POST['firstName']
    last_name = request.POST['lastName']
    email = request.POST['email']
    password = request.POST['password']
    re_password = request.POST['re_password']

    if password == re_password:
        user = User(username=username, first_name=first_name, last_name=last_name, email=email)
        user.set_password(password)
        user.save()

    return HttpResponseRedirect('/')

@staff_member_required
def UserDelete(request):
    del_ids = request.GET.getlist('data[]')

    for del_id in del_ids:
        User.objects.filter(id=int(del_id)).delete()
    return HttpResponse("success")

@staff_member_required
def UserStatus(request):
    userid = request.GET.get('userid')
    userStatus = request.GET.get('userStatus')

    if userStatus == 'true':
        User.objects.filter(id=int(userid)).update(is_active=0)
    else:
        User.objects.filter(id=int(userid)).update(is_active=1)

    return HttpResponse("success")

@login_required
def GUserIndex(request):
    return render(request, 'admin/user.html')
