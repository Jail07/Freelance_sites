from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate, logout
from django.contrib import messages
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.views import View
from .models import Profile
from .forms import CustomUserCreationForm, ProfileForm, SkillForm, MessageForm
from django.contrib.auth.mixins import LoginRequiredMixin
from .utils import searchProfiles, paginateProfiles

from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework.response import Response

@api_view(['GET'])
def getRoutes(request):

    routes = [
        {'POST': '/api/account/token'},
        {'POST': '/api/account/token/refresh'},
    ]
    return Response(routes)



class LoginUserView(View):
    page = 'login'
    def get(self, request):
        context = {'page': self.page}
        return render(request, 'account/login_register.html', context)

    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect('/')
        return super().dispatch(request, *args, **kwargs)
    
    def post(self, request):
        username = request.POST['username'].lower()
        password = request.POST['password']
        try:
            user = User.objects.get(username=username)
        except:
            messages.error(request, 'Username does not exist')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect(request.GET['next'] if 'next' in request.GET else 'account')
        else:
            messages.error(request, 'Username OR password is incorrect')
        return render(request, 'account/login_register.html', {'page': self.page})


class LogoutUserView(LoginRequiredMixin, View):
    def get(self, request):
        logout(request)
        messages.info(request, 'User was logged out!')
        return redirect('login')


class RegisterUserView(View):
    page = 'register'
    form = CustomUserCreationForm

    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect('/')
        return super().dispatch(request, *args, **kwargs)

    def get(self, request):
        context = {'page': self.page, 'form': self.form}
        return render(request, 'account/login_register.html', context)

    def post(self, request):
        form = self.form(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.username = user.username.lower()
            user.save()
            messages.success(request, 'User account was created!')
            login(request, user)
            return redirect('/account')
        else:
            messages.error(request, 'An error has occurred during registration')
        return render(request, 'account/login_register.html', {'page': self.page, 'form': form})


def profiles(request):
    profiles, search_query = searchProfiles(request)
    custom_range, profiles = paginateProfiles(request, profiles, 6)

    context = {'profiles': profiles, 'search_query': search_query, 'custom_range': custom_range}
    return render(request, 'account/profiles.html', context)


class ProfileDetailView(View):
    def get(self, request, pk):
        profile = Profile.objects.get(id=pk)
        topSkills = profile.skill_set.exclude(description__exact="")
        otherSkills = profile.skill_set.filter(description="")
        context = {'profile': profile, 'topSkills': topSkills,
               "otherSkills": otherSkills}
        return render(request, 'account/profile_detail.html', context)


class UserAccountView(LoginRequiredMixin, View):
    def get(self, request):
        profile = request.user.profile
        skills = profile.skill_set.all()
        projects = profile.project_set.all()
        context = {'profile': profile, 'skills': skills, 'main': projects}
        return render(request, 'account/account.html', context)


class EditAccountView(LoginRequiredMixin, View):
    form = ProfileForm

    def setup(self, request, *args, **kwargs):
        self.profile_instance = request.user.profile
        return super().setup(self, request, *args, **kwargs)

    def get(self, request):
        form = self.form(instance=self.profile_instance)
        context = {'form': form}
        return render(request, 'account/profile_form.html', context)

    def post(self, request):
        form = ProfileForm(request.POST, request.FILES, instance=self.profile_instance)
        if form.is_valid():
            form.save()
            return redirect('account')
        return render(request, 'account/profile_form.html', {'form': form})


@login_required(login_url='login')
def createSkill(request):
    profile = request.user.profile
    form = SkillForm()

    if request.method == 'POST':
        form = SkillForm(request.POST)
        if form.is_valid():
            skill = form.save(commit=False)
            skill.owner = profile
            skill.save()
            messages.success(request, 'Skill was added successfully!')
            return redirect('account')

    context = {'form': form}
    return render(request, 'account/skill_form.html', context)


@login_required(login_url='login')
def updateSkill(request, pk):
    profile = request.user.profile
    skill = profile.skill_set.get(id=pk)
    form = SkillForm(instance=skill)

    if request.method == 'POST':
        form = SkillForm(request.POST, instance=skill)
        if form.is_valid():
            form.save()
            messages.success(request, 'Skill was updated successfully!')
            return redirect('account')

    context = {'form': form}
    return render(request, 'account/skill_form.html', context)


@login_required(login_url='login')
def deleteSkill(request, pk):
    profile = request.user.profile
    skill = profile.skill_set.get(id=pk)
    if request.method == 'POST':
        skill.delete()
        messages.success(request, 'Skill was deleted successfully!')
        return redirect('account')

    context = {'object': skill}
    return render(request, 'delete_template.html', context)


@login_required(login_url='login')
def inbox(request):
    profile = request.user.profile
    messageRequests = profile.messages.all()
    unreadCount = messageRequests.filter(is_read=False).count()
    context = {'messageRequests': messageRequests, 'unreadCount': unreadCount}
    return render(request, 'account/inbox.html', context)


@login_required(login_url='login')
def viewMessage(request, pk):
    profile = request.user.profile
    message = profile.messages.get(id=pk)
    if message.is_read == False:
        message.is_read = True
        message.save()
    context = {'message': message}
    return render(request, 'account/message.html', context)


def createMessage(request, pk):
    recipient = Profile.objects.get(id=pk)
    form = MessageForm()

    try:
        sender = request.user.profile
    except:
        sender = None

    if request.method == 'POST':
        form = MessageForm(request.POST)
        if form.is_valid():
            message = form.save(commit=False)
            message.sender = sender
            message.recipient = recipient

            if sender:
                message.name = sender.name
                message.email = sender.email
            message.save()

            messages.success(request, 'Your message was successfully sent!')
            return redirect('profile-detail', pk=recipient.id)

    context = {'recipient': recipient, 'form': form}
    return render(request, 'account/message_form.html', context)