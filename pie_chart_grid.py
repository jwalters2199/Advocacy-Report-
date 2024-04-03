from app import app
from static import constants as C
from static import dataframe_init as D

import plotly.graph_objects as go
from plotly.subplots import make_subplots

# constants
# column titles with formatting
COLUMN_TITLES = ['', 'For an <br> academic letter of <br> recommendation <br> <br>',
                    'To inquire <br> about research <br> opportunities <br> <br>',
                    'To inquire <br> about career <br> opportunities <br> <br>',
                    'To inquire <br> about advice for <br> my concentration <br> <br>']

# label names used to extract data
ANSWER_OPTIONS = ['For an academic letter of recommendation', 'To inquire about research opportunities',
                  'To inquire about career opportunities',  'To inquire about advice for my concentration']

def is_sample_size_insufficient(dff, q_id, axis):
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
    # extract relevant data
    dff = filter_df(D.AXIS_DF[axis], gender_filter, race_ethnicity_filter, bgltq_filter,
                    fgli_filter, class_year_filter, school_filter, concentration_filter)
    if is_sample_size_insufficient(dff, q_id, axis):
        return C.EMPTY_FIGURE

    columnOptions = []
    for choice in ANSWER_OPTIONS:
        columnOptions.append(dff[dff[q_id].str.contains(
            choice, na=False)])
            
    # names is used for labelling
    names = list(dff[axis].unique())

    # initialize subplot
    generateSpecs = [[{"type": "pie"} for _ in range(len(columnOptions)+1)] for _ in names]
    figSub = make_subplots(rows=len(names), cols=len(
        columnOptions)+1, specs=generateSpecs, column_titles=COLUMN_TITLES)
    rowNum = 1

    for label in names:
        colNum = 1
        # add row title
        figSub.add_trace(go.Table(
            header=dict(
                values=[label],
                fill_color='rgba(0,0,0,0)',
                font=dict(color='black', size=16), align='right'),
                cells=dict(
                    values=[' '],
                    fill_color='rgba(0,0,0,0)',
                    align='center'
                )),
            row=rowNum, col=colNum)
        colNum += 1

        # construct pie chart
        for colOption in columnOptions:
            votes = [0, 0]
            for x in colOption[axis]:
                if x == label:
                    votes[0] += 1
            total = dff[dff[axis] == label][q_id].count()
            votes[1] = total - votes[0]
            figSub.add_trace(
                go.Pie(
                    labels=['Yes', 'No'],
                    values=votes,
                    textinfo='none',
                    hoverinfo='label+percent',
                    direction = 'clockwise',
                    sort = False,
                    marker={
                        'colors': ['rgb(71,159,118)', 'rgb(233,236,239)']
                    }),
                row=rowNum, col=colNum)
            colNum += 1
        rowNum += 1

    # plot titles
    figSub.update_layout(
        margin=dict(l=0, r=0, t=80, b=30),
        height=400,
        font=dict(
            size=16,
            color="black"
        )
    )
    return figSub
