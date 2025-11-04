"""
캐릭터별 프레임 설정 정보
각 캐릭터마다 어떤 동작이 몇 번째 프레임에 있는지 정의
"""
from characters_naruto_frames import FRAMES as NARUTO_FRAMES
from characters_itachi_frames import FRAMES as ITACHI_FRAMES
from characters_jiraiya_frames import FRAMES as JIRAIYA_FRAMES

class CharacterConfig:
    """캐릭터 설정 베이스 클래스"""
    def __init__(self):
        self.name = ""
        self.image_path = ""
        self.frames = []  # 전체 프레임 정보

        # 캐릭터 스케일 (출력 크기 조정)
        self.scale_x = 1.0
        self.scale_y = 1.0

        # 캐릭터 그리기 오프셋 (피벗 차이 보정)
        self.draw_offset_y = 0

        # 각 동작의 프레임 인덱스 범위
        self.idle_frames = []
        self.run_frames = []
        self.normal_attack_frames = []
        self.normal_attack_segments = []
        self.jump_frames = []
        self.defense_frames = []
        self.special_attack_frames = []
        self.ranged_attack_char_frames = []
        self.ranged_attack_effect_frames = []
        self.hit_frames = []  # 피격 프레임

        # 히트박스 설정 (각 상태별 scale_x, scale_y, x_offset, y_offset)
        self.hitbox_idle = {'scale_x': 0.7, 'scale_y': 0.8, 'x_offset': 0, 'y_offset': 0}
        self.hitbox_run = {'scale_x': 0.7, 'scale_y': 0.8, 'x_offset': 0, 'y_offset': 0}
        self.hitbox_jump = {'scale_x': 0.7, 'scale_y': 0.8, 'x_offset': 0, 'y_offset': 0}
        self.hitbox_normal_attack = {'scale_x': 0.7, 'scale_y': 0.8, 'x_offset': 0, 'y_offset': 0}
        self.hitbox_defense = {'scale_x': 1.0, 'scale_y': 1.0, 'x_offset': 0, 'y_offset': 0}
        self.hitbox_special_attack = {'scale_x': 1.2, 'scale_y': 1.2, 'x_offset': 0, 'y_offset': 0}
        self.hitbox_ranged_attack = {'scale_x': 0.7, 'scale_y': 0.8, 'x_offset': 0, 'y_offset': 0}
        self.hitbox_hit = {'scale_x': 0.7, 'scale_y': 0.8, 'x_offset': 0, 'y_offset': 0}  # 피격 히트박스

class NarutoConfig(CharacterConfig):
    def __init__(self):
        super().__init__()
        self.name = "Naruto"
        self.image_path = "Characters_Naruto_clean.png"
        self.frames = NARUTO_FRAMES

        # 각 동작의 프레임 인덱스
        self.idle_frames = list(range(41, 47))
        self.run_frames = list(range(26, 32))
        self.normal_attack_frames = list(range(0, 12))
        self.normal_attack_segments = [(0, 3), (4, 7), (8, 11)]
        self.jump_frames = [33, 34]
        self.defense_frames = list(range(12, 17))
        self.special_attack_frames = list(range(98, 136))
        self.ranged_attack_char_frames = list(range(91, 97))
        self.ranged_attack_effect_frames = list(range(67, 71))
        self.hit_frames = [47, 48]  # 피격 프레임

        # 나루토 전용 히트박스 설정 (기본값 사용)
        self.hitbox_idle = {'scale_x': 0.7, 'scale_y': 0.8, 'x_offset': 0, 'y_offset': 0}
        self.hitbox_run = {'scale_x': 0.7, 'scale_y': 0.8, 'x_offset': 0, 'y_offset': 0}
        self.hitbox_jump = {'scale_x': 0.7, 'scale_y': 0.8, 'x_offset': 0, 'y_offset': 0}
        self.hitbox_normal_attack = {'scale_x': 0.7, 'scale_y': 0.8, 'x_offset': 0, 'y_offset': 0}
        self.hitbox_defense = {'scale_x': 1.0, 'scale_y': 1.0, 'x_offset': 0, 'y_offset': 0}
        self.hitbox_special_attack = {'scale_x': 1.2, 'scale_y': 1.2, 'x_offset': 0, 'y_offset': 0}
        self.hitbox_ranged_attack = {'scale_x': 0.7, 'scale_y': 0.8, 'x_offset': 0, 'y_offset': 0}
        self.hitbox_hit = {'scale_x': 0.7, 'scale_y': 0.8, 'x_offset': 0, 'y_offset': 0}  # 피격 히트박스

