from app import app
from static import constants as C
from static import dataframe_init as D

import plotly.graph_objects as go
import textwrap

def is_sample_size_insufficient(dff, axis, q_id):
    # get number of responses per category
    category_counts = dff[dff[q_id].notna()][axis].value_counts().reset_index(name='counts')['counts'].tolist()
    # check number of responses per category is greater than minimum sample size
    return any(c < C.MIN_SAMPLE_SIZE for c in category_counts)

def filter_df(df, gender_filter, race_ethnicity_filter, bgltq_filter, fgli_filter, 
    class_year_filter, school_filter, concentration_filter):
    df = D.filter_gender(df, gender_filter)
    df = D.filter_race_ethnicity(df, race_ethnicity_filter)
    df = D.filter_bgltq(df, bgltq_filter)
    df = D.filter_fgli(df, fgli_filter)
    df = D.filter_class_year(df, class_year_filter)
    df = D.filter_school(df, school_filter)
    df = D.filter_conc(df, concentration_filter)
    return df

def generate_figure(q_id, axis, gender_filter, race_ethnicity_filter, bgltq_filter, fgli_filter, 
    class_year_filter, school_filter, concentration_filter):
    # get relevant dataframe according to axis
    dff = filter_df(D.AXIS_DF[axis], gender_filter, race_ethnicity_filter, bgltq_filter,
        fgli_filter, class_year_filter, school_filter, concentration_filter)
    # return empty plot if there is not enough data
    if is_sample_size_insufficient(dff, axis, q_id):
        return C.EMPTY_FIGURE
    # y is the categories under the selected axis
    axis_categories = dff[axis].unique()[::-1]
    
    if q_id == "Q8":
        choices = ["In elementary school (including summer after graduation)", 
                    "In middle school (including summer after graduation)",
                    "In high school (including summer after graduation)", "In college"]
        colors = ["rgb(10,54,34)", "rgb(20,108,67)", "rgb(71,159,118)", "rgb(162,207,187)"]
    elif q_id == "Q20":
        choices = ["No", "Not Decided", "Yes"]
        colors = ["rgb(227,93,106)", "rgb(255,205,57)", "rgb(71,159,118)"]
    elif q_id == "Q22":
        choices = ["No, I have not considered applying to graduate studies in CS", 
                    "Yes, I have considered but do not intend to apply to graduate studies in CS", 
                    "Yes, I have considered and intend to apply (or am currently applying) to graduate studies in CS"]
        colors = ["rgb(227,93,106)", "rgb(255,205,57)", "rgb(71,159,118)"]
    else:
        choices = []
        for i in dff[q_id].unique():
            choices.append(i)
        colors = ["rgb(220,53,69)", "rgb(255,193,8)", "rgb(25,135,84)"]

    fig = go.Figure()

    is_first_category = True
    for c in axis_categories:
        # dict to store the options and how many people chose it
        d = {}
        updated_dff = dff[dff[axis] == c]   
        # total number of respondents
        cat_total = 0
        for i in range(0, len(choices)):
            cat_total += updated_dff[updated_dff[q_id] == choices[i]].shape[0]

        for i in range(0, len(choices)):
            # for each option store the percentage of people that chose it
            d[choices[i]] = 0
            if cat_total != 0:
                d[choices[i]] = updated_dff[updated_dff[q_id] == choices[i]].shape[0] / cat_total * 100

            hovertext = str(round(d[choices[i]], 2)) + '% - ' + choices[i]
            fig.add_trace(go.Bar(
                y=[c],
                x=[d[choices[i]]],
                name=choices[i],
                orientation='h',
                hoverinfo='text',
                hovertext=hovertext,
                marker=dict(
                    color=colors[i],
                    line=dict(color='rgb(248, 248, 249)', width=1)
                ),
                showlegend = is_first_category
            ))
        is_first_category = False

    annotations = []
    for i in range(len(axis_categories)):
        # labeling the y-axis
        split_label = textwrap.wrap(str(axis_categories[i]), width=16)
        annotations.append(dict(xref='paper',
                                yref='y',
                                x=0.1, y=i,
                                xanchor='right',
                                text='<br>'.join(split_label),
                                font=dict(
                                    size=12
                                ),
                                showarrow=False,
                                align='right'))

    fig.update_layout(
        annotations=annotations,
        xaxis=dict(
            showgrid=False,
            showline=False,
            showticklabels=True,
            zeroline=False,
            domain=[0.11, 1]
        ),
        yaxis=dict(
            showgrid=False,
            showline=False,
            showticklabels=False,
            zeroline=False,
        ),
        barmode='stack',
        paper_bgcolor='white',
        plot_bgcolor='white',
        height=350,
        margin=dict(l=0, r=0, t=0, b=100),
        legend=dict(
            orientation="h",
            traceorder="normal",
            yanchor="top",
            y=-0.1,
            xanchor="left",
            x=-0.01
        )
    )
    
    return fig
