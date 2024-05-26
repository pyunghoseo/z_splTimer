# 20240207 22시 이벤트 드리븐 버튼으로 변경까지 했으나 오동작
from tkinter import *
import os
import winsound  # winsound 모듈을 임포트

# ---------------------------- CONSTANTS ------------------------------- #
PINK = "#FF004D"
RED = "#FF004D"
YELLOW = "#FFEA20"
INDOGO = "#030637"
FONT_NAME = "Courier"
# 각 WAVE별 초기 카운트다운 시간 설정
INITIAL_TIMES = [118, 113, 112, 112, 110]
reps = 0
timer = None
current_time = 0  # 현재 카운트다운 시간
is_paused = False  # A flag to determine if the timer is paused

# 현재 스크립트 파일의 디렉토리 경로를 얻음
current_folder = os.path.dirname(__file__)
# 이 경로를 사용하여 이미지 파일의 상대경로를 생성
image_path = os.path.join(current_folder, "egg.png")

# 이벤트 메시지 딕셔너리 (각 WAVE별로 설정 가능)
event_messages = [
    {100: "Wave1 시작", 82: "어깨패드 처리", 46: "타워 처리"},
    {100: "Wave2 시작", 90: "90초 이벤트", 80: "80초 이벤트", 70: "70초 이벤트", 60: "60초 이벤트"},
    {100: "Wave3 시작", 90: "90초 이벤트", 80: "80초 이벤트", 70: "70초 이벤트", 60: "60초 이벤트"},
    {100: "Wave4 시작", 90: "90초 이벤트", 80: "80초 이벤트", 70: "70초 이벤트", 60: "60초 이벤트"},
    {100: "Wave5 시작", 90: "90초 이벤트", 80: "80초 이벤트", 70: "70초 이벤트", 60: "60초 이벤트"}      
]

