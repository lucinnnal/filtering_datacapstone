import json
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
from matplotlib import rcParams

OUTPUT_PATH = 'assets/filtering_result.png'
FILTERED_PATH = 'data/filtered_comments_kexaone_kkp.jsonl'


def load_stats(path: str) -> dict:
    """filtered_comments JSONL에서 전체/통과 댓글 수를 집계한다.

    Args:
        path: filtered_comments_kexaone_kkp.jsonl 경로.

    Returns:
        {
            'general_total': int,
            'general_pass': int,
            'timestamp_total': int,
            'timestamp_pass': int,
        }
    """
    general_total = general_pass = 0
    timestamp_total = timestamp_pass = 0

    with open(path) as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            obj = json.loads(line)
            er = obj.get('evaluation_result', {})
            for c in er.get('general_comments', []):
                general_total += 1
                if c.get('is_pass'):
                    general_pass += 1
            for c in er.get('timestamp_comments', []):
                timestamp_total += 1
                if c.get('is_pass'):
                    timestamp_pass += 1

    return {
        'general_total': general_total,
        'general_pass': general_pass,
        'timestamp_total': timestamp_total,
        'timestamp_pass': timestamp_pass,
    }


def draw_chart(stats: dict, output_path: str) -> None:
    """필터링 결과를 막대 차트로 저장한다.

    Args:
        stats: load_stats() 결과.
        output_path: 저장할 이미지 경로.
    """
    rcParams['font.family'] = 'AppleGothic'
    rcParams['axes.unicode_minus'] = False

    total_total = stats['general_total'] + stats['timestamp_total']
    total_pass = stats['general_pass'] + stats['timestamp_pass']
    total_fail = total_total - total_pass

    g_pass = stats['general_pass']
    g_fail = stats['general_total'] - g_pass

    t_pass = stats['timestamp_pass']
    t_fail = stats['timestamp_total'] - t_pass

    labels = ['전체 댓글', '일반 댓글', '타임스탬프 댓글']
    passes = [total_pass, g_pass, t_pass]
    fails = [total_fail, g_fail, t_fail]
    totals = [total_total, stats['general_total'], stats['timestamp_total']]

    COLOR_PASS = '#4C9BE8'
    COLOR_FAIL = '#E8A04C'

    fig, ax = plt.subplots(figsize=(9, 5))
    x = range(len(labels))
    bar_width = 0.5

    bars_fail = ax.bar(x, fails, bar_width, label='필터링 제거', color=COLOR_FAIL)
    bars_pass = ax.bar(x, passes, bar_width, bottom=fails, label='통과', color=COLOR_PASS)

    for i, (p, f, total) in enumerate(zip(passes, fails, totals)):
        pass_pct = p / total * 100 if total else 0
        fail_pct = f / total * 100 if total else 0
        # 제거 영역 라벨
        if f > 0:
            ax.text(i, f / 2, f'{f:,}\n({fail_pct:.1f}%)',
                    ha='center', va='center', fontsize=9, color='white', fontweight='bold')
        # 통과 영역 라벨
        if p > 0:
            ax.text(i, f + p / 2, f'{p:,}\n({pass_pct:.1f}%)',
                    ha='center', va='center', fontsize=9, color='white', fontweight='bold')
        # 합계 라벨 (막대 위)
        ax.text(i, total + total * 0.01, f'합계 {total:,}',
                ha='center', va='bottom', fontsize=9, color='#333333')

    ax.set_xticks(list(x))
    ax.set_xticklabels(labels, fontsize=11)
    ax.set_ylabel('댓글 수', fontsize=10)
    ax.set_title('K-EXAONE 필터링 결과', fontsize=14, fontweight='bold', pad=16)
    ax.legend(handles=[
        mpatches.Patch(color=COLOR_PASS, label='통과'),
        mpatches.Patch(color=COLOR_FAIL, label='필터링 제거'),
    ], loc='upper right', fontsize=10)
    ax.set_ylim(0, max(totals) * 1.12)
    ax.yaxis.set_major_formatter(plt.FuncFormatter(lambda v, _: f'{int(v):,}'))
    ax.spines[['top', 'right']].set_visible(False)

    plt.tight_layout()
    plt.savefig(output_path, dpi=150, bbox_inches='tight')
    plt.close()


if __name__ == '__main__':
    stats = load_stats(FILTERED_PATH)

    total_total = stats['general_total'] + stats['timestamp_total']
    total_pass = stats['general_pass'] + stats['timestamp_pass']

    print("=== 필터링 결과 ===")
    print(f"전체 댓글    : {total_total:>8,}개  통과 {total_pass:,} ({total_pass/total_total*100:.1f}%)  제거 {total_total-total_pass:,} ({(total_total-total_pass)/total_total*100:.1f}%)")
    print(f"일반 댓글    : {stats['general_total']:>8,}개  통과 {stats['general_pass']:,} ({stats['general_pass']/stats['general_total']*100:.1f}%)  제거 {stats['general_total']-stats['general_pass']:,} ({(stats['general_total']-stats['general_pass'])/stats['general_total']*100:.1f}%)")
    print(f"타임스탬프   : {stats['timestamp_total']:>8,}개  통과 {stats['timestamp_pass']:,} ({stats['timestamp_pass']/stats['timestamp_total']*100:.1f}%)  제거 {stats['timestamp_total']-stats['timestamp_pass']:,} ({(stats['timestamp_total']-stats['timestamp_pass'])/stats['timestamp_total']*100:.1f}%)")

    draw_chart(stats, OUTPUT_PATH)
    print(f"\n차트 저장 완료: {OUTPUT_PATH}")
