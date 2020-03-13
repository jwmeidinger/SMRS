from plotly.offline import plot
import plotly.graph_objs as graph_objs
import datetime

from restAPI.models import Project, Review, Defect, ProjectNumber, PhaseType

def AllDefectsTable(start_date, end_date):
    # Filter based on this range
    defects = Defect.objects.filter(dateOpened__range=[start_date, end_date]).all()
    defect_values = defects.values()
    if not defect_values:
        return None
    
    cell_columns = dict()
    for key in defect_values[0].keys():
        cell_columns[key] = list()
        for defect in defect_values:
            cell_columns[key].append(defect[key])

    print(cell_columns)
    header = dict(values=list(defect_values[0].keys()))
    cells = dict(values=[col for col in cell_columns.values()])
    table = graph_objs.Table(header=header, 
                            cells=cells,)
    fig = graph_objs.Figure(data=[table])
    
    return plot(fig, output_type='div', include_plotlyjs=False, show_link=False, link_text="")


def DefectsWhereFound(start_date, end_date):

    # Filter based on this range
    defects = Defect.objects.filter(dateOpened__range=[start_date, end_date]).all()
    defect_values = defects.values("whereFound", "dateOpened", "id", "projectID")

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
        defects_by_year[defect["dateOpened"].year][defect["whereFound"]-1] += 1
        
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
                    yaxis_title="Defects")

    # Generate graph object
    return plot(fig, output_type='div', include_plotlyjs=False, show_link=False, link_text="")


def ReviewsOverTime(start_date="2000-11-01", end_date=datetime.date.today()):
    reviews = Review.objects.filter(dateOpened__range=[start_date, end_date]).all()
    review_values = reviews.values("dateOpened")
    fig = graph_objs.Figure()

    counts_by_year = dict()

    for review in review_values:
        review_year = review["dateOpened"].year
        if review_year not in counts_by_year:
            counts_by_year[review_year] = dict()
            for i in range(1, 13):
                counts_by_year[review_year][i] = 0

        counts = counts_by_year[review_year]
        review_month = review["dateOpened"].month
        counts[review_month] += 1

    months = ["January", "February", "March", "April", "May", "June", "July", "August", "September", "October", "November", "December"]
    
    for year, counts in counts_by_year.items():
        for i in range(1, 12):
            counts[i+1] += counts[i]

        new_scatter = graph_objs.Scatter(x=months, y=list(counts.values()),
                                        name=year)
        fig.add_trace(new_scatter)

    fig.update_layout(title="Reviews over time",
                      xaxis_title="Months",
                      yaxis_title="Reviews")

    graph = plot(fig, output_type='div', include_plotlyjs=False, show_link=False, link_text="")
    return graph

def PostReleaseDefects(start_date="2000-11-01", end_date=datetime.date.today()):
    defects = Defect.objects.all()
    defect_values = defects.values("dateOpened", "whereFound")

    total_defects = dict()
    post_release_defects = dict()

    for defect in defect_values:
        year = defect["dateOpened"].year
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
        percentages.append(100 * float(post_release_defects[year])/total_defects[year]) 
    
    
    fig = graph_objs.Figure()
    new_scatter = graph_objs.Bar(x=years, y=percentages)
    fig.add_trace(new_scatter)

    fig.update_layout(title="Post Release Defects",
                      xaxis_title="Years",
                      yaxis_title="Percentage")

    # Set x axis to show only integers
    fig.update_xaxes(
        tickformat="d"
    )
    fig.update_yaxes(ticksuffix="%")

    graph = plot(fig, output_type='div', include_plotlyjs=False, show_link=False, link_text="")
    return graph
