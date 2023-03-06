from django.http import JsonResponse


from rest_framework.decorators import api_view
from rest_framework import status
from api.models.work_model import WorkExpenseModel


FOOT_YARDS = 195
CUBIC_YARDS_COST = 1900


@api_view(["GET"])
def get_day_ice_amount(request, profile: int, day: int):
    objects = WorkExpenseModel.objects.filter(profile=profile, day=day)
    ice_amount = sum([obj.ice for obj in objects])
    return JsonResponse({"day": day, "ice_amount": ice_amount * FOOT_YARDS}, status=status.HTTP_200_OK)


@api_view(["GET"])
def get_total_cost(request):
    objects = WorkExpenseModel.objects.filter()
    cost = sum([obj.ice for obj in objects]) * FOOT_YARDS * CUBIC_YARDS_COST
    return JsonResponse({"day": None, "cost": cost}, status=status.HTTP_200_OK)

@api_view(["GET"])
def get_profiles_cost_per_day(request, day: int):
    objects = WorkExpenseModel.objects.filter(day=day)
    cost = sum([obj.ice for obj in objects]) * FOOT_YARDS * CUBIC_YARDS_COST
    return JsonResponse({"day": None, "cost": cost}, status=status.HTTP_200_OK)


@api_view(["GET"])
def get_profile_cost_per_day(request, profile: int, day: int):
    objects = WorkExpenseModel.objects.filter(profile=profile, day=day)
    cost = sum([obj.ice for obj in objects]) * FOOT_YARDS * CUBIC_YARDS_COST
    return JsonResponse({"day": None, "cost": cost}, status=status.HTTP_200_OK)