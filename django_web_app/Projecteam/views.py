import os
from django.contrib.auth.models import User
from django.core.mail import send_mail
from django.core.paginator import Paginator
from django.shortcuts import render, redirect
from .models import projectdb,projectFiles
from django.db.models import Q
from .forms import TeamCreations


def TeamCreate(request):
    if request.method =="POST":
        form=TeamCreations(request.POST)
        print('entered')
        if form.is_valid():
            print(form.cleaned_data['status'],"***************")
            db=projectdb(name=form.cleaned_data['name'],
                      title=form.cleaned_data['title'],
                      leader=request.user,
                    status=form.cleaned_data['status'],
                      member=request.POST.getlist('members'))
            db.save()
            recp=[request.user.email]
            for i in db.member:
                recp.append(User.objects.filter(username__icontains=i).first().email)

            send_mail(
                'team created',
                'you  have been selected to  {} project under the leadership of {}'.format(db.title,request.user),
                None,
                recp,
                fail_silently=True, )
            return redirect("team:list")
    form=TeamCreations()
    choose = []
    res = User.objects.all()
    for i in res:
        choose.append((str(i.username), str(i.username)))
    context={'list':choose,'form':form}
    return render(request,"Projecteam/project.html",context)

def TeamList(request):
    projects=projectdb.objects.filter(status=True)
    print(projects,"*************")
    alist = []
    for i in range(0, len(projects) - 1, 2):
        alist.append([projects[i], projects[i + 1]])
    if len(projects) % 2 != 0:
        alist.append([projects[len(projects) - 1], None])
    paginator = Paginator(alist, 2)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    res = page_obj.paginator.count
    context = {"page_obj": page_obj}
    return render(request,"Projecteam/teamlist.html",context)

def teamDetail(request,name):
    details=projectdb.objects.filter(name=name).first()
    Files=projectFiles.objects.filter(user=details)
    filename=[]
    if str(request.user)==str(details.leader.username):
        lead,mem=True,True
    elif str(request.user) in details.member:
        lead,mem=False,True
    else:
        lead,mem=False,False
    for i in Files:
        filename.append(str(os.path.basename(str(i.file))).strip(" "))
    Files=list(zip(filename,Files))
    members=""
    for i in range(len(details.member)-1):
        members+=details.member[i]+" ,"
    members+=" "+details.member[len(details.member)-1]
    context={"details":details,"files":Files,"lead":lead,"mem":mem,'members':members}
    return render(request,"Projecteam/details.html",context)


def Filedelete(request,name):
    user=projectdb.objects.filter(name=name).first()
    res=projectFiles.objects.filter(file__icontains=name,user=user).first()
    if res:
        res.delete()
    return redirect('team:detail',name=user.name)

def Fileupload(request,name):
    user = projectdb.objects.filter(name=name).first()
    t=projectFiles(user=user,file=request.FILES.get('file'))
    t.save()
    return redirect("team:detail",name=user.name)

def search(request):
    obj=str(request.GET.get('q'))
    projects = projectdb.objects.filter(Q(name=obj) |
                                     Q(title=obj) | Q(leader=User.objects.filter(username=obj).first()) |
                                     Q(member__contains=[obj]))
    alist = []
    for i in range(0, len(projects) - 1, 2):
        alist.append([projects[i], projects[i + 1]])
    if len(projects) % 2 != 0:
        alist.append([projects[len(projects) - 1], None])
    paginator = Paginator(alist, 2)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    context = {"page_obj": page_obj,'qu':True,'q':obj}
    return render(request, "Projecteam/teamlist.html", context)

def memeberTeam(request):
    projects = projectdb.objects.filter(Q(leader=request.user)|Q(member__contains=[request.user]))
    alist = []
    for i in range(0, len(projects) - 1, 2):
        alist.append([projects[i], projects[i + 1]])
    if len(projects) % 2 != 0:
        alist.append([projects[len(projects) - 1], None])
    paginator = Paginator(alist, 2)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    context = {"page_obj": page_obj}
    return render(request, "Projecteam/myTeamlist.html", context)

def delTeam(request,id):
    res=projectdb.objects.filter(id=id).first()
    recp=[]
    for i in res.member:
        recp.append(User.objects.filter(username__icontains=i).first().email)
    send_mail(
        'Team Terminated',
        'team has been deleted by leader {}'.format(request.user),
        None,
        recp,
        fail_silently=True, )
    res.delete()
    return redirect("team:mlist")


