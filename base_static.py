from apps.visualizations import bubble_chart, heatmap, pie_chart_grid, pie_chart_select, stacked_bar_likert, stacked_bar_standard
from static import constants as C
from static import dataframe_init as D

import dash
import dash_bootstrap_components as dbc
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output

from app import app

def serve_layout(viz_index, pathname, axis, gender_filter, race_ethnicity_filter, bgltq_filter, fgli_filter,
    class_year_filter, school_filter, concentration_filter, width, custom_dropdown_value=None):
    return html.Div([
        html.Div(id='hidden-pathname' + str(viz_index), children=pathname, style={'display' : 'none'}),
        html.Div(id='hidden-axis' + str(viz_index), children=axis, style={'display' : 'none'}),
        html.Div(id='hidden-gender-filter' + str(viz_index), children=gender_filter, style={'display' : 'none'}),
        html.Div(id='hidden-race-ethnicity-filter' + str(viz_index), children=race_ethnicity_filter, style={'display' : 'none'}),
        html.Div(id='hidden-bgltq-filter' + str(viz_index), children=bgltq_filter, style={'display' : 'none'}),
        html.Div(id='hidden-fgli-filter' + str(viz_index), children=fgli_filter, style={'display' : 'none'}),
        html.Div(id='hidden-class-year-filter' + str(viz_index), children=class_year_filter, style={'display' : 'none'}),
        html.Div(id='hidden-school-filter' + str(viz_index), children=school_filter, style={'display' : 'none'}),
        html.Div(id='hidden-concentration-filter' + str(viz_index), children=concentration_filter, style={'display' : 'none'}),
        html.Div(id='hidden-custom-dropdown-value' + str(viz_index), children=custom_dropdown_value, style={'display' : 'none'}),
        html.Div([
            html.P(
                id='question-label-static' + str(viz_index),
                style={
                    'display' : 'inline-table',
                    'font-weight' : 'bold',
                    'font-size' : '18px',
                    'width' : '75%'
                }),
            html.Div([
                dcc.Dropdown(
                    id='custom-dropdown-static' + str(viz_index),
                    options=[],
                    value='',
                    clearable=False,
                    optionHeight=50
                )
            ], id='custom-dropdown-static-parent' + str(viz_index), style={'display': 'none'}),
            dbc.Button("Explore the Data",
                id='explore-button' + str(viz_index),
                color="primary",
                href=pathname,
                size="sm",
                style={'display' : 'none'
            })
        ], style={'display': 'inline-table', 'width' : '100%', 'margin-top' : '24px'}),
        html.Div([
            dcc.Graph(
                id='visualization-static' + str(viz_index),
                config={
                    'displayModeBar': False
                },
                style={'display' : 'none'}
            ),
        ]),
        html.P(
            id='audience-label-static' + str(viz_index),
            style={
                'font-size' : '12px',
                'font-style' : 'italic'
            })
    ], style={'width' : width, 'display': 'inline-table'})

def update_custom_dropdown(pathname, custom_dropdown_value):
    if pathname == '/':
        return [[], '', {'display': 'none'}, {'display': 'none'}]
    q_id = C.URL_SLUGS[pathname]['question_id']
    if isinstance(q_id, str) and not 'dropdown_options' in C.URL_SLUGS[pathname]:
        return [[], '', {'display': 'none'}, {'display': 'inline-table', 'float' : 'right'}]
    if 'dropdown_options' in C.URL_SLUGS[pathname]:
        options_list = C.URL_SLUGS[pathname]['dropdown_options']
    else:
        options_list = list(q_id.values())
    value = custom_dropdown_value if custom_dropdown_value else options_list[0]
    return [[{'label': i, 'value': i} for i in options_list], value, {'display': 'inline-table', 'width': '60%', 'margin-right' : '24px'}, {'display': 'inline-table'}]

def clean_question_label(pathname, label):
    viz_type = C.URL_SLUGS[pathname]['viz_type']
    if viz_type == 'stacked_bar_likert' or viz_type == 'pie_chart_grid' or viz_type == 'pie_chart_select' or viz_type == 'heatmap':
        label = label.replace('Please indicate the extent to which you disagree or agree with the following statement:\n', '')
        label = label.replace('Please indicate the extent to which you disagree or agree with each of the following statements:\n', '')
        label = label.replace('Please indicate the extent to which you disagree or agree each of the following statements:\n', '')
        label = label.replace('Please indicate the extent to which you disagree or agree with each of the following statements: - ', '')
        label = label.replace('Please indicate which of the following statements you agree with:\n', '')
        hyphen_index = label.rfind('-')
        if hyphen_index != -1:
            label = label[0:hyphen_index]
    return label

def set_question_label(pathname, custom_dropdown_value):
    if pathname == '/':
        return ['', '']
    q_id = C.URL_SLUGS[pathname]['question_id']
    if isinstance(q_id, str): # single question, no options
        return clean_question_label(pathname, D.QUESTION_KEY[q_id][0])
    dropdown_options = list(q_id.values())
    index = dropdown_options.index(custom_dropdown_value)
    return clean_question_label(pathname, D.QUESTION_KEY[list(q_id.keys())[index]][0])

