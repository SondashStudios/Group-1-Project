from django.shortcuts import render

# This will render the checklist page
def checklist_view(request):
    return render(request, 'checklist.html')
