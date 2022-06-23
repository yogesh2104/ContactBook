from pickletools import read_uint1
import re
from django.shortcuts import render, redirect
from .models import Contact

# Create your views here.

def index(request):
    contacts = Contact.objects.all()
    search_input = request.GET.get('search-area')
    if search_input:
        contacts = Contact.objects.filter(full_name__icontains=search_input)
    else:
        contacts = Contact.objects.all()
        search_input = ''
    return render(request, 'index.html', {'contacts': contacts, 'search_input': search_input})
 
def addContact(request):
    if request.method == 'POST':
        # new_contact = Contact(
        #     full_name=request.POST['fullname'],
        #     relationship=request.POST['relationship'],
        #     email=request.POST['email'],
        #     phone_number=request.POST['phone-number'],
        #     address=request.POST['address'],
        #     )
        new_contact=Contact()
        new_contact.full_name=request.POST.get('fullname')
        new_contact.relationship=request.POST.get('relationship')
        new_contact.email=request.POST.get('email')
        new_contact.phone_number=request.POST.get('phone-number')
        new_contact.imgs=request.POST.get('image')
        new_contact.address=request.POST.get('address')
        if len(request.FILES)!=0:
            new_contact.imgs=request.FILES['image']
        new_contact.save()
        return redirect('/')

    return render(request, 'new.html')

def editContact(request, pk):
    contact = Contact.objects.get(id=pk)
    if request.method == 'POST':
        contact.full_name = request.POST['fullname']
        contact.relationship = request.POST['relationship']
        contact.email = request.POST['email']
        contact.phone_number = request.POST['phone-number']
        contact.address = request.POST['address']
        contact.save()

        return redirect('/profile/'+str(contact.id))
    return render(request, 'edit.html', {'contact': contact})

def deleteContact(request, pk):
    contact = Contact.objects.get(id=pk)

    if request.method == 'POST':
        contact.delete()
        return redirect('/')

    return render(request, 'delete.html', {'contact': contact})

def contactProfile(request, pk):
    contact = Contact.objects.get(id=pk)
    return render(request, 'contact-profile.html', {'contact':contact})