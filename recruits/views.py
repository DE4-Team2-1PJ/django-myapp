import os
from django.conf import settings
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px
import json
from django.shortcuts import render
from .models import Recruit
from datetime import datetime, timedelta
from django.shortcuts import render
from .recruit_data_visualization.region_converter import convert_region
from .recruit_data_visualization.data_processing import get_job_data
from .recruit_data_visualization.graph_generation import create_line_and_pie_charts, create_choropleth

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

def job_graph(request):
    # 데이터 처리
    df, df_filtered = get_job_data()

    # 그래프 생성
    line_plot_html = create_line_and_pie_charts(df)
    choropleth_html = create_choropleth(df_filtered)

    # 컨텍스트 설정
    context = {
        'line_plot_html': line_plot_html,
        'choropleth_html': choropleth_html
    }

    # 템플릿 렌더링
    return render(request, 'job_graph.html', context)