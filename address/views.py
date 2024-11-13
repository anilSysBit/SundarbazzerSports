from django.shortcuts import render
from django.http import JsonResponse
from .models import Province, District, Municipality, Area

def load_districts(request):
    province_id = request.GET.get('province_id')
    districts = District.objects.filter(province_id=province_id).all()
    return JsonResponse(list(districts.values('id', 'name')), safe=False)

def load_municipalities(request):
    district_id = request.GET.get('district_id')
    municipalities = Municipality.objects.filter(district_id=district_id).all()
    return JsonResponse(list(municipalities.values('id', 'name')), safe=False)

def load_areas(request):
    municipality_id = request.GET.get('municipality_id')
    areas = Area.objects.filter(municipality_id=municipality_id).all()
    return JsonResponse(list(areas.values('id', 'name')), safe=False)