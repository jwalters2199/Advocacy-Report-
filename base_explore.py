from apps.visualizations import bubble_chart, heatmap, pie_chart_grid, pie_chart_select, stacked_bar_likert, stacked_bar_standard
from static import constants as C
from static import dataframe_init as D
from static import text as T

import dash
import dash_bootstrap_components as dbc
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output, State

from app import app

layout = html.Div([
    html.Div([
        dbc.Button("About", color="secondary", id="open-about-explore", className="mr-1", style={'float' : 'right'}),
        dcc.Link('Back to Report', href='/'),
        dbc.Modal(
            [
                dbc.ModalHeader("About"),
                html.Div([
                    T.ABOUT_P1,
                    T.ABOUT_P2,
                    T.ABOUT_KEY_TERMS
                ], style={'padding' : '14px'}),
                dbc.ModalFooter(
                    dbc.Button("Close", id="close-about-explore", className="ml-auto")
                )
            ],
            id="about-explore-modal",
            size="lg",
        )
    ], style={'width': '95%', 'display': 'inline-table', 'margin-top' : '24px', 'margin-left' : '24px'}),
    html.Div([
        html.P(id='question-label', style={'font-weight' : 'bold', 'font-size' : '24px'}),
        html.Div([
            html.Div([
                dcc.Dropdown(
                    id='custom-dropdown',
                    options=[],
                    value='',
                    clearable=False,
                    optionHeight=50,
                    style={'display': 'none'}
                )
            ], style={'width': '70%', 'display': 'inline-table'})
        ])
    ], style={'width': '50%', 'display': 'inline-table', 'margin-top' : '24px', 'margin-left' : '48px'}),
    html.Div([
        html.H5('Split by'),
        html.Div([
            dcc.Dropdown(
                id='axis',
                options=[{'label': i, 'value': i} for i in C.VIZ_AXES_ALL],
                value='Gender',
                clearable=False
            )
        ])
    ], style={'width': '15%', 'display': 'inline-table', 'margin-left' : '48px'}),
    html.Div([
        html.H5('Filter'),
        dbc.Button("Select Filters", color="info", id="open-filter", className="mr-1"),
        dbc.Modal(
            [
                dbc.ModalHeader("Filter Options"),
                dbc.ModalBody("You may only select up to two filters at a time, and you may not filter on the basis of your selected split."),
                html.Div([
                    html.Div([
                        html.P('Gender'),
                        dcc.Dropdown(
                            id='filter-gender-dropdown',
                            options=[{'label': i, 'value': i} for i in C.GENDER_FILTER_OPTIONS],
                            value='All',
                            clearable=False
                        )
                    ],
                    style={'width': '40%', 'display': 'inline-block', 'margin' : 15}),
                    html.Div([
                        html.P('Race/Ethnicity'),
                        dcc.Dropdown(
                            id='filter-race-ethnicity-dropdown',
                            options=[{'label': i, 'value': i} for i in C.RACE_ETHNICITY_FILTER_OPTIONS],
                            value='All',
                            clearable=False
                        )
                    ],
                    style={'width': '40%', 'display': 'inline-block', 'margin' : 15})
                ]),
                html.Div([
                    html.Div([
                        html.P('BGLTQ+'),
                        dcc.Dropdown(
                            id='filter-bgltq-dropdown',
                            options=[{'label': i, 'value': i} for i in C.BGLTQ_FILTER_OPTIONS],
                            value='All',
                            clearable=False
                        )
                    ],
                    style={'width': '40%', 'display': 'inline-block', 'margin' : 15}),
                    html.Div([
                        html.P('First Generation, Low Income (FGLI)'),
                        dcc.Dropdown(
                            id='filter-fgli-dropdown',
                            options=[{'label': i, 'value': i} for i in C.FGLI_FILTER_OPTIONS],
                            value='All',
                            clearable=False
                        )
                    ],
                    style={'width': '40%', 'display': 'inline-block', 'margin' : 15}),
                ]),
                html.Div([
                    html.Div([
                        html.P('Class Year'),
                        dcc.Dropdown(
                            id='filter-class-year-dropdown',
                            options=[{'label': i, 'value': i} for i in C.CLASS_YEAR_FILTER_OPTIONS],
                            value='All',
                            clearable=False
                        )
                    ],
                    style={'width': '40%', 'display': 'inline-block', 'margin' : 15}),
                    html.Div([
                        html.P('School of Primary Concentration'),
                        dcc.Dropdown(
                            id='filter-school-dropdown',
                            options=[{'label': i, 'value': i} for i in C.SCHOOL_FILTER_OPTIONS],
                            value='All',
                            clearable=False
                        )
                    ],
                    style={'width': '40%', 'display': 'inline-block', 'margin' : 15})
                ]),
                html.Div([
                    html.Div([
                        html.P('Primary Concentration'),
                        dcc.Dropdown(
                            id='filter-concentration-dropdown',
                            options=[{'label': i, 'value': i} for i in C.CONCENTRATION_FILTER_OPTIONS],
                            value='All',
                            clearable=False
                        )
                    ],
                    style={'width': '40%', 'display': 'inline-block', 'margin' : 15})
                ]),
                dbc.ModalFooter(
                    dbc.Button("Close", id="close-filter", className="ml-auto")
                ),
            ],
            id="filter-modal",
            size="lg",
        ),
        html.P('Filters: None', id='filters-label', style={'font-style' : 'italic'})
    ], style={'width': '20%', 'display': 'inline-table', 'margin-left' : '24px'}),
    html.Div([
        dcc.Graph(
            id='visualization',
            config={
                'displayModeBar': False
            }
        ),
    ], style={'width': '90%', 'display': 'inline-table', 'margin-top' : '0px', 'margin-left' : '48px'}),
    html.P(id='audience-label', style={'font-size' : '10px', 'margin-left' : '48px'})
])

