from django.shortcuts import render
from django.shortcuts import render
from rest_framework import viewsets, permissions
from plotly.offline import plot
import plotly.graph_objs as graph_objs
import random

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
    projects = Project.objects.all()
    reviews = Review.objects.all()
    project_values = projects.values("name", "id")
    defect_values = defects.values("whereFound", "id", "projectID")
    review_values = reviews.values("dateOpened")

    colors = ["red", "green", "blue", "orange"]
    fig = graph_objs.Figure()

    for proj_val in project_values:
        name = proj_val["name"]

        counts = dict()
        for i in range(len(phase_type_values)):
            counts[i] = 0

        for defect in defect_values:
            if defect["projectID"] == proj_val["id"]:
                counts[defect['whereFound']-1] += 1

        if colors:
            my_color = random.choice(colors)
            colors.remove(my_color)
        else:
            my_color = "black"

        new_scatter = graph_objs.Bar(x=phase_type_values, y=list(counts.values()),
            name=name,
            opacity=0.8, marker_color=my_color
        )
        fig.add_trace(new_scatter)


        new_scatter = graph_objs.Scatter(x=phase_type_values, y=list(counts.values()))

    fig.update_layout(title="Defects Where Found",
                    xaxis_title="Phases",
                    yaxis_title="Defects")

    fig2 = graph_objs.Figure()

    counts = dict()
    for i in range(1, 13):
        counts[i] = 0

    for review in review_values:
        review_month = review["dateOpened"].month
        counts[review_month] += 1
    for i in range(1, 13):
        if not counts[i]:
            del counts[i]

    months = ["January", "February", "March", "April", "May", "June", "July", "August", "September", "October", "November", "December"]
    new_scatter = graph_objs.Scatter(x=months, y=list(counts.values()))
    fig2.add_trace(new_scatter)
    fig2.update_layout(title="Reviews over time",
                    xaxis_title="Months",
                    yaxis_title="Reviews")
    context['graph'] = plot(fig, output_type='div', include_plotlyjs=False, show_link=False, link_text="")
    context['graph2'] = plot(fig2, output_type='div', include_plotlyjs=False, show_link=False, link_text="")
    
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
