from django.shortcuts import render
from django.shortcuts import render
from rest_framework import viewsets, permissions
from plotly.offline import plot
import plotly.graph_objs as graph_objs

from restAPI.models import Project, Review, Defect, ProjectNumber, PhaseType
from account.models import Team, Account


'''
*** Splash page
'''

def home_view(request):
    context= {}

    phase_type = PhaseType.objects.all()
    phase_type_values = [val['phase_type'] for val in list(phase_type.values('phase_type'))]

    defects = Defect.objects.all()
    defect_values = defects.values("whereFound", "id")

    counts = dict()
    for i in range(len(phase_type_values)):
        counts[i] = 0

    for defect in defect_values:
        counts[defect['whereFound']-1] += 1

    #defect_values = [val['phase_type'] for val in list(defects.values('phase_type'))]
    #print(defect_values)

    fig = graph_objs.Figure()
    scatter = graph_objs.Bar(x=phase_type_values, y=list(counts.values()),
                        name='John Deere Graphs',
                        opacity=0.8, marker_color='green')
    scatter2 = graph_objs.Bar(x=phase_type_values, y=list(counts.values()),
                    name='John Deere Graphs',
                    opacity=0.8, marker_color='red')
    fig.add_trace(scatter)
    fig.add_trace(scatter2)
    plt_div = plot(fig, output_type='div', include_plotlyjs=False, show_link=False, link_text="")
    context['graph'] = plt_div

    user = request.user
    if user.is_authenticated:
        context['message'] = 'Welcome to the Dashboard'

    return render(request, "dashboard/home.html", context)

def project_view(request):
    context= {}
    user = request.user
    if user.is_authenticated:
        project = Project.objects.all()
    return render(request, "dashboard/projects.html", context)

def team_view(request):
    context= {}
    user = request.user
    if user.is_authenticated:
        team = Team.objects.filter(pk = user.pk)
    return render(request, "dashboard/team.html", context)

