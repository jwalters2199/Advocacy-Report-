from app import app
from static import constants as C
from static import dataframe_init as D

import plotly.graph_objects as go
import textwrap

BAR_COLORS = ['rgba(102, 0, 0, 0.8)', 'rgba(204, 0, 0, 0.8)', 'rgba(234, 153, 153, 0.8)', 'rgba(217, 217, 217, 0.8)', 'rgba(164, 194, 244, 0.8)', 'rgba(60, 120, 216, 0.8)', 'rgba(28, 69, 135, 0.8)']

def is_sample_size_insufficient(dff, q_id, axis):
    # get number of responses per category
    category_counts = dff[dff[q_id].notna()][axis].value_counts().reset_index(name='counts')['counts'].tolist()
    # check number of responses per category is greater than minimum sample size
    return any(c < C.MIN_SAMPLE_SIZE for c in category_counts)

def calculate_percentages(dff, q_id, axis, y_data, legend_labels):
    data = []
    for y_label in y_data:
        filt_dff = dff[dff[axis] == y_label]
        eval_counts = []
        total = 0
        row = []
        for eval_label in legend_labels:
            count = filt_dff[filt_dff[q_id] == eval_label].shape[0]
            eval_counts.append(count)
            total += count
        for count in eval_counts:
            value = 0
            if total != 0:
                value = round(count * 100 / total, 2)
            row.append(value)
        data.append(row)
    return data

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
    dff = filter_df(D.AXIS_DF[axis], gender_filter, race_ethnicity_filter, bgltq_filter,
        fgli_filter, class_year_filter, school_filter, concentration_filter)
    # return empty plot if there is not enough data
    if is_sample_size_insufficient(dff, q_id, axis):
        return C.EMPTY_FIGURE

    fig = go.Figure()
    y_data = dff[axis].unique()[::-1]

    legend_labels = ['Strongly disagree', 'Disagree', 'Somewhat disagree', 'Neither agree nor disagree',
        'Somewhat agree', 'Agree', 'Strongly agree']
    if q_id in list(C.URL_SLUGS['/explore/cs-knowledge']['question_id'].keys()):
        legend_labels = ['Significantly less knowledgeable', 'Less knowledgeable',
            'Slightly less knowledgeable', 'Similarly knowledgeable', 'Slightly more knowledgeable',
            'More knowledgeable', 'Significantly more knowledgeable']
    x_data = calculate_percentages(dff, q_id, axis, y_data, legend_labels)

    is_first_category = True
    for row in range(len(x_data)):
        for col in range(len(x_data[0])):
            hovertext = str(x_data[row][col]) + '% - ' + legend_labels[col]
            fig.add_trace(go.Bar(
                x=[x_data[row][col]], y=[row],
                orientation='h',
                hoverinfo='text',
                hovertext=hovertext,
                name=legend_labels[col],
                marker=dict(
                    color=BAR_COLORS[col],
                    line=dict(color='rgb(248, 248, 249)', width=1)
                ),
                showlegend = is_first_category
            ))
        is_first_category = False

    fig.update_layout(
        xaxis=dict(
            showgrid=False,
            showline=False,
            showticklabels=True,
            zeroline=False,
            domain=[0.15, 1]
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
        margin=dict(l=0, r=0, t=20, b=30),
        legend=dict(
            traceorder="normal"
        )
    )

    annotations = []
    for i in range(len(y_data)):
        # labeling the y-axis
        split_label = textwrap.wrap(str(y_data[i]), width=11)
        annotations.append(dict(xref='paper',
                                yref='y',
                                x=0.13, y=i,
                                xanchor='right',
                                text='<br>'.join(split_label),
                                font=dict(
                                    size=12
                                ),
                                showarrow=False,
                                align='right'))

    fig.update_layout(annotations=annotations, height=300)

    return fig
