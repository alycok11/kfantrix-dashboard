# kfantrix_deep_app.py - PLAVE 심층 분석 대시보드 v2
# GitHub에 업로드 후 Streamlit Cloud에서 실행

import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime

# ============================================================
# 페이지 설정
# ============================================================
st.set_page_config(
    page_title="KFANTRIX - PLAVE Deep Analytics",
    page_icon="💜",
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
        background: linear-gradient(135deg, #8B5CF6 0%, #EC4899 100%);
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
    .insight-box {
        background: linear-gradient(135deg, #8B5CF6 0%, #EC4899 100%);
        color: white;
        padding: 1.2rem 1.5rem;
        border-radius: 12px;
        margin: 1rem 0;
        font-size: 1rem;
    }
    .insight-box-blue {
        background: linear-gradient(135deg, #3B82F6 0%, #8B5CF6 100%);
        color: white;
        padding: 1.2rem 1.5rem;
        border-radius: 12px;
        margin: 1rem 0;
    }
    .keyword-tag {
        display: inline-block;
        background: #f0f0ff;
        padding: 0.3rem 0.8rem;
        border-radius: 20px;
        margin: 0.2rem;
        font-size: 0.9rem;
    }
    .divider {
        height: 3px;
        background: linear-gradient(90deg, #8B5CF6 0%, #EC4899 100%);
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
</style>
""", unsafe_allow_html=True)

# ============================================================
# 데이터 로드
# ============================================================
@st.cache_data
def load_all_data():
    """모든 CSV 데이터 로드"""
    data = {}
    
    files = {
        'summary': 'plave_summary.csv',
        'language': 'plave_language_stats.csv',
        'member': 'plave_member_stats.csv',
        'region_member': 'plave_region_member.csv',
        'cooccurrence': 'plave_member_cooccurrence.csv',
        'member_keywords': 'plave_member_keywords.csv',
        'region_keywords': 'plave_region_keywords.csv',
        'member_region_keywords': 'plave_member_region_keywords.csv',
        'loyal_fans': 'plave_loyal_fans.csv',
        'video_engagement': 'plave_video_engagement.csv'
    }
    
    for key, filename in files.items():
        try:
            data[key] = pd.read_csv(filename)
        except:
            data[key] = None
    
    return data

data = load_all_data()

# 데이터 체크
if data['summary'] is None:
    st.error("⚠️ 데이터 파일을 찾을 수 없습니다.")
    st.stop()

# ============================================================
# 사이드바
# ============================================================
with st.sidebar:
    st.markdown("## 💜 KFANTRIX")
    st.markdown("PLAVE 심층 분석 v2")
    st.divider()
    
    if data['summary'] is not None:
        summary = data['summary'].iloc[0]
        st.markdown("### 📊 데이터 정보")
        st.markdown(f"**수집일시:** {summary['collected_at']}")
        st.markdown(f"**총 댓글:** {summary['total_comments']:,}개")
        st.markdown(f"**분석 영상:** {summary['total_videos']}개")
        st.markdown(f"**고유 작성자:** {summary['unique_authors']:,}명")
    
    st.divider()
    
    st.markdown("### 📑 분석 메뉴")
    analysis_type = st.radio(
        "분석 유형 선택",
        [
            "📊 전체 요약",
            "💑 멤버 케미 분석",
            "🏷️ 키워드 심층 분석",
            "💜 진성팬 분석",
            "📹 영상별 반응",
            "🎯 마케팅 인사이트"
        ],
        label_visibility="collapsed"
    )

# ============================================================
# 헤더
# ============================================================
st.markdown('<h1 class="main-header">KFANTRIX</h1>', unsafe_allow_html=True)
st.markdown('<p class="sub-header">PLAVE 글로벌 팬덤 심층 분석 · 마케팅 인사이트</p>', unsafe_allow_html=True)
st.markdown('<hr class="divider">', unsafe_allow_html=True)

# ============================================================
# 📊 전체 요약
# ============================================================
if analysis_type == "📊 전체 요약":
    st.markdown("## 📊 전체 요약")
    
    summary = data['summary'].iloc[0]
    
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
    
    st.markdown("")
    
    col_left, col_right = st.columns(2)
    
    with col_left:
        st.markdown("### 🌐 언어 분포")
        if data['language'] is not None:
            df_lang = data['language'].head(8)
            fig_lang = px.pie(
                df_lang, values='percentage', names='region',
                color_discrete_sequence=px.colors.sequential.Purples_r, hole=0.4
            )
            fig_lang.update_layout(showlegend=True)
            st.plotly_chart(fig_lang, use_container_width=True)
    
    with col_right:
        st.markdown("### 👥 멤버 언급 비율")
        if data['member'] is not None:
            df_mem = data['member'].sort_values('mention_count', ascending=True)
            fig_mem = px.bar(
                df_mem, x='mention_count', y='member', orientation='h',
                color='mention_rate', color_continuous_scale='Purples', text='mention_rate'
            )
            fig_mem.update_traces(texttemplate='%{text:.1f}%', textposition='outside')
            fig_mem.update_layout(showlegend=False, coloraxis_showscale=False)
            st.plotly_chart(fig_mem, use_container_width=True)
    
    # 케미 TOP 3
    if data['cooccurrence'] is not None and len(data['cooccurrence']) > 0:
        st.markdown("### 💑 인기 케미 TOP 3")
        col1, col2, col3 = st.columns(3)
        df_chem = data['cooccurrence'].head(3)
        
        for idx, (col, (_, row)) in enumerate(zip([col1, col2, col3], df_chem.iterrows())):
            with col:
                st.metric(f"#{idx+1} {row['pair']}", f"{row['count']}회 동시 언급")

# ============================================================
# 💑 멤버 케미 분석
# ============================================================
elif analysis_type == "💑 멤버 케미 분석":
    st.markdown("## 💑 멤버 케미 분석")
    st.markdown("*어떤 멤버들이 함께 언급되나요?*")
    
    if data['cooccurrence'] is not None and len(data['cooccurrence']) > 0:
        df_chem = data['cooccurrence']
        
        col_left, col_right = st.columns(2)
        
        with col_left:
            st.markdown("### 📊 동시 언급 순위")
            fig = px.bar(
                df_chem.head(10), x='pair', y='count',
                color='count', color_continuous_scale='Purples', text='count'
            )
            fig.update_traces(textposition='outside')
            fig.update_layout(coloraxis_showscale=False, xaxis_title='멤버 조합', yaxis_title='동시 언급 횟수')
            st.plotly_chart(fig, use_container_width=True)
        
        with col_right:
            st.markdown("### 🔗 케미 네트워크")
            
            # 히트맵 데이터 준비
            members = ['노아', '밤비', '은호', '하민', '예준']
            matrix = pd.DataFrame(0, index=members, columns=members)
            
            for _, row in df_chem.iterrows():
                m1, m2 = row['member_1'], row['member_2']
                if m1 in members and m2 in members:
                    matrix.loc[m1, m2] = row['count']
                    matrix.loc[m2, m1] = row['count']
            
            fig_heat = px.imshow(
                matrix.values, x=members, y=members,
                color_continuous_scale='Purples', text_auto=True
            )
            fig_heat.update_layout(xaxis_title='', yaxis_title='')
            st.plotly_chart(fig_heat, use_container_width=True)
        
        # 인사이트
        top_pair = df_chem.iloc[0]
        st.markdown(f"""
        <div class="insight-box">
        <strong>💑 케미 인사이트</strong><br><br>
        • 가장 인기 있는 케미: <strong>{top_pair['pair']}</strong> ({top_pair['count']}회)<br>
        • 이 조합으로 듀오 콘텐츠/광고 제작 시 팬 반응 극대화 기대<br>
        • 팬미팅, 유닛 활동, 브랜드 협업에 활용 추천
        </div>
        """, unsafe_allow_html=True)
    else:
        st.info("케미 데이터가 없습니다.")

# ============================================================
# 🏷️ 키워드 심층 분석
# ============================================================
elif analysis_type == "🏷️ 키워드 심층 분석":
    st.markdown("## 🏷️ 키워드 심층 분석")
    
    tab1, tab2, tab3 = st.tabs(["👥 멤버별 키워드", "🌍 국가별 키워드", "🎯 멤버×국가"])
    
    # 멤버별 키워드
    with tab1:
        st.markdown("### 👥 멤버별 연관 키워드")
        
        if data['member_keywords'] is not None:
            selected_member = st.selectbox("멤버 선택", data['member_keywords']['member'].tolist())
            member_kw = data['member_keywords'][data['member_keywords']['member'] == selected_member].iloc[0]
            
            col1, col2 = st.columns(2)
            
            with col1:
                st.markdown("#### 🎨 비주얼 키워드")
                st.info(member_kw['top_visual'] if member_kw['top_visual'] else "데이터 없음")
                
                st.markdown("#### 🎤 실력 키워드")
                st.info(member_kw['top_talent'] if member_kw['top_talent'] else "데이터 없음")
            
            with col2:
                st.markdown("#### 😊 성격 키워드")
                st.info(member_kw['top_personality'] if member_kw['top_personality'] else "데이터 없음")
                
                st.markdown("#### ❤️ 사랑 키워드")
                st.info(member_kw['top_love'] if member_kw['top_love'] else "데이터 없음")
            
            st.markdown("#### 📝 자주 등장하는 단어 TOP 10")
            st.success(member_kw['top_raw_words'] if member_kw['top_raw_words'] else "데이터 없음")
    
    # 국가별 키워드
    with tab2:
        st.markdown("### 🌍 국가별 반응 키워드")
        
        if data['region_keywords'] is not None:
            df_rk = data['region_keywords']
            
            for _, row in df_rk.iterrows():
                with st.expander(f"🌐 {row['region']} ({row['comment_count']:,}개 댓글)"):
                    col1, col2 = st.columns(2)
                    with col1:
                        st.markdown("**비주얼 반응**")
                        st.write(row['top_visual'] if row['top_visual'] else "-")
                        st.markdown("**실력 반응**")
                        st.write(row['top_talent'] if row['top_talent'] else "-")
                    with col2:
                        st.markdown("**사랑 표현**")
                        st.write(row['top_love'] if row['top_love'] else "-")
                        st.markdown("**자주 쓰는 단어**")
                        st.write(row['top_raw_words'] if row['top_raw_words'] else "-")
    
    # 멤버×국가 키워드
    with tab3:
        st.markdown("### 🎯 멤버별 국가별 반응")
        
        if data['member_region_keywords'] is not None:
            df_mrk = data['member_region_keywords']
            
            # 필터
            col1, col2 = st.columns(2)
            with col1:
                filter_member = st.selectbox("멤버", ['전체'] + df_mrk['member'].unique().tolist())
            with col2:
                filter_region = st.selectbox("국가", ['전체'] + df_mrk['region'].unique().tolist())
            
            df_filtered = df_mrk.copy()
            if filter_member != '전체':
                df_filtered = df_filtered[df_filtered['member'] == filter_member]
            if filter_region != '전체':
                df_filtered = df_filtered[df_filtered['region'] == filter_region]
            
            # 히트맵
            if len(df_filtered) > 0:
                st.markdown("#### 📊 반응 카테고리 분포")
                
                fig = go.Figure()
                
                for _, row in df_filtered.iterrows():
                    fig.add_trace(go.Bar(
                        name=f"{row['member']}-{row['region']}",
                        x=['비주얼', '실력', '성격', '사랑'],
                        y=[row['visual_score'], row['talent_score'], row['personality_score'], row['love_score']],
                        text=[row['visual_score'], row['talent_score'], row['personality_score'], row['love_score']]
                    ))
                
                fig.update_layout(barmode='group', xaxis_title='카테고리', yaxis_title='점수')
                st.plotly_chart(fig, use_container_width=True)
                
                # 테이블
                st.markdown("#### 📋 상세 데이터")
                df_display = df_filtered[['member', 'region', 'comment_count', 'top_category', 'top_words']].copy()
                df_display.columns = ['멤버', '국가', '댓글 수', '주요 반응', '키워드']
                st.dataframe(df_display, use_container_width=True, hide_index=True)

# ============================================================
# 💜 진성팬 분석
# ============================================================
elif analysis_type == "💜 진성팬 분석":
    st.markdown("## 💜 진성팬 분석")
    st.markdown("*팬덤의 깊이와 충성도를 분석합니다*")
    
    if data['loyal_fans'] is not None:
        df_lf = data['loyal_fans']
        
        # 전체 요약
        summary = data['summary'].iloc[0]
        col1, col2, col3 = st.columns(3)
        with col1:
            st.metric("전체 진성팬 비율 (2회+)", f"{summary['loyal_fan_rate']}%")
        with col2:
            st.metric("슈퍼팬 비율 (5회+)", f"{summary['super_fan_rate']}%")
        with col3:
            total_super = df_lf['super_fans'].sum()
            st.metric("슈퍼팬 수", f"{total_super}명")
        
        st.markdown("### 👥 멤버별 팬 등급 분포")
        
        # 스택 바 차트
        fig = go.Figure()
        
        colors = {'일반팬': '#E0E0E0', '정규팬': '#B39DDB', '진성팬': '#7C4DFF', '슈퍼팬': '#EC4899'}
        
        for fan_type, col, color in [
            ('일반팬 (1회)', 'casual_fans', colors['일반팬']),
            ('정규팬 (2-4회)', 'regular_fans', colors['정규팬']),
            ('진성팬 (5-9회)', 'loyal_fans', colors['진성팬']),
            ('슈퍼팬 (10회+)', 'super_fans', colors['슈퍼팬'])
        ]:
            fig.add_trace(go.Bar(
                name=fan_type,
                x=df_lf['member'],
                y=df_lf[col],
                marker_color=color,
                text=df_lf[col],
                textposition='inside'
            ))
        
        fig.update_layout(barmode='stack', xaxis_title='멤버', yaxis_title='팬 수')
        st.plotly_chart(fig, use_container_width=True)
        
        # 멤버별 상세
        st.markdown("### 📊 멤버별 상세")
        
        col_left, col_right = st.columns(2)
        
        with col_left:
            # 진성팬 비율 비교
            fig2 = px.bar(
                df_lf.sort_values('loyal_rate', ascending=True),
                x='loyal_rate', y='member', orientation='h',
                color='loyal_rate', color_continuous_scale='Purples',
                text='loyal_rate', title='진성팬 비율 (5회+ 작성)'
            )
            fig2.update_traces(texttemplate='%{text:.1f}%', textposition='outside')
            fig2.update_layout(coloraxis_showscale=False)
            st.plotly_chart(fig2, use_container_width=True)
        
        with col_right:
            # 슈퍼팬 비율 비교
            fig3 = px.bar(
                df_lf.sort_values('super_fan_rate', ascending=True),
                x='super_fan_rate', y='member', orientation='h',
                color='super_fan_rate', color_continuous_scale='RdPu',
                text='super_fan_rate', title='슈퍼팬 비율 (10회+ 작성)'
            )
            fig3.update_traces(texttemplate='%{text:.1f}%', textposition='outside')
            fig3.update_layout(coloraxis_showscale=False)
            st.plotly_chart(fig3, use_container_width=True)
        
        # 진성팬 키워드
        st.markdown("### 🏷️ 진성팬들이 자주 쓰는 키워드")
        
        for _, row in df_lf.iterrows():
            if row['loyal_fan_keywords']:
                with st.expander(f"💜 {row['member']} 진성팬 키워드"):
                    st.write(row['loyal_fan_keywords'])
        
        # 인사이트
        top_loyal = df_lf.sort_values('loyal_rate', ascending=False).iloc[0]
        st.markdown(f"""
        <div class="insight-box">
        <strong>💜 진성팬 인사이트</strong><br><br>
        • 가장 높은 진성팬 비율: <strong>{top_loyal['member']}</strong> ({top_loyal['loyal_rate']}%)<br>
        • 진성팬은 바이럴 마케팅의 핵심 → 이들 타겟 이벤트/굿즈 추천<br>
        • 슈퍼팬({df_lf['super_fans'].sum()}명)은 팬커뮤니티 리더 역할 기대
        </div>
        """, unsafe_allow_html=True)

# ============================================================
# 📹 영상별 반응
# ============================================================
elif analysis_type == "📹 영상별 반응":
    st.markdown("## 📹 영상별 반응 분석")
    
    if data['video_engagement'] is not None:
        df_ve = data['video_engagement']
        
        # 요약
        col1, col2, col3 = st.columns(3)
        with col1:
            st.metric("분석 영상", f"{len(df_ve)}개")
        with col2:
            st.metric("평균 댓글", f"{df_ve['comment_count'].mean():.0f}개")
        with col3:
            st.metric("평균 작성자", f"{df_ve['unique_authors'].mean():.0f}명")
        
        # 영상별 댓글 수
        st.markdown("### 📊 영상별 댓글 수")
        
        fig = px.bar(
            df_ve, x='video_title', y='comment_count',
            color='comment_count', color_continuous_scale='Purples',
            text='comment_count'
        )
        fig.update_traces(textposition='outside')
        fig.update_layout(xaxis_tickangle=-45, coloraxis_showscale=False)
        st.plotly_chart(fig, use_container_width=True)
        
        # 영상별 언어 비율
        st.markdown("### 🌐 영상별 한국어/영어 비율")
        
        fig2 = go.Figure()
        fig2.add_trace(go.Bar(name='한국어', x=df_ve['video_title'], y=df_ve['korean_rate'], marker_color='#8B5CF6'))
        fig2.add_trace(go.Bar(name='영어', x=df_ve['video_title'], y=df_ve['english_rate'], marker_color='#EC4899'))
        fig2.update_layout(barmode='group', xaxis_tickangle=-45, yaxis_title='비율 (%)')
        st.plotly_chart(fig2, use_container_width=True)
        
        # 영상별 인기 멤버 & 키워드
        st.markdown("### 👥 영상별 인기 멤버 & 키워드")
        
        df_display = df_ve[['video_title', 'comment_count', 'top_member', 'top_member_count', 'top_keywords']].copy()
        df_display.columns = ['영상', '댓글 수', '인기 멤버', '언급 횟수', '주요 키워드']
        df_display['영상'] = df_display['영상'].str[:40] + '...'
        st.dataframe(df_display, use_container_width=True, hide_index=True)

# ============================================================
# 🎯 마케팅 인사이트
# ============================================================
elif analysis_type == "🎯 마케팅 인사이트":
    st.markdown("## 🎯 마케팅 인사이트")
    st.markdown("*어떤 국가에서 어떤 멤버와 어떤 키워드로 마케팅할까?*")
    
    # 국가 선택
    if data['member_region_keywords'] is not None:
        df_mrk = data['member_region_keywords']
        regions = df_mrk['region'].unique().tolist()
        selected_region = st.selectbox("🌍 타겟 국가/지역 선택", regions)
        
        df_region = df_mrk[df_mrk['region'] == selected_region].sort_values('comment_count', ascending=False)
        
        if len(df_region) > 0:
            st.markdown(f"### 🎯 {selected_region} 시장 분석")
            
            col1, col2 = st.columns(2)
            
            with col1:
                # 멤버별 인기도
                fig1 = px.bar(
                    df_region, x='member', y='comment_count',
                    color='member', color_discrete_sequence=px.colors.qualitative.Set2, text='comment_count'
                )
                fig1.update_traces(textposition='outside')
                fig1.update_layout(showlegend=False, title='멤버별 인기도')
                st.plotly_chart(fig1, use_container_width=True)
            
            with col2:
                # 반응 카테고리
                total = {
                    '비주얼': df_region['visual_score'].sum(),
                    '실력': df_region['talent_score'].sum(),
                    '성격': df_region['personality_score'].sum(),
                    '사랑': df_region['love_score'].sum()
                }
                df_cat = pd.DataFrame({'category': list(total.keys()), 'score': list(total.values())})
                
                fig2 = px.pie(df_cat, values='score', names='category', title='반응 카테고리',
                             color_discrete_sequence=['#8B5CF6', '#EC4899', '#F59E0B', '#10B981'])
                st.plotly_chart(fig2, use_container_width=True)
            
            # 추천 전략
            top_member = df_region.iloc[0]
            top_category = max(total, key=total.get)
            
            st.markdown(f"""
            <div class="insight-box">
            <strong>🎯 {selected_region} 마케팅 전략</strong><br><br>
            
            <strong>1. 추천 협업 멤버:</strong> {top_member['member']}<br>
            &nbsp;&nbsp;&nbsp;• 언급량 {top_member['comment_count']}회로 해당 지역 1위<br>
            &nbsp;&nbsp;&nbsp;• 주요 반응: {top_member['top_category']}<br><br>
            
            <strong>2. 추천 마케팅 키워드:</strong> {top_category}<br>
            &nbsp;&nbsp;&nbsp;• 해당 지역에서 가장 많은 반응을 얻는 요소<br><br>
            
            <strong>3. 콘텐츠 방향:</strong><br>
            &nbsp;&nbsp;&nbsp;• {top_member['member']}의 {top_category} 중심 콘텐츠 제작<br>
            &nbsp;&nbsp;&nbsp;• 관련 키워드: {top_member['top_words'] if top_member['top_words'] else 'N/A'}
            </div>
            """, unsafe_allow_html=True)
    
    # 전체 히트맵
    st.markdown("### 📊 전체 멤버×국가 히트맵")
    
    if data['member_region_keywords'] is not None:
        df_mrk = data['member_region_keywords']
        
        pivot = df_mrk.pivot_table(index='member', columns='region', values='comment_count', fill_value=0)
        
        fig_heat = px.imshow(
            pivot.values, x=pivot.columns.tolist(), y=pivot.index.tolist(),
            color_continuous_scale='Purples', text_auto=True, aspect='auto'
        )
        fig_heat.update_layout(xaxis_title='국가/지역', yaxis_title='멤버')
        st.plotly_chart(fig_heat, use_container_width=True)
    
    # 케미 활용 전략
    if data['cooccurrence'] is not None and len(data['cooccurrence']) > 0:
        st.markdown("### 💑 케미 활용 전략")
        
        top_chems = data['cooccurrence'].head(3)
        
        col1, col2, col3 = st.columns(3)
        for col, (_, row) in zip([col1, col2, col3], top_chems.iterrows()):
            with col:
                st.markdown(f"""
                <div class="insight-box-blue">
                <strong>{row['pair']}</strong><br>
                동시 언급 {row['count']}회<br><br>
                • 듀오 콘텐츠 추천<br>
                • 팬미팅 유닛 활동<br>
                • 브랜드 듀얼 모델
                </div>
                """, unsafe_allow_html=True)

# ============================================================
# 푸터
# ============================================================
st.markdown('<hr class="divider">', unsafe_allow_html=True)

col_dl1, col_dl2, col_dl3 = st.columns(3)

with col_dl1:
    if data['member_keywords'] is not None:
        csv = data['member_keywords'].to_csv(index=False, encoding='utf-8-sig')
        st.download_button("📥 멤버 키워드 CSV", csv, "plave_member_keywords.csv", "text/csv")

with col_dl2:
    if data['loyal_fans'] is not None:
        csv = data['loyal_fans'].to_csv(index=False, encoding='utf-8-sig')
        st.download_button("📥 진성팬 분석 CSV", csv, "plave_loyal_fans.csv", "text/csv")

with col_dl3:
    if data['member_region_keywords'] is not None:
        csv = data['member_region_keywords'].to_csv(index=False, encoding='utf-8-sig')
        st.download_button("📥 마케팅 인사이트 CSV", csv, "plave_marketing.csv", "text/csv")

st.markdown("""
<div class="footer">
    <p><strong>KFANTRIX</strong> - K-pop 팬덤 데이터로 글로벌 마케팅 성공률을 높이다</p>
    <p>© 2025 KFANTRIX. All rights reserved.</p>
</div>
""", unsafe_allow_html=True)
