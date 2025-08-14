from .models import Culture
from paliwalsamaj.settings import SHOW_GOPAL_BRANDING


def culture_menu_items(request):
    return {
        'all_cultures': Culture.objects.all().order_by('rank')
    }

def show_gopal_branding(request):
    return {'show_gopal_branding': SHOW_GOPAL_BRANDING}