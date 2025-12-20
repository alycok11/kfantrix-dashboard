# KFANTRIX - K-pop Channel Analytics Dashboard

K-pop 채널 성과 분석 대시보드 프로토타입입니다.

## 🚀 실행 방법

### 1. 설치
```bash
pip install -r requirements.txt
```

### 2. 실행
```bash
streamlit run kfantrix_app.py
```

### 3. 브라우저 접속
자동으로 열리거나, http://localhost:8501 로 접속하세요.

---

## 📦 무료 배포 (Streamlit Cloud)

### 방법 1: GitHub 연동 배포

1. **GitHub에 레포지토리 생성**
   - 새 레포지토리: `kfantrix-dashboard`

2. **파일 업로드**
   - `kfantrix_app.py`
   - `requirements.txt`

3. **Streamlit Cloud 접속**
   - https://streamlit.io/cloud
   - GitHub 계정으로 로그인

4. **New app 클릭**
   - Repository: `your-username/kfantrix-dashboard`
   - Branch: `main`
   - Main file path: `kfantrix_app.py`

5. **Deploy 클릭**
   - 약 2-3분 후 배포 완료
   - URL: `https://kfantrix.streamlit.app` (커스텀 가능)

---

## 🎨 주요 기능

- ✅ 아티스트 비교 분석 (NMIXX vs PLAVE)
- ✅ 핵심 지표 대시보드 (구독자, 조회수, 참여도, 팬덤활성도)
- ✅ 인터랙티브 차트 (Plotly)
- ✅ 레이더 차트 (종합 스코어)
- ✅ CSV 다운로드
- ✅ 반응형 레이아웃
- ✅ 필터 기능

---

## 📊 확장 아이디어

### Phase 2: 기능 추가
- [ ] 실시간 YouTube API 연동
- [ ] 아티스트 검색 기능
- [ ] 국가별 팬덤 분석 페이지
- [ ] 감성 분석 결과 시각화

### Phase 3: 비즈니스 확장
- [ ] 사용자 로그인/결제 시스템
- [ ] 구독 플랜별 기능 제한
- [ ] API 제공

---

## 🛠 기술 스택

- **Frontend**: Streamlit
- **Charts**: Plotly
- **Data**: Pandas
- **Deployment**: Streamlit Cloud (무료)

---

## 📧 문의

- Email: contact@kfantrix.com
- Website: www.kfantrix.com

© 2025 KFANTRIX
