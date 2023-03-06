from pathlib import Path
from django.http import JsonResponse
from django.db import transaction
from api.db_logger import DbLoger

from api.models.setup_model import SetupModel

from rest_framework.decorators import api_view
from rest_framework import serializers, status
from rest_framework.response import Response
from api.models.work_model import WorkExpenseModel
from thewall.domains import Team, WallSection
from thewall.logs.file_log import FileLog
from thewall.team_pool import Task, TeamPool

STATIC_SETUP_ID = 1

class SetupSerializer(serializers.ModelSerializer):
    class Meta:
        model = SetupModel
        fields = ["done"]

class MutlithreadInitSerializer(serializers.ModelSerializer):
    class Meta:
        model = SetupModel
        fields = ["done"]

class MultithreadInitSerializer(serializers.Serializer):
    teams = serializers.IntegerField()
    profiles = serializers.ListField(
        child=serializers.ListField(
            child=serializers.IntegerField(min_value=1, max_value=30),
            min_length=1,
            max_length=2000
        ),
        min_length=1
    )
    team_power_per_day = serializers.IntegerField(required=False)
    team_sleep_per_foot = serializers.FloatField(required=False)


@api_view(["POST"])
@transaction.atomic
def init_multithreading(request):
    try:
        setup = SetupModel.objects.get(pk=STATIC_SETUP_ID)
    except SetupModel.DoesNotExist:
        setup = None
    if setup and setup.done:
        response_data = {
            "error": "App already setted up. Call DELETE /setup/reset to use it again."
        }
        return JsonResponse(response_data, status=status.HTTP_409_CONFLICT)
    
    serializer = MultithreadInitSerializer(data=request.data)
    if not serializer.is_valid():
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        
    SetupModel(id=STATIC_SETUP_ID, done=True).save()
    
    sections = [
        Task(
            profile_id=profile_id, 
            section=WallSection(
                id=section_id,
                current_height=current_height
            )
        ) for profile_id, profile in enumerate(request.data["profiles"], start=1) for section_id, current_height in enumerate(profile, start=1)]
    
    teams = [
        Team(
            id=str(i), 
            power=request.data.get("team_power_per_day", 1),
            _sleep=request.data.get("team_sleep_per_foot", 0.1) # sec
        ) for i in range(1, request.data["teams"] + 1)
    ]
    db_logger = DbLoger()
    tmp_log_file = Path('./.tmp.log.txt')
    tmp_file_logger = FileLog(tmp_log_file)
    with TeamPool(teams=teams, loggers=[db_logger, tmp_file_logger]) as team_pool:
        team_pool.process(tasks=sections)
    logs = [line for line in tmp_log_file.read_text().split('\n') if line]
    if tmp_log_file.exists():
        tmp_log_file.unlink()
    return JsonResponse({"setup": True, "logs": logs}, status=status.HTTP_200_OK)


@api_view(["DELETE"])
@transaction.atomic 
def delete_setup(request):
    SetupModel.objects.all().delete()
    WorkExpenseModel.objects.all().delete()
    return JsonResponse({"deleted": True}, status=status.HTTP_200_OK)


@api_view(["GET"])
def get_setup_status(request):
    try:
        setup = SetupModel.objects.get(pk=STATIC_SETUP_ID)
    except SetupModel.DoesNotExist:
        setup = None
    return JsonResponse({"setup": bool(setup and setup.done)}, status=status.HTTP_200_OK)