# -*- coding: utf-8 -*-
"""
Spyder Editor

This is a temporary script file.
"""
import dash
from dash import dcc
from dash import html
import pandas as pd
from dash.dependencies import Input, Output
import plotly.express as px
import dash_daq as daq
   

df = pd.read_csv(r'economic_freedom_index2019_data.csv', encoding = 'latin-1')

df.columns = ['CountryID', 'Country Name', 'WEBNAME', 'Region', 'World Rank',
        'Region Rank', '2019 Score', 'Property Rights', 'Judical Effectiveness',
        'Government Integrity', 'Tax Burden', 'Govt Spending', 'Fiscal Health',
        'Business Freedom', 'Labor Freedom', 'Monetary Freedom',
        'Trade Freedom', 'Investment Freedom ', 'Financial Freedom',
        'Tariff Rate (%)', 'Income Tax Rate (%)', 'Corporate Tax Rate (%)',
        'Tax Burden % of GDP', 'Govt Expenditure % of GDP ', 'Country',
        'Population (Millions)', 'GDP (Billions, PPP)', 'GDP Growth Rate (%)',
        '5 Year GDP Growth Rate (%)', 'GDP per Capita (PPP)',
        'Unemployment (%)', 'Inflation (%)', 'FDI Inflow (Millions)',
        'Public Debt (% of GDP)']

df['GDP (Billions, PPP)'] = df['GDP (Billions, PPP)'].apply(lambda x: str(x).replace('$','').replace(',','').split(' ')[0])
df['GDP (Billions, PPP)'] = df['GDP (Billions, PPP)'].apply(lambda x: float(x))

def CountryRank(country):
    main_df = df[df['Country']==country]
    WorldRank = main_df.iloc[0,4]
    return html.Div(id = "world-rank",
            children=[
                html.P("World Rank"),
                daq.LEDDisplay(
                    id="world-rank-display",
                    value = WorldRank,
                    color="#7fafdf",
                    backgroundColor="#252e3f",
                    size=70,
                            ),
                        ]
                    )
                                 
def RegionRank(country):
    main_df = df[df['Country']==country]
    RegionRank = main_df.iloc[0,5]
    return html.Div(id = "region-rank",
        children=[
            html.P("Rank within Region"),
            daq.LEDDisplay(
                id="region-rank-display",
                value = RegionRank,
                color="#7fafdf",
                backgroundColor="#252e3f",
                size=70,
                           ),
                  ]
                        )

def NoinRegion(country):
    main_df = df[df['Country']==country]
    Region = main_df.iloc[0,3]
    inregion = df[df['Region'] == Region]
    noinregion = len(inregion['Region'])
    return html.Div(id = "in-region-rank",
        children=[
            html.P("Number of Countries in Region"),
            daq.LEDDisplay(
                id="in-region-rank-display",
                value = noinregion,
                color="#7fafdf",
                backgroundColor="#252e3f",
                size=70,
                            ),
                    ]
                        )



averages = df.describe()
 
def displaygraph(country,graph_value):
    countryname = [country, "World Average", "Region Average"]
    emptylist = []
        
    main_df = df[df['Country']==country]
    region_df = df[df['Region']== main_df.iloc[0,3]]
    region_averages = region_df.describe()
        
    if graph_value == 'Judicial Effectiveness':
        a = 8
        b = 5
        y = 'Judicial Effectiveness'
    elif graph_value == 'Government Integrity':
            a = 9
            b = 6
            y = 'Government Integrity'
    elif graph_value == 'Property Rights':
        a = 7
        b = 5
        y = 'Property Rights'
    else:
        a = 8
        b = 5
        y = 'Judicial Effectiveness'
            
    emptylist.append(main_df.iloc[0,a])
    emptylist.append(averages.iloc[1,b])
    emptylist.append(region_averages.iloc[1,b])
        
    df_data = {'Country': countryname, y: emptylist}
    graph_df = pd.DataFrame(data = df_data)
        
    fig = px.bar(graph_df, x="Country", y=y, color="Country",
                 labels={'Country':'Country', y:y}, height=550, width = 510,
                     template='plotly_dark')
    fig.update_layout({'paper_bgcolor': '#252e3f', 'plot_bgcolor':'#252e3f', "font_color" : "#7fafdf"})
    return fig

titles = html.Div(id = "header",
                  children = [
                      html.H1(id ="maintitle",
                              children = ["2019 Economic Freedom Index by Country"]),
                      html.H2(id = "description",
                              children = [ "The Heritage Foundation produces a yearly ranking of countries' Economic Freedom based on a range of criteria.",
                                           "This dashboard allows exploration of that data and displays a countries overall economic freedom ranking, ",
                                           "it's ranking within it's region (continent) and the number of countries in that region.",
                                           " The graphs below show where each country stands on individual criteria against the world and region average.",
                                           " Dropdowns faciliatate choice of factors."
                                           " The data is from Heritage Foundation's 2019 report."
                                          ]),
                      html.A("Source on Kaggle",id = "Kaggle",
                            href = "https://www.kaggle.com/lewisduncan93/the-economic-freedom-index"
                             ),
                      html.A("The Heritage Foundation Data", id = "Heritage",
                             href = "https://www.heritage.org/index/")
                      ]
                  )

options = [{"label":i, "value":i} for i in df["Country"].unique()]
  
