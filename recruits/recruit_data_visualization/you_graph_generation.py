import pandas as pd
from datetime import datetime
from wordcloud import WordCloud
import io
import base64
import matplotlib.pyplot as plt
import matplotlib
import matplotlib.colors as mcolors
matplotlib.use('Agg')  # GUI 창을 띄우지 않도록 설정
from .you_data_processing import make_df
from django.conf import settings
import json
import os
# 운영 체제에 맞는 폰트 설정 (Mac, Windows, Linux)
import platform
current_os = platform.system()  # 다른 변수명 사용
if current_os == 'Windows': # 여기가 핵심 os 변수명에서 current_os 로 변경
    plt.rc('font', family='Malgun Gothic')
elif current_os == 'Darwin':
    plt.rc('font', family='AppleGothic')
elif current_os == 'Linux':
    plt.rc('font', family='NanumGothic')
else:
    print(f'{current_os} is not set')
def generate_wordcloud():
    df = make_df()
    # 제외하고 싶은 단어 리스트
    remove_words = ['기술 스택 없음', '기술스택', '외']
    # stack이 리스트로 되어 있는 경우
    df_drop_category = df.groupby('category_name')['stack'].apply(
        lambda x: ' '.join([' '.join([item.strip() for item in stack_list if item and item.strip() not in remove_words])
                            for stack_list in x if isinstance(stack_list, list)])
    )
    font_path = os.path.join(settings.BASE_DIR, 'recruits/static/assets/NanumGothic.ttf')
    # 워드클라우드 생성 및 이미지로 변환
    wordcloud_images = {}
    for category, stack_words in df_drop_category.items():
        wordcloud = WordCloud(width=800, height=400, background_color='white', font_path=font_path).generate(stack_words)
        buffer = io.BytesIO()
        plt.figure(figsize=(6, 3))
        plt.imshow(wordcloud, interpolation='bilinear')
        plt.axis('off')
        plt.savefig(buffer, format='png')
        buffer.seek(0)
        image_png = buffer.getvalue()
        buffer.close()
        graph = base64.b64encode(image_png).decode('utf-8')
        wordcloud_images[category] = graph
    return wordcloud_images
# 신입/경력 공고 수 비율 그래프 생성
# def generate_bar_graph():
#     df = make_df()
#     career_count = df['career'].value_counts()
#     # 각 막대의 색상을 지정된 색상 코드로 설정
#     hex_colors = ['#87A2FF', '#A7BBFF', '#C7D3FF', '#E7ECFF']
#     buffer = io.BytesIO()
#     plt.figure(figsize=(7, 4))
#     # 막대 그래프 생성
#     bars = plt.bar(career_count.index, career_count.values, color=hex_colors)
#     # 타이틀 및 레이아웃 설정
#     plt.title('신입/경력 공고 수 비율')
#     plt.tight_layout()
#     # 그래프를 메모리 버퍼에 저장
#     plt.savefig(buffer, format='png')
#     buffer.seek(0)
#     image_png = buffer.getvalue()
#     buffer.close()
#     # 이미지를 base64로 인코딩
#     graph = base64.b64encode(image_png).decode('utf-8')
#     return graph

def generate_bar_graph():
    df = make_df()
    career_count = df['career'].value_counts()

    # 각 막대의 색상을 지정된 색상 코드로 설정
    hex_colors = ['#4A90E2', '#50E3C2', '#F5A623', '#D0021B']  # 바 그래프 색상 코드
    buffer = io.BytesIO()
    
    # 그래프 크기와 막대 너비 조정
    plt.figure(figsize=(7, 5))  # 너비와 높이 조정 (더 컴팩트하게)
    bars = plt.bar(career_count.index, career_count.values, color=hex_colors, width=0.35)  # 막대 너비 조정
    
    # 테마에 맞춰 그래프 스타일 설정 
    plt.xticks(fontsize=8, weight='bold', color='#333333')  # x축 라벨 크기와 굵기
    plt.yticks(fontsize=10, color='#333333')  # y축 라벨 크기
    plt.grid(axis='y', linestyle='--', alpha=0.4, color='#DDDDDD')  # y축 격자선 (선 스타일 조정)
    plt.tight_layout()  # 레이아웃 조정

    # 그래프를 메모리 버퍼에 저장
    plt.savefig(buffer, format='png', transparent=True)  # 투명 배경
    buffer.seek(0)
    image_png = buffer.getvalue()
    buffer.close()

    # 이미지를 base64로 인코딩
    graph = base64.b64encode(image_png).decode('utf-8')
    
    return graph