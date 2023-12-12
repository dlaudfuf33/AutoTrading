import tkinter as tk
from tkinter import ttk, messagebox
import pyupbit
import threading
import time

access_key_label = None
access_key_entry = None
secret_key_label = None
secret_key_entry = None
next_button = None

def enter_api_keys():
    def on_submit():
        global access_key, secret_key
        access_key = access_key_entry.get()
        secret_key = secret_key_entry.get()
        print(access_key,"   ",secret_key)
        api_window.destroy()
        messagebox.showinfo("알림", "API 키가 저장되었습니다.")  # API 키 저장 메시지 출력

    api_window = tk.Tk()
    api_window.title("API 키 입력")

    tk.Label(api_window, text="엑세스 키를 입력하세요:").pack()
    access_key_entry = tk.Entry(api_window)
    access_key_entry.pack()

    tk.Label(api_window, text="시크릿 키를 입력하세요:").pack()
    secret_key_entry = tk.Entry(api_window)
    secret_key_entry.pack()

    submit_button = tk.Button(api_window, text="확인", command=on_submit)
    submit_button.pack()

    api_window.protocol("WM_DELETE_WINDOW", lambda: api_window.destroy())  # 창 닫기 버튼 클릭 시 창만 닫음

    api_window.mainloop()

# API 키 설정
access_key = ""
secret_key = ""
enter_api_keys()

# API 키 확인
if not access_key or not secret_key:
    messagebox.showerror("오류", "API 키를 입력해야 합니다.")
    exit()

upbit = pyupbit.Upbit(access_key, secret_key)

# 대표적인 코인 리스트
coin_list = ["KRW-BTC", "KRW-XRP", "KRW-ETH"]

# 거래 진행 중 플래그
trading_in_progress = False

# 거래 내역 저장 리스트
trade_history = []

# 보유 자산 초기화
asset_balance = {coin: 0 for coin in coin_list}
asset_balance["KRW"] = upbit.get_balance("KRW")

# GUI 초기화
root = tk.Tk()
root.title("자동 코인 거래 프로그램")

# 거래 시작 함수
def start_trading():
    global trading_in_progress

    # 거래 진행 중이면 중복 실행 방지
    if trading_in_progress:
        messagebox.showinfo("알림", "거래가 이미 진행 중입니다.")
        return

    # 거래 조건 설정 코드...

    # 거래 진행 중 플래그 설정
    trading_in_progress = True

    # 거래 내역 초기화
    trade_history.clear()

    # 거래 시작 메시지 표시
    status_text.set("거래가 시작되었습니다. 거래 내역은 아래에서 확인하세요.")

    # 거래 실행 및 매 60초마다 업데이트
    def execute_trading():
        while trading_in_progress:
            try:
                # 거래 실행 코드 추가 (매수 및 매도)

                # 거래 내역 업데이트
                update_trade_history()

                # 60초 대기
                time.sleep(60)
            except Exception as e:
                status_text.set(f"오류 발생: {e}")

    trading_thread = threading.Thread(target=execute_trading)
    trading_thread.start()



# 거래 내역 리스트
trade_history = []
# 거래 내역 리스트 박스 업데이트 함수
def update_trade_history_listbox():
    global trade_history_listbox, trade_history_listbox  # 전역 변수로 선언
    trade_history_listbox.delete(0, tk.END)
    for trade in trade_history:
        trade_history_listbox.insert(tk.END, trade)

# 거래 내역 업데이트 함수
def update_trade_history():
    global trade_history_listbox, trade_history_listbox  # 전역 변수로 선언
    # 거래 내역 조회 및 업데이트
    new_trade = "매수: BTC 1.0 - 50,000,000원"  # 여기에 실제 거래 내역 조회 및 포맷팅 로직 추가
    trade_history.append(new_trade)
    update_trade_history_listbox()
    # 5초마다 업데이트
    root.after(5000, update_trade_history)



# 거래 종료 버튼 이벤트 처리
def stop_trading():
    global trading_in_progress
    trading_in_progress = False
    status_text.set("거래가 종료되었습니다.")



