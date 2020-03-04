
from django.shortcuts import render, get_object_or_404
from rest_framework import viewsets, permissions
from plotly.offline import plot
import plotly.graph_objs as graph_objs
import random

from restAPI.models import Project, Review, Defect, ProjectNumber, PhaseType
from account.models import Team, Account 
from dashboard.forms import DefectForm, ReviewForm


'''
*** Splash page
'''
## TODO: Need to Figure out a better way to Create custom graphs or make all the ones they want and let them select them.
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
    for i in range(2, 13):
        if counts[i]:
            counts[i] += counts[i-1]
        else:
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

'''
*** User's Team, members, and Projects
'''
## TODO: Need to Finish HTML and CSS
def team_view(request):
    context= {}
    user = request.user
    if user.is_authenticated:
        team = Team.objects.filter(pk = user.pk).first()
        allmembers = Account.objects.filter(teamid = team)
        projectsOfTeam = Project.objects.filter(teamID = team)
        context['TeamName'] = team.name
        context['TeamMembers'] = allmembers
        context['projectList'] = projectsOfTeam
    return render(request, "dashboard/team.html", context)

'''
*** User's Personally selected Projects
'''
## TODO: This needs to be done
def project_view(request):
    context= {}
    user = request.user
    if user.is_authenticated:
        project = Project.objects.all()
    return render(request, "dashboard/projects.html", context)

'''
*** User's Personally selected Projects
'''
## TODO: Need to Finish HTML and CSS
def projectDetail_view(request, pk):
    context= {}
    user = request.user
    if user.is_authenticated:
        project_detail = get_object_or_404(Project, pk=pk)
        allDefects = Defect.objects.filter(projectID=project_detail)
        allReviews = Review.objects.filter(projectID=project_detail)

        context['allDefects'] = allDefects
        context['allReviews'] = allReviews
    return render(request, "dashboard/project_detail.html", context)

'''
*** User's Personally selected Projects
'''
## TODO: Need Team Leader to be able to change items
def defect_view(request, pk):
    context= {}
    user = request.user
    if not user.is_authenticated:
        return redirect("acccount:login")
    
    currentDefect = Defect.objects.filter(pk = pk).first()
    if request.POST:
        form = DefectForm(request.POST, instance = currentDefect)
        if form.is_valid():
            form.initial = {
                "dateOpened": request.POST["dateOpened"],
                "dateClosed": request.POST["dateClosed"],
                "projectID" : request.POST["projectID"],
                "whereFound": request.POST["whereFound"],
                "tag"       : request.POST["tag"],
                "severity"  : request.POST["severity"],
                "url"       : request.POST["url"]
            }
            form.save()
            context["success_message"] = "Updated"
    else:
        form = DefectForm(
             initial = {
                "dateOpened": currentDefect.dateOpened,
                "dateClosed": currentDefect.dateClosed,
                "projectID" : currentDefect.projectID,
                "whereFound": currentDefect.whereFound,
                "tag"       : currentDefect.tag,
                "severity"  : currentDefect.severity,
                "url"       : currentDefect.url,
             }
        )
    context['form'] = form
    return render(request, "dashboard/defect_detail.html", context)

'''
*** User's Personally selected Projects
'''
## TODO: Need Team Leader to be able to change items
def review_view(request, pk):
    context= {}
    user = request.user
    if not user.is_authenticated:
        return redirect("acccount:login")
    
    currentReview = Review.objects.filter(pk = pk).first()

    if request.POST:
        form = ReviewForm(request.POST)
        if form.is_valid():
            form.initial = {
                "dateOpened": request.POST["dateOpened"],
                "dateClosed": request.POST["dateClosed"],
                "projectID" : request.POST["projectID"],
                "whereFound": request.POST["whereFound"],
                "tag"       : request.POST["tag"],
                "severity"  : request.POST["severity"],
                "url"       : request.POST["url"]
            }
            form.save()
            context["success_message"] = "Updated"
    else:
        form = ReviewForm(
             initial = {
                "dateOpened": currentReview.dateOpened,
                "dateClosed": currentReview.dateClosed,
                "projectID" : currentReview.projectID,
                "whereFound": currentReview.whereFound,
                "tag"       : currentReview.tag,
                "severity"  : currentReview.severity,
                "url"       : currentReview.url,
             }
        )
    context['form'] = form
    return render(request, "dashboard/review_detail.html", context)