from django.shortcuts import render
from upload.forms import DocumentForm 

# Create your views here.
from django.http import HttpResponse

def index(request):
    if request.method == 'POST':
        forms = DocumentForm(request.POST, request.FILES)
        for form in forms: #Description, data, labels
            if form.is_valid():
                form.save()
                #handle_uploaded_file(request.FILES['file'])
        return redirect('')
    else:
        form = DocumentForm()
    return render(request, 'upload.html', {
        'form': form
    })
