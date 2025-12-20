# KFANTRIX - K-pop Channel Analytics Dashboard
# 실행: streamlit run kfantrix_app.py

import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime

# ============================================================
# 페이지 설정
# ============================================================
st.set_page_config(
    page_title="KFANTRIX - K-pop Channel Analytics",
    page_icon="🎵",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ============================================================
# 커스텀 CSS
# ============================================================
st.markdown("""
<style>
    /* 메인 헤더 */
    .main-header {
        font-size: 3rem;
        font-weight: bold;
        background: linear-gradient(135deg, #E91E63 0%, #9C27B0 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        text-align: center;
        margin-bottom: 0.5rem;
    }
    
    .sub-header {
        text-align: center;
        color: #666;
        font-size: 1.1rem;
        margin-bottom: 2rem;
    }
    
    /* 메트릭 카드 스타일 */
    .metric-container {
        background: linear-gradient(135deg, #1A1A2E 0%, #16213E 100%);
        padding: 1.5rem;
        border-radius: 15px;
        text-align: center;
        box-shadow: 0 4px 15px rgba(0,0,0,0.2);
    }
    
    .metric-value {
        font-size: 2rem;
        font-weight: bold;
        color: #E91E63;
    }
    
    .metric-label {
        font-size: 0.9rem;
        color: #aaa;
        margin-top: 0.5rem;
    }
    
    /* 카드 스타일 */
    .artist-card {
        background: white;
        padding: 1.5rem;
        border-radius: 15px;
        box-shadow: 0 2px 10px rgba(0,0,0,0.1);
        margin-bottom: 1rem;
    }
    
    /* 사이드바 스타일 */
    .css-1d391kg {
        background: linear-gradient(180deg, #1A1A2E 0%, #16213E 100%);
    }
    
    /* 구분선 */
    .divider {
        height: 3px;
        background: linear-gradient(90deg, #E91E63 0%, #9C27B0 100%);
        border: none;
        margin: 2rem 0;
        border-radius: 2px;
    }
    
    /* 푸터 */
    .footer {
        text-align: center;
        color: #888;
        padding: 2rem;
        margin-top: 3rem;
    }
    
    /* 인사이트 박스 */
    .insight-box {
        background: linear-gradient(135deg, #E91E63 0%, #9C27B0 100%);
        color: white;
        padding: 1rem 1.5rem;
        border-radius: 10px;
        margin: 1rem 0;
    }
</style>
""", unsafe_allow_html=True)

# ============================================================
# 데이터 (실제 분석 결과)
# ============================================================
@st.cache_data
def load_data():
    data = {
        'artist': ['NMIXX', 'PLAVE'],
        'subscribers': [3810000, 1120000],
        'total_views': [1774700038, 670533871],
        'video_count': [1536, 1401],
        'avg_views': [632147, 200592],
        'avg_likes': [18500, 16800],
        'avg_comments': [980, 3200],
        'engagement_rate': [3.56, 9.98],
        'views_per_subscriber': [16.6, 17.9],
        'created_at': ['2021-07-12', '2022-06-16'],
        'category': ['4세대 걸그룹', '버추얼 아이돌'],
        'company': ['JYP Entertainment', 'VLAST']
    }
    return pd.DataFrame(data)

df = load_data()

# ============================================================
# 사이드바
# ============================================================
with st.sidebar:
    st.markdown("## 🎵 KFANTRIX")
    st.markdown("K-pop 채널 분석 플랫폼")
    st.divider()
    
    # 아티스트 필터
    st.markdown("### 🔍 필터")
    selected_artists = st.multiselect(
        "아티스트 선택",
        df['artist'].tolist(),
        default=df['artist'].tolist()
    )
    
    # 카테고리 필터
    selected_category = st.multiselect(
        "카테고리",
        df['category'].unique().tolist(),
        default=df['category'].unique().tolist()
    )
    
    st.divider()
    
    # 정보
    st.markdown("### 📊 데이터 정보")
    st.markdown(f"**분석 아티스트:** {len(df)}개")
    st.markdown(f"**최종 업데이트:** {datetime.now().strftime('%Y-%m-%d')}")
    
    st.divider()
    st.markdown("### 💡 서비스 안내")
    st.markdown("""
    - **Free**: 기본 지표 열람
    - **Pro**: 상세 분석 + 비교
    - **Enterprise**: API + 맞춤 리포트
    """)

# 필터 적용
df_filtered = df[
    (df['artist'].isin(selected_artists)) & 
    (df['category'].isin(selected_category))
]

# ============================================================
# 메인 콘텐츠
# ============================================================

# 헤더
st.markdown('<h1 class="main-header">KFANTRIX</h1>', unsafe_allow_html=True)
st.markdown('<p class="sub-header">K-pop 팬덤 데이터로 글로벌 마케팅 성공률을 높이다</p>', unsafe_allow_html=True)

# 구분선
st.markdown('<hr class="divider">', unsafe_allow_html=True)

# ============================================================
# 핵심 메트릭 카드
# ============================================================
st.markdown("## 📊 핵심 지표 요약")

col1, col2, col3, col4, col5 = st.columns(5)

with col1:
    st.metric(
        label="분석 아티스트",
        value=f"{len(df_filtered)}개",
        delta=None
    )

with col2:
    avg_subs = df_filtered['subscribers'].mean() / 1000000
    st.metric(
        label="평균 구독자",
        value=f"{avg_subs:.1f}M",
        delta=f"{((df_filtered['subscribers'].iloc[0] - df_filtered['subscribers'].iloc[-1]) / df_filtered['subscribers'].iloc[-1] * 100):.0f}% 차이" if len(df_filtered) > 1 else None
    )

with col3:
    avg_views = df_filtered['avg_views'].mean() / 1000000
    st.metric(
        label="평균 조회수",
        value=f"{avg_views:.2f}M",
        delta=None
    )

with col4:
    avg_eng = df_filtered['engagement_rate'].mean()
    st.metric(
        label="평균 참여도",
        value=f"{avg_eng:.2f}%",
        delta=None
    )

with col5:
    avg_fan = df_filtered['views_per_subscriber'].mean()
    st.metric(
        label="팬덤 활성도",
        value=f"{avg_fan:.1f}%",
        delta=None
    )

st.markdown("")

# ============================================================
# 아티스트 비교 차트
# ============================================================
st.markdown("## 📈 아티스트 비교 분석")

tab1, tab2, tab3 = st.tabs(["📊 기본 지표", "🎯 참여도 분석", "🌐 종합 스코어"])

with tab1:
    col_left, col_right = st.columns(2)
    
    with col_left:
        # 구독자 수 비교
        fig1 = px.bar(
            df_filtered,
            x='artist',
            y='subscribers',
            color='artist',
            color_discrete_sequence=['#E91E63', '#9C27B0'],
            title='구독자 수 비교'
        )
        fig1.update_layout(
            showlegend=False,
            yaxis_title='구독자 수',
            xaxis_title='',
            plot_bgcolor='rgba(0,0,0,0)',
            paper_bgcolor='rgba(0,0,0,0)'
        )
        fig1.update_traces(
            texttemplate='%{y:,.0f}',
            textposition='outside'
        )
        st.plotly_chart(fig1, use_container_width=True)
    
    with col_right:
        # 평균 조회수 비교
        fig2 = px.bar(
            df_filtered,
            x='artist',
            y='avg_views',
            color='artist',
            color_discrete_sequence=['#E91E63', '#9C27B0'],
            title='영상당 평균 조회수'
        )
        fig2.update_layout(
            showlegend=False,
            yaxis_title='평균 조회수',
            xaxis_title='',
            plot_bgcolor='rgba(0,0,0,0)',
            paper_bgcolor='rgba(0,0,0,0)'
        )
        fig2.update_traces(
            texttemplate='%{y:,.0f}',
            textposition='outside'
        )
        st.plotly_chart(fig2, use_container_width=True)

with tab2:
    col_left2, col_right2 = st.columns(2)
    
    with col_left2:
        # 참여도 비교
        fig3 = px.bar(
            df_filtered,
            x='artist',
            y='engagement_rate',
            color='artist',
            color_discrete_sequence=['#E91E63', '#9C27B0'],
            title='참여도 (좋아요+댓글/조회수)'
        )
        fig3.update_layout(
            showlegend=False,
            yaxis_title='참여도 (%)',
            xaxis_title='',
            plot_bgcolor='rgba(0,0,0,0)',
            paper_bgcolor='rgba(0,0,0,0)'
        )
        fig3.update_traces(
            texttemplate='%{y:.2f}%',
            textposition='outside'
        )
        st.plotly_chart(fig3, use_container_width=True)
    
    with col_right2:
        # 팬덤 활성도 비교
        fig4 = px.bar(
            df_filtered,
            x='artist',
            y='views_per_subscriber',
            color='artist',
            color_discrete_sequence=['#E91E63', '#9C27B0'],
            title='팬덤 활성도 (평균조회수/구독자)'
        )
        fig4.update_layout(
            showlegend=False,
            yaxis_title='활성도 (%)',
            xaxis_title='',
            plot_bgcolor='rgba(0,0,0,0)',
            paper_bgcolor='rgba(0,0,0,0)'
        )
        fig4.update_traces(
            texttemplate='%{y:.1f}%',
            textposition='outside'
        )
        st.plotly_chart(fig4, use_container_width=True)

with tab3:
    col_radar, col_insight = st.columns([2, 1])
    
    with col_radar:
        # 레이더 차트
        categories = ['구독자', '평균조회수', '참여도', '팬덤활성도']
        
        fig5 = go.Figure()
        
        colors = ['#E91E63', '#9C27B0']
        for idx, row in df_filtered.iterrows():
            # 정규화
            values = [
                row['subscribers'] / df['subscribers'].max(),
                row['avg_views'] / df['avg_views'].max(),
                row['engagement_rate'] / df['engagement_rate'].max(),
                row['views_per_subscriber'] / df['views_per_subscriber'].max()
            ]
            values.append(values[0])  # 닫기
            
            fig5.add_trace(go.Scatterpolar(
                r=values,
                theta=categories + [categories[0]],
                fill='toself',
                name=row['artist'],
                line_color=colors[idx % 2],
                fillcolor=f"rgba{tuple(list(int(colors[idx % 2].lstrip('#')[i:i+2], 16) for i in (0, 2, 4)) + [0.3])}"
            ))
        
        fig5.update_layout(
            polar=dict(
                radialaxis=dict(
                    visible=True,
                    range=[0, 1],
                    tickfont=dict(size=10)
                ),
                angularaxis=dict(
                    tickfont=dict(size=12)
                )
            ),
            showlegend=True,
            title='종합 스코어 비교',
            legend=dict(
                orientation="h",
                yanchor="bottom",
                y=-0.2,
                xanchor="center",
                x=0.5
            )
        )
        st.plotly_chart(fig5, use_container_width=True)
    
    with col_insight:
        st.markdown("### 💡 인사이트")
        
        if len(df_filtered) >= 2:
            nmixx = df_filtered[df_filtered['artist'] == 'NMIXX']
            plave = df_filtered[df_filtered['artist'] == 'PLAVE']
            
            if not nmixx.empty and not plave.empty:
                st.markdown("""
                <div class="insight-box">
                <strong>NMIXX</strong><br>
                • 대형 기획사 안정적 팬덤<br>
                • 높은 구독자 & 조회수<br>
                • 글로벌 확장 진행 중
                </div>
                """, unsafe_allow_html=True)
                
                st.markdown("""
                <div class="insight-box">
                <strong>PLAVE</strong><br>
                • 버추얼 아이돌 급성장<br>
                • 참여도 9.98% (매우 높음)<br>
                • MZ세대 타겟 강점
                </div>
                """, unsafe_allow_html=True)
                
                st.info("💡 **브랜드 협업 추천**: PLAVE는 높은 참여도로 팬 반응형 캠페인에, NMIXX는 대중성 있는 광고에 적합")

# ============================================================
# 상세 데이터 테이블
# ============================================================
st.markdown("## 📋 상세 데이터")

# 데이터 포맷팅
df_display = df_filtered.copy()
df_display['subscribers'] = df_display['subscribers'].apply(lambda x: f"{x:,}")
df_display['total_views'] = df_display['total_views'].apply(lambda x: f"{x:,}")
df_display['avg_views'] = df_display['avg_views'].apply(lambda x: f"{x:,.0f}")
df_display['engagement_rate'] = df_display['engagement_rate'].apply(lambda x: f"{x:.2f}%")
df_display['views_per_subscriber'] = df_display['views_per_subscriber'].apply(lambda x: f"{x:.1f}%")

# 컬럼명 한글화
df_display.columns = ['아티스트', '구독자', '총 조회수', '영상 수', '평균 조회수', 
                      '평균 좋아요', '평균 댓글', '참여도', '팬덤 활성도', 
                      '채널 생성일', '카테고리', '소속사']

st.dataframe(df_display, use_container_width=True, hide_index=True)

# 다운로드 버튼
csv = df_filtered.to_csv(index=False, encoding='utf-8-sig')
st.download_button(
    label="📥 CSV 다운로드",
    data=csv,
    file_name=f"kfantrix_data_{datetime.now().strftime('%Y%m%d')}.csv",
    mime="text/csv"
)

# ============================================================
# 서비스 안내 섹션
# ============================================================
st.markdown('<hr class="divider">', unsafe_allow_html=True)
st.markdown("## 🚀 KFANTRIX 서비스")

col_s1, col_s2, col_s3 = st.columns(3)

with col_s1:
    st.markdown("""
    ### 📊 Basic (무료)
    - 기본 채널 지표 열람
    - 아티스트 랭킹
    - 월간 업데이트
    
    **₩0 / 월**
    """)

with col_s2:
    st.markdown("""
    ### 🎯 Pro (추천)
    - 상세 참여도 분석
    - 아티스트 비교 분석
    - 주간 업데이트
    - CSV 다운로드
    
    **₩290,000 / 월**
    """)

with col_s3:
    st.markdown("""
    ### 🏢 Enterprise
    - 국가별 팬덤 분석
    - AI 감성 분석
    - API 접근
    - 맞춤 리포트
    
    **별도 문의**
    """)

# ============================================================
# 푸터
# ============================================================
st.markdown('<hr class="divider">', unsafe_allow_html=True)
st.markdown("""
<div class="footer">
    <p><strong>KFANTRIX</strong> - K-pop 팬덤 데이터로 글로벌 마케팅 성공률을 높이다</p>
    <p>© 2025 KFANTRIX. All rights reserved.</p>
    <p>📧 contact@kfantrix.com | 🌐 www.kfantrix.com</p>
</div>
""", unsafe_allow_html=True)
