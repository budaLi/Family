from django.shortcuts import render,redirect
from django.http.response import JsonResponse,HttpResponse
from app.models import F_User,F_UserRelation,F_Admin,Role,Auth,F_Admin_Oplog,F_UserOptionlog,F_AdminLoginlog,F_UserLoginLog
from django.forms import ModelForm
from django.forms import widgets as wid
from functools import wraps
from django.core.mail import send_mail,send_mass_mail
import json

sessin={}
#登陆装饰器
def admin_login_req(f):
    @wraps(f)
    def decorted(*args,**kwargs):
        if 'admin' not in sessin:
            return redirect('ad_login')
    return decorted

#权限装饰器
def admin_auth(f):
    @wraps(f)
    def decorted(*args,**kwargs):
        request=args[0]  #反向解析url
        authslist=[]
        url=request.path #当前url  /path/
        admin=F_Admin.objects.filter(name=sessin[0]).first()
        auths=Auth.objects.all()
        for one in auths:
            authslist.append(one.url)   #权限列表中  /xxx/,/xxx/这种形式
        if admin:
            role=Role.objects.filter(pk=admin.role_id.id).first()
            tem=role.auths.split(',')
            if url not in tem:
                return render(request,'admin404.html')
        return f(*args,**kwargs)
    return decorted

#管理员登陆表单
class AdminLoginForm(ModelForm):
    class Meta:
        model = F_Admin
        fields = ('name','pwd')      #字段，如果是__all__,就是表示列出所有的字段
        #exclude = ('uniqueid','register_time')          #排除的字段
        help_texts = None       #帮助提示信息
        # widgets = {
        #     # 'username': wid.Input(attrs={'name':"user" ,'type':"text", 'class':"form-control" ,'placeholder':"请输入账号！"}),
        #     'pwd': wid.PasswordInput(attrs={}),
        # }

#管理员登陆
def admin_login(request):
    if request.method=='GET':
        adminform=AdminLoginForm()
        # user=adminform['name']
        # pwd=adminform['pwd']
        return render(request,'admin_login.html',{'admin_form':adminform})
    else:
        adminform=AdminLoginForm(request.POST)
        if adminform.is_valid():
            admin=F_Admin.objects.filter(name=request.POST['name']).first()
            if admin and admin.pwd==request.POST['pwd']:
                sessin['admin']=request.POST['name']
                return redirect('ad_index')
            else:
                return render(request,'admin_login.html',{'admin_form':adminform})
        return render(request,'admin_login.html',{'admin_form':adminform})


#管理员退出登陆
def admin_logout(request):
    sessin.clear()
    return redirect('ad_login')


#查看用户信息
# @admin_auth
def user_list(request):
    userlist=F_User.objects.all()
    return render(request, 'user_list.html',{'userlist':userlist})



#查看该用户详细信息
def user_view(request,id):
    userinfo=F_User.objects.filter(pk=id).first()
    relation_user=F_UserRelation.objects.filter(user_id=id).all()
    other_lis=[]

    for one_user in relation_user:
        other_lis.append(F_UserRelation.objects.filter(user_id=one_user.user_id).first())
    return render(request,'user_view.html',{'userinfo':userinfo,'other_lis':other_lis})



#用户注册表单
class UserLoginForm(ModelForm):
    class Meta:
        model = F_User  #对应的Model中的类
        fields = ('uniqueid','register_time')      #字段，如果是__all__,就是表示列出所有的字段
        #exclude = ('uniqueid','register_time')          #排除的字段
        help_texts = None       #帮助提示信息

#用户登陆
def user_login(request):
    if request.method=='GET':
        return render(request,'user_loin.html')
    if request.method=='POST':
        user=F_User.objects.filter(email=request.POST['user_name']).first()
        if user and user.pwd==request.POST['password']:
            return redirect('/user_index/'+str(user.id))
        return render(request,'user_loin.html')


#用户家庭信息
def user_index(request,id):
    userlist=F_User.objects.filter(pk=id).all()
    return render(request, 'user_index.html',{'userlist':userlist,'id':id})



# @admin_auth
# @admin_login_req
# 管理员主页
def ad_index(request):
    admin=F_Admin.objects.filter(name=sessin['admin']).first()
    return render(request,'admin_index.html',{'admin':sessin['admin'],'id':admin.uniqueid})


# 用户注册
def user_register(request):
    if request.method=='GET':
        userform=UserLoginForm()
        return render(request, 'admin_login.html', {'userform':userform})
    if request.method=='POST':
        userform=UserLoginForm(request.POST)
        if userform.is_valid():
            userform.save()
            return render(request, "admin_login.html", {'userform':userform})

# 关系图
def index(request,id):
    return render(request, "relationforce.html",{'id':id})


