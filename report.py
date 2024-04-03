import dash_bootstrap_components as dbc
import dash_core_components as dcc
from dash.dependencies import State, Input, Output
import dash_html_components as html

from app import app
from apps import base_static
from static import text as T

layout = html.Div([
    html.Div([
        dbc.Button("About", color="secondary", id="open-about-report", className="mr-1", style={'float' : 'right'}),
        html.H1('The 2020 WiCS Advocacy Survey Report'),
        dbc.Modal(
            [
                dbc.ModalHeader("About"),
                html.Div([
                    T.ABOUT_P1,
                    T.ABOUT_P2,
                    T.ABOUT_KEY_TERMS
                ], style={'padding' : '14px'}),
                dbc.ModalFooter(
                    dbc.Button("Close", id="close-about-report", className="ml-auto")
                )
            ],
            id="about-report-modal",
            size="lg",
        )
    ], style={'margin-bottom' : '12px'}),
    dcc.Tabs(id='report-tabs', value='', children=[
        dcc.Tab(label='Introduction', value='intro'),
        dcc.Tab(label='Background', value='background'),
        dcc.Tab(label='Academics', value='academics'),
        dcc.Tab(label='Post-Grad', value='post-grad'),
        dcc.Tab(label='Discrimination', value='discrimination'),
        dcc.Tab(label='Belonging', value='belonging'),
        dcc.Tab(label='Conclusion', value='conclusion'),
    ]),
    html.Div(id='report-content', style={'padding' : '20px', 'margin-top' : '12px'})
], style={'padding' : '24px'})

@app.callback(
    Output('report-tabs', 'value'),
    Input('hidden-nav', 'children'))
def update_tab(tab_value):
    return tab_value

@app.callback(
    Output('about-report-modal', 'is_open'),
    Input('open-about-report', 'n_clicks'),
    Input('close-about-report', 'n_clicks'),
    State('about-report-modal', 'is_open'))
def toggle_modal(n1, n2, is_open):
    if n1 or n2:
        return not is_open
    return is_open

@app.callback(
    Output('report-content', 'children'),
    Input('report-tabs', 'value'))