@app.callback(
    Output('hidden-nav', 'children'),
    Input('url', 'pathname'))
def set_hidden_nav(pathname):
    if pathname != '/':
        return C.URL_SLUGS[pathname]['tab']
    return dash.no_update

@app.callback(
    Output('about-explore-modal', 'is_open'),
    Input('open-about-explore', 'n_clicks'),
    Input('close-about-explore', 'n_clicks'),
    State('about-explore-modal', 'is_open'))
def toggle_about_modal(n1, n2, is_open):
    if n1 or n2:
        return not is_open
    return is_open

@app.callback(
    Output('filter-modal', 'is_open'),
    Input('open-filter', 'n_clicks'),
    Input('close-filter', 'n_clicks'),
    State('filter-modal', 'is_open'))
def toggle_filter_modal(n1, n2, is_open):
    if n1 or n2:
        return not is_open
    return is_open

@app.callback(
    Output('filter-gender-dropdown', 'disabled'),
    Output('filter-race-ethnicity-dropdown', 'disabled'),
    Output('filter-bgltq-dropdown', 'disabled'),
    Output('filter-fgli-dropdown', 'disabled'),
    Output('filter-class-year-dropdown', 'disabled'),
    Output('filter-school-dropdown', 'disabled'),
    Output('filter-concentration-dropdown', 'disabled'),
    Input('axis', 'value'),
    Input('filter-gender-dropdown', 'value'),
    Input('filter-race-ethnicity-dropdown', 'value'),
    Input('filter-bgltq-dropdown', 'value'),
    Input('filter-fgli-dropdown', 'value'),
    Input('filter-class-year-dropdown', 'value'),
    Input('filter-school-dropdown', 'value'),
    Input('filter-concentration-dropdown', 'value'))
def toggle_filters(axis, gender_filter, race_ethnicity_filter, bgltq_filter, fgli_filter, 
    class_year_filter, school_filter, concentration_filter):
    filter_count = 0
    filter_enable_list = [False, False, False, False, False, False, False]
    filter_enable_list[C.VIZ_AXES_ALL.index(axis)] = True
    filter_disable_list = filter_enable_list.copy()

    filter_selections = [gender_filter, race_ethnicity_filter, bgltq_filter, fgli_filter, class_year_filter, school_filter, concentration_filter]
    for i in range(len(filter_selections)):
        if filter_selections[i] == 'All':
            filter_disable_list[i] = (True)
        else:
            filter_count += 1

    if filter_count >= 2:
        return filter_disable_list
    return filter_enable_list

@app.callback(
    Output('filter-gender-dropdown', 'value'),
    Output('filter-race-ethnicity-dropdown', 'value'),
    Output('filter-bgltq-dropdown', 'value'),
    Output('filter-fgli-dropdown', 'value'),
    Output('filter-class-year-dropdown', 'value'),
    Output('filter-school-dropdown', 'value'),
    Output('filter-concentration-dropdown', 'value'),
    Input('axis', 'value'))
def reset_filters(axis):
    return ['All', 'All', 'All', 'All', 'All', 'All', 'All']

@app.callback(
    Output('filters-label', 'children'),
    Input('filter-gender-dropdown', 'value'),
    Input('filter-race-ethnicity-dropdown', 'value'),
    Input('filter-bgltq-dropdown', 'value'),
    Input('filter-fgli-dropdown', 'value'),
    Input('filter-class-year-dropdown', 'value'),
    Input('filter-school-dropdown', 'value'),
    Input('filter-concentration-dropdown', 'value'))
def set_filters_label(gender_filter, race_ethnicity_filter, bgltq_filter, fgli_filter, 
    class_year_filter, school_filter, concentration_filter):
    filter_str_list = []
    filter_selections = [gender_filter, race_ethnicity_filter, bgltq_filter, fgli_filter, class_year_filter, school_filter, concentration_filter]
    for sel in filter_selections:
        if sel != 'All':
            filter_str_list.append(sel)
    
    if len(filter_str_list) == 0:
        return 'Filters: None'
    return 'Filters: ' + ', '.join(filter_str_list)

