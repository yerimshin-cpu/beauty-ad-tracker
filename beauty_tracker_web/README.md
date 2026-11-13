# Indonesia Beauty Ad Tracker — 자동 갱신 웹 버전

이 프로젝트는 공개 Meta 광고 데이터를 Apify로 수집해 GitHub Pages에 표시해. 현재는 기존 테스트 데이터가 포함돼 있고, 연결 후 매일 새 데이터로 갱신돼.

## 최초 설치

1. GitHub에서 새 **Public** 저장소를 만들고 이 ZIP의 **내용물**(`index.html`, `data.json`, `scripts/`, `.github/`, `.nojekyll`)을 저장소 최상위에 업로드해. ZIP 파일 자체만 올리면 안 돼. `.github/workflows/update.yml` 경로가 유지돼야 해.
2. GitHub 저장소 **Settings → Pages → Build and deployment → Deploy from a branch → main / (root) → Save**를 선택해. 수 분 후 `https://사용자명.github.io/저장소명/` 주소가 만들어져.
3. Apify 콘솔에서 **Settings → API & Integrations**에서 API 토큰을 확인해. 이 토큰을 채팅, 저장소 코드, 공개 파일에 절대 적지 마.
4. GitHub 저장소 **Settings → Secrets and variables → Actions → New repository secret**에서 이름을 `APIFY_TOKEN`으로 하고 토큰 값을 저장해.
5. GitHub 저장소 **Actions → Refresh Meta Ads → Run workflow**로 첫 테스트를 실행해. 실행 성공 후 `data.json`이 바뀌는지 확인하고 웹 페이지를 새로고침해.
6. 이후 GitHub Actions가 매일 **한국 시간 오전 10시(UTC 01:00)** 예약 실행을 시도해. GitHub 일정 실행은 지연되거나 건너뛸 수 있어.

## 변경할 곳

- 수집 브랜드 및 브랜드당 목표량: `scripts/update.py`의 `SEARCH`, `maxAds`.
- 대시보드 필터: `index.html`의 `<select id="brand">`와 `function brand(r)`를 **같이** 수정해야 해. 초기 화면은 SKIN1004 / Skintific 필터 중심이야.
- Apify Actor: 현재 성공했던 Actor ID `juh6OwzcsI0sdSFsn`으로 설정. Actor가 다른 입력 규격으로 바뀌면 코드 수정이 필요해.

## 유의사항

- **공개 사이트**야. 광고 데이터는 누구나 볼 수 있어. 회사 내부 메모, 사내 지표, API 토큰은 절대 올리지 마.
- `RESIDENTIAL` 프록시와 광고 수집은 **유료 사용량**이 발생할 수 있어. 매일 7개 브랜드 x 30개 목표로 실행하기 전 Apify 가격·사용 한도 확인해. 이 코드에는 실행당 비용 상한이 구현되어 있지 않아.
- `maxAds`의 정확한 적용 범위는 Actor 구현에 따라 달라질 수 있어.
- Meta의 이미지 URL은 만료될 수 있어. 원본 광고 링크를 함께 제공하지만, 이미지 영구 보존 기능은 아직 없어.
- 광고의 게재 기간은 성과를 보증하지 않아. 실제 ROAS/전환율은 경쟁사 공개 데이터로 알 수 없어.
- 현재 대시보드는 **규칙 기반 소구점 태깅**이며 생성형 AI의 자동 전략 분석은 아직 아니야.
- Apify 작업이 실패하거나 결과가 비면 이전 `data.json`을 유지하도록 했어.