#此处应该是传入登陆者id 获取其家谱
def relation(request,id):
    user=F_User.objects.filter(pk=id).first()
    rela=F_UserRelation.objects.filter(user_id_id=id).all()
    dic={}
    if user and rela:
        node=[{ "name": user.name, "image" : user.image }]
        edges=[]
        for i,one in enumerate(rela):
            # tem=F_User.objects.filter(uniqueid=one.user_id_id).first()
            node.append({"name": one.name, "image" : one.image })
            edges.append({ "source": 0 , "target": i+1 , "relation":one.relation })

            dic={
                    "nodes":node,
                    "edges":edges,
            }
    return JsonResponse(dic)

#获取从前端传来得个人族谱信息数据
def makefamilytree(request):
    data=request.POST['data']

#族谱
def tree(request):
    if request.method == 'GET':
        personform=UserRelaForm()
        return render(request,'tree.html',{'personform':personform})
    if request.method == 'POST':
        personform=UserRelaForm(request.POST)
        if personform.is_valid():
            personform.save()
            return redirect('tree',{'sucess':'编辑信息成功'})
        else:
            personform=UserRelaForm()
            return render(request,'tree.html',{'personform':personform,'errors':personform.errors})

#操作日志列表
def oplog_list(request):
    oploglist=F_Admin_Oplog.objects.all()
    return render(request,'oplog_list.html',{'oploglist':oploglist})

#管理员登陆日志
def adminloginlog_list(request):
    adminloginloglist=F_AdminLoginlog.objects.all()
    return render(request,'adminloginlog_list.html',{'adminloginloglist':adminloginloglist})

#会员登陆日志
def userloginlog_list(request):
    userloginloglist=F_UserLoginLog.objects.all()
    return render(request,'userloginlog_list.html',{'userloginloglist':userloginloglist})

#权限表单
class AuthForm(ModelForm):
    class Meta:
        model = Auth  #对应的Model中的类
        fields = '__all__'      #字段，如果是__all__,就是表示列出所有的字段
        exclude = ('id','addtime')          #排除的字段
        help_texts = None       #帮助提示信息

#添加权限
def auth_add(request):
    if request.method == 'GET':
        authform=AuthForm()
        return render(request,'auth_add.html',{'authform':authform})
    if request.method == 'POST':
        authform=AuthForm(request.POST)
        if authform.is_valid():
            authform.save()
            return redirect('auth_list')
        else:
            return render(request,'auth_add.html',{'error':authform.errors})

#权限列表
def auth_list(request):
    authlist=Auth.objects.all()
    return render(request,'auth_list.html',{'authlist':authlist})

# 编辑权限
def auth_edit(request,id):
    auth=Auth.objects.filter(pk=id).first()
    if request.method == 'GET':
        authform=AuthForm(instance=auth)
        return render(request,'auth_edit.html',{'authform':authform})
    if request.method == 'POST':
        authform=AuthForm(request.POST,instance=auth)
        if authform.is_valid():
            authform.save()
            return redirect('auth_list')
        else:
            return render(request,'auth_edit.html',{'authform':authform,'errors':authform.errors})

# 删除权限
def auth_del(request,id):
    auth=Auth.objects.filter(pk=id).first()
    auth.delete()
    return redirect('auth_list')

#角色表单
class RoleForm(ModelForm):
    class Meta:
        model = Role  #对应的Model中的类
        fields = '__all__'      #字段，如果是__all__,就是表示列出所有的字段
        exclude = ('addtime','auths')          #排除的字段
        help_texts = None       #帮助提示信息
        widgets = {
            'name': wid.Input(attrs={'name':"user" ,'type':"text", 'class':"form-control" ,'placeholder':"请输入角色名称！"}),
            # 'auths': wid.Input(attrs={'type':"checkbox",'choices':((i,v.name) for i,v in enumerate(Auth.objects.all()))}),
        }

#添加角色
def role_add(request):
    if request.method == 'GET':
        roleform=RoleForm()
        rolename=roleform['name']
        auths=Auth.objects.all()
        return render(request,'role_add.html',{'rolename':rolename,'auths':auths})
    if request.method == 'POST':
        roleform=RoleForm(request.POST)
        if roleform.is_valid():
            instance=roleform.save(commit=False)
            tem=request.POST.getlist('input_url')
            instance.auths=','.join(tem)
            roleform.save()
            return redirect('role_list')
        else:
            roleform=RoleForm()
            rolename=roleform['name']
            auths=Auth.objects.all()
            return render(request,'role_add.html',{'rolename':rolename,'auths':auths,'error':roleform.errors})


#角色列表
def role_list(request):
    rolelist=Role.objects.all()
    return render(request,'role_list.html',{'rolelist':rolelist})

# 编辑角色
def role_edit(request,id):
    role=Role.objects.filter(pk=id).first()

    if request.method == 'GET':
        roleform=RoleForm(instance=role)
        rolename=roleform['name']
        authlist=[]   #已有权限
        allauths=[]
        tem=role.auths.split(',')
        ss=Auth.objects.all()
        for one in ss:
            allauths.append(one)
        for one in tem:   #已有权限
            authlist.append(Auth.objects.filter(url=one).first())
        for one in allauths:
            if one in authlist:
                allauths.remove(one)
        return render(request,'role_edit.html',{'rolename':rolename,'auths':authlist,'emptyauth':allauths})
    if request.method == 'POST':
        roleform=RoleForm(request.POST,instance=role)
        print(roleform)
        if roleform.is_valid():
            instance=roleform.save(commit=False)
            tem=request.POST.getlist('input_url')
            instance.auths=','.join(tem)
            roleform.save()
            return redirect('role_list')
        else:
            return render(request,'role_edit.html',{'roleform':roleform,'errors':roleform.errors})

