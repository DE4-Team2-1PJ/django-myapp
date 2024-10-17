import os
from django.conf import settings
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px
import json
from django.shortcuts import render
from .models import Recruit
from datetime import datetime, timedelta

def job_list(request):
    today = datetime.now()
    end_of_week = today + timedelta(days=7)
    recruits = Recruit.objects.filter(end_date__lte=end_of_week, end_date__gte=today)
    return render(request, 'job_list.html', {'recruits': recruits})

    # recruits = Recruit.objects.all()
    # context = {'recruits' : recruits}
    # return render(request, 'job_list.html', context)

def job_table(request):
    recruits = Recruit.objects.all()
    context = {'recruits' : recruits}
    return render(request, 'job_table.html', context)

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
    df = pd.DataFrame(recruits)

    # 데이터 처리: 'platform_name'과 'category_name'이 없을 경우 기본값 지정
    df['platform_name'] = df.get('platform_name', 'Unknown')
    df['category_name'] = df.get('category_name', 'Unknown')

    # 첫 번째 라인 플롯 데이터 (플랫폼별 채용 공고 수)
    platform_counts = df['platform_name'].value_counts()
    platform_jobs_df = pd.DataFrame({
        'Platform': platform_counts.index,
        'Counts': platform_counts.values
    })

    # 두 번째 파이 차트 데이터 (카테고리별 채용 공고 수)
    category_counts = df['category_name'].value_counts()
    category_jobs_df = pd.DataFrame({
        'Category': category_counts.index,
        'Counts': category_counts.values
    })

    # 색상 정의
    colors = ['rgba(135, 162, 255, 1)', 'rgba(135, 162, 255, 0.5)', 'rgba(135, 162, 255, 0.2)']

    # Plotly Figure 생성
    fig = go.Figure()

    # 첫 번째 라인 플롯 (플랫폼 별 채용 공고)
    fig.add_trace(go.Scatter(x=platform_jobs_df['Platform'],
                             y=platform_jobs_df['Counts'],
                             mode='lines+markers',  # 라인과 점 모두 표시
                             name='플랫폼 별 채용 공고',
                             visible=True))  # 첫 번째 그래프는 처음에 보임

    # 두 번째 파이 차트 (카테고리 별 채용 공고)
    fig.add_trace(go.Pie(labels=category_jobs_df['Category'],
                         values=category_jobs_df['Counts'],
                         marker=dict(colors=colors),
                         textinfo='percent',
                         textposition='inside',
                         hoverinfo='label+percent',
                         name='카테고리 별 채용 공고',
                         visible=False))  # 두 번째 차트는 처음에 숨겨짐

    # 레이아웃에 버튼 추가 (updatemenus)
    fig.update_layout(
        updatemenus=[
            dict(
                type="buttons",
                direction="right",  # 버튼을 가로 방향으로 배치
                x=0.5,  # 버튼 위치 조정 (x축 중앙)
                y=1.2,  # 버튼을 상단에 배치
                xanchor='center',  # 버튼 중앙 정렬
                yanchor='top',     # 버튼 상단 정렬
                buttons=[
                    dict(label="플랫폼 별 채용 공고",
                         method="update",
                         args=[{"visible": [True, False]},  # 라인 플롯만 보임
                               {"xaxis.showgrid": True,  # X축 그리드 표시
                                "yaxis.showgrid": True,  # Y축 그리드 표시
                                "xaxis.visible": True,   # X축 표시
                                "yaxis.visible": True,   # Y축 표시
                                "plot_bgcolor": "rgba(135, 162, 255, 0.2)",  # 회색 배경
                                "paper_bgcolor": "rgba(255, 255, 255, 1)",  # 흰색 배경
                                "showlegend": False}]),  # 범례 숨김
                    dict(label="카테고리 별 채용 공고",
                         method="update",
                         args=[{"visible": [False, True]},  # 파이 차트만 보임
                               {"xaxis.showgrid": False,  # 그리드 숨김
                                "yaxis.showgrid": False,  # 그리드 숨김
                                "xaxis.visible": False,   # X축 숨김
                                "yaxis.visible": False,   # Y축 숨김
                                "plot_bgcolor": "rgba(255, 255, 255, 1)",  # 흰색 배경
                                "paper_bgcolor": "rgba(255, 255, 255, 1)",  # 흰색 종이 배경
                                "showlegend": True}])    # 파이 차트에서 범례 표시
                ]
            )
        ],
        xaxis=dict(showgrid=True),  # X축 그리드 기본값
        yaxis=dict(showgrid=True),  # Y축 그리드 기본값
        plot_bgcolor="rgba(135, 162, 255, 0.2)",  # 라인 플롯 기본 배경색 (회색)
        paper_bgcolor="rgba(255, 255, 255, 1)",  # 라인 플롯 기본 종이 배경색 (흰색)
        width=600, height=400,  # 차트 크기
        showlegend=False,        # 범례 기본값
        margin=dict(t=30)        # 위쪽 여백을 좁게 설정하여 버튼과 차트 간격 조정
    )

    # 지역 변환 및 시/도별 채용 공고 수 데이터 생성
    df['region_converted'] = df['region'].apply(convert_region)
    df_filtered = df.dropna(subset=['region_converted'])
    region_counts = df_filtered['region_converted'].value_counts()
    region_jobs_df = pd.DataFrame({
        'Region': region_counts.index,
        'Counts': region_counts.values
    })

    # 지도 데이터 불러오기
    geojson_path = os.path.join(settings.BASE_DIR, 'recruits', 'static', 'assets', 'TL_SCCO_CTPRVN.json')
    with open(geojson_path, encoding='utf-8') as f:
        geojson_data = json.load(f)

    # Choropleth (지역별 채용 공고 수)
    fig_choropleth = px.choropleth(region_jobs_df,
                                   geojson=geojson_data,
                                   locations='Region',
                                   featureidkey='properties.CTP_KOR_NM',
                                   color='Counts',
                                   title='시/도별 채용 공고 수',
                                   color_continuous_scale='Blues',
                                   width=900,
                                   height=700,
                                   range_color=[1, region_jobs_df['Counts'].max()])
    fig_choropleth.update_geos(fitbounds="locations", visible=False, projection_scale=16, 
                               center={"lat": 36.5, "lon": 127.5}, projection_type="mercator")
    fig_choropleth.update_layout(dragmode=False, geo=dict(showframe=False, showcoastlines=False, showland=True, landcolor="white"))

    # Plotly 그래프를 HTML로 변환
    line_plot_html = fig.to_html(full_html=False)
    choropleth_html = fig_choropleth.to_html(full_html=False)

    # 컨텍스트 설정
    context = {
        'line_plot_html': line_plot_html,
        'choropleth_html': choropleth_html
    }

    # 템플릿 렌더링
    return render(request, 'job_graph.html', context)