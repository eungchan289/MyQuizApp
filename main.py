import random
import csv
from datetime import datetime
import math
from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.image import Image
from kivy.uix.popup import Popup
from kivy.uix.textinput import TextInput
from kivy.core.text import LabelBase, DEFAULT_FONT
from kivy.core.window import Window
from kivy.clock import Clock
from kivy.graphics import Color, Mesh, Line, Rectangle
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.uix.floatlayout import FloatLayout
from kivy.metrics import dp

# --- 파일 경로 설정 ---
# 모든 폰트와 이미지 파일이 이 코드 파일과 **같은 폴더** 안에 있는지 확인해주세요.
DEFAULT_FONT_PATH = "NanumGothic.ttf"
EMOJI_FONT_PATH = "seguiemj.ttf"
CORRECT_IMAGE_PATH = 'Correct.jpg'
WRONG_IMAGE_PATH = 'Wrong.jpg'
RECORD_IMAGE_PATH = 'Recordbreak.jpg'
IMAGE_40_30_PATH = 'Image1_Happy.jpg'
IMAGE_29_20_PATH = 'Image2_Smile.jpg'
IMAGE_19_10_PATH = 'Image3_Concerned.jpg'
IMAGE_9_1_PATH = 'Image4_Sad.jpg'

# --- Special 모드 이미지 경로 ---
SPECIAL_CORRECT_IMAGE_PATH = 'Specialcorrect.jpg'
SPECIAL_WRONG_IMAGE_PATH = 'SpecialWrong.jpg'
SPECIAL_IMAGE_1ST = 'Special1st.jpg'
SPECIAL_IMAGE_2ND = 'Special2nd.jpg'
SPECIAL_IMAGE_3RD = 'Special3rd.jpg'
SPECIAL_IMAGE_4TH = 'Special4th.jpg'

try:
    LabelBase.register(DEFAULT_FONT, DEFAULT_FONT_PATH)
    LabelBase.register("emoji", EMOJI_FONT_PATH)
except IOError:
    print(f"폰트 파일을 찾을 수 없습니다: {DEFAULT_FONT_PATH} 또는 {EMOJI_FONT_PATH}")

TIME_LIMIT = 40

# --- 기존 영어 단어 퀴즈 데이터 ---
ENGLISH_WORD_QUIZ = {
    "Something that is grinding causes people or activities to lose energy and spirit.": "grinding",
    "gradually making something weaker and destroying it, especially the strength or confidence of an enemy by repeatedly attacking it.": "attrition",
    "to think about something too much and find it difficult to stop.": "fixate",
    "a change in the way you do or think about something.": "recalibration",
    "the act or process of forcing people by law to join the armed services.": "conscription",
    "to make a picture or idea appear in someone's mind.": "conjure something up",
    "extremely optimistic, especially in the face of unrelieved hardship or adversity.": "panglossian",
    "to make the sound of heavy objects hitting together, or to cause this sound to be made.": "clunk",
    "helping poor people, especially by giving them money.": "philanthropic",
    "to examine something very carefully in order to discover information.": "scrutinize",
    "speech or writing that is nonsense.": "guff",
    "an expert in a particular subject who gives advice.": "guru",
    "an activity, group, etc., that has become successful or fashionable and so attracts many new people.": "bandwagon",
    "always being careful to notice things, especially possible danger.": "vigilant",
    "collaborations between businesses, civil society and other stakeholders that seek to address issues of mutual concern, including human rights and sustainability.": "multi-stakeholder initiatives",
    "to make something weaker or worse in quality.": "impoverish",
    "to make a formal judgment to decide an argument.": "arbitrate",
    "a way of talking or behaving that is too proud.": "hubris",
    "to (cause to) move up and down and/or from side to side with small, quick movements.": "wiggle",
    "to use something carefully so that you do not use all of it.": "husband",
    "knowing a lot about modern technology, especially computers.": "tech-savvy",
    "to increase activity or the level of something.": "ramp something up",
    "having no excitement, interest, or new and different events.": "humdrum",
    "very large guns that are moved on wheels or metal tracks, or the part of the army that uses these.": "artillery",
    "freedom from punishment or from the unpleasant results of something that has been done.": "impunity",
    "trying to seem very important or serious, but without having a good reason for doing so and looking silly as a result.": "highfalutin",
    "to go down in amount or value very quickly and suddenly.": "plunge",
    "involving or affecting two different organizations, countries, etc.": "bilateral",
    "the action of continuously firing large guns to protect soldiers advancing on an enemy.": "barrage",
    "to cause someone to suddenly take action, especially by shocking or exciting them in some way.": "galvanize",
    "tome": "a large, heavy book.",
    "trailblazer": "the first person, company, etc. to do something new.",
    "miasma": "an unpleasant fog that smells bad.",
    "exponential": "becoming quicker and quicker.",
    "chrysalis": "a moth or butterfly at the stage of development when it is covered by a hard case, before it becomes an adult insect with wings, or the case itself.",
    "u-bend": "a line on a graph that starts high, gets much lower, and then rises again, giving it the shape of the letter 'U'. It is also used to refer to situations in which something decreases and then increases again.",
    "reciprocity": "a situation in which two groups agree to help each other by behaving in the same way or by giving each other similar advantages.",
    "rambling": "too long and confused.",
    "bill": "a formal statement of a planned new law that is discussed before being voted on.",
}

