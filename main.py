
from __future__ import annotations

import json
from datetime import datetime
from pathlib import Path
from data.loader import load_questions, load_texts

VERSION = "1.1.0"
LEVELS = ["beginner", "developer", "expert"]
LEVEL_POINTS = {"beginner": 1.0, "developer": 2.0, "expert": 3.0}

BASE_DIR = Path(__file__).resolve().parent
REPORTS_DIR = BASE_DIR / "reports"
SESSIONS_DIR = BASE_DIR / "sessions"
STATE_PATH = SESSIONS_DIR / "session_state.json"


def ensure_dirs() -> None:
    REPORTS_DIR.mkdir(exist_ok=True)
    SESSIONS_DIR.mkdir(exist_ok=True)


def choose_language() -> str:
    print(f"Welcome to PyTrainerEdu v{VERSION}")
    print("\nChoose language:")
    print("1. Slovak")
    print("2. Czech")
    print("3. English")
    print("4. Spanish")
    while True:
        c = input("> ").strip()
        if c == "1":
            return "sk"
        if c == "2":
            return "cz"
        if c == "3":
            return "en"
        if c == "4":
            return "es"
        print("Invalid choice, try again.")


def choose_level(texts: dict) -> str:
    print("\n" + texts["choose_level"])
    print("1. " + texts["lvl_beginner"])
    print("2. " + texts["lvl_developer"])
    print("3. " + texts["lvl_expert"])
    while True:
        c = input("> ").strip()
        if c == "1":
            return "beginner"
        if c == "2":
            return "developer"
        if c == "3":
            return "expert"
        print(texts["invalid_choice"])


def normalize_answer(ans: str) -> str:
    ans = ans.strip().lower()
    if len(ans) >= 2 and ans[1] in [")", "."]:
        ans = ans[0]
    return ans


def parse_options(options: list[str]) -> list[tuple[str, str]]:
    parsed = []
    for opt in options:
        if ")" in opt:
            letter, text = opt.split(")", 1)
            parsed.append((letter.strip().lower(), text.strip()))
        else:
            parsed.append(("", opt.strip()))
    return parsed


def get_correct_display(q: dict) -> str:
    if q["type"] == "choice":
        for letter, text in parse_options(q.get("options", [])):
            if letter == normalize_answer(str(q["correct"])):
                return f"{letter.upper()}) {text}"
    return str(q["correct"])


def is_correct_answer(q: dict, ans: str) -> bool:
    user = normalize_answer(ans)

    if q["type"] == "choice":
        correct_letter = normalize_answer(str(q["correct"]))
        if user == correct_letter:
            return True
        for letter, text in parse_options(q.get("options", [])):
            if letter == correct_letter and user == text.lower():
                return True
        for item in q.get("accepted_answers", []):
            if user == normalize_answer(str(item)):
                return True
        return False

    accepted = q.get("accepted_answers", [])
    if accepted:
        return user in [normalize_answer(str(x)) for x in accepted]
    return user == normalize_answer(str(q["correct"]))


def get_grade(percent: float) -> str:
    if percent == 100:
        return "1*"
    if percent >= 80:
        return "1"
    if percent >= 60:
        return "2"
    if percent >= 40:
        return "3"
    if percent >= 10:
        return "4"
    return "5"


def get_recommendation_key(level: str, percent: float) -> str:
    if level == "expert":
        if percent >= 80:
            return "expert_strong"
        if percent >= 40:
            return "expert_mid"
        return "expert_low"
    if percent >= 60:
        return "advance"
    if percent >= 40:
        return "repeat"
    return "train_more"


def build_questions_by_level(lang: str) -> dict:
    questions = load_questions(lang)
    grouped = {level: [] for level in LEVELS}
    for q in questions:
        grouped[q["level"]].append(q)
    for level in grouped:
        grouped[level].sort(key=lambda x: x.get("order_index", 9999))
    return grouped


def empty_level_stats(questions_by_level: dict, levels_allowed: list[str]) -> dict:
    out = {}
    for level in levels_allowed:
        out[level] = {
            "answered": 0,
            "correct": 0,
            "wrong": 0,
            "solution": 0,
            "hinted": 0,
            "points": 0.0,
            "max_points": float(len(questions_by_level[level]) * LEVEL_POINTS[level]),
            "completed": False,
        }
    return out


