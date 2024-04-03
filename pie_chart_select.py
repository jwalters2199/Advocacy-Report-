from app import app
from static import constants as C
from static import dataframe_init as D

from plotly.subplots import make_subplots
import plotly.graph_objects as go
import textwrap

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

def wrap_text(text, width):
    return '<br>'.join(textwrap.wrap(text, width=width))

def generate_figure(q_id, axis, question_option, gender_filter, race_ethnicity_filter, bgltq_filter,
    fgli_filter, class_year_filter, school_filter, concentration_filter):
    # get relevant dataframe according to axis
    dff = filter_df(D.AXIS_DF[axis], gender_filter, race_ethnicity_filter, bgltq_filter, fgli_filter,
        class_year_filter, school_filter, concentration_filter)
    # return empty plot if there is not enough data
    if is_sample_size_insufficient(dff, q_id, axis):
        return C.EMPTY_FIGURE
    unique_categories = dff[axis].unique()
    category_names = [wrap_text(t, 16) for t in list(dff[axis].unique())]
    
    new_category = []
    
    for c in unique_categories:
        category_df = dff[dff[axis] == c]
        new_category.append(category_df)
 
    generateSpecs = [[{"type": "pie"} for _ in new_category]]
    fig = make_subplots(rows=1, cols=len(new_category),specs = generateSpecs, subplot_titles = category_names)
    colNum = 1
   
    text_annotations=[]
    text_annotations.append(dict(font=dict(size=14)))

    for df in new_category: #new category = inc. in colnum
        yes_num = df[df[q_id].str.contains(question_option, na=False)].shape[0] #filters out yes respondents 
        no_num = df[~(df[q_id].str.contains(question_option, na=False))].shape[0] #filters our no respondents
        y_n_values = [yes_num,no_num]
        fig.add_trace(go.Pie(
            labels = ['Yes', 'No'],
            values = y_n_values,
            textinfo='none',
            hoverinfo='label+percent',
            direction = 'clockwise',
            sort = False,
            marker={'colors': ['rgb(71,159,118)', 'rgb(233,236,239)']}
        ), row=1, col=colNum)
        colNum +=1
    fig.update_layout(
        annotations=text_annotations,
        height=300,
        margin=dict(l=0, r=0, t=70, b=30),
        legend=dict(
            yanchor="bottom",
            y=1.02,
            xanchor="left",
            x=1.02
        )
    )

    return fig
