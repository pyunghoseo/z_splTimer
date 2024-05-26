from tkinter import *
import os
import winsound  # winsound 모듈을 임포트

# ---------------------------- CONSTANTS ------------------------------- #
PINK = "#FF004D"
RED = "#FF004D"
YELLOW = "#FFEA20"
INDOGO = "#030637"
FONT_NAME = "Courier"
INITIAL_SEC = 100  # 초기 카운트다운 시간 설정, 테스트로는 100초로 설정
reps = 0
timer = None

# 현재 스크립트 파일의 디렉토리 경로를 얻음
current_folder = os.path.dirname(__file__)
# 이 경로를 사용하여 이미지 파일의 상대경로를 생성
image_path = os.path.join(current_folder, "egg.png")

# 이벤트 메시지 딕셔너리
event_messages = {
    100: "100초 알주어 등장",
    90: "90초 기둥 3개 출현",
    80: "80초 철구 출현",
    70: "70초 타워 3개 출현",
    60: "60초 알넣기",
}

# ---------------------------- TIMER RESET ------------------------------- #
def reset_timer():
    window.after_cancel(timer)
    canvas.itemconfig(timer_text, text="00:00")
    current_label.config(text="SalmonRun Timer")
    next_label.config(text="")
    global reps
    reps = 0
    canvas.itemconfig(timer_text, text="Ready")

# ---------------------------- TIMER MECHANISM ------------------------------- # 
def start_timer():
    global reps
    reps += 1
    # 시작 시 Beep 소리
    winsound.Beep(2000, 1000)  # 주파수 2000, 지속시간 1000ms
    count_down(INITIAL_SEC)  # 초기 시간으로 카운트다운 시작

# ---------------------------- COUNTDOWN MECHANISM ------------------------------- #
def count_down(count):
    count_sec = f"{count:02d}"
    canvas.itemconfig(timer_text, text=count_sec)
    if count > 0:
        global timer
        timer = window.after(1000, count_down, count - 1)

        keys = sorted(event_messages.keys())
        if count in keys:
            current_event_index = keys.index(count)
            current_label.config(text=event_messages[count])

            next_event_index = current_event_index - 1
            if next_event_index >= 0:
                next_event_time = keys[next_event_index]
                next_label.config(text=event_messages[next_event_time])
            else:
                next_label.config(text="")

            winsound.Beep(2000, 1000)

    else:
        winsound.Beep(2000, 1000)
        start_timer()
        check_marks.config(text="")

# ---------------------------- UI SETUP ------------------------------- #
window = Tk()
window.title("SalmonRun")
window.config(padx=100, pady=50, bg=INDOGO)

current_label = Label(window, text="SalmonRun Timer", fg=YELLOW, bg=INDOGO, font=(FONT_NAME, 35))
current_label.grid(column=1, row=0)

next_label = Label(window, text="", fg=PINK, bg=INDOGO, font=(FONT_NAME, 20))
next_label.grid(column=1, row=1)

# 캔버스 크기 조정 (기존 크기의 2배)
canvas = Canvas(window, width=400, height=448, bg=INDOGO, highlightthickness=0)
tomato_img = PhotoImage(file=image_path)
# 이미지 위치 조정 (캔버스 중앙으로)
canvas.create_image(200, 224, image=tomato_img)
timer_text = canvas.create_text(210, 180, text="118", fill="red", font=(FONT_NAME, 50, "bold"))
canvas.grid(column=1, row=2)

start_button = Button(text="Start", highlightthickness=0, command=start_timer, font=(FONT_NAME, 20, "bold"), height=2, width=10)
start_button.grid(column=0, row=2)

reset_button = Button(text="Reset", highlightthickness=0, command=reset_timer, font=(FONT_NAME, 20, "bold"), height=2, width=10)
reset_button.grid(column=2, row=2)

check_marks = Label(window, fg=YELLOW, bg=INDOGO)
check_marks.grid(column=1, row=4)

window.mainloop()
