# -*- coding: utf-8 -*-
"""노트북 LM 총정리 편 사이트 만들기 (notebook/) — myfirstaigent(build_new.py) 틀을 그대로 따름
   - 홈(허브) · 개념 · 처음 준비 · 실습 페이지들 · 정리
   - 실습 목록·프롬프트·실측 메모는 tools/notebook_practices.py (P·INFO·NOTE) 한 곳에서
   - 캡처: assets/notebook/shot/<키>.png 가 있으면 그림, 없으면 '캡처 예정' 칸
     키 목록: 01_home 03_upload_formats 04_citation 05_trap_answer 06_label 07_slide 08_infographic 09_datatable_sheet 10_form
   - 스타일: notebook/styles.css · extra.css · site.js (myfirstaigent에서 복사) + notebook/nb.css
   사용: python tools/build_notebook.py   (저장소 루트에서 / 의존: qrcode)"""
import os, re, sys, html
sys.stdout.reconfigure(encoding="utf-8")
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUT = os.path.join(ROOT, "notebook")
SHOT_DIR = os.path.join(ROOT, "assets", "notebook", "shot")
sys.path.insert(0, os.path.join(ROOT, "tools"))
from notebook_practices import P, INFO, NOTE  # noqa: E402

E = html.escape
NAME = "노트북 LM 총정리 편"
SITE_URL = "https://classroomaicontents.vercel.app/notebook/"
ZIP_FILE = os.path.join(ROOT, "assets", "notebook", "노트북연수_실습.zip")
ZIP_HREF = "../assets/notebook/%EB%85%B8%ED%8A%B8%EB%B6%81%EC%97%B0%EC%88%98_%EC%8B%A4%EC%8A%B5.zip"
ZIP_SIZE = f"{os.path.getsize(ZIP_FILE)/1024/1024:.0f}MB" if os.path.exists(ZIP_FILE) else ""
assert sorted(x[0] for x in P) == sorted(INFO), "P와 INFO의 실습 번호가 달라요"

LEVELS = ["기본", "보통", "도전"]
LVCLS = {"기본": "lv1", "보통": "lv2", "도전": "lv3"}
TILES = ["tile-notebook", "tile-write", "tile-eval", "tile-image", "tile-code", "tile-flow", "tile-video"]
SHOT_CAP = {"01_home": "노트북 첫 화면", "03_upload_formats": "올릴 수 있는 형식 (hwp·hwpx 포함, xlsx 없음)",
            "04_citation": "답마다 붙는 인용 번호", "05_trap_answer": "함정 질문: 자료에 없다고 답함",
            "06_label": "라벨로 소스 나누기", "07_slide": "결과 보고 슬라이드", "08_infographic": "실측 인포그래픽 — 상위 점수가 부풀려짐(4.2~4.4 표시, 실제 4.16)",
            "09_datatable_sheet": "데이터 표 → 구글 시트", "10_form": "구글 폼 퀴즈",
            "b1_video_dialog": "동영상 맞춤설정 — 짧은 버전(세로)·설명 동영상, 추천 주제, 맞춤 주제",
            "b1_video_explain": "예시 정답 · 설명 동영상 7분 19초 (종이공예 장면 + 교과서 쪽을 근거로 보여 줌)",
            "b1_video_short": "예시 정답 · 짧은 버전 1분 8초 (세로, 한글 자막) — 제목은 '15일', 장면은 '7일'로 어긋남",
            "b1_infographic": "예시 정답 · 옛날/오늘날 대조 인포그래픽",
            "b1_mindmap": "예시 정답 · 마인드맵 (교과서에 없는 의식주·통신 가지까지 만듦 → 원문 확인)",
            "b2_mindmap_design": "예시 정답 · 나노바나나로 다듬은 마인드맵 (글자 깨짐 있음 → 확인 후 사용)",
            "b2_character": "예시 정답 · 캐릭터 세트 (단발머리·파란 셔츠)",
            "b3_outline": "예시 정답 · 개요 — '의식주·통신은 자료에 없다'며 교통 중심으로 짬",
            "b3_slide": "예시 정답 · 캐릭터 세트를 소스로 넣어 만든 슬라이드 (오른쪽 아래 단색 유지)",
            "b4_edit": "슬라이드 [수정] → 'N번 슬라이드 변경'에 4단계 프롬프트",
            "b4_result": "예시 정답 · 제목 '옛날의 교통수단', 가마 설명 추가 (수정본은 (2)로 따로 저장)",
            "b5_style_minimal": "예시 정답 · 미니멀 카드 스타일 (세로)",
            "goe_privacy": "goe 계정 Gemini 화면 아래 안내: 채팅은 Gemini 모델 개선에 사용되지 않음"}
