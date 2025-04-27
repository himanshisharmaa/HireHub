from django.shortcuts import render,get_object_or_404,redirect
from django.views.generic import ListView,DetailView,CreateView,UpdateView,DeleteView,View
from .models import Job,Application
from django.contrib.auth.mixins import LoginRequiredMixin,UserPassesTestMixin
from django.urls import reverse_lazy
from .forms import JobForm,ApplicationForm
from django.contrib import messages
from django.db.models import Q


# Create your views here.
class JobListView(ListView):
    model=Job
    template_name='jobs/job_list.html'
    context_object_name='jobs'
    ordering=['-created_at']
    paginate_by=5

    def get_queryset(self):
        query=self.request.GET.get('q')
        
        if query:
            return Job.objects.filter(
                Q(title__icontains=query)|
                Q(company__icontains=query)|
                Q(location__icontains=query)
            ).order_by('-created_at')
        return Job.objects.all().order_by('-created_at')

class JobDetailView(DetailView):
    model=Job
    template_name='jobs/job_detail.html'
    context_object_name='job'

#only for employers
class JobCreateView(LoginRequiredMixin,UserPassesTestMixin,CreateView):
    model=Job
    form_class=JobForm
    template_name="jobs/job_form.html"

    def form_valid(self,form):
        form.instance.employer=self.request.user
        return super().form_valid(form)
    
    def test_func(self):
        return self.request.user.profile.is_employer

class JobUpdateView(LoginRequiredMixin,UserPassesTestMixin,UpdateView):
    model=Job
    form_class=JobForm
    template_name='jobs/job_form.html'

    def form_valid(self,form):
        form.instance.employer=self.request.user
        return super().form_valid(form)
    
    def test_func(self):
        job=self.get_object()
        return job.employer==self.request.user

class JobDeleteView(LoginRequiredMixin,UserPassesTestMixin,DeleteView):
    model=Job
    template_name='jobs/job_confirm_delete.html'
    success_url=reverse_lazy('job_list')

    def test_func(self):
        job=self.get_object()
        return job.employer==self.request.user
    
class ApplyJobView(LoginRequiredMixin,UserPassesTestMixin,CreateView):
    model=Application
    form_class=ApplicationForm
    template_name='jobs/apply_job.html'

    def form_valid(self,form):
        job=get_object_or_404(Job,pk=self.kwargs['pk'])
        if Application.objects.filter(job=job,candidate=self.request.user).exists():
            messages.warning(self.request,"You have already applied for this job.")
            return self.form_invalid(form)

        form.instance.job=job
        form.instance.candidate=self.request.user
        messages.success(self.request, "Successfully applied for the job!")
        return super().form_valid(form)
    
    def get_success_url(self):
        return reverse_lazy('job_detail',kwargs={'pk':self.kwargs['pk']})
    
    def test_func(self):
        return not self.request.user.profile.is_employer

class CandidateDashboardView(LoginRequiredMixin,ListView):
    model=Application
    template_name='jobs/candidate_dashboard.html'
    context_object_name='applications'
    def get_queryset(self):
        return Application.objects.filter(candidate=self.request.user).select_related('job')
    
class WithdrawApplicationView(LoginRequiredMixin,View):
    def post(self,request,pk):
        application=get_object_or_404(Application,pk=pk,candidate=request.user)
        application.delete()
        messages.info(request,"You have withdrawn the application")
        return redirect('candidate_dashboard')
    
class EmployerDashboardView(LoginRequiredMixin, ListView):
    model = Job
    template_name = 'jobs/employer_dashboard.html'
    context_object_name = 'jobs'

    def get_queryset(self):
        return Job.objects.filter(employer=self.request.user).prefetch_related('application_set__candidate')

class UpdateApplicationStatusView(LoginRequiredMixin, UpdateView):
    model = Application
    fields = ['status']  # Only allow editing the status
    template_name = 'jobs/update_status_form.html'

    def get_success_url(self):
        return reverse_lazy('employer_dashboard')