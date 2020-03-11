from plotly.offline import plot
import plotly.graph_objs as graph_objs
import datetime

from restAPI.models import Project, Review, Defect, ProjectNumber, PhaseType

def DefectsWhereFound(start_date="2000-11-01", end_date=datetime.date.today()):

    start_year = int(start_date.split("-")[0])
    end_year = end_date.year ## Need to also allow strings

    defects = Defect.objects.filter(dateOpened__range=[start_date, end_date]).all()
    phase_type = PhaseType.objects.all()

    defect_values = defects.values("whereFound", "dateOpened", "id", "projectID")
    phase_type_values = [val['phase_type'] for val in list(phase_type.values('phase_type'))]

    fig = graph_objs.Figure()
    defects_by_year = dict()

    for i in range(start_year, end_year+1):
        defects_by_year[i] = dict()
        for j in range(len(phase_type_values)):
            defects_by_year[i][j] = 0

    for defect in defect_values:
        defects_by_year[defect["dateOpened"].year][defect["whereFound"]-1] += 1

    for year, counts in defects_by_year.items():

        new_scatter = graph_objs.Bar(x=phase_type_values, y=list(counts.values()),
            name=year,
            opacity=0.8,
        )
        fig.add_trace(new_scatter)

    fig.update_layout(title="Defects Where Found",
                    xaxis_title="Phases",
                    yaxis_title="Defects")

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

    for counts in counts_by_year.values():
        for i in range(1, 12):
            counts[i+1] += counts[i]

        new_scatter = graph_objs.Scatter(x=months, y=list(counts.values()))
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

        if defect["whereFound"] == 8:
            post_release_defects[year] += 1

    years = list(total_defects.keys())
    percentages = list()
    for year in years:
        percentages.append(float(post_release_defects[year])/total_defects[year])


    fig = graph_objs.Figure()
    new_scatter = graph_objs.Bar(x=years, y=percentages)
    fig.add_trace(new_scatter)

    fig.update_layout(title="Reviews over time",
                      xaxis_title="Years",
                      yaxis_title="Percentage")

    graph = plot(fig, output_type='div', include_plotlyjs=False, show_link=False, link_text="")
    return graph