def calculate_totals(state: dict) -> tuple[float, float]:
    gained = 0.0
    maximum = 0.0
    for lvl in state["levels_allowed"]:
        gained += float(state["level_stats"][lvl]["points"])
        maximum += float(state["level_stats"][lvl]["max_points"])
    return gained, maximum


def save_state(state: dict) -> None:
    ensure_dirs()
    STATE_PATH.write_text(json.dumps(state, ensure_ascii=False, indent=2), encoding="utf-8")


def load_state() -> dict | None:
    if not STATE_PATH.exists():
        return None
    try:
        return json.loads(STATE_PATH.read_text(encoding="utf-8"))
    except Exception:
        return None


def delete_state() -> None:
    if STATE_PATH.exists():
        STATE_PATH.unlink()


def reset_level_progress(state: dict, level: str) -> None:
    state["question_logs"] = [x for x in state["question_logs"] if x["level"] != level]
    max_points = state["level_stats"][level]["max_points"]
    state["level_stats"][level] = {
        "answered": 0,
        "correct": 0,
        "wrong": 0,
        "solution": 0,
        "hinted": 0,
        "points": 0.0,
        "max_points": max_points,
        "completed": False,
    }
    state["current_index"] = 0


def print_pause_summary(texts: dict, state: dict) -> None:
    gained, maximum = calculate_totals(state)
    missing = round(maximum - gained, 1)
    current = state["current_level"]
    stats = state["level_stats"][current]
    print("\n" + "=" * 60)
    print(texts["paused"])
    print(f"{texts['selected_level']}: {texts[f'lvl_{current}']}")
    print(f"{texts['answered_count']}: {stats['answered']}")
    print(f"{texts['correct_count']}: {stats['correct']}")
    print(f"{texts['wrong_count']}: {stats['wrong']}")
    print(f"{texts['solution_count']}: {stats['solution']}")
    print(f"{texts['hint_count']}: {stats['hinted']}")
    print(f"{texts['points_now']}: {round(gained, 1)} / {round(maximum, 1)}")
    print(f"{texts['missing_points']}: {missing}")
    print("=" * 60)


def pause_menu(texts: dict, state: dict) -> str:
    while True:
        print_pause_summary(texts, state)
        print("1. " + texts["pause_continue"])
        print("2. " + texts["pause_restart_level"])
        print("3. " + texts["pause_save_and_quit"])
        choice = input("> ").strip()
        if choice == "1":
            return "continue"
        if choice == "2":
            return "restart_level"
        if choice == "3":
            return "save_and_quit"
        print(texts["invalid_choice"])


def update_stats_for_result(state: dict, level: str, status: str, used_hint: bool, points_awarded: float) -> None:
    stats = state["level_stats"][level]
    stats["answered"] += 1
    if status == "correct":
        stats["correct"] += 1
    elif status == "wrong":
        stats["wrong"] += 1
    elif status == "solution":
        stats["solution"] += 1
    if used_hint:
        stats["hinted"] += 1
    stats["points"] = round(stats["points"] + points_awarded, 1)


def append_log(state: dict, level: str, q: dict, status_key: str, user_answer: str, used_hint: bool, points_awarded: float) -> None:
    state["question_logs"].append({
        "id": q.get("id", ""),
        "level": level,
        "status_key": status_key,
        "user_answer": user_answer,
        "correct_answer": get_correct_display(q),
        "used_hint": used_hint,
        "question": q["question"],
        "explanation": q["explanation"],
        "points_awarded": round(points_awarded, 1),
        "max_points": LEVEL_POINTS[level],
    })


