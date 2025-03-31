# LIBRARY IMPORTS


# LOCAL IMPORTS
import dash
from dash import dcc, html
import dash_bootstrap_components as dbc
import plotly.graph_objs as go
import pandas as pd
from dash.dependencies import Input, Output, State
import json
from collections import Counter, defaultdict
import re
# ----------------------------------------------------------------------------------------------- #
class Graphs():

# ----------------------------------------------------------------------------------------------- #
# it is gonna run rn haha, need to add self to make it work in the class
    # ------------------------------------------------------------------------------------------- #
    def process_most_played(input_file):
        with open(input_file, "r", encoding="utf-8") as file:
            data = json.load(file)

        play_counts = Counter()
        play_durations = {}

        for entry in data:
            key = entry.get("spotify_track_uri") or entry.get("spotify_episode_uri")
            if key:
                play_counts[key] += 1
                play_durations[key] = play_durations.get(key, 0) + entry.get("ms_played", 0)

        sorted_by_count = sorted(play_counts.items(), key=lambda x: x[1], reverse=True)[:20]
        sorted_by_hours = sorted(play_durations.items(), key=lambda x: x[1], reverse=True)[:20]

        top_10 = []
        seen_keys = set()

        for key, _ in sorted_by_count + sorted_by_hours:
            if key not in seen_keys:
                seen_keys.add(key)
                entry = {
                    "uri": key,
                    "times_played": play_counts[key],
                    "total_hours_played": round(play_durations[key] / 3600000, 2)
                }
                matching_entry = next((e for e in data if (e.get("spotify_track_uri") == key or e.get("spotify_episode_uri") == key)), None)
                if matching_entry:
                    entry["name"] = matching_entry.get("master_metadata_track_name") or matching_entry.get("episode_name")
                    entry["album"] = matching_entry.get("master_metadata_album_album_name") if matching_entry.get("master_metadata_track_name") else None
                top_10.append(entry)
        return pd.DataFrame(top_10)



    def process_most_skipped_songs(input_file):
        with open(input_file, "r", encoding="utf-8") as file:
            data = json.load(file)

        skip_counts = Counter()
        play_durations = {}

        for entry in data:
            key = entry.get("spotify_track_uri")
            if key:
                skip = entry.get("skipped")
                if skip is True:
                    skip_counts[key] += 1
                    play_durations[key] = play_durations.get(key, 0) + entry.get("ms_played", 0)

        sorted_by_skipped= sorted(skip_counts.items(), key=lambda x: x[1], reverse=True)[:20]
        top_10 = []
        seen_keys = set()

        for key, _ in sorted_by_skipped:
            if key not in seen_keys:
                seen_keys.add(key)
                entry = {
                    "uri": key,
                    "times_skipped": skip_counts[key],
                    "total_mins_played": round(play_durations[key] / 60000, 2)
                }
                matching_entry = next((e for e in data if (e.get("spotify_track_uri") == key)), None)
                if matching_entry:
                    entry["name"] = matching_entry.get("master_metadata_track_name")
                    entry["album"] = matching_entry.get("master_metadata_album_album_name") if matching_entry.get("master_metadata_track_name") else None
                top_10.append(entry)
        return pd.DataFrame(top_10)

    def process_day_time(input_file):
        with open(input_file, "r", encoding="utf-8") as file:
            data = json.load(file)

        morning_counts = Counter()
        afternoon_counts = Counter()
        evening_counts = Counter()
        night_counts = Counter()

        yearCount = {}

        for entry in data:
            key = entry.get("spotify_track_uri") or entry.get("spotify_episode_uri")
            if key:
                hourResult = int(entry.get("ts")[11:13])
                year = int(entry.get("ts")[0:4])

                if 6 <= hourResult < 12:
                    morning_counts[year] += 1
                elif 12 <= hourResult < 18:
                    afternoon_counts[year] += 1
                elif 18 <= hourResult < 24:
                    evening_counts[year] += 1
                else:
                    night_counts[year] += 1

                if year not in yearCount:
                    yearCount[year] = 1
                else:
                    yearCount[year] += 1

        return morning_counts, afternoon_counts, evening_counts, night_counts, yearCount


    def time_of_the_day(input_file):
        morning_counts, afternoon_counts, evening_counts, night_counts, yearCount = process_day_time(input_file)

        years = sorted(yearCount.keys())

        trace_morning = go.Scatter(
            x=years, 
            y=[morning_counts.get(year, 0) for year in years],
            mode='lines+markers',
            name='Morning'
        )
        trace_afternoon = go.Scatter(
            x=years, 
            y=[afternoon_counts.get(year, 0) for year in years], 
            mode='lines+markers', 
            name='Afternoon'
        )
        trace_evening = go.Scatter(
            x=years, 
            y=[evening_counts.get(year, 0) for year in years],
            mode='lines+markers',
            name='Evening'
        )
        trace_night = go.Scatter(
            x=years, 
            y=[night_counts.get(year, 0) for year in years],
            mode='lines+markers',
            name='Night'
        )

        figureId = {
            'data': [trace_morning, trace_afternoon, trace_evening, trace_night],
            'layout': go.Layout(
                title='Number of songs played yearly',
                xaxis={'title': 'Year'},
                yaxis={'title': 'Number of Songs Played'},
                hovermode='closest'
            )
        }
        app = dash.Dash(external_stylesheets=[dbc.themes.BOOTSTRAP])

        app.layout = html.Div(children=[
            html.H1(children='Songs played in each time of day'),

            html.Div(children='''not decided yet.'''),

            dcc.Graph(
                id='time_of_day_graph',
                figure=figureId
            ),
        ])

        if __name__ == '__main__':
            app.run(debug=True)

    def top10SkippedSDiagram(input_file):
        df = process_most_skipped_songs(input_file)
        df_songs = df[df["uri"].str.startswith("spotify:track")]

        trace_songs = go.Bar(
            x=df_songs["name"],
            y=df_songs["times_skipped"],
            text=df_songs["album"],
            name="Total Mins Played"
        )
        app = dash.Dash(external_stylesheets=[dbc.themes.BOOTSTRAP])

        app.layout = html.Div(children=[
            html.H1(children='Top 10 Most Skipped Songs'),
        
            html.Div(children='''Comparison of most skipped songs.'''),

            html.Div([
                dcc.Graph(
                    id='songs_graph',
                    figure={
                        'data': [trace_songs],
                        'layout': go.Layout(title='Top 10 Most Skipped Songs', xaxis={'title': 'Song'}, yaxis={'title': 'times_skipped'})
                    }
                ),
            ], style={'display': 'flex', 'justify-content': 'space-around'}),

            dbc.Modal(
                [
                    dbc.ModalHeader(id='modalheader'),
                    dbc.ModalBody(id='modalbody'),
                    dbc.ModalFooter(dbc.Button("Close", id="close", className="ml-auto")),
                ],
                size="lg",
                id="modal",
            )
        ])

        def display_modal(songs_click, episodes_click, close_clicks, is_open):
            ctx = dash.callback_context

            if ctx.triggered[0]['prop_id'] == "close.n_clicks":
                return "", "", False

            clickData = songs_click or episodes_click
            if clickData:
                point = clickData["points"][0]
                item_name = point["x"]
                total_skipped = point["y"]
                album_name = point.get("text", "Unknown Album")
                return (
                    item_name,
                    html.Div([
                        html.P(f"Total Mins Played: {total_skipped}"),
                        html.P(f"Album: {album_name}" if album_name else "No album information"),
                    ]),
                    True
            )

            raise dash.exceptions.PreventUpdate

        if __name__ == '__main__':
            app.run(debug=True)


    def top10SDiagram(input_file):
        df = process_most_played(input_file) 

        df_songs = df[df["uri"].str.startswith("spotify:track")]
        df_episodes = df[df["uri"].str.startswith("spotify:episode")]

        trace_songs = go.Bar(
            x=df_songs["name"],
            y=df_songs["total_hours_played"],
            text=df_songs["album"],  
            name="Total Hours Played (Songs)"
        )
        trace_episodes = go.Bar(
            x=df_episodes["name"],
            y=df_episodes["total_hours_played"],
            name="Total Hours Played (Episodes)"
        )

        app = dash.Dash(external_stylesheets=[dbc.themes.BOOTSTRAP])

        app.layout = html.Div(children=[
            html.H1(children='Top 10 Most Played Songs & Episodes'),
        
            html.Div(children='''Comparison of most played songs and podcast episodes.'''),

            html.Div([
                dcc.Graph(
                    id='songs_graph',
                    figure={
                        'data': [trace_songs],
                        'layout': go.Layout(title='Top 10 Most Played Songs', xaxis={'title': 'Song'}, yaxis={'title': 'Total Hours Played'})
                    }
                ),
                dcc.Graph(
                    id='episodes_graph',
                    figure={
                        'data': [trace_episodes],
                        'layout': go.Layout(title='Top 10 Most Played Episodes', xaxis={'title': 'Episode'}, yaxis={'title': 'Total Hours Played'})
                    }
                ),
            ], style={'display': 'flex', 'justify-content': 'space-around'}),

            dbc.Modal(
                [
                    dbc.ModalHeader(id='modalheader'),
                    dbc.ModalBody(id='modalbody'),
                    dbc.ModalFooter(dbc.Button("Close", id="close", className="ml-auto")),
                ],
                size="lg",
                id="modal",
            )
        ])

        @app.callback(
            [Output("modalheader", "children"), Output("modalbody", "children"), Output("modal", "is_open")],
                [Input("songs_graph", "clickData"), Input("episodes_graph", "clickData"), Input("close", "n_clicks")],
        [State("modal", "is_open")]
        )

        def display_modal(songs_click, episodes_click, close_clicks, is_open):
            ctx = dash.callback_context

            if ctx.triggered[0]['prop_id'] == "close.n_clicks":
                return "", "", False

            clickData = songs_click or episodes_click
            if clickData:
                point = clickData["points"][0]
                item_name = point["x"]
                hours_played = point["y"]
                album_name = point.get("text", "Unknown Album")
                return (
                    item_name,
                    html.Div([
                        html.P(f"Total Hours Played: {hours_played}"),
                        html.P(f"Album: {album_name}" if album_name else "No album information"),
                    ]),
                    True
            )

            raise dash.exceptions.PreventUpdate

        if __name__ == '__main__':
            app.run(debug=True)

    # top10SDiagram("Streaming_History_Audio_2021-2025.json")

    # top10SkippedSDiagram("Streaming_History_Audio_2021-2025.json")

    # time_of_the_day("testFiles/testSet/Streaming_History_Audio_2024_16.json")
