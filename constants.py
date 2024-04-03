# CONSTANTS

# Minimum sample size
MIN_SAMPLE_SIZE = 5

# Drop columns
DROP_COLUMNS = ['StartDate', 'EndDate', 'Status', 'Progress', 'Duration (in seconds)', 'Finished', 'RecordedDate', 'ResponseId', 'DistributionChannel', 'UserLanguage']

# Schools
ARTS_HUMANITIES = ['Art, Film, and Visual Studies', 'Classics', 'Comparative Literature', 'East Asian Studies', 'English', 'Folklore and Mythology', 'Germanic Languages and Literatures', 'History and Literature', 'History of Art and Architecture', 'Linguistics', 'Music', 'Near Eastern Languages and Civilizations', 'Philosophy', 'Religion, Comparative Study of', 'Romance Languages and Literatures', 'Slavic Languages and Literatures', 'South Asian Studies', 'Theater, Dance, & Media']
SOCIAL_SCIENCES = ['African and African American Studies', 'Anthropology', 'Economics', 'Environmental Science and Public Policy', 'Government', 'History', 'History and Science', 'Psychology', 'Social Studies', 'Sociology', 'Women, Gender, and Sexuality, Study of']
PURE_SCIENCES = ['Astrophysics', 'Chemical and Physical Biology', 'Chemistry', 'Chemistry and Physics', 'Earth and Planetary Sciences', 'Human Developmental and Regenerative Biology', 'Human Evolutionary Biology', 'Integrative Biology', 'Mathematics', 'Molecular and Cellular Biology', 'Neuroscience', 'Physics', 'Statistics']
SEAS = ['Applied Mathematics', 'Biomedical Engineering', 'Computer Science', 'Electrical Engineering', 'Engineering Sciences', 'Environmental Science and Engineering', 'Mechanical Engineering']
UNDECIDED = ['Undecided']
NONE = ['None']

# Gender identity
MALE = ['Male']
NONMALE = ['Female', 'Non-binary/third gender', 'Agender', 'Genderqueer']

# Sexual orientation
STRAIGHT = ['Straight/Heterosexual']
NONSTRAIGHT = ['Gay or Lesbian', 'Bisexual', 'Asexual', 'Queer']

# Diagnosed with disability/impairment
DIAGNOSED = ['A sensory impairment (vision or hearing)', 'A mobility impairment', 'A learning disability (e.g., ADHD, dyslexia)', 'A mental health disorder']
NONDIAGNOSED = ['None, I have not be diagnosed with a disability or impairment']

# Likert scales
LIKERT_KNOWLEDGE_KEY = {
    'Significantly less knowledgeable' : 1,
    'Less knowledgeable' : 2,
    'Slightly less knowledgeable' : 3,
    'Similarly knowledgeable' : 4,
    'Slightly more knowledgeable' : 5,
    'More knowledgeable' : 6,
    'Significantly more knowledgeable' : 7
}

LIKERT_AGREEMENT_KEY = {
    'Strongly disagree' : 1,
    'Disagree' : 2,
    'Somewhat disagree' : 3,
    'Neither agree nor disagree' : 4,
    'Somewhat agree' : 5,
    'Agree' : 6,
    'Strongly agree' : 7
}

# Axes
VIZ_AXES_ALL = ['Gender', 'Race/Ethnicity', 'BGLTQ+', 'FGLI', 'Class Year', 'School']
VIZ_AXES_CS = ['Gender', 'Race/Ethnicity', 'BGLTQ+', 'FGLI', 'Class Year']

# Axes categories
GENDER_CATEGORIES = ['Male', 'Non-male']
RACE_ETHNICITY_CATEGORIES = ['Asian', 'Black or African American', 'Hispanic or Latinx', 'White']
BGLTQ_CATEGORIES = ['BGLTQ+', 'Non-BGLTQ+']
FGLI_CATEGORIES = ['FGLI', 'Non-FGLI']
CLASS_YEAR_CATEGORIES = ['First-year', 'Sophomore', 'Junior', 'Senior']
SCHOOL_CATEGORIES = ['Arts and Humanities', 'Social Sciences', 'Pure Sciences', 'Engineering and Applied Sciences']

