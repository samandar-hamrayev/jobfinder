from django.db.models import Q
from django.http import JsonResponse
from django.views import View
from django.views.decorators.http import require_GET
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from django.shortcuts import get_object_or_404, redirect, render
from django.contrib import messages

from .models import Job, JobCategory, JobApplication
from .forms import JobForm, JobApplicationForm

class JobListView(ListView):
    model = Job
    template_name = 'jobs/job_list.html'
    context_object_name = 'jobs'
    paginate_by = 10

    def get_queryset(self):
        queryset = super().get_queryset()
        search = self.request.GET.get('search')
        job_type = self.request.GET.get('job_type')
        category = self.request.GET.get('category')
        sort = self.request.GET.get('sort', 'newest')

        if search:
            queryset = queryset.filter(
                Q(title__icontains=search) | Q(company__icontains=search) | Q(description__icontains=search)
            )
        if job_type:
            queryset = queryset.filter(job_type=job_type)
        if category:
            queryset = queryset.filter(category_id=category)

        if sort == 'newest':
            queryset = queryset.order_by('-posted_at')
        elif sort == 'oldest':
            queryset = queryset.order_by('posted_at')

        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['categories'] = JobCategory.objects.all()
        return context


class JobDetailView(DetailView):
    model = Job
    template_name = 'jobs/job_detail.html'
    context_object_name = 'job'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if self.request.user.is_authenticated:
            context['has_applied'] = JobApplication.objects.filter(
                job=self.object,
                applicant=self.request.user
            ).exists()
        context['similar_jobs'] = Job.objects.filter(
            category=self.object.category,
            is_active=True
        ).exclude(pk=self.object.pk)[:3]
        return context


class JobCreateView(LoginRequiredMixin, CreateView):
    model = Job
    form_class = JobForm
    template_name = 'jobs/job_form.html'
    success_url = reverse_lazy('job_list')

    def form_valid(self, form):
        form.instance.posted_by = self.request.user
        messages.success(self.request, 'Job posted successfully!')
        return super().form_valid(form)


class JobUpdateView(LoginRequiredMixin, UpdateView):
    model = Job
    form_class = JobForm
    template_name = 'jobs/job_form.html'

    def get_success_url(self):
        return reverse_lazy('job_detail', kwargs={'pk': self.object.pk})

    def dispatch(self, request, *args, **kwargs):
        obj = self.get_object()
        if obj.posted_by != self.request.user:
            messages.error(request, 'You are not authorized to edit this job.')
            return redirect('job_detail', pk=obj.pk)
        return super().dispatch(request, *args, **kwargs)

    def form_valid(self, form):
        messages.success(self.request, 'Job updated successfully!')
        return super().form_valid(form)


class JobDeleteView(LoginRequiredMixin, DeleteView):
    model = Job
    template_name = 'jobs/job_confirm_delete.html'
    success_url = reverse_lazy('job_list')

    def dispatch(self, request, *args, **kwargs):
        obj = self.get_object()
        if obj.posted_by != request.user:
            messages.error(request, 'You are not authorized to delete this job.')
            return redirect('job_detail', pk=obj.pk)
        return super().dispatch(request, *args, **kwargs)

    def delete(self, request, *args, **kwargs):
        messages.success(request, 'Job deleted successfully!')
        return super().delete(request, *args, **kwargs)


class JobApplicationView(LoginRequiredMixin, View):
    template_name = 'jobs/job_application.html'

    def get(self, request, pk):
        job = get_object_or_404(Job, pk=pk)

        # Check if user already applied
        if JobApplication.objects.filter(job=job, applicant=request.user).exists():
            messages.warning(request, 'You have already applied for this job.')
            return redirect('job_detail', pk=job.pk)

        form = JobApplicationForm()
        return render(request, self.template_name, {
            'form': form,
            'job': job
        })

    def post(self, request, pk):
        job = get_object_or_404(Job, pk=pk)
        form = JobApplicationForm(request.POST, request.FILES)

        if form.is_valid():
            application = form.save(commit=False)
            application.job = job
            application.applicant = request.user
            application.save()

            messages.success(request, 'Your application has been submitted successfully!')
            return redirect('job_detail', pk=job.pk)

        return render(request, self.template_name, {
            'form': form,
            'job': job
        })


class MyApplicationsView(LoginRequiredMixin, ListView):
    model = JobApplication
    template_name = 'jobs/my_applications.html'
    context_object_name = 'applications'

    def get_queryset(self):
        return JobApplication.objects.filter(applicant=self.request.user)


class MyPostedJobsView(LoginRequiredMixin, ListView):
    model = Job
    template_name = 'jobs/my_posted_jobs.html'
    context_object_name = 'jobs'

    def get_queryset(self):
        return Job.objects.filter(posted_by=self.request.user)

class JobApplicantsView(LoginRequiredMixin, DetailView):
    model = Job
    template_name = 'jobs/job_applicants.html'
    context_object_name = 'job'

    def dispatch(self, request, *args, **kwargs):
        obj = self.get_object()
        if obj.posted_by != request.user:
            messages.error(request, "You don't have permission to view applicants for this job.")
            return redirect('job_detail', pk=obj.pk)
        return super().dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['applications'] = self.object.jobapplication_set.all().select_related('applicant', 'applicant__profile')
        return context

def update_application_status(request, pk, status):
    application = get_object_or_404(JobApplication, pk=pk)
    if request.user != application.job.posted_by:
        messages.error(request, "You don't have permission to update this application.")
    else:
        valid_statuses = [choice[0] for choice in JobApplication.STATUS_CHOICES]
        if status in valid_statuses:
            application.status = status
            application.save()
            messages.success(request, f"Application status updated to {application.get_status_display()}.")
        else:
            messages.error(request, "Invalid status.")
    return redirect('job_detail', pk=application.job.pk)


def job_quick_view(request, pk):
    job = get_object_or_404(Job, pk=pk)
    return JsonResponse({
        'title': job.title,
        'company': job.company,
        'job_type': job.get_job_type_display(),
        'category': job.category.name,
        'description': job.description,
        'location': job.location,
        'salary': job.salary or 'Not specified',
        'posted_at': job.posted_at.strftime('%b %d, %Y'),
    })