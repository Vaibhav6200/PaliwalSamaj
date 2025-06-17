from .models import Culture

def culture_menu_items(request):
    return {
        'all_cultures': Culture.objects.all()
    }