EXTRA = {("06", 1): ["b1_video_dialog", "b1_video_explain", "b1_video_short", "b1_infographic", "b1_mindmap"],
         ("06", 2): ["b2_mindmap_design", "b2_character"],
         ("06", 3): ["b3_outline", "b3_slide"],
         ("06", 4): ["b4_edit", "b4_result"],
         ("06", 5): ["b5_style_minimal"]}
EXNOTE = {("06", 1): "예시 정답(goe 계정, 2026. 10. 13.): 동영상은 기본값이 <strong>짧은 버전(세로)</strong>이에요 — 가로 설명 영상은 <strong>설명 동영상</strong>을 골라요. 설명 동영상은 10분 남짓 걸렸어요. 마인드맵은 교과서(교통 단원)에 없는 <strong>의식주·통신 가지</strong>까지 만들었어요 — 프롬프트가 요구하면 작업실 결과물은 소스 밖 내용을 채울 수 있어요.",
          ("06", 2): "예시 정답: Gemini 앱 <strong>임시 채팅</strong>에서 만들었어요(대화 기록 안 남음). 다듬은 마인드맵은 보기 좋지만 <strong>글자가 깨진 곳</strong>이 있어요. 캐릭터 세트는 3×3 칸이 정확하지 않을 때가 있어 다시 요청해요.",
          ("06", 3): "예시 정답: 채팅 개요는 <strong>'의식주·통신 사례는 자료에 직접 다루어지지 않아 교통 중심으로 짰다'</strong>고 밝혔어요 — 근거로 답하는 노트북의 모습. 캐릭터 세트 PNG를 소스로 올리고 ②를 넣으니 모든 장에 그 캐릭터가 나오고 오른쪽 아래 단색도 지켜졌어요(덱 제목만 영어로 붙어 바꿨어요).",
          ("06", 4): "예시 정답: 슬라이드 보기에서 <strong>[수정]</strong> → 고칠 장을 고르고 프롬프트 → <strong>수정된 자료 생성</strong>. 몇 분 뒤 수정본이 <strong>(2)</strong>로 따로 생겨요.",
          ("06", 5): "예시 정답: 교과서의 '교통 문제점과 해결 노력'을 미니멀 카드(세로)로 만든 결과예요."}


def photo(key):
    cap = SHOT_CAP.get(key, key)
    if os.path.exists(os.path.join(SHOT_DIR, key + ".png")):
        src = f"../assets/notebook/shot/{key}.png"
        return (f'<figure class="guide-shot"><a href="{src}" target="_blank" rel="noopener"><img src="{src}" alt="{E(cap)}" loading="lazy" /></a>'
                f'<figcaption class="shot-cap">{E(cap)}</figcaption></figure>')
    return f'<figure class="guide-shot shot-empty"><div>캡처 예정</div><figcaption class="shot-cap">{E(cap)}</figcaption></figure>'


def prompt_row(text):
    """text 또는 (이름, text) — 이름은 복사되지 않는 머리표(pcat)"""
    cat = ""
    if isinstance(text, tuple):
        cat, text = text
        cat = f'<span class="pcat">{E(cat)}</span>'
    return (f'<div class="prompt-row"><div class="pbody">{cat}<span class="ptext">{E(text)}</span></div>'
            f'<button class="prompt-copy" type="button">복사</button></div>')


def badges(no):
    i = INFO[no]
    return (f'<span class="pbadges"><span class="pb pb-lv {LVCLS[i["level"]]}">{E(i["level"])}</span>'
            f'<span class="pb pb-mode"><i>소스</i>{E(i["src"])}</span>'
            f'<span class="pb"><i>시간</i>{E(i["time"] if ("안팎" in i["time"] or "이상" in i["time"]) else "약 " + i["time"])}</span></span>')


def plain(t):
    return re.sub("<br />", " ", t)


# (파일, 제목, (탭 번호, 탭 이름))
PNO = {f"p{x[0]}.html": x[0] for x in P}
DISP = lambda no: "기본" if no == "06" else no
PAGES = ([("concept.html", "근거로 답하는 AI란?", ("1", "개념")), ("start.html", "처음 준비", ("2", "준비"))]
         + [(f"p{no}.html", plain(t), (DISP(no), nav)) for no, _, t, nav, _, _ in P]
         + [("wrap.html", "정리 · 내일부터 이렇게", ("✓", "정리"))])
GROUP = {"concept.html": "개념", "start.html": "처음 준비", "wrap.html": "정리"}

