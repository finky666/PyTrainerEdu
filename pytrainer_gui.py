from __future__ import annotations

import json
import random
import textwrap
import tkinter as tk
from datetime import datetime
from pathlib import Path
from tkinter import messagebox

from data.loader import load_questions, load_texts
from main import (
    LEVEL_POINTS,
    LEVELS,
    get_correct_display,
    get_grade,
    get_recommendation_key,
    is_correct_answer,
    normalize_answer,
    parse_options,
)

APP_VERSION = "1.1.0"
APP_TITLE = f"PyTrainerEdu v{APP_VERSION}"
APP_BG = "#000000"
APP_FG = "#FFFFFF"
BTN_BG = "#F0F0F0"
BTN_FG = "#000000"
OUTLINE = "#FFFFFF"
SUBTLE = "#BFBFBF"
INPUT_BG = "#000000"
INPUT_FG = "#FFFFFF"
FONT_UI = ("Consolas", 14)
FONT_SMALL = ("Consolas", 11)
FONT_TITLE = ("Consolas", 17, "bold")
FONT_BIG = ("Consolas", 18, "bold")
FONT_QUESTION = ("Consolas", 17, "bold")
FONT_OPTION = ("Consolas", 13)
FONT_FEEDBACK = ("Consolas", 15)
WRAP = 980

BASE_DIR = Path(__file__).resolve().parent
REPORTS_DIR = BASE_DIR / "reports"
SESSIONS_DIR = BASE_DIR / "sessions"
GUI_STATE_PATH = SESSIONS_DIR / "session_state_gui_v1.json"

LANG_CHOICES = [("en", "English"), ("sk", "Slovak"), ("cz", "Czech"), ("es", "Spanish")]

