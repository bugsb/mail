from django.shortcuts import render,redirect
from django.http import HttpResponse,JsonResponse
from app.models import Mail_detail
import datetime
from django.contrib import messages
from django.contrib.auth.models import User


def validate_receiver(receiver):
    is_email_exists = User.objects.filter(email=receiver).exists()
    if is_email_exists:
        return True
    return False

def get_inbox(email):
    data = []

    for mail in Mail_detail.objects.filter(receiver=email,is_draft=0,in_inbox=1):
        temp = dict()
        temp['id'] = mail.id
        temp['sender'] = mail.sender
        temp['sub'] = mail.subject
        temp['receiver'] = mail.receiver
        temp['body'] = mail.body[0:20] + ' . . . . .'
        data.append(temp)
    return data

def get_outbox(email):
    data = []

    for mail in Mail_detail.objects.filter(sender=email,is_draft=0,in_outbox=1):
        temp = dict()
        temp['id'] = mail.id
        temp['sender'] = mail.sender
        temp['sub'] = mail.subject
        temp['receiver'] = mail.receiver
        temp['body'] = mail.body[0:20] + ' . . . . .'
        data.append(temp)
    return data

def home(request):
    return render(request,'home.html')

def inbox(request,email):
    data = get_inbox(email)
    context = {
        'data':data
    }
    return render(request,'inbox.html',context)

def replay(request,mid):
    data = Mail_detail.objects.filter(id=mid).first()
    context = dict()
    context['receiver'] = data.sender
    context['sub'] = 'Re:'

    return render(request,'replay.html',context)

def forward(request,mid):
    data = Mail_detail.objects.filter(id=mid).first()
    context = dict()
    context['body'] = data.body
    context['sub'] = 'Fw: ' + data.subject
    return render(request,'forward.html',context)

def outbox(request,email):
    data = get_outbox(email)
    context = {
        'data':data
    }
    return render(request,'outbox.html',context)

def drafts(request,mail):
    data = []

    for mail in Mail_detail.objects.filter(sender=mail):
        temp = dict()
        temp['id'] = mail.id
        temp['sender'] = mail.sender
        temp['sub'] = mail.subject
        temp['receiver'] = mail.receiver
        temp['file'] = mail.file
        temp['is_draft'] = mail.is_draft
        temp['body'] = mail.body[0:20] + ' . . . . .'
        data.append(temp)
    context = {
        'data':data
    }
    return render(request,'drafts.html',context)

def compose(request,mail):
    if request.method == 'POST':
        receiver = request.POST.get('receiver')
        if receiver == '':
            messages.info(request,"recipients Id Blank !")
            return redirect(f'/app/compose/{mail}')
        if validate_receiver(receiver):
            body =request.POST.get('body')
            sub = request.POST.get('sub')
            date = datetime.datetime.today()
            if 'file' in request.FILES:
                file = request.FILES['file']
            else:
                file = None
            mail = Mail_detail(sender=mail,receiver=receiver,file=file,in_inbox=1,in_outbox=1,is_draft=0, subject= sub,body=body,date=date)
            mail.save()
            messages.success(request, 'Email Sent success !')
        else:
            messages.info(request,"recipients Id is not valid !")
    return render(request,'compose.html')

def autosuggest(request):
    query = request.GET.get('term')
    query_set = User.objects.filter(email__icontains=query)
    store = []
    store += [q.email for q in query_set]
    return JsonResponse(store,safe=False)

def send_draft(request,mid):
    data = Mail_detail.objects.filter(id=mid).first()
    context = dict()
    context['body'] = data.body
    context['receiver'] = data.receiver
    context['file'] =data.file
    context['is_draft'] =data.is_draft
    context['sub'] = data.subject

    return render(request,'sendDraft.html',context)

def save(request,mail):
    if request.method == 'POST':

        receiver = request.POST['receiver']
        if validate_receiver(receiver):
            body =request.POST.get('body')
            sub = request.POST.get('sub')
            date = datetime.datetime.today()
            if 'file' in request.FILES:
                file = request.FILES['file']
            else:
                file = None
            mail = Mail_detail(sender=mail,receiver=receiver,file=file,in_inbox=0,in_outbox=0,is_draft=1, subject= sub,body=body,date=date)
            mail.save()
            print("-------------------------------------saved--------------------------------")
            messages.success(request, 'Saved to drafts !')
        else:
            messages.info(request,"recipients Id is not valid !")
    return render(request,'drafts.html')

def view(request, mid,coming_from):
    data = Mail_detail.objects.filter(id=mid).first()
    context = dict()
    context['mid'] = data.id
    context['receiver'] = data.receiver
    context['body'] = data.body
    context['sender'] = data.sender
    context['sub'] = data.subject
    context['file'] = data.file
    context['is_draft'] = data.is_draft
    context['date'] = datetime.datetime.today()
    context['coming_from'] = coming_from

    return render(request,'view.html',context)

def delete(request,mid,val):
    try:
        if val == 'inbox':
            inbox_value = Mail_detail.objects.get(id=mid)
            outbox_value = Mail_detail.objects.get(id=mid)
            if not outbox_value.in_outbox:
                Mail_detail.objects.filter(id=mid).delete()
                messages.warning(request, 'Email deleted from Database!')
            else:
                inbox_value.in_inbox = False
                inbox_value.save()
                messages.warning(request, 'Email deleted from Inbox!')
        elif val == 'outbox':
            outbox_value = Mail_detail.objects.get(id=mid)
            inbox_value = Mail_detail.objects.get(id=mid)
            if not inbox_value.in_inbox:
                Mail_detail.objects.filter(id=mid).delete()
                messages.warning(request, 'Email deleted !')
            else:
                outbox_value.in_outbox = False
                outbox_value.save()
                messages.warning(request, 'Email deleted From outbox!')
        else:
            Mail_detail.objects.filter(id=mid).delete()
            messages.warning(request, 'Email deleted !')
        return redirect('/app')
    except Exception as e:
        return HttpResponse(f"{e}")

