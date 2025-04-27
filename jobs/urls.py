from django.urls import path
from .views import (JobListView,JobDetailView,JobCreateView,JobUpdateView,JobDeleteView,ApplyJobView
                    ,CandidateDashboardView,WithdrawApplicationView
                    ,EmployerDashboardView,UpdateApplicationStatusView)

urlpatterns = [
    path('',JobListView.as_view(),name="job_list"),
    path('job/<int:pk>/',JobDetailView.as_view(),name="job_detail"),
    path('job/new/',JobCreateView.as_view(),name="job_create"),
    path('job/<int:pk>/update/',JobUpdateView.as_view(),name="job_update"),
    path('job/<int:pk>/delete/',JobDeleteView.as_view(),name="job_delete"),
    path('job/<int:pk>/apply/',ApplyJobView.as_view(),name="job_apply"),
    path('my-applications/', CandidateDashboardView.as_view(), name='candidate_dashboard'),
    path('application/<int:pk>/withdraw/', WithdrawApplicationView.as_view(), name='withdraw_application'),
    path('employer-dashboard/', EmployerDashboardView.as_view(), name='employer_dashboard'),
    path('update-status/<int:pk>/', UpdateApplicationStatusView.as_view(), name='update_application_status'),
]