GUI_TEXT = {
    "en": {
        "welcome_title": "Welcome to PyTrainerEdu!",
        "welcome_subtitle": "Welcome to Python Test",
        "select_language": "Select language",
        "select_counts": "Select number of questions per level (0–50)",
        "random_questions": "Random question selection?",
        "start_test": "Start Test",
        "about": "About",
        "exit": "Exit",
        "yes": "Yes",
        "no": "No",
        "beginner": "Beginner",
        "developer": "Developer",
        "expert": "Expert",
        "about_text": "PyTrainerEdu is an offline Python quiz application with beginner, developer, and expert levels.\n\nChoose the language, set the number of questions for each level, and practice without internet access.",
        "welcome_body": "PyTrainerEdu is an interactive application for practicing and testing your Python knowledge through quizzes with multiple difficulty levels.",
        "bullet_1": "Choose a language and set the number of questions for each level.",
        "bullet_2": "Questions can be selected randomly from the database.",
        "bullet_3": "Track your progress and keep improving.",
        "concept": "Concept C – Header dashboard",
        "status_ready": "Ready.",
        "status_loaded": "Test loaded.",
        "status_correct": "Correct answer.",
        "status_wrong": "Wrong answer.",
        "status_hint": "Hint used. A correct answer now loses 0.5 point.",
        "status_solution": "Solution shown without a point.",
        "status_finished": "Test completed.",
        "answer_here": "Type answer here:",
        "pick_answer": "Select an answer or type one first.",
        "hint_prefix": "Hint:",
        "correct_answer": "Correct answer:",
        "explanation": "Explanation:",
        "next_question": "Next Question",
        "finish_button": "Finish",
        "submit_answer": "Submit Answer",
        "hint": "Hint",
        "solution": "Solution",
        "save_quit": "Save and Close",
        "question_type_choice": "Multiple choice",
        "question_type_text": "Text answer",
        "question_counter": "Question",
        "level_result": "Level result",
        "final_result": "Final result",
        "result_saved": "Report saved:",
        "resume_title": "Unfinished session",
        "resume_text": "An unfinished GUI session was found. Do you want to resume it?",
        "close_title": "Close GUI",
        "close_text": "Save unfinished progress and create a partial report?",
        "discarded": "Unfinished progress was discarded.",
        "saved_partial": "Progress saved. Report: {path}",
        "saved_final": "Final report saved: {path}",
        "continue_next": "Continue to level {next_level}?",
        "no_levels": "Set at least one level to 1–50 questions.",
        "bad_count": "Each level must be between 0 and 50.",
        "tt_submit": "Check answer",
        "tt_next": "Next question",
        "tt_hint": "Hint: -0.5 point",
        "tt_solution": "Show solution",
        "tt_save_quit": "Save progress",
        "tt_entry": "Type A/B/C or answer",
        "tt_option": "Choose: {answer}",
        "tt_start": "Start test",
        "tt_about": "About app",
        "tt_exit": "Exit",
        "footer": "PyTrainerEdu is an offline test application for learning Python.",
    },
    "sk": {
        "welcome_title": "Vitajte v PyTrainerEdu!",
        "welcome_subtitle": "Vitajte v teste Pythonu",
        "select_language": "Vyber jazyk",
        "select_counts": "Vyber počet otázok pre úrovne (0–50)",
        "random_questions": "Náhodný výber otázok?",
        "start_test": "Spustiť test",
        "about": "About",
        "exit": "Koniec",
        "yes": "Áno",
        "no": "Nie",
        "beginner": "Začiatočník",
        "developer": "Vývojár",
        "expert": "Expert",
        "about_text": "PyTrainerEdu je offline aplikácia na testovanie znalostí Pythonu pre začiatočníkov, vývojárov aj pokročilých.\n\nVyber jazyk, nastav počet otázok pre každú úroveň a uč sa bez internetu.",
        "welcome_body": "PyTrainerEdu je interaktívna aplikácia na precvičovanie a overovanie Vašich vedomostí z Pythonu formou testov s rôznymi úrovňami náročnosti.",
        "bullet_1": "Vyberte jazyk a počet otázok pre každú úroveň.",
        "bullet_2": "Otázky sa vyberajú náhodne z databázy.",
        "bullet_3": "Sledujte svoj pokrok a zlepšujte sa.",
        "concept": "Koncept C – Header dashboard",
        "status_ready": "Pripravené.",
        "status_loaded": "Test načítaný.",
        "status_correct": "Správna odpoveď.",
        "status_wrong": "Nesprávna odpoveď.",
        "status_hint": "Nápoveda použitá. Pri správnej odpovedi sa odráta 0.5 bodu.",
        "status_solution": "Zobrazené riešenie bez bodu.",
        "status_finished": "Test dokončený.",
        "answer_here": "Odpoveď píš sem:",
        "pick_answer": "Najprv označ odpoveď alebo ju napíš.",
        "hint_prefix": "Nápoveda:",
        "correct_answer": "Správna odpoveď:",
        "explanation": "Vysvetlenie:",
        "next_question": "Ďalšia otázka",
        "finish_button": "Vyhodnotiť",
        "submit_answer": "Potvrdiť odpoveď",
        "hint": "Nápoveda",
        "solution": "Riešenie",
        "save_quit": "Uložiť a zavrieť",
        "question_type_choice": "Výber z možností",
        "question_type_text": "Textová odpoveď",
        "question_counter": "Otázka",
        "level_result": "Výsledok úrovne",
        "final_result": "Finálny výsledok",
        "result_saved": "Report uložený:",
        "resume_title": "Nedokončená session",
        "resume_text": "Našla sa nedokončená GUI session. Chceš pokračovať?",
        "close_title": "Ukončenie GUI",
        "close_text": "Uložiť rozpracovaný stav a vytvoriť čiastočný report?",
        "discarded": "Rozpracovaný stav bol zahodený.",
        "saved_partial": "Stav uložený. Report: {path}",
        "saved_final": "Finálny report uložený: {path}",
        "continue_next": "Pokračovať na úroveň {next_level}?",
        "no_levels": "Nastav aspoň jednu úroveň na 1–50 otázok.",
        "bad_count": "Každá úroveň musí byť v rozsahu 0 až 50.",
        "tt_submit": "Skontrolovať odpoveď",
        "tt_next": "Ďalšia otázka",
        "tt_hint": "Nápoveda: -0.5 bodu",
        "tt_solution": "Riešenie bez bodu",
        "tt_save_quit": "Uložiť postup",
        "tt_entry": "Napíš A/B/C alebo odpoveď",
        "tt_option": "Vybrať: {answer}",
        "tt_start": "Spustiť test",
        "tt_about": "O programe",
        "tt_exit": "Zavrieť",
        "footer": "PyTrainerEdu je offline testovacia aplikácia na učenie Pythonu.",
    },
    "cz": {
        "welcome_title": "Vítejte v PyTrainerEdu!",
        "welcome_subtitle": "Vítejte v Python testu",
        "select_language": "Vyber jazyk",
        "select_counts": "Vyber počet otázek pro úrovně (0–50)",
        "random_questions": "Náhodný výběr otázek?",
        "start_test": "Spustit test",
        "about": "About",
        "exit": "Konec",
        "yes": "Ano",
        "no": "Ne",
        "beginner": "Začátečník",
        "developer": "Vývojář",
        "expert": "Expert",
        "about_text": "PyTrainerEdu je offline aplikace pro testování znalostí Pythonu pro začátečníky, vývojáře i pokročilé.\n\nVyber jazyk, nastav počet otázek pro každou úroveň a uč se bez internetu.",
        "welcome_body": "PyTrainerEdu je interaktivní aplikace pro procvičování a ověřování vašich znalostí Pythonu formou testů s různými úrovněmi náročnosti.",
        "bullet_1": "Vyberte jazyk a počet otázek pro každou úroveň.",
        "bullet_2": "Otázky se vybírají náhodně z databáze.",
        "bullet_3": "Sledujte svůj pokrok a zlepšujte se.",
        "concept": "Koncept C – Header dashboard",
        "status_ready": "Připraveno.",
        "status_loaded": "Test načten.",
        "status_correct": "Správná odpověď.",
        "status_wrong": "Špatná odpověď.",
        "status_hint": "Nápověda použita. Při správné odpovědi se odečte 0.5 bodu.",
        "status_solution": "Zobrazené řešení bez bodu.",
        "status_finished": "Test dokončen.",
        "answer_here": "Odpověď piš sem:",
        "pick_answer": "Nejdřív označ odpověď nebo ji napiš.",
        "hint_prefix": "Nápověda:",
        "correct_answer": "Správná odpověď:",
        "explanation": "Vysvětlení:",
        "next_question": "Další otázka",
        "finish_button": "Vyhodnotit",
        "submit_answer": "Potvrdit odpověď",
        "hint": "Nápověda",
        "solution": "Řešení",
        "save_quit": "Uložit a zavřít",
        "question_type_choice": "Výběr z možností",
        "question_type_text": "Textová odpověď",
        "question_counter": "Otázka",
        "level_result": "Výsledek úrovně",
        "final_result": "Finální výsledek",
        "result_saved": "Report uložen:",
        "resume_title": "Nedokončená session",
        "resume_text": "Našla se nedokončená GUI session. Chceš pokračovat?",
        "close_title": "Ukončení GUI",
        "close_text": "Uložit rozpracovaný stav a vytvořit částečný report?",
        "discarded": "Rozpracovaný stav byl zahozen.",
        "saved_partial": "Stav uložen. Report: {path}",
        "saved_final": "Finální report uložen: {path}",
        "continue_next": "Pokračovat na úroveň {next_level}?",
        "no_levels": "Nastav alespoň jednu úroveň na 1–50 otázek.",
        "bad_count": "Každá úroveň musí být v rozsahu 0 až 50.",
        "tt_submit": "Zkontrolovat odpověď",
        "tt_next": "Další otázka",
        "tt_hint": "Nápověda: -0.5 bodu",
        "tt_solution": "Řešení bez bodu",
        "tt_save_quit": "Uložit postup",
        "tt_entry": "Napiš A/B/C nebo odpověď",
        "tt_option": "Vybrat: {answer}",
        "tt_start": "Spustit test",
        "tt_about": "O programu",
        "tt_exit": "Zavřít",
        "footer": "PyTrainerEdu je offline testovací aplikace pro učení Pythonu.",
    },
    "es": {
        "welcome_title": "¡Bienvenido a PyTrainerEdu!",
        "welcome_subtitle": "Bienvenido al test de Python",
        "select_language": "Selecciona idioma",
        "select_counts": "Selecciona el número de preguntas por nivel (0–50)",
        "random_questions": "¿Selección aleatoria de preguntas?",
        "start_test": "Iniciar test",
        "about": "About",
        "exit": "Salir",
        "yes": "Sí",
        "no": "No",
        "beginner": "Principiante",
        "developer": "Desarrollador",
        "expert": "Experto",
        "about_text": "PyTrainerEdu es una aplicación offline para poner a prueba conocimientos de Python para principiantes, desarrolladores y usuarios avanzados.\n\nSelecciona idioma, ajusta el número de preguntas por nivel y estudia sin internet.",
        "welcome_body": "PyTrainerEdu es una aplicación interactiva para practicar y comprobar tus conocimientos de Python mediante cuestionarios con varios niveles de dificultad.",
        "bullet_1": "Elige un idioma y el número de preguntas para cada nivel.",
        "bullet_2": "Las preguntas pueden seleccionarse aleatoriamente de la base de datos.",
        "bullet_3": "Sigue tu progreso y mejora poco a poco.",
        "concept": "Concepto C – Header dashboard",
        "status_ready": "Listo.",
        "status_loaded": "Test cargado.",
        "status_correct": "Respuesta correcta.",
        "status_wrong": "Respuesta incorrecta.",
        "status_hint": "Pista usada. Una respuesta correcta ahora pierde 0.5 punto.",
        "status_solution": "Solución mostrada sin punto.",
        "status_finished": "Test completado.",
        "answer_here": "Escribe la respuesta aquí:",
        "pick_answer": "Primero selecciona o escribe una respuesta.",
        "hint_prefix": "Pista:",
        "correct_answer": "Respuesta correcta:",
        "explanation": "Explicación:",
        "next_question": "Siguiente pregunta",
        "finish_button": "Finalizar",
        "submit_answer": "Confirmar respuesta",
        "hint": "Pista",
        "solution": "Solución",
        "save_quit": "Guardar y cerrar",
        "question_type_choice": "Opción múltiple",
        "question_type_text": "Respuesta de texto",
        "question_counter": "Pregunta",
        "level_result": "Resultado del nivel",
        "final_result": "Resultado final",
        "result_saved": "Informe guardado:",
        "resume_title": "Sesión incompleta",
        "resume_text": "Se encontró una sesión GUI incompleta. ¿Quieres continuar?",
        "close_title": "Cerrar GUI",
        "close_text": "¿Guardar el progreso y crear un informe parcial?",
        "discarded": "El progreso fue descartado.",
        "saved_partial": "Progreso guardado. Informe: {path}",
        "saved_final": "Informe final guardado: {path}",
        "continue_next": "¿Continuar al nivel {next_level}?",
        "no_levels": "Configura al menos un nivel con 1–50 preguntas.",
        "bad_count": "Cada nivel debe estar entre 0 y 50.",
        "tt_submit": "Comprobar respuesta",
        "tt_next": "Siguiente pregunta",
        "tt_hint": "Pista: -0.5 punto",
        "tt_solution": "Solución sin punto",
        "tt_save_quit": "Guardar progreso",
        "tt_entry": "Escribe A/B/C o respuesta",
        "tt_option": "Elegir: {answer}",
        "tt_start": "Iniciar test",
        "tt_about": "Acerca de",
        "tt_exit": "Salir",
        "footer": "PyTrainerEdu es una aplicación offline para aprender Python.",
    },
}


