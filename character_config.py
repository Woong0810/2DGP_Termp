from character_itachi_frames import FRAMES as ITACHI_FRAMES
from character_itachi_sa_frames import FRAMES as ITACHI_SPECIAL_FRAMES
from characters_jiraiya_frames import FRAMES as JIRAIYA_FRAMES
from character_naruto_frames import FRAMES as NARUTO_FRAMES
from character_naruto_sa_frames import FRAMES as NARUTO_SPECIAL_FRAMES
from character_naruto_sa_2_frames import FRAMES as NARUTO_SPECIAL2_FRAMES

# ===== 물리 기반 상수 설정 =====
PIXEL_PER_METER = (10.0 / 0.4)  # 10 pixel = 40 cm

# Run Speed
RUN_SPEED_KMPH = 25.0  # Km / Hour
RUN_SPEED_MPM = (RUN_SPEED_KMPH * 1000.0 / 60.0)
RUN_SPEED_MPS = (RUN_SPEED_MPM / 60.0)
RUN_SPEED_PPS = (RUN_SPEED_MPS * PIXEL_PER_METER)  # Pixel Per Second

# Jump Physics
JUMP_SPEED_KMPH = 20.0  # Km / Hour (공중에서 수평 이동)
JUMP_SPEED_MPM = (JUMP_SPEED_KMPH * 1000.0 / 60.0)
JUMP_SPEED_MPS = (JUMP_SPEED_MPM / 60.0)
JUMP_SPEED_PPS = (JUMP_SPEED_MPS * PIXEL_PER_METER)

JUMP_HEIGHT_METER = 4.5
JUMP_HEIGHT_PIXEL = (JUMP_HEIGHT_METER * PIXEL_PER_METER)

# Gravity
GRAVITY_MPS2 = 9.8 * 3  # m/s^2
GRAVITY_PPS2 = (GRAVITY_MPS2 * PIXEL_PER_METER)  # pixel/s^2

DOWN_ATTACK_SPEED_PPS = RUN_SPEED_PPS * 2.0

# ===== 애니메이션 속도 설정 =====
# 기본 애니메이션 시간
TIME_PER_ACTION = 1.0  # 한 사이클 애니메이션 재생 시간 (초)
ACTION_PER_TIME = 1.0 / TIME_PER_ACTION  # 초당 사이클 수

# 각 동작별 애니메이션 속도 배수 (ACTION_PER_TIME에 곱해서 사용)
IDLE_ANIMATION_SPEED = 1.5
RUN_ANIMATION_SPEED = 1.5
JUMP_ANIMATION_SPEED = 1.5
DEFENSE_ANIMATION_SPEED = 1.5
DASH_ANIMATION_SPEED = 2.0
SHIELD_EFFECT_ANIMATION_SPEED = 2.0
NORMAL_ATTACK_ANIMATION_SPEED = 2.0
SPECIAL_ATTACK_ANIMATION_SPEED = 0.2
RANGED_ATTACK_CHAR_ANIMATION_SPEED = 2.0
HIT_ANIMATION_SPEED = 1.5
STAND_UP_ANIMATION_SPEED = 1.5

# ===== 공격 설정 =====
# Normal Attack
NORMAL_ATTACK_DAMAGE = 5        # 기본 공격 데미지 (지상 기본 공격)
NORMAL_ATTACK_KNOCKBACK = 50    # 넉백 거리 (pixel)

# Jump Attack
JUMP_ATTACK_DAMAGE = 7          # 점프 공격 데미지 (일반 공격보다 약간 높음)
JUMP_ATTACK_KNOCKBACK = 50      # 넉백 거리 (기본 공격과 동일하게 설정)

# Special Attack
SPECIAL_ATTACK_DAMAGE = 15      # 스페셜 공격 데미지
SPECIAL_ATTACK_KNOCKBACK = 100  # 넉백 거리 (현재 코드는 넉백은 아직 사용 안 함)
SPECIAL_ATTACK_LOOP_COUNT = 3   # 마지막 프레임 반복 횟수

# Ranged Attack
RANGED_ATTACK_DAMAGE = 10       # 원거리 공격 데미지 (수리검 등)