# 화면 2: 거래 설정 화면
def show_second_screen():
    global trading_in_progress, access_key_label, access_key_entry, secret_key_label
    secret_key_entry,next_button

    # 첫 번째 화면 숨김
    if access_key_label:
        access_key_label.grid_remove()
    if access_key_entry:
        access_key_entry.grid_remove()
    if secret_key_label:
        secret_key_label.grid_remove()
    if secret_key_entry:
        secret_key_entry.grid_remove()
    if next_button:
        next_button.grid_remove()
    # 두 번째 화면 표시
    coin_label = tk.Label(root, text="거래할 코인을 선택하세요:")
    coin_label.grid(row=0, column=0)
    coin_combo = ttk.Combobox(root, values=coin_list)
    coin_combo.grid(row=0, column=1)

    buy_ratio_label = tk.Label(root, text="매수할 비율을 입력하세요 (%):")
    buy_ratio_label.grid(row=1, column=0)
    buy_ratio_entry = tk.Entry(root)
    buy_ratio_entry.grid(row=1, column=1)

    sell_ratio_label = tk.Label(root, text="매도할 비율을 입력하세요 (%):")
    sell_ratio_label.grid(row=2, column=0)
    sell_ratio_entry = tk.Entry(root)
    sell_ratio_entry.grid(row=2, column=1)

    ma_short_label = tk.Label(root, text="단기 이동평균선 조건을 선택하세요:")
    ma_short_label.grid(row=3, column=0)
    ma_short_combo = ttk.Combobox(root, values=["사용 안 함", "이상", "이하"])
    ma_short_combo.grid(row=3, column=1)

    ma_mid_label = tk.Label(root, text="중기 이동평균선 조건을 선택하세요:")
    ma_mid_label.grid(row=4, column=0)
    ma_mid_combo = ttk.Combobox(root, values=["사용 안 함", "이상", "이하"])
    ma_mid_combo.grid(row=4, column=1)

    ma_long_label = tk.Label(root, text="장기 이동평균선 조건을 선택하세요:")
    ma_long_label.grid(row=5, column=0)
    ma_long_combo = ttk.Combobox(root, values=["사용 안 함", "이상", "이하"])
    ma_long_combo.grid(row=5, column=1)

    volume_label = tk.Label(root, text="거래량 조건을 선택하세요:")
    volume_label.grid(row=6, column=0)
    volume_combo = ttk.Combobox(root, values=["사용 안 함", "이상", "이하"])
    volume_combo.grid(row=6, column=1)

    volume_condition_label = tk.Label(root, text="거래량 임계값을 입력하세요:")
    volume_condition_label.grid(row=7, column=0)
    volume_threshold_entry = tk.Entry(root)
    volume_threshold_entry.grid(row=7, column=1)

    specific_price_label = tk.Label(root, text="특정 가격 조건을 선택하세요:")
    specific_price_label.grid(row=8, column=0)
    specific_price_combo = ttk.Combobox(root, values=["사용 안 함", "이상", "이하"])
    specific_price_combo.grid(row=8, column=1)

    specific_price_condition_label = tk.Label(root, text="특정 가격을 입력하세요:")
    specific_price_condition_label.grid(row=9, column=0)
    specific_price_entry = tk.Entry(root)
    specific_price_entry.grid(row=9, column=1)

    specific_price_threshold_label = tk.Label(root, text="특정 가격 임계값을 입력하세요:")
    specific_price_threshold_label.grid(row=10, column=0)
    specific_price_threshold_entry = tk.Entry(root)
    specific_price_threshold_entry.grid(row=10, column=1)

    # 모든 코인 초기화
    for coin in coin_list:
        asset_balance[coin] = upbit.get_balance(coin)

    # 보유 자산 표시
    asset_label = tk.Label(root, text="보유 자산:")
    asset_label.grid(row=11, column=0, columnspan=2,sticky="e")

    asset_listbox = tk.Listbox(root)
    asset_listbox.grid(row=12, column=0, columnspan=2,sticky="e")
    for coin in coin_list:
        asset_listbox.insert(tk.END, f"{coin}: {asset_balance[coin]}")

    # 거래 내역 스크롤 가능한 리스트
    trade_history_label = tk.Label(root, text="거래 내역:")
    trade_history_label.grid(row=11, column=0, columnspan=2, sticky="w")

    trade_history_frame = tk.Frame(root)
    trade_history_frame.grid(row=12, column=0, columnspan=2, sticky="w")

    trade_history_scrollbar = tk.Scrollbar(trade_history_frame, orient=tk.VERTICAL)
    trade_history_listbox = tk.Listbox(trade_history_frame, yscrollcommand=trade_history_scrollbar.set)
    trade_history_scrollbar.config(command=trade_history_listbox.yview)

    trade_history_listbox.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
    trade_history_scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

    # 거래 내역 업데이트 시작
    # update_trade_history()      
    
    # 거래 시작 버튼 생성
    start_button = tk.Button(root, text="거래 시작", command=start_trading)
    start_button.grid(row=12 + len(coin_list), column=0, columnspan=2,sticky="w",padx=45)

    # 거래 종료 버튼 생성
    stop_button = tk.Button(root, text="거래 종료", command=stop_trading)
    stop_button.grid(row=12 + len(coin_list), column=0, columnspan=2,sticky="e",padx=45)


# 2번째 화면 
show_second_screen()



# 거래 상태 메시지 초기화
status_text = tk.StringVar()
status_label = tk.Label(root, textvariable=status_text)
status_label.grid(row=13 + len(coin_list), column=0, columnspan=2)

root.mainloop()
