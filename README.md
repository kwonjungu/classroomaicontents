# 교실에서 바로 사용하는 AI 컨텐츠 제작

수업에 바로 쓰는 AI 콘텐츠·도구·활용 가이드를 모아두는 페이지입니다.

## 디자인 시스템

Nike 에디토리얼 커머스 시스템을 기반으로 합니다.

- **색**: 검정(`--ink #111`) · 흰색(`--canvas`) · 소프트클라우드(`--soft-cloud #f5f5f5`)가 화면의 95%
- **타이포**: 캠페인 헤드라인은 Black Han Sans / Bebas Neue (Futura ND 대체, 96px·line-height 0.9), UI는 Pretendard (Helvetica Now / Inter 대체)
- **버튼**: 모두 pill (`--rounded-lg 30px`) 또는 원형 아이콘. 각진 버튼 없음
- **카드**: 그림자·라운드 없이 평평하게, 사진이 곧 카드
- **간격**: 8px 기준, 섹션 사이 48px 리듬

## 파일

| 파일 | 내용 |
|---|---|
| `index.html` | 페이지 마크업 |
| `styles.css` | 디자인 시스템 토큰 + 컴포넌트 |

## 구성

위에서 아래로 스크롤하는 강의용 페이지입니다.

1. 질문 히어로 — "인공지능 어떻게 쓰고 계신가요?" + Gemini 배지
2. 수업 목표
3. Gemini 바로 가기 (주의: `@gmail.com` 일반 계정 접속)
4. 강의 섹션 6개 (`#s1`~`#s6`)
   - `s1` 바이브 코딩이란
   - `s2` 인공지능으로 그리는 그림
   - `s3` 인공지능으로 만드는 나만의 앱
   - `s4` 인공지능으로 간단한 영상 만들기
   - `s5` PPT 자료가 이렇게 쉽게?
   - `s6` 패들렛 아케이드로 빠르게 만드는 학생참여형 퀴즈

## 콘텐츠 채우는 법

- **설명 수정**: 각 `<section class="lecture">`의 `.lecture-copy p` 문구를 강의 내용에 맞게 고칩니다.
- **이미지 넣기**: `.lecture-media` 안에 `<img src="assets/..." alt="...">`를 넣으면 그라데이션 자리에 사진/캡처가 들어갑니다.
- **히어로 사진**: `<section class="hero">`에 `style="background-image:url('이미지경로')"`를 추가하면 질문이 사진 위에 얹힙니다.
- **순서·추가**: `lecture` 블록을 복사하고 `reverse` 클래스를 번갈아 붙이면 좌우 교차 배치가 유지됩니다.

## GitHub Pages 배포

저장소 **Settings → Pages → Branch: `main` / `(root)`** 선택 후 저장하면
`https://kwonjungu.github.io/classroomaicontents/` 에서 열립니다.