class SpeechBubble(FloatLayout):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.label = Label(
            text="",
            font_size='16sp',
            color=(0, 0, 0, 1),
            halign='center',
            valign='center',
            size_hint=(0.8, 0.7),
            pos_hint={'center_x': 0.45, 'center_y': 0.55}
        )
        self.add_widget(self.label)
        self.bind(pos=self.update_canvas, size=self.update_canvas)
        self.update_canvas()

    def update_canvas(self, *args):
        self.canvas.before.clear()
        body_width_ratio = 0.85
        center_x = self.x + (self.width * body_width_ratio) / 2
        center_y = self.y + self.height / 2
        radius_x = (self.width * body_width_ratio) / 2
        radius_y = self.height / 2
        points = []
        num_segments = 60
        tail_start_angle_deg = 310
        tail_end_angle_deg = 340
        for i in range(num_segments + 1):
            angle_deg = (360 / num_segments) * i
            if not (tail_start_angle_deg <= angle_deg <= tail_end_angle_deg):
                angle_rad = math.radians(angle_deg)
                px = center_x + radius_x * math.cos(angle_rad)
                py = center_y + radius_y * math.sin(angle_rad)
                points.append((px, py))
        p1_angle_rad = math.radians(tail_start_angle_deg)
        p1_x = center_x + radius_x * math.cos(p1_angle_rad)
        p1_y = center_y + radius_y * math.sin(p1_angle_rad)
        p2_x = self.x + self.width * 0.95
        p2_y = self.y - dp(5)
        p3_angle_rad = math.radians(tail_end_angle_deg)
        p3_x = center_x + radius_x * math.cos(p3_angle_rad)
        p3_y = center_y + radius_y * math.sin(p3_angle_rad)
        insert_index_p1 = 0
        min_dist_p1 = float('inf')
        for i, (px, py) in enumerate(points):
            dist = (px - p1_x)**2 + (py - p1_y)**2
            if dist < min_dist_p1:
                min_dist_p1 = dist
                insert_index_p1 = i + 1
        points.insert(insert_index_p1, (p1_x, p1_y))
        points.insert(insert_index_p1 + 1, (p2_x, p2_y))
        points.insert(insert_index_p1 + 2, (p3_x, p3_y))
        vertices = []
        for p in points:
            vertices.extend([p[0], p[1], 0, 0])
        indices = list(range(len(points)))
        with self.canvas.before:
            Color(1, 1, 1, 1)
            Mesh(vertices=vertices, indices=indices, mode='triangle_fan')
            Color(0, 0, 0, 1)
            Line(points=[coord for p in points for coord in p], close=True, width=1.5)

    def update_text(self, new_text):
        self.label.text = new_text

class BackgroundLabel(Label):
    def __init__(self, color=(1, 0, 0, 1), **kwargs):
        self.color_val = color
        super().__init__(**kwargs)
        self.bind(size=self.update_canvas, pos=self.update_canvas)
        self.update_canvas()

    def update_canvas(self, *args):
        self.canvas.before.clear()
        with self.canvas.before:
            Color(*self.color_val)
            Rectangle(pos=self.pos, size=self.size)

class StartScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        layout = BoxLayout(orientation='vertical', padding=100, spacing=40)
        title_label = Label(text="퀴즈!", font_size='80sp', bold=True, size_hint_y=0.3)
        center_image = Image(source=IMAGE_29_20_PATH, size_hint_y=0.5, allow_stretch=True, keep_ratio=True)
        start_button = Button(text="Start", font_size='40sp', size_hint_y=0.2)
        start_button.bind(on_press=self.go_to_difficulty_screen)
        layout.add_widget(title_label)
        layout.add_widget(center_image)
        layout.add_widget(start_button)
        self.add_widget(layout)

    def go_to_difficulty_screen(self, instance):
        self.manager.current = 'difficulty'

class DifficultyScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        layout = BoxLayout(orientation='vertical', padding=100, spacing=20)
        title = Label(text="Select the difficulty", font_size='60sp', bold=True, size_hint_y=0.3)
        easy_btn = Button(text="Easy", font_size='30sp', background_color=(0.1, 0.8, 0.1, 1))
        normal_btn = Button(text="Normal", font_size='30sp', background_color=(0.1, 0.5, 1, 1))
        hard_btn = Button(text="Hard", font_size='30sp', background_color=(1, 1, 0.2, 1))
        very_hard_btn = Button(text="Very Hard", font_size='30sp', background_color=(1, 0.2, 0.2, 1))
        special_btn = Button(text="Special", font_size='30sp', background_color=(0.5, 0.2, 0.8, 1))
        easy_btn.bind(on_press=self.select_difficulty)
        normal_btn.bind(on_press=self.select_difficulty)
        hard_btn.bind(on_press=self.select_difficulty)
        very_hard_btn.bind(on_press=self.select_difficulty)
        special_btn.bind(on_press=self.select_difficulty)
        layout.add_widget(title)
        layout.add_widget(easy_btn)
        layout.add_widget(normal_btn)
        layout.add_widget(hard_btn)
        layout.add_widget(very_hard_btn)
        layout.add_widget(special_btn)
        self.add_widget(layout)

    def select_difficulty(self, instance):
        difficulty_level = instance.text
        App.get_running_app().set_difficulty(difficulty_level)
        self.manager.current = 'quiz'

class QuizScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.bind(on_enter=self.setup_game)

    def setup_game(self, *args):
        self.clear_widgets()
        self.app = App.get_running_app()
        self.app.initialize_game_data()
        self.build_quiz_layout()
        Clock.schedule_once(self.app.start_game_logic)

    def build_quiz_layout(self):
        main_layout = BoxLayout(orientation='vertical', padding=[50, 20, 50, 50], spacing=20)
        header_area = BoxLayout(orientation='vertical', size_hint_y=0.25, spacing=5, padding=[0, 5, 0, 5])
        self.app.bar_progress_area = BoxLayout(size_hint_y=0.4)
        self.app.bar_fill = BackgroundLabel(color=(0.1, 0.5, 0.8, 1), size_hint_x=1.0)
        self.app.bar_empty = BackgroundLabel(color=(0.8, 0.8, 0.8, 1), size_hint_x=0.0)
        self.app.bar_progress_area.add_widget(self.app.bar_fill)
        self.app.bar_progress_area.add_widget(self.app.bar_empty)
        info_layout = BoxLayout(orientation='horizontal', size_hint_y=0.6, spacing=20)
        self.app.time_display_label = Label(text=f"00:{TIME_LIMIT:02d}", font_size='35sp', bold=True, size_hint_x=0.15, halign='left', valign='center')
        self.app.difficulty_label = Label(text=f"{self.app.difficulty}", font_size='25sp', size_hint_x=0.2, halign='left', valign='center')
        self.app.score_label = Label(text=f"점수: {self.app.score}점", font_size='30sp', size_hint_x=0.35, halign='center', valign='center')
        heart_container = BoxLayout(orientation='horizontal', size_hint_x=0.3, spacing=5)
        self.app.hearts = [Label(text='💖', font_size='35sp', font_name='emoji', size_hint_x=None, width=50) for _ in range(3)]
        heart_container.add_widget(BoxLayout())
        for heart in self.app.hearts:
            heart_container.add_widget(heart)
        info_layout.add_widget(self.app.time_display_label)
        info_layout.add_widget(self.app.difficulty_label)
        info_layout.add_widget(self.app.score_label)
        info_layout.add_widget(heart_container)
        header_area.add_widget(self.app.bar_progress_area)
        header_area.add_widget(info_layout)
        main_layout.add_widget(header_area)
        
        character_and_speech_layout = FloatLayout(size_hint_y=1.5)
        self.app.result_image = Image(source=IMAGE_40_30_PATH, allow_stretch=True, keep_ratio=True, size_hint=(1, 1), pos_hint={'center_x': 0.5, 'center_y': 0.5})
        self.app.speech_bubble = SpeechBubble(
            size_hint=(0.18, 0.25),
            pos_hint={'x': 0.24, 'y': 0.8}
        )
        
        self.app.pause_button = Button(
            text='▶',
            font_size='25sp',
            color=(1, 1, 1, 1),
            background_color=(0, 0, 0, 1),
            size_hint=(None, None),
            size=(dp(45), dp(45)),
            pos_hint={'right': 0.97, 'top': 0.88}
        )
        self.app.pause_button.background_normal = ''
        self.app.pause_button.background_down = ''
        self.app.pause_button.bind(on_press=self.app.pause_game)

        # 보너스 문제를 표시할 BoxLayout 생성
        self.app.bonus_display_layout = BoxLayout(
            orientation='horizontal',
            size_hint=(None, None),
            size=(dp(200), dp(50)),
            pos_hint={'right': 0.95, 'top': 0.7},
            spacing=dp(5)
        )

        # 별 이모티콘 Label
        self.app.bonus_star_label = Label(
            text="⭐",
            font_size='25sp',
            color=(1, 1, 0, 1),
            font_name='emoji',
            size_hint_x=None,
            width=dp(40),
            valign='middle'
        )
        # "보너스!" 텍스트 Label
        self.app.bonus_text_label = Label(
            text="보너스!",
            font_size='25sp',
            color=(1, 1, 0, 1),
            bold=True,
            font_name=DEFAULT_FONT,
            size_hint_x=None,
            width=dp(120),
            valign='middle'
        )
        
        self.app.bonus_display_layout.add_widget(self.app.bonus_star_label)
        self.app.bonus_display_layout.add_widget(self.app.bonus_text_label)
        self.app.bonus_display_layout.opacity = 0

        character_and_speech_layout.add_widget(self.app.result_image)
        character_and_speech_layout.add_widget(self.app.speech_bubble)
        character_and_speech_layout.add_widget(self.app.pause_button)
        character_and_speech_layout.add_widget(self.app.bonus_display_layout)

        main_layout.add_widget(character_and_speech_layout)
        self.app.question_label = Label(text="", font_size='30sp', bold=True, halign='center', size_hint_y=0.5, padding=(20,0))
        self.app.answer_input = TextInput(multiline=False, font_size='20sp', size_hint_y=0.2, disabled=True)
        submission_layout = BoxLayout(orientation='horizontal', size_hint_y=0.2, spacing=10)
        self.app.submit_button = Button(text="정답 제출", font_size='25sp', size_hint_x=0.7)
        self.app.submit_button.bind(on_press=self.app.check_answer)
        self.app.hint_button = Button(text="힌트", font_size='25sp', size_hint_x=0.3)
        self.app.hint_button.bind(on_press=self.app.use_hint)
        submission_layout.add_widget(self.app.submit_button)
        submission_layout.add_widget(self.app.hint_button)
        main_layout.add_widget(self.app.question_label)
        main_layout.add_widget(self.app.answer_input)
        main_layout.add_widget(submission_layout)
        self.add_widget(main_layout)

