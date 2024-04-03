from app import app
from static import constants as C
from static import dataframe_init as D

import numpy as np
import plotly.graph_objects as go
from plotly.subplots import make_subplots

## Constants
# sets up discrete colorscale, dictates where COLORS start
BVALS = [0.5, 1.5, 2.5, 3.5, 4.5, 5.5, 6.5, 7.5] 

COLORS = ['rgb(28, 69, 135)', 'rgb(60, 120, 216)', 'rgb(164, 194, 244)', 'rgb(217, 217, 217)', 'rgb(234, 153, 153)', 'rgb(204, 0, 0)', 'rgb(102, 0, 0)']

# Sets up labels
BVALS = np.array(BVALS)
#position with respect to BVALS where ticktext is displayed
tickvals = [np.mean(BVALS[k:k+2]) for k in range(len(BVALS))] 
ticktext = ['Strongly Disagree', 'Disagree', 'Somewhat Disagree', 'Neither agree nor disagree', 'Somewhat Agree', 'Agree', 'Strongly Agree'] 

def is_sample_size_insufficient(dff, axis):

    #TODO

    # get number of responses per category
    category_counts = dff[axis].value_counts().reset_index(name='counts')['counts'].tolist()
    # check number of responses per category is greater than minimum sample size
    return any(c < C.MIN_SAMPLE_SIZE for c in category_counts)

# define discrete colorscale
# https://chart-studio.plotly.com/~empet/15229/heatmap-with-a-discrete-colorscale/#/
def discrete_colorscale(BVALS, COLORS):
    """
    BVALS - list of values bounding intervals/ranges of interest
    COLORS - list of rgb or hex colorcodes for values in [BVALS[k], BVALS[k+1]],0<=k < len(BVALS)-1
    returns the plotly  discrete colorscale
    """
    if len(BVALS) != len(COLORS)+1:
        raise ValueError('len(boundary values) should be equal to  len(COLORS)+1')
    BVALS = sorted(BVALS)
    #normalized values
    nvals = [(v-BVALS[0])/(BVALS[-1]-BVALS[0]) for v in BVALS]
    
    #discrete colorscale
    dcolorscale = []
    for k in range(len(COLORS)):
        dcolorscale.extend([[nvals[k], COLORS[k]], [nvals[k+1], COLORS[k]]])
    return dcolorscale

dcolorsc = discrete_colorscale(BVALS, COLORS)

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

def construct_map(q_id, axis, df):
    filter_funcs = []
    # index 1 & 2 are subplot labels, 3 & 4 are map lists 
    final_maps = [] 
    if axis == 'Gender':
        filter_funcs = [D.filter_male, D.filter_non_male]
        final_maps.append('Male')
        final_maps.append('Non-Male')
    elif axis == 'Race/Ethnicity':
        filter_funcs = [D.filter_non_urm, D.filter_urm]
        final_maps.append('Non-URM')
        final_maps.append('URM')
    elif axis == 'Sexuality':  
        filter_funcs = [D.filter_is_non_bgltq, D.filter_is_bgltq]
        final_maps.append('Non-BGLTQ+')
        final_maps.append('BGLTQ+')
    else:
        return []

    for f in filter_funcs:
        # Return the list (map)
        total = []
        # count the number of responses 
        nrows = 0 
        filt_df = f(df)
        for i in list(C.LIKERT_AGREEMENT_KEY.keys()): # for 1 to 7 likert responses
            count = 0
            # replace with axis df 
            for x in filt_df[q_id]: 
                if x == i:
                    count += 1
                    nrows += 1
            total.append(count)
        # makes sure total is 100 
        total = [x / nrows for x in total]

        # creates the right number of each index
        map_list = []
        for i in range(1, 8):
            x = [i]*round(total[i-1]*400)
            map_list.extend(x)

        # adjust for the extra decimal 
        map_list.extend([7])

        # reshapes to the multi-dim list size we need 
        map_array = np.array(map_list)
        map_array = np.resize(map_array, (20, 20)) 

        # convert back to list 
        map_array = map_array.tolist()
        map_array = np.fliplr(map_array)

        final_maps.append(map_array)

    return final_maps

def generate_figure(q_id, axis, gender_filter, race_ethnicity_filter, bgltq_filter, fgli_filter, 
    class_year_filter, school_filter, concentration_filter):
    filt_df = filter_df(D.CLEAN_DF, gender_filter, race_ethnicity_filter, bgltq_filter,
        fgli_filter, class_year_filter, school_filter, concentration_filter)

    #return empty plot if there is not enough data (or if figure is not yet implemented)
    # if is_sample_size_insufficient(filt_df, axis):
    #     return C.EMPTY_FIGURE

    # get relevant dataframe according to axis, returns list of maps
    dff = construct_map(q_id, axis, filt_df)

    # create heat maps with dataframe
    heatmap = go.Heatmap(
        z=dff[2], 
        colorscale=dcolorsc,
        hoverinfo='text',
        hovertext=[[ticktext[y-1] for y in x] for x in dff[2].tolist()],
        colorbar = dict(thickness=25, 
                    tickvals=tickvals, 
                    ticktext=['', '', '', '', '', '', ''])) 
    heatmap_non = go.Heatmap(
        z=dff[3],
        colorscale=dcolorsc,
        hoverinfo='text',
        hovertext=[[ticktext[y-1] for y in x] for x in dff[3].tolist()],
        colorbar = dict(thickness=25,
                    tickvals=tickvals,
                    ticktext=ticktext)
        ) 

    fig = make_subplots(rows=1, cols=2, subplot_titles=(dff[0],dff[1]))

    fig.add_trace(heatmap, row=1, col=1)
    fig.add_trace(heatmap_non, row=1, col=2)

    fig.update_layout(
        height = 400,
        margin=dict(l=0, r=0, t=20, b=30),
        xaxis = dict(showticklabels=False),
        yaxis = dict(showticklabels=False))

    return fig
