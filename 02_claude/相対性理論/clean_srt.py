"""
SRTファイルをクリーンなテキストに変換するスクリプト
使用方法: python3 clean_srt.py <input.srt> <output.txt>
処理内容: タイムスタンプ・番号を除去し、重複テキストを削除して連続した文章にする
"""
import re
import sys

def clean_srt(input_path, output_path):
    with open(input_path, 'r', encoding='utf-8') as f:
        content = f.read()

    # SRTのブロックを解析
    blocks = re.split(r'\n\n+', content.strip())

    lines = []
    prev_text = ""

    for block in blocks:
        block_lines = block.strip().split('\n')
        # 番号行とタイムスタンプ行を除去してテキスト部分を取得
        text_parts = []
        for line in block_lines:
            line = line.strip()
            # 番号のみの行をスキップ
            if re.match(r'^\d+$', line):
                continue
            # タイムスタンプ行をスキップ
            if re.match(r'^\d{2}:\d{2}:\d{2}', line):
                continue
            if line:
                text_parts.append(line)

        text = ' '.join(text_parts)
        if text and text != prev_text:
            lines.append(text)
            prev_text = text

    # 連続するテキストを結合（適度に改行を入れる）
    output_lines = []
    current_paragraph = []

    for i, line in enumerate(lines):
        current_paragraph.append(line)
        # 約10行ごとに段落を区切る
        if len(current_paragraph) >= 10:
            output_lines.append(''.join(current_paragraph))
            current_paragraph = []

    if current_paragraph:
        output_lines.append(''.join(current_paragraph))

    with open(output_path, 'w', encoding='utf-8') as f:
        f.write('\n\n'.join(output_lines))

    print(f"変換完了: {len(lines)}行 → {len(output_lines)}段落")

if __name__ == '__main__':
    input_path = sys.argv[1] if len(sys.argv) > 1 else '/tmp/yobinori_subs/relativity.ja.srt'
    output_path = sys.argv[2] if len(sys.argv) > 2 else '/Users/user/Documents/GitHub/物理学_physics-study/02_claude/相対性理論/文字起こし_生データ.txt'
    clean_srt(input_path, output_path)