class TerminalButton(tk.Button):
    def __init__(self, master: tk.Misc, **kwargs) -> None:
        font = kwargs.pop("font", FONT_UI)
        padx = kwargs.pop("padx", 9)
        pady = kwargs.pop("pady", 7)
        super().__init__(
            master,
            bg=BTN_BG,
            fg=BTN_FG,
            activebackground=BTN_BG,
            activeforeground=BTN_FG,
            relief="flat",
            bd=0,
            highlightthickness=1,
            highlightbackground=OUTLINE,
            font=font,
            padx=padx,
            pady=pady,
            cursor="hand2",
            **kwargs,
        )


class OutlineButton(tk.Button):
    def __init__(self, master: tk.Misc, **kwargs) -> None:
        font = kwargs.pop("font", FONT_UI)
        padx = kwargs.pop("padx", 9)
        pady = kwargs.pop("pady", 7)
        super().__init__(
            master,
            bg=APP_BG,
            fg=APP_FG,
            activebackground=APP_BG,
            activeforeground=APP_FG,
            relief="flat",
            bd=0,
            highlightthickness=1,
            highlightbackground=OUTLINE,
            font=font,
            padx=padx,
            pady=pady,
            cursor="hand2",
            **kwargs,
        )


class Panel(tk.Frame):
    def __init__(self, master: tk.Misc, **kwargs) -> None:
        super().__init__(master, bg=APP_BG, highlightbackground=OUTLINE, highlightthickness=1, bd=0, **kwargs)


class ToolTip:
    def __init__(self, widget: tk.Misc, text: str) -> None:
        self.widget = widget
        self.text = text
        self.tip_window: tk.Toplevel | None = None
        self.widget.bind("<Enter>", self._show, add="+")
        self.widget.bind("<Leave>", self._hide, add="+")
        self.widget.bind("<ButtonPress>", self._hide, add="+")

    def _show(self, _event=None) -> None:
        if self.tip_window or not self.text:
            return
        x = self.widget.winfo_rootx() + 18
        y = self.widget.winfo_rooty() + self.widget.winfo_height() + 8
        screen_h = self.widget.winfo_screenheight()
        if y + 90 > screen_h:
            y = max(20, self.widget.winfo_rooty() - 58)
        self.tip_window = tw = tk.Toplevel(self.widget)
        tw.wm_overrideredirect(True)
        tw.configure(bg=APP_BG)
        tw.wm_geometry(f"+{x}+{y}")
        label = tk.Label(
            tw,
            text=self.text,
            justify="left",
            bg=APP_BG,
            fg=APP_FG,
            font=FONT_SMALL,
            relief="flat",
            bd=0,
            highlightthickness=1,
            highlightbackground=OUTLINE,
            padx=8,
            pady=6,
            wraplength=260,
        )
        label.pack()

    def _hide(self, _event=None) -> None:
        if self.tip_window is not None:
            self.tip_window.destroy()
            self.tip_window = None


