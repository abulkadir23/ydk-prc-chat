from django.shortcuts import render
from django.contrib.auth.decorators import login_required

@login_required
def spare_parts_list(request):
    return render(request, 'spare_parts/list.html') 