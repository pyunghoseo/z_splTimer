import random

def recommend_lunch():
    # 음식군 정의
    foods = {
        "한식": ["김치찌개", "된장찌개", "제육볶음"],
        "양식": ["파스타", "스테이크", "피자"],
        "중식": ["짜장면", "짬뽕", "마파두부"]
    }
    
    # 사용자 선택 프롬프트
    print("무슨 음식을 드시겠습니까? (한식, 양식, 중식)")
    choice = input().strip()
    
    # 선택된 음식군에서 랜덤으로 음식 추천
    if choice in foods:
        selected_food = random.choice(foods[choice])
        print(f"{choice} 중에서 오늘의 추천 메뉴는 '{selected_food}'입니다!")
    else:
        print("잘못된 입력입니다. 한식, 양식, 중식 중에서 선택해주세요.")

# recommend_lunch() 함수를 호출하여 프로그램을 실행해보세요.