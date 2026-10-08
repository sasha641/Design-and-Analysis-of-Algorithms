import math
import time

import streamlit as st

st.set_page_config(page_title="Binary Search Simulator", page_icon="🔍", layout="wide")

DEFAULT_ARRAY = "2, 5, 8, 12, 16, 23, 38, 56, 72, 91"
MAX_ITEMS = 30
SPEEDS = {"Slow": 1.6, "Medium": 1.0, "Fast": 0.45}

st.markdown(
    """
<style>
@import url('https://fonts.googleapis.com/css2?family=DM+Mono:wght@400;500&family=DM+Sans:wght@400;500;700&family=Fraunces:ital,opsz,wght@0,9..144,600;1,9..144,500&display=swap');

html, body, [class*="css"], .stApp { font-family: 'DM Sans', system-ui, sans-serif; color: #34303a; }
#MainMenu, footer { visibility: hidden; }
.block-container { padding-top: 2.2rem; max-width: 1150px; }

.hero { text-align: center; padding: 6px 0 22px; border-bottom: 2px dotted #e7a7b6; margin-bottom: 26px; }
.hero .stamp { display: inline-block; font-family: 'DM Mono', monospace; font-size: 12px; letter-spacing: .18em;
  text-transform: uppercase; background: #e1ecdf; color: #4b6a50; border: 1.5px dashed #7c9a80;
  border-radius: 999px; padding: 4px 16px; transform: rotate(-2deg); }
.hero h1 { font-family: 'Fraunces', Georgia, serif; font-weight: 600; font-size: 40px; margin: 14px 0 6px; line-height: 1.15; }
.hero p { color: #6d6672; margin: 0 auto; max-width: 620px; font-size: 16px; }

.label { font-family: 'DM Mono', monospace; font-size: 12px; letter-spacing: .14em; text-transform: uppercase; color: #b04e68; margin: 0 0 8px; }

.card { background: #fffafb; border: 1.5px dashed #e7a7b6; border-radius: 18px; padding: 16px 20px; margin: 14px 0; }
.card p, .card li { font-size: 14.5px; line-height: 1.6; margin: 3px 0; }
.card ul { padding-left: 18px; margin: 4px 0; }

.stage { background: #fff; border: 1.5px solid #f0e4e8; border-radius: 18px; padding: 20px 16px 12px; min-height: 150px; }
.row { display: flex; flex-wrap: wrap; gap: 8px; justify-content: center; }
.cell { text-align: center; min-width: 54px; }
.box { padding: 14px 8px; border-radius: 12px; font-weight: 700; font-size: 18px; border: 2px solid transparent; transition: all .2s; }
.box.out { background: #f4f1f3; color: #b5afb9; }
.box.active { background: #e1ecdf; color: #34303a; border-color: #7c9a80; }
.box.mid { background: #b04e68; color: #fff; border-color: #b04e68; transform: translateY(-4px); box-shadow: 0 6px 14px rgba(176,78,104,.28); }
.box.found { background: #4b6a50; color: #fff; border-color: #4b6a50; transform: translateY(-4px); box-shadow: 0 6px 14px rgba(75,106,80,.3); }
.idx { font-family: 'DM Mono', monospace; font-size: 11px; color: #9a94a0; margin-top: 6px; }
.ptr { font-family: 'DM Mono', monospace; font-size: 12px; font-weight: 500; color: #b04e68; height: 18px; letter-spacing: .08em; }

.legend { display: flex; flex-wrap: wrap; gap: 14px; justify-content: center; margin-top: 14px; font-size: 13px; color: #6d6672; }
.legend span::before { content: ''; display: inline-block; width: 12px; height: 12px; border-radius: 4px; margin-right: 6px; vertical-align: -1px; }
.legend .l-active::before { background: #e1ecdf; border: 1.5px solid #7c9a80; }
.legend .l-mid::before { background: #b04e68; }
.legend .l-out::before { background: #f4f1f3; border: 1px solid #ddd6dc; }
.legend .l-found::before { background: #4b6a50; }

.log { background: #fff; border: 1.5px solid #f0e4e8; border-radius: 16px; padding: 10px 16px; margin-top: 16px; max-height: 300px; overflow-y: auto; }
.log .line { padding: 6px 0; border-bottom: 1px dotted #eadfe3; font-size: 14.5px; }
.log .line:last-child { border-bottom: none; }
.log .note { color: #6d6672; padding-left: 14px; }

.result { border-radius: 16px; padding: 14px 20px; margin-top: 16px; font-size: 16px; }
.result.ok { background: #e1ecdf; border: 1.5px solid #7c9a80; }
.result.no { background: #f8e3e7; border: 1.5px solid #e7a7b6; }

.stButton > button, .stFormSubmitButton > button { width: 100%; border-radius: 999px; font-weight: 700; padding: .55rem 1rem; }
.foot { text-align: center; font-family: 'DM Mono', monospace; font-size: 12px; color: #9a94a0; margin-top: 36px;
  border-top: 2px dotted #e7a7b6; padding-top: 14px; }
.foot a { color: #b04e68; text-decoration: none; }
</style>
""",
    unsafe_allow_html=True,
)


