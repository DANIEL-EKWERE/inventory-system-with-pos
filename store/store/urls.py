# from django.contrib import admin
# from django.urls import path, include

# urlpatterns = [
#     path('admin/', admin.site.urls),
#     path('', include('core.urls')),
#     path('inventory/', include('inventory.urls')),
    
#     path('pos/', include('pos.urls')),
#     path('purchase/', include('purchase.urls')),
#     path('report/', include('report.urls')),
# ] 


from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('core.urls')),
    path('inventory/', include('inventory.urls')),
    path('pos/', include('pos.urls')),
    path('purchase/', include('purchase.urls')),
    path('report/', include('report.urls')),
]

