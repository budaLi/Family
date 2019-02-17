from django.shortcuts import render,redirect
from django.http.response import JsonResponse,HttpResponse
from app.models import F_User,F_UserRelation,F_Admin
from django.forms import ModelForm
from django.forms import widgets as wid


#管理员登陆表单
class AdminLoginForm(ModelForm):
    class Meta:
        model = F_Admin
        fields = ('name','pwd')      #字段，如果是__all__,就是表示列出所有的字段
        #exclude = ('uniqueid','register_time')          #排除的字段
        help_texts = None       #帮助提示信息
        widgets = {
            # 'username': wid.Input(attrs={'name':"user" ,'type':"text", 'class':"form-control" ,'placeholder':"请输入账号！"}),
            'pwd': wid.PasswordInput(attrs={}),
        }

#管理员登陆
def ad_login(request):
    if request.method=='GET':
        adminform=AdminLoginForm()
        # user=adminform['name']
        # pwd=adminform['pwd']
        return render(request,'admin_login.html',{'admin_form':adminform})
    else:
        adminform=AdminLoginForm(request.POST)
        if adminform.is_valid():
            return redirect('ad_index')
        return render(request,'admin_login.html',{'admin_form':adminform})

#查看用户信息
def user_list(request):
    userlist=F_User.objects.all()
    return render(request, 'user_list.html',{'userlist':userlist})



#查看该用户详细信息
def user_view(request,id):
    userinfo=F_User.objects.filter(pk=id).first()
    relation_user=F_UserRelation.objects.filter(user_id=id).all()
    other_lis=[]
    for one_user in relation_user:
        other_lis.append(F_User.objects.filter(pk=one_user.other_user).first())
    print(other_lis)
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
    return render(request,'')

def ad_index(request):
    return render(request,'admin_index.html')



def user_register(request):
    if request.method=='GET':
        userform=UserLoginForm()
        return render(request, 'admin_login.html', {'userform':userform})
    if request.method=='POST':
        userform=UserLoginForm(request.POST)
        if userform.is_valid():
            userform.save()
            return render(request, "admin_login.html", {'userform':userform})


def index(request):
    return render(request, "relationforce.html")

#此处应该是传入登陆者id 获取其家谱
def relation(request):
    user=F_User.objects.filter(id=1).first()
    rela=F_UserRelation.objects.filter(user_id=1).all()
    dic={}
    if user and rela:
        node=[{ "name": user.name, "image" : user.image }]
        edges=[]
        for i,one in enumerate(rela):
            tem=F_User.objects.filter(uniqueid=one.other_user).first()
            node.append({"name": tem.name, "image" : tem.image })
            edges.append({ "source": 0 , "target": i+1 , "relation":one.relation })

            dic={
                    "nodes":node,
                    "edges":edges,
            }
    return JsonResponse(dic)

#获取从前端传来得个人族谱信息数据
def makefamilytree(request):
    data=request.POST['data']

def editperson(request):
    for one in request.POST:
        print(one)
    return HttpResponse(request.POST)

#族谱
def tree(request):
    return render(request,'tree.html')

#操作日志列表
def oplog_list(request):
    return render(request,'oplog_list.html')

#管理员登陆日志
def adminloginlog_list(request):
    return render(request,'adminloginlog_list.html')

#会员登陆日志
def userloginlog_list(request):
    return render(request,'userloginlog_list.html')

#添加权限
def auth_add(request):
    return render(request,'auth_add.html')

#权限列表
def auth_list(request):
    return render(request,'auth_list.html')

#添加角色
def role_add(request):
    return render(request,'role_add.html')

#角色列表
def role_list(request):
    return render(request,'role_list.html')

#添加管理员
def admin_add(request):
    return render(request,'admin_add.html')

#管理员列表
def admin_list(request):
    return render(request,'admin_list.html')

