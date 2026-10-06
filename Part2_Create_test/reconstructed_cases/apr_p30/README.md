# Qiskit APR: p case 30개 적용

첨부 `qiskit_apr.zip`의 APR 흐름은 이 데이터셋에 적용 가능하다. 원본의 `case_XXX`/CSV 입력을 현재 `issue_XXX`/p-case 검증 이력에 연결하는 어댑터가 필요하며, 원본의 단순 실행 성공 판정을 기존 `test.py`의 의도 검증으로 강화했다.

표와 CSV의 이름은 `buggy`(기존 buggy.py), `fix`(기존 fixed.py), `generated fix`(Codex 생성 patched.py)다. 실행 이력 JSON의 내부 키 `original/reference/candidate`는 같은 세 대상을 가리키며, 기존 감사 기록과의 호환성을 위해 유지한다.

이 실행은 **Codex 엔진 / MCP 비활성 / 로컬 버전별 실행**이다. 원본 `mini-swe-agent` 또는 Anthropic 모델을 실행한 결과와 동일한 실험으로 취급하면 안 된다. 원본의 bash 전용 도구 형식, 종료 sentinel, 40-step/$1/1200초 제한을 Codex 세션에 적용하지 않았다. 개별 Python 프로세스의 제한 시간은 120초다.

## 범위와 선정

`test_validation/consolidated_data.json`, `consolidated_runs.json`, `repair01/results.json`을 병합하고 원본 workbook 행 순서로 p case 30개를 선정했다. 현재 `fixed.py` 및 `test.py` SHA256가 검증 이력과 일치하는 가장 최신 통과 버전을 case마다 하나 사용했다. `issue_018_se`는 기준 수정본에서도 네이티브 Aer 충돌이 기록되어 제외했다. 전체 버전 조합을 수행한 실험은 아니다.

| Qiskit 배포 버전 | Python | Case 수 |
|---|---|---:|
| 0.25.3 | 3.9.25 | 6 |
| 0.46.3 | 3.11.15 | 12 |
| 2.5.0 | 3.12.13 | 12 |

오래된 Qiskit에서는 `qiskit.__version__`이 Terra 버전을 나타낼 수 있으므로 배포 버전은 `importlib.metadata.version('qiskit')`로 확인한다.

## 실제 흐름

1. 정확히 30개 선정, 원본 및 테스트 해시 고정.
2. `original_question.txt`의 `Question:` 구간만 추출. Category/Winner, 정답 설명 및 fixed 코드는 모델 입력에서 제외.
3. 원본 복사본과 질문을 별도 작업공간에 제공하고, 고정 버전에서 오류 재현.
4. Codex가 원인을 분석하여 `workspace/buggy.py`만 수정하고 스크립트를 재실행.
5. 별도 검증기가 변경하지 않은 기존 테스트를 `MUT`로 원본·기준 수정본·후보에 각각 실행.
6. 원본 실패, 기준 통과, 후보 통과를 확인하고 diff·실행 로그·trajectory·해시 저장.

사전 조사에서 정답 설명에 노출된 에이전트는 수리에 투입하지 않았다. 첫 20개 수리 작업은 사전 조사 내용을 상속하지 않는 새 에이전트가 수행했다. 마지막 10개를 수리한 주 에이전트는 해당 case의 정답 또는 테스트 소스를 읽지 않았다. 공개 SDK 소스·공식 문서는 참고할 수 있다. 고정된 모델 입력에 포함된 의도 요약은 기존 검증 메타데이터에서 가져왔다.

정답 소스·해설 노출을 피한 것과 test 정보 노출이 전혀 없는 것은 다르다. 061/096/1035/189/453은 테스트 실패 진단을 수리에 사용했으므로 평가 테스트는 엄격한 held-out 테스트가 아니다. 이 실행을 zero-leakage blind 평가로 취급하지 않는다.

## 검증과 산출물

- `runs/codex_p30/manifest.json`: 30개 선정, 원본 해시 및 원본 ZIP 코드의 출처.
- `runs/codex_p30/applicability.json`: ZIP SHA256, 적용 방식 및 제한사항.
- `runs/codex_p30/baseline_summary.json`: 새 baseline 30개. 원본 28 ERROR/2 FAIL, 기준 30 PASS.
- `runs/codex_p30/summary.json` 및 `summary.csv`: 최종 실제 실행 결과.
- `runs/codex_p30/audit/first_full_validation`: 최초 전체 검증 26/30 결과와 당시 실패 후보 보존.
- `runs/codex_p30/tasks/<case>/`: `original.py`, `patched.py`, `patch.diff`, `traj.json`, `result.json`, 실행 로그.
- `runs/codex_p30/dependency_support.json`: 로컬로 복사한 보조 의존성 파일 해시.
- `upstream/`: ZIP에서 가져온 실행 코드 및 설정. ZIP의 가상환경·결과·비밀정보는 복사하지 않았다.

성공 판정에는 실제 unittest가 1개 이상 실행되고 skip 없이 통과해야 한다. 문법 오류, 변경 없음, 추가된 광범위 예외 처리, 대부분의 코드 삭제는 성공으로 집계하지 않는다. 원본 source, 원본 test, 검증기 test 복사본의 변경도 거부한다. 어댑터 계약 테스트 8개가 통과했다.

validation의 주요 판정은 이미 우리가 만든 각 case의 기존 `test.py`다. `validator/test.py`는 바이트 단위 복사본이며, 실행 전후 SHA256로 동일성을 확인한다. 새 테스트를 생성하거나 기존 테스트를 패치에 맞춰 수정하지 않았다. 원본 ZIP의 `plausible = script exit 0`/기준 stdout 비교는 이 어댑터의 성공 판정에 사용하지 않는다.

최초 전체 검증 이후 061/096/1035/189를 검증 피드백으로 수정했다. 453도 전체 검증 전 파일럿에서 helper API 및 inplace 반환 규약을 피드백으로 보완했다. 이를 한 번의 blind 수리 성공률로 해석하면 안 된다.

## 다시 검증

이 폴더에서 다음 명령으로 저장된 후보 30개를 재검증할 수 있다. API 키는 필요 없다.

```powershell
python -B adapter.py validate --workers 3
python -B -m unittest test_adapter -v
```

특정 후보만 다시 검증할 때는 `--cases issue_061 issue_096`처럼 지정한다. 별도 부분 결과 파일을 작성한다. `prepare`는 기존 manifest와 선택이 일치하면 패치를 유지하며, manifest가 없는 비어 있지 않은 run 폴더에서는 덮어쓰기를 거부한다.

## 해석의 한계

로컬 실행은 작업 디렉터리 및 runtime/home 파일을 격리하지만 OS 보안 sandbox가 아니다. 실제 MCP 호출은 없었으며 원본 MCP 환경의 손상된 Python 경로도 이 실행에서 사용하지 않았다. 보조 의존성 파일 해시를 기록했지만 모든 전이 의존성의 lockfile을 만든 것은 아니다.

기존 테스트 통과는 그 테스트가 검사하는 동작에 대한 근거다. 모든 입력에 대한 정확성이나 원 질문의 모든 조건 충족을 보장하지 않는다. 특히 009는 SABRE를 사용하여 GHZ 회로를 올바르게 컴파일했지만, 원 질문의 **CSPLayout 사용**까지 해결한 결과는 아니다. 453의 재사용 helper는 기존 ancilla가 깨끗한 상태라는 호출자 전제가 있다.

원래 `buggy.py`, `fixed.py`, `test.py`는 수정하지 않았다. 검토 가능한 후보는 이 폴더의 run 산출물에만 저장했다.
