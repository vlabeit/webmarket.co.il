from django.urls import reverse_lazy

from oscar.apps.catalogue.models import Product
from .models import Projects, SecurityProducts, UserSecurity, UserStorage, UserSupport
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseForbidden, HttpResponseRedirect
#from django.core.exceptions import PermissionDenied
from django.http.response import HttpResponse, HttpResponseNotAllowed
from django.shortcuts import get_object_or_404, redirect, render
from .forms import ContentUpdateForm, MenuForm, PictureUpdateForm, ProjectCreateForm, ProjectUpdateForm
from .models import Projects, Menu
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from oscar.apps.order.models import Line as LineProduct
from oscar.apps.order.models import Order as OrderProduct


from .models import ImageUploader
from django.contrib import messages
from datetime import datetime

@login_required
def index(request):
    
    support = UserSupport.objects.filter(user_id=request.user, is_active=True)
    storage = UserStorage.objects.filter(user_id=request.user, is_active=True)
    sublist = [*support, *storage]


    context = {
        'user': request.user,
        'projects': Projects.objects.filter(user_id=request.user).order_by('-pk'),
        'subslist': sublist

    }
    return render(request, 'userpanel/index.html', context)


def list(request):
    return render(request, 'userpanel/list.html')


def newproject(request):
    #Employees.objects.values_list('eng_name', flat=True)
    try:
        project = Projects.objects.filter(
            user_id=request.user).values_list('id', flat=True)
    except TypeError:
        return HttpResponseForbidden("You are not logged in")

    context = {'project': project}
    return render(request, 'userpanel/newproject.html', context)


def blogtest(request):
    return render(request, 'userpanel/blogtest.html')

# Project views

# Changing the template detaults attributes
class ProjectListView(LoginRequiredMixin, UserPassesTestMixin, ListView):
    model = Projects
    template_name = 'userpanel/projects.html'  # <app>/<model>_<viewtype>.html
    context_object_name = 'projects'
    ordering = ['-date_started']
    paginate_by = 10

    def test_func(self):
        user = self.request.user
        return Projects.objects.filter(user_email=user)

    def get_queryset(self):
        user = self.request.user
        return Projects.objects.filter(user_id=user).order_by('-pk')


# NOT changing the template detaults attributes
class ProjectDetailView(LoginRequiredMixin, UserPassesTestMixin, DetailView):
    model = Projects
    context_object_name = 'projects'

    def test_func(self):
        project = self.get_object()
        if str(self.request.user) == str(project.user_id):
            return True
        return False

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['fields'] = [
            field.name for field in Projects._meta.get_fields()]
        context['proj_cats'] = (
            'accepted', 'work', 'waiting', 'review', 'complete',)
        return context


class ProjectCreateView(LoginRequiredMixin, CreateView):
    model = Projects
    template_name = 'userpanel/newproject.html'
    form_class = ProjectCreateForm

    def form_valid(self, form):
        form.instance.user_id = self.request.user
        return super().form_valid(form)

    def test_func(self):
        user = self.request.user
        return Projects.objects.filter(user_email=user)
    
    def get_success_url(self):
        return reverse_lazy('users:userpanel:project-detail', kwargs={'pk': self.object.pk}) #, kwargs={'pk': self.object.pk}


class ProjectUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Projects

    readonly_fields = ('user_id')
    form_class = ProjectUpdateForm
    #success_url = '/'

    def form_valid(self, form):
        form.instance.user_id = self.request.user
        return super().form_valid(form)

    def test_func(self):
        project = self.get_object()
        if str(self.request.user) == str(project.user_id):
            return True
        return False


class ProjectDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Projects
    fields = ['title', 'date_started']
    success_url = '/'

    def form_valid(self, form):
        form.instance.user_id = self.request.user
        return super().form_valid(form)

    def test_func(self):
        project = self.get_object()
        if str(self.request.user) == str(project.user_id):
            return True
        return False


# Project Menus
@login_required
def create_menu(request, project):
    project = Projects.objects.get(id=project)
    print(project.pk)
    menus = Menu.objects.filter(project=project.pk)
    form = MenuForm(request.POST or None)

    if str(request.user) == str(project.user_id):

        if request.method == "POST":
            if form.is_valid():
                menu = form.save(commit=False)
                menu.project = project
                menu.save()
                return redirect("users:userpanel:detail-menu", pk=menu.id)
            else:
                return render(request, "userpanel/menu_form.html", context={
                    "form": form
                })

        context = {
            "form": form,
            "project": project,
            "menus": menus
        }

        return render(request, "userpanel/create_menu.html", context)
    else:
        return HttpResponseForbidden("Sorry, you have no permission to create this menu.")
        #raise PermissionDenied("Custom message")


def update_menu(request, pk):

    menu = Menu.objects.get(id=pk)
    form = MenuForm(request.POST or None, instance=menu)

    if str(request.user) == str(menu.project.user_id):

        if request.method == "POST":
            if form.is_valid():
                form.save()
                return redirect("users:userpanel:detail-menu", pk=menu.id)

        context = {
            "form": form,
            "menu": menu
        }

        return render(request, "userpanel/menu_form.html", context)
    else:
        return HttpResponseForbidden("Sorry, you have no permission to edit this menu.")


