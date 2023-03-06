from django.urls import path
from api.views.cost_view import get_total_cost, get_profiles_cost_per_day, get_profile_cost_per_day, get_day_ice_amount
from api.views.setup_view import init_multithreading, delete_setup, get_setup_status

urlpatterns = [
    path('setup', get_setup_status, name="Get The Wall status"),
    path('setup/multithread', init_multithreading, name="Init The Wall with multithread mode"),
    path('setup/reset', delete_setup, name="Reset The Wall"),
    path('cost', get_total_cost, name="Total wall cost"),
    path('day/<int:day>/cost', get_profiles_cost_per_day, name="Profile cost"),
    path('<int:profile>/day/<int:day>/cost', get_profile_cost_per_day, name="Profile cost per day"),
    path('<int:profile>/day/<int:day>', get_day_ice_amount, name="Ice amount per day"),
]
