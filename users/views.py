from django.shortcuts import render,redirect
from django.contrib.auth import authenticate,login,logout
from .forms import EmployerSignUpForm,CandidateProfileForm,EmployerProfileForm,CandidateSignUpForm
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.decorators import login_required 
from django.views.generic import DetailView, UpdateView
from django.contrib.auth.mixins import LoginRequiredMixin
from .models import Profile
from django.urls import reverse_lazy
# Create your views here.

def employer_signup(request):
    if request.method=="POST":
        form =EmployerSignUpForm(request.POST)
        if form.is_valid():
            user=form.save()
            login(request,user)
            return redirect('job_list')
    else:
        form =EmployerSignUpForm()
    return render(request,'users/employer_signup.html',{"form":form})

def candidate_signup(request):
    if request.method=="POST":
        form=CandidateSignUpForm(request.POST)
        if form.is_valid():
            user=form.save()
            login(request,user)
            return redirect('job_list')
    else:
        form=CandidateSignUpForm()
    return render(request,'users/candidate_signup.html',{'form':form})

def user_login(request):
    if request.method=="POST":
        form=AuthenticationForm(request,data=request.POST)
        if form.is_valid():
            user=form.get_user()
            login(request,user)
            return redirect('job_list')
    else:
        form=AuthenticationForm()
    return render(request,"users/login.html",{"form":form})

@login_required
def user_logout(request):
    logout(request)
    return redirect('login')

class ProfileDetailView(LoginRequiredMixin, DetailView):
    model = Profile
    template_name = 'users/profile.html'
    context_object_name = 'profile'

    def get_object(self):
        return self.request.user.profile

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        profile = self.get_object()

        # Split the skills field into a list only if it exists
        if profile.skills:
            context['skills_list'] = [skill.strip() for skill in profile.skills.split(',')]
        else:
            context['skills_list'] = []

        return context



# Profile Update View (Editable form)
class ProfileUpdateView(LoginRequiredMixin, UpdateView):
    model = Profile
    template_name = 'users/profile_form.html'
    context_object_name = 'profile'

    def get_object(self):
        return self.request.user.profile

    def get_form_class(self):
        if self.request.user.profile.is_employer:
            return EmployerProfileForm
        else:
            return CandidateProfileForm

    def get_success_url(self):
        from django.urls import reverse_lazy
        return reverse_lazy('profile') 