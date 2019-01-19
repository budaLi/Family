from django.shortcuts import render
from django.http.response import JsonResponse
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
def admin_login(request):
    if request.method=='GET':
        adminform=AdminLoginForm()
        # user=adminform['name']
        # pwd=adminform['pwd']
        return render(request,'admin/login.html',{'admin_form':adminform})
    if request.method=='POST':
        adminform=AdminLoginForm(request.POST)
        if adminform.is_valid():
            return render(request,"admin/index.html")

#查看用户信息
def user_list(request):
    userlist=F_User.objects.all()
    return render(request, 'user_list.html',{'userlist':userlist})


#查看该用户详细信息
def user_view(request):
    return render(request,'user_view.html')



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
def admin_index(request):
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
    user=F_User.objects.filter(id=2).first()
    rela=F_UserRelation.objects.filter(user_id=2).all()
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