# ===== 방어 설정 =====
DEFENSE_DAMAGE_REDUCTION = 0.5  # 방어 시 데미지 감소율 (50%)

# ===== 피격 설정 =====
HIT_DURATION = 0.3              # 피격 애니메이션 지속 시간 (초)
HIT_INVINCIBILITY_TIME = 0.5    # 피격 후 무적 시간 (초)
KNOCKBACK_DOWN_TIME = 2.0       # 넉백 후 누워있는 시간 (초)

# 히트스턴 프레임 수
HITSTUN_FRAMES_NORMAL = 16      # 지상 일반 공격에 맞았을 때
HITSTUN_FRAMES_JUMP = 18        # 점프 공격에 맞았을 때
HITSTUN_FRAMES_SPECIAL = 24     # 스페셜/강 공격에 맞았을 때
HITSTUN_FRAMES_RANGED = 12      # 수리검 등 원거리 공격에 맞았을 때

# ===== 히트스톱 설정 =====
HITSTOP_FRAMES_NORMAL = 3       # 지상 기본기
HITSTOP_FRAMES_JUMP = 4         # 점프 공격
HITSTOP_FRAMES_SPECIAL = 6      # 스페셜 / 강한 기술
HITSTOP_FRAMES_RANGED = 2       # 수리검 등 원거리

class CharacterConfig:
    def __init__(self):
        self.name = ""
        self.image_path = ""

        self.icon_default_path = ""
        self.icon_unselected_path = ""
        self.illust_image_path = ""
        self.name_image_path = ""
        self.special_attack_illust_image_path = ""

        self.frames = []  # 전체 프레임 정보

        # 캐릭터 스케일 (출력 크기 조정)
        self.scale_x = 1.0
        self.scale_y = 1.0

        # 캐릭터 그리기 오프셋 (피벗 차이 보정)
        self.draw_offset_y = 0

        # 상태별 전용 오프셋
        self.knockback_draw_offset_y = 0
        self.special_attack_offset_y = 0
        self.special_attack2_offset_y = 0

        # 각 동작의 프레임 인덱스 범위
        self.idle_frames = []
        self.run_frames = []
        self.normal_attack_frames = []
        self.normal_attack_segments = []
        self.jump_frames = []
        self.defense_frames = []
        self.special_attack_frames = []
        self.special_attack2_frames = []
        self.ranged_attack_frames = []
        self.hit_frames = []
        self.dash_frames = []

        # 모든 스페셜 공격을 프레임 단위 타격으로 처리
        self.special1_hit_frames = []
        self.special2_hit_frames = []
        self.special1_offset_x = 50
        self.special2_offset_x = 50

        # 히트박스 설정 (각 상태별 scale_x, scale_y, x_offset, y_offset)
        self.hitbox_idle = {'scale_x': 0.7, 'scale_y': 0.8, 'x_offset': 0, 'y_offset': 0}
        self.hitbox_run = {'scale_x': 0.7, 'scale_y': 0.8, 'x_offset': 0, 'y_offset': 0}
        self.hitbox_jump = {'scale_x': 0.7, 'scale_y': 0.8, 'x_offset': 0, 'y_offset': 0}
        self.hitbox_normal_attack = {'scale_x': 0.7, 'scale_y': 0.8, 'x_offset': 0, 'y_offset': 0}
        self.hitbox_defense = {'scale_x': 1.0, 'scale_y': 1.0, 'x_offset': 0, 'y_offset': 0}
        self.hitbox_special_attack = {'scale_x': 1.2, 'scale_y': 1.2, 'x_offset': 0, 'y_offset': 0}
        self.hitbox_special_attack2 = {'scale_x': 1.2, 'scale_y': 1.2, 'x_offset': 0, 'y_offset': 0}
        self.hitbox_ranged_attack = {'scale_x': 0.7, 'scale_y': 0.8, 'x_offset': 0, 'y_offset': 0}
        self.hitbox_hit = {'scale_x': 0.7, 'scale_y': 0.8, 'x_offset': 0, 'y_offset': 0}  # 피격 히트박스

        self.shuriken = {
            'image_path': None,
            'speed': 300,
            'rotation_speed': 720,
            'max_distance': 400,
            'damage': 10,
            'draw_size': None,
            'bbox_size': 20,
            'use_rotation': True,
            'frame': None
        }

