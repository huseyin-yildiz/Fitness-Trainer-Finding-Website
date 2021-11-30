from django.shortcuts import render, HttpResponse , get_object_or_404, HttpResponseRedirect, Http404
from .models import Trainer
from .forms import TrainerForm, CommentForm
from django.contrib import messages

def trainer_index(request):
    trainers = Trainer.objects.all()
    auth_trainer = None
    if request.user.is_authenticated:
        auth_trainer = trainers.filter(User_ID=request.user)

    return render(request, 'trainer/index.html', {'trainers': trainers, 'auth_trainer': auth_trainer})

def trainer_detail(request, id):
    trainer = get_object_or_404(Trainer, id=id)

    form= CommentForm(request.POST or None )
    if form.is_valid():
        comment=form.save(commit=False)
        comment.trainer = trainer
        comment.save()
        return HttpResponseRedirect(trainer.get_absolute_url())

    context= {
        'trainer':trainer,
        'form':form,
    }
    return render(request,'trainer/detail.html',context)

def trainer_create(request):
    form= TrainerForm(request.POST or None,request.FILES or None)
    if form.is_valid():
        form.save()
    else:
        form=TrainerForm()
    context = {
        'form': form,
    }
    return render(request, 'trainer/form.html',context)

def trainer_update(request, id):
    if not request.user.is_authenticated:
        return Http404()

    trainer = get_object_or_404(Trainer, id=id)
    print(trainer.User_ID)
    form = TrainerForm(request.POST or None, request.FILES or None, instance=trainer)
    if form.is_valid():
        if request.user == trainer.User_ID:
            form.save()
            messages.success(request, 'Successfully updated!')
            return HttpResponseRedirect(trainer.get_absolute_url())
        else:
            messages.warning(request, 'You can not edit another trainer\'s information.')
            return redirect('trainer:index')
    context = {
        'form': form,
    }
    return render(request, 'trainer/form.html', context)

def trainer_delete(request):
    return HttpResponse('Burası trainer delete sayfası')