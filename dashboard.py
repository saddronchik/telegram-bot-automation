import dash
from dash import html, dcc
from dash.dependencies import Input, Output
import pandas as pd
import sqlite3

def load_data():
    conn = sqlite3.connect('appointments.db')
    df = pd.read_sql_query("SELECT name, date, time FROM appointments", conn)
    conn.close()
    return df

df = load_data()

app = dash.Dash(__name__)

app.layout = html.Div([
    html.H1("Дашборд записей через Telegram-бот"),
    html.P("Фильтруйте записи по имени, дате и времени."),
    
    dcc.Dropdown(
        id='name-filter',
        options=[{'label': n, 'value': n} for n in sorted(df['name'].unique())],
        placeholder="Выберите имя",
        multi=False
    ),
    
    dcc.DatePickerRange(
        id='date-filter',
        start_date=df['date'].min(),
        end_date=df['date'].max()
    ),
    
    dcc.Dropdown(
        id='time-filter',
        options=[{'label': t, 'value': t} for t in sorted(df['time'].unique())],
        multi=True,
        placeholder="Выберите время (можно несколько)"
    ),
    
    dcc.Graph(id='appointments-graph')
])

@app.callback(
    Output('appointments-graph', 'figure'),
    Input('name-filter', 'value'),
    Input('date-filter', 'start_date'),
    Input('date-filter', 'end_date'),
    Input('time-filter', 'value')
)
def update_graph(selected_name, start_date, end_date, selected_times):
    filtered = df.copy()
    if selected_name:
        filtered = filtered[filtered['name'] == selected_name]
    if start_date:
        filtered = filtered[filtered['date'] >= start_date]
    if end_date:
        filtered = filtered[filtered['date'] <= end_date]
    if selected_times:
        filtered = filtered[filtered['time'].isin(selected_times)]

    grouped = filtered.groupby('date').size().reset_index(name='count')

    fig = {
        'data': [{
            'x': grouped['date'],
            'y': grouped['count'],
            'type': 'bar',
            'name': 'Количество записей'
        }],
        'layout': {
            'title': 'Количество записей по дате',
            'xaxis': {'title': 'Дата'},
            'yaxis': {'title': 'Количество'}
        }
    }
    return fig

if __name__ == '__main__':
    app.run(debug=True)