# 删除角色
def role_del(request,id):
    role=Role.objects.filter(pk=id).first()
    role.delete()
    return redirect('role_list')

class AdminaddForm(ModelForm):
    class Meta:
        model = F_Admin  #对应的Model中的类
        fields = ('name','pwd','role_id')
        #exclude = ('uniqueid','register_time')
        help_texts = None       #帮助提示信息

#添加管理员
def admin_add(request):
    return render(request,'admin_add.html')
    # if request.method == 'GET':
    #     adminform=AdminaddForm()
    #     return render(request,'auth_add.html',{'adminform':adminform})
    # if request.method == 'POST':
    #     adminform=AdminaddForm(request.POST)
    #     if adminform.is_valid():
    #         adminform.save()
    #         return redirect('admin_list')
    #     else:
    #         return render(request,'admin_add.html',{'error':adminform.errors})

# 管理员修改密码
def admin_cgpwd(request,id):
    if request.method == 'GET':
        return render(request,'ad_changepwd.html')

    if not sessin['admin']:
        return redirect('admin_login')
    admin=F_Admin.objects.filter(name=sessin['admin']).first()
    if request.POST['input_pwd'] == admin.pwd:
        admin.pwd=request.POST['input_newpwd']
        admin.save()
        return redirect('admin_list')
    return render(request, 'ad_changepwd.html')

#管理员列表
def admin_list(request):
    adminlist=F_Admin.objects.all()
    return render(request,'admin_list.html',{'adminlist':adminlist})

#用户关系表单
class UserRelaForm(ModelForm):
    class Meta:
        model = F_UserRelation
        fields = '__all__'     #字段，如果是__all__,就是表示列出所有的字段
        exclude = ('user_id','register_time')          #排除的字段
        help_texts = None       #帮助提示信息

#编辑会员关联的人物信息
def editperson(request):
    if request.method == 'GET':
        personform=UserRelaForm()
        return render(request,'tree.html',{'personform':personform})
    if request.method == 'POST':
        personform=UserRelaForm(request.POST)
        if personform.is_valid():
            personform.save()
            return redirect('tree',{'sucess':'编辑信息成功'})
        else:
            personform=UserRelaForm()
            return render(request,'tree.html',{'personform':personform,'errors':personform.errors})




# 会员关系图
def user_relations(request,id):
    return render(request,'user_relations.html',{'id':id})


# 用户族谱
def user_tree(request):
    return render(request,'user_tree.html')

# 照片墙
def imageswall(request):
    return render(request,'imageswal.html')

# 视频墙
def vediowall(request):
    return render(request,'vediowall.html')

# 邮箱发送功能
def sendemail(request,from_email,to_email):
    from Family.settings import DEFAULT_FROM_EMAIL
    email_title = "您的家人 %s 邀请注册"%(from_email)
    email_body = "请点击 http://127.0.0.1:8000/register/  注册  如果认为被骚扰请无视"
    send_status = send_mail(email_title, email_body, DEFAULT_FROM_EMAIL, [to_email])
    user=F_UserRelation.objects.filter(email=to_email).first()
    if user:
        user.is_yaoqin='已邀请'
        user.save()
    return redirect('/user_view/'+str(user.user_id.id))


# 冻结/解冻 用户  返回user_list
def freeze_or_unfreeze_user(request,id):
    user=F_User.objects.filter(pk=id).first()
    if user.state=='正常':
        user.state='冻结'
    else:
        user.state='正常'
    user.save()
    print(user.state)
    return redirect('user_list')

# 冻结/解冻可能存在的用户  返回user_view
def freeze_or_unfreeze_users(request,id):
    user=F_UserRelation.objects.filter(pk=id).first()
    if user.state=='正常':
        user.state='冻结'
    else:
        user.state='正常'
    user.save()
    return redirect('/user_view/'+str(user.user_id.id))


# 删除关联用户  未注册状态下
def del_user(request,id):
    user=F_UserRelation.objects.filter(pk=id).first()
    tem=user.user_id.id
    user.delete()
    return redirect('/user_view/'+str(tem))


def write(request):
    print(request.body)
    data=json.loads(request.body)
    res={
        'success':True
    }
    return HttpResponse(json.dumps(res),content_type='application/json')


def save(request):
    data=request.POST
    print(type(data))
    for key,value in data.items():
        print(key,'value:'+value)
    res={
        'success':True
    }
    return HttpResponse(json.dumps(res),content_type='application/json')


def articlelist(request):
    return render(request,'user_loin.html')