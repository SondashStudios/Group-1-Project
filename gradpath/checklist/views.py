from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .models import ChecklistProgress

@login_required
def checklist_view(request):
    if request.method == "POST":
        # Clear old selections
        ChecklistProgress.objects.filter(user=request.user).delete()

        # Save the new selections
        selected_items = request.POST.getlist("moduleItemCheckboxInput")
        for item_id in selected_items:
            ChecklistProgress.objects.create(user=request.user, module_item_id=item_id)

        return redirect('checklist')  # Refreshing the page (prevents re-submitting on reload)

    # GET request – load saved progress
    saved_items = ChecklistProgress.objects.filter(user=request.user)
    selected_ids = [item.module_item_id for item in saved_items]

    return render(request, 'checklist.html', {'userSelections': selected_ids})
