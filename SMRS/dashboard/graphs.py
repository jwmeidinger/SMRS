from plotly.offline import plot
import plotly.graph_objs as graph_objs
import datetime

from django.db.models import Max, Min
from restAPI.models import Project, Review, Defect, Product, PhaseType

def OpenDefectsTable(date_range=None):
    # Filter based on this range
    defects = Defect.objects.all()
    defects = defects.filter(dateClosed=None)
    if date_range:
        defects = defects.filter(dateOpened__range=date_range)
    defect_values = defects.values("id", "dateOpened", "projectID", "whereFound", "tag", "severity", "url", "description")
    if not defect_values:
        return None
    
    # Create a dictionary wherer project ids correlate to project names
    projects = Project.objects.all()
    project_values = projects.values("id", "name")
    project_dict = dict()
    for project in project_values:
        proj_id = project["id"]
        proj_name = project["name"]
        project_dict[proj_id] = proj_name

    phase_types = PhaseType.objects.all()
    phase_type_values = [val['phase_type'] for val in list(phase_types.values('phase_type'))]

    if date_range:
        start_date = date_range[0]
        end_date = date_range[1]
    else:
        start_date = defects.aggregate(Min('dateOpened'))["dateOpened__min"]
        end_date = defects.aggregate(Max('dateOpened'))["dateOpened__max"]

    cell_columns = dict()
    for key in defect_values[0].keys():
        cell_columns[key] = list()
        for defect in defect_values:
            if key == "projectID":
                proj_id = defect[key]
                proj_name = project_dict[proj_id]
                cell_columns[key].append(proj_name)
            elif key == "whereFound":
                phase_type_index = int(defect[key]) - 1
                phase_type = phase_type_values[phase_type_index]
                cell_columns[key].append(phase_type)
            else:
                cell_columns[key].append(defect[key])

    header = dict(values=list(defect_values[0].keys()))
    cells = dict(values=[col for col in cell_columns.values()])
    table = graph_objs.Table(header=header, 
                            cells=cells,)
    fig = graph_objs.Figure(data=[table])
    
    return plot(fig, output_type='div', include_plotlyjs=False, show_link=False, link_text="")

def OpenReviewsTable(date_range=None):
    # Filter based on this range
    reviews = Review.objects.all()
    reviews = reviews.filter(dateClosed=None)
    if date_range:
        reviews = reviews.filter(dateOpened__range=date_range)
    review_values = reviews.values()
    if not review_values:
        return None
    
    if date_range:
        start_date = date_range[0]
        end_date = date_range[1]
    else:
        start_date = reviews.aggregate(Min('dateOpened'))["dateOpened__min"]
        end_date = reviews.aggregate(Max('dateOpened'))["dateOpened__max"]

    cell_columns = dict()
    for key in review_values[0].keys():
        cell_columns[key] = list()
        for review in review_values:
            cell_columns[key].append(review[key])

    header = dict(values=list(review_values[0].keys()))
    cells = dict(values=[col for col in cell_columns.values()])
    table = graph_objs.Table(header=header, 
                            cells=cells,)
    fig = graph_objs.Figure(data=[table])
    
    return plot(fig, output_type='div', include_plotlyjs=False, show_link=False, link_text="")

def ContainmentPieChart(date_range=None):
    # Filter based on this range
    defects = Defect.objects.all()
    if date_range:
        defects = defects.filter(dateOpened__range=date_range)

    defect_values = defects.values("dateOpened", "whereFound")
    if not defect_values:
        return None
    
    if date_range:
        start_date = date_range[0]
        end_date = date_range[1]
    else:
        start_date = defects.aggregate(Min('dateOpened'))["dateOpened__min"]
        end_date = defects.aggregate(Max('dateOpened'))["dateOpened__max"]

    post_release_defects = 0

    for defect in defect_values:
        if defect["whereFound"] in [6, 7, 8]:
            post_release_defects += 1
    
    contained_defects = len(defect_values) - post_release_defects

    fig = graph_objs.Figure()
    trace = graph_objs.Pie(labels = ["Post Release Defects", "Contained Defects"], values = [post_release_defects, contained_defects])
    fig.add_trace(trace)

    return plot(fig, output_type='div', include_plotlyjs=False, show_link=False, link_text="")

