---
name: visualize-filtering-result
description: filtered_comments_kexaone_kkp.jsonl의 필터링 결과를 전체/일반/타임스탬프 댓글 기준으로 시각화할 때 사용한다.
---

# visualize-filtering-result

`data/filtered_comments_kexaone_kkp.jsonl`의 `is_pass` 값을 집계해
전체 댓글, 일반 댓글, 타임스탬프 댓글 각각의 통과/제거 비율을 막대 차트로 시각화한다.

## 실행 방법

프로젝트 루트에서 아래 명령을 실행한다.

```bash
python3 .claude/skills/visualize-filtering-result/visualize_filtering_result.py
```

## 출력

| 항목 | 내용 |
|---|---|
| 콘솔 | 전체/일반/타임스탬프 댓글의 통과·제거 수 및 비율 |
| 이미지 | `assets/filtering_result.png` (누적 막대 차트) |

### 콘솔 출력 예시

```
=== 필터링 결과 ===
전체 댓글    :   150,000개  통과 72,000 (48.0%)  제거 78,000 (52.0%)
일반 댓글    :   100,000개  통과 50,000 (50.0%)  제거 50,000 (50.0%)
타임스탬프   :    50,000개  통과 22,000 (44.0%)  제거 28,000 (56.0%)
```

## 집계 기준

| filtered 파일 필드 | 의미 |
|---|---|
| `evaluation_result.general_comments[].is_pass` | 일반 댓글 통과 여부 |
| `evaluation_result.timestamp_comments[].is_pass` | 타임스탬프 댓글 통과 여부 |
