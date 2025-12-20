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
    
    .divider {
        height: 3px;
        background: linear-gradient(90deg, #E91E63 0%, #9C27B0 100%);
        border: none;
        margin: 2rem 0;
        border-radius: 2px;
    }
    
    .footer {
        text-align: center;
        color: #888;
        padding: 2rem;
        margin-top: 3rem;
    }
    
    .insight-box {
        background: linear-gradient(135deg, #E91E63 0%, #9C27B0 100%);
        color: white;
        padding: 1rem 1.5rem;
        border-radius: 10px;
        margin: 1rem 0;
    }
    
    .update-info {
        text-align: center;
        color: #888;
        font-size: 0.9rem;
        margin-bottom: 1rem;
    }
</style>
""", unsafe_allow_html=True)

# ============================================================
# 데이터 로드 (CSV 파일에서)
# ============================================================
@st.cache_data
def load_data():
    try:
        df = pd.read_csv('channels_data.csv')
        return df
    except:
        st.error("⚠️ channels_data.csv 파일을 찾을 수 없습니다.")
        return pd.DataFrame()

df = load_data()

if df.empty:
    st.stop()

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
    
    # 수집 일시 표시
    if 'collected_at' in df.columns:
        last_update = df['collected_at'].iloc[0]
        st.markdown(f"**최종 업데이트:** {last_update}")
    
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

if df_filtered.empty:
    st.warning("선택된 필터에 해당하는 데이터가 없습니다.")
    st.stop()

# ============================================================
# 메인 콘텐츠
# ============================================================

# 헤더
st.markdown('<h1 class="main-header">KFANTRIX</h1>', unsafe_allow_html=True)
st.markdown('<p class="sub-header">K-pop 팬덤 데이터로 글로벌 마케팅 성공률을 높이다</p>', unsafe_allow_html=True)

# 수집 일시 표시
if 'collected_at' in df.columns:
    st.markdown(f'<p class="update-info">📅 데이터 수집: {df["collected_at"].iloc[0]}</p>', unsafe_allow_html=True)

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
        value=f"{len(df_filtered)}개"
    )

with col2:
    avg_subs = df_filtered['subscribers'].mean() / 1000000
    st.metric(
        label="평균 구독자",
        value=f"{avg_subs:.1f}M"
    )

with col3:
    avg_views = df_filtered['avg_views'].mean() / 1000000
    st.metric(
        label="평균 조회수",
        value=f"{avg_views:.2f}M"
    )

with col4:
    avg_eng = df_filtered['engagement_rate'].mean()
    st.metric(
        label="평균 참여도",
        value=f"{avg_eng:.2f}%"
    )

with col5:
    avg_fan = df_filtered['fandom_activity'].mean()
    st.metric(
        label="팬덤 활성도",
        value=f"{avg_fan:.1f}%"
    )

st.markdown("")

# ============================================================
# 아티스트 비교 차트
# ============================================================
st.markdown("## 📈 아티스트 비교 분석")

tab1, tab2, tab3 = st.tabs(["📊 기본 지표", "🎯 참여도 분석", "🌐 종합 스코어"])

# 색상 팔레트
colors = px.colors.qualitative.Set2

with tab1:
    col_left, col_right = st.columns(2)
    
    with col_left:
        # 구독자 수 비교
        fig1 = px.bar(
            df_filtered.sort_values('subscribers', ascending=True),
            x='subscribers',
            y='artist',
            orientation='h',
            color='artist',
            color_discrete_sequence=colors,
            title='구독자 수 비교'
        )
        fig1.update_layout(
            showlegend=False,
            xaxis_title='구독자 수',
            yaxis_title='',
            plot_bgcolor='rgba(0,0,0,0)',
            paper_bgcolor='rgba(0,0,0,0)'
        )
        st.plotly_chart(fig1, use_container_width=True)
    
    with col_right:
        # 평균 조회수 비교
        fig2 = px.bar(
            df_filtered.sort_values('avg_views', ascending=True),
            x='avg_views',
            y='artist',
            orientation='h',
            color='artist',
            color_discrete_sequence=colors,
            title='영상당 평균 조회수'
        )
        fig2.update_layout(
            showlegend=False,
            xaxis_title='평균 조회수',
            yaxis_title='',
            plot_bgcolor='rgba(0,0,0,0)',
            paper_bgcolor='rgba(0,0,0,0)'
        )
        st.plotly_chart(fig2, use_container_width=True)

with tab2:
    col_left2, col_right2 = st.columns(2)
    
    with col_left2:
        # 참여도 비교
        fig3 = px.bar(
            df_filtered.sort_values('engagement_rate', ascending=True),
            x='engagement_rate',
            y='artist',
            orientation='h',
            color='artist',
            color_discrete_sequence=colors,
            title='참여도 (좋아요+댓글/조회수)'
        )
        fig3.update_layout(
            showlegend=False,
            xaxis_title='참여도 (%)',
            yaxis_title='',
            plot_bgcolor='rgba(0,0,0,0)',
            paper_bgcolor='rgba(0,0,0,0)'
        )
        st.plotly_chart(fig3, use_container_width=True)
    
    with col_right2:
        # 팬덤 활성도 비교
        fig4 = px.bar(
            df_filtered.sort_values('fandom_activity', ascending=True),
            x='fandom_activity',
            y='artist',
            orientation='h',
            color='artist',
            color_discrete_sequence=colors,
            title='팬덤 활성도 (평균조회수/구독자)'
        )
        fig4.update_layout(
            showlegend=False,
            xaxis_title='활성도 (%)',
            yaxis_title='',
            plot_bgcolor='rgba(0,0,0,0)',
            paper_bgcolor='rgba(0,0,0,0)'
        )
        st.plotly_chart(fig4, use_container_width=True)

with tab3:
    col_radar, col_insight = st.columns([2, 1])
    
    with col_radar:
        # 레이더 차트
        categories = ['구독자', '평균조회수', '참여도', '팬덤활성도']
        
        fig5 = go.Figure()
        
        for idx, row in df_filtered.iterrows():
            values = [
                row['subscribers'] / df['subscribers'].max(),
                row['avg_views'] / df['avg_views'].max(),
                row['engagement_rate'] / df['engagement_rate'].max(),
                row['fandom_activity'] / df['fandom_activity'].max()
            ]
            values.append(values[0])
            
            fig5.add_trace(go.Scatterpolar(
                r=values,
                theta=categories + [categories[0]],
                fill='toself',
                name=row['artist'],
                opacity=0.7
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
                y=-0.3,
                xanchor="center",
                x=0.5
            )
        )
        st.plotly_chart(fig5, use_container_width=True)
    
    with col_insight:
        st.markdown("### 💡 인사이트")
        
        # 참여도 TOP 3
        top_engagement = df_filtered.nlargest(3, 'engagement_rate')
        st.markdown("**🔥 참여도 TOP 3**")
        for _, row in top_engagement.iterrows():
            st.markdown(f"- {row['artist']}: {row['engagement_rate']}%")
        
        st.markdown("")
        
        # 구독자 TOP 3
        top_subs = df_filtered.nlargest(3, 'subscribers')
        st.markdown("**👑 구독자 TOP 3**")
        for _, row in top_subs.iterrows():
            st.markdown(f"- {row['artist']}: {row['subscribers']:,}")
        
        st.markdown("")
        
        # 팬덤 활성도 TOP 3
        top_fandom = df_filtered.nlargest(3, 'fandom_activity')
        st.markdown("**💜 팬덤 활성도 TOP 3**")
        for _, row in top_fandom.iterrows():
            st.markdown(f"- {row['artist']}: {row['fandom_activity']}%")

# ============================================================
# 카테고리별 분석
# ============================================================
st.markdown('<hr class="divider">', unsafe_allow_html=True)
st.markdown("## 📂 카테고리별 분석")

col_cat1, col_cat2 = st.columns(2)

with col_cat1:
    # 카테고리별 평균 구독자
    cat_subs = df_filtered.groupby('category')['subscribers'].mean().reset_index()
    fig_cat1 = px.pie(
        cat_subs,
        values='subscribers',
        names='category',
        title='카테고리별 평균 구독자 비중',
        color_discrete_sequence=colors
    )
    st.plotly_chart(fig_cat1, use_container_width=True)

with col_cat2:
    # 카테고리별 평균 참여도
    cat_eng = df_filtered.groupby('category')['engagement_rate'].mean().reset_index()
    fig_cat2 = px.bar(
        cat_eng.sort_values('engagement_rate', ascending=True),
        x='engagement_rate',
        y='category',
        orientation='h',
        title='카테고리별 평균 참여도',
        color='category',
        color_discrete_sequence=colors
    )
    fig_cat2.update_layout(showlegend=False)
    st.plotly_chart(fig_cat2, use_container_width=True)

# ============================================================
# 상세 데이터 테이블
# ============================================================
st.markdown('<hr class="divider">', unsafe_allow_html=True)
st.markdown("## 📋 상세 데이터")

# 데이터 포맷팅
df_display = df_filtered[['artist', 'category', 'subscribers', 'avg_views', 'avg_likes', 
                          'avg_comments', 'engagement_rate', 'fandom_activity', 'recent_videos_30d']].copy()
df_display['subscribers'] = df_display['subscribers'].apply(lambda x: f"{x:,}")
df_display['avg_views'] = df_display['avg_views'].apply(lambda x: f"{x:,}")
df_display['avg_likes'] = df_display['avg_likes'].apply(lambda x: f"{x:,}")
df_display['avg_comments'] = df_display['avg_comments'].apply(lambda x: f"{x:,}")
df_display['engagement_rate'] = df_display['engagement_rate'].apply(lambda x: f"{x:.2f}%")
df_display['fandom_activity'] = df_display['fandom_activity'].apply(lambda x: f"{x:.2f}%")

# 컬럼명 한글화
df_display.columns = ['아티스트', '카테고리', '구독자', '평균 조회수', '평균 좋아요', 
                      '평균 댓글', '참여도', '팬덤 활성도', '최근 30일 영상']

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
    <p>📧 contact@kfantrix.com</p>
</div>
""", unsafe_allow_html=True)