def parse_array(text):
    parts = [p.strip() for p in text.replace(";", ",").split(",") if p.strip()]
    if not parts:
        raise ValueError("Please enter at least one number.")
    if len(parts) > MAX_ITEMS:
        raise ValueError(f"Please use at most {MAX_ITEMS} numbers so the boxes fit on screen.")
    try:
        return sorted(int(p) for p in parts)
    except ValueError:
        raise ValueError("Use whole numbers separated by commas, for example: 2, 5, 8, 12.")


def draw_array(arr, low, high, mid, found=False):
    cells = []
    for i, value in enumerate(arr):
        if found and i == mid:
            css = "found"
        elif i == mid:
            css = "mid"
        elif low <= i <= high:
            css = "active"
        else:
            css = "out"
        tags = []
        if low <= high:
            if i == low:
                tags.append("L")
            if i == mid:
                tags.append("M")
            if i == high:
                tags.append("H")
        pointer = "·".join(tags) if tags else "&nbsp;"
        cells.append(
            f"<div class='cell'><div class='box {css}'>{value}</div>"
            f"<div class='idx'>{i}</div><div class='ptr'>{pointer}</div></div>"
        )
    legend = (
        "<div class='legend'><span class='l-active'>Still possible</span>"
        "<span class='l-mid'>Middle (being checked)</span>"
        "<span class='l-out'>Ruled out</span><span class='l-found'>Found</span></div>"
    )
    return f"<div class='stage'><div class='row'>{''.join(cells)}</div>{legend}</div>"


def draw_log(lines):
    body = "".join(f"<div class='line{' note' if l.startswith('↳') else ''}'>{l}</div>" for l in lines)
    return f"<div class='log'>{body}</div>"


st.markdown(
    """
<div class="hero">
  <span class="stamp">Unit 2 · Divide and Conquer</span>
  <h1>Binary Search Simulator</h1>
  <p>Watch the search space shrink by half at every step. Type your own numbers, pick a target and press start.</p>
</div>
""",
    unsafe_allow_html=True,
)

left, right = st.columns([1, 2], gap="large")

with left:
    st.markdown("<p class='label'>Your input</p>", unsafe_allow_html=True)
    with st.form("inputs"):
        arr_text = st.text_input("Numbers (comma-separated)", DEFAULT_ARRAY)
        target = st.number_input("Number to find", value=23, step=1)
        speed_name = st.select_slider("Animation speed", options=list(SPEEDS), value="Medium")
        start = st.form_submit_button("Start simulation", type="primary")

    st.markdown(
        """
<div class="card">
  <p class="label">How it works</p>
  <ul>
    <li>The numbers are sorted for you first.</li>
    <li>Look at the <b>middle</b> number (M).</li>
    <li>If it is smaller than the target, drop the left half. If it is bigger, drop the right half.</li>
    <li>Repeat until it is found or nothing is left.</li>
  </ul>
  <p><b>L</b> = low, <b>M</b> = mid, <b>H</b> = high</p>
</div>
<div class="card">
  <p class="label">Complexity</p>
  <ul>
    <li>Best case: O(1) (found at the middle)</li>
    <li>Average and worst case: O(log n)</li>
    <li>Space: O(1) (iterative)</li>
  </ul>
</div>
""",
        unsafe_allow_html=True,
    )

