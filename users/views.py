from django.shortcuts import render
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from users.forms import profileUpdateForm, userUpdateForm
from users.models import Profile as Pro
from users.models import  Requests
from django.contrib.auth.models import User
from django.contrib import messages
from django.shortcuts import render, get_object_or_404, redirect
from django.core.mail import send_mail
from django.core.mail import EmailMessage

# Create your views here.




@login_required
def Profile(request):
    if request.method == 'POST':
        u_form = userUpdateForm(request.POST,instance=request.user)
        p_form = profileUpdateForm(request.POST,request.FILES,instance=request.user.profile)
        if u_form.is_valid() and p_form.is_valid():
            u_form.save()
            p_form.save()
            messages.success(request, 'Your account has been successfully updated')
            return redirect('users:profile')
    else:
        u_form = userUpdateForm(instance=request.user)
        p_form = profileUpdateForm(instance=request.user.profile)

    context= {
        'u_form':u_form,
        'p_form':p_form,
    }
    return render(request,'profile/profile.html',context)


def request(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        email = request.POST.get('e-mail')
        contact = request.POST.get('phone')
        prof = request.user.profile
        request = Requests(profile=prof, name=name, email=email, contact=contact)
        request.save()
        prof_id = prof.id
        Pro.objects.filter(id=prof_id).update(is_teacher=True)
        
        message = 'Your request for a teacher account has been accepted! Now you can go back to Webera and upload courses and lectures, good job!'
        send_mail(
            'The request was accepted',
            message,
            'abhishekpm54@gmail.com',
            [email],
            fail_silently=False,
        )
        send_mail(
            'MesoOn',
            'Someone requested a teacher account. Me info: ' + name + ' , ' + email + ' , ' + contact + ' , ' + str(prof) + '.',
            'abhishek@gmail.com',
            ['abhishekpm54@gmail.com'],
            fail_silently=False,
        )
        messages.info(request, f'The request was sent successfully, you will be notified by email.')
        return redirect('courses:home')