def delete_menu(request, pk):
    menu = get_object_or_404(Menu, id=pk)

    if request.method == "POST":
        menu.delete()
        return HttpResponse("")

    return HttpResponseNotAllowed(
        [
            "POST",
        ]
    )


@login_required
def detail_menu(request, pk):
    menu = get_object_or_404(Menu, id=pk)
    if str(request.user) == str(menu.project.user_id):
        context = {
            "menu": menu
        }
        return render(request, "userpanel/menu_detail.html", context)
    else:
        return HttpResponseForbidden("Sorry, you have no permission to view this menu.")

def create_menu_form(request):
    form = MenuForm(request.POST or None)
    context = {
        "form": form
    }
    return render(request, "userpanel/menu_form.html", context)


class ContentUpdateView(LoginRequiredMixin, UserPassesTestMixin, CreateView, UpdateView):
    model = Projects
    readonly_fields = ('user_id')
    template_name = 'userpanel/project_content.html'
    form_class = ContentUpdateForm

    def form_valid(self, form):
        form.instance.user_id = self.request.user
        return super().form_valid(form)

    def test_func(self):
        project = self.get_object()
        if str(self.request.user) == str(project.user_id):
            return True
        return False

    def picupload(request):
        if request.method == "POST" and 'upload' in request.POST:
                img_name = 'img_name' in request.POST and request.POST['img_name']
                img = 'img' in request.FILES and request.FILES['img']
                u_profile = 'u_profile' in request.POST and request.POST['u_profile']
                img_uploader = ImageUploader(image_name = img_name,
                                                image = img,
                                                user=request.user,
                                                user_profile = u_profile,
                                                date=datetime.now())
                img_uploader.save()
                messages.success(request,'Your Image Uploaded Successfully !!')

        images = ImageUploader.objects.filter(user=request.user)
        return render(request,'userpanel/picture-upload.html',{'images':images})

    def deletePic(request, pk):
            pic = ImageUploader.objects.filter(id=pk)
            pic.delete()
            messages.success(request, "Picture deleted succesfuly")
            return redirect('/dashboard/picture-upload')

    def get_context_data(self, **kwargs):
        context = super(ContentUpdateView,self).get_context_data(**kwargs)
        project = get_object_or_404(Projects.objects, id=int(self.kwargs['pk']))
        images = ImageUploader.objects.filter(user=self.request.user)

        context['projects'] = Projects.objects.get(id=project.id)
        context['form2'] = PictureUpdateForm()
        context['images'] = images
        return context

class AddonsListView(LoginRequiredMixin, UserPassesTestMixin, ListView):
    template_name = 'userpanel/project-addons.html' 
    context_object_name = 'projectaddons'
    
    paginate_by = 10
    
    def test_func(self):
        return OrderProduct.objects.all()

    def get_queryset(self):
        user = self.request.user
        return Product.objects.filter(line__order__user=user)

    def get_context_data(self, **kwargs):
        user = self.request.user
        context = super(AddonsListView,self).get_context_data(**kwargs)
        project = get_object_or_404(Projects.objects, id=int(self.kwargs['pk']))
        images = ImageUploader.objects.filter(user=self.request.user)
        # context['products'] = Product.objects.filter(line__order__user=user).distinct() 
        context['addon_name'] = LineProduct.objects.filter(product__line__product='1')
        context['projects'] = Projects.objects.get(id=project.id)
        context['proj_cats'] = (
            'accepted', 'work', 'waiting', 'review', 'complete',)
        context['images'] = images
        return context


# @login_required
# def picupload(request):
#         if request.method == "POST" and 'upload' in request.POST:
#                 img_name = 'img_name' in request.POST and request.POST['img_name']
#                 img = 'img' in request.FILES and request.FILES['img']
#                 u_profile = 'u_profile' in request.POST and request.POST['u_profile']


#                 img_uploader = ImageUploader(image_name = img_name,
#                                                 image = img,
#                                                 user=request.user,
#                                                 user_profile = u_profile,
#                                                 date=datetime.now())
#                 img_uploader.save()
#                 messages.success(request,'Your Image Uploaded Successfully !!')


#         images = ImageUploader.objects.filter(user=request.user)
#         return render(request,'userpanel/project_content.html',{'images':images})

# def deletePic(request, pk):
#         pic = ImageUploader.objects.filter(id=pk)
#         pic.delete()
#         messages.success(request, "Picture deleted succesfuly")
#         return redirect('/dashboard/picture-upload')

class SupportCreate(LoginRequiredMixin, CreateView): #UserPassesTestMixin, - to add after linking to spesific project.
    model = UserSupport
    template_name = 'userpanel/project-support.html' 
    context_object_name = 'supports'
    fields = ['plan', 'period',]

    def test_func(self):
        user = self.request.user
        return UserSupport.objects.filter(user_id=user)
  
    def get_success_url(self):
        return reverse_lazy('users:userpanel:support-create') #, kwargs={'pk': self.object.pk

    def form_valid(self, form):
        form.instance.user_id = self.request.user
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super(SupportCreate,self).get_context_data(**kwargs)
        user = self.request.user
        context['support_list'] = UserSupport.objects.filter(user_id=user)
        return context