HEAD = '''<!DOCTYPE html>
<html lang="ko">
<head>
  <meta charset="UTF-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1.0" />
  <meta name="color-scheme" content="light" />
  <title>{title}</title>
  <meta name="description" content="지어내지 않는 AI, 근거를 대는 AI — Gemini 노트북으로 학교 규정·매뉴얼 업무 실습" />
  <link rel="preconnect" href="https://fonts.googleapis.com" />
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin />
  <link href="https://fonts.googleapis.com/css2?family=Bebas+Neue&family=Black+Han+Sans&display=swap" rel="stylesheet" />
  <link rel="stylesheet" as="style" crossorigin href="https://cdn.jsdelivr.net/gh/orioncactus/pretendard@v1.3.9/dist/web/static/pretendard.min.css" />
  <link rel="stylesheet" href="styles.css" />
  <link rel="stylesheet" href="extra.css" />
  <link rel="stylesheet" href="nb.css" />
</head>
<body>
'''


def topbar(current):
    def tab(f, num, name):
        on = f == current
        cur = " aria-current=page" if on else ""
        if f in PNO:
            lv = INFO[PNO[f]]["level"]
            return (f'<a class="tab tab-p {LVCLS[lv]}{" on" if on else ""}" href="{f}" title="실습 {E(num)} · {E(name)} ({E(lv)})"{cur}>'
                    f'<span class="tab-no">{E(num)}</span><span class="tab-name">{E(name)}</span></a>')
        return (f'<a class="tab{" on" if on else ""}" href="{f}"{cur}>' + (f'<span class="tab-no">{E(num)}</span>' if num else "") + f'{E(name)}</a>')
    tabs = tab("index.html", "", "홈")
    for k, (f, _, n) in enumerate(PAGES):
        if f in PNO and (k == 0 or PAGES[k - 1][0] not in PNO):
            tabs += '<span class="tab-group" aria-hidden="true"><span class="tab-no">3</span>실습</span>'
        tabs += tab(f, n[0], n[1])
    return f'''  <div class="utility-bar">
    <div class="shell">
      <a class="caption-sm" href="start.html">처음 준비</a>
      <a class="caption-sm deck-tab-pdf" href="{ZIP_HREF}" download>실습 자료 zip ↓</a>
      <a class="deck-tab" href="../index.html">AI 콘텐츠 홈 &#8599;</a>
      <a class="deck-tab deck-tab-padlet" href="https://notebook.google.com/" target="_blank" rel="noopener">노트북 열기 &#8599;</a>
      <button class="deck-tab addr-open" type="button" title="사이트 주소와 QR 크게 보기">주소 · QR</button>
    </div>
  </div>
  <header class="primary-nav">
    <div class="shell">
      <a class="brand" href="index.html"><span class="swoosh">노트북 LM</span> 총정리 편</a>
    </div>
    <nav class="tabs" aria-label="목차"><div class="shell tabs-row">{tabs}</div></nav>
  </header>
'''


import qrcode as _qr  # noqa: E402


def _qrsvg(text):
    q = _qr.QRCode(border=2); q.add_data(text); q.make(); m = q.get_matrix(); n = len(m)
    r = "".join(f'<rect x="{x}" y="{y}" width="1" height="1"/>' for y, row in enumerate(m) for x, v in enumerate(row) if v)
    return f'<svg viewBox="0 0 {n} {n}" role="img" aria-label="QR: {SITE_URL}" shape-rendering="crispEdges"><rect width="{n}" height="{n}" fill="#fff"/><g fill="#111">{r}</g></svg>'


FOOT = f'''
  <div class="addr" id="addr" role="dialog" aria-label="사이트 주소와 QR" hidden>
    <button class="addr-x" type="button" aria-label="닫기">✕</button>
    <div class="addr-box"><p class="addr-k">사이트 주소</p><p class="addr-url">classroomaicontents.vercel.app/notebook</p>
    <div class="addr-qr">{_qrsvg(SITE_URL)}</div><p class="addr-hint">휴대폰 카메라로 찍어도 열려요 · Esc로 닫기</p></div>
  </div>
  <footer class="site-footer shell">
    <div class="footer-fine utility-xs">
      <span>{NAME} · Gemini 노트북 업무 실습</span>
      <span class="grow">실습 자료 속 학교·사람 이름은 실습용이에요. 화면과 한도는 2026. 10. goe 학교 계정 기준이라 업데이트로 바뀔 수 있어요.</span>
    </div>
  </footer>
  <div class="toast" id="toast" role="status" aria-live="polite"></div>
  <script src="site.js"></script>
</body>
</html>
'''