class NarutoConfig(CharacterConfig):
    def __init__(self):
        super().__init__()
        self.name = "Naruto"
        self.image_path = "character_naruto.png"
        self.frames = NARUTO_FRAMES

        self.icon_default_path = "character_naruto_icon.png"
        self.icon_unselected_path = "character_naruto_icon_unselected.png"
        self.illust_image_path = "character_naruto_illust.png"
        self.name_image_path = "character_naruto_name.png"
        self.special_attack_illust_image_path = "character_naruto_sa_illust.png"

        self.shuriken = {
            'image_path': 'shuriken.png',
            'speed': 300,
            'rotation_speed': 720,
            'max_distance': 400,
            'damage': 10,
            'draw_size': (52, 52),
            'bbox_size': 20,
            'use_rotation': True,
            'frame': None
        }

        self.special_attack_image_path = "character_naruto_2.png"
        self.special_attack_frames_data = NARUTO_SPECIAL_FRAMES
        self.special_attack2_image_path = "character_naruto_sa_2.png"
        self.special_attack2_frames_data = NARUTO_SPECIAL2_FRAMES

        self.scale_x = 1.1
        self.scale_y = 1.2
        self.draw_offset_y = 0

        self.knockback_draw_offset_y = -10
        self.special_attack_offset_y = -10
        self.special_attack2_offset_y = 20

        self.idle_frames = list(range(0, 0 + 4))
        self.run_frames = list(range(10, 10 + 6))
        self.normal_attack_frames = list(range(35, 35 + 13))
        self.normal_attack_segments = [(35, 38), (39, 42), (43, 47)]
        self.run_attack_segments = [(61, 73)]
        self.up_attack_segments = [(48, 52)]
        self.down_attack_segments = [(271, 278)]
        self.jump_attack_segments = [(76, 79), (80, 82)]
        self.jump_frames = [20, 21]
        self.defense_frames = [19]
        self.special_attack_frames = list(range(0, 84))
        self.special_attack2_frames = list(range(0, 51))
        self.ranged_attack_frames = list(range(30, 30 + 3))
        self.hit_frames = [54, 55]
        self.knockback_frames = [53, 56, 57, 58, 59]
        self.stand_up_frames = [60, 18, 17, 16]
        self.dash_frames = list(range(101, 101 + 6))

        self.special1_hit_frames = [43, 44, 59, 67, 73, 78]
        self.special2_hit_frames = [26, 29, 32, 35, 38, 41, 44, 47, 50]
        self.special1_offset_x = 50
        self.special2_offset_x = 50

        self.hitbox_idle = {'scale_x': 0.7, 'scale_y': 0.8, 'x_offset': 0, 'y_offset': 0}
        self.hitbox_run = {'scale_x': 0.7, 'scale_y': 0.8, 'x_offset': 0, 'y_offset': 0}
        self.hitbox_jump = {'scale_x': 0.7, 'scale_y': 0.8, 'x_offset': 0, 'y_offset': 0}
        self.hitbox_normal_attack = {'scale_x': 0.7, 'scale_y': 0.8, 'x_offset': 0, 'y_offset': 0}
        self.hitbox_defense = {'scale_x': 1.0, 'scale_y': 1.0, 'x_offset': 0, 'y_offset': 0}
        self.hitbox_special_attack = {'scale_x': 20.0, 'scale_y': 4.0, 'x_offset': 0, 'y_offset': 0}
        self.hitbox_special_attack2 = {'scale_x': 20.0, 'scale_y': 1.0, 'x_offset': 0, 'y_offset': 0}
        self.hitbox_ranged_attack = {'scale_x': 0.7, 'scale_y': 0.8, 'x_offset': 0, 'y_offset': 0}
        self.hitbox_hit = {'scale_x': 0.7, 'scale_y': 0.8, 'x_offset': 0, 'y_offset': 0}

        self.normal_attack_data = [
            {
                'name': 'naruto_ground_A_1',  # 1타
                'damage': 4,
                'hitstop_frames': 3,
                'hitstun_frames': 14,
                'knockback': 10,
                'attacker_push': 10,
                'knockdown': False,
            },
            {
                'name': 'naruto_ground_A_2',  # 2타
                'damage': 4,
                'hitstop_frames': 3,
                'hitstun_frames': 14,
                'knockback': 15,
                'attacker_push': 15,
                'knockdown': False,
            },
            {
                'name': 'naruto_ground_A_3',  # 3타
                'damage': 8,
                'hitstop_frames': 5,
                'hitstun_frames': 20,
                'knockback': 80,
                'attacker_push': 20,
                'knockdown': True,
            },
        ]
        self.run_attack_data = [
            {
                'name': 'naruto_run_A',
                'damage': 6,
                'hitstop_frames': 4,
                'hitstun_frames': 18,
                'knockback': 70,
                'attacker_push': 40,
                'knockdown': True,
            },
        ]
        self.up_attack_data = [
            {
                'name': 'naruto_up_A',
                'damage': 5,
                'hitstop_frames': 3,
                'hitstun_frames': 18,
                'knockback': 30,
                'attacker_push': 0,
                'knockdown': False,
            },
        ]
        self.down_attack_data = [
            {
                'name': 'naruto_down_A',
                'damage': 7,
                'hitstop_frames': 4,
                'hitstun_frames': 22,
                'knockback': 80,
                'attacker_push': 10,
                'knockdown': True,
            },
        ]
        self.jump_attack_data = [
            {
                'name': 'naruto_jump_A_1',
                'damage': 5,
                'hitstop_frames': 3,
                'hitstun_frames': 16,
                'knockback': 15,
                'attacker_push': 5,
                'knockdown': False,
            },
            {
                'name': 'naruto_jump_A_2',
                'damage': 7,
                'hitstop_frames': 4,
                'hitstun_frames': 22,
                'knockback': 70,
                'attacker_push': 10,
                'knockdown': True,
            },
        ]
        self.special_attack_data = [
            {
                'name': 'naruto_special_A_1',
                'damage': 5,
                'hitstop_frames': 15,
                'hitstun_frames': 32,
                'knockback': 40,
                'knockdown': False,
            },
            {
                'name': 'naruto_special_A_2',
                'damage': 3.5,
                'hitstop_frames': 20,
                'hitstun_frames': 40,
                'knockback': 60,
                'knockdown': False,
            },
        ]

        self.ranged_attack_data = {
            'name': 'naruto_shuriken',
            'damage': 10,
            'hitstop_frames': 2,
            'hitstun_frames': 14,
            'knockback': 20,
            'knockdown': False,
        }

