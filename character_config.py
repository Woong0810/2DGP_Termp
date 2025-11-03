# 캐릭터별 프레임 설정 정보
# 각 캐릭터마다 어떤 동작이 몇 번째 프레임에 있는지 정의
from characters_naruto_frames import FRAMES as NARUTO_FRAMES
from characters_itachi_frames import FRAMES as ITACHI_FRAMES
from characters_jiraiya_frames import FRAMES as JIRAIYA_FRAMES

class CharacterConfig:
    # 캐릭터 설정 베이스 클래스
    def __init__(self):
        self.name = ""
        self.image_path = ""
        self.frames = []  # 전체 프레임 정보

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

class ItachiConfig(CharacterConfig):
    def __init__(self):
        super().__init__()
        self.name = "Itachi"
        self.image_path = "Characters_Itachi_clean.png"
        self.frames = ITACHI_FRAMES

        # Itachi의 프레임 인덱스 설정 (나중에 추가)
        self.idle_frames = list(range(0, 6))  # 임시
        self.run_frames = list(range(6, 12))  # 임시
        # ... 나머지 동작들도 추가 필요

class JiraiyaConfig(CharacterConfig):
    def __init__(self):
        super().__init__()
        self.name = "Jiraiya"
        self.image_path = "Characters_Jiraiya_clean.png"
        self.frames = JIRAIYA_FRAMES

        # Jiraiya의 프레임 인덱스 설정 (나중에 추가)
        self.idle_frames = list(range(0, 6))  # 임시
        self.run_frames = list(range(6, 12))  # 임시
        # ... 나머지 동작들도 추가 필요

# 캐릭터 설정 딕셔너리
CHARACTER_CONFIGS = {
    "Naruto": NarutoConfig,
    "Itachi": ItachiConfig,
    "Jiraiya": JiraiyaConfig
}

