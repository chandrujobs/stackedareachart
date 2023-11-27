import pandas as pd
import dash
from dash import dcc, html
from dash.dependencies import Input, Output
import plotly.express as px

# Load the dataset
data = pd.read_excel("C:/Users/Chandru/OneDrive/Desktop/Python Visuals/Sample - Superstore.xls", sheet_name="Orders")

# Preprocess the data
data['Order Year'] = data['Order Date'].dt.year
segmented_sales = data.groupby(['Order Year', 'Segment'])['Sales'].sum().reset_index()

# Create a Dash application
app = dash.Dash(__name__)

# Define the app layout
app.layout = html.Div([
    dcc.Dropdown(
        id='year-dropdown',
        options=[{'label': year, 'value': year} for year in segmented_sales['Order Year'].unique()],
        value=segmented_sales['Order Year'].unique(),
        multi=True
    ),
    dcc.Graph(id='stacked-area-chart')
])

# Define callback to update graph
@app.callback(
    Output('stacked-area-chart', 'figure'),
    [Input('year-dropdown', 'value')]
)
def update_graph(selected_years):
    filtered_data = segmented_sales[segmented_sales['Order Year'].isin(selected_years)]
    fig = px.area(filtered_data, x='Order Year', y='Sales', color='Segment', line_group='Segment')
    fig.update_layout(title='Sales by Customer Segment Over Time')
    return fig

# Run the app
if __name__ == '__main__':
    app.run_server(debug=True, port=8058)