def DefectsWhereFound(date_range=None, project_ID=None):

    # Filter based on input
    defects = Defect.objects.all()
    if date_range:
        defects = Defect.objects.filter(dateOpened__range=date_range)
    if project_ID:
        defects = defects.filter(projectID=project_ID)
    defect_values = defects.values("whereFound", "dateOpened", "id", "projectID")

    if not defect_values:
        return None

    if date_range:
        start_date = date_range[0]
        end_date = date_range[1]
    else:
        start_date = defects.aggregate(Min('dateOpened'))["dateOpened__min"]
        end_date = defects.aggregate(Max('dateOpened'))["dateOpened__max"]

    # Get phase types
    phase_type = PhaseType.objects.all()
    phase_type_values = [val['phase_type'] for val in list(phase_type.values('phase_type'))]

    # Create figure
    fig = graph_objs.Figure()
    defects_by_year = dict()

    # Loop per year
    for i in range(start_date.year, end_date.year+1):
        defects_by_year[i] = dict()
        for j in range(len(phase_type_values)):
            defects_by_year[i][j] = 0

    # find which phase each defect falls in
    for defect in defect_values:
        year = getFiscalYear(defect["dateOpened"])
        defects_by_year[year][defect["whereFound"]-1] += 1
        
    # Make bar graph scatter for each year
    for year, counts in defects_by_year.items():

        new_scatter = graph_objs.Bar(x=phase_type_values, y=list(counts.values()),
            name=year,
            opacity=0.8,
        )
        fig.add_trace(new_scatter)

    # Set figure details
    fig.update_layout(title="Defects Where Found",
                    xaxis_title="Phases",
                    yaxis_title="Defects",
                    margin=dict(l=0, r=0, b=0, t=0, pad=0))

    # Set y axis to show only integers
    fig.update_yaxes(
        tickformat="d"
    )

    # Generate graph object
    return plot(fig, output_type='div', include_plotlyjs=False, show_link=False, link_text="")


def ReviewsOverTime(date_range=None):
    reviews = Review.objects.all()
    if date_range:
        reviews = reviews.filter(dateOpened__range=date_range)
    review_values = reviews.values("dateOpened")
    if not review_values:
        return None

    if date_range:
        start_date = date_range[0]
        end_date = date_range[1]
    else:
        start_date = reviews.aggregate(Min('dateOpened'))["dateOpened__min"]
        end_date = reviews.aggregate(Max('dateOpened'))["dateOpened__max"]

    fig = graph_objs.Figure()

    counts_by_year = dict()

    for review in review_values:
        review_year = getFiscalYear(review["dateOpened"])
        if review_year not in counts_by_year:
            counts_by_year[review_year] = dict()
            for i in range(1, 13):
                counts_by_year[review_year][i] = 0

        counts = counts_by_year[review_year]
        review_month = review["dateOpened"].month
        counts[review_month] += 1

    months = ["November", "December", "January", "February", "March", "April", "May", "June", "July", "August", "September", "October"]
    max_on_graph = 0
    for year, counts in sorted(counts_by_year.items()):

        # make sure the review count increments with each passing month
        for i in [10, 11, 12] + list(range(1, 10)):
            if i == 12:
                counts[1] += counts[12]
            else:
                counts[i+1] += counts[i]
        
        # reorder the list of counts such that November and December come first
        count_output = list(counts.values())
        count_output = count_output[-2:] + count_output[:-2]

        max_on_graph = max(max_on_graph, count_output[-1])

        new_scatter = graph_objs.Scatter(x=months, y=count_output,
                                        name=year)
        fig.add_trace(new_scatter)

    fig.update_layout(title="Reviews over time",
                      xaxis_title="Months",
                      yaxis_title="Reviews",
                      yaxis=dict(range=[0, max_on_graph]))
    # Set x axis to show only integers
    fig.update_yaxes(
        tickformat="d"
    )
    graph = plot(fig, output_type='div', include_plotlyjs=False, show_link=False, link_text="")
    return graph

def PostReleaseDefects(date_range=None):
    defects = Defect.objects.all()
    if date_range:
        defects = defects.filter(dateOpened__range=date_range)
    defect_values = defects.values("dateOpened", "whereFound")

    total_defects = dict()
    post_release_defects = dict()

    for defect in defect_values:
        year = getFiscalYear(defect["dateOpened"])
        if year in total_defects.keys():
            total_defects[year] += 1
        else:
            total_defects[year] = 1
            post_release_defects[year] = 0

        if defect["whereFound"] in [6, 7, 8]:
            post_release_defects[year] += 1

    years = list(total_defects.keys())
    percentages = list()
    for year in years:
        percentages.append(post_release_defects[year]/total_defects[year]) 

    fig = graph_objs.Figure()
    new_scatter = graph_objs.Bar(x=years, y=percentages)
    fig.add_trace(new_scatter)

    fig.update_layout(title="Post Release Defects",
                      xaxis_title="Years",
                      yaxis=dict(range=[0, 1]),
                      yaxis_title="Percentage")

    # if there's only one bar, update title to show the year
    if len(years) == 1:
        fig.update_layout(xaxis_title=years[0])

    # Update x axis to show integers
    fig.update_xaxes(tickformat="d")

    # Update y axis to show integer percentages
    fig.update_yaxes(tickformat="%")

    graph = plot(fig, output_type='div', include_plotlyjs=False, show_link=False, link_text="")
    return graph

def getFiscalYear(date):
    if date.month in [11, 12]:
        return date.year + 1
    else:
        return date.year

def formatDates(start_date, end_date):
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
    if type(end_date) != datetime.date:
        end_date = datetime.datetime.strptime(end_date, "%Y-%m-%d").date()
    if type(start_date) != datetime.date:
        start_date = datetime.datetime.strptime(start_date, "%Y-%m-%d").date()
    
    return start_date, end_date