def set_audience_label(pathname, gender_filter, race_ethnicity_filter, bgltq_filter, fgli_filter, 
    class_year_filter, school_filter, concentration_filter):
    audience_label = 'Respondents to this question included ' + C.URL_SLUGS[pathname]['audience'] + '. '
    filter_str_list = []
    filter_selections = {
        'gender' : gender_filter,
        'race/ethnicity' : race_ethnicity_filter,
        'BGLTQ+' : bgltq_filter,
        'FGLI' : fgli_filter,
        'class year' : class_year_filter,
        'school' : school_filter,
        'primary concentration' : concentration_filter
    }
    filter_label = 'Filtered by '
    for k in filter_selections.keys():
        sel = filter_selections[k]
        if sel != 'All':
            filter_str_list.append(sel)
            filter_label += k + ' (' + sel + '),'

    if len(filter_str_list) == 0:
        return audience_label
    filter_label = filter_label[:-1] + '.'
    return audience_label + filter_label

def update_graph(pathname, axis, custom_dropdown_value, gender_filter, race_ethnicity_filter,
    bgltq_filter, fgli_filter, class_year_filter, school_filter, concentration_filter):
    if pathname == '/':
        return [C.EMPTY_FIGURE, {'display' : 'none'}]
    viz_type = C.URL_SLUGS[pathname]['viz_type']
    q_id = C.URL_SLUGS[pathname]['question_id']
    if not isinstance(q_id, str):
        if custom_dropdown_value == '':
            q_id = list(q_id.keys())[0]
        else:
            dropdown_options = list(q_id.values())
            q_id = list(q_id.keys())[dropdown_options.index(custom_dropdown_value)]
    if viz_type == 'stacked_bar_standard':
        return [
            stacked_bar_standard.generate_figure(q_id, axis, gender_filter, race_ethnicity_filter,
                bgltq_filter, fgli_filter, class_year_filter, school_filter, concentration_filter),
            {'display' : 'block'}
        ]
    if viz_type == 'stacked_bar_likert':
        return [
            stacked_bar_likert.generate_figure(q_id, axis, gender_filter, race_ethnicity_filter,
                bgltq_filter, fgli_filter, class_year_filter, school_filter, concentration_filter),
            {'display' : 'block'}
        ]
    if viz_type == 'pie_chart_grid':
        return [
            pie_chart_grid.generate_figure(q_id, axis, gender_filter, race_ethnicity_filter,
                bgltq_filter, fgli_filter, class_year_filter, school_filter, concentration_filter),
            {'display' : 'block'}
        ]
    if viz_type == 'bubble_chart':
        return [
            bubble_chart.generate_figure(q_id, axis, custom_dropdown_value, gender_filter,
                race_ethnicity_filter, bgltq_filter, fgli_filter, class_year_filter, school_filter,
                concentration_filter),
            {'display' : 'block'}
        ]
    if viz_type == 'pie_chart_select':
        return [
            pie_chart_select.generate_figure(q_id, axis, custom_dropdown_value, gender_filter,
                race_ethnicity_filter, bgltq_filter, fgli_filter, class_year_filter, school_filter,
                concentration_filter),
            {'display' : 'block'}
        ]
    if viz_type == 'heatmap':
        return [
            heatmap.generate_figure(q_id, axis, gender_filter, race_ethnicity_filter, bgltq_filter,
                fgli_filter, class_year_filter, school_filter, concentration_filter),
            {'display' : 'block'}
        ]
    return [C.EMPTY_FIGURE, {'display' : 'none'}]

for i in range(1, C.NUM_VIZ + 1):
    app.callback(
        Output('custom-dropdown-static' + str(i), 'options'),
        Output('custom-dropdown-static' + str(i), 'value'),
        Output('custom-dropdown-static-parent' + str(i), 'style'),
        Output('explore-button' + str(i), 'style'),
        Input('hidden-pathname' + str(i), 'children'),
        Input('hidden-custom-dropdown-value' + str(i), 'children')
    )(update_custom_dropdown)

    app.callback(
        Output('question-label-static' + str(i), 'children'),
        Input('hidden-pathname' + str(i), 'children'),
        Input('custom-dropdown-static' + str(i), 'value')
    )(set_question_label)

    app.callback(
        Output('audience-label-static' + str(i), 'children'),
        Input('hidden-pathname' + str(i), 'children'),
        Input('hidden-gender-filter' + str(i), 'children'),
        Input('hidden-race-ethnicity-filter' + str(i), 'children'),
        Input('hidden-bgltq-filter' + str(i), 'children'),
        Input('hidden-fgli-filter' + str(i), 'children'),
        Input('hidden-class-year-filter' + str(i), 'children'),
        Input('hidden-school-filter' + str(i), 'children'),
        Input('hidden-concentration-filter' + str(i), 'children')
    )(set_audience_label)

    app.callback(
        Output('visualization-static' + str(i), 'figure'),
        Output('visualization-static' + str(i), 'style'),
        Input('hidden-pathname' + str(i), 'children'),
        Input('hidden-axis' + str(i), 'children'),
        Input('custom-dropdown-static' + str(i), 'value'),
        Input('hidden-gender-filter' + str(i), 'children'),
        Input('hidden-race-ethnicity-filter' + str(i), 'children'),
        Input('hidden-bgltq-filter' + str(i), 'children'),
        Input('hidden-fgli-filter' + str(i), 'children'),
        Input('hidden-class-year-filter' + str(i), 'children'),
        Input('hidden-school-filter' + str(i), 'children'),
        Input('hidden-concentration-filter' + str(i), 'children')
    )(update_graph)
