from django.db import models
from django.utils.translation import ugettext_lazy as _
import datetime

#用户信息报表
class F_User(models.Model):
    uniqueid=models.CharField(_('唯一ID'),max_length=200,unique=True)
    name=models.CharField(_('真实姓名'),max_length=50)
    nickname=models.CharField(_('昵称'),max_length=50)
    xingshi=models.CharField(_('姓氏'),max_length=20,default=name) #默认为姓名
    pwd=models.CharField(_('密码'),max_length=20)
    sex=models.CharField(_('性别'),choices=(('0',_('男')), ('1',_('女')), ('3',_('不详'))),default=_('男'),max_length=20)
    birthday=models.DateField(_('出生日期'),max_length=20)
    phone=models.CharField(_('手机号码'),max_length=20)
    email=models.CharField(_('邮箱'),max_length=30)
    image=models.CharField(_('头像'),max_length=200,default="")   #可以设置默认头像
    jiguan=models.CharField(_('籍贯'),max_length=200)
    register_time=models.DateTimeField(_('注册时间'),default=datetime.datetime.now)
    info=models.TextField(_('个人介绍'))

    def __str__(self):
        return self.name

    class Meta:
        verbose_name=_('用户信息')

#用户关系表
class F_UserRelation(models.Model):

    user_id=models.ForeignKey('F_User',on_delete=models.CASCADE)
    # other_user=models.IntegerField(_('个人'))
    relation=models.CharField(_('关系'),max_length=20)
    name=models.CharField(_('真实姓名'),max_length=50)
    nickname=models.CharField(_('昵称'),max_length=50,null=True,blank=True)
    xingshi=models.CharField(_('姓氏'),max_length=20,default=name,null=True,blank=True) #默认为姓名
    sex=models.CharField(_('性别'),choices=(('0',_('男')), ('1',_('女')), ('3',_('不详'))),default=_('男'),max_length=20)
    birthday=models.DateField(_('出生日期'),max_length=20,null=True,blank=True)
    phone=models.CharField(_('手机号码'),max_length=20,null=True,blank=True)
    email=models.CharField(_('邮箱'),max_length=30,null=True,blank=True)
    image=models.CharField(_('照片'),max_length=200,default="",null=True,blank=True)   #可以设置默认头像
    jiguan=models.CharField(_('籍贯'),max_length=200,null=True,blank=True)
    register_time=models.DateTimeField(_('注册时间'),default=datetime.datetime.now)
    story=models.TextField(_('事件'),null=True,blank=True)
    info=models.TextField(_('个人介绍'),null=True,blank=True)

    def __str__(self):
        return self.relation

    class Meta:
        verbose_name=_('关系')


#会员登陆日志
class F_UserLoginLog(models.Model):
    login_id=models.ForeignKey('F_User',on_delete=models.CASCADE)
    ip=models.CharField(_('登陆IP'),max_length=20)
    logintime=models.DateTimeField(_('登陆时间'),default=datetime.datetime.now)


#管理员信息表
class F_Admin(models.Model):

    uniqueid=models.CharField(_('ID'),max_length=200,unique=True,primary_key=True)
    role_id=models.ForeignKey('Role',on_delete=models.CASCADE)
    name=models.CharField(_('名称'),max_length=50)
    pwd=models.CharField(_('密码'),max_length=20)
    ip=models.CharField(_('ip'),max_length=100)
    register_time=models.DateTimeField(_('注册时间'),default=datetime.datetime.now)
    admin_login_log=models.ForeignKey('F_AdminLoginlog',on_delete=models.CASCADE)
    admin_op_log=models.ForeignKey('F_Admin_Oplog',on_delete=models.CASCADE)


    def __str__(self):
        return self.name

    class Meta:
        verbose_name=_('管理员信息')

#管理员登陆日志
class F_AdminLoginlog(models.Model):

    login_id=models.ForeignKey('F_Admin',on_delete=models.CASCADE)        #应该设置不是级联删除
    ip=models.CharField(_('登陆IP'),max_length=20)
    logintime=models.DateTimeField(_('登陆时间'),default=datetime.datetime.now)

    def __str__(self):
        return self.login_id

    class Meta:
        verbose_name=_('管理员登陆日志')


#管理员操作日志
class F_Admin_Oplog(models.Model):

    op_id=models.ForeignKey('F_Admin',on_delete=models.CASCADE)        #应该设置不是级联删除
    reason=models.CharField(_("操作原因"),max_length=200)
    optime=models.DateTimeField(_('操作时间'),default=datetime.datetime.now)
    ip=models.CharField(_('ip'),max_length=200)

    def __str__(self):
        return self.op_id

    class Meta:
        verbose_name=_('管理员操作日志')


#个人信息墙  可以用于寻亲等
class F_Userphote(models.Model):

    user_id=models.ForeignKey("F_User",on_delete=models.CASCADE)
    image_path=models.CharField(_('图片地址'),max_length=200)
    photo_info=models.CharField(_('图片介绍'),max_length=200)
    add_time=models.DateTimeField(_('添加时间'),default=datetime.datetime.now)
    vedio_path=models.CharField(_('视频地址'),max_length=200)
    vedio_info=models.CharField(_('视频介绍'),max_length=200)

    def __str__(self):
        return self.user_id

    class Meta:
        verbose_name=_('个人信息墙')


#用户操作记录 可以用于生成时间轴等
class F_UserOptionlog(models.Model):

    user_id=models.ForeignKey("F_User",on_delete=models.CASCADE)
    op_time=models.DateTimeField(_('操作时间'),default=datetime.datetime.now)
    reason=models.CharField(_('事件'),max_length=200)

#角色
class Role(models.Model):

    name=models.CharField(_('角色名称'),max_length=200)
    auths=models.CharField(_('权限列表'),max_length=200)
    addtime=models.DateTimeField(_('添加时间'),default=datetime.datetime.now)


    def __str__(self):
        return self.name

#权限表
class Auth(models.Model):

    # id=models.IntegerField(_('id'),primary_key=True)
    name=models.CharField(_('权限名称'),max_length=200)
    url=models.CharField(_('权限地址'),max_length=200)
    addtime=models.DateTimeField(_('添加时间'),default=datetime.datetime.now)

    def __str__(self):
        return self.url

