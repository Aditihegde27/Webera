import secrets
from django.shortcuts import render, redirect
from django.views.generic import TemplateView,ListView,DetailView,View
from courses.models import Subject,Lesson,Class
from memberships.models import UserMembership
from django.shortcuts import render, get_object_or_404
from django.contrib.auth.mixins import LoginRequiredMixin,UserPassesTestMixin
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .forms import ClassForm, SubjectForm, LessonForm
# Create your views here.

class HomeView(TemplateView):
    template_name = 'index.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        category = Class.objects.all()
        context['category'] = category
        return context

class AboutView(TemplateView):
    template_name = 'about.html'


class ContactView(TemplateView):
    template_name = 'contact.html'



def CourseListView(request, category):
    courses = Subject.objects.filter(classa=category)
    context = {
        'courses':courses
    }
    return render(request, 'courses/course_list.html', context)



class CourseDetailView(DetailView):
    context_object_name = 'course'
    template_name = 'courses/course_detail.html'
    model = Subject


 
class LessonDetailView(View,LoginRequiredMixin):
    def get(self, request, course_slug, lesson_slug, *args, **kwargs):
        course = get_object_or_404(Subject, slug=course_slug)
        lesson = get_object_or_404(Lesson, slug=lesson_slug)
        context = {'lesson': lesson}
        return render(request, "courses/lesson_detail.html", context)


@login_required
def SearchView(request):
    if request.method == 'POST':
        kerko = request.POST.get('search')
        results = Lesson.objects.filter(title__contains=kerko)
        context = {
            'results':results
        }
        return render(request, 'courses/search_result.html', context)


@login_required
def create_class(request):
    if not request.user.profile.is_teacher == True:
        messages.error(request, f'Your account does not have access to this url only teacher accounts!')
        return redirect('courses:home')
    if request.method == 'POST':
        form = ClassForm(data=request.POST, files=request.FILES)
        if form.is_valid():
            form.save()
            messages.success(request, f'Your Class was created')
            return redirect('courses:home')
    else:
        form = ClassForm()
    context = {
        'form':form
    }
    return render(request, 'courses/create_class.html', context)


@login_required
def create_subject(request):
    if not request.user.profile.is_teacher == True:
        messages.error(request, f'Your account does not have access to this url only teacher accounts!')
        return redirect('courses:home')
    if request.method == 'POST':
        form = SubjectForm(request.POST)
        if form.is_valid():
            form.save()
            classa = form.cleaned_data['classa']
            slug = classa.id
            messages.success(request, f'Your subject matter was created.')
            return redirect('/courses/' + str(slug))
    else:
        form = SubjectForm(initial={'creator':request.user.id, 'slug':secrets.token_hex(nbytes=16)})
    context = {
        'form':form
    }
    return render(request, 'courses/create_subject.html', context)


@login_required
def create_lesson(request):
    if not request.user.profile.is_teacher == True:
        messages.error(request, f'Your account does not have access to this url only teacher accounts!')
        return redirect('courses:home')
    if request.method == 'POST':
        form = LessonForm(request.POST)
        if form.is_valid():
            form.save()
            subject = form.cleaned_data['subject']
            slug = subject.slug
            messages.success(request, f'Your lesson was created.')
            return redirect('/courses/' + str(slug) )
    else:
        form = LessonForm(initial={'slug':secrets.token_hex(nbytes=16)})
    context = {
        'form':form
    }
    return render(request, 'courses/create_lesson.html', context)


def view_404(request, exception):
    return render(request, '404.html')

def view_403(request, exception):
    return render(request, '403.html')

def view_500(request):
    return render(request, '500.html')

