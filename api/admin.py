from django.contrib import admin
from .models import Teams,Players,Games,Brands,Signed_contract,Player_Scores,Team_Scores
# Register your models here.
admin.site.register(Teams)
admin.site.register(Players)
admin.site.register(Games)
admin.site.register(Brands)
admin.site.register(Signed_contract)
admin.site.register(Player_Scores)
admin.site.register(Team_Scores)