class QuizApp(App):
    def build(self):
        Window.size = (1280, 1080)
        self.sm = ScreenManager()
        self.difficulty = "Normal"
        self.pause_popup = None
        self.sm.add_widget(StartScreen(name='start'))
        self.sm.add_widget(DifficultyScreen(name='difficulty'))
        self.sm.add_widget(QuizScreen(name='quiz'))
        return self.sm

    def set_difficulty(self, level):
        self.difficulty = level

    def initialize_game_data(self):
        self.timer_event = None
        if self.difficulty == "Special":
            self.items = self.generate_math_problems()
        else:
            self.items = list(ENGLISH_WORD_QUIZ.items())
        random.shuffle(self.items)
        self.score = 0
        self.wrong_answers = 0
        self.current_question_index = 0
        self.time_left = TIME_LIMIT
        self.quiz_active = True
        self.paused = False
        self.hint_used_this_question = False
        self.is_bonus_question = False

    def generate_math_problems(self):
        problems = []
        for i in range(50):
            # 2단계: 두 자릿수 덧셈, 뺄셈, 곱셈, 나눗셈
            if i < 15:
                op = random.choice(['+', '-', '*', '/'])
                if op == '+':
                    a, b = random.randint(10, 99), random.randint(10, 99)
                    answer = a + b
                    question = f"{a} + {b} = ?"
                elif op == '-':
                    a, b = random.randint(50, 150), random.randint(10, 99)
                    answer = a - b
                    question = f"{a} - {b} = ?"
                elif op == '*':
                    a, b = random.randint(10, 20), random.randint(10, 20)
                    answer = a * b
                    question = f"{a} * {b} = ?"
                else: # '/'
                    b = random.randint(10, 20)
                    a = random.randint(10, 20) * b
                    answer = a // b
                    question = f"{a} / {b} = ?"
                problems.append((question, str(answer)))
            # 3단계: 두 방정식의 교점, 연립방정식, 인수분해, 다항식 미분, 삼각함수
            elif i < 35:
                problem_type = random.randint(0, 4)
                if problem_type == 0: # 두 방정식의 교점
                    m1 = random.randint(1, 5)
                    b1 = random.randint(-10, 10)
                    m2 = random.randint(1, 5)
                    b2 = random.randint(-10, 10)
                    if m1 == m2: m2 += 1
                    x_ans = (b2 - b1) / (m1 - m2)
                    y_ans = m1 * x_ans + b1
                    question = f"What is the intersection point (x, y) of y = {m1}x + {b1} and y = {m2}x + {b2}? (Round to 2 decimal places)"
                    answer = f"({round(x_ans, 2)}, {round(y_ans, 2)})"
                elif problem_type == 1: # 연립방정식
                    x_ans, y_ans = random.randint(1, 5), random.randint(1, 5)
                    a1, b1 = random.randint(1, 5), random.randint(1, 5)
                    c1 = a1 * x_ans + b1 * y_ans
                    a2, b2 = random.randint(1, 5), random.randint(1, 5)
                    c2 = a2 * x_ans + b2 * y_ans
                    question = f"What is x+y if {a1}x + {b1}y = {c1} and {a2}x + {b2}y = {c2}?"
                    answer = x_ans + y_ans
                elif problem_type == 2: # 인수분해
                    a = random.randint(1, 5)
                    b = random.randint(1, 5)
                    c = a * b
                    d = a + b
                    question = f"Factorize x^2 + {d}x + {c}. Provide the positive root."
                    answer = max(-a, -b)
                elif problem_type == 3: # 다항식 미분
                    a = random.randint(1, 3)
                    b = random.randint(1, 5)
                    c = random.randint(1, 10)
                    x = random.randint(1, 3)
                    question = f"If f(x) = {a}x^3 + {b}x^2 + {c}, what is f'({x})?"
                    answer = 3*a*x**2 + 2*b*x
                else: # 삼각함수
                    angle = random.choice([0, 30, 45, 60, 90])
                    trig_func = random.choice(['sin', 'cos'])
                    if trig_func == 'sin':
                        val = round(math.sin(math.radians(angle)), 2)
                        question = f"What is sin({angle}°)? (Round to 2 decimal places)"
                    else: # 'cos'
                        val = round(math.cos(math.radians(angle)), 2)
                        question = f"What is cos({angle}°)? (Round to 2 decimal places)"
                    answer = val
                problems.append((question, str(answer)))
            # 4단계: 적분, 확률 및 통계, 수열
            else:
                problem_type = random.randint(0, 3)
                if problem_type == 0: # 간단한 적분
                    a = random.randint(1, 3)
                    b = random.randint(1, 5)
                    upper_bound = random.randint(1, 3)
                    lower_bound = random.randint(0, upper_bound - 1)
                    integral = (a/3) * (upper_bound**3 - lower_bound**3) + (b/2) * (upper_bound**2 - lower_bound**2)
                    question = f"What is the definite integral of {a}x^2 + {b}x from x={lower_bound} to x={upper_bound}? (Round to 2 decimal places)"
                    answer = round(integral, 2)
                elif problem_type == 1: # 조합 및 확률
                    n = random.randint(5, 10)
                    k = random.randint(2, n - 1)
                    combo = math.comb(n, k)
                    question = f"What is C({n}, {k})?"
                    answer = combo
                elif problem_type == 2: # 등차/등비수열
                    seq_type = random.choice(['arithmetic', 'geometric'])
                    n = random.randint(5, 10)
                    if seq_type == 'arithmetic':
                        a1 = random.randint(1, 10)
                        d = random.randint(1, 5)
                        an = a1 + (n - 1) * d
                        question = f"What is the {n}-th term of an arithmetic sequence with a first term of {a1} and a common difference of {d}?"
                        answer = an
                    else: # 'geometric'
                        a1 = random.randint(1, 5)
                        r = random.randint(2, 4)
                        an = a1 * (r**(n - 1))
                        question = f"What is the {n}-th term of a geometric sequence with a first term of {a1} and a common ratio of {r}?"
                        answer = an
                else: # 로그
                    base = random.randint(2, 5)
                    power = random.randint(2, 4)
                    value = base**power
                    question = f"What is log base {base} of {value}?"
                    answer = power
                problems.append((question, str(answer)))
        return problems

    def start_game_logic(self, dt=0):
        self.update_hearts()
        self.next_question()

    def update_hearts(self):
        for i, heart in enumerate(reversed(self.hearts)):
            heart.opacity = 0 if self.wrong_answers > i else 1

    def update_timer(self, dt):
        if self.paused or not self.quiz_active: return
        self.time_left -= 1
        self.time_display_label.text = f"00:{self.time_left:02d}"
        ratio = max(0, self.time_left / TIME_LIMIT)
        self.bar_fill.size_hint_x = ratio
        self.bar_empty.size_hint_x = 1.0 - ratio

        current_speech = ""
        img_path = ""
        color = (0.1, 0.5, 0.8, 1)

        if self.difficulty == "Special":
            if self.time_left > 29:
                img_path = SPECIAL_IMAGE_1ST
                current_speech = "아 이거~!"
            elif self.time_left > 19:
                img_path = SPECIAL_IMAGE_2ND
                current_speech = "이게 뭐더라~?"
            elif self.time_left > 9:
                img_path = SPECIAL_IMAGE_3RD
                current_speech = "뭐였지? 기억이 안나네.."
            else:
                img_path = SPECIAL_IMAGE_4TH
                current_speech = "ㅠㅠ~모르겠어!"
        else: # 기존 모드
            if self.time_left > 29:
                color, img_path = (0.1, 0.5, 0.8, 1), IMAGE_40_30_PATH
                current_speech = "아 이거~!"
            elif self.time_left > 19:
                color, img_path = (0, 0.7, 0, 1), IMAGE_29_20_PATH
                current_speech = "이게 뭐더라~?"
            elif self.time_left > 9:
                color, img_path = (1, 0.8, 0, 1), IMAGE_19_10_PATH
                current_speech = "뭐였지? 기억이 안나네.."
            else:
                color, img_path = (1, 0, 0, 1), IMAGE_9_1_PATH
                current_speech = "ㅠㅠ~모르겠어!"
        
        if self.difficulty != "Special" and self.bar_fill.color_val != color:
            self.bar_fill.color_val = color
            self.bar_fill.update_canvas()

        if self.result_image.source != img_path:
            self.result_image.source = img_path
        self.speech_bubble.update_text(current_speech)

        if self.time_left <= 0:
            self.stop_timer()
            if self.difficulty == "Special":
                self.show_image_popup(SPECIAL_WRONG_IMAGE_PATH, "시간 초과! 오답 처리됩니다.")
            else:
                self.show_image_popup(WRONG_IMAGE_PATH, "시간 초과! 오답 처리됩니다.")
            self.wrong_answers += 1
            self.update_hearts()

    def pause_game(self, instance):
        if not self.quiz_active or self.paused: return
        self.paused = True
        self.stop_timer()
        content = BoxLayout(orientation='vertical', spacing=20, padding=20)
        content.add_widget(Label(text="일시정지됨", font_size='35sp'))
        resume_button = Button(text="계속하기", font_size='25sp')
        resume_button.bind(on_press=self.resume_game)
        content.add_widget(resume_button)
        self.pause_popup = Popup(title="Pause", content=content, size_hint=(0.6, 0.5), auto_dismiss=False)
        self.pause_popup.open()

    def resume_game(self, instance):
        if self.pause_popup:
            self.pause_popup.dismiss()
            self.pause_popup = None
        self.paused = False
        if self.time_left > 0:
            self.timer_event = Clock.schedule_interval(self.update_timer, 1)
    
    def start_timer(self):
        self.time_left = TIME_LIMIT
        self.time_display_label.text = f"00:{TIME_LIMIT:02d}"
        self.bar_fill.size_hint_x = 1.0
        self.bar_empty.size_hint_x = 0.0
        
        if self.difficulty == "Special":
            self.result_image.source = SPECIAL_IMAGE_1ST
        else:
            self.result_image.source = IMAGE_40_30_PATH

        self.speech_bubble.update_text("아 이거~!")
        self.stop_timer()
        self.timer_event = Clock.schedule_interval(self.update_timer, 1)

    def stop_timer(self):
        if self.timer_event:
            self.timer_event.cancel()
            self.timer_event = None

    def next_question(self):
        if self.current_question_index < len(self.items):
            self.is_bonus_question = random.random() < 0.3
            question, _ = self.items[self.current_question_index]
            self.current_question_text = f"({self.current_question_index + 1}/{len(self.items)}) {question}"
            self.begin_question_countdown(3)
        else:
            self.end_game()

    def begin_question_countdown(self, count):
        if count > 0:
            self.question_label.text = str(count)
            self.question_label.font_size = '80sp'
            self.speech_bubble.update_text("")
            self.bonus_display_layout.opacity = 0
            Clock.schedule_once(lambda dt: self.begin_question_countdown(count - 1), 1)
        else:
            self.question_label.text = "Start!"
            Clock.schedule_once(self.prepare_question_ui, 1)

    def prepare_question_ui(self, dt):
        self.question_label.text = self.current_question_text
        self.question_label.font_size = '28sp'
        self.answer_input.disabled = False
        self.submit_button.disabled = False
        self.hint_button.disabled = False
        self.hint_used_this_question = False
        self.answer_input.text = ""
        self.answer_input.hint_text = ""
        self.answer_input.focus = True
        
        self.bonus_display_layout.opacity = 1 if self.is_bonus_question else 0
        
        self.start_timer()

    def check_answer(self, instance):
        if self.paused or not self.quiz_active: return
        self.stop_timer()
        self.hint_button.disabled = True
        self.speech_bubble.update_text("")
        user_answer = self.answer_input.text.strip().lower()
        _, correct_answer = self.items[self.current_question_index]
        
        if self.is_bonus_question:
            self.bonus_display_layout.opacity = 0
            
        is_correct = False
        if self.difficulty == "Special":
            try:
                # 수학 문제의 경우, 정답과 사용자 입력이 같은지 확인 (문자열 비교)
                if user_answer == correct_answer.lower():
                    is_correct = True
            except ValueError:
                is_correct = False
        else:
            if user_answer == correct_answer.lower():
                is_correct = True

        if is_correct:
            points = 30 if self.time_left > 29 else 25 if self.time_left > 19 else 20 if self.time_left > 9 else 10
            
            if self.is_bonus_question:
                if random.random() < 0.5:
                    points *= 2
                    message = f"보너스! 점수 2배! (+{points}점 획득)"
                else:
                    if self.wrong_answers > 0:
                        self.wrong_answers -= 1
                        self.update_hearts()
                        message = f"보너스! 하트 하나 회복! (+{points}점 획득)"
                    else:
                        points *= 2
                        message = f"보너스! 이미 하트가 가득! 점수 2배! (+{points}점 획득)"
            else:
                message = f"정답입니다! (+{points}점 획득)"
            
            self.score += points
            self.score_label.text = f"점수: {self.score}점"
            if self.difficulty == "Special":
                self.show_image_popup(SPECIAL_CORRECT_IMAGE_PATH, message)
            else:
                self.show_image_popup(CORRECT_IMAGE_PATH, message)
        else:
            self.wrong_answers += 1
            self.update_hearts()
            if self.difficulty == "Special":
                self.show_image_popup(SPECIAL_WRONG_IMAGE_PATH, f"오답입니다...\n(정답: {correct_answer})")
            else:
                self.show_image_popup(WRONG_IMAGE_PATH, f"오답입니다...\n(정답: {correct_answer})")

    def use_hint(self, instance):
        if self.paused or self.hint_used_this_question or not self.quiz_active: return
        _, correct_answer = self.items[self.current_question_index]
        
        if self.difficulty == "Special":
            # Special 모드 힌트: 정답의 일부를 보여주는 대신, 힌트 텍스트 제공
            if self.time_left > 20:
                self.speech_bubble.update_text("이건 산수 문제에요!")
            elif self.time_left > 10:
                self.speech_bubble.update_text("사칙연산을 다시 확인해보세요.")
            else:
                self.speech_bubble.update_text(f"정답은 {correct_answer}이에요! (힌트 사용)")
            self.hint_used_this_question = True
        else:
            # 기존 모드 힌트
            if 10 <= self.time_left <= 19:
                self.answer_input.hint_text = correct_answer[0]
                self.hint_used_this_question = True
            elif self.time_left <= 9:
                self.answer_input.hint_text = correct_answer[:2]
                self.hint_used_this_question = True

    def show_image_popup(self, image_path, message):
        content = BoxLayout(orientation='vertical', spacing=10, padding=10)
        img = Image(source=image_path, size_hint_y=0.6, allow_stretch=True)
        label = Label(text=message, font_size='25sp', size_hint_y=0.2)
        close_button = Button(text="확인", size_hint_y=0.2, font_size='20sp')
        content.add_widget(img)
        content.add_widget(label)
        content.add_widget(close_button)
        popup = Popup(title='결과', content=content, size_hint=(0.9, 0.9), auto_dismiss=False)
        close_button.bind(on_release=lambda x: self.close_popup_and_next_question(popup))
        popup.open()

    def close_popup_and_next_question(self, popup):
        popup.dismiss()
        self.current_question_index += 1
        self.answer_input.disabled = True
        self.submit_button.disabled = True
        self.hint_button.disabled = True
        self.speech_bubble.update_text("")
        self.bonus_display_layout.opacity = 0
        if self.wrong_answers >= 3 or self.current_question_index >= len(self.items):
            self.end_game()
        elif self.quiz_active:
            self.next_question()

    def save_score(self, score, difficulty):
        try:
            with open('scores.csv', 'a', newline='', encoding='utf-8') as f:
                csv.writer(f).writerow([score, difficulty, datetime.now().strftime("%Y-%m-%d")])
        except Exception as e:
            print(f"점수 저장 중 오류 발생: {e}")

    def load_scores(self):
        try:
            with open('scores.csv', 'r', newline='', encoding='utf-8') as f:
                return sorted(
                    [[int(row[0]), row[1], row[2]] for row in csv.reader(f) if len(row) >= 3],
                    key=lambda x: x[0], reverse=True
                )
        except FileNotFoundError: return []
        except Exception as e:
            print(f"점수 로딩 중 오류 발생: {e}")
            return []

    def end_game(self):
        self.stop_timer()
        if self.pause_popup:
            self.pause_popup.dismiss()
            self.pause_popup = None
        self.quiz_active = False
        self.speech_bubble.update_text("")
        all_scores = self.load_scores()
        difficulty_scores = [s[0] for s in all_scores if s[1] == self.difficulty]
        previous_high_score = difficulty_scores[0] if difficulty_scores else 0
        self.save_score(self.score, self.difficulty)
        if self.score > 0 and self.score > previous_high_score:
            self.show_record_popup()
        else:
            self.show_final_score_popup()

    def show_record_popup(self):
        content = BoxLayout(orientation='vertical', spacing=10, padding=10)
        img = Image(source=RECORD_IMAGE_PATH, size_hint_y=0.6, allow_stretch=True)
        label = Label(text="축하합니다! 최고점수 달성!", font_size='30sp', size_hint_y=0.2, bold=True)
        close_button = Button(text="확인", size_hint_y=0.2, font_size='20sp')
        content.add_widget(img)
        content.add_widget(label)
        content.add_widget(close_button)
        popup = Popup(title='🎉 신기록 달성! 🎉', content=content, size_hint=(0.7, 0.8), auto_dismiss=False)
        close_button.bind(on_release=lambda x: (popup.dismiss(), self.show_final_score_popup()))
        popup.open()

    def show_final_score_popup(self):
        all_scores = self.load_scores()
        final_message = f"게임 종료!\n최종 점수는 {self.score}점입니다."
        if self.wrong_answers >= 3:
            final_message = "기회를 모두 소진했습니다!\n" + final_message
        scores_text = f"\n\n🏆 최고 기록 ({self.difficulty}) 🏆\n" + ("-" * 20)
        filtered_scores = [r for r in all_scores if r[1] == self.difficulty][:5]
        scores_text += "\n아직 기록이 없습니다." if not filtered_scores else "".join(f"\n{i+1}. {r[0]}점 - {r[2]}" for i, r in enumerate(filtered_scores))
        content = BoxLayout(orientation='vertical', spacing=10, padding=20)
        content.add_widget(Label(text=final_message, font_size='25sp', size_hint_y=0.3))
        content.add_widget(Label(text=scores_text, font_size='20sp', size_hint_y=0.5))
        restart_button = Button(text="다시 시작", size_hint_y=0.2, font_size='20sp')
        restart_button.bind(on_release=self.restart_app)
        content.add_widget(restart_button)
        popup = Popup(title='게임 종료', content=content, size_hint=(0.8, 0.8), auto_dismiss=False)
        self.final_popup = popup
        popup.open()

    def restart_app(self, instance):
        self.stop_timer()
        if hasattr(self, 'final_popup') and self.final_popup:
            self.final_popup.dismiss()
        self.sm.current = 'difficulty'

if __name__ == '__main__':
    QuizApp().run()