def save_report(state: dict, texts: dict, final: bool) -> Path:
    ensure_dirs()
    ts = datetime.now().strftime("%Y%m%d_%H%M%S")
    suffix = "final" if final else "partial"
    path = REPORTS_DIR / f"report_{state['lang']}_{suffix}_{ts}.txt"

    gained, maximum = calculate_totals(state)
    missing = round(maximum - gained, 1)
    questions_by_level = build_questions_by_level(state["lang"])

    lines = []
    lines.append(f"PyTrainerEdu v{VERSION} report")
    lines.append("=" * 60)
    lines.append(f"{texts['report_language']}: {state['lang']}")
    lines.append(f"{texts['report_status']}: {texts['report_status_complete'] if final else texts['report_status_interrupted']}")
    lines.append("")
    lines.append(texts["summary"])
    lines.append("-" * 60)

    for level in state["levels_allowed"]:
        stats = state["level_stats"][level]
        answered = stats["answered"]
        total_q = len(questions_by_level[level])
        percent = round((stats["points"] / stats["max_points"]) * 100, 1) if stats["max_points"] else 0.0
        grade = get_grade(percent)
        recommendation_key = get_recommendation_key(level, percent)
        lines.append(
            f"{texts[f'lvl_{level}']}: {answered}/{total_q} | "
            f"{texts['correct_count_short']} {stats['correct']} | "
            f"{texts['wrong_count_short']} {stats['wrong']} | "
            f"{texts['solution_count_short']} {stats['solution']} | "
            f"{texts['points_word']} {round(stats['points'],1)}/{round(stats['max_points'],1)} | "
            f"{texts['grade']} {grade} | "
            f"{texts['recommendation']}: {texts[recommendation_key]}"
        )

    lines.append("")
    lines.append(texts["details"])
    lines.append("-" * 60)
    for row in state["question_logs"]:
        lines.append(f"[{row['id']}] {texts[f'lvl_{row['level']}']} | {texts[row['status_key']]}")
        lines.append(row["question"])
        lines.append(f"{texts['report_user_answer']}: {row['user_answer']}")
        lines.append(f"{texts['report_correct_answer']}: {row['correct_answer']}")
        lines.append(f"{texts['report_hint_used']}: {texts['yes'] if row['used_hint'] else texts['no']}")
        lines.append(f"{texts['report_points_awarded']}: {row['points_awarded']} / {row['max_points']}")
        lines.append(f"{texts['report_explanation']}: {row['explanation']}")
        lines.append("-" * 60)

    lines.append("")
    lines.append(texts["final_evaluation"])
    lines.append("-" * 60)
    lines.append(f"{texts['points_word']}: {round(gained,1)} / {round(maximum,1)}")
    lines.append(f"{texts['missing_points']}: {missing}")
    path.write_text("\n".join(lines), encoding="utf-8")
    return path


def ask_resume() -> bool:
    state = load_state()
    if not state or state.get("version") != VERSION:
        return False
    print(f"PyTrainerEdu v{VERSION}")
    print("Found unfinished session. Resume? (y/n)")
    answer = input("> ").strip().lower()
    if answer in ["y", "yes", "a", "ano", "áno", "s", "si", "sí"]:
        return True
    delete_state()
    return False


def create_new_state(lang: str, start_level: str) -> dict:
    questions_by_level = build_questions_by_level(lang)
    start_idx = LEVELS.index(start_level)
    allowed = LEVELS[start_idx:]
    return {
        "version": VERSION,
        "lang": lang,
        "levels_allowed": allowed,
        "current_level": start_level,
        "current_index": 0,
        "question_logs": [],
        "level_stats": empty_level_stats(questions_by_level, allowed),
    }


