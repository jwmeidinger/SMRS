
from django.shortcuts import render, get_object_or_404, redirect
from django.core.paginator import Paginator
from rest_framework import viewsets, permissions
from plotly.offline import plot
import plotly.graph_objs as graph_objs
import datetime
import random

from restAPI.models import Project, Review, Defect, ProjectNumber, PhaseType
from account.models import Team, Account 
from dashboard.forms import DefectForm, ReviewForm
from dashboard.graphs import *

'''
*** Splash page
'''
## TODO: Need to Figure out a better way to Create custom graphs or make all the ones they want and let them select them.
def home_view(request):
    context= {}
    start_date = None
    end_date = None

    if request.POST:
        start_date = request.POST["startDate"]
        end_date = request.POST["endDate"]

    # Set default end date to be right now
    if not end_date:
        end_date = datetime.date.today()

    # Set default start date to be one year before end date (if applicable)
    if not start_date:
        if type(end_date) != datetime.date:
            end_date = datetime.datetime.strptime(end_date, '%Y-%m-%d').date()
        start_date = end_date
        start_date = start_date.replace(year=end_date.year-1)

    # Convert strings to dates
    if type(start_date) != datetime.date:
        start_date = datetime.datetime.strptime(start_date, "%Y-%m-%d").date()
    if type(end_date) != datetime.date:
        end_date = datetime.datetime.strptime(end_date, "%Y-%m-%d").date()

    context['startDate'] = start_date
    context['endDate'] = end_date
    context['graph'] = DefectsWhereFound(start_date=start_date, end_date=end_date)
    context['graph2'] = ReviewsOverTime(start_date=start_date, end_date=end_date)
    context['graph3'] = PostReleaseDefects(start_date=start_date, end_date=end_date)
    # context['graph'] = AllDefectsTable(start_date=start_date, end_date=end_date)
    context['graph'] = ContainmentPieChart(start_date=start_date, end_date=end_date)
    
    ##TODO: need to add Date to Date
    
    user = request.user
    if user.is_authenticated:
        context['message'] = 'Welcome to the Dashboard'

    return render(request, "dashboard/home.html", context)

'''
*** User's Team, members, and Projects
'''
def team_view(request):
    context= {}
    user = request.user
    if user.is_authenticated:
        team = Team.objects.filter(pk = user.teamid.pk).first()
        allmembers = Account.objects.filter(teamid = team)
        projectsOfTeam = Project.objects.filter(teamID = team)
        context['TeamName'] = team.name
        context['TeamMembers'] = allmembers
        context['projectList'] = projectsOfTeam
    return render(request, "dashboard/team.html", context)

'''
*** User's Personally selected Projects
'''
def project_view(request):
    context= {}
    user = request.user
    if user.is_authenticated:
        value = request.COOKIES.get('FavoriteProjects')
        if value != None: ## Browser never on the page before
            favs = set(value.split(","))
            blankspace  = ",".join(favs)
            if blankspace != "": ## if empty don't make a request to DB
                favoriteProjects = Project.objects.filter(pk__in = favs ).all()
                context["FavProjects"]= favoriteProjects

        team= Team.objects.filter(pk=user.teamid.pk).first()
        projects = Project.objects.filter(teamID=team)
    
        context["projects"]=projects
        context["team"]=team.name
    return render(request, "dashboard/projects.html", context)

'''
*** User's Personally selected Projects
'''
## TODO: Need to add Graph and Table
def projectDetail_view(request, pk):
    context= {}
    user = request.user
    
    project_detail = get_object_or_404(Project, pk=pk) # Get the project info
    allDefects = Defect.objects.filter(projectID=project_detail) # Get the Defects of project
    allReviews = Review.objects.filter(projectID=project_detail) # Get the Reviews of project

    ## This allows to have pages of items 
    paginator = Paginator(allDefects, 15) ## To switch items per page change the number
    try: # If no items
        page = int(request.GET.get('page', '1'))
    except:
        page = 1
    try:# If page is not found
        allDefects = paginator.page(page)
    except:
        allDefects = paginator.page(paginator.num_pages)

    ## Used to filter open Defects
    if request.POST:
        if request.POST["defectCheck"] != "0":
            openDefects = Defect.objects.filter(projectID=project_detail, dateClosed__isnull=True)
            context['openDefects'] = openDefects

    ## Setting items to the template
    context['allDefects'] = allDefects
    context['allReviews'] = allReviews
    context['projectName'] = project_detail.name
    return render(request, "dashboard/project_detail.html", context)

