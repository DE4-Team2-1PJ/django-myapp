import os
from django.conf import settings
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px
import json
from django.shortcuts import render
from .models import Recruit

regions_dict = {
    '서울': '서울특별시',
    '부산': '부산광역시',
    '대구': '대구광역시',
    '인천': '인천광역시',
    '광주': '광주광역시',
    '대전': '대전광역시',
    '울산': '울산광역시',
    '세종': '세종특별자치시',
    '경기': '경기도',
    '강원': '강원도',
    '충북': '충청북도',
    '충남': '충청남도',
    '전북': '전라북도',
    '전남': '전라남도',
    '경북': '경상북도',
    '경남': '경상남도',
    '제주': '제주특별자치도'
}

def job_list(request):
    recruits = Recruit.objects.all()
    context = {'recruits' : recruits}
    return render(request, 'job_list.html', context)

def job_table(request):
    recruits = Recruit.objects.all()
    context = {'recruits' : recruits}
    return render(request, 'job_table.html', context)

def convert_region(region):
    if region is None:
        return None
    for key in regions_dict:
        if region.startswith(key):
            return regions_dict[key]
    return None

def job_graph(request):
    # Recruit 데이터베이스에서 모든 데이터를 가져옴
    recruits = Recruit.objects.all().values()

    # Pandas DataFrame 생성
    df = pd.DataFrame(recruits)

    # 'platform_name'과 'category_name'이 없으면 기본값으로 처리
    if 'platform_name' not in df.columns:
        df['platform_name'] = 'Unknown'

    if 'category_name' not in df.columns:
        df['category_name'] = 'Unknown'

    # 플랫폼별 채용 공고 수 계산
    platform_counts = df['platform_name'].value_counts()
    platform_df = pd.DataFrame({
        'Platform': platform_counts.index,
        'Counts': platform_counts.values
    })

    # 플랫폼 그래프 색상 설정
    platform_colors = platform_df['Counts'] / platform_df['Counts'].max()
    platform_colors = [f'rgba(135, 162, 255, {c})' for c in platform_colors]

    # 플랫폼 별 파이 차트 생성
    fig_pie_platform = go.Figure(data=[go.Pie(labels=platform_df['Platform'],
                                              values=platform_df['Counts'],
                                              marker=dict(colors=platform_colors),
                                              textinfo='percent',
                                              textposition='inside')])

    fig_pie_platform.update_layout(title='플랫폼 별 채용 공고',
                                   width=600, height=400)

    # 카테고리별 채용 공고 수 계산
    category_counts = df['category_name'].value_counts()
    category_df = pd.DataFrame({
        'Category': category_counts.index,
        'Counts': category_counts.values
    })

    # 카테고리 그래프 색상 설정
    category_colors = ['rgba(135, 162, 255, 1)', 'rgba(135, 162, 255, 0.5)', 'rgba(135, 162, 255, 0.2)']

    # 카테고리 별 파이 차트 생성
    fig_pie_category = go.Figure(data=[go.Pie(labels=category_df['Category'],
                                              values=category_df['Counts'],
                                              marker=dict(colors=category_colors),
                                              textinfo='percent',
                                              textposition='inside')])

    fig_pie_category.update_layout(title='카테고리 별 채용 공고',
                                   width=600, height=400)
    
    df['region_converted'] = df['region'].apply(convert_region)
    df_filtered = df.dropna(subset=['region_converted'])
    region_counts = df_filtered['region_converted'].value_counts()
    region_df = pd.DataFrame({
        'Region': region_counts.index,
        'Counts': region_counts.values
    })

    geojson_path = os.path.join(settings.BASE_DIR, 'recruits', 'static', 'assets', 'TL_SCCO_CTPRVN.json')
    with open(geojson_path, encoding='utf-8') as f:
        geojson_data = json.load(f)

    fig_choropleth = px.choropleth(region_df,
                                   geojson=geojson_data,
                                   locations='Region',
                                   featureidkey='properties.CTP_KOR_NM',
                                   color='Counts',
                                   title='시/도별 채용 공고 수',
                                   color_continuous_scale='Blues',
                                   width=900,
                                   height=700,
                                   range_color=[1, region_df['Counts'].max()])
    fig_choropleth.update_geos(fitbounds="locations", visible=False, projection_scale=16, 
                               center={"lat": 36.5, "lon": 127.5}, projection_type="mercator")
    fig_choropleth.update_layout(dragmode=False, geo=dict(showframe=False, showcoastlines=False, showland=True, landcolor="white"))

    # Plotly 그래프를 HTML로 변환
    graph_platform_html = fig_pie_platform.to_html(full_html=False)
    graph_category_html = fig_pie_category.to_html(full_html=False)
    graph_choropleth_html = fig_choropleth.to_html(full_html=False)

    context = {
        'graph_platform': graph_platform_html,
        'graph_category': graph_category_html,
        'graph_choropleth': graph_choropleth_html
    }

    return render(request, 'job_graph.html', context)