def page(fname, kicker, h2, lead, tile, no, body, extra=""):
    i = [f for f, _, _ in PAGES].index(fname)
    title = PAGES[i][1]
    prev = PAGES[i - 1] if i > 0 else None
    nxt = PAGES[i + 1] if i + 1 < len(PAGES) else None
    pn = ('<nav class="pager" aria-label="이전 다음">'
          + (f'<a class="btn btn-secondary" href="{prev[0]}">← {E(prev[1])}</a>' if prev else "<span></span>")
          + '<a class="btn btn-primary" href="index.html">홈</a>'
          + (f'<a class="btn btn-secondary" href="{nxt[0]}">{E(nxt[1])} →</a>' if nxt else "<span></span>") + "</nav>")
    h = (HEAD.format(title=E(title) + " · " + NAME) + topbar(fname)
         + f'''  <main class="shell page" id="top">
    <p class="crumb"><a class="btn btn-secondary btn-sm" href="index.html">← 홈</a><span class="here">지금 여기 · {GROUP.get(fname, "실습")} › <strong>{"실습 " if fname in PNO else ""}{E(PAGES[i][2][0])} {E(PAGES[i][2][1])}</strong><span class="pos">{i+1} / {len(PAGES)}</span></span></p>
    <section class="lecture open" aria-label="{E(title)}">
      <div class="lecture-row">
        <div class="lecture-media {tile}"><span class="lecture-no">{no}</span></div>
        <div class="lecture-copy">
          <p class="lecture-kicker">{kicker}</p>
          <h2>{h2}</h2>
          <p class="lead">{lead}</p>{extra}
        </div>
      </div>
      <div class="lecture-detail">
        <div class="lecture-detail-inner">{body}
        </div>
      </div>
    </section>
    {pn}
  </main>
''' + FOOT)
    open(os.path.join(OUT, fname), "w", encoding="utf-8").write(h)


def key_grid(items, hz=False):
    return (f'<div class="key-grid{" hz" if hz else ""}">'
            + "".join(f'<div class="key-item"><span class="key-label">{a}</span><p class="key-text">{b}</p></div>' for a, b in items) + '</div>')


def mix(tag, h3, lead, inner=""):
    return f'<div class="guide-mix"><p class="mix-highlight">{tag}</p><h3>{h3}</h3>' + (f'<p class="mix-lead">{lead}</p>' if lead else "") + inner + '</div>'


def table(head, rows, cls="cmp"):
    return (f'<div class="cmp-wrap"><table class="{cls}"><thead><tr>' + "".join(f"<th>{h}</th>" for h in head) + '</tr></thead><tbody>'
            + "".join("<tr>" + "".join((f"<th>{c}</th>" if j == 0 else f"<td>{c}</td>") for j, c in enumerate(r)) + "</tr>" for r in rows)
            + '</tbody></table></div>')


HWP_CALLOUT = ('<div class="hwp-callout"><span class="hwp-big">한/글</span><div><p class="hwp-h">한/글 파일, <strong>변환 없이 그대로</strong> 올라가요</p>'
               '<p>hwp·hwpx 계획서와 서식을 바로 소스로. 엑셀(xlsx)만 안 돼요 → <strong>CSV</strong>나 <strong>구글 시트</strong>로.</p>'
               '<p class="hwp-fmt">pdf · txt · md · docx · csv · pptx · epub · odt · rtf · <b>hwp</b> · <b>hwpx</b> · 이미지 · 오디오 · 영상</p></div></div>')

MSG_FILE = '<span class="hwp-chip">한/글 그대로</span>'

# ------------------------------------------------------------------ 개념
CMP = mix("💬 → 📚 비교", "일반 Gemini와 무엇이 다를까요?",
          "일반 Gemini는 <strong>인터넷 전체</strong>로 그럴듯하게 답하고, 노트북은 <strong>내가 넣은 자료 안에서만</strong> 근거를 대고 답해요.",
          table(["", "일반 Gemini 대화", "Gemini 노트북"], [
              ["답의 근거", "학습한 인터넷 지식", "<b>내가 올린 소스</b>(규정집·지침·매뉴얼)"],
              ["출처", "알기 어려움", "문장마다 <b>[1] [2] 인용</b> → 누르면 원문 위치"],
              ["모르는 것", "지어낼 수 있음", "\"<b>소스에 없습니다</b>\"라고 말함 (실측)"],
              ["쓰임", "아이디어·범용", "<b>업무 전용</b>: 우리 학교 규정·공문 지침에 맞춘 답"],
              ["결과물", "채팅 답", "채팅 + 작업실(슬라이드·인포그래픽·퀴즈·데이터 표·오디오·영상)"],
          ]))
SAFE = ('<div class="guide-key"><h3>업무에 써도 될까요?</h3><p class="key-lead">goe <strong>학교 계정</strong>은 올린 자료와 대화가 AI 학습에 쓰이지 않고 비공개로 유지된다고 안내돼요.</p>'
        + key_grid([("학교 계정", "goe.go.kr로 로그인 — <strong>학습에 안 쓰임</strong>"), ("개인정보", "학생 실명·연락처는 <strong>지우고</strong> 올리기"), ("공유", "공유 링크를 받은 사람은 <strong>소스와 대화를 봐요</strong>")])
        + '<div class="pstep-shots n1">' + photo("goe_privacy") + '</div>'
        + '</div>')
