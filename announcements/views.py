# announcements/views.py

from django.http import JsonResponse
from django.shortcuts import render
from .models import AnnouncementGroup, Announcement
from Users.decorators import verified_user_required

@verified_user_required
def announcements_view(request):
    group_names = []
    jnv_group_name = f"jnv_{request.user.usercard.jnv_name}".replace(' ','_')
    region_group_name = f"region_{request.user.usercard.region_name}".replace(' ','_')
    group_names.extend(['All',jnv_group_name,region_group_name])
    if request.user.usercard.role=='S' or request.user.usercard.role=='A':
        group_names.append(f"Batch_{request.user.usercard.jnv_name}_{request.user.usercard.year}".replace(' ','_'))
    
    group_list = []
    for group in group_names:
        group,created = AnnouncementGroup.objects.get_or_create(name=group)
        if group:
            group_list.append(group)
    
    chat = {}
    for group in group_list:
        obj = Announcement.objects.filter(group=group).order_by('timestamp')
        chat[group] = obj
    
    context = {'groups': group_list, 'chat': chat}
    return render(request, 'announcements.html', context)
