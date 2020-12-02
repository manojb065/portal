from django.urls import path

from .views import TeamCreate,TeamList,teamDetail,Filedelete,Fileupload,search,memeberTeam,delTeam

app_name = 'team'
urlpatterns = [
path('create/',TeamCreate,name="add"),
path('',TeamList,name="list"),
path('myteam/',memeberTeam,name="mlist"),
path('detial/<str:name>',teamDetail,name="detail"),
path('delf/<str:name>',Filedelete,name="del"),
path('upload/<str:name>',Fileupload,name='upload'),
path('search/',search,name="search"),
path('del/<int:id>',delTeam,name="teamdel"),

]