HABIT = ('<div class="guide-key"><h3>할루시네이션 0이 아니라, 확인하는 습관</h3><p class="key-lead">노트북은 지어내는 일을 <strong>크게 줄여요</strong>. 그래도 <strong>숫자·날짜·쪽 번호는 사람이 확인</strong>해요.</p>'
         + key_grid([("채팅 답", "실측에서 <strong>정확</strong> — 설문 평균·학폭 기한·인사 조항"), ("작업실 그림", "인포그래픽 숫자가 <strong>부풀려진</strong> 적 있어요"), ("쪽 번호", "데이터 표의 '근거 쪽'이 <strong>실제와 달랐어요</strong>")])
         + '<p class="key-foot">그래서 이 연수의 규칙: 인용을 눌러 확인한 답만 <strong>[검증]</strong>을 붙여 다시 소스로 올려요.</p></div>')
FOUND = mix("🧪 실측", "goe 학교 계정에서 직접 해 봤어요 (2026. 10. 13.)", "",
            table(["해 본 것", "결과"], [
                ["한/글 hwpx · CSV · md · PDF 올리기", "<b>모두 됨</b> — 노트북 제목도 소스 이름으로 자동"],
                ["엑셀 xlsx 올리기", "<b>안 됨</b> — 섞여 있으면 묶음 전체 거절"],
                ["설문 CSV 평균 (채팅)", "<b>정확</b> 6번 3.27 · 5번 3.46 · 7번 3.53"],
                ["같은 내용 인포그래픽", "그림은 좋지만 상위 점수를 4.2~4.4로 <b>부풀림</b>(실제 4.16)"],
                ["함정 질문: 교직원 주차", "\"자료에 <b>포함되어 있지 않습니다</b>\" + 웹 검색 제안"],
                ["학폭 분리·보고 기한", "<b>24시간 · 48시간</b>, 양식 1-2·1-3 정확"],
                ["띄어쓰기 빠진 인사기준 PDF", "제10조 갑구역 10년·세 자녀 유예 <b>정확</b>"],
                ["데이터 표", "출처 열 자동, 단 '근거 쪽' 숫자는 <b>실제 쪽과 다름</b>"],
            ]))
CONCEPT = CMP + SAFE + HABIT + FOUND

# ------------------------------------------------------------------ 처음 준비
ZIPBOX = mix("📦 실습 자료", "실습 자료는 이것 하나만 받아요",
             "받아서 <strong>바탕화면</strong>에 압축을 풀면 <strong>노트북연수_실습</strong> 폴더가 생겨요. 00~05 실습 파일이 모두 들어 있어요.",
             f'<div class="practice-download row"><a class="btn btn-primary" href="{ZIP_HREF}" download>실습 자료 전체 내려받기 (zip · {ZIP_SIZE}) ↓</a></div>')
LOGIN = mix("🔑 로그인", "학교 계정으로 노트북 열기",
            "크롬에서 <strong>notebook.google.com</strong> → <strong>goe.go.kr 학교 계정</strong>으로 로그인 → <strong>새 노트북</strong>.",
            '<div class="practice-download row"><a class="btn btn-secondary" href="https://notebook.google.com/" target="_blank" rel="noopener">Gemini 노트북 열기 &#8599;</a></div>'
            + '<div class="pstep-shots n1">' + photo("01_home") + '</div>')
THREE = ('<div class="guide-key"><h3>화면은 세 칸</h3><p class="key-lead">왼쪽에 넣고, 가운데서 묻고, 오른쪽에서 만들어요.</p>'
         + key_grid([("자료실 (소스)", "PDF·한/글·CSV·웹·유튜브·드라이브를 <strong>근거로</strong> 넣는 곳"),
                     ("질문창", "소스를 바탕으로 묻고 답하는 곳. 답마다 <strong>인용 번호</strong>"),
                     ("작업실 (스튜디오)", "오디오·슬라이드·동영상·마인드맵·보고서·플래시카드·퀴즈·인포그래픽·<strong>데이터 표</strong>")])
         + '</div>')
LIMIT = ('<div class="guide-key"><h3>무료 하루 한도</h3><p class="key-lead">연수 중에는 <strong>슬라이드 3회</strong>가 가장 빠듯해요. 한 번에 잘 만들도록 프롬프트를 준비했어요.</p>'
         + key_grid([("채팅", "하루 <strong>50회</strong>"), ("슬라이드 · 오디오", "하루 <strong>3회</strong>씩"), ("노트북당 소스", "<strong>50개</strong> (학교 계정은 기관 설정에 따라)")])
         + '<p class="key-foot">한도는 공개 가이드(2026. 8.) 기준이에요. 학교 계정 설정에 따라 다를 수 있어요.</p></div>')
