from django.shortcuts import get_object_or_404
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST, require_GET
import json
from .models import SerialNumber, Stage, StageCompletion
from django.db import transaction
from django.utils import timezone

@csrf_exempt
@require_POST
def update_stage(request):
    try:
        data = json.loads(request.body)
        serial_number = data.get('serial_number')
        stage = data.get('stage')
    except json.JSONDecodeError:
        return JsonResponse({'message': 'Invalid JSON'}, status=400)
    
    if not serial_number or not stage:
        return JsonResponse({'message': 'Missing serial_number or stage'}, status=400)
    
    stage_order = ['Qr1', 'Qr2', 'Qr3']
    if stage not in stage_order:
        return JsonResponse({'message': 'Invalid stage'}, status=400)
    
    serial = get_object_or_404(SerialNumber, serial_number=serial_number)
    
    stage_completion, _ = StageCompletion.objects.get_or_create(serial_number=serial)
    
    current_stage_index = stage_order.index(stage)
    if current_stage_index > 0:
        previous_stage = stage_order[current_stage_index - 1]
        previous_stage_obj = Stage.objects.filter(serial_number=serial, stage=previous_stage).first()
        
        if not previous_stage_obj or not previous_stage_obj.completed:
            return JsonResponse({'message': f'Previous stage ({previous_stage}) not completed'}, status=400)
    
    with transaction.atomic():
        stage_obj, created = Stage.objects.get_or_create(serial_number=serial, stage=stage)
        
        if stage_obj.completed:
            return JsonResponse({'message': 'Stage already completed'}, status=200)
        
        stage_obj.completed = True
        stage_obj.time = timezone.now()
        stage_obj.save()
        
        now = timezone.now()  
        if stage == 'Qr1':
            stage_completion.qr1_completed = True
            stage_completion.qr1_completed_time = now
        elif stage == 'Qr2':
            stage_completion.qr2_completed = True
            stage_completion.qr2_completed_time = now
        elif stage == 'Qr3':
            stage_completion.qr3_completed = True
            stage_completion.qr3_completed_time = now
        
        stage_completion.save()
    
    return JsonResponse({
        'message': 'Stage updated successfully' if not created else 'Stage created and marked as completed'
    }, status=200 if not created else 201)

@require_GET
def get_all_stage_completions(request):
    stage_completions = StageCompletion.objects.all()
    
    data = []
    for completion in stage_completions:
        data.append({
            'serial_number': completion.serial_number.serial_number,
            'qr1_completed': completion.qr1_completed,
            'qr1_completed_time': completion.qr1_completed_time.isoformat() if completion.qr1_completed_time else None,
            'qr2_completed': completion.qr2_completed,
            'qr2_completed_time': completion.qr2_completed_time.isoformat() if completion.qr2_completed_time else None,
            'qr3_completed': completion.qr3_completed,
            'qr3_completed_time': completion.qr3_completed_time.isoformat() if completion.qr3_completed_time else None
        })
    
    return JsonResponse(data, safe=False, status=200)
