#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
262건의 예약 더미 데이터 생성 스크립트
2025년 11월 1일 ~ 11월 30일 (22일 운영)
"""

import json
import random
from datetime import datetime, timedelta

# 시드 설정 (재현 가능하도록)
random.seed(42)

# ============ 기본 데이터 풀 ============

# 고객 이름 (50개)
CUSTOMER_NAMES = [
    "김민준", "이서연", "박지훈", "최수아", "정예준", "강하은", "조시우", "윤서아", "임도윤", "한예은",
    "오지호", "신서윤", "장우진", "권지우", "황서준", "송하린", "배은우", "노유나", "류시현", "문채원",
    "서준혁", "안소율", "이도현", "최예린", "김하준", "박서영", "정지훈", "강채은", "조민서", "윤수호",
    "임유진", "한지안", "오건우", "신다은", "장재윤", "권서진", "황민재", "송아인", "배도윤", "노채아",
    "류준서", "문지유", "서윤호", "안하율", "이서준", "최지민", "김예준", "박수빈", "정하은", "강시우"
]

# 일자별 행사 정보
EVENTS = [
    {"date": "2025-11-01", "count": 12, "name": "IVE 콘서트 Day1", "venue": "KSPO돔", "type": "콘서트", "start": "18:00", "end": "21:30"},
    {"date": "2025-11-02", "count": 15, "name": "IVE 콘서트 Day2", "venue": "KSPO돔", "type": "콘서트", "start": "18:00", "end": "21:30"},
    {"date": "2025-11-03", "count": 14, "name": "IVE 콘서트 Day3", "venue": "KSPO돔", "type": "콘서트", "start": "18:00", "end": "21:30"},
    {"date": "2025-11-08", "count": 10, "name": "KBO 준플레이오프", "venue": "잠실야구장", "type": "스포츠", "start": "18:30", "end": "21:30"},
    {"date": "2025-11-09", "count": 16, "name": "세븐틴 콘서트 Day1", "venue": "고척스카이돔", "type": "콘서트", "start": "18:00", "end": "21:00"},
    {"date": "2025-11-10", "count": 15, "name": "세븐틴 콘서트 Day2", "venue": "고척스카이돔", "type": "콘서트", "start": "18:00", "end": "21:00"},
    {"date": "2025-11-12", "count": 8, "name": "건국대 녹색지대 Day1", "venue": "건국대", "type": "대학축제", "start": "17:00", "end": "23:00"},
    {"date": "2025-11-13", "count": 9, "name": "건국대 녹색지대 Day2", "venue": "건국대", "type": "대학축제", "start": "17:00", "end": "23:00"},
    {"date": "2025-11-14", "count": 11, "name": "서울시립대 축제", "venue": "서울시립대", "type": "대학축제", "start": "17:00", "end": "23:00"},
    {"date": "2025-11-15", "count": 14, "name": "KGMA Day1", "venue": "인스파이어 아레나", "type": "콘서트", "start": "18:00", "end": "22:00"},
    {"date": "2025-11-16", "count": 18, "name": "KGMA Day2", "venue": "인스파이어 아레나", "type": "콘서트", "start": "18:00", "end": "22:00"},
    {"date": "2025-11-17", "count": 16, "name": "에스파 콘서트 Day1", "venue": "잠실주경기장", "type": "콘서트", "start": "18:00", "end": "21:00"},
    {"date": "2025-11-19", "count": 10, "name": "한양대 ERICA 축제", "venue": "한양대 ERICA", "type": "대학축제", "start": "17:00", "end": "22:00"},
    {"date": "2025-11-20", "count": 12, "name": "K-POP 뮤직 위크", "venue": "광화문광장", "type": "페스티벌", "start": "18:00", "end": "21:00"},
    {"date": "2025-11-21", "count": 11, "name": "그랜드민트페스티벌", "venue": "올림픽공원", "type": "페스티벌", "start": "17:00", "end": "22:00"},
    {"date": "2025-11-22", "count": 13, "name": "시그리드 내한공연", "venue": "블루스퀘어", "type": "콘서트", "start": "19:30", "end": "22:00"},
    {"date": "2025-11-23", "count": 20, "name": "NCT DREAM 콘서트 Day1", "venue": "KSPO돔", "type": "콘서트", "start": "18:00", "end": "21:00"},
    {"date": "2025-11-24", "count": 19, "name": "NCT DREAM 콘서트 Day2", "venue": "KSPO돔", "type": "콘서트", "start": "18:00", "end": "21:00"},
    {"date": "2025-11-27", "count": 8, "name": "프로농구", "venue": "잠실실내체육관", "type": "스포츠", "start": "19:00", "end": "21:00"},
    {"date": "2025-11-28", "count": 9, "name": "프로농구", "venue": "잠실실내체육관", "type": "스포츠", "start": "19:00", "end": "21:00"},
    {"date": "2025-11-29", "count": 10, "name": "V-리그 배구", "venue": "수원실내체육관", "type": "스포츠", "start": "19:00", "end": "21:00"},
    {"date": "2025-11-30", "count": 12, "name": "뉴진스 콘서트", "venue": "고척스카이돔", "type": "콘서트", "start": "18:00", "end": "21:00"},
]

# 배송 주소 데이터
ADDRESSES = {
    "서울-강남권": {
        "region": "서울",
        "cities": {
            "강남구": ["서울시 강남구 테헤란로 123", "서울시 강남구 역삼동 456", "서울시 강남구 삼성로 789"],
            "서초구": ["서울시 서초구 반포대로 234", "서울시 서초구 서초대로 567"],
            "송파구": ["서울시 송파구 올림픽로 321", "서울시 송파구 송파대로 654"],
            "강동구": ["서울시 강동구 천호대로 890", "서울시 강동구 명일로 111"],
        },
        "delivery_hours": (3, 4)
    },
    "서울-강북권": {
        "region": "서울",
        "cities": {
            "마포구": ["서울시 마포구 월드컵로 567", "서울시 마포구 와우산로 222"],
            "용산구": ["서울시 용산구 한강대로 890", "서울시 용산구 이태원로 333"],
            "영등포구": ["서울시 영등포구 여의대로 111", "서울시 영등포구 영등포로 444"],
            "종로구": ["서울시 종로구 세종대로 222", "서울시 종로구 종로 555"],
            "중구": ["서울시 중구 을지로 333"],
        },
        "delivery_hours": (3.5, 4.5)
    },
    "서울-기타": {
        "region": "서울",
        "cities": {
            "동작구": ["서울시 동작구 상도로 444", "서울시 동작구 동작대로 666"],
            "관악구": ["서울시 관악구 신림로 555", "서울시 관악구 관악로 777"],
            "성북구": ["서울시 성북구 성북로 666", "서울시 성북구 보문로 888"],
            "노원구": ["서울시 노원구 노원로 777", "서울시 노원구 동일로 999"],
        },
        "delivery_hours": (3.5, 4.5)
    },
    "경기-남부": {
        "region": "경기",
        "cities": {
            "성남시 분당구": ["경기도 성남시 분당구 정자로 888", "경기도 성남시 분당구 판교로 111", "경기도 성남시 분당구 황새울로 222"],
            "수원시 영통구": ["경기도 수원시 영통구 광교로 999", "경기도 수원시 영통구 영통로 333"],
            "용인시 수지구": ["경기도 용인시 수지구 신수로 1010", "경기도 용인시 수지구 포은대로 444"],
        },
        "delivery_hours": (4, 5)
    },
    "경기-북부": {
        "region": "경기",
        "cities": {
            "고양시 일산서구": ["경기도 고양시 일산서구 중앙로 1111", "경기도 고양시 일산서구 킨텍스로 555"],
            "부천시": ["경기도 부천시 원미구 중동로 1212", "경기도 부천시 소사구 소사로 777"],
            "남양주시": ["경기도 남양주시 다산로 1313", "경기도 남양주시 화도읍 888"],
        },
        "delivery_hours": (4, 5)
    },
    "경기-기타": {
        "region": "경기",
        "cities": {
            "화성시": ["경기도 화성시 동탄대로 1414", "경기도 화성시 병점로 999"],
            "평택시": ["경기도 평택시 평택로 1515"],
            "안양시": ["경기도 안양시 동안구 평촌대로 1616"],
        },
        "delivery_hours": (4.5, 5.5)
    },
    "인천": {
        "region": "인천",
        "cities": {
            "남동구": ["인천시 남동구 구월동 1717", "인천시 남동구 인주대로 111"],
            "연수구": ["인천시 연수구 송도동 1818", "인천시 연수구 센트럴로 222"],
            "부평구": ["인천시 부평구 부평대로 1919", "인천시 부평구 경원대로 333"],
        },
        "delivery_hours": (4, 5)
    },
    "부산": {
        "region": "부산",
        "cities": {
            "해운대구": ["부산시 해운대구 해운대로 2020", "부산시 해운대구 센텀로 111"],
            "부산진구": ["부산시 부산진구 서면로 2121", "부산시 부산진구 중앙대로 222"],
            "남구": ["부산시 남구 수영로 2222"],
        },
        "delivery_hours": (7, 8)
    },
    "대구": {
        "region": "대구",
        "cities": {
            "수성구": ["대구시 수성구 동대구로 2323", "대구시 수성구 범어로 111"],
            "달서구": ["대구시 달서구 달구벌대로 2424", "대구시 달서구 성서로 222"],
        },
        "delivery_hours": (7, 8)
    },
    "대전": {
        "region": "대전",
        "cities": {
            "서구": ["대전시 서구 둔산로 2525", "대전시 서구 대덕대로 111"],
            "유성구": ["대전시 유성구 대학로 2626"],
        },
        "delivery_hours": (5, 6)
    },
    "광주": {
        "region": "광주",
        "cities": {
            "서구": ["광주시 서구 상무대로 2727", "광주시 서구 치평로 111"],
            "광산구": ["광주시 광산구 수완로 2828"],
        },
        "delivery_hours": (5, 6)
    },
    "기타": {
        "region": "기타",
        "cities": {
            "울산시": ["울산시 남구 삼산로 2929"],
            "세종시": ["세종시 한누리대로 3030"],
            "강원도": ["강원도 춘천시 중앙로 3131"],
        },
        "delivery_hours": (8, 10)
    },
}

# 지역 분포 (배송 183건 기준)
REGION_DISTRIBUTION = [
    ("서울-강남권", 0.202),  # 37건
    ("서울-강북권", 0.148),  # 27건
    ("서울-기타", 0.098),    # 18건
    ("경기-남부", 0.148),    # 27건
    ("경기-북부", 0.120),    # 22건
    ("경기-기타", 0.033),    # 6건
    ("인천", 0.098),         # 18건
    ("부산", 0.060),         # 11건
    ("대구", 0.033),         # 6건
    ("대전", 0.022),         # 4건
    ("광주", 0.022),         # 4건
    ("기타", 0.016),         # 3건
]

# 내용물 카테고리 분포
ITEM_TYPES = [
    ("의류", 0.35),
    ("식품(상온)", 0.20),
    ("전자제품", 0.15),
    ("화장품", 0.10),
    ("생활용품", 0.08),
    ("식품(냉장)", 0.05),
    ("서적/문구", 0.04),
    ("기타", 0.02),
    ("식품(냉동)", 0.01),
]

# 짐 크기 분포
ITEM_SIZES = [
    ("Small", 0.15, 6800),
    ("Medium", 0.65, 7800),
    ("Large", 0.20, 12800),
]

# 결제 수단 분포
PAYMENT_METHODS = [
    ("카드", 0.35),
    ("간편결제", 0.30),
    ("계좌이체", 0.25),
    ("현금", 0.10),
]

def weighted_choice(choices):
    """가중치 기반 랜덤 선택"""
    items = [c[0] for c in choices]
    weights = [c[1] for c in choices]
    return random.choices(items, weights=weights, k=1)[0]

def generate_phone():
    """전화번호 생성"""
    return f"010-{random.randint(1000, 9999):04d}-{random.randint(1000, 9999):04d}"

def parse_time(date_str, time_str):
    """날짜와 시간 문자열을 datetime으로 변환"""
    return datetime.strptime(f"{date_str} {time_str}", "%Y-%m-%d %H:%M")

def to_iso(dt):
    """datetime을 ISO 형식 문자열로 변환"""
    if dt is None:
        return None
    return dt.strftime("%Y-%m-%dT%H:%M:%SZ")

def get_next_business_day(dt):
    """다음 영업일 반환 (토,일 -> 월)"""
    # 토요일(5) 또는 일요일(6)이면 월요일로
    while dt.weekday() >= 5:
        dt += timedelta(days=1)
    return dt

def generate_reserved_at(event_date, event_start_time):
    """예약 시간 생성"""
    event_dt = parse_time(event_date, event_start_time)

    # 예약 시점 분포
    choice = random.random()

    if choice < 0.10:  # 6~7일 전 (10%)
        days_before = random.randint(6, 7)
        hour = random.randint(10, 22)
    elif choice < 0.25:  # 4~5일 전 (15%)
        days_before = random.randint(4, 5)
        hour = random.randint(10, 22)
    elif choice < 0.40:  # 2~3일 전 (15%)
        days_before = random.randint(2, 3)
        hour = random.randint(10, 22)
    elif choice < 0.60:  # 당일 09:00~12:00 (20%)
        days_before = 0
        hour = random.randint(9, 11)
    elif choice < 0.90:  # 당일 12:00~15:00 (30%)
        days_before = 0
        hour = random.randint(12, 14)
    else:  # 현장 예약 15:00~18:00 (10%)
        days_before = 0
        hour = random.randint(15, 17)

    reserved_dt = event_dt - timedelta(days=days_before)
    reserved_dt = reserved_dt.replace(hour=hour, minute=random.randint(0, 59), second=random.randint(0, 59))

    return reserved_dt

def generate_dropoff_time(event_date, event_start_time):
    """맡김 시간 생성 (행사 시작 1~3시간 전)"""
    event_start = parse_time(event_date, event_start_time)

    # 분포: 3시간 전 5%, 2.5시간 전 15%, 2시간 전 35%, 1.5시간 전 30%, 1시간 전 15%
    choice = random.random()
    if choice < 0.05:
        hours_before = 3.0
    elif choice < 0.20:
        hours_before = 2.5
    elif choice < 0.55:
        hours_before = 2.0
    elif choice < 0.85:
        hours_before = 1.5
    else:
        hours_before = 1.0

    dropoff_dt = event_start - timedelta(hours=hours_before)
    # 약간의 랜덤성 추가
    dropoff_dt += timedelta(minutes=random.randint(-10, 10))

    return dropoff_dt

def generate_pickup_time(event_date, event_end_time):
    """찾음 시간 생성 (행사 종료 후 0~2시간) - 현장수령만"""
    event_end = parse_time(event_date, event_end_time)

    # 분포: 종료 직후~30분 45%, 30분~1시간 40%, 1~2시간 15%
    choice = random.random()
    if choice < 0.45:
        minutes_after = random.randint(0, 30)
    elif choice < 0.85:
        minutes_after = random.randint(30, 60)
    else:
        minutes_after = random.randint(60, 120)

    pickup_dt = event_end + timedelta(minutes=minutes_after)

    return pickup_dt

def generate_delivery_changed_at(dropoff_time, event_start, event_end, is_app_change):
    """배송 변경 시간 생성 (앱 변경 건만)"""
    if not is_app_change:
        return None

    # 변경 시점 분포: 행사 시작 전 35%, 행사 중 40%, 행사 후 25%
    choice = random.random()

    if choice < 0.35:  # 행사 시작 전
        # dropoffTime + 30분~2시간
        minutes_after = random.randint(30, 120)
        changed_dt = dropoff_time + timedelta(minutes=minutes_after)
        # 행사 시작 전이어야 함
        if changed_dt > event_start:
            changed_dt = event_start - timedelta(minutes=random.randint(5, 30))
    elif choice < 0.75:  # 행사 중
        # eventStartTime + 30분~2시간
        minutes_after = random.randint(30, 120)
        changed_dt = event_start + timedelta(minutes=minutes_after)
        # 행사 종료 전이어야 함
        if changed_dt > event_end:
            changed_dt = event_end - timedelta(minutes=random.randint(5, 30))
    else:  # 행사 후
        # eventEndTime + 10분~1시간
        minutes_after = random.randint(10, 60)
        changed_dt = event_end + timedelta(minutes=minutes_after)

    return changed_dt

def get_region_group(region_group_name):
    """지역 그룹명 반환"""
    return region_group_name

def select_address():
    """배송 주소 선택"""
    region_group = weighted_choice(REGION_DISTRIBUTION)
    region_data = ADDRESSES[region_group]

    city = random.choice(list(region_data["cities"].keys()))
    address = random.choice(region_data["cities"][city])

    return {
        "address": address,
        "region": region_data["region"],
        "city": city,
        "regionGroup": region_group,
        "deliveryHours": region_data["delivery_hours"]
    }

def generate_reservations():
    """262건의 예약 데이터 생성"""
    reservations = []
    reservation_id = 1

    # 재방문 고객 설정 (11명, 각각 2회 예약)
    # 첫 번째 예약과 두 번째 예약 간격은 최소 7일
    returning_customers = []
    returning_phones = [generate_phone() for _ in range(11)]

    # 재방문 고객 매핑: (첫 예약 날짜 인덱스, 재방문 날짜 인덱스)
    # 최소 7일 간격 유지
    returning_schedule = [
        (0, 7),   # 11/1 -> 11/9
        (1, 8),   # 11/2 -> 11/10
        (2, 9),   # 11/3 -> 11/12
        (4, 11),  # 11/9 -> 11/17
        (5, 12),  # 11/10 -> 11/19
        (6, 13),  # 11/12 -> 11/20
        (7, 14),  # 11/13 -> 11/21
        (9, 16),  # 11/15 -> 11/23
        (10, 17), # 11/16 -> 11/24
        (11, 19), # 11/17 -> 11/28
        (12, 20), # 11/19 -> 11/29
    ]

    # 각 행사별로 재방문 고객 배치
    returning_first = {}  # 첫 방문 배치
    returning_second = {} # 재방문 배치

    for i, (first_idx, second_idx) in enumerate(returning_schedule):
        phone = returning_phones[i]
        if first_idx not in returning_first:
            returning_first[first_idx] = []
        if second_idx not in returning_second:
            returning_second[second_idx] = []
        returning_first[first_idx].append(phone)
        returning_second[second_idx].append(phone)

    # 총 수익 계산용
    total_revenue = 0

    for event_idx, event in enumerate(EVENTS):
        event_date = event["date"]
        count = event["count"]

        # 이 행사에서 배송/현장수령 비율 결정
        delivery_count = int(count * 0.7)  # 70% 배송
        pickup_count = count - delivery_count  # 30% 현장수령

        # 배송 건 중 앱 변경 비율 (40%)
        app_change_count = int(delivery_count * 0.4)

        for i in range(count):
            is_delivery = i < delivery_count
            is_app_change = is_delivery and i < app_change_count

            # 재방문 고객 확인
            is_returning = False
            customer_phone = None

            if event_idx in returning_second and returning_second[event_idx]:
                customer_phone = returning_second[event_idx].pop(0)
                is_returning = True
            elif event_idx in returning_first and returning_first[event_idx]:
                customer_phone = returning_first[event_idx].pop(0)
                is_returning = False
            else:
                customer_phone = generate_phone()
                is_returning = False

            # 기본 정보 생성
            res_id = f"RES-{event_date.replace('-', '')}-{reservation_id:04d}"
            reservation_id += 1

            # 시간 정보
            event_start = parse_time(event_date, event["start"])
            event_end = parse_time(event_date, event["end"])

            reserved_at = generate_reserved_at(event_date, event["start"])
            dropoff_time = generate_dropoff_time(event_date, event["start"])

            # 현장수령/배송에 따른 시간 설정
            if is_delivery:
                pickup_time = None

                # 배송 변경 시간
                delivery_changed_at = generate_delivery_changed_at(
                    dropoff_time, event_start, event_end, is_app_change
                )

                # 배송 집하 시간 (당일 23:00)
                delivery_pickup_time = parse_time(event_date, "23:00")

                # 배송 시작 시간 (익일 또는 월요일 09:00~10:00)
                next_day = datetime.strptime(event_date, "%Y-%m-%d") + timedelta(days=1)
                delivery_start_date = get_next_business_day(next_day)
                delivery_start_time = delivery_start_date.replace(
                    hour=9, minute=random.randint(0, 45), second=0
                )

                # 배송 주소 선택
                addr_info = select_address()

                # 배송 완료 시간 (시작 + 거리별 소요 시간)
                min_hours, max_hours = addr_info["deliveryHours"]
                delivery_hours = random.uniform(min_hours, max_hours)
                delivery_completed_time = delivery_start_time + timedelta(hours=delivery_hours)

                delivery_address = addr_info["address"]
                delivery_region = addr_info["region"]
                delivery_city = addr_info["city"]
                delivery_region_group = addr_info["regionGroup"]
            else:
                pickup_time = generate_pickup_time(event_date, event["end"])
                delivery_changed_at = None
                delivery_pickup_time = None
                delivery_start_time = None
                delivery_completed_time = None
                delivery_address = None
                delivery_region = None
                delivery_city = None
                delivery_region_group = None

            # 짐 정보
            item_type = weighted_choice(ITEM_TYPES)
            size_info = random.choices(ITEM_SIZES, weights=[s[1] for s in ITEM_SIZES], k=1)[0]
            item_size = size_info[0]
            original_price = size_info[2]

            # 할인 (5~10% 정도에만)
            discount_amount = 0
            discount_code = None
            if random.random() < 0.08:  # 8%
                if is_returning:
                    discount_code = "WELCOME10"
                    discount_amount = int(original_price * 0.1)
                else:
                    discount_code = "FIRST2000"
                    discount_amount = 2000

            total_price = original_price - discount_amount
            total_revenue += total_price

            # 결제 수단
            payment_method = weighted_choice(PAYMENT_METHODS)

            # 고객 이름
            customer_name = random.choice(CUSTOMER_NAMES)

            # 특별 요청 (10% 정도)
            special_request = None
            if random.random() < 0.10:
                requests = ["취급주의", "파손주의", "습기주의", "직사광선 피해주세요", None]
                special_request = random.choice(requests)

            reservation = {
                "id": res_id,
                "reservedAt": to_iso(reserved_at),
                "dropoffTime": to_iso(dropoff_time),
                "pickupTime": to_iso(pickup_time),
                "status": "완료",

                "customerName": customer_name,
                "customerPhone": customer_phone,
                "isReturningCustomer": is_returning,

                "eventName": event["name"],
                "eventDate": event_date,
                "eventVenue": event["venue"],
                "eventType": event["type"],
                "eventStartTime": to_iso(event_start),
                "eventEndTime": to_iso(event_end),

                "itemType": item_type,
                "itemSize": item_size,
                "itemCount": random.choices([1, 2, 3], weights=[0.85, 0.12, 0.03], k=1)[0],
                "specialRequest": special_request,

                "deliveryType": "배송" if is_delivery else "현장수령",
                "deliveryStatus": "완료",
                "deliveryChangedAt": to_iso(delivery_changed_at),
                "deliveryPickupTime": to_iso(delivery_pickup_time),
                "deliveryStartTime": to_iso(delivery_start_time),
                "deliveryCompletedTime": to_iso(delivery_completed_time),
                "deliveryAddress": delivery_address,
                "deliveryRegion": delivery_region,
                "deliveryCity": delivery_city,
                "deliveryRegionGroup": delivery_region_group,

                "paymentMethod": payment_method,
                "originalPrice": original_price,
                "discountAmount": discount_amount,
                "discountCode": discount_code,
                "totalPrice": total_price,
            }

            reservations.append(reservation)

    return reservations, total_revenue

def calculate_stats(reservations):
    """통계 계산"""
    total = len(reservations)
    total_revenue = sum(r["totalPrice"] for r in reservations)
    avg_price = total_revenue / total if total > 0 else 0

    # 행사 유형별 통계
    event_types = {}
    for r in reservations:
        t = r["eventType"]
        event_types[t] = event_types.get(t, 0) + 1

    # 재방문 고객 수
    returning_count = sum(1 for r in reservations if r["isReturningCustomer"])

    # 대시보드 주간 (11/17~11/23)
    dashboard_reservations = [r for r in reservations
                              if "2025-11-17" <= r["eventDate"] <= "2025-11-23"]
    dashboard_count = len(dashboard_reservations)
    dashboard_revenue = sum(r["totalPrice"] for r in dashboard_reservations)

    # 지역 그룹 통계 (배송 건만)
    region_groups = {}
    delivery_reservations = [r for r in reservations if r["deliveryType"] == "배송"]
    for r in delivery_reservations:
        rg = r["deliveryRegionGroup"]
        if rg:
            region_groups[rg] = region_groups.get(rg, 0) + 1

    # 상위 3개 지역
    sorted_regions = sorted(region_groups.items(), key=lambda x: x[1], reverse=True)[:3]
    region_group_top3 = [
        {"region": rg, "percentage": round(count / len(delivery_reservations) * 100, 1), "count": count}
        for rg, count in sorted_regions
    ]

    return {
        "period": "2025-11-01 ~ 2025-11-30",
        "phase": "베타 테스트 / 시장 검증 단계",
        "operatingDays": 22,
        "totalReservations": total,
        "dailyAverage": round(total / 22, 1),
        "dailyTarget": 100,
        "achievementRate": f"{round(total / 22 / 100 * 100, 1)}%",
        "totalRevenue": total_revenue,
        "averagePrice": round(avg_price),
        "returningCustomerRate": round(returning_count / total * 100, 1),
        "dropoffPeakHours": [15, 16, 17, 18],
        "pickupPeakHours": [21, 22, 23],
        "deliveryChangePeakHours": [19, 20, 21],
        "dashboardPeriod": "2025-11-17 ~ 2025-11-23",
        "dashboardReservations": dashboard_count,
        "dashboardRevenue": dashboard_revenue,
        "regionGroupTop3": region_group_top3,
        "note": "초기 런칭 기간으로 손익분기점 미달을 감수하고 다양한 행사 유형 테스트"
    }

def main():
    print("예약 데이터 생성 중...")

    reservations, total_revenue = generate_reservations()
    metadata = calculate_stats(reservations)

    data = {
        "reservations": reservations,
        "metadata": metadata
    }

    # JSON 파일 저장
    output_path = "/home/user/team3_practice/src/data/reservations_2025_11.json"
    with open(output_path, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

    print(f"\n✅ 생성 완료: {output_path}")
    print(f"\n📊 검증 결과:")
    print(f"  - 총 건수: {len(reservations)}건")
    print(f"  - 운영일: {metadata['operatingDays']}일")
    print(f"  - 일평균: {metadata['dailyAverage']}건")
    print(f"  - 총 수익: {metadata['totalRevenue']:,}원")
    print(f"  - 평균 가격: {metadata['averagePrice']:,}원")
    print(f"  - 재방문 고객률: {metadata['returningCustomerRate']}%")
    print(f"  - 대시보드 주간 건수: {metadata['dashboardReservations']}건")
    print(f"  - 대시보드 주간 수익: {metadata['dashboardRevenue']:,}원")

    # 행사 유형별 통계
    event_types = {}
    for r in reservations:
        t = r["eventType"]
        event_types[t] = event_types.get(t, 0) + 1

    print(f"\n📌 행사 유형별 분포:")
    for t, c in sorted(event_types.items(), key=lambda x: x[1], reverse=True):
        print(f"  - {t}: {c}건 ({round(c/len(reservations)*100, 1)}%)")

    # 배송/현장수령 비율
    delivery_count = sum(1 for r in reservations if r["deliveryType"] == "배송")
    print(f"\n📦 배송 방식:")
    print(f"  - 배송: {delivery_count}건 ({round(delivery_count/len(reservations)*100, 1)}%)")
    print(f"  - 현장수령: {len(reservations) - delivery_count}건 ({round((len(reservations)-delivery_count)/len(reservations)*100, 1)}%)")

    # 짐 크기 분포
    sizes = {}
    for r in reservations:
        s = r["itemSize"]
        sizes[s] = sizes.get(s, 0) + 1

    print(f"\n📏 짐 크기 분포:")
    for s in ["Small", "Medium", "Large"]:
        if s in sizes:
            print(f"  - {s}: {sizes[s]}건 ({round(sizes[s]/len(reservations)*100, 1)}%)")

if __name__ == "__main__":
    main()