dropdown_box = html.Div(children = [
                dcc.Dropdown(
                        id='CountryDropdown',  
                        options=options,
                        clearable = False,
                        multi = False,
                        value='United Kingdom',            
                        placeholder="Select a country"
                 )
                ],
                    style = {'top':"80px","right" :"80px", "position":"absolute"}
    )

graph_options = ["Judicial Effectiveness","Government Integrity","Property Rights"]
graph_choices = [{"label":i, "value":i} for i in graph_options]          
  
graph_dropdown_1 = html.Div(id = "graph-container-1", children = [
               html.Div(children =  [
                   html.H3("Select Chart:"),        
                   dcc.Dropdown(
                        id='GraphDropdown1',  
                        options=graph_choices,
                        clearable = False,
                        multi = False,
                        value='Judicial Effectiveness',             
                        placeholder="Select a graph to display"
                 )]
                   ),
                 html.Div(children= 
                   dcc.Graph(
                            id = "graph_1"),
                    style ={"top": "20%"}
                         )  
                ],
                style = {'width': '25%', "position": "fixed", "left": "5%",
                         'display': 'inline-block',"top": "35%", "z-index":"1"}
    )
   
graph_dropdown_2 = html.Div(id = "graph-container-2", children = [
                html.Div(children =  [
                    html.H3("Select Chart:"),
                    dcc.Dropdown(
                        id='GraphDropdown2',  
                        options=graph_choices,
                        clearable = False,
                        multi = False,
                        value='Government Integrity',             
                        placeholder="Select a graph to display"
                 )]
                    ),
                  html.Div(children= 
                   dcc.Graph(
                            id = "graph_2"),
                    style ={"top": "20%"}
                         )
                ],
                style = {'width': '25%', "position": "fixed", "left": "37.5%",
                         'display': 'inline-block',"top": "35%", "z-index":"1"}
    )
 
graph_dropdown_3 = html.Div(id = "graph-container-3",children = 
            [html.Div(children = [
                    html.H3("Select Chart:"),
                    dcc.Dropdown(
                        id='GraphDropdown3',  
                        options=graph_choices,
                        clearable = False,
                        multi = False,
                        value='Property Rights',             
                        placeholder="Select a graph to display"
                    )] 
                         ),
                html.Div(children= 
                   dcc.Graph(
                            id = "graph_3"),
                    style ={"top": "20%"}
                         )
                ],
                    style = {'width': '25%', "position": "fixed", "left": "70%", 
                         'display': 'inline-block',"top": "35%", "z-index":"1"}
    )
  
app_container = html.Div(id = "app_content", children = [html.Div(id = "world_ranks")]
                            )

#graphs = html.Div(children = [html.Div(children = [dcc.Graph(id = "graph_1")], 
                                       #style = {'width': '25%', "position": "fixed", "left": "5%",
                                                ##'display': 'inline-block',"top":"40%", "z-index":"1",
                                                #"background-color":"#ffffff"}),
                              #html.Div(children = [dcc.Graph(id = "graph_2")], 
                                       #style = {'width': '25%', "position": "fixed", "left": "37.5%",
                                                #'display': 'inline-block',"top": "40%", "z-index":"1"})])
                              #html.Div(children = [dcc.Graph(id = "graph_3")], 
                                       #style = {'width': '25%', "position": "fixed", "left": "70%",
                                                #'display': 'inline-block',"top": "40%", "z-index":"1"})])


#main_div_style = {"background-color": "#ffffff", 
                      #"padding":"0", 
                      #"width":"100%", 
                      #"height":"100",
                      #"position": "fixed",
                      #"top": "0%",
                      #"left": "0",
                      #"bottom": "0",
                      #"font-family":"Open Sans",
                    #}
   
app = dash.Dash(__name__) 
app.title = "Economic Freedom Index by Country"
   
app.layout = html.Div(id = "main_div", children =[titles,dropdown_box, app_container,
                                                  graph_dropdown_1, graph_dropdown_2, graph_dropdown_3],
                          )
    
@app.callback([Output(component_id = "app_content", component_property = "children"),
                   Output(component_id = "graph_1", component_property = "figure"),
                   Output(component_id = "graph_2", component_property = "figure"),
                   Output(component_id = "graph_3", component_property = "figure")],
                  [Input(component_id = "CountryDropdown", component_property = "value"),
                   Input(component_id = "GraphDropdown1", component_property = "value"),
                   Input(component_id = "GraphDropdown2", component_property = "value"),
                   Input(component_id = "GraphDropdown3", component_property = "value")
                   ]
                 )
def render_tab_content(country,graphvalue1,graphvalue2,graphvalue3):
        fig1 = displaygraph(country=country,graph_value=graphvalue1)
        fig2 = displaygraph(country=country,graph_value=graphvalue2)
        fig3 = displaygraph(country=country,graph_value=graphvalue3)
        return (
            html.Div(
                id="status-container",
                children=[
                    CountryRank(country),
                    RegionRank(country),
                    NoinRegion(country)                
                ],                
            ),
        fig1,
        fig2,
        fig3
        )
    
    #Output(component_id = "graph_1", component_property = "figure"),
    #Output(component_id = "graph_2", component_property = "figure"),
    #Output(component_id = "graph_3", component_property = "figure"),

    #Input(component_id = "GraphDropdown1", component_property = "value"),
    #Input(component_id = "GraphDropdown2", component_property = "value"),
    #Input(component_id = "GraphDropdown3", component_property = "value"),  

if __name__ == '__main__':
    app.run_server(debug=False, port = 8080)