'''
*** User's Favorite Projects
'''
def projectAddFav_view(request, pk):
    value = request.COOKIES.get('FavoriteProjects')
    projectpk = pk ## have to declare before response
    response = redirect("dashboard:project_team")
    if value == None or value == "": ## No Favorite set yet
        response.set_cookie('FavoriteProjects', '{}'.format(projectpk))
    else: ## Have Favorite
        value += ",{}".format(projectpk)
        items = list(value.split(","))
        setOfElems = set()
        for elem in items:
            if elem in setOfElems:
                print("double")
            else:
                setOfElems.add(elem)         
        final  = ",".join(setOfElems) ## back to string
        response.set_cookie('FavoriteProjects', final)
    return response


'''
*** User's Removes Favorite Projects
'''
def projectDelFav_view(request, pk):
    value = request.COOKIES.get('FavoriteProjects')
    projectpk = pk
    items = set(value.split(','))
    items.remove("{}".format(projectpk))
    response = redirect("dashboard:project_team")
    final  = ",".join(items)
    response.set_cookie('FavoriteProjects', final)
    return response

'''
*** All Projects viewable by everyone
'''
def projectAll_view(request):
    context= {}
    projects = Project.objects.all()

    ## This allows to have pages of items 
    paginator = Paginator(projects, 20) ## To switch items per page change the number
    try: # If no items
        page = int(request.GET.get('page', '1'))
    except:
        page = 1
    try:# If page is not found
        projects = paginator.page(page)
    except:
        projects = paginator.page(paginator.num_pages)

    context["projects"] = projects
    
    if request.POST:
        filterItem = request.POST.get('filterItem')
        filterInput = request.POST.get('filterInput')
        if filterItem == "projectName":
            projects = Project.objects.filter(name=filterInput).all()
        if filterItem == "projectTeam":
            teamID = Team.objects.filter(name=filterInput).first()
            projects = Project.objects.filter(teamID=teamID).all()
        if filterItem == "projectOwner":
            productOwner = Account.objects.filter(name=filterInput).first()
            projects = Project.objects.filter(productOwner=productOwner).all()
        if filterItem == "projectPk":
            projects = Project.objects.filter(pk=int(filterInput)).all() 

    context["projects"] = projects
    return render(request, "dashboard/project_all.html", context)

'''
*** User's Personally selected Projects
'''
def defect_view(request, pk):
    context= {}
    user = request.user
    if not user.is_authenticated:
        return redirect("account:login")
    
    currentDefect = Defect.objects.filter(pk = pk).first()
    project = Project.objects.filter(pk = currentDefect.projectID.pk).first()

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
            if project.productOwner == user or user.is_admin:
                form.save()
                context["success_message"] = "Updated"
            else:
                context["success_message"] = "Must be Product Owner or Admin"
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
def review_view(request, pk):
    context= {}
    user = request.user
    if not user.is_authenticated:
        return redirect("account:login")
    
    currentReview = Review.objects.filter(pk = pk).first()
    project = Project.objects.filter(pk = currentReview.projectID.pk).first()

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
            if project.productOwner == user or user.is_admin:
                form.save()
                context["success_message"] = "Updated"
            else:
                context["success_message"] = "Must be Product Owner or Admin"
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

'''
*** Information on website
'''
def about_view (request):
    context= {}

    return render(request, "dashboard/about.html", context)