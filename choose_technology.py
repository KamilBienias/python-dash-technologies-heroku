import dash
import dash_core_components as dcc
import dash_html_components as html
import plotly.graph_objects as go
from dash.dependencies import Input, Output

external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

app = dash.Dash(__name__, external_stylesheets=external_stylesheets)
# to trzeba do heroku
# server = app.server
# to blokuje rzucanie wyjatkow, gdy callback nie jest w layout
app.config.suppress_callback_exceptions = True

app.layout = html.Div([
    dcc.Location(id='url', refresh=False),
    # sekcja wynikowa. Zmieniany bedzie parametr children
    html.Div(id='page-content')
], style={
    "background-color": '#B5D8CC',
    "height": "1000px"
})

index_page = html.Div([
    html.H3('MENU:'),
    # sekcja z linkami do podstron
    html.Div([
        html.Hr(),
        dcc.Link('Choose technology', href='/tech'),
        html.Br(),
        dcc.Link('Display what I have learned', href='/learned'),
        html.Hr()
    ], style={"background-color": "white"}  # otacza linki "Choose technology" i "Display..."
    ),
    html.H6('You are using the application in the development phase.')
], style={
    "textAlign": "center",
    "fontSize": 36,
    "color": "#545254"
})

tab_style = {
    "background-color": "#8A7090"
}

tab_selected_style = {
    "background-color": "#89A7A7",
    "borderTop": "5px solid #8D3B72"
}

tech_layout = html.Div([
    html.Div([
        html.H4('Choose a technology to view a code sample'),
        html.Hr(),
        dcc.Tabs(
            id='tech-1-tabs',
            children=[
                # label to wyswietlone na zakladce
                dcc.Tab(label='Python', value='tab-1', style=tab_style, selected_style=tab_selected_style),
                dcc.Tab(label='SQL', value='tab-2', style=tab_style, selected_style=tab_selected_style),
                dcc.Tab(label='Java', value='tab-3', style=tab_style, selected_style=tab_selected_style)
            ],
            # wartosc domyslna
            value='tab-1'
        )
    ], style={"fontSize": 28, "textAlign": "center"}),
    # sekcja wynikowa, to co wybralem jako zakladke
    html.Div(id='tech-1-div'),
    html.Hr(),
    html.Div([
        dcc.Link('Back to MENU', href='/')
    ])
], style={"fontSize": 20})

learned_layout = html.Div([
    html.Div([
        html.H4('Choose technology to see what I have learned')
    ], style={
        "fontSize": 32
    }),
    html.Hr(),
    dcc.RadioItems(
        id='learned-1-radio',
        options=[{'label': i, 'value': i} for i in ['Python', 'SQL', 'Java']]
    ),
    html.Hr(),
    # sekcja wynikowa, to co wybralem w radiobutton
    html.Div(id='learned-1-div'),
    html.Hr(),
    dcc.Link('Back to MENU', href='/')
], style={
    "textAlign": "center",
    "fontSize": 20
})


@app.callback(
    Output('page-content', 'children'),
    # funkcje zasila komponent Location o component_id='url'
    # Sciezke biore z jego wlasciwosci component_property='pathname'
    [Input('url', 'pathname')]
)
def display_page(pathname):
    if pathname == '/tech':
        return tech_layout
    elif pathname == '/learned':
        return learned_layout
    else:
        return index_page


@app.callback(
    Output('tech-1-div', 'children'),
    [Input('tech-1-tabs', 'value')]
)
def tech_1_tabs(value):
    if value == 'tab-1':
        return html.Div([
            dcc.Markdown('''
            ```python
            import pandas as pd

            df = pd.DataFrame(
                    {'A': [1,2,3,4], 
                     'B': [10,20,30,40],
                     'C': [20,40,60,80]}, 
                  index=['Row 1', 'Row 2', 'Row 3', 'Row 4'])

            df['D'] = df.apply(lambda x: x.sum(), axis=1)
            ```
            ''')
        ])
    elif value == 'tab-2':
        return html.Div([
            dcc.Markdown('''
            ```sql
            CREATE TABLE Persons (
                PersonID int,
                LastName varchar(255),
                FirstName varchar(255),
                Address varchar(255),
                City varchar(255)
            );
            ```
            ''')
        ])
    elif value == 'tab-3':
        return html.Div([
            dcc.Markdown('''
            ```
            public class Hello{
                public static void main(String[] args){
                    System.out.print("Hello World");
                }
            }       
            ```
            ''')
        ])


@app.callback(
    Output('learned-1-div', 'children'),
    [Input('learned-1-radio', 'value')]
)
def learned_1_radio(value):
    if value is None:
        return html.Div([
            html.H6('Select one of the options to display frameworks or extensions')
        ])
    elif value == 'Python':
        return html.Div([
            html.H4("I have learned: Django, Pandas, Scikit-Learn and Dash.")
        ])
    elif value == 'SQL':
        return html.Div([
            html.H4("I have learned Oracle 11g.")
        ])
    elif value == 'Java':
        return html.Div([
            html.H4("I have learned SpringBoot and FX.")
        ])

if __name__ == '__main__':
    app.run_server(debug=True)