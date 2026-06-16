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

## 콘텐츠 채우는 법

1. **카드 추가**: `index.html`의 `.grid` 안에 `<article class="card">` 블록을 복사해 제목/대상/메타를 바꾸면 됩니다.
2. **썸네일 넣기**: 카드의 `<div class="card-image">` 안 `<span class="placeholder">` 자리에 `<img src="..." alt="...">`를 넣습니다.
3. **히어로 사진**: `<section class="hero" ...>`에 `style="background-image:url('이미지경로')"`를 추가하면 헤드라인이 사진 위에 얹힙니다.
4. **분야 타일 / 도구 아이콘 / 활용 카드**도 같은 방식으로 텍스트만 교체하면 됩니다.

## GitHub Pages 배포

저장소 **Settings → Pages → Branch: `main` / `(root)`** 선택 후 저장하면
`https://kwonjungu.github.io/classroomaicontents/` 에서 열립니다.