class PyTrainerGuiV1:
    def __init__(self, root: tk.Tk) -> None:
        self.root = root
        REPORTS_DIR.mkdir(exist_ok=True)
        SESSIONS_DIR.mkdir(exist_ok=True)

        self.root.title(APP_TITLE)
        self.root.configure(bg=APP_BG)
        self.root.geometry("1440x900")
        self.root.minsize(1180, 780)
        try:
            self.root.state("zoomed")
        except Exception:
            pass

        self.lang_var = tk.StringVar(value="en")
        self.random_var = tk.StringVar(value="yes")
        self.status_var = tk.StringVar(value=self.ui("status_ready"))
        self.score_var = tk.StringVar(value="0 / 0")
        self.points_var = tk.StringVar(value="0.0 / 0.0")
        self.progress_var = tk.StringVar(value="0 / 0")
        self.status_line1_var = tk.StringVar(value="")
        self.status_line2_var = tk.StringVar(value="")
        self.answer_text = tk.StringVar(value="")

        self.count_vars = {lvl: tk.IntVar(value=10) for lvl in LEVELS}
        self.questions_by_level: dict[str, list[dict]] = {}
        self.selected_questions: dict[str, list[dict]] = {}
        self.level_order: list[str] = []
        self.state: dict | None = None
        self.current_question: dict | None = None
        self.question_answered = False
        self.hint_used_current = False

        self.welcome_frame: tk.Frame | None = None
        self.test_frame: tk.Frame | None = None
        self.option_buttons: list[tk.Button] = []
        self.current_feedback = ""
        self.tooltips: list[ToolTip] = []
        self.logo_image: tk.PhotoImage | None = None

        self._build_welcome_screen()
        self._bind_keys()
        self._try_resume()
        self.root.protocol("WM_DELETE_WINDOW", self.on_close)

    def ui(self, key: str) -> str:
        return GUI_TEXT[self.lang_var.get()][key]

    def texts(self) -> dict:
        return load_texts(self.lang_var.get())

    def level_label(self, level: str) -> str:
        return self.texts()[f"lvl_{level}"]

    def _add_tooltip(self, widget: tk.Misc, text: str) -> None:
        self.tooltips.append(ToolTip(widget, text))

    def _get_logo_image(self) -> tk.PhotoImage:
        """Load a small logo for the header.

        The original logo is 96x96. In the compact header we use 48x48 so it
        does not push the title/info line out of alignment.
        """
        if self.logo_image is None:
            logo_path = BASE_DIR / "python_logo_small.png"
            full_logo = tk.PhotoImage(file=str(logo_path))
            self.logo_image = full_logo.subsample(2, 2)
        return self.logo_image

    def _place_header_logo(self, master: tk.Misc) -> None:
        tk.Label(master, image=self._get_logo_image(), bg=APP_BG, bd=0).place(relx=1.0, x=-18, y=10, anchor="ne")

    def _bind_keys(self) -> None:
        self.root.bind("<Return>", self._on_enter)
        self.root.bind("<F1>", lambda _e: self.show_hint())
        self.root.bind("?", lambda _e: self.show_solution())
        self.root.bind("<Escape>", lambda _e: self.save_and_quit())

    def _on_enter(self, _event=None) -> None:
        if self.test_frame is None:
            return
        if self.question_answered:
            self.next_question()
        else:
            self.submit_answer()

    def _destroy_frame(self, frame: tk.Frame | None) -> None:
        if frame is not None:
            frame.destroy()

    def _build_welcome_screen(self) -> None:
        self._destroy_frame(self.test_frame)
        self._destroy_frame(self.welcome_frame)
        self.welcome_frame = tk.Frame(self.root, bg=APP_BG)
        self.welcome_frame.pack(fill="both", expand=True, padx=16, pady=16)

        title_panel = Panel(self.welcome_frame)
        title_panel.pack(fill="x", pady=(0, 14))
        tk.Label(title_panel, text=APP_TITLE, bg=APP_BG, fg=APP_FG, font=FONT_BIG).pack(pady=(22, 4))
        tk.Label(title_panel, text="Welcome to Python Test", bg=APP_BG, fg=APP_FG, font=FONT_TITLE).pack(pady=(0, 18))
        self._place_header_logo(title_panel)

        body = tk.Frame(self.welcome_frame, bg=APP_BG)
        body.pack(fill="both", expand=True)

        left = Panel(body)
        left.pack(side="left", fill="both", expand=True, padx=(0, 8))
        right = Panel(body)
        right.pack(side="left", fill="both", expand=True, padx=(8, 0))

        self._fill_welcome_left(left)
        self._fill_welcome_right(right)

    def _fill_welcome_left(self, panel: tk.Frame) -> None:
        for child in panel.winfo_children():
            child.destroy()
        lang = self.lang_var.get()
        tk.Label(panel, text=self.ui("welcome_title"), bg=APP_BG, fg=APP_FG, font=FONT_TITLE).pack(anchor="w", padx=30, pady=(34, 18))
        tk.Frame(panel, bg=OUTLINE, height=1).pack(fill="x", padx=30, pady=(0, 26))
        tk.Label(panel, text=self.ui("welcome_body"), bg=APP_BG, fg=APP_FG, font=FONT_UI, justify="left", wraplength=430).pack(anchor="w", padx=30)

        bullets = [self.ui("bullet_1"), self.ui("bullet_2"), self.ui("bullet_3")]
        icons = ["▣", "◎", "↗"]
        block = tk.Frame(panel, bg=APP_BG)
        block.pack(fill="x", padx=30, pady=(34, 30))
        for icon, text in zip(icons, bullets):
            row = tk.Frame(block, bg=APP_BG)
            row.pack(fill="x", pady=10)
            tk.Label(row, text=icon, bg=APP_BG, fg=APP_FG, font=("Consolas", 24)).pack(side="left")
            tk.Label(row, text=text, bg=APP_BG, fg=APP_FG, font=FONT_UI, justify="left", wraplength=360).pack(side="left", padx=18)

        tk.Frame(panel, bg=SUBTLE, height=1).pack(fill="x", padx=30, pady=(12, 22))
        tk.Label(panel, text=self.ui("concept"), bg=APP_BG, fg=APP_FG, font=FONT_UI).pack(anchor="w", padx=30)

    def _fill_welcome_right(self, panel: tk.Frame) -> None:
        for child in panel.winfo_children():
            child.destroy()

        top = tk.Frame(panel, bg=APP_BG)
        top.pack(fill="x", padx=24, pady=(24, 10))
        tk.Label(top, text=self.ui("select_language"), bg=APP_BG, fg=APP_FG, font=FONT_TITLE).pack(anchor="w")

        langs = tk.Frame(panel, bg=APP_BG)
        langs.pack(fill="x", padx=24, pady=(0, 14))
        for code, label in LANG_CHOICES:
            rb = tk.Radiobutton(
                langs, text=label, variable=self.lang_var, value=code,
                indicatoron=False, bg=APP_BG, fg=APP_FG, selectcolor=APP_BG,
                activebackground=APP_BG, activeforeground=APP_FG,
                highlightbackground=OUTLINE, highlightthickness=1,
                font=FONT_UI, width=12, pady=12, command=self._refresh_welcome_locale,
            )
            rb.pack(side="left", padx=(0, 10))

        tk.Frame(panel, bg=OUTLINE, height=1).pack(fill="x", padx=24, pady=(0, 18))
        tk.Label(panel, text=self.ui("select_counts"), bg=APP_BG, fg=APP_FG, font=FONT_TITLE).pack(anchor="w", padx=24)

        counts_box = Panel(panel)
        counts_box.pack(fill="x", padx=24, pady=(14, 18))
        self.count_spinboxes = {}
        for level in LEVELS:
            row = tk.Frame(counts_box, bg=APP_BG)
            row.pack(fill="x")
            tk.Label(row, text=self.level_label(level), bg=APP_BG, fg=APP_FG, font=FONT_UI).pack(side="left", padx=18, pady=14)
            sp = tk.Spinbox(
                row, from_=0, to=50, textvariable=self.count_vars[level], width=5,
                bg=INPUT_BG, fg=INPUT_FG, insertbackground=INPUT_FG,
                buttonbackground=APP_BG, highlightbackground=OUTLINE, highlightthickness=1,
                relief="flat", font=FONT_UI, justify="center"
            )
            sp.pack(side="right", padx=18)
            self.count_spinboxes[level] = sp
            if level != LEVELS[-1]:
                tk.Frame(counts_box, bg=OUTLINE, height=1).pack(fill="x")

        tk.Frame(panel, bg=OUTLINE, height=1).pack(fill="x", padx=24, pady=(0, 18))
        tk.Label(panel, text=self.ui("random_questions"), bg=APP_BG, fg=APP_FG, font=FONT_TITLE).pack(anchor="w", padx=24)
        rnd = tk.Frame(panel, bg=APP_BG)
        rnd.pack(anchor="w", padx=24, pady=(10, 20))
        for value, label in [("yes", self.ui("yes")), ("no", self.ui("no"))]:
            tk.Radiobutton(
                rnd, text=label, variable=self.random_var, value=value,
                bg=APP_BG, fg=APP_FG, selectcolor=APP_BG,
                activebackground=APP_BG, activeforeground=APP_FG,
                highlightthickness=0, font=FONT_UI
            ).pack(side="left", padx=(0, 30))

        tk.Frame(panel, bg=OUTLINE, height=1).pack(fill="x", padx=24, pady=(0, 18))
        buttons = tk.Frame(panel, bg=APP_BG)
        buttons.pack(fill="x", padx=24, pady=(0, 22))
        btn_start = TerminalButton(buttons, text=self.ui("start_test"), command=self.start_test)
        btn_start.pack(side="left", fill="x", expand=True, padx=(0, 10))
        self._add_tooltip(btn_start, self.ui("tt_start"))
        btn_about = OutlineButton(buttons, text=self.ui("about"), command=self.show_about)
        btn_about.pack(side="left", fill="x", expand=True, padx=10)
        self._add_tooltip(btn_about, self.ui("tt_about"))
        btn_exit = OutlineButton(buttons, text=self.ui("exit"), command=self.root.destroy)
        btn_exit.pack(side="left", fill="x", expand=True, padx=(10, 0))
        self._add_tooltip(btn_exit, self.ui("tt_exit"))

        footer = tk.Frame(panel, bg=APP_BG)
        footer.pack(fill="x", padx=24, pady=(0, 22))
        tk.Frame(footer, bg=SUBTLE, height=1).pack(fill="x", pady=(0, 12))
        tk.Label(footer, text=self.ui("footer"), bg=APP_BG, fg=APP_FG, font=FONT_SMALL).pack(anchor="w")
        self.status_label_welcome = tk.Label(footer, textvariable=self.status_var, bg=APP_BG, fg=SUBTLE, font=FONT_SMALL)
        self.status_label_welcome.pack(anchor="w", pady=(8, 0))

    def _refresh_welcome_locale(self) -> None:
        if self.welcome_frame is None:
            return
        self.status_var.set(self.ui("status_ready"))
        body = self.welcome_frame.winfo_children()[1]
        left = body.winfo_children()[0]
        right = body.winfo_children()[1]
        self._fill_welcome_left(left)
        self._fill_welcome_right(right)

    def show_about(self) -> None:
        messagebox.showinfo(APP_TITLE, self.ui("about_text"))

    def _all_questions_grouped(self, lang: str) -> dict[str, list[dict]]:
        grouped = {lvl: [] for lvl in LEVELS}
        for q in load_questions(lang):
            grouped[q["level"]].append(q)
        for lvl in LEVELS:
            grouped[lvl].sort(key=lambda x: x.get("order_index", 9999))
        return grouped

    def _build_selection(self, lang: str) -> tuple[dict[str, list[dict]], list[str]]:
        grouped = self._all_questions_grouped(lang)
        selected = {lvl: [] for lvl in LEVELS}
        order = []
        do_random = self.random_var.get() == "yes"
        for lvl in LEVELS:
            count = int(self.count_vars[lvl].get())
            if not 0 <= count <= 50:
                raise ValueError(self.ui("bad_count"))
            if count == 0:
                continue
            source = grouped[lvl][:]
            if do_random:
                random.shuffle(source)
            count = min(count, len(source))
            if not do_random:
                source = source[:count]
            else:
                source = source[:count]
                source.sort(key=lambda x: x.get("order_index", 9999))
            selected[lvl] = source
            if source:
                order.append(lvl)
        if not order:
            raise ValueError(self.ui("no_levels"))
        return selected, order

    def start_test(self) -> None:
        try:
            self.selected_questions, self.level_order = self._build_selection(self.lang_var.get())
        except Exception as e:
            self.status_var.set(str(e))
            return

        self.state = self._create_state()
        self._save_state()
        self._build_test_screen()
        self._show_current_question()
        self.status_var.set(self.ui("status_loaded"))

    def _create_state(self) -> dict:
        stats = {}
        for lvl in self.level_order:
            stats[lvl] = {
                "answered": 0,
                "correct": 0,
                "wrong": 0,
                "solution": 0,
                "hinted": 0,
                "points": 0.0,
                "max_points": len(self.selected_questions[lvl]) * LEVEL_POINTS[lvl],
                "completed": False,
            }
        return {
            "version": APP_VERSION,
            "lang": self.lang_var.get(),
            "random_questions": self.random_var.get() == "yes",
            "counts": {lvl: int(self.count_vars[lvl].get()) for lvl in LEVELS},
            "level_order": self.level_order,
            "selected_ids": {lvl: [q["id"] for q in self.selected_questions[lvl]] for lvl in LEVELS},
            "current_level_idx": 0,
            "current_question_idx": 0,
            "question_logs": [],
            "level_stats": stats,
        }

    def _questions_from_state(self, state: dict) -> tuple[dict[str, list[dict]], list[str]]:
        grouped = self._all_questions_grouped(state["lang"])
        by_id = {q["id"]: q for qs in grouped.values() for q in qs}
        selected = {lvl: [] for lvl in LEVELS}
        for lvl in LEVELS:
            selected[lvl] = [by_id[qid] for qid in state["selected_ids"].get(lvl, []) if qid in by_id]
        return selected, state["level_order"]

    def _save_state(self) -> None:
        if self.state is None:
            return
        GUI_STATE_PATH.write_text(json.dumps(self.state, ensure_ascii=False, indent=2), encoding="utf-8")

    def _try_resume(self) -> None:
        if not GUI_STATE_PATH.exists():
            return
        try:
            state = json.loads(GUI_STATE_PATH.read_text(encoding="utf-8"))
        except Exception:
            GUI_STATE_PATH.unlink(missing_ok=True)
            return
        if state.get("version") != APP_VERSION:
            GUI_STATE_PATH.unlink(missing_ok=True)
            return
        self.lang_var.set(state.get("lang", "en"))
        self.random_var.set("yes" if state.get("random_questions") else "no")
        for lvl in LEVELS:
            self.count_vars[lvl].set(int(state.get("counts", {}).get(lvl, 10)))
        self._refresh_welcome_locale()
        if messagebox.askyesno(self.ui("resume_title"), self.ui("resume_text")):
            self.state = state
            self.selected_questions, self.level_order = self._questions_from_state(state)
            self._build_test_screen()
            self._show_current_question()
        else:
            GUI_STATE_PATH.unlink(missing_ok=True)

    def _build_test_screen(self) -> None:
        self._destroy_frame(self.welcome_frame)
        self._destroy_frame(self.test_frame)
        self.test_frame = tk.Frame(self.root, bg=APP_BG)
        self.test_frame.pack(fill="both", expand=True, padx=14, pady=14)
        self.test_frame.grid_columnconfigure(0, weight=1)
        self.test_frame.grid_rowconfigure(0, weight=0)  # compact header
        self.test_frame.grid_rowconfigure(1, weight=1)  # main content
        self.test_frame.grid_rowconfigure(2, weight=0)  # status bar

        # COMPACT HEADER: title left, current info center, small logo right.
        header = Panel(self.test_frame)
        header.grid(row=0, column=0, sticky="ew", pady=(0, 10))
        header.grid_columnconfigure(0, weight=1)
        header.grid_columnconfigure(1, weight=2)
        header.grid_columnconfigure(2, weight=1)

        tk.Label(
            header,
            text=APP_TITLE,
            bg=APP_BG,
            fg=APP_FG,
            font=FONT_BIG,
            anchor="w",
        ).grid(row=0, column=0, sticky="w", padx=20, pady=10)

        self.meta_label = tk.Label(
            header,
            text="",
            bg=APP_BG,
            fg=APP_FG,
            font=FONT_UI,
            anchor="center",
        )
        self.meta_label.grid(row=0, column=1, sticky="ew", padx=10, pady=10)

        tk.Label(
            header,
            image=self._get_logo_image(),
            bg=APP_BG,
            bd=0,
            anchor="e",
        ).grid(row=0, column=2, sticky="e", padx=20, pady=6)

        # Main area: left feedback column, right work/question column.
        main = tk.Frame(self.test_frame, bg=APP_BG)
        main.grid(row=1, column=0, sticky="nsew")
        main.grid_columnconfigure(0, weight=3, uniform="main")
        main.grid_columnconfigure(1, weight=9, uniform="main")
        main.grid_rowconfigure(0, weight=1)

        # LEFT: hint on top, result/correct answer under it.
        left = tk.Frame(main, bg=APP_BG)
        left.grid(row=0, column=0, sticky="nsew", padx=(0, 8))
        left.grid_columnconfigure(0, weight=1)
        left.grid_rowconfigure(0, weight=2)
        left.grid_rowconfigure(1, weight=5)

        hint_panel = Panel(left)
        hint_panel.grid(row=0, column=0, sticky="nsew", pady=(0, 8))
        tk.Label(hint_panel, text=self.ui("hint"), bg=APP_BG, fg=APP_FG, font=FONT_TITLE).pack(anchor="w", padx=18, pady=(10, 6))
        self.hint_box = tk.Text(
            hint_panel,
            height=5,
            wrap="word",
            bg=APP_BG,
            fg=APP_FG,
            insertbackground=APP_FG,
            relief="flat",
            highlightthickness=1,
            highlightbackground=OUTLINE,
            font=FONT_UI,
            state="disabled",
        )
        self.hint_box.pack(fill="both", expand=True, padx=18, pady=(0, 10))

        result_panel = Panel(left)
        result_panel.grid(row=1, column=0, sticky="nsew")
        tk.Label(result_panel, text=self.ui("correct_answer"), bg=APP_BG, fg=APP_FG, font=FONT_TITLE).pack(anchor="w", padx=18, pady=(14, 8))
        self.feedback = tk.Text(
            result_panel,
            height=10,
            wrap="word",
            bg=APP_BG,
            fg=APP_FG,
            insertbackground=APP_FG,
            relief="flat",
            highlightthickness=1,
            highlightbackground=OUTLINE,
            font=FONT_FEEDBACK,
            state="disabled",
        )
        self.feedback.pack(fill="both", expand=True, padx=18, pady=(0, 18))

        # RIGHT: question, answer choices, answer entry and action buttons.
        right = Panel(main)
        right.grid(row=0, column=1, sticky="nsew", padx=(8, 0))
        right.grid_columnconfigure(0, weight=1)
        right.grid_rowconfigure(0, weight=1)  # question area expands
        right.grid_rowconfigure(1, weight=0)  # answer buttons have fixed 2-line height
        right.grid_rowconfigure(2, weight=0)  # entry
        right.grid_rowconfigure(3, weight=0)  # action buttons

        # Kept only as an internal variable; the visible "Multiple choice" line was wasted space.
        self.question_type = tk.Label(right, text="", bg=APP_BG, fg=SUBTLE, font=FONT_SMALL)

        self.question_text = tk.Text(
            right,
            height=8,
            wrap="word",
            bg=APP_BG,
            fg=APP_FG,
            insertbackground=APP_FG,
            relief="flat",
            highlightthickness=1,
            highlightbackground=OUTLINE,
            font=FONT_QUESTION,
            state="disabled",
        )
        self.question_text.grid(row=0, column=0, sticky="nsew", padx=18, pady=(16, 10))

        self.options_frame = tk.Frame(right, bg=APP_BG)
        self.options_frame.grid(row=1, column=0, sticky="ew", padx=18, pady=(0, 10))
        self.options_frame.grid_columnconfigure(0, weight=1)

        answer_frame = tk.Frame(right, bg=APP_BG)
        answer_frame.grid(row=2, column=0, sticky="ew", padx=18, pady=(0, 10))
        answer_frame.grid_columnconfigure(0, weight=1)
        self.answer_label = tk.Label(answer_frame, text=self.ui("answer_here"), bg=APP_BG, fg=APP_FG, font=FONT_UI)
        self.answer_label.grid(row=0, column=0, sticky="w", pady=(0, 6))
        self.answer_entry = tk.Entry(
            answer_frame,
            textvariable=self.answer_text,
            bg=INPUT_BG,
            fg=INPUT_FG,
            insertbackground=INPUT_FG,
            highlightbackground=OUTLINE,
            highlightthickness=1,
            relief="flat",
            font=FONT_UI,
        )
        self.answer_entry.grid(row=1, column=0, sticky="ew")
        self._add_tooltip(self.answer_entry, self.ui("tt_entry"))

        actions = tk.Frame(right, bg=APP_BG)
        actions.grid(row=3, column=0, sticky="ew", padx=18, pady=(0, 16))
        actions.grid_columnconfigure(0, weight=3)
        actions.grid_columnconfigure(1, weight=3)
        actions.grid_columnconfigure(2, weight=2)
        actions.grid_columnconfigure(3, weight=2)
        actions.grid_columnconfigure(4, weight=3)

        self.submit_button = TerminalButton(actions, text=self.ui("submit_answer"), command=self.submit_answer)
        self.submit_button.grid(row=0, column=0, sticky="ew", padx=(0, 8))
        self._add_tooltip(self.submit_button, self.ui("tt_submit"))
        self.next_button = OutlineButton(actions, text=self.ui("next_question"), command=self.next_question)
        self.next_button.grid(row=0, column=1, sticky="ew", padx=8)
        self._add_tooltip(self.next_button, self.ui("tt_next"))
        self.hint_button = OutlineButton(actions, text=self.ui("hint"), command=self.show_hint)
        self.hint_button.grid(row=0, column=2, sticky="ew", padx=8)
        self._add_tooltip(self.hint_button, self.ui("tt_hint"))
        self.solution_button = OutlineButton(actions, text=self.ui("solution"), command=self.show_solution)
        self.solution_button.grid(row=0, column=3, sticky="ew", padx=8)
        self._add_tooltip(self.solution_button, self.ui("tt_solution"))
        self.save_quit_button = OutlineButton(actions, text=self.ui("save_quit"), command=self.save_and_quit)
        self.save_quit_button.grid(row=0, column=4, sticky="ew", padx=(8, 0))
        self._add_tooltip(self.save_quit_button, self.ui("tt_save_quit"))

        status = Panel(self.test_frame)
        status.grid(row=2, column=0, sticky="ew", pady=(10, 0))
        tk.Label(status, textvariable=self.status_line1_var, bg=APP_BG, fg=APP_FG, font=FONT_SMALL, anchor="w").pack(fill="x", padx=12, pady=(6, 1))
        tk.Label(status, textvariable=self.status_line2_var, bg=APP_BG, fg=SUBTLE, font=FONT_SMALL, anchor="w").pack(fill="x", padx=12, pady=(1, 6))

        self.answer_entry.focus_set()

    def _current_level(self) -> str:
        return self.state["level_order"][self.state["current_level_idx"]]

    def _current_questions(self) -> list[dict]:
        return self.selected_questions[self._current_level()]

    def _current_total_questions(self) -> int:
        return sum(len(self.selected_questions[l]) for l in self.level_order)

    def _current_absolute_index(self) -> int:
        idx = self.state["current_question_idx"]
        for i in range(self.state["current_level_idx"]):
            idx += len(self.selected_questions[self.level_order[i]])
        return idx + 1

    def _safe_word_wrap(self, text: str, width: int) -> str:
        """Wrap prose lines by words while preserving readable code lines."""
        if not text:
            return ""

        wrapped_lines: list[str] = []

        for raw_line in str(text).splitlines():
            line = raw_line.rstrip()

            if not line:
                wrapped_lines.append("")
                continue

            stripped = line.lstrip()
            is_indented_code = line.startswith((" ", "\t"))
            is_code_like = any(token in stripped for token in ("def ", "print(", "return ", "=", "[", "]", "{", "}", "lambda"))

            if is_indented_code or (is_code_like and len(line) <= width):
                wrapped_lines.append(line)
                continue

            wrapped = textwrap.wrap(
                line,
                width=width,
                break_long_words=False,
                break_on_hyphens=False,
                replace_whitespace=False,
                drop_whitespace=True,
            )

            wrapped_lines.extend(wrapped if wrapped else [line])

        return "\n".join(wrapped_lines)

    def _format_question_text(self, text: str) -> str:
        return self._safe_word_wrap(text, 82)

    def _format_side_text(self, text: str) -> str:
        return self._safe_word_wrap(text, 31)

    def _show_current_question(self) -> None:
        level = self._current_level()
        questions = self._current_questions()
        idx = self.state["current_question_idx"]
        if idx >= len(questions):
            self._finish_level()
            return

        q = questions[idx]
        self.current_question = q
        self.question_answered = False
        self.hint_used_current = False
        self.answer_text.set("")
        self.current_feedback = ""

        self.meta_label.config(
            text=f"{self.ui('question_counter')} {self._current_absolute_index()}/{self._current_total_questions()}   [{q.get('id','')}]   {self.level_label(level)}"
        )
        self.question_type.config(text=self.ui("question_type_choice") if q["type"] == "choice" else self.ui("question_type_text"))

        self.question_text.config(state="normal")
        self.question_text.delete("1.0", tk.END)
        self.question_text.insert("1.0", self._format_question_text(q["question"]))
        self.question_text.config(state="disabled")

        for child in self.options_frame.winfo_children():
            child.destroy()
        self.option_buttons = []

        if q["type"] == "choice":
            self.options_frame.grid()
            self.options_frame.grid_columnconfigure(0, weight=1)
            parsed_options = parse_options(q.get("options", []))

            # v1.0.13: always stack A/B/C vertically.
            # Each choice button is exactly two text lines high; long translated
            # answers wrap inside the button instead of disappearing or stretching
            # the whole layout.
            for index, (letter, text) in enumerate(parsed_options):
                full = f"{letter.upper()}) {text}" if letter else text
                self.options_frame.grid_rowconfigure(index, weight=0, minsize=58)
                btn = TerminalButton(
                    self.options_frame,
                    text=full,
                    anchor="w",
                    justify="left",
                    wraplength=980,
                    height=2,
                    font=FONT_OPTION,
                    padx=12,
                    pady=4,
                    command=lambda l=letter, f=full: self._select_option(l, f),
                )
                btn.grid(row=index, column=0, sticky="ew", padx=0, pady=4)
                self._add_tooltip(btn, self.ui("tt_option").format(answer=full))
                self.option_buttons.append(btn)
        else:
            # Keep the row stable even for text questions.
            spacer = tk.Label(self.options_frame, text="", bg=APP_BG, fg=APP_FG, font=FONT_UI)
            spacer.grid(row=0, column=0, sticky="ew", pady=4)

        # New question must start with clean side panels.
        # This avoids carrying the previous correct answer/explanation forward.
        self._set_hint("")
        self._set_feedback("")
        self.current_feedback = ""

        # v1.0.15: On the last question of the current level, the "Next question"
        # button becomes a finish/evaluate button. The command stays the same,
        # because next_question() already triggers level/test completion when
        # there is no next question.
        if hasattr(self, "next_button"):
            is_last_question = (idx == len(questions) - 1)
            self.next_button.config(
                text=self.ui("finish_button") if is_last_question else self.ui("next_question")
            )

        self._refresh_status()
        self.root.update_idletasks()
        self.answer_entry.focus_set()

    def _select_option(self, letter: str, full: str) -> None:
        self.answer_text.set(letter.upper() if letter else full)
        self.answer_entry.focus_set()

    def _set_hint(self, text: str) -> None:
        if not hasattr(self, "hint_box"):
            return
        self.hint_box.config(state="normal")
        self.hint_box.delete("1.0", tk.END)
        self.hint_box.insert("1.0", self._format_side_text(text))
        self.hint_box.config(state="disabled")

    def _set_feedback(self, text: str) -> None:
        self.current_feedback = text
        if not hasattr(self, "feedback"):
            return
        self.feedback.config(state="normal")
        self.feedback.delete("1.0", tk.END)
        self.feedback.insert("1.0", self._format_side_text(text))
        self.feedback.config(state="disabled")

    def _hint_word(self, n: int) -> tuple[str, str]:
        lang = self.lang_var.get()
        if lang == "sk":
            if n == 1:
                return "Použitá", "nápoveda"
            if 2 <= n <= 4:
                return "Použité", "nápovedy"
            return "Použitých", "nápoved"
        if lang == "cz":
            if n == 1:
                return "Použita", "nápověda"
            if 2 <= n <= 4:
                return "Použity", "nápovědy"
            return "Použito", "nápověd"
        return "", ""

    def _format_status_lines(self, answered: int, total: int, gained: float, maximum: float, hints: int, correct: int, wrong: int, solutions: int) -> tuple[str, str]:
        gained_txt = str(round(gained, 1))
        max_txt = str(round(maximum, 1))
        lang = self.lang_var.get()
        if lang == "sk":
            used_word, hint_word = self._hint_word(hints)
            return (
                f"Zodpovedané: {answered} / {total} | Body: {gained_txt} / {max_txt}",
                f"{used_word} {hints} {hint_word} | Správne: {correct} | Nesprávne: {wrong} | Riešenia: {solutions}",
            )
        if lang == "cz":
            used_word, hint_word = self._hint_word(hints)
            return (
                f"Zodpovězeno: {answered} / {total} | Body: {gained_txt} / {max_txt}",
                f"{used_word} {hints} {hint_word} | Správně: {correct} | Špatně: {wrong} | Řešení: {solutions}",
            )
        if lang == "es":
            return (
                f"Respondidas: {answered} / {total} | Puntos: {gained_txt} / {max_txt}",
                f"Pistas usadas: {hints} | Correctas: {correct} | Incorrectas: {wrong} | Soluciones: {solutions}",
            )
        return (
            f"Answered: {answered} / {total} | Points: {gained_txt} / {max_txt}",
            f"Hints used: {hints} | Correct: {correct} | Wrong: {wrong} | Solutions: {solutions}",
        )

    def _log_question(self, level: str, q: dict, status_key: str, user_answer: str, used_hint: bool, points: float) -> None:
        self.state["question_logs"].append({
            "id": q.get("id", ""),
            "level": level,
            "status_key": status_key,
            "user_answer": user_answer,
            "correct_answer": get_correct_display(q),
            "used_hint": used_hint,
            "question": q["question"],
            "explanation": q["explanation"],
            "points_awarded": round(points, 1),
            "max_points": LEVEL_POINTS[level],
        })

    def _refresh_status(self) -> None:
        if self.state is None:
            return
        gained = sum(self.state["level_stats"][lvl]["points"] for lvl in self.level_order)
        maximum = sum(self.state["level_stats"][lvl]["max_points"] for lvl in self.level_order)
        answered = sum(self.state["level_stats"][lvl]["answered"] for lvl in self.level_order)
        correct = sum(self.state["level_stats"][lvl]["correct"] for lvl in self.level_order)
        wrong = sum(self.state["level_stats"][lvl]["wrong"] for lvl in self.level_order)
        hints = sum(self.state["level_stats"][lvl]["hinted"] for lvl in self.level_order)
        solutions = sum(self.state["level_stats"][lvl]["solution"] for lvl in self.level_order)
        total = self._current_total_questions()
        self.score_var.set(f"{correct} / {total}")
        self.points_var.set(f"{round(gained,1)} / {round(maximum,1)}")
        self.progress_var.set(f"{answered} / {total}")
        line1, line2 = self._format_status_lines(answered, total, gained, maximum, hints, correct, wrong, solutions)
        self.status_line1_var.set(line1)
        self.status_line2_var.set(line2)

    def _advance(self) -> None:
        self.state["current_question_idx"] += 1
        self._save_state()

    def show_hint(self) -> None:
        if self.current_question is None or self.question_answered:
            return
        self.hint_used_current = True
        self.status_var.set(self.ui("status_hint"))
        self._set_hint(f"{self.ui('hint_prefix')} {self.current_question.get('hint','...')}\n\n{self.ui('status_hint')}")
        if hasattr(self, "answer_entry"):
            self.answer_entry.focus_set()

    def show_solution(self) -> None:
        if self.current_question is None or self.question_answered:
            return
        level = self._current_level()
        stats = self.state["level_stats"][level]
        self.question_answered = True
        stats["answered"] += 1
        stats["solution"] += 1
        if self.hint_used_current:
            stats["hinted"] += 1
        self._log_question(level, self.current_question, "status_solution", "?", self.hint_used_current, 0.0)
        self.status_var.set(self.ui("status_solution"))
        self._set_feedback(f"{self.ui('correct_answer')} {get_correct_display(self.current_question)}\n\n{self.ui('explanation')} {self.current_question['explanation']}")
        self._advance()
        self._refresh_status()
        if hasattr(self, "answer_entry"):
            self.answer_entry.focus_set()

    def submit_answer(self) -> None:
        if self.current_question is None or self.question_answered:
            return
        ans = self.answer_text.get().strip()
        if not ans:
            self.status_var.set(self.ui("pick_answer"))
            return
        level = self._current_level()
        stats = self.state["level_stats"][level]
        stats["answered"] += 1
        if self.hint_used_current:
            stats["hinted"] += 1
        self.question_answered = True
        if is_correct_answer(self.current_question, ans):
            points = max(0.0, LEVEL_POINTS[level] - (0.5 if self.hint_used_current else 0.0))
            stats["correct"] += 1
            stats["points"] = round(stats["points"] + points, 1)
            self._log_question(level, self.current_question, "status_correct", ans, self.hint_used_current, points)
            self.status_var.set(self.ui("status_correct"))
            header = self.ui("status_correct")
        else:
            points = 0.0
            stats["wrong"] += 1
            self._log_question(level, self.current_question, "status_wrong", ans, self.hint_used_current, points)
            self.status_var.set(self.ui("status_wrong"))
            header = self.ui("status_wrong")
        self._set_feedback(f"{header}\n\n{self.ui('correct_answer')} {get_correct_display(self.current_question)}\n\n{self.ui('explanation')} {self.current_question['explanation']}")
        self._advance()
        self._refresh_status()
        if hasattr(self, "answer_entry"):
            self.answer_entry.focus_set()

    def next_question(self) -> None:
        if self.test_frame is None:
            return
        self._show_current_question()

    def _finish_level(self) -> None:
        level = self._current_level()
        stats = self.state["level_stats"][level]
        stats["completed"] = True
        percent = round((stats["points"] / stats["max_points"]) * 100, 1) if stats["max_points"] else 0.0
        grade = get_grade(percent)
        recommendation_key = get_recommendation_key(level, percent)
        texts = self.texts()
        summary = (
            f"{self.ui('level_result')}\n\n"
            f"{texts['score']} {stats['correct']} / {len(self.selected_questions[level])}\n"
            f"{texts['points_word']}: {round(stats['points'],1)} / {round(stats['max_points'],1)}\n"
            f"{texts['success_rate']} {percent}%\n"
            f"{texts['grade']} {grade}\n"
            f"{texts['recommendation']}: {texts[recommendation_key]}"
        )
        self._set_feedback(summary)
        next_idx = self.state["current_level_idx"] + 1
        if next_idx < len(self.level_order):
            next_level = self.level_order[next_idx]
            if messagebox.askyesno(APP_TITLE, self.ui("continue_next").format(next_level=self.level_label(next_level))):
                self.state["current_level_idx"] = next_idx
                self.state["current_question_idx"] = 0
                self._save_state()
                self._show_current_question()
                return
        self._finish_all()

    def _report_path(self, final: bool) -> Path:
        ts = datetime.now().strftime("%Y%m%d_%H%M%S")
        suffix = "final" if final else "partial"
        return REPORTS_DIR / f"report_{self.lang_var.get()}_{suffix}_{ts}.txt"

    def _save_report(self, final: bool) -> Path:
        texts = self.texts()
        path = self._report_path(final)
        gained = sum(self.state["level_stats"][lvl]["points"] for lvl in self.level_order)
        maximum = sum(self.state["level_stats"][lvl]["max_points"] for lvl in self.level_order)
        lines = [f"PyTrainerEdu v{APP_VERSION} report", "=" * 60, f"Language: {self.lang_var.get()}", f"Status: {'Complete' if final else 'Interrupted'}", ""]
        for lvl in self.level_order:
            stats = self.state["level_stats"][lvl]
            percent = round((stats["points"] / stats["max_points"]) * 100, 1) if stats["max_points"] else 0.0
            grade = get_grade(percent)
            recommendation_key = get_recommendation_key(lvl, percent)
            lines.append(
                f"{self.level_label(lvl)}: {stats['answered']}/{len(self.selected_questions[lvl])} | "
                f"OK {stats['correct']} | Wrong {stats['wrong']} | Solution {stats['solution']} | "
                f"Points {round(stats['points'],1)}/{round(stats['max_points'],1)} | Grade {grade} | "
                f"Recommendation: {texts[recommendation_key]}"
            )
        lines += ["", "Details", "-" * 60]
        for row in self.state["question_logs"]:
            lines += [
                f"[{row['id']}] {self.level_label(row['level'])} | {row['status_key']}",
                row["question"],
                f"User answer: {row['user_answer']}",
                f"Correct answer: {row['correct_answer']}",
                f"Hint used: {'yes' if row['used_hint'] else 'no'}",
                f"Points awarded: {row['points_awarded']} / {row['max_points']}",
                f"Explanation: {row['explanation']}",
                "-" * 60,
            ]
        lines += ["", f"Total points: {round(gained,1)} / {round(maximum,1)}"]
        path.write_text("\n".join(lines), encoding="utf-8")
        return path

    def _finish_all(self) -> None:
        path = self._save_report(final=True)
        self.status_var.set(self.ui("status_finished"))
        self._set_feedback(f"{self.ui('final_result')}\n\n{self.ui('result_saved')} {path}")
        GUI_STATE_PATH.unlink(missing_ok=True)
        messagebox.showinfo(APP_TITLE, self.ui("saved_final").format(path=path))
        self._build_welcome_screen()
        self.state = None

    def save_and_quit(self) -> None:
        if self.state is None:
            return
        self._save_state()
        path = self._save_report(final=False)
        messagebox.showinfo(APP_TITLE, self.ui("saved_partial").format(path=path))
        self._build_welcome_screen()
        self.state = None

    def on_close(self) -> None:
        if self.state is None:
            self.root.destroy()
            return
        answer = messagebox.askyesnocancel(self.ui("close_title"), self.ui("close_text"))
        if answer is None:
            return
        if answer:
            self._save_state()
            path = self._save_report(final=False)
            messagebox.showinfo(APP_TITLE, self.ui("saved_partial").format(path=path))
        else:
            GUI_STATE_PATH.unlink(missing_ok=True)
            messagebox.showinfo(APP_TITLE, self.ui("discarded"))
        self.root.destroy()


def main() -> None:
    root = tk.Tk()
    PyTrainerGuiV1(root)
    root.mainloop()


if __name__ == "__main__":
    main()
