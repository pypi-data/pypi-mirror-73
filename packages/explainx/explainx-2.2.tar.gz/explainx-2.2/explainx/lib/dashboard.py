from imports import *
from plotly_graphs import *
from protodash import *
from insights import *
from plotly_css import *
import time
import performance_metrics
from performance_metrics import *
from explainx import explain

class dashboard():
    def __init__(self, key, secret):
        super(dashboard, self).__init__()
        self.param = None
        self.key=key
        self.secret= secret




    def increate_counter(self,model_name):
        # call api call here

        url = 'https://us-central1-explainx-25b88.cloudfunctions.net/increaseCounter'
        params = {

        }
        data = {
            "key": self.key,
            "secret": self.secret,
            "model": model_name

        }
        r = requests.post(url, params=params, json=data)
        if r.json()["message"]=="200":
            return True
        else:
            return False

    def find(self, df, y_variable, y_variable_predict, mode, param):
        self.available_columns = available_columns = list(df.columns)
        original_variables = [col for col in df.columns if '_impact' in col]
        self.impact_variables = [col for col in original_variables if not '_rescaled' in col]
        self.y_variable = y_variable
        self.y_variable_predict = y_variable_predict
        self.param = param

        self.insights = insights(self.param)

        d = self.dash(df, mode)

        return True

    def dash(self, df, mode):

        y_variable = self.y_variable

        g = plotly_graphs()
        y_variables = [col for col in df.columns if '_impact' in col]
        original_variables = [col for col in df.columns if not '_impact' in col]
        original_variables = [col for col in original_variables if not '_rescaled' in col]
        array = []

        row_number = 1
        # y_variable = "predict"
        columns = ['index', '0', '1', '2', '3', '4']
        dat = []

        available_columns = list(df.columns)

        external_stylesheets = ['https://codepen.io/rab657/pen/LYpKraq.css',
                                {
                                    'href': 'https://stackpath.bootstrapcdn.com/bootstrap/4.5.0/css/bootstrap.min.css',
                                    'rel': 'stylesheet'
                                }
                                ]

        app = JupyterDash(__name__, external_stylesheets=external_stylesheets)

        app.title = "explainX.ai - Main Dashboard"

        navbar = dbc.Navbar(
            [
                html.A(
                    # Use row and col to control vertical alignment of logo / brand
                    dbc.Row(
                        [
                            dbc.Col(dbc.NavbarBrand("explainX.ai DASHBOARD", className="ml-2"))
                        ],
                        align="center",
                        no_gutters=True,
                    ),
                    href="https://plot.ly",
                ),

                html.A(
                    # Use row and col to control vertical alignment of logo / brand
                    dbc.Row(
                        [
                            dbc.Col(dbc.NavbarBrand("Explain any machine learning model", className="ml-4"))
                        ],
                        align="center",
                        no_gutters=True,
                    ),
                    href="https://plot.ly",
                ),
                dbc.NavbarToggler(id="navbar-toggler"),

            ],
            color="dark",
            dark=True,
        )

        app.layout = html.Div([
            navbar,
    #         html.Div([
    #             dbc.Card(
    #     [
    #         dbc.CardHeader(
    #             html.H2(
    #                 dbc.Button(
    #                 "View Model Metrics",
    #                 id="collapse-button-2",
    #                 color="link", 
    #                 style={'fontSize':'14px'})
    #             )
    #         ),
    #         dbc.Collapse(html.Div([
    #                 html.H4('',
    #                         style=style1),
    #                 html.Div([
    #                     dbc.Row(
    #                     [
    #                         dbc.Col(html.Div([
                                
    #                            html.Div(id='classification_metrics_1',style={'marginTop':"20px", 'marginBottom':"5px"})

    #                         ])),
                            
    #                         dbc.Col(html.Div([
    #                             html.Div(id="roc_curve")
    #                         ])),
    #                         dbc.Col(html.Div("One of three columns")),
    #                     ], style={'margin':20, 'marginTop':'-20px'} )])
    #             ], style={'marginTop': 0}), id="collapse-2"),
    #     ]
    # ),],style=style4),
    #End of collapsable div 2
            html.Div([
                dbc.Card(
        [
            dbc.CardHeader(
                html.H2(
                    dbc.Button(
                    "View Your Data",
                    id="collapse-button",
                    color="link", 
                    style={'fontSize':'14px'})
                )
            ),
            dbc.Collapse(html.Div([
                    html.H4('',
                            style=style1),
                    html.Div([
                        dash_table.DataTable(
                            id='datatable-interactivity',
                            columns=[
                                {"name": i, "id": i, "deletable": False, "selectable": True} for i in df.columns
                            ],
                            data=df.to_dict('records'),
                            editable=True,
                            filter_action="native",
                            sort_mode="multi",
                            row_selectable="multi",
                            row_deletable=False,
                            selected_columns=[],
                            selected_rows=[],
                            page_action="native",
                            page_current=0,
                            page_size=10,
                            style_table=style2,
                            style_header=style3,
                            style_cell={
                                "font-family": "Helvetica, Arial, sans-serif",
                                "fontSize": "11px",
                                'width': '{}%'.format(len(df.columns)),
                                'textOverflow': 'ellipsis',
                                'overflow': 'hidden',
                                'textAlign': 'left',
                                'minWidth': '180px', 'width': '180px', 'maxWidth': '180px',
                            },
                            css=[
                                {
                                    'selector': '.dash-spreadsheet td div',

                                    'rule': '''
                                    line-height: 15px;
                                    max-height: 20px; min-height: 20px; height: 20px;
                                    display: block;
                                    overflow-y: hidden;

                                '''
                                }])
                    ])

                ], style={'marginTop': 0}), id="collapse"),
        ]
    ),],style=style4),

            # end of collapsable div
            dcc.Tabs(id="tabs-styled-with-inline", value='tab-1', children=[
                dcc.Tab(label='Global Explanation', value='tab-1', children=[

                    # Global Feature Impact & Importance
                    html.Div(id='datatable-interactivity-container', children=[
                        html.Div([
                            html.Div([
                                html.H4('Global Feature Importance',
                                        style=style5),
                                html.P(
                                    'Feature importance assign a score to input features based on how useful they are at predicting a target variable. ',
                                    style=style6)
                                ,
                                dcc.Loading(
                                    id="loading-1",
                                    type="circle",
                                    children=dbc.Row(
                                        [
                                            dbc.Col(html.Div(dcc.Graph(id="global_feature_importance",
                                                                       style={'marginLeft': 50, 'marginTop': 0,
                                                                              'height': '500px'}
                                                                       )), width=9),
                                            dbc.Col(
                                                [
                                                    html.Div([
                                                        html.H2("How to read this graph?"),
                                                        html.P(
                                                            "This graph helps you identify which features in your dataset have the greatest effect on the outcomes of your machine learning model")
                                                    ]),
                                                    html.Div([
                                                        html.H2("Insights"),
                                                        html.P(id='global_message_1'),
                                                        html.P(id='global_message_2'),
                                                        html.P(id='global_message_3'),
                                                        html.P(id='global_message_4'),
                                                        html.P(id='global_message_5')

                                                    ]

                                                    )]
                                            )

                                        ])

                                )
                                , ], style=style7,
                            ),

                            html.Div([
                                html.H4('Global Feature Impact',
                                        style=style8),
                                html.P(
                                    'Feature impact identifies which features (also known as columns or inputs) in a dataset have the greatest positive or negative effect on the outcomes of a machine learning model.',
                                    style=style9),
                                dcc.Loading(
                                    id="loading-2",
                                    type="circle",
                                    children=dbc.Row(
                                        [
                                            dbc.Col(html.Div(dcc.Graph(id='global_feature_impact',
                                                                       style={'marginLeft': 50, 'marginTop': 0,
                                                                              'height': '500px'})), width=9),
                                            dbc.Col(
                                                [
                                                    html.Div([
                                                        html.H2("How to read this graph?"),
                                                        html.P(
                                                            "This tells you which features have positive impact and which features have negative impact on the output of the decision")
                                                    ]),
                                                    html.Div([
                                                        html.H2("Insights"),
                                                        html.P(id='message_1'),
                                                        html.P(id='message_2'),
                                                        html.P(id='message_3')
                                                    ]

                                                    )]
                                            )

                                        ])

                                )

                            ],
                                style=style10,
                            ),
                        ],

                            style=style11
                        )
                    ], style={'height': '400'})
                ]),

                dcc.Tab(label='Feature Interaction', value='tab-2', children=[

                    dcc.Loading(
                        id="feature_interaction_load",
                        type="circle",
                        children=html.Div([
                            html.Div([
                                html.H4('Partial Dependence Plot',
                                        style=style12),
                                html.P(
                                    'The partial dependence plot (short PDP or PD plot) shows the marginal effect one or two features have on the predicted outcome of a machine learning model',
                                    style=style13),
                                html.Div([
                                    html.P('Variable Name'),
                                    dcc.Dropdown(
                                        id='xaxis-column',
                                        options=[{'label': i, 'value': i} for i in original_variables],
                                        value=original_variables[1],
                                        clearable=False
                                    ),

                                ],
                                    style={'width': '20%', 'marginLeft': 70, 'float': 'left',
                                           'display': 'inline-block'}),

                                html.Div([
                                    html.P("Variable Impact Values"),
                                    dcc.Dropdown(
                                        id='yaxis-column',
                                        options=[{'label': i, 'value': i} for i in y_variables],
                                        value=y_variables[1],
                                        clearable=False
                                    ),

                                ], style=style14),

                                html.Div([
                                    html.P('3rd Variable'),
                                    dcc.Dropdown(
                                        id='third-axis',
                                        options=[{'label': i, 'value': i} for i in original_variables],
                                        value=original_variables[-3],
                                        clearable=False
                                    ),

                                ], style=style15),
                            ]),
                            dcc.Loading(
                                id="loading-5",
                                type="circle",
                                children=dcc.Graph(id='indicator-graphic', style={'marginLeft': 50})
                            ),
                        ],
                            style=style16),
                    ),

                    dcc.Loading(
                        id="loading-2-pdp",
                        type='circle',
                        children=html.Div([
                            html.Div([
                                html.H4('Summary Plot',
                                        style=style17),
                                html.P(
                                    'In the summary plot, we see first indications of the relationship between the value of a feature and the impact on the prediction',
                                    style=style18),

                                    html.Button('Display Summary Plot', id='btn-nclicks-2', n_clicks=0, style=style34),
                                dcc.Loading(
                                    id="loading-3",
                                    type="circle",
                                    children=dcc.Graph(id='summary_plot', style={'marginLeft': 50, 'height': '600px'})

                                ),

                            ], style=style19),
                        ], style=style20)
                    )

                ]),

                # tab 3:Distribution

                dcc.Tab(label='Distribution',value='tab-3',  children=[

                    html.Div([

                        html.Div([
                            html.Div([
                                html.H4('Distributions',
                                        style=style21),
                                html.Div([
                                    html.P('Variable Name'),
                                    dcc.Dropdown(
                                        id='xaxis-column-name',
                                        options=[{'label': i, 'value': i} for i in original_variables],
                                        value=original_variables[0]
                                    ),
                                ],
                                    style=style22),
                                html.Div([
                                    html.P('Plot Type'),
                                    dcc.Dropdown(
                                        id='plot_type',
                                        options=[{'label': 'Violin Plot', 'value': 'Violin Plot'},
                                                 {'label': 'Histogram', 'value': 'Histogram'}, ],
                                        value='Histogram'
                                    ),
                                ],
                                    style=style23),

                            ]),

                            dcc.Graph(id='indicator-graphic2',
                                      style={'marginLeft': 50, 'marginTop': 100, 'height': '500px'}),
                        ],
                            style=style24),

                        html.Div([

                            html.Div([
                                    html.H4('Multi-Level EDA', style=style21),
                            html.Div([
                                html.P('X-Axis Variable'),
                                dcc.Dropdown(
                                    id='x_axis',
                                    options=[{'label':i, 'value':i} for i in original_variables],
                                    value=original_variables[0]
                                ),
                            ], style=style22),
                            html.Div([
                                html.P('Y-Axis Variable'),
                                dcc.Dropdown(
                                    id='y_axis',
                                    options=[{'label':i, 'value':i} for i in original_variables],
                                    value=original_variables[1]
                                ),
                            ], style=style22),
                            html.Div([
                                html.P('Size'),
                                dcc.Dropdown(
                                    id='size',
                                    options=[{'label':i, 'value':i} for i in original_variables],
                                    # value=original_variables[0]
                                    placeholder="Choose a variable"
                                ),
                            ], style=style22),
                            html.Div([
                                html.P('Color'),
                                dcc.Dropdown(
                                    id='color',
                                    options=[{'label':i, 'value':i} for i in original_variables],
                                    placeholder="Choose a variable"
                                ),
                            ], style=style22),
                            html.Div([
                                html.P('Drill-down by Column'),
                                dcc.Dropdown(
                                    id='facet_col',
                                    options=[{'label':i, 'value':i} for i in original_variables],
                                    placeholder="Select a categorical variable"
                                    # value=original_variables[0]
                                ),
                            ], style=style22),
                            html.Div([
                                html.P('Drill-down by Row'),
                                dcc.Dropdown(
                                    id='facet_row',
                                    options=[{'label':i, 'value':i} for i in original_variables],
                                    placeholder="Select a categorical variable"
                                ),
                            ], style=style22)
                            ]),
                             dcc.Graph(id='multi_level_eda',
                                      style={'marginLeft': 50, 'marginTop': 200, 'height': '700px'})
                            
                        ], style=style24)

                    ], style=style25)

                ]),
                # tab 4:Local Explanation

                dcc.Tab(label='Local Explanation', value='tab-4', children=[

                    html.Div([

                        # Input and Data
                        html.Div([

                            html.Div([
                                html.H4('Data',
                                        style=style26),
                                html.I("Index of Row That You Want To Explain.", style={'padding-left': '70px'}),

                                dcc.Input(id="row_number", type="number", value=1,
                                          placeholder="Enter a Row Number e.g. 1, 4, 5",
                                          style={'text-align': 'center'}),
                                
                                html.Div(id='local_data_table',style={'marginTop':"20px", 'marginBottom':"5px"}),
                                          
                        
                            ]),

                        ]),  # End of Input & Data Div

                        dcc.Tabs([
                            dcc.Tab(label='Local Feature Explanation', children=[

                                html.Div(id='datatable-interactivity-container2', children=[
                                    html.Div([

                                        html.Div([
                                            html.H4('Local Feature Impact',
                                                    style=style29),
                                            html.P(
                                                'Local Feature impact identifies which features have the greatest positive or negative effect on the outcome of a machine learning model for a specific row.',
                                                style=style30),
                                            dcc.Loading(
                                                id="local_feature_impact_1",
                                                type="circle",
                                                children=dbc.Row(
                                                    [
                                                        dbc.Col(html.Div(dcc.Graph(id='local_feature_impact',
                                                                                   style={'marginLeft': 50,
                                                                                          'marginTop': 0,
                                                                                          'height': '500px'})),
                                                                width=8),
                                                        dbc.Col(
                                                            [
                                                                html.Div([
                                                                    html.H2("How to read this graph?"),
                                                                    html.P(
                                                                        "According to the model, the features are most important in explaining the target variable. Most importance is on the top.")
                                                                ]),
                                                                html.Div([
                                                                    html.H2("Insights"),
                                                                    html.P(id='local_message_1'),
                                                                    html.P(id='local_message_2'),
                                                                    html.P(id='local_message_3')
                                                                ]),
                                                                html.Div([
                                                                    html.H2("Next Steps"),
                                                                    html.P(
                                                                        "Click on the similar profile tabs and explore profiles that had similar attributes"),
                                                                ])
                                                            ]
                                                            , width=4),

                                                    ]))

                                        ],
                                            style=style31,
                                        ),
                                    ],

                                        style=style32)], style={'height': '400'})

                            ]),

                            dcc.Tab(id="similar_tabs", label='Similar Profiles', children=[

                                html.Div([
                                    html.H4('Similar Profiles',
                                            style=style33),

                                    html.Button('Display Similar Profiles', id='btn-nclicks-1', n_clicks=0,
                                                style=style34),

                                    html.P(
                                        'Display similar  profiles and the extent to which they are similar to the chosen applicant as indicated by the last row in the table below labelled as "Weight"',
                                        style=style35),
                                    html.Div([
                                        dcc.Loading(
                                            id="table",
                                            type="circle",
                                            children=dash_table.DataTable(
                                                id='prototype_data',
                                                columns=[{"name": i, "id": i} for i in columns],
                                                data=[],
                                                editable=False,
                                                # filter_action="native",
                                                sort_mode="multi",
                                                row_deletable=False,
                                                page_action="native",
                                                page_current=0,
                                                page_size=len(original_variables) + 1,
                                                style_table=style36,
                                                style_header=style37,
                                                style_cell={
                                                    "font-family": "Helvetica, Arial, sans-serif",
                                                    "fontSize": "15px",
                                                    'width': '{}%'.format(len(df.columns)),
                                                    'textOverflow': 'ellipsis',
                                                    'overflow': 'hidden',
                                                    'textAlign': 'left',
                                                    'minWidth': '180px', 'width': '180px', 'maxWidth': '180px',
                                                    "marginBottom": "100px"
                                                },
                                                style_data_conditional=[
                                                    {
                                                        'if': {

                                                            'filter_query': '{index} = "Weight(%)"'

                                                        },
                                                        "backgroundColor": "green",
                                                        'color': 'white'

                                                    }

                                                ],
                                                #
                                            )
                                        )

                                    ])

                                ], style=style39),

                            ])

                        ], style={'marginTop': 50}), ])

                ])

            ]), ], style=style40)

        # Callbacks transferred
        @app.callback(
            Output('datatable-interactivity', 'style_data_conditional'),
            [Input('datatable-interactivity', 'selected_columns')]
        )
        def update_styles(selected_columns):
            return [{
                'if': {'column_id': i},
                'background_color': '#D2F3FF'
            } for i in selected_columns]

        @app.callback(
            Output("collapse", "is_open"),
            [Input("collapse-button", "n_clicks")],
            [State("collapse", "is_open")],
        )
        def toggle_collapse(n, is_open):
            if n:
                return not is_open
            return is_open

        # #second collapse
        # @app.callback(
        #     Output("collapse-2", "is_open"),
        #     [Input("collapse-button-2", "n_clicks")],
        #     [State("collapse-2", "is_open")],
        # )
        # def toggle_collapse(n, is_open):
        #     if n:
        #         return not is_open
        #     return is_open

        # Global Feature Importance
        @app.callback(
            [Output('global_feature_importance', "figure"),
             Output('global_message_1', "children"),
             Output('global_message_2', "children"),
             Output('global_message_3', "children"),
             Output('global_message_4', "children"),
             Output('global_message_5', "children")],
            [Input('datatable-interactivity', "derived_virtual_data"),
             Input('datatable-interactivity', "derived_virtual_selected_rows")])
        def update_graphs(rows, derived_virtual_selected_rows):
            
            dff = df if rows is None else pd.DataFrame(rows)
            g = plotly_graphs()
            figure, data = g.feature_importance(dff)
            message = self.insights.insight_1_feature_imp(data)
           
            if len(message) == 4:
                return figure, message[0], message[1], message[2], message[3], ""
            return figure, message[0], message[1], message[2], message[3], message[4]

        # Global Feature Impact
        @app.callback(
            [Output('global_feature_impact', "figure"),
             Output('message_1', "children"),
             Output('message_2', "children"),
             Output('message_3', "children")],
            [Input('datatable-interactivity', "derived_virtual_data"),
             Input('datatable-interactivity', "derived_virtual_selected_rows")])
        def update_graphs(rows, derived_virtual_selected_rows):
            dff = df if rows is None else pd.DataFrame(rows)
            g = plotly_graphs()
            figure, data = g.feature_impact(dff)
            message = self.insights.insight_2_global_feature_impact(data)
            return figure, message[0], message[1], message[2]

        #Classification Metrics
        # @app.callback(
        #     Output(component_id='classification_metrics_1', component_property='children'),
        #     [Input('datatable-interactivity', "derived_virtual_data")])
        # def update_classification(rows):
        #     data = df 
        #     figure = clf_performance(data.y_actual, data.y_prediction).F_pos_F_neg()
        #     figure_a = clf_performance(data.y_actual, data.y_prediction).fp_fn_table()
        #     figure2 = dbc.Table.from_dataframe(figure, striped=True, bordered=True, hover=True, responsive=True, size='lg', style={'font-size': '12px'})
        #     figure3 = dbc.Table.from_dataframe(figure_a, striped=True, bordered=True, hover=True, responsive=True, size='lg', style={'font-size': '12px'})

            
        #     return figure3, figure2
        
        #ROC curnve
        # @app.callback(
        #     Output(component_id="roc_curve", component_property='children'),
        #     [Input('datatable-interactivity', 'derived_virtual_data')])
        # def update_roc_curve(rows):
        #     data = df
        #     init = explain.explain()
        #     figure = clf_performance(data.y_actual, data.y_prediction).plot_roc_curve(init.model, init.X_test)
        #     return figure


        @app.callback(
            Output(component_id='local_data_table', component_property='children'),
            [Input(component_id='row_number', component_property='value')])
        def update_local_table(row_number):
            i = 0
            if type(row_number) == type(1):
                i = row_number
            array = df[i:i + 1]
            array1 = array
            impact_variables = [col for col in array if '_impact' in col]
            for col in impact_variables:
                array1.drop([col], axis=1, inplace=True)
            figure = dbc.Table.from_dataframe(array1, striped=True, bordered=True, hover=True, responsive=True, size='lg', style={'font-size': '12px'})
            #data = pd.DataFrame(df.iloc[row_number])
            return figure

         # Local Feature Impact Graph
        @app.callback(
            [Output('local_feature_impact', "figure"),
             Output('local_message_1', "children"),
             Output('local_message_2', "children"),
             Output('local_message_3', "children")],
            [Input(component_id='row_number', component_property='value')
                #  Input('data_table_row', "data")
                 ])
        def update_impact_graph(row_number):
            i = 0
            if type(row_number) == type(1):
                i = row_number
            array = df[i:i + 1]
            #data = pd.DataFrame(data)
            figure, dat = g.feature_impact(array)
            message = self.insights.insight_2_local_feature_impact(dat)
            return figure, message[0], message[1], message[2]



        # Partial Dependence Plot Graph
        @app.callback(
            Output('indicator-graphic', 'figure'),
            [Input('xaxis-column', 'value'),
             Input('yaxis-column', 'value'),
             Input('third-axis', 'value'),
             Input('datatable-interactivity', "derived_virtual_data"),
             Input('datatable-interactivity', "derived_virtual_selected_rows")
                # ,Input('tabs-styled-with-inline', "value")
             ])
        def update_graph(xaxis_column_name, yaxis_column_name, third_axis_name, rows, derived_virtual_selected_rows):
            # if tab=='tab-2':
            df3 = df if rows is None else pd.DataFrame(rows)
            g = plotly_graphs()
            fig, __ = g.partial_dependence_plot(df3, df3[xaxis_column_name], df3[yaxis_column_name],
                                                    df3[third_axis_name])

            return fig
            # else:
            #     return {}


        # Prototypical Analysis
        @app.callback(
            Output(component_id='prototype_data', component_property='data'),
            [Input(component_id='row_number', component_property='value'),
             Input('btn-nclicks-1', 'n_clicks')])
        def update_table(row_number, btn1):
            changed_id = [p['prop_id'] for p in dash.callback_context.triggered][0]
            if 'btn-nclicks-1' in changed_id:
                p = protodash()
                p.preprocess_data(df, y_variable)
                dfs = p.find_prototypes(row_number)
                dat = dfs.T.reset_index()
                dat = dat.to_dict('records')
                return dat
            else:
                return []

        # Summary Plot
        @app.callback(
            Output('summary_plot', 'figure'),
            [Input('datatable-interactivity', "derived_virtual_data"),
            Input('btn-nclicks-2', 'n_clicks')
             ])
        def update_graph2(rows,btn):
            changed_id = [p['prop_id'] for p in dash.callback_context.triggered][0]
            if 'btn-nclicks-2' in changed_id:
                dff = df if rows is None else pd.DataFrame(rows)
                sp, __ = g.summary_plot(dff)
                return sp
            else:
                return {}

        # Distributions
        @app.callback(
            Output('indicator-graphic2', 'figure'),
            [Input('xaxis-column-name', 'value'),
             Input('plot_type', 'value')
             ])
        def update_graph2(xaxis_column_name, plot_type):
            df3 = df
            # For categorical variables only
            cat_variables = []
            num_variables = []
            for i in original_variables:
                if df[i].dtype == 'object':
                    cat_variables.append(i)
                else:
                    num_variables.append(i)

            if plot_type == "Histogram":
                # group_labels = ['xxaxis_column_name']
                return px.histogram(df3, x=xaxis_column_name, marginal="box")
            else:
                for i in cat_variables:
                    return px.violin(df3, x=xaxis_column_name, box=True, points='all')
                else:
                    return px.violin(df3, y=xaxis_column_name, box=True, points='all', )

        #Multi Level EDA
        @app.callback(
            Output('multi_level_eda', 'figure'),
            [Input('x_axis','value'),
            Input('y_axis', 'value'),
            Input('size','value'),
            Input('color','value'),
            Input('facet_col','value'),
            Input('facet_row','value')]
        )
        def multi_level(x_axis, y_axis,size,color, facet_col,facet_row):
            df3 = df
            return px.scatter(df3, x=x_axis, y=y_axis, size=size, color=color, facet_col=facet_col,facet_row=facet_row, facet_col_wrap=4)

       
    #Port Finder
        if mode == "inline":
            app.run_server(mode="inline")
        else:
            try:
                try:
                    app.run_server(host='0.0.0.0', port=8080)
                except:
                    app.run_server(host='0.0.0.0', port=self.find_free_port())
            except:
                try:
                    app.run_server(port=8080)
                except:
                    app.run_server(port=self.find_free_port())

        return True

    def find_free_port(self):
        with closing(socket.socket(socket.AF_INET, socket.SOCK_STREAM)) as s:
            s.bind(('', 0))
            s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
            return s.getsockname()[1]