# ---------------------------- TIME ADJUSTMENT ------------------------------- #
def adjust_time(amount):
    global current_time, timer
    if current_time > 0:
        window.after_cancel(timer)  # Cancel the ongoing countdown
        current_time += amount
        current_time = max(0, current_time)  # Ensure time doesn't go below 0
        # Round the time to the nearest whole number before displaying
        current_time = round(current_time)
        count_sec = f"{current_time}"
        canvas.itemconfig(timer_text, text=count_sec)
        # Start a new countdown with the adjusted time
        count_down(current_time, reps // 2)

# ---------------------------- TIMER RESET ------------------------------- #
def reset_timer():
    window.after_cancel(timer)
    current_label.config(text="SalmonRun Timer")
    wave_label.config(text="")  # WAVE 레이블 업데이트
    next_label.config(text="")
    global reps
    reps = 0
    global current_time
    current_time = 0
    canvas.itemconfig(timer_text, text="Ready")

# ---------------------------- TIMER MECHANISM ------------------------------- # 
def start_timer():
    global reps
    if reps < len(INITIAL_TIMES) * 2:
        if reps % 2 == 0:
            # 시작 시 Beep 소리
            winsound.Beep(2000, 1000)  # 주파수 2000, 지속시간 1000ms
            wave = reps // 2
            wave_label.config(text=f"WAVE {wave + 1}")  # 현재 WAVE 표시
            count_down(INITIAL_TIMES[wave], wave)  # 초기 시간으로 카운트다운 시작
        else:
            # WAVE 사이의 7초 인터벌
            count_down(7, -1)  # 인터벌 카운트다운, wave 인덱스 -1로 설정
        reps += 1
    else:
        # 모든 WAVE 완료 후 종료 처리
        reset_timer()

# ---------------------------- COUNTDOWN MECHANISM ------------------------------- #
def count_down(count, wave):
    global current_time, timer
    current_time = count
    count_sec = f"{count}"
    canvas.itemconfig(timer_text, text=count_sec)
    if count > 0:
        global timer
        timer = window.after(1000, count_down, count - 1, wave)

        if wave >= 0:  # 인터벌이 아닌 경우에만 이벤트 체크
            keys = sorted(event_messages[wave].keys(), reverse=True)
            if count in keys:
                current_event_index = keys.index(count)
                # Format the event message to include the time
                event_time_message = f"{count}초 : {event_messages[wave][count]}"
                current_label.config(text=event_time_message)

                next_event_index = current_event_index + 1
                if next_event_index < len(keys):
                    next_event_time = keys[next_event_index]
                    # Format the next event message to include the time
                    next_event_time_message = f"{next_event_time}초 : {event_messages[wave][next_event_time]}"
                    next_label.config(text=next_event_time_message)
                else:
                    next_label.config(text="")

                winsound.Beep(2000, 1000)

    else:
        if wave >= 0:
            winsound.Beep(2000, 1000)
        start_timer()

# ---------------------------- PAUSE MECHANISM ------------------------------- #
def pause_or_resume_timer():
    global is_paused, timer
    if is_paused:
        # If the timer is paused, resume it
        count_down(current_time, reps // 2)
    else:
        # If the timer is running, pause it
        window.after_cancel(timer)
    is_paused = not is_paused  # Toggle the pause state
        
# ---------------------------- UI SETUP ------------------------------- #
window = Tk()
window.title("SalmonRun")
window.config(padx=100, pady=50, bg=INDOGO)

# WAVE 표시 레이블 추가
wave_label = Label(window, text="", fg=RED, bg=INDOGO, font=(FONT_NAME, 24))
wave_label.grid(column=1, row=0)

current_label = Label(window, text="SalmonRun Timer", fg=YELLOW, bg=INDOGO, font=(FONT_NAME, 35))
current_label.grid(column=1, row=1)

next_label = Label(window, text="", fg=PINK, bg=INDOGO, font=(FONT_NAME, 20))
next_label.grid(column=1, row=2)

canvas = Canvas(window, width=400, height=448, bg=INDOGO, highlightthickness=0)
tomato_img = PhotoImage(file=image_path)
canvas.create_image(200, 224, image=tomato_img)
timer_text = canvas.create_text(210, 180, text="Ready", fill="red", font=(FONT_NAME, 50, "bold"))
canvas.grid(column=1, row=3)

start_button = Button(text="Start", highlightthickness=0, command=start_timer, font=(FONT_NAME, 20, "bold"), height=2, width=10)
start_button.grid(column=0, row=3)

reset_button = Button(text="Reset", highlightthickness=0, command=reset_timer, font=(FONT_NAME, 20, "bold"), height=2, width=10)
reset_button.grid(column=2, row=3)

# Adjust time buttons
frame = Frame(window, bg=INDOGO)
frame.grid(column=1, row=5, pady=20)

# Update the buttons to include only the -1.0 and +1.0 buttons, and the new Pause button
adjust_buttons = [
    ("-10", -10),
    ("-1", -1),
    ("Pause", pause_or_resume_timer),
    ("+1", 1),
    ("+10", +10)
]

# Create buttons based on the adjust_buttons list
for text, command in adjust_buttons:
    if text == "Pause":
        # Create a Pause button that calls pause_or_resume_timer
        button = Button(frame, text=text, command=command, font=(FONT_NAME, 20, "bold"), height=2, width=6)
    else:
        # Create time adjustment buttons
        button = Button(frame, text=text, command=lambda a=command: adjust_time(a), font=(FONT_NAME, 20, "bold"), height=2, width=6)
        
    button.pack(side=LEFT, expand=True)

# ---------------------------- 반응형 라디오 버튼 ------------------------------- #
# 선택된 위험도 저장을 위한 변수
selected_danger_level = {}

# Button click event handler 수정 버전
def handle_danger_level_click(wave, btn, percent):
    global selected_danger_level, event_messages
    # 선택된 위험도 업데이트
    selected_danger_level[wave] = percent

    # btn의 부모 위젯(프레임) 찾기
    parent_frame = btn.master

    # 모든 버튼의 상태 초기화
    for child in parent_frame.winfo_children():
        if isinstance(child, Button):
            child.config(relief=RAISED, bg=INDOGO)
    # 선택된 버튼 강조
    btn.config(relief=SUNKEN, bg=RED)

    # wave 번호에 따른 인덱스 설정
    wave_index = int(wave[1:]) - 2

    # 위험도에 따른 이벤트 메시지 업데이트
    # 참고 내용에 따라 event_messages 업데이트
    if wave == 'W2' and percent == '90%':
        event_messages[1] = {100: "Wave2-90% 시작", 90: "어깨패드 처리", 80: "타워 처리", 70: "철구 처리", 60: "기둥 처리"}
    elif wave == 'W2' and percent == '120%':
        event_messages[1] = {100: "Wave2-120% 시작", 90: "타워처리", 80: "어깨패드 처리", 70: "기둥 처리"}
    elif wave == 'W3' and percent == '120%':
        event_messages[1] = {100: "Wave3-120% 시작", 90: "철구 처리", 70: "어깨패드 처리"}
    elif wave == 'W3' and percent == '150%':
        event_messages[1] = {100: "Wave3-150% 시작", 90: "철구 처리", 60: "어깨패드 처리"}
    elif wave == 'W3' and percent == '180%':
        event_messages[1] = {100: "Wave3-180% 시작", 90: "타워처리", 80: "어깨패드 처리", 70: "기둥 처리", 70: "타워처리"}
    elif wave == 'W4' and percent == '150%':
        event_messages[1] = {100: "Wave4-150% 시작", 90: "어깨패드 처리", 80: "기둥 처리"}
    elif wave == 'W4' and percent == '180%':
        event_messages[1] = {100: "Wave4-180% 시작", 90: "타워처리", 80: "철구 처리"}
    elif wave == 'W4' and percent == '210%':
        event_messages[1] = {100: "Wave4-210% 시작", 90: "기둥 처리", 80: "기둥 처리"}
    elif wave == 'W4' and percent == '240%':
        event_messages[1] = {100: "Wave4-240% 시작", 90: "타워처리",60: "기둥 처리"}
    elif wave == 'W5' and percent == '210%':
        event_messages[1] = {100: "Wave5-210% 시작", 80: "철구 처리", 70: "타워처리"}
    elif wave == 'W5' and percent == '240%':
        event_messages[1] = {100: "Wave5-240% 시작", 90: "어깨패드 처리", 80: "기둥 처리", 70: "타워처리", 60: "어깨패드 처리"}
    elif wave == 'W5' and percent == '270%':
        event_messages[1] = {100: "Wave5-270% 시작", 90: "타워처리", 80: "기둥 처리", 70: "기둥 처리", 60: "어깨패드 처리"}
    elif wave == 'W5' and percent == '300%':
        event_messages[1] = {100: "Wave5-300% 시작", 90: "타워처리", 80: "기둥 처리", 70: "어깨패드 처리", 60: "기둥 처리"}
    else:
        exit

# 초기 선택된 위험도 설정 수정
initial_selections = {
    'W2': '120%',
    'W3': '180%',
    'W4': '240%',
    'W5': '270%',
}

# 각 wave별 위험도 배열 정의
danger_levels = {
    'W2': ['60%', '90%', '120%', None],
    'W3': ['120%', '150%', '180%', None],
    'W4': ['150%', '180%', '210%', '240%'],
    'W5': ['210%', '240%', '270%', '300%'],
}

# Define buttons_info with the button text and its position for each wave
buttons_info = {
    'W2': [('60%', 1), ('90%', 2), ('120%', 3), ('', 4)],
    'W3': [('120%', 1), ('150%', 2), ('180%', 3), ('', 4)],
    'W4': [('150%', 1), ('180%', 2), ('210%', 3), ('240%', 4)],
    'W5': [('210%', 1), ('240%', 2), ('270%', 3), ('300%', 4)],
}

# Custom radio buttons addition function 수정 버전
def add_custom_radio_buttons():
    radio_frame = Frame(window, bg=INDOGO)
    radio_frame.grid(column=1, row=4, pady=(10, 20))

    # 가장 긴 텍스트를 가진 버튼의 글자 수를 기준으로 너비를 설정합니다.
    button_width = max(len(button_text) for rows in danger_levels.values() for button_text in rows if button_text)

    for wave, buttons in buttons_info.items():
        wave_frame = Frame(radio_frame, bg=INDOGO)
        wave_frame.grid(row=int(wave[1])-2, column=0, sticky="w", padx=10, pady=5)
        Label(wave_frame, text=wave, bg=INDOGO, fg=YELLOW, font=(FONT_NAME, int(16*1.5))).pack(side=LEFT)

        for percent, column in buttons:
            btn = Button(wave_frame, text=percent, bg=INDOGO, fg=YELLOW,
                         font=(FONT_NAME, int(12*1.5)), relief=RAISED, width=button_width)
            btn.pack(side=LEFT, padx=10, pady=5)
            # 여기서 btn 객체를 정확히 캡처하기 위해 람다 함수 수정
            btn.config(command=lambda btn=btn, w=wave, p=percent: handle_danger_level_click(w, btn, p))
            
            
            # 초기 상태 설정이 문제가 없는지 확인
            if initial_selections.get(wave) == percent:
                btn.invoke()  # btn 객체를 사용하여 직접 invoke() 메서드를 호출


add_custom_radio_buttons()

window.mainloop()