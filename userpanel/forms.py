
from django import forms
from .models import AddOns, ImageUploader, Projects, Menu, SitePages, SupportPlans, UserStorage, UserSupport
from captcha.fields import ReCaptchaField
from captcha.widgets import ReCaptchaV2Invisible, ReCaptchaV2Checkbox
from django.forms.models import inlineformset_factory


class ProjectUpdateForm(forms.ModelForm):
    captcha = ReCaptchaField(widget=ReCaptchaV2Invisible)

    class Meta:
        model = Projects
        fields = ['user_id', 'is_active', 'project_name', 'captcha']


class ProjectCreateForm(forms.ModelForm):
    captcha = ReCaptchaField(widget=ReCaptchaV2Invisible)

    class Meta:
        model = Projects
        fields = ['project_name', 'project_category',
                  'site_category', 'add_languages', ]


class ContentUpdateForm(forms.ModelForm):
    captcha = ReCaptchaField(widget=ReCaptchaV2Invisible)

    class Meta:
        model = Projects
        fields = ['content', 'content_upload',]




class PictureUpdateForm(forms.ModelForm):
    captcha = ReCaptchaField(widget=ReCaptchaV2Invisible)

    class Meta:
        model = ImageUploader
        fields = '__all__'


class MenuForm(forms.ModelForm):

    class Meta:
        model = Menu
        fields = ('title',)


MenuFormSet = inlineformset_factory(
    Projects,
    Menu,
    form=MenuForm,
    min_num=1,  # minimum number of forms that must be filled in
    extra=3,  # number of empty forms to display
    can_delete=False  # show a checkbox in each form to delete the row
)


class SitePagesForm(forms.ModelForm):

    class Meta:
        model = SitePages
        fields = ('title',)


MenuFormSet = inlineformset_factory(
    Projects,
    SitePages,
    form=SitePagesForm,
    min_num=1,  # minimum number of forms that must be filled in
    extra=3,  # number of empty forms to display
    can_delete=False  # show a checkbox in each form to delete the row
)


class ProjectAddonForm(forms.ModelForm):
    captcha = ReCaptchaField(widget=ReCaptchaV2Invisible)
    class Meta:
        model = AddOns
        fields = ('__all__')

