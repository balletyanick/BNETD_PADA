from myapp.models import publicites  

def publicite_context(request):
    try:
        pub = publicites.objects.first()  
    except publicites.DoesNotExist:
        pub = None
    return {'publicite_globale': pub}
