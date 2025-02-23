from django.shortcuts import render, get_object_or_404
from .serializers import JobSerializer
from .models import Job
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from django.db.models import Sum, Avg, Count, Min, Max


@api_view(['GET'])
def get_all_jobs(request):
    jobs = Job.objects.filter(is_soft_deleted=False)
    serializer = JobSerializer(jobs, many=True)
    return Response(serializer.data, status=status.HTTP_200_OK)


@api_view(['GET'])
def get_job(request, pk):
    job = get_object_or_404(Job, pk=pk)
    serializer = JobSerializer(job, many=False)
    return Response(serializer.data, status=status.HTTP_200_OK)

@api_view(['POST'])
def create_job(request):
    data = request.data
    try:
        company = data['company']
    except:
        return Response(data={'error': 'Company name is required!'}, status=status.HTTP_400_BAD_REQUEST)
    
    data['company'] = company.upper()
    
    job = Job.objects.create(**data)
        # title=data['title'],
        # description=data['description'],
        # email=data['email'],
        # address=data['address'],
        # job_type=data['job_type'],
        # education=data['education'],
        # industry=data['industry'],
        # experience=data['experience'],
        # salary=data['salary'],
        # position=data['position'],
        # company=company,
        # last_date=data['last_date'],
        # user=request.user
    
    serializer = JobSerializer(job, many=False)
    return Response(serializer.data, status=status.HTTP_201_CREATED)

@api_view(['PUT'])
def update_job(request, pk):
    job = get_object_or_404(Job, pk=pk)
    job.title = request.data['title']
    # job.description = request.data['description']
    # job.email = request.data['email']
    # job.address = request.data['address']
    # job.job_type = request.data['job_type']
    # job.education = request.data['education']
    # job.industry = request.data['industry']
    # job.experience = request.data['experience']
    # job.salary = request.data['salary']
    # job.position = request.data['position']
    # job.company = request.data['company']
    # job.last_date = request.data['last_date']
    job.save()
    
    serialzier = JobSerializer(job, many=False)
    return Response(serialzier.data, status=status.HTTP_200_OK)

@api_view(['DELETE'])
def delete_job(request, pk):
    job = get_object_or_404(Job, pk=pk)
    if job.is_soft_deleted:
        return Response(data={'error': 'Job is already deleted!'}, status=status.HTTP_400_BAD_REQUEST)
    job.is_soft_deleted = True
    job.save()
    return Response(data={'message': 'Job deleted successfully!'}, status=status.HTTP_200_OK)

@api_view(['DELETE'])
def destroy_job(request, pk):
    job = get_object_or_404(Job, pk=pk)
    job.delete()
    return Response(data={'message': 'Job deleted successfully!'}, status=status.HTTP_200_OK)



@api_view(['GET'])
def get_topic_search(request, topic):
    args = {'title__icontains': topic}
    jobs = Job.objects.filter(**args)
    
    if len(jobs) == 0:
        return Response(data={'error': f'No job found with topic: {topic}'}, status=status.HTTP_404_NOT_FOUND)
    
    stats = jobs.aggregate(
        total_jobs=Count('title'),
        avg_position=Avg('position'),
        avg_salary=Avg('salary'),
        min_salary=Min('salary'),
        max_salary=Max('salary'),
    )
    
    return Response(data={'stats': stats}, status=status.HTTP_200_OK)
    