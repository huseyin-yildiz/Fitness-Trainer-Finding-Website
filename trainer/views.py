from django.shortcuts import render, HttpResponse , get_object_or_404, HttpResponseRedirect
from .models import Trainer
from .forms import TrainerForm , CommentForm

def trainer_index(request):
    trainers = Trainer.objects.all()
    return render(request, 'trainer/index.html', {'trainers': trainers})

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

def trainer_update(request):
    return HttpResponse('Burası trainer update sayfası')

def trainer_delete(request):
    return HttpResponse('Burası trainer delete sayfası')