class ItachiConfig(CharacterConfig):
    def __init__(self):
        super().__init__()
        self.name = "Itachi"
        self.image_path = "character_itachi.png"
        self.frames = ITACHI_FRAMES

        self.icon_default_path = "character_itachi_icon.png"
        self.icon_unselected_path = "character_itachi_icon_unselected.png"
        self.illust_image_path = "character_itachi_illust.png"
        self.name_image_path = "character_itachi_name.png"
        self.special_attack_illust_image_path = "character_itachi_sa_illust.png"

        self.shuriken = {
            'image_path': 'shuriken2.png',
            'speed': 600,
            'rotation_speed': 0,
            'max_distance': 400,
            'damage': 8,
            'draw_size': (26, 13),
            'bbox_size': 20,
            'use_rotation': False,
            'frame': None
        }

        self.special_attack_image_path = "character_itachi_sa.png"
        self.special_attack_frames_data = ITACHI_SPECIAL_FRAMES

        from character_itachi_sa_2_frames import FRAMES as ITACHI_SPECIAL2_FRAMES
        self.special_attack2_image_path = "character_itachi_sa_2.png"
        self.special_attack2_frames_data = ITACHI_SPECIAL2_FRAMES

        self.scale_x = 1.0
        self.scale_y = 1.0
        self.draw_offset_y = 0

        self.knockback_draw_offset_y = -12
        self.special_attack_offset_y = 40
        self.special_attack2_offset_y = 0

        self.idle_frames = list(range(88, 88 + 4))
        self.run_frames = list(range(30, 30 + 6))
        self.normal_attack_frames = list(range(0, 13))
        self.normal_attack_segments = [(0, 3), (4, 7), (8, 12)]
        self.run_attack_segments = [(8, 12)]
        self.up_attack_segments = [(13, 16)]
        self.down_attack_segments = [(77, 84)]
        self.jump_attack_segments = [(94, 97), (98, 100)]
        self.jump_frames = [44, 45, 46, 47]
        self.defense_frames = [48]
        self.special_attack_frames = list(range(112, 112 + 12))
        self.special_attack2_frames = list(range(0, 60))
        self.ranged_attack_frames = list(range(49, 49 + 3))
        self.hit_frames = [86, 87]
        self.knockback_frames = [85, 69, 70, 71, 72, 73, 74, 75]
        self.stand_up_frames = [38, 37, 36]
        self.dash_frames = list(range(42, 42 + 2))

        self.special1_hit_frames = [7, 11, 13, 15, 17, 19, 21, 25, 28, 31, 34, 37, 41]
        self.special2_hit_frames = [15, 25, 35, 45, 55]
        self.special1_offset_x = 100
        self.special2_offset_x = 5

        self.hitbox_idle = {'scale_x': 0.7, 'scale_y': 0.7, 'x_offset': 0, 'y_offset': 0}
        self.hitbox_run = {'scale_x': 0.7, 'scale_y': 0.7, 'x_offset': 0, 'y_offset': 5}
        self.hitbox_jump = {'scale_x': 0.7, 'scale_y': 0.7, 'x_offset': 0, 'y_offset': 5}
        self.hitbox_normal_attack = {'scale_x': 0.7, 'scale_y': 0.7, 'x_offset': 0, 'y_offset': 5}
        self.hitbox_defense = {'scale_x': 1.0, 'scale_y': 0.95, 'x_offset': 0, 'y_offset': 5}
        self.hitbox_special_attack = {'scale_x': 25.0, 'scale_y': 1.05, 'x_offset': 0, 'y_offset': 5}
        self.hitbox_special_attack2 = {'scale_x': 20.0, 'scale_y': 4.0, 'x_offset': 0, 'y_offset': 5}
        self.hitbox_ranged_attack = {'scale_x': 0.7, 'scale_y': 0.7, 'x_offset': 0, 'y_offset': 5}
        self.hitbox_hit = {'scale_x': 0.7, 'scale_y': 0.7, 'x_offset': 0, 'y_offset': 0}

        self.normal_attack_data = [
            {
                'name': 'itachi_ground_A_1',
                'damage': 4,
                'hitstop_frames': 3,
                'hitstun_frames': 14,
                'knockback': 8,
                'attacker_push': 8,
                'knockdown': False,
            },
            {
                'name': 'itachi_ground_A_2',
                'damage': 4,
                'hitstop_frames': 3,
                'hitstun_frames': 14,
                'knockback': 12,
                'attacker_push': 12,
                'knockdown': False,
            },
            {
                'name': 'itachi_ground_A_3',
                'damage': 8,
                'hitstop_frames': 5,
                'hitstun_frames': 20,
                'knockback': 80,
                'attacker_push': 15,
                'knockdown': True,
            },
        ]
        self.run_attack_data = [
            {
                'name': 'itachi_run_A',
                'damage': 6,
                'hitstop_frames': 4,
                'hitstun_frames': 20,
                'knockback': 80,
                'attacker_push': 35,
                'knockdown': True,
            },
        ]
        self.up_attack_data = [
            {
                'name': 'itachi_up_A',
                'damage': 5,
                'hitstop_frames': 3,
                'hitstun_frames': 20,
                'knockback': 35,
                'attacker_push': 5,
                'knockdown': False,
            },
        ]
        self.down_attack_data = [
            {
                'name': 'itachi_down_A',
                'damage': 6,
                'hitstop_frames': 4,
                'hitstun_frames': 22,
                'knockback': 70,
                'attacker_push': 10,
                'knockdown': True,
            },
        ]
        self.jump_attack_data = [
            {
                'name': 'itachi_jump_A_1',
                'damage': 5,
                'hitstop_frames': 3,
                'hitstun_frames': 16,
                'knockback': 25,
                'attacker_push': 5,
                'knockdown': False,
            },
            {
                'name': 'itachi_jump_A_2',
                'damage': 7,
                'hitstop_frames': 4,
                'hitstun_frames': 22,
                'knockback': 70,
                'attacker_push': 10,
                'knockdown': True,
            },
        ]
        self.special_attack_data = [
            {
                'name': 'itachi_special_A_1',
                'damage': 2.4,
                'hitstop_frames': 10,
                'hitstun_frames': 45,
                'knockback': 60,
                'knockdown': False,
            },
            {
                'name': 'itachi_special_A_2',
                'damage': 6,
                'hitstop_frames': 15,
                'hitstun_frames': 60,
                'knockback': 60,
                'knockdown': True,
            },
        ]

