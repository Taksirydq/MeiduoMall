import xadmin
from .models import User
from xadmin.plugins import auth


class UserAdmin(auth.UserAdmin):
    list_display = ['id', 'username', 'mobile', 'email', 'date_joined']
    readonly_fields = ['last_login', 'date_joined']
    search_fields = ('username', 'first_name', 'last_name', 'email', 'mobile')
    style_fields = {'user_permissions': 'm2m_transfer', 'groups': 'm2m_transfer'}

    # 重写添加表单，显示手机号、管理员选项
    def get_model_form(self, **kwargs):
        if self.org_obj is None:
            self.fields = ['username', 'mobile', 'is_staff']

        return super().get_model_form(**kwargs)


# 取消默认注册的用户类
xadmin.site.unregister(User)
# 自定义注册用户类
xadmin.site.register(User, UserAdmin)
