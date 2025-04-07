from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponse
from django.template.loader import get_template
from django.views.generic.edit import CreateView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required

from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated

from xhtml2pdf import pisa
from .models import Resume
from .forms import ResumeForm
from .serializers import ResumeSerializer

# API View for Resume CRUD
class ResumeViewSet(viewsets.ModelViewSet):
    serializer_class = ResumeSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Resume.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

# Form-based Resume Creation View (UI form)
class ResumeCreateView(LoginRequiredMixin, CreateView):
    model = Resume
    form_class = ResumeForm
    template_name = 'resumes/resume_form.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        try:
            context['resume'] = Resume.objects.filter(user=self.request.user).last()
        except Exception as e:
            print("🔥 DEBUG: Error in get_context_data:", e)
            context['resume'] = None
        return context

    def form_valid(self, form):
        try:
            form.instance.user = self.request.user
            resume = form.save()
            if resume.pdf_file:
                print("✅ File saved to:", resume.pdf_file.path)
            else:
                print("⚠️ No PDF file attached.")
            return redirect('resumes:generate_pdf', resume_id=resume.id)
        except Exception as e:
            print("🔥 DEBUG: Error during resume save:", e)
            return HttpResponse("Something went wrong. Check server logs.", status=500)


# Optional fallback handler
@login_required
def resume_create(request):
    resume = Resume.objects.filter(user=request.user).last()

    if request.method == 'POST':
        form = ResumeForm(request.POST, request.FILES)
        if form.is_valid():
            resume = form.save(commit=False)
            resume.user = request.user
            resume.save()
            return render(request, 'resumes/resume_form.html', {'form': ResumeForm(), 'resume': resume})
    else:
        form = ResumeForm()

    return render(request, 'resumes/resume_form.html', {'form': form, 'resume': resume})

@login_required
def generate_pdf(request, resume_id):
    resume = get_object_or_404(Resume, id=resume_id, user=request.user)

    skills_list = [skill.strip() for skill in resume.skills.split(",")] if resume.skills else []

    resume_data = {
        "name": resume.title,
        "summary": resume.summary,
        "skills": skills_list,
        "education": resume.education,
        "experience": resume.experience,
        "certifications": resume.certifications,
    }

    template = get_template('resumes/resume_pdf_template.html')
    html = template.render(resume_data)

    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = f'attachment; filename="resume_{resume_id}.pdf"'

    pisa_status = pisa.CreatePDF(html, dest=response)
    if pisa_status.err:
        return HttpResponse('PDF generation failed', status=500)

    return response

@login_required
def delete_resume(request, resume_id):
    resume = get_object_or_404(Resume, id=resume_id, user=request.user)
    if request.method == 'POST':
        resume.delete()
        return redirect('resumes:resume_list')
    return render(request, 'resumes/confirm_delete.html', {'resume': resume})

@login_required
def resume_list(request):
    resumes = Resume.objects.filter(user=request.user)
    return render(request, 'resumes/resume_list.html', {'resumes': resumes})

@login_required
def resume_detail(request, resume_id):
    resume = get_object_or_404(Resume, id=resume_id, user=request.user)
    return render(request, 'resumes/resume_detail.html', {'resume': resume})

@login_required
def resume_edit(request, resume_id):
    resume = get_object_or_404(Resume, id=resume_id, user=request.user)
    if request.method == 'POST':
        form = ResumeForm(request.POST, request.FILES, instance=resume)
        if form.is_valid():
            form.save()
            return redirect('resumes:resume_detail', resume_id=resume.id)
    else:
        form = ResumeForm(instance=resume)
    return render(request, 'resumes/resume_form.html', {'form': form, 'resume': resume})
