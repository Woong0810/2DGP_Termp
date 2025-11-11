from pico2d import load_font
import game_framework
import os

class RoundTimer:
    def __init__(self, x, y, round_time=60):
        # Windows 시스템 폰트 경로 리스트 (굵고 선명한 격투게임 스타일)
        font_paths = [
            'PressStart2P.ttf',  # 다운로드한 아케이드 폰트
            'C:\\Windows\\Fonts\\impact.ttf',  # Impact - 굵고 강렬함
            'C:\\Windows\\Fonts\\arialbd.ttf',  # Arial Bold
            'C:\\Windows\\Fonts\\ariblk.ttf',  # Arial Black - 매우 굵음
            'C:\\Windows\\Fonts\\consola.ttf',  # Consolas - 명확함
            'C:\\Windows\\Fonts\\cour.ttf',  # Courier - 고정폭
        ]

        # 사용 가능한 폰트 찾기
        font_loaded = False
        for font_path in font_paths:
            if os.path.exists(font_path):
                try:
                    self.font = load_font(font_path, 50)
                    font_loaded = True
                    break
                except:
                    continue

        # 모든 폰트 로드 실패 시 에러
        if not font_loaded:
            raise Exception("폰트를 로드할 수 없습니다. Windows Fonts 폴더를 확인하세요.")

        self.x = x
        self.y = y
        self.max_time = round_time
        self.time = round_time

    def update(self):
        self.time -= game_framework.frame_time
        if self.time < 0:
            self.time = 0

    def draw(self):
        time_int = int(self.time)
        self.font.draw(self.x - 25, self.y, f'{time_int:02d}', (64, 64, 64))

    def is_time_over(self):
        return self.time <= 0

    def reset(self):
        self.time = self.max_time

    def handle_collision(self, group, other):
        pass

