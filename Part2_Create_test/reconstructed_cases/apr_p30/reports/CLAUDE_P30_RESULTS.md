# Claude API p30 비교

|실제 모델|테스트 PASS|패치 검사 통과|제출+패치 검사 통과|비용 USD|
|---|---:|---:|---:|---:|
|claude-sonnet-5-5|20/30|20/30|20/30|0.8703|
|claude-haiku-4-5-20251001|19/30|19/30|19/30|2.9302|

같은 30개 p case, case당 기존에 선정한 Qiskit 버전 하나, ZIP의 실제 DefaultAgent 2.4.6, 40단계·$1 제한(마지막 응답 비용 초과 가능)·1200초 제한. 두 모델은 같은 입력 및 스크립트 오류 피드백을 사용했다. 최종 기존 테스트는 제출/종료 후 실행했으며 수정 피드백으로 사용하지 않았다.

MCP 미사용. Docker가 실행 중이지 않아 제한된 로컬 프로세스와 명령 검사로 실행했다. 이는 컨테이너 격리가 아니므로 학습 데이터 유출까지 포함한 무누출을 증명하지 않는다. Agent 입력에서 fixed.py, test.py, Codex 패치, 테스트에서 유래한 intent 요약은 제외했다. API 키는 worker와 로그에 전달하지 않았다.

Haiku 5.0은 API 목록에 없어 사용자의 승인에 따라 Haiku 4.5로 대체했다. 폴더 haiku5p30은 요청된 경로명을 유지한다. 이전 Codex 실행은 다른 루프 및 테스트 피드백을 사용했으므로 모델만 바꾼 직접 비교가 아니다.

입력/명령/대화/패치/검증 근거는 각 runs 폴더에 저장했다. CSV의 generated fix는 테스트 결과, repaired는 기준 유효성 및 패치 감사까지 통과한 결과, strict_success는 agent 제출까지 완료한 결과다. 실행기 확인용 issue_036 pilot은 명령 검사 보정 후 pipeline_smoke에 보존하고 본 실험에서 새로 실행했다. 본 실험 비용과 pilot 비용은 비교 CSV에 별도 기록했다.

Sonnet은 30개 모두 제출했고 Haiku는 29개를 제출했다. Haiku issue_436은 buggy.py를 삭제한 상태로 40단계 제한에 도달했다. 삭제된 작업 파일은 복원하지 않았으며 빈 patched.py와 candidate_missing=true로 실패를 기록했다.

최종 검증에서 API 생성 코드의 LF/CRLF를 바꾸지 않도록 스냅샷 바이트를 그대로 보존했다. 이 검증 저장 변경은 모든 agent 루프가 끝난 뒤 적용했고, 기존 adapter.py 사본과 변경 함수/전후 해시/시각을 validation_audit/receipt.json에 보존했다. Agent 실행 환경 함수는 변경하지 않았다.

본 실험의 API 호출 수는 Sonnet 103회(평균 3.43), Haiku 378회(평균 12.6)였다. 공개 단가와 응답 토큰 사용량으로 계산한 비용은 확인용 pilot을 포함해 총 약 $3.86이다.

명령 검사 제한: Haiku issue_021_se의 자기 workspace 절대경로로 cd하는 명령과 issue_032_se의 출력 문자열 "Script runs"가 runs 토큰 검사에 걸려 차단됐다. 두 명령은 기존 정답·테스트·다른 실행 결과를 읽는 명령이 아니었다. 이 오차를 포함한 실제 실행 결과이며, 평가 후 agent를 다시 실행하거나 후보를 수정하지 않았다.

최종 감사: 두 실행 60개 case의 원본/테스트 불변성, 실제 API 모델·토큰 비용·대화·코드 해시, 전체 agent 종료 후 테스트 실행을 확인했다. 오류 0건으로 통과했으며, 검증 저장 보정 2건과 무해한 명령 차단 2건은 경고로 기록했다. 이 감사는 학습 데이터 중복이나 휴리스틱 명령 검사 우회를 배제하는 증명이 아니다.

단가 근거(100만 토큰 기준): [Sonnet 5.5 공식 문서](https://platform.claude.com/docs/en/models/sonnet-5-5/overview)의 입력 $2·출력 $10, [Haiku 4.5 공식 문서](https://platform.claude.com/docs/en/models/haiku-4-5/overview)의 입력 $1·출력 $5를 사용했다.