class ItachiConfig(CharacterConfig):
    def __init__(self):
        super().__init__()
        self.name = "Itachi"
        self.image_path = "Characters_Itachi_clean.png"
        self.frames = ITACHI_FRAMES

        # 이타치 스케일 조정 (나루토와 같은 크기로)
        self.scale_x = 1.0
        self.scale_y = 0.85  # y축 크기를 줄여서 나루토와 비슷하게

        # 이타치 피벗 보정
        self.draw_offset_y = 5

        # TODO: Itachi의 프레임 인덱스 설정 (나중에 추가)
        self.idle_frames = list(range(42, 46))
        self.run_frames = list(range(6, 12))
        self.hit_frames = [46, 47]
        # ... 나머지 동작들도 추가 필요

        # 이타치 전용 히트박스 설정
        self.hitbox_idle = {'scale_x': 0.7, 'scale_y': 0.7, 'x_offset': 0, 'y_offset': 0}
        self.hitbox_run = {'scale_x': 0.7, 'scale_y': 0.7, 'x_offset': 0, 'y_offset': 5}
        self.hitbox_jump = {'scale_x': 0.7, 'scale_y': 0.7, 'x_offset': 0, 'y_offset': 5}
        self.hitbox_normal_attack = {'scale_x': 0.7, 'scale_y': 0.7, 'x_offset': 0, 'y_offset': 5}
        self.hitbox_defense = {'scale_x': 1.0, 'scale_y': 0.95, 'x_offset': 0, 'y_offset': 5}
        self.hitbox_special_attack = {'scale_x': 1.1, 'scale_y': 1.05, 'x_offset': 0, 'y_offset': 5}
        self.hitbox_ranged_attack = {'scale_x': 0.7, 'scale_y': 0.7, 'x_offset': 0, 'y_offset': 5}
        self.hitbox_hit = {'scale_x': 0.7, 'scale_y': 0.7, 'x_offset': 0, 'y_offset': -5}  # 피격 히트박스

class JiraiyaConfig(CharacterConfig):
    def __init__(self):
        super().__init__()
        self.name = "Jiraiya"
        self.image_path = "Characters_Jiraiya_clean.png"
        self.frames = JIRAIYA_FRAMES

        # TODO: Jiraiya의 프레임 인덱스 설정 (나중에 추가)
        self.idle_frames = list(range(42, 45))  # 임시
        self.run_frames = list(range(6, 12))  # 임시
        # ... 나머지 동작들도 추가 필요

        # 지라이야 전용 히트박스 설정
        self.hitbox_idle = {'scale_x': 0.65, 'scale_y': 0.78, 'x_offset': 0, 'y_offset': 3}
        self.hitbox_run = {'scale_x': 0.65, 'scale_y': 0.78, 'x_offset': 0, 'y_offset': 3}
        self.hitbox_jump = {'scale_x': 0.65, 'scale_y': 0.78, 'x_offset': 0, 'y_offset': 3}
        self.hitbox_normal_attack = {'scale_x': 0.65, 'scale_y': 0.78, 'x_offset': 0, 'y_offset': 3}
        self.hitbox_defense = {'scale_x': 1.0, 'scale_y': 1.0, 'x_offset': 0, 'y_offset': 3}
        self.hitbox_special_attack = {'scale_x': 1.15, 'scale_y': 1.15, 'x_offset': 0, 'y_offset': 3}
        self.hitbox_ranged_attack = {'scale_x': 0.65, 'scale_y': 0.78, 'x_offset': 0, 'y_offset': 3}
        self.hitbox_hit = {'scale_x': 0.65, 'scale_y': 0.78, 'x_offset': 0, 'y_offset': 3}  # 피격 히트박스

# 캐릭터 설정 딕셔너리
CHARACTER_CONFIGS = {
    "Naruto": NarutoConfig,
    "Itachi": ItachiConfig,
    "Jiraiya": JiraiyaConfig
}