class SupportDetail(LoginRequiredMixin, UserPassesTestMixin, DetailView):
    model = UserSupport
    template_name = 'userpanel/support-details.html' 

    def test_func(self):
        user = self.request.user
        return UserSupport.objects.filter(user_id=user)

class SupportChange(LoginRequiredMixin, UserPassesTestMixin, CreateView):
    model = UserSupport
    template_name = 'userpanel/support-change.html' 
    fields = ['plan', 'period',]

    def test_func(self):
        user = self.request.user
        return UserSupport.objects.filter(user_id=user)

    def form_valid(self, form):
        form.instance.user_id = self.request.user
        return super().form_valid(form) 
    
    def get_context_data(self, **kwargs):
        context = super(SupportChange,self).get_context_data(**kwargs)
        user = self.request.user
        context['support_list'] = UserSupport.objects.get(user_id=user, is_active=True)
        return context

    def get_success_url(self):
        return reverse_lazy('users:userpanel:support-create') #,kwargs={'pk': self.object.pk}

class StorageUpdate(LoginRequiredMixin, UserPassesTestMixin, CreateView):
    pass


class StorageCreate(LoginRequiredMixin, CreateView): #UserPassesTestMixin, - to add after linking to spesific project.
    model = UserStorage
    template_name = 'userpanel/project-storage.html' 
    context_object_name = 'storages'
    fields = ['plan', 'period',]

    def test_func(self):
        user = self.request.user
        return UserStorage.objects.filter(user_id=user)
  
    def get_success_url(self):
        return reverse_lazy('users:userpanel:storage-create') #, kwargs={'pk': self.object.pk

    def form_valid(self, form):
        form.instance.user_id = self.request.user
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super(StorageCreate,self).get_context_data(**kwargs)
        user = self.request.user
        context['storage_list'] = UserStorage.objects.filter(user_id=user)
        return context


class StorageDetail(LoginRequiredMixin, UserPassesTestMixin, DetailView):
    model = UserStorage
    template_name = 'userpanel/storage-details.html'

    def test_func(self):
        user = self.request.user
        return UserStorage.objects.filter(user_id=user)

class StorageChange(LoginRequiredMixin, UserPassesTestMixin, CreateView):
    model = UserStorage
    template_name = 'userpanel/storage-change.html' 
    fields = ['plan', 'period',]

    def test_func(self):
        user = self.request.user
        return UserStorage.objects.filter(user_id=user)

    def form_valid(self, form):
        form.instance.user_id = self.request.user
        return super().form_valid(form) 
    
    def get_context_data(self, **kwargs):
        context = super(StorageChange,self).get_context_data(**kwargs)
        user = self.request.user
        context['storage_list'] = UserStorage.objects.get(user_id=user, is_active=True)
        return context

    def get_success_url(self):
        return reverse_lazy('users:userpanel:storage-create') #, kwargs={'pk': self.object.pk

class SecurityCreate(LoginRequiredMixin, CreateView): #UserPassesTestMixin
    model = UserSecurity
    template_name = 'userpanel/project-security.html' 
    context_object_name = 'secu'
    fields = ['plan',]

    # def test_func(self):
    #     user = self.request.user
    #     return True
    # def test_func(self):
    #     user = self.request.user
    #     return UserSecurity.objects.filter(user_id=user)
  
    def get_success_url(self):
        return reverse_lazy('users:userpanel:security-create') #, kwargs={'pk': self.object.pk}

    def form_valid(self, form):
        form.instance.user_id = self.request.user
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super(SecurityCreate,self).get_context_data(**kwargs)
        user = self.request.user
        context['secu_list'] = UserSecurity.objects.filter(user_id=user)
        context['secu_prods'] = SecurityProducts.objects.all()
        return context


class ServiceSubscribeListView(LoginRequiredMixin, ListView): #, UserPassesTestMixin
    model = UserStorage
    template_name = 'userpanel/services-subscribes.html'  # <app>/<model>_<viewtype>.html
    context_object_name = 'storagesubs'
    ordering = ['-id']
    paginate_by = 10

    def test_func(self):
        user = self.request.user
        return UserStorage.objects.filter(user_id=user)

    def get_queryset(self):
        user = self.request.user
        return UserStorage.objects.filter(user_id=user, is_active=True).order_by('-pk')

    def get_context_data(self, **kwargs):
        context = super(ServiceSubscribeListView,self).get_context_data(**kwargs)
        user = self.request.user
        supportsubs = UserSupport.objects.filter(user_id=user, is_active=True)
        storagesubslist = UserStorage.objects.filter(user_id=user, is_active=True)
        newlist = [*supportsubs, *storagesubslist]
        context['newlist'] = newlist
        return context