# Filter options
GENDER_FILTER_OPTIONS = GENDER_CATEGORIES.copy()
GENDER_FILTER_OPTIONS.insert(0, 'All')
RACE_ETHNICITY_FILTER_OPTIONS = RACE_ETHNICITY_CATEGORIES.copy()
RACE_ETHNICITY_FILTER_OPTIONS.insert(0, 'All')
BGLTQ_FILTER_OPTIONS = BGLTQ_CATEGORIES.copy()
BGLTQ_FILTER_OPTIONS.insert(0, 'All')
FGLI_FILTER_OPTIONS = FGLI_CATEGORIES.copy()
FGLI_FILTER_OPTIONS.insert(0, 'All')
CLASS_YEAR_FILTER_OPTIONS = CLASS_YEAR_CATEGORIES.copy()
CLASS_YEAR_FILTER_OPTIONS.insert(0, 'All')
SCHOOL_FILTER_OPTIONS = SCHOOL_CATEGORIES.copy()
SCHOOL_FILTER_OPTIONS.insert(0, 'All')
CONCENTRATION_FILTER_OPTIONS = ['All', 'Computer Science']

# Question-specific constants
COURSE_CATEGORIES = [
    'CS50: Introduction to Computer Science I',
    'CS51: Introduction to Computer Science II',
    'CS61: Systems Programming and Machine Organization',
    'CS0xx, an introductory undergraduate-level course (other than CS50, CS51, CS61)',
    'CS1xx, an undergraduate-level course',
    'CS2xx, a graduate-level course'
]

PERSONAL_RESOURCE_CATEGORIES = [      
    'Close friends and family',
    'Fellow students',
    'Professional networks',
    'Alumni networks',
    'The Harvard Office of Career Services'
]

NUM_VIZ = 20