with right:
    st.markdown("<p class='label'>Live simulation</p>", unsafe_allow_html=True)
    visual = st.empty()
    log_box = st.empty()
    result_box = st.empty()

    try:
        arr = parse_array(arr_text)
        error = None
    except ValueError as exc:
        arr, error = [], str(exc)

    if error:
        st.error(error)
    elif not start:
        visual.markdown(draw_array(arr, 0, len(arr) - 1, -1), unsafe_allow_html=True)
        log_box.markdown(
            "<div class='log'><div class='line note'>Press <b>Start simulation</b> to begin.</div></div>",
            unsafe_allow_html=True,
        )
    else:
        target = int(target)
        delay = SPEEDS[speed_name]
        low, high, step, found_at = 0, len(arr) - 1, 0, None
        logs = [f"Sorted array: {arr}", f"Looking for <b>{target}</b> among {len(arr)} numbers."]
        log_box.markdown(draw_log(logs), unsafe_allow_html=True)

        while low <= high:
            step += 1
            mid = (low + high) // 2
            visual.markdown(draw_array(arr, low, high, mid), unsafe_allow_html=True)
            logs.append(f"<b>Step {step}</b>: low = {low}, high = {high}, mid = {mid}, so check <b>{arr[mid]}</b>")
            log_box.markdown(draw_log(logs), unsafe_allow_html=True)
            time.sleep(delay)

            if arr[mid] == target:
                found_at = mid
                visual.markdown(draw_array(arr, low, high, mid, found=True), unsafe_allow_html=True)
                logs.append(f"✓ {arr[mid]} equals {target}. Found at index {mid}.")
                log_box.markdown(draw_log(logs), unsafe_allow_html=True)
                break
            if arr[mid] < target:
                logs.append(f"↳ {arr[mid]} is smaller than {target}, so drop the left half. low becomes {mid + 1}.")
                low = mid + 1
            else:
                logs.append(f"↳ {arr[mid]} is bigger than {target}, so drop the right half. high becomes {mid - 1}.")
                high = mid - 1
            log_box.markdown(draw_log(logs), unsafe_allow_html=True)
            time.sleep(delay * 0.6)

        if found_at is None:
            visual.markdown(draw_array(arr, 0, -1, -1), unsafe_allow_html=True)
            logs.append(f"✗ Nothing left to check. {target} is not in the array.")
            log_box.markdown(draw_log(logs), unsafe_allow_html=True)
            result_box.markdown(
                f"<div class='result no'><b>{target} is not in the array.</b> Checked {step} "
                f"number{'s' if step != 1 else ''} before the search space ran out.</div>",
                unsafe_allow_html=True,
            )
        else:
            result_box.markdown(
                f"<div class='result ok'><b>Found {target} at index {found_at}</b> in {step} "
                f"step{'s' if step != 1 else ''}.</div>",
                unsafe_allow_html=True,
            )

        worst = math.floor(math.log2(len(arr))) + 1
        c1, c2, c3 = st.columns(3)
        c1.metric("Steps taken", step)
        c2.metric("Most steps possible here", worst)
        c3.metric("Linear search could need", len(arr))

st.markdown(
    "<div class='foot'>Part of <a href='https://algorithmcornerbysasha.blogspot.com' target='_blank'>The Weekly Algorithm</a>"
    " · Design and Analysis of Algorithm</div>",
    unsafe_allow_html=True,
)
