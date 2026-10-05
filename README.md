# 배민진컴퍼니

> 무엇을 만들지 정하는 중입니다.

## CI (GitHub Actions)
`main` 푸시와 모든 PR에서 `.github/workflows/ci.yml`이 자동으로 돌아갑니다.

- **비밀키 유출 검사** — API 키·비밀번호가 실수로 커밋되면 잡아요 (`gitleaks`)
- **빌드 · 테스트 (자동 감지)** — 저장소에 있는 파일을 보고 알아서 돌아요
  - `package.json` 있음 → `npm run lint` / `test` / `build` (있는 것만)
  - `requirements.txt` · `pyproject.toml` 있음 → `pytest`
  - 아무것도 없음 → 건너뜀 (실패 아님)

만들 걸 정하면 코드만 추가하세요. CI는 따로 손대지 않아도 됩니다.