INSTR = mix("🧭 맞춤 지침", "모든 노트북에 같은 지침을",
            "오른쪽 위 <strong>노트북 구성</strong> → 대화 스타일 <strong>맞춤</strong>에 붙여 넣어요.",
            '<div class="prompt-list">' + prompt_row(P[0][5][1][2][0]) + '</div>')
FLOW = mix("⏱ 90분", "오늘의 흐름", "",
           table(["시간", "실습", "결과물"], [
               ["0–10", "00 시작하기 — 일반 Gemini와 비교", "인용 있는 답 vs 없는 답"],
               ["10–28", "01 공문서 — 규칙표·[검증] 소스·틀린 기안문·기안문", "규정 근거가 달린 기안문"],
               ["28–55", "02 엑셀→슬라이드 — 채점·결과 문단·슬라이드·인포그래픽", "운영 결과 보고 슬라이드"],
               ["55–70", "03 내 업무 규정 — A~F 중 하나 + 함정 질문", "\"소스에 없습니다\" 확인"],
               ["70–80", "04 퀴즈 → 데이터 표 → 시트 → 폼", "교직원 연수 퀴즈 폼"],
               ["80–90", "정리 + 05 작업실 더 해 보기(미리 만든 예시) + 06 기본편 실습(과제)", "에이전트 vs 노트북"],
           ]))
START = ZIPBOX + LOGIN + HWP_CALLOUT + mix("📎 올릴 수 있는 형식", "업로드 창에서 확인했어요", "", '<div class="pstep-shots n1">' + photo("03_upload_formats") + '</div>') + THREE + LIMIT + INSTR + FLOW

# ------------------------------------------------------------------ 정리
FEAT = [
    ("소스만 근거로 답·인용 번호·자료에 없으면 없다고 함", "00 · 01 · 03 함정 질문"),
    ("학교 계정은 학습에 안 쓰임·비공개", "개념"),
    ("자료 올리기: PDF·한/글·CSV·웹·유튜브·드라이브·텍스트·사진·mp4", "00 ~ 03"),
    ("웹 검색(빠른/심층 조사)으로 소스 추가", "03 (사람이 고른 것만 들이기)"),
    ("라벨(자동 분류, 한 소스 여러 라벨)", "03"),
    ("맞춤 대화 설정·답변 길이", "00 · 05"),
    ("메모에 저장 → 소스로 변환", "01 ([검증] 규칙)"),
    ("소스 점검(깡통·중복 소스 골라내기)", "03"),
    ("슬라이드 + 스타일 옵션(화살표 &gt;)", "02 · 02b"),
    ("슬라이드 개요 → 캐릭터 세트 → PDF 재소스로 무한 확장", "02b ①~④"),
    ("슬라이드 한 장 고치기", "02b ⑤"),
    ("인포그래픽(10 스타일·방향·세부 정보)", "02 · 02b ⑥ · 03e · 03f"),
    ("마인드맵 + 노드 클릭 → 질문창", "03e · 06"),
    ("마인드맵 → 나노바나나로 다듬기", "05"),
    ("동영상 개요(설명/요약, 스타일, 다운로드)", "05 · 06"),
    ("시네마틱 영상(영어 설정) · 숏폼(9:16)", "05 (소개)"),
    ("오디오 개요(팟캐스트)", "05"),
    ("데이터 표 → 구글 시트 내보내기", "04"),
    ("퀴즈 · 플래시카드(작업실)", "04 · 06"),
    ("채팅 표 → HWPX/Word 변환 제안", "01"),
    ("Gemini 앱 '노트북' 메뉴 연동", "05"),
    ("구글 클래스룸 연동", "05"),
    ("업무 미션: 학교자율시간 연구부장 / 급식 인포그래픽·가정통신문", "03e · 03f"),
    ("기본편: 교과서 PDF 한 파일로 끝내기(1~4단계·한 걸음 더)", "06"),
    ("하루 한도(채팅 50·슬라이드 3·오디오 3)", "처음 준비"),
]
VS = ('<div class="guide-key"><h3>에이전트 AI와 노트북, 언제 무엇을?</h3><p class="key-lead">같은 자료를 <strong>에이전트는 고치고</strong>, <strong>노트북은 근거로 답해요</strong>.</p>'
      + key_grid([("에이전트 (inline AI)", "내 컴퓨터의 한/글·엑셀 <strong>파일을 직접 고쳐</strong> 저장"),
                  ("노트북 (Gemini)", "규정·매뉴얼을 넣고 <strong>근거를 대며 답</strong>, 작업실로 자료 만들기"),
                  ("같이 쓰면", "노트북으로 <strong>근거 확인</strong> → 에이전트로 <strong>양식 채우기</strong>")])
      + '</div>')