def render_content(tab):
    if tab == 'intro':
        return html.Div([
            T.INTRO_P1,
            T.INTRO_P2,
            T.INTRO_P3
        ])
    if tab == 'background':
        return html.Div([
            T.BACKGROUND_P1,
            html.Div([
                base_static.serve_layout(
                    viz_index=1,
                    pathname='/explore/background',
                    axis='Gender',
                    gender_filter='All',
                    race_ethnicity_filter='All',
                    bgltq_filter='All',
                    fgli_filter='All',
                    class_year_filter='All',
                    school_filter='All',
                    concentration_filter='All',
                    width='95%')
            ]),
            T.BACKGROUND_P2,
            html.Div([
                base_static.serve_layout(
                    viz_index=2,
                    pathname='/explore/background',
                    axis='Race/Ethnicity',
                    gender_filter='All',
                    race_ethnicity_filter='All',
                    bgltq_filter='All',
                    fgli_filter='All',
                    class_year_filter='All',
                    school_filter='All',
                    concentration_filter='All',
                    width='95%')
            ]),
            T.BACKGROUND_P3
        ])
    if tab == 'academics':
        return html.Div([
            T.ACADEMICS_P1,
            html.H4('Course Enrollment & Confidence', style={'margin-top' : '24px'}),
            html.Div([
                base_static.serve_layout(
                    viz_index=3,
                    pathname='/explore/course-enrollment',
                    axis='Gender',
                    gender_filter='All',
                    race_ethnicity_filter='All',
                    bgltq_filter='All',
                    fgli_filter='All',
                    class_year_filter='All',
                    school_filter='All',
                    concentration_filter='All',
                    width='50%'),
                html.Div([
                    T.ACADEMICS_P2
                ], style={'display' : 'inline-table', 'width' : '40%'})
            ]),
            html.Div([
                base_static.serve_layout(
                    viz_index=4,
                    pathname='/explore/course-enrollment',
                    axis='Race/Ethnicity',
                    gender_filter='All',
                    race_ethnicity_filter='All',
                    bgltq_filter='All',
                    fgli_filter='All',
                    class_year_filter='All',
                    school_filter='All',
                    concentration_filter='All',
                    width='50%'),
                html.Div([
                    T.ACADEMICS_P3,
                    T.ACADEMICS_P4
                ], style={'display' : 'inline-table', 'width' : '40%'})
            ]),
            html.Div([
                base_static.serve_layout(
                    viz_index=5,
                    pathname='/explore/cs-knowledge',
                    axis='Gender',
                    gender_filter='All',
                    race_ethnicity_filter='All',
                    bgltq_filter='All',
                    fgli_filter='All',
                    class_year_filter='All',
                    school_filter='All',
                    concentration_filter='All',
                    width='95%')
            ]),
            T.ACADEMICS_P5,
            html.Div([
                html.Div([
                    T.ACADEMICS_P6
                ], style={'display' : 'inline-table', 'width' : '32%', 'margin-right' : '20px'}),
                base_static.serve_layout(
                    viz_index=6,
                    pathname='/explore/cs-knowledge',
                    axis='Race/Ethnicity',
                    gender_filter='All',
                    race_ethnicity_filter='All',
                    bgltq_filter='All',
                    fgli_filter='All',
                    class_year_filter='All',
                    school_filter='All',
                    concentration_filter='All',
                    width='65%')
            ]),
            html.H4('Course Engagement', style={'margin-top' : '24px'}),
            html.Div([
                base_static.serve_layout(
                    viz_index=7,
                    pathname='/explore/course-participation',
                    axis='Gender',
                    gender_filter='All',
                    race_ethnicity_filter='All',
                    bgltq_filter='All',
                    fgli_filter='All',
                    class_year_filter='All',
                    school_filter='All',
                    concentration_filter='Computer Science',
                    width='60%'),
                html.Div([
                    T.ACADEMICS_P7
                ], style={'display' : 'inline-table', 'width' : '30%', 'margin-left' : '20px'})
            ]),
            html.Div([
                html.Div([
                    T.ACADEMICS_P8
                ], style={'display' : 'inline-table', 'width' : '32%', 'margin-right' : '20px'}),
                base_static.serve_layout(
                    viz_index=8,
                    pathname='/explore/problem-set-partners',
                    axis='Race/Ethnicity',
                    gender_filter='All',
                    race_ethnicity_filter='All',
                    bgltq_filter='All',
                    fgli_filter='All',
                    class_year_filter='All',
                    school_filter='All',
                    concentration_filter='All',
                    width='65%'),
                T.ACADEMICS_P9
            ]),
            html.H4('Department Engagement', style={'margin-top' : '24px'}),
            html.Div([
                base_static.serve_layout(
                    viz_index=9,
                    pathname='/explore/department-engagement',
                    axis='School',
                    gender_filter='All',
                    race_ethnicity_filter='All',
                    bgltq_filter='All',
                    fgli_filter='All',
                    class_year_filter='All',
                    school_filter='All',
                    concentration_filter='All',
                    width='90%')
            ]),
            T.ACADEMICS_P10
        ])
    if tab == 'post-grad':
        return html.Div([
            T.POST_GRAD_P1,
            html.Div([
                base_static.serve_layout(
                    viz_index=10,
                    pathname='/explore/future-graduate-studies',
                    axis='Gender',
                    gender_filter='All',
                    race_ethnicity_filter='All',
                    bgltq_filter='All',
                    fgli_filter='All',
                    class_year_filter='All',
                    school_filter='All',
                    concentration_filter='All',
                    width='95%')
            ]),
            T.POST_GRAD_P2,
            html.Div([
                base_static.serve_layout(
                    viz_index=11,
                    pathname='/explore/future-graduate-studies',
                    axis='FGLI',
                    gender_filter='All',
                    race_ethnicity_filter='All',
                    bgltq_filter='All',
                    fgli_filter='All',
                    class_year_filter='All',
                    school_filter='All',
                    concentration_filter='All',
                    width='95%')
            ]),
            T.POST_GRAD_P3,
            html.Div([
                html.Div([
                    T.POST_GRAD_P4
                ], style={'display' : 'inline-table', 'width' : '25%', 'margin-right' : '36px'}),
                base_static.serve_layout(
                    viz_index=12,
                    pathname='/explore/professional-opportunities-referrals',
                    axis='Gender',
                    gender_filter='All',
                    race_ethnicity_filter='All',
                    bgltq_filter='All',
                    fgli_filter='All',
                    class_year_filter='All',
                    school_filter='All',
                    concentration_filter='Computer Science',
                    width='40%')
            ]),
            html.Div([
                base_static.serve_layout(
                    viz_index=13,
                    pathname='/explore/professional-opportunities-mentorship',
                    axis='FGLI',
                    gender_filter='All',
                    race_ethnicity_filter='All',
                    bgltq_filter='All',
                    fgli_filter='All',
                    class_year_filter='All',
                    school_filter='All',
                    concentration_filter='Computer Science',
                    width='40%'),
                html.Div([
                    T.POST_GRAD_P5
                ], style={'display' : 'inline-table', 'width' : '30%', 'margin-left' : '24px'})
            ])
        ])
    if tab == 'discrimination':
        return html.Div([
            T.DISCRIMINATION_P1,
            html.Div([
                base_static.serve_layout(
                    viz_index=14,
                    pathname='/explore/discrimination-experience',
                    axis='Gender',
                    gender_filter='All',
                    race_ethnicity_filter='All',
                    bgltq_filter='All',
                    fgli_filter='All',
                    class_year_filter='All',
                    school_filter='All',
                    concentration_filter='All',
                    width='95%')
            ]),
            T.DISCRIMINATION_P2,
            T.DISCRIMINATION_P3,
            html.Div([
                html.Div([
                    T.DISCRIMINATION_P4
                ], style={'display' : 'inline-table', 'width' : '30%', 'margin-right' : '24px'}),
                base_static.serve_layout(
                    viz_index=15,
                    pathname='/explore/department-discrimination',
                    axis='Gender',
                    gender_filter='All',
                    race_ethnicity_filter='All',
                    bgltq_filter='All',
                    fgli_filter='All',
                    class_year_filter='All',
                    school_filter='All',
                    concentration_filter='Computer Science',
                    width='65%',
                    custom_dropdown_value='Gender')
            ]),
            html.Div([
                base_static.serve_layout(
                    viz_index=16,
                    pathname='/explore/department-discrimination',
                    axis='Race/Ethnicity',
                    gender_filter='All',
                    race_ethnicity_filter='All',
                    bgltq_filter='All',
                    fgli_filter='All',
                    class_year_filter='All',
                    school_filter='All',
                    concentration_filter='Computer Science',
                    width='65%',
                    custom_dropdown_value='Race/Ethnicity'),
                html.Div([
                    T.DISCRIMINATION_P5
                ], style={'display' : 'inline-table', 'width' : '30%', 'margin-left' : '24px'})
            ]),
        ])
    if tab == 'belonging':
        return html.Div([
            T.BELONGING_P1,
            html.Div([
                base_static.serve_layout(
                    viz_index=17,
                    pathname='/explore/identity-representation',
                    axis='Gender',
                    gender_filter='All',
                    race_ethnicity_filter='All',
                    bgltq_filter='All',
                    fgli_filter='All',
                    class_year_filter='All',
                    school_filter='All',
                    concentration_filter='Computer Science',
                    width='67%'),
                html.Div([
                    T.BELONGING_P2
                ], style={'display' : 'inline-table', 'width' : '28%', 'margin-left' : '24px'})
            ]),
            html.Div([
                html.Div([
                    T.BELONGING_P3
                ], style={'display' : 'inline-table', 'width' : '32%', 'margin-right' : '36px'}),
                base_static.serve_layout(
                    viz_index=18,
                    pathname='/explore/identity-representation',
                    axis='Race/Ethnicity',
                    gender_filter='All',
                    race_ethnicity_filter='All',
                    bgltq_filter='All',
                    fgli_filter='All',
                    class_year_filter='All',
                    school_filter='All',
                    concentration_filter='Computer Science',
                    width='65%')
            ]),
            T.BELONGING_P4,
            html.Div([
                base_static.serve_layout(
                    viz_index=19,
                    pathname='/explore/community-support-department',
                    axis='Gender',
                    gender_filter='All',
                    race_ethnicity_filter='All',
                    bgltq_filter='All',
                    fgli_filter='All',
                    class_year_filter='All',
                    school_filter='All',
                    concentration_filter='Computer Science',
                    width='65%',
                    custom_dropdown_value='Welcoming and inclusive'),
                html.Div([
                    T.BELONGING_P5
                ], style={'display' : 'inline-table', 'width' : '30%', 'margin-left' : '24px'})
            ]),
            html.Div([
                base_static.serve_layout(
                    viz_index=20,
                    pathname='/explore/community-support-students',
                    axis='Gender',
                    gender_filter='All',
                    race_ethnicity_filter='All',
                    bgltq_filter='All',
                    fgli_filter='All',
                    class_year_filter='All',
                    school_filter='All',
                    concentration_filter='Computer Science',
                    width='95%',
                    custom_dropdown_value='Welcoming and inclusive')
            ]),
            T.BELONGING_P6
        ])
    if tab == 'conclusion':
        return html.Div([
            T.CONCLUSION_P1,
            html.H4('Acknowledgements', style={'margin-top' : '24px'}),
            T.CONCLUSION_P2
        ])
    return html.Div([])