class JiraiyaConfig(CharacterConfig):
    def __init__(self):
        super().__init__()
        self.name = "Jiraiya"
        self.image_path = "Characters_Jiraiya_clean.png"
        self.frames = JIRAIYA_FRAMES

        self.icon_default_path = "character_jiraiya_icon.png"
        self.icon_unselected_path = "character_jiraiya_icon_unselected.png"
        self.illust_image_path = "character_jiraiya_illust.png"
        self.name_image_path = "character_jiraiya_name.png"
        self.special_attack_illust_image_path = "character_jiraiya_sa_illust.png"

        self.scale_x = 1.1
        self.scale_y = 1.1
        self.draw_offset_y = 0

        self.knockback_draw_offset_y = -15
        self.special_attack_offset_y = 0
        self.special_attack2_offset_y = 0

        # TODO: Jiraiya의 프레임 인덱스 설정 (나중에 추가)
        self.idle_frames = list(range(54, 54 + 4))
        self.run_frames = list(range(39, 39 + 6))
        self.normal_attack_frames = list(range(0, 34))
        self.normal_attack_segments = [(0, 4), (5, 12), (28, 33)]
        self.run_attack_segments = [(50, 51)] # 상대 위치로 순간 이동 후 점프 공격?
        self.up_attack_segments = [(24, 28)]
        self.down_attack_segments = [] # 불 나가게?
        self.jump_attack_segments = [(13, 22), (34, 38)]
        self.jump_frames = [48, 49]
        self.defense_frames = [69]
        self.special_attack_frames = list(range(0, 84))
        self.special_attack2_frames = list(range(252, 252 + 39))
        self.ranged_attack_frames = list(range(69, 69 + 4))
        self.hit_frames = [58, 59]
        self.knockback_frames = [60, 65, 64, 63, 62, 61]
        self.stand_up_frames = [68, 45]
        self.dash_frames = list(range(87, 87 + 2))

        self.special1_hit_frames = []
        self.special2_hit_frames = []
        self.special1_offset_x = 50
        self.special2_offset_x = 50

        self.hitbox_idle = {'scale_x': 0.65, 'scale_y': 0.78, 'x_offset': 0, 'y_offset': 0}
        self.hitbox_run = {'scale_x': 0.65, 'scale_y': 0.78, 'x_offset': 0, 'y_offset': 0}
        self.hitbox_jump = {'scale_x': 0.65, 'scale_y': 0.78, 'x_offset': 0, 'y_offset': 0}
        self.hitbox_normal_attack = {'scale_x': 0.65, 'scale_y': 0.78, 'x_offset': 0, 'y_offset': 0}
        self.hitbox_defense = {'scale_x': 1.0, 'scale_y': 1.0, 'x_offset': 0, 'y_offset': 0}
        self.hitbox_special_attack = {'scale_x': 1.15, 'scale_y': 1.15, 'x_offset': 0, 'y_offset': 0}
        self.hitbox_special_attack2 = {'scale_x': 1.15, 'scale_y': 1.15, 'x_offset': 0, 'y_offset': 0}
        self.hitbox_ranged_attack = {'scale_x': 0.65, 'scale_y': 0.78, 'x_offset': 0, 'y_offset': 0}
        self.hitbox_hit = {'scale_x': 0.65, 'scale_y': 0.78, 'x_offset': 0, 'y_offset': 0}

CHARACTER_CONFIGS = {
    "Naruto": NarutoConfig,
    "Itachi": ItachiConfig,
    "Jiraiya": JiraiyaConfig
}