TAKE = ('<div class="guide-key"><h3>오늘 가져가는 것</h3>'
        + key_grid([("맞춤 지침", "\"소스에 없으면 없다고\" — <strong>모든 노트북에</strong>"),
                    ("[검증] 규칙", "인용을 눌러 확인한 답만 <strong>다시 소스로</strong>"),
                    ("내 업무 노트북", "규정·지침·서식을 <strong>한/글 그대로</strong> 모아 두기")])
        + '</div>')
CHECK = mix("✅ 빠짐없이", "기능 체크리스트", "참고 영상·자료에 나온 기능이 어느 실습에 있는지예요.",
            table(["기능", "실습"], [[a, b] for a, b in FEAT]))
CREDIT = ('<p class="credit">프롬프트·활용법 출처: 쓰로인훈쌤 「노트북LM 활용 연수(Live)」 · 오빠두엑셀 「노트북 LM 2.0 핵심 기능」 · 강성희 「선생님을 위한 노트북LM 활용법」 · '
          'AI 콘텐츠 노트북LM 섹션. 실습 자료의 학교·사람 이름은 가상이에요.</p>')
WRAP = VS + TAKE + CHECK + CREDIT

# ------------------------------------------------------------------ 생성
os.makedirs(OUT, exist_ok=True)
page("concept.html", "STEP 1 · 개념", "지어내지 않는 AI,<br />근거를 대는 AI",
     "노트북은 내가 넣은 규정·지침·매뉴얼 안에서만 답하고, 답마다 근거를 붙여요.", "tile-notebook", "NB", CONCEPT)
page("start.html", "STEP 2 · 준비", "처음 준비<br />학교 계정으로",
     "실습 자료 받기, 로그인, 화면 세 칸, 한도, 맞춤 지침까지. 여기만 따라 하면 돼요.", "tile-flow", "00", START)

CIRCLE = "①②③④⑤⑥⑦⑧⑨"
for k, (no, folder, title, nav, lead, steps) in enumerate(P):
    out = []
    for j, (gt, gd, prs, keys) in enumerate(steps):
        keys = list(keys) + EXTRA.get((no, j), [])
        if (no, j) in EXNOTE:
            gd = (gd or "") + f'</p><p class="guide-desc ex-answer">✅ {EXNOTE[(no, j)]}'
        shots = "".join(photo(x) for x in keys)
        out.append(f'<div class="pstep"><div class="pstep-head"><span class="guide-no">{j+1}</span><h3>{E(gt)}</h3></div>'
                   + (f'<p class="guide-desc">{gd}</p>' if gd else "")
                   + (f'<div class="prompt-list">{"".join(prompt_row(x) for x in prs)}</div>' if prs else "")
                   + (f'<div class="pstep-shots n{min(len(keys), 3)}">{shots}</div>' if shots else "") + '</div>')
    if no == "03":  # 트랙 허브
        out.insert(3, '<div class="hub-grid track-grid">' + "".join(
            f'<a class="hub-card" href="p{t}.html"><span class="hub-tag">트랙 {E(plain(tt).split()[0])}</span><b>{E(plain(tt))}</b><span class="hub-sub">{E(tl)}</span>{badges(t)}</a>'
            for t, _, tt, _, tl, _ in P if t.startswith("03") and len(t) == 3) + '</div>')
    notes = NOTE.get(no, [])
    tips = ('<div class="ptips" role="note"><p class="ptips-h">막히면 이렇게 · 실측</p><ul>' + "".join(f"<li>{x}</li>" for x in notes) + '</ul></div>') if notes else ""
    body = (f'<p class="pnote">순서: 소스 넣기 → 프롬프트 <strong>[복사]</strong> → 질문창 <strong>Ctrl+V</strong> → 인용 눌러 확인. '
            f'파일은 바탕화면 <strong>노트북연수_실습/{E(folder)}</strong> 폴더에 있어요.</p>' + tips + "".join(out))
    page(f"p{no}.html", f"실습 {DISP(no)}", title, lead, TILES[k % len(TILES)], DISP(no).upper(), body, badges(no))

page("wrap.html", "마무리", "정리 ·<br />내일부터 이렇게", "근거로 답하는 노트북을 내 업무에 붙이는 법.", "tile-flow", "✓", WRAP)


# ------------------------------------------------------------------ 홈
def card(href, tag, name, sub, accent=False, extra=""):
    return (f'<a class="hub-card" href="{href}"><span class="hub-tag{" p" if accent else ""}">{E(tag)}</span>'
            f'<b>{E(name)}</b><span class="hub-sub">{E(sub)}</span>{extra}</a>')