@app.callback(
    Output('axis', 'options'),
    Input('url', 'pathname'))
def update_axis_options(pathname):
    if pathname == '/':
        return []
    if C.URL_SLUGS[pathname]['audience'] == 'CS concentrators':
        return [{'label': i, 'value': i} for i in C.VIZ_AXES_CS]
    return [{'label': i, 'value': i} for i in C.VIZ_AXES_ALL]

@app.callback(
    Output('custom-dropdown', 'options'),
    Output('custom-dropdown', 'value'),
    Output('custom-dropdown', 'style'),
    Input('url', 'pathname'))
def update_custom_dropdown(pathname):
    if pathname == '/':
        return [[], '', {'display': 'none'}]
    q_id = C.URL_SLUGS[pathname]['question_id']
    if isinstance(q_id, str) and not 'dropdown_options' in C.URL_SLUGS[pathname]:
        return [[], '', {'display': 'none'}]
    if 'dropdown_options' in C.URL_SLUGS[pathname]:
        options_list = C.URL_SLUGS[pathname]['dropdown_options']
    else:
        options_list = list(q_id.values())
    return [[{'label': i, 'value': i} for i in options_list], options_list[0], {'display': 'block', 'margin-bottom' : '24px'}]

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

@app.callback(
    Output('question-label', 'children'),
    Output('audience-label', 'children'),
    Input('url', 'pathname'),
    Input('custom-dropdown', 'value'))
def set_question_label(pathname, custom_dropdown_value):
    if pathname == '/':
        return ['', '']
    q_id = C.URL_SLUGS[pathname]['question_id']
    audience = C.URL_SLUGS[pathname]['audience']
    if isinstance(q_id, str): # single question, no options
        return [clean_question_label(pathname, D.QUESTION_KEY[q_id][0]), '*Respondents to this question included ' + audience + '.']
    dropdown_options = list(q_id.values())
    index = dropdown_options.index(custom_dropdown_value)
    return [clean_question_label(pathname, D.QUESTION_KEY[list(q_id.keys())[index]][0]), '*Respondents to this question included ' + audience + '.']

@app.callback(
    Output('visualization', 'figure'),
    Input('url', 'pathname'),
    Input('axis', 'value'),
    Input('custom-dropdown', 'value'),
    Input('filter-gender-dropdown', 'value'),
    Input('filter-race-ethnicity-dropdown', 'value'),
    Input('filter-bgltq-dropdown', 'value'),
    Input('filter-fgli-dropdown', 'value'),
    Input('filter-class-year-dropdown', 'value'),
    Input('filter-school-dropdown', 'value'),
    Input('filter-concentration-dropdown', 'value'))
def update_graph(pathname, axis, custom_dropdown_value, gender_filter, race_ethnicity_filter,
    bgltq_filter, fgli_filter, class_year_filter, school_filter, concentration_filter):
    if pathname == '/':
        return C.EMPTY_FIGURE
    viz_type = C.URL_SLUGS[pathname]['viz_type']
    q_id = C.URL_SLUGS[pathname]['question_id']
    if not isinstance(q_id, str):
        if custom_dropdown_value == '':
            q_id = list(q_id.keys())[0]
        else:
            dropdown_options = list(q_id.values())
            q_id = list(q_id.keys())[dropdown_options.index(custom_dropdown_value)]
    if viz_type == 'stacked_bar_standard':
        return stacked_bar_standard.generate_figure(q_id, axis, gender_filter, race_ethnicity_filter,
            bgltq_filter, fgli_filter, class_year_filter, school_filter, concentration_filter)
    if viz_type == 'stacked_bar_likert':
        return stacked_bar_likert.generate_figure(q_id, axis, gender_filter, race_ethnicity_filter,
            bgltq_filter, fgli_filter, class_year_filter, school_filter, concentration_filter)
    if viz_type == 'pie_chart_grid':
        return pie_chart_grid.generate_figure(q_id, axis, gender_filter, race_ethnicity_filter,
            bgltq_filter, fgli_filter, class_year_filter, school_filter, concentration_filter)
    if viz_type == 'bubble_chart':
        return bubble_chart.generate_figure(q_id, axis, custom_dropdown_value, gender_filter,
            race_ethnicity_filter, bgltq_filter, fgli_filter, class_year_filter, school_filter,
            concentration_filter)
    if viz_type == 'pie_chart_select':
        return pie_chart_select.generate_figure(q_id, axis, custom_dropdown_value, gender_filter,
            race_ethnicity_filter, bgltq_filter, fgli_filter, class_year_filter, school_filter,
            concentration_filter)
    if viz_type == 'heatmap':
        return heatmap.generate_figure(q_id, custom_dropdown_value, gender_filter,
            race_ethnicity_filter, bgltq_filter, fgli_filter, class_year_filter, school_filter,
            concentration_filter)
    return C.EMPTY_FIGURE