URL_SLUGS = {
    '/explore/background' : {
        'viz_type' : 'stacked_bar_standard',
        'question_id' : 'Q8',
        'audience' : 'all undergraduates',
        'tab' : 'background'
    },
    '/explore/future-cs-course' : {
        'viz_type' : 'stacked_bar_standard',
        'question_id' : 'Q20',
        'audience' : 'undergraduates who had taken a CS course',
        'tab' : 'post-grad'
    },
    '/explore/future-graduate-studies' : {
        'viz_type' : 'stacked_bar_standard',
        'question_id' : 'Q22',
        'audience' : 'CS concentrators',
        'tab' : 'post-grad'
    },
    '/explore/cs-knowledge' : {
        'viz_type' : 'stacked_bar_likert',
        'question_id' : {
            'Q10_1' : 'Computer programming',
            'Q10_2' : 'Theoretical CS',
            'Q10_3' : 'Economics and computation',
            'Q10_4' : 'Networks',
            'Q10_5' : 'Programming languages',
            'Q10_6' : 'Systems',
            'Q10_7' : 'Graphics, visualization, UI',
            'Q10_8' : 'Artificial intelligence'
        },
        'audience' : 'CS concentrators',
        'dropdown_label' : 'Topic',
        'tab' : 'academics'
    },
    '/explore/course-participation' : {
        'viz_type' : 'stacked_bar_likert',
        'question_id' : {
            'Q12_1' : 'Asking or answering questions during lecture',
            'Q12_2' : 'Asking or answering questions during sections',
            'Q12_3' : 'Asking or answering questions in an online forum (ex: Canvas, Piazza, Ed)',
            'Q12_4' : 'Privately asking the teaching staff questions'
        },
        'audience' : 'decided concentrators',
        'dropdown_label' : 'Location',
        'tab' : 'academics'
    },
    '/explore/problem-set-partners' : {
        'viz_type' : 'stacked_bar_likert',
        'question_id' : 'Q19',
        'audience' : 'undergraduates who had taken a CS course',
        'tab' : 'academics'
    },
    '/explore/identity-representation' : {
        'viz_type' : 'stacked_bar_likert',
        'question_id' : {
            'Q14_1' : 'The students in my primary concentration department',
            'Q14_2' : 'The teaching staff for courses in my primary concentration department'
        },
        'audience' : 'decided concentrators',
        'dropdown_label' : 'Group',
        'tab' : 'belonging'
    },
    '/explore/community-support-department' : {
        'viz_type' : 'stacked_bar_likert',
        'question_id' : {
            'Q31_1' : 'Academically supportive',
            'Q31_2' : 'Professionally supportive',
            'Q31_3' : 'Emotionally supportive',
            'Q31_4' : 'Welcoming and inclusive'
        },
        'dropdown_label' : '',
        'audience' : 'decided concentrators',
        'tab' : 'belonging'
    },
    '/explore/community-support-students' : {
        'viz_type' : 'stacked_bar_likert',
        'question_id' : {
            'Q43_1' : 'Academically supportive',
            'Q43_2' : 'Professionally supportive',
            'Q43_3' : 'Emotionally supportive',
            'Q43_4' : 'Welcoming and inclusive'
        },
        'dropdown_label' : '',
        'audience' : 'decided concentrators',
        'tab' : 'belonging'
    },
    '/explore/department-discrimination' : {
        'viz_type' : 'stacked_bar_likert',
        'question_id' : {
            'Q30_1' : 'Gender',
            'Q30_2' : 'Race/Ethnicity',
            'Q30_3' : 'Sexuality'
        },
        'audience' : 'decided concentrators',
        'dropdown_label' : 'Identity Category',
        'tab' : 'discrimination'
    },
    '/explore/course-enrollment' : {
        'viz_type' : 'bubble_chart',
        'question_id' : 'Q17',
        'audience' : 'undergraduates who had taken a CS course',
        'dropdown_label' : 'Course',
        'dropdown_options' : COURSE_CATEGORIES,
        'tab' : 'academics'
    },
    '/explore/department-engagement' : {
        'viz_type' : 'pie_chart_grid',
        'question_id' : 'Q13',
        'audience' : 'decided concentrators',
        'tab' : 'academics'
    },
    '/explore/professional-opportunities-referrals' : {
        'viz_type' : 'pie_chart_select',
        'question_id' : 'Q33',
        'audience' : 'all undergraduates',
        'dropdown_label' : 'Resource',
        'dropdown_options' : PERSONAL_RESOURCE_CATEGORIES,
        'tab' : 'post-grad'
    },
    '/explore/professional-opportunities-mentorship' : {
        'viz_type' : 'pie_chart_select',
        'question_id' : 'Q36',
        'audience' : 'all undergraduates',
        'dropdown_label' : 'Resource',
        'dropdown_options' : PERSONAL_RESOURCE_CATEGORIES,
        'tab' : 'post-grad'
    },
    '/explore/discrimination-experience' : {
        'viz_type' : 'stacked_bar_likert',
        'question_id' : {
            'Q29_1' : 'Gender',
            'Q29_2' : 'Race/Ethnicity',
            'Q29_3' : 'Sexuality'
        },
        'audience' : 'decided concentrators',
        'dropdown_label' : 'Identity Category',
        'tab' : 'discrimination'
    }
}

# Empty figure
EMPTY_FIGURE = {
    "layout": {
        "xaxis": {
            "visible": False
        },
        "yaxis": {
            "visible": False
        },
        "annotations": [
            {
                "text": "Not enough data",
                "xref": "paper",
                "yref": "paper",
                "showarrow": False,
                 "font": {
                    "size": 28
                }
            }
        ]
    }
}