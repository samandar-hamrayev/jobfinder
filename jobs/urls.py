from django.urls import path
from .views import (
    JobListView,
    JobDetailView,
    JobCreateView,
    JobUpdateView,
    JobDeleteView,
    JobApplicationView,
    MyApplicationsView,
    MyPostedJobsView,
    JobApplicantsView,
    update_application_status,
    job_quick_view
)

urlpatterns = [
    path('', JobListView.as_view(), name='job_list'),
    path('<int:pk>/', JobDetailView.as_view(), name='job_detail'),
    path('<int:pk>/quick-view/', job_quick_view, name='quick_view'),
    path('create/', JobCreateView.as_view(), name='job_create'),
    path('<int:pk>/update/', JobUpdateView.as_view(), name='job_update'),
    path('<int:pk>/delete/', JobDeleteView.as_view(), name='job_delete'),
    path('<int:pk>/apply/', JobApplicationView.as_view(), name='job_apply'),
    path('my-applications/', MyApplicationsView.as_view(), name='my_applications'),
    path('my-posted-jobs/', MyPostedJobsView.as_view(), name='my_posted_jobs'),
    path('<int:pk>/applicants/', JobApplicantsView.as_view(), name='job_applicants'),
    path('application/<int:pk>/update-status/<str:status>/', update_application_status,
         name='update_application_status'),

]