MAIN = [x for x in P if not (x[0].startswith("03") and len(x[0]) == 3)]
TRACK = [x for x in P if x[0].startswith("03") and len(x[0]) == 3]
hero = f'''<section class="hero" aria-label="{NAME}">
      <div class="hero-inner">
        <span class="hero-badge">교원 연수 · Gemini 노트북 · 업무 규정</span>
        <h1 class="display-campaign">지어내지 않는 AI,<br />근거를 대는 AI</h1>
        <p class="hero-sub">규정집·공문 지침·매뉴얼을 넣으면, 그 안에서만 답하고 근거를 붙여요.</p>
        <div class="hero-cta">
          <a class="btn btn-on-image" href="{ZIP_HREF}" download>실습 자료 전체 내려받기 ({ZIP_SIZE}) ↓</a>
          <a class="btn btn-ghost" href="start.html">처음 준비 →</a>
        </div>
      </div>
    </section>

    <section class="goal" aria-label="연수 목표">
      <div class="goal-label">연수 목표</div>
      <div>
        <p class="goal-text">내 업무 규정을 노트북에 넣고, 근거가 달린 답과 자료를 만들어 확인해 쓸 수 있다.</p>
        <div class="goal-tags">
          <span class="goal-tag">① 소스만 근거로</span>
          <span class="goal-tag">② 인용 눌러 확인</span>
          <span class="goal-tag">③ 없으면 \"없다\"</span>
          <span class="goal-tag">한/글 그대로 올리기</span>
        </div>
      </div>
    </section>
    {HWP_CALLOUT}
'''
home_body = (hero
             + '<section class="hub"><h2 class="hub-h"><span>1</span>근거로 답하는 AI란?</h2><div class="hub-grid">'
             + card("concept.html", "개념", "일반 Gemini와 무엇이 다를까", "비교표 · 학교 계정 · 확인하는 습관 · 실측 결과")
             + '</div></section>'
             + '<section class="hub"><h2 class="hub-h"><span>2</span>처음 준비</h2><div class="hub-grid">'
             + card("start.html", "준비", "학교 계정으로 노트북 열기", "화면 세 칸 · 올릴 수 있는 형식 · 하루 한도 · 맞춤 지침")
             + f'<a class="hub-card" href="{ZIP_HREF}" download><span class="hub-tag">실습 자료</span><b>노트북연수_실습.zip ↓</b><span class="hub-sub">{ZIP_SIZE} · 바탕화면에 압축 풀기</span></a>'
             + card("https://notebook.google.com/", "바로 가기", "Gemini 노트북 열기", "goe.go.kr 학교 계정으로", True)
             + '</div></section>'
             + '<section class="hub"><h2 class="hub-h"><span>3</span>실습</h2><p class="hub-lead">페이지마다 단계별 안내 · 프롬프트 [복사] · 실측 메모가 있어요. 기본 → 보통 → 도전 순서예요.</p>'
             + "".join(
                 (f'<h3 class="hub-lv {LVCLS[lv]}">{lv}</h3><div class="hub-grid">'
                  + "".join(card(f"p{no}.html", f"실습 {DISP(no)}", plain(t), l, extra=badges(no)) for no, _, t, _, l, _ in MAIN if INFO[no]["level"] == lv)
                  + '</div>') for lv in LEVELS)
             + '<h3 class="hub-lv lv2">03 내 업무 트랙 (하나 고르기)</h3><div class="hub-grid">'
             + "".join(card(f"p{no}.html", f"트랙 {no[-1].upper()}", plain(t), l, extra=badges(no)) for no, _, t, _, l, _ in TRACK)
             + '</div></section>'
             + '<section class="hub"><h2 class="hub-h"><span>✓</span>정리</h2><div class="hub-grid">'
             + card("wrap.html", "정리", "내일부터 이렇게", "에이전트 vs 노트북 · 가져가는 것 · 기능 체크리스트")
             + card("../index.html", "AI 콘텐츠", "AI 콘텐츠 홈으로", "바이브코딩 · 이미지 · 노트북LM 기초 · PPT · 앱")
             + '</div></section>')
home = HEAD.format(title=NAME + " · Gemini 노트북 업무 실습") + topbar("index.html") + f'  <main class="shell" id="top">\n{home_body}\n  </main>\n' + FOOT
open(os.path.join(OUT, "index.html"), "w", encoding="utf-8").write(home)

missing = sorted({k for _, _, _, _, _, st in P for s in st for k in s[3]} | {"01_home", "03_upload_formats"})
missing = [k for k in missing if not os.path.exists(os.path.join(SHOT_DIR, k + ".png"))]
print("pages:", len(PAGES) + 1, "| 캡처 예정:", " ".join(missing) or "없음")
