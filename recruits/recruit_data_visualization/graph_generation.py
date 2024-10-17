import pandas as pd
import plotly.graph_objects as go
import plotly.express as px
import os
import json
from django.conf import settings
from .data_processing import get_job_data

def create_line_and_pie_charts(df):
    platform_counts = df['platform_name'].value_counts()
    platform_jobs_df = pd.DataFrame({
        'Platform': platform_counts.index,
        'Counts': platform_counts.values
    })

    category_counts = df['category_name'].value_counts()
    category_jobs_df = pd.DataFrame({
        'Category': category_counts.index,
        'Counts': category_counts.values
    })

    colors = ['rgba(135, 162, 255, 1)', 'rgba(135, 162, 255, 0.5)', 'rgba(135, 162, 255, 0.2)']

    fig = go.Figure()

    fig.add_trace(go.Scatter(x=platform_jobs_df['Platform'],
                             y=platform_jobs_df['Counts'],
                             mode='lines+markers',
                             name='플랫폼 별 채용 공고',
                             visible=True))

    fig.add_trace(go.Pie(labels=category_jobs_df['Category'],
                         values=category_jobs_df['Counts'],
                         marker=dict(colors=colors),
                         textinfo='percent',
                         textposition='inside',
                         hoverinfo='label+percent',
                         name='카테고리 별 채용 공고',
                         visible=False))

    fig.update_layout(
        updatemenus=[dict(type="buttons", direction="right", x=0.5, y=1.2, xanchor='center', yanchor='top',
                          buttons=[dict(label="플랫폼 별 채용 공고", method="update", args=[{"visible": [True, False]}]),
                                   dict(label="카테고리 별 채용 공고", method="update", args=[{"visible": [False, True]}])])],
        xaxis=dict(showgrid=True),
        yaxis=dict(showgrid=True),
        plot_bgcolor="rgba(135, 162, 255, 0.2)",
        paper_bgcolor="rgba(255, 255, 255, 1)",
        width=600, height=400,
        showlegend=False
    )
    return fig.to_html(full_html=False)

def create_choropleth(df_filtered):
    geojson_path = os.path.join(settings.BASE_DIR, 'recruits', 'static', 'assets', 'TL_SCCO_CTPRVN.json')
    with open(geojson_path, encoding='utf-8') as f:
        geojson_data = json.load(f)

    region_counts = df_filtered['region_converted'].value_counts()
    region_jobs_df = pd.DataFrame({
        'Region': region_counts.index,
        'Counts': region_counts.values
    })

    fig_choropleth = px.choropleth(region_jobs_df,
                                   geojson=geojson_data,
                                   locations='Region',
                                   featureidkey='properties.CTP_KOR_NM',
                                   color='Counts',
                                   title='시/도별 채용 공고 수',
                                   color_continuous_scale='Blues',
                                   width=900, height=700,
                                   range_color=[1, region_jobs_df['Counts'].max()])

    fig_choropleth.update_geos(fitbounds="locations", visible=False, projection_scale=16, center={"lat": 36.5, "lon": 127.5})
    fig_choropleth.update_layout(dragmode=False, geo=dict(showframe=False, showcoastlines=False, showland=True, landcolor="white"))

    return fig_choropleth.to_html(full_html=False)