def run() -> None:
    ensure_dirs()

    if ask_resume():
        state = load_state()
        if state is None:
            lang = choose_language()
            texts = load_texts(lang)
            level = choose_level(texts)
            state = create_new_state(lang, level)
        else:
            lang = state["lang"]
            texts = load_texts(lang)
            print(f"\n{texts['resuming']} {texts[f'lvl_{state['current_level']}']}")
    else:
        lang = choose_language()
        texts = load_texts(lang)
        level = choose_level(texts)
        state = create_new_state(lang, level)

    questions_by_level = build_questions_by_level(lang)

    while True:
        current_level = state["current_level"]
        questions = questions_by_level[current_level]

        print("\n" + texts["intro"])
        print(f"{texts['selected_level']}: {texts[f'lvl_{current_level}']}")
        print(texts["hint_info"])
        print(texts["solution_info"])
        print(texts["pause_info"])
        print(texts["quit_info"])
        input(texts["press_enter"])

        idx = state["current_index"]
        while idx < len(questions):
            q = questions[idx]
            print("\n" + "=" * 60)
            print(f"{texts['question']} {idx+1}/{len(questions)}  [{q.get('id', '')}]")
            print("-" * 60)
            print(q["question"])

            if q["type"] == "choice":
                for opt in q.get("options", []):
                    print(opt)

            used_hint = False

            while True:
                ans = input(texts["answer"]).strip()

                if ans == "":
                    print(f"{texts['hint']} {q.get('hint', '...')}")
                    used_hint = True
                    continue

                if normalize_answer(ans) == "q":
                    action = pause_menu(texts, state)
                    if action == "continue":
                        continue
                    if action == "restart_level":
                        reset_level_progress(state, current_level)
                        save_state(state)
                        idx = 0
                        break
                    if action == "save_and_quit":
                        state["current_index"] = idx
                        save_state(state)
                        report_path = save_report(state, texts, final=False)
                        print(f"{texts['report_saved']} {report_path}")
                        return

                if normalize_answer(ans) == "quit":
                    state["current_index"] = idx
                    save_state(state)
                    report_path = save_report(state, texts, final=False)
                    print(f"{texts['report_saved']} {report_path}")
                    return

                if ans == "?":
                    points = 0.0
                    print(f"{texts['solution']} {get_correct_display(q)}")
                    print(f"{texts['report_explanation']}: {q['explanation']}")
                    update_stats_for_result(state, current_level, "solution", used_hint, points)
                    append_log(state, current_level, q, "status_solution", "?", used_hint, points)
                    idx += 1
                    state["current_index"] = idx
                    save_state(state)
                    break

                if is_correct_answer(q, ans):
                    points = LEVEL_POINTS[current_level] - (0.5 if used_hint else 0.0)
                    if points < 0:
                        points = 0.0
                    print(texts["correct"])
                    print(f"{texts['report_explanation']}: {q['explanation']}")
                    update_stats_for_result(state, current_level, "correct", used_hint, points)
                    append_log(state, current_level, q, "status_correct", ans, used_hint, points)
                    idx += 1
                    state["current_index"] = idx
                    save_state(state)
                    break

                points = 0.0
                print(f"{texts['wrong']} {get_correct_display(q)}")
                print(f"{texts['report_explanation']}: {q['explanation']}")
                update_stats_for_result(state, current_level, "wrong", used_hint, points)
                append_log(state, current_level, q, "status_wrong", ans, used_hint, points)
                idx += 1
                state["current_index"] = idx
                save_state(state)
                break

            if state["current_index"] == 0 and idx != 0:
                idx = 0
                continue

        state["level_stats"][current_level]["completed"] = True

        stats = state["level_stats"][current_level]
        percent = round((stats["points"] / stats["max_points"]) * 100, 1) if stats["max_points"] else 0.0
        grade = get_grade(percent)
        recommendation_key = get_recommendation_key(current_level, percent)

        print("\n" + "=" * 60)
        print(f"{texts['score']} {stats['correct']} / {len(questions)}")
        print(f"{texts['points_word']}: {round(stats['points'],1)} / {round(stats['max_points'],1)}")
        print(f"{texts['success_rate']} {percent}%")
        print(f"{texts['grade']} {grade}")
        print(f"{texts['recommendation']}: {texts[recommendation_key]}")

        next_idx = LEVELS.index(current_level) + 1
        if next_idx < len(LEVELS) and LEVELS[next_idx] in state["levels_allowed"] and percent >= 60:
            nxt = LEVELS[next_idx]
            answer = input(texts["continue_prompt"].format(next_level=texts[f"lvl_{nxt}"])).strip().lower()
            if answer in [x.lower() for x in texts["yes_answers"]]:
                state["current_level"] = nxt
                state["current_index"] = 0
                save_state(state)
                continue

        break

    report_path = save_report(state, texts, final=True)
    delete_state()
    print(f"{texts['report_saved']} {report_path}")


if __name__ == "__main__":
    run()
