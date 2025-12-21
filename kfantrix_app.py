# kfantrix_app.py - KFANTRIX 통합 대시보드
# 채널 기본 지표 + 3개 그룹 심층 분석

import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime

# ============================================================
# 페이지 설정
# ============================================================
st.set_page_config(
    page_title="KFANTRIX - K-pop Analytics",
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
        font-size: 2.8rem;
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
    .insight-box {
        background: linear-gradient(135deg, #E91E63 0%, #9C27B0 100%);
        color: white;
        padding: 1.2rem 1.5rem;
        border-radius: 12px;
        margin: 1rem 0;
    }
    .insight-box-blue {
        background: linear-gradient(135deg, #3B82F6 0%, #8B5CF6 100%);
        color: white;
        padding: 1.2rem 1.5rem;
        border-radius: 12px;
        margin: 1rem 0;
    }
    .group-card {
        background: #f8f9fa;
        padding: 1rem;
        border-radius: 10px;
        border-left: 4px solid #E91E63;
        margin: 0.5rem 0;
    }
    .footer {
        text-align: center;
        color: #888;
        padding: 2rem;
        margin-top: 3rem;
    }
</style>
""", unsafe_allow_html=True)

# ============================================================
# 데이터 로드
# ============================================================
@st.cache_data
def load_channel_data():
    """채널 기본 지표 로드"""
    try:
        return pd.read_csv('channels_data.csv')
    except:
        return None

@st.cache_data
def load_deep_analysis(prefix):
    """심층 분석 데이터 로드"""
    data = {}
    files = {
        'summary': f'{prefix}_summary.csv',
        'language': f'{prefix}_language_stats.csv',
        'member': f'{prefix}_member_stats.csv',
        'region_member': f'{prefix}_region_member.csv',
        'cooccurrence': f'{prefix}_member_cooccurrence.csv',
        'member_keywords': f'{prefix}_member_keywords.csv',
        'region_keywords': f'{prefix}_region_keywords.csv',
        'member_region_keywords': f'{prefix}_member_region_keywords.csv',
        'loyal_fans': f'{prefix}_loyal_fans.csv',
        'video_engagement': f'{prefix}_video_engagement.csv'
    }
    for key, filename in files.items():
        try:
            data[key] = pd.read_csv(filename)
        except:
            data[key] = None
    return data

# 그룹별 데이터 로드
GROUPS = {
    'PLAVE': {'prefix': 'plave', 'color': '#8B5CF6', 'emoji': '💜'},
    'NMIXX': {'prefix': 'nmixx', 'color': '#EC4899', 'emoji': '💗'},
    'skz': {'prefix': 'skz', 'color': '#F59E0B', 'emoji': '🖤'}
}

channel_data = load_channel_data()
deep_data = {name: load_deep_analysis(info['prefix']) for name, info in GROUPS.items()}

# ============================================================
# 사이드바
# ============================================================
with st.sidebar:
    st.markdown("## 🎵 KFANTRIX")
    st.markdown("K-pop 팬덤 분석 플랫폼")
    st.divider()
    
    # 분석 유형 선택
    st.markdown("### 📊 분석 유형")
    analysis_mode = st.radio(
        "분석 모드 선택",
        ["📈 채널 기본 지표", "🔬 심층 댓글 분석", "⚖️ 그룹 비교"],
        label_visibility="collapsed"
    )
    
    st.divider()
    
    # 심층 분석일 때 그룹 선택
    if analysis_mode == "🔬 심층 댓글 분석":
        st.markdown("### 🎤 그룹 선택")
        selected_group = st.selectbox(
            "분석할 그룹",
            list(GROUPS.keys()),
            label_visibility="collapsed"
        )
        
        st.divider()
        
        st.markdown("### 📑 분석 메뉴")
        deep_menu = st.radio(
            "상세 분석",
            ["📊 전체 요약", "💑 멤버 케미", "🏷️ 키워드 분석", "💜 진성팬 분석", "🎯 마케팅 인사이트"],
            label_visibility="collapsed"
        )
    
    st.divider()
    st.markdown("### 💡 서비스 안내")
    st.markdown("""
    - **Basic**: 기본 지표
    - **Pro**: 심층 분석
    - **Enterprise**: API + 리포트
    """)

# ============================================================
# 헤더
# ============================================================
st.markdown('<h1 class="main-header">KFANTRIX</h1>', unsafe_allow_html=True)
st.markdown('<p class="sub-header">K-pop 팬덤 데이터로 글로벌 마케팅 성공률을 높이다</p>', unsafe_allow_html=True)
st.markdown('<hr class="divider">', unsafe_allow_html=True)

# ============================================================
# 📈 채널 기본 지표
# ============================================================
if analysis_mode == "📈 채널 기본 지표":
    st.markdown("## 📈 채널 기본 지표")
    
    if channel_data is None:
        st.warning("⚠️ channels_data.csv 파일을 찾을 수 없습니다.")
        st.stop()
    
    df = channel_data
    
    # 핵심 메트릭
    col1, col2, col3, col4, col5 = st.columns(5)
    with col1:
        st.metric("분석 채널", f"{len(df)}개")
    with col2:
        st.metric("평균 구독자", f"{df['subscribers'].mean()/1000000:.1f}M")
    with col3:
        st.metric("평균 조회수", f"{df['avg_views'].mean()/1000000:.2f}M")
    with col4:
        st.metric("평균 참여도", f"{df['engagement_rate'].mean():.2f}%")
    with col5:
        st.metric("팬덤 활성도", f"{df['fandom_activity'].mean():.1f}%")
    
    st.markdown("")
    
    # 차트
    col_left, col_right = st.columns(2)
    
    with col_left:
        fig1 = px.bar(
            df.sort_values('subscribers', ascending=True),
            x='subscribers', y='artist', orientation='h',
            color='artist', color_discrete_sequence=px.colors.qualitative.Set2,
            title='구독자 수 비교'
        )
        fig1.update_layout(showlegend=False, xaxis_title='구독자', yaxis_title='')
        st.plotly_chart(fig1, use_container_width=True)
    
    with col_right:
        fig2 = px.bar(
            df.sort_values('engagement_rate', ascending=True),
            x='engagement_rate', y='artist', orientation='h',
            color='artist', color_discrete_sequence=px.colors.qualitative.Set2,
            title='참여도 비교'
        )
        fig2.update_layout(showlegend=False, xaxis_title='참여도 (%)', yaxis_title='')
        st.plotly_chart(fig2, use_container_width=True)
    
    # 레이더 차트
    st.markdown("### 🎯 종합 스코어")
    categories = ['구독자', '평균조회수', '참여도', '팬덤활성도']
    
    fig_radar = go.Figure()
    for _, row in df.iterrows():
        values = [
            row['subscribers'] / df['subscribers'].max(),
            row['avg_views'] / df['avg_views'].max(),
            row['engagement_rate'] / df['engagement_rate'].max(),
            row['fandom_activity'] / df['fandom_activity'].max()
        ]
        values.append(values[0])
        fig_radar.add_trace(go.Scatterpolar(
            r=values, theta=categories + [categories[0]],
            fill='toself', name=row['artist'], opacity=0.7
        ))
    fig_radar.update_layout(
        polar=dict(radialaxis=dict(visible=True, range=[0, 1])),
        showlegend=True,
        legend=dict(orientation="h", yanchor="bottom", y=-0.3, xanchor="center", x=0.5)
    )
    st.plotly_chart(fig_radar, use_container_width=True)
    
    # 데이터 테이블
    st.markdown("### 📋 상세 데이터")
    st.dataframe(df, use_container_width=True, hide_index=True)

# ============================================================
# 🔬 심층 댓글 분석
# ============================================================
elif analysis_mode == "🔬 심층 댓글 분석":
    group_info = GROUPS[selected_group]
    data = deep_data[selected_group]
    
    st.markdown(f"## {group_info['emoji']} {selected_group} 심층 분석")
    
    if data['summary'] is None:
        st.warning(f"⚠️ {selected_group} 데이터를 찾을 수 없습니다. {group_info['prefix']}_*.csv 파일을 업로드해주세요.")
        st.stop()
    
    summary = data['summary'].iloc[0]
    
    # -------------------- 📊 전체 요약 --------------------
    if deep_menu == "📊 전체 요약":
        col1, col2, col3, col4, col5 = st.columns(5)
        with col1:
            st.metric("총 댓글", f"{summary['total_comments']:,}개")
        with col2:
            st.metric("분석 영상", f"{summary['total_videos']}개")
        with col3:
            st.metric("고유 작성자", f"{summary['unique_authors']:,}명")
        with col4:
            st.metric("진성팬 비율", f"{summary['loyal_fan_rate']}%")
        with col5:
            st.metric("슈퍼팬 비율", f"{summary['super_fan_rate']}%")
        
        col_left, col_right = st.columns(2)
        
        with col_left:
            st.markdown("### 🌐 언어 분포")
            if data['language'] is not None:
                fig = px.pie(data['language'].head(8), values='percentage', names='region',
                           color_discrete_sequence=px.colors.sequential.Purples_r, hole=0.4)
                st.plotly_chart(fig, use_container_width=True)
        
        with col_right:
            st.markdown("### 👥 멤버 언급 비율")
            if data['member'] is not None:
                df_mem = data['member'].sort_values('mention_count', ascending=True)
                fig = px.bar(df_mem, x='mention_count', y='member', orientation='h',
                           color='mention_rate', color_continuous_scale='Purples', text='mention_rate')
                fig.update_traces(texttemplate='%{text:.1f}%', textposition='outside')
                fig.update_layout(coloraxis_showscale=False)
                st.plotly_chart(fig, use_container_width=True)
        
        # 케미 TOP 3
        if data['cooccurrence'] is not None and len(data['cooccurrence']) > 0:
            st.markdown("### 💑 인기 케미 TOP 3")
            cols = st.columns(3)
            for idx, (col, (_, row)) in enumerate(zip(cols, data['cooccurrence'].head(3).iterrows())):
                with col:
                    st.metric(f"#{idx+1} {row['pair']}", f"{row['count']}회")
    
    # -------------------- 💑 멤버 케미 --------------------
    elif deep_menu == "💑 멤버 케미":
        st.markdown("### 💑 멤버 동시 언급 분석")
        
        if data['cooccurrence'] is not None and len(data['cooccurrence']) > 0:
            col_left, col_right = st.columns(2)
            
            with col_left:
                fig = px.bar(data['cooccurrence'].head(10), x='pair', y='count',
                           color='count', color_continuous_scale='Purples', text='count')
                fig.update_traces(textposition='outside')
                fig.update_layout(coloraxis_showscale=False, title='동시 언급 순위')
                st.plotly_chart(fig, use_container_width=True)
            
            with col_right:
                # 히트맵
                if data['member'] is not None:
                    members = data['member']['member'].tolist()
                    matrix = pd.DataFrame(0, index=members, columns=members)
                    for _, row in data['cooccurrence'].iterrows():
                        m1, m2 = row['member_1'], row['member_2']
                        if m1 in members and m2 in members:
                            matrix.loc[m1, m2] = row['count']
                            matrix.loc[m2, m1] = row['count']
                    fig = px.imshow(matrix.values, x=members, y=members,
                                  color_continuous_scale='Purples', text_auto=True)
                    fig.update_layout(title='케미 히트맵')
                    st.plotly_chart(fig, use_container_width=True)
            
            top = data['cooccurrence'].iloc[0]
            st.markdown(f"""
            <div class="insight-box">
            <strong>💑 케미 인사이트</strong><br><br>
            가장 인기 케미: <strong>{top['pair']}</strong> ({top['count']}회)<br>
            → 듀오 콘텐츠/광고 제작 시 팬 반응 극대화 기대
            </div>
            """, unsafe_allow_html=True)
        else:
            st.info("케미 데이터가 없습니다.")
    
    # -------------------- 🏷️ 키워드 분석 --------------------
    elif deep_menu == "🏷️ 키워드 분석":
        tab1, tab2 = st.tabs(["👥 멤버별 키워드", "🌍 국가별 키워드"])
        
        with tab1:
            if data['member_keywords'] is not None:
                selected = st.selectbox("멤버 선택", data['member_keywords']['member'].tolist())
                kw = data['member_keywords'][data['member_keywords']['member'] == selected].iloc[0]
                
                col1, col2 = st.columns(2)
                with col1:
                    st.markdown("**🎨 비주얼 키워드**")
                    st.info(kw['top_visual'] if kw['top_visual'] else "-")
                    st.markdown("**🎤 실력 키워드**")
                    st.info(kw['top_talent'] if kw['top_talent'] else "-")
                with col2:
                    st.markdown("**😊 성격 키워드**")
                    st.info(kw['top_personality'] if kw['top_personality'] else "-")
                    st.markdown("**❤️ 사랑 키워드**")
                    st.info(kw['top_love'] if kw['top_love'] else "-")
                
                st.markdown("**📝 자주 등장하는 단어**")
                st.success(kw['top_raw_words'] if kw['top_raw_words'] else "-")
        
        with tab2:
            if data['region_keywords'] is not None:
                for _, row in data['region_keywords'].iterrows():
                    with st.expander(f"🌐 {row['region']} ({row['comment_count']:,}개)"):
                        col1, col2 = st.columns(2)
                        with col1:
                            st.markdown(f"**비주얼**: {row['top_visual'] or '-'}")
                            st.markdown(f"**실력**: {row['top_talent'] or '-'}")
                        with col2:
                            st.markdown(f"**사랑 표현**: {row['top_love'] or '-'}")
                            st.markdown(f"**자주 쓰는 단어**: {row['top_raw_words'] or '-'}")
    
    # -------------------- 💜 진성팬 분석 --------------------
    elif deep_menu == "💜 진성팬 분석":
        st.markdown("### 💜 진성팬 분석")
        
        col1, col2, col3 = st.columns(3)
        with col1:
            st.metric("진성팬 비율 (2회+)", f"{summary['loyal_fan_rate']}%")
        with col2:
            st.metric("슈퍼팬 비율 (5회+)", f"{summary['super_fan_rate']}%")
        with col3:
            if data['loyal_fans'] is not None:
                st.metric("슈퍼팬 수", f"{data['loyal_fans']['super_fans'].sum()}명")
        
        if data['loyal_fans'] is not None:
            # 스택 바 차트
            fig = go.Figure()
            df_lf = data['loyal_fans']
            for fan_type, col, color in [
                ('일반팬', 'casual_fans', '#E0E0E0'),
                ('정규팬', 'regular_fans', '#B39DDB'),
                ('진성팬', 'loyal_fans', '#7C4DFF'),
                ('슈퍼팬', 'super_fans', '#E91E63')
            ]:
                fig.add_trace(go.Bar(name=fan_type, x=df_lf['member'], y=df_lf[col], marker_color=color))
            fig.update_layout(barmode='stack', title='멤버별 팬 등급 분포')
            st.plotly_chart(fig, use_container_width=True)
            
            # 진성팬 비율 비교
            col_l, col_r = st.columns(2)
            with col_l:
                fig2 = px.bar(df_lf.sort_values('loyal_rate'), x='loyal_rate', y='member',
                            orientation='h', color='loyal_rate', color_continuous_scale='Purples',
                            text='loyal_rate', title='진성팬 비율')
                fig2.update_traces(texttemplate='%{text:.1f}%', textposition='outside')
                fig2.update_layout(coloraxis_showscale=False)
                st.plotly_chart(fig2, use_container_width=True)
            
            with col_r:
                fig3 = px.bar(df_lf.sort_values('super_fan_rate'), x='super_fan_rate', y='member',
                            orientation='h', color='super_fan_rate', color_continuous_scale='RdPu',
                            text='super_fan_rate', title='슈퍼팬 비율')
                fig3.update_traces(texttemplate='%{text:.1f}%', textposition='outside')
                fig3.update_layout(coloraxis_showscale=False)
                st.plotly_chart(fig3, use_container_width=True)
    
    # -------------------- 🎯 마케팅 인사이트 --------------------
    elif deep_menu == "🎯 마케팅 인사이트":
        st.markdown("### 🎯 마케팅 인사이트")
        
        if data['member_region_keywords'] is not None:
            df_mrk = data['member_region_keywords']
            regions = df_mrk['region'].unique().tolist()
            selected_region = st.selectbox("🌍 타겟 국가/지역", regions)
            
            df_region = df_mrk[df_mrk['region'] == selected_region].sort_values('comment_count', ascending=False)
            
            if len(df_region) > 0:
                col1, col2 = st.columns(2)
                
                with col1:
                    fig = px.bar(df_region, x='member', y='comment_count', color='member',
                               color_discrete_sequence=px.colors.qualitative.Set2, text='comment_count')
                    fig.update_traces(textposition='outside')
                    fig.update_layout(showlegend=False, title=f'{selected_region} 멤버별 인기도')
                    st.plotly_chart(fig, use_container_width=True)
                
                with col2:
                    total = {
                        '비주얼': df_region['visual_score'].sum(),
                        '실력': df_region['talent_score'].sum(),
                        '성격': df_region['personality_score'].sum(),
                        '사랑': df_region['love_score'].sum()
                    }
                    df_cat = pd.DataFrame({'category': list(total.keys()), 'score': list(total.values())})
                    fig = px.pie(df_cat, values='score', names='category', title='반응 카테고리',
                               color_discrete_sequence=['#8B5CF6', '#EC4899', '#F59E0B', '#10B981'])
                    st.plotly_chart(fig, use_container_width=True)
                
                top = df_region.iloc[0]
                top_cat = max(total, key=total.get)
                st.markdown(f"""
                <div class="insight-box">
                <strong>🎯 {selected_region} 마케팅 전략</strong><br><br>
                <strong>추천 멤버:</strong> {top['member']} (언급 {top['comment_count']}회)<br>
                <strong>추천 키워드:</strong> {top_cat}<br>
                <strong>콘텐츠 방향:</strong> {top['member']}의 {top_cat} 중심 콘텐츠
                </div>
                """, unsafe_allow_html=True)
        
        # 히트맵
        st.markdown("### 📊 멤버×국가 히트맵")
        if data['member_region_keywords'] is not None:
            pivot = data['member_region_keywords'].pivot_table(
                index='member', columns='region', values='comment_count', fill_value=0)
            fig = px.imshow(pivot.values, x=pivot.columns.tolist(), y=pivot.index.tolist(),
                          color_continuous_scale='Purples', text_auto=True, aspect='auto')
            st.plotly_chart(fig, use_container_width=True)

# ============================================================
# ⚖️ 그룹 비교
# ============================================================
elif analysis_mode == "⚖️ 그룹 비교":
    st.markdown("## ⚖️ 그룹 비교 분석")
    
    # 데이터 수집
    compare_data = []
    for name, info in GROUPS.items():
        d = deep_data[name]
        if d['summary'] is not None:
            s = d['summary'].iloc[0]
            compare_data.append({
                'group': name,
                'emoji': info['emoji'],
                'color': info['color'],
                'total_comments': s['total_comments'],
                'unique_authors': s['unique_authors'],
                'loyal_fan_rate': s['loyal_fan_rate'],
                'super_fan_rate': s['super_fan_rate']
            })
    
    if not compare_data:
        st.warning("비교할 데이터가 없습니다. 각 그룹의 CSV 파일을 업로드해주세요.")
        st.stop()
    
    df_compare = pd.DataFrame(compare_data)
    
    # 요약 카드
    st.markdown("### 📊 핵심 지표 비교")
    cols = st.columns(len(df_compare))
    for col, (_, row) in zip(cols, df_compare.iterrows()):
        with col:
            st.markdown(f"#### {row['emoji']} {row['group']}")
            st.metric("총 댓글", f"{row['total_comments']:,}")
            st.metric("고유 작성자", f"{row['unique_authors']:,}")
            st.metric("진성팬 비율", f"{row['loyal_fan_rate']}%")
            st.metric("슈퍼팬 비율", f"{row['super_fan_rate']}%")
    
    st.markdown("")
    
    # 비교 차트
    col_left, col_right = st.columns(2)
    
    with col_left:
        st.markdown("### 💜 진성팬 비율 비교")
        fig = px.bar(df_compare.sort_values('loyal_fan_rate'), x='loyal_fan_rate', y='group',
                   orientation='h', color='group',
                   color_discrete_map={r['group']: r['color'] for _, r in df_compare.iterrows()},
                   text='loyal_fan_rate')
        fig.update_traces(texttemplate='%{text:.1f}%', textposition='outside')
        fig.update_layout(showlegend=False, xaxis_title='진성팬 비율 (%)', yaxis_title='')
        st.plotly_chart(fig, use_container_width=True)
    
    with col_right:
        st.markdown("### 👥 고유 작성자 수 비교")
        fig = px.bar(df_compare.sort_values('unique_authors'), x='unique_authors', y='group',
                   orientation='h', color='group',
                   color_discrete_map={r['group']: r['color'] for _, r in df_compare.iterrows()},
                   text='unique_authors')
        fig.update_traces(texttemplate='%{text:,}', textposition='outside')
        fig.update_layout(showlegend=False, xaxis_title='고유 작성자 수', yaxis_title='')
        st.plotly_chart(fig, use_container_width=True)
    
    # 언어 분포 비교
    st.markdown("### 🌐 언어 분포 비교")
    
    lang_compare = []
    for name, info in GROUPS.items():
        d = deep_data[name]
        if d['language'] is not None:
            for _, row in d['language'].head(5).iterrows():
                lang_compare.append({
                    'group': name,
                    'region': row['region'],
                    'percentage': row['percentage']
                })
    
    if lang_compare:
        df_lang = pd.DataFrame(lang_compare)
        fig = px.bar(df_lang, x='region', y='percentage', color='group', barmode='group',
                   color_discrete_map={r['group']: r['color'] for _, r in df_compare.iterrows()})
        fig.update_layout(xaxis_title='국가/지역', yaxis_title='비율 (%)')
        st.plotly_chart(fig, use_container_width=True)
    
    # 인사이트
    top_loyal = df_compare.sort_values('loyal_fan_rate', ascending=False).iloc[0]
    top_authors = df_compare.sort_values('unique_authors', ascending=False).iloc[0]
    
    st.markdown(f"""
    <div class="insight-box">
    <strong>⚖️ 그룹 비교 인사이트</strong><br><br>
    • <strong>가장 높은 진성팬 비율:</strong> {top_loyal['group']} ({top_loyal['loyal_fan_rate']}%)<br>
    &nbsp;&nbsp;&nbsp;→ 팬덤 충성도가 가장 높아 장기 마케팅에 유리<br><br>
    • <strong>가장 많은 참여자:</strong> {top_authors['group']} ({top_authors['unique_authors']:,}명)<br>
    &nbsp;&nbsp;&nbsp;→ 팬덤 규모가 커서 바이럴 마케팅에 유리
    </div>
    """, unsafe_allow_html=True)

# ============================================================
# 푸터
# ============================================================
st.markdown('<hr class="divider">', unsafe_allow_html=True)

# 다운로드 버튼
if analysis_mode == "🔬 심층 댓글 분석" and data['member'] is not None:
    col1, col2, col3 = st.columns(3)
    with col1:
        csv = data['member'].to_csv(index=False, encoding='utf-8-sig')
        st.download_button("📥 멤버 분석 CSV", csv, f"{group_info['prefix']}_member.csv", "text/csv")
    with col2:
        if data['loyal_fans'] is not None:
            csv = data['loyal_fans'].to_csv(index=False, encoding='utf-8-sig')
            st.download_button("📥 진성팬 CSV", csv, f"{group_info['prefix']}_loyal.csv", "text/csv")
    with col3:
        if data['member_region_keywords'] is not None:
            csv = data['member_region_keywords'].to_csv(index=False, encoding='utf-8-sig')
            st.download_button("📥 마케팅 인사이트 CSV", csv, f"{group_info['prefix']}_marketing.csv", "text/csv")

st.markdown("""
<div class="footer">
    <p><strong>KFANTRIX</strong> - K-pop 팬덤 데이터로 글로벌 마케팅 성공률을 높이다</p>
    <p>© 2025 KFANTRIX. All rights reserved.</p>
    <p>📧 contact@kfantrix.com</p>
</div>
""", unsafe_allow_html=True)
