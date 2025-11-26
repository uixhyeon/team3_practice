<template>
  <div class="pb-20">
    <!-- 상단 : 월 이동 -->
    <div class="flex items-center justify-between mb-3 mx-4 mt-4">
      <button
        @click="prevMonth"
        class="px-4 py-2 rounded-lg bg-gray-100 dark:bg-gray-800 text-gray-700 dark:text-gray-300 shrink-0 min-w-[60px] text-center"
      >
        이전
      </button>
      <div
        class="text-base font-semibold text-gray-900 dark:text-white flex-1 text-center"
      >
        {{ year }}년 {{ month + 1 }}월
      </div>
      <button
        @click="nextMonth"
        class="px-4 py-2 rounded-lg bg-gray-100 dark:bg-gray-800 text-gray-700 dark:text-gray-300 shrink-0 min-w-[60px] text-center"
      >
        다음
      </button>
    </div>
    <!-- 요일 헤더 -->
    <div
      class="grid grid-cols-7 text-center text-xs text-gray-500 dark:text-gray-400 mb-1 mx-4"
    >
      <div>일</div>
      <div>월</div>
      <div>화</div>
      <div>수</div>
      <div>목</div>
      <div>금</div>
      <div>토</div>
    </div>

    <!-- 달력 그리드 -->
    <div class="grid grid-cols-7 gap-1 mx-4">
      <div
        v-for="d in calendarDays"
        :key="d.key"
        :class="dayClass(d)"
        @click="selectDate(d)"
        class="aspect-square rounded-xl flex flex-col items-center justify-center text-sm cursor-pointer select-none"
      >
        <span>{{ d.date.getDate() }}</span>
        <span
          v-if="countJobs[d.key]"
          class="mt-1 text-[10px] px-1.5 py-0.5 rounded-full bg-blue-50 dark:bg-blue-900/50 text-blue-700 dark:text-blue-300"
          >{{ countJobs[d.key] }}건</span
        >
      </div>
    </div>

    <!-- 선택 날짜 일정 리스트 -->
    <div class="mt-4 mx-4">
      <div class="flex items-center justify-between mb-2">
        <p class="text-sm text-gray-600 dark:text-gray-400">
          {{ selectedDateLabel }}일정
        </p>
        <select
          v-model="statusFilter"
          class="text-sm border border-gray-300 dark:border-gray-600 rounded-lg px-2 py-1 bg-white dark:bg-gray-800 text-gray-900 dark:text-gray-100"
        >
          <option value="all">전체</option>
          <option value="scheduled">예약</option>
          <option value="onroute">이동중</option>
          <option value="working">작업중</option>
          <option value="done">완료</option>
        </select>
      </div>
    </div>

    <!-- 일정리스트   if 일정이 없으면-->
    <div
      v-if="filteredJobsSelected.length === 0"
      class="text-center text-gray-500 dark:text-gray-400 text-sm py-6 mx-4"
    >
      일정이 없습니다.
    </div>
    <ul class="space-y-2 mx-4">
      <li
        v-for="job in filteredJobsSelected"
        :key="job.id"
        class="rounded-xl border border-gray-200 dark:border-gray-700 p-3 bg-white dark:bg-gray-800"
      >
        <div class="flex items-start gap-3">
          <div
            class="w-9 h-9 rounded-lg flex items-center justify-center text-xs font-bold"
            :class="
              job.type === 'luggage'
                ? 'bg-purple-100 dark:bg-purple-900/50 text-purple-700 dark:text-purple-300'
                : 'bg-teal-100 dark:bg-teal-900/50 text-teal-700 dark:text-teal-300'
            "
          >
            {{ job.type === "luggage" ? "수" : "제" }}
          </div>
          <div class="flex-1 min-w-0">
            <p
              class="text-sm font-semibold truncate text-gray-900 dark:text-white"
            >
              {{ job.customerName }}
              <span class="text-gray-400 dark:text-gray-500" v-if="job.time">{{
                job.time
              }}</span>
            </p>
            <p class="text-xs text-gray-600 dark:text-gray-400 truncate">
              {{ job.address }}
            </p>
            <div
              class="mt-1 text-xs text-gray-500 dark:text-gray-500"
              v-if="job.original?.eventName"
            >
              {{ job.original.eventName }}
            </div>
            <div class="mt-2 flex items-center gap-1.5 flex-wrap">
              <span
                class="text-[10px] px-1.5 py-0.5 rounded-full"
                :class="
                  job.status === 'done'
                    ? 'bg-green-100 dark:bg-green-900/50 text-green-700 dark:text-green-300'
                    : job.status === 'onroute'
                      ? 'bg-yellow-100 dark:bg-yellow-900/50 text-yellow-700 dark:text-yellow-300'
                      : job.status === 'working'
                        ? 'bg-blue-100 dark:bg-blue-900/50 text-blue-700 dark:text-blue-300'
                        : 'bg-gray-100 dark:bg-gray-700 text-gray-700 dark:text-gray-300'
                "
                >{{ statusText(job.status) }}</span
              >
              <span
                class="text-[10px] px-1.5 py-0.5 rounded-full bg-gray-100 dark:bg-gray-700 text-gray-600 dark:text-gray-400"
                v-if="job.memo"
                >메모: {{ job.memo }}</span
              >
            </div>
          </div>
        </div>

        <div class="mt-3 grid grid-cols-3 gap-2 text-xs">
          <a
            :href="`tel:${job.phone}`"
            class="py-2 rounded-lg bg-blue-600 text-white text-center"
            >전화</a
          >
          <a
            :href="mapLink(job.address)"
            class="py-2 rounded-lg bg-gray-100 text-gray-700 text-center"
            >길찾기</a
          >
          <button
            @click="advance(job)"
            class="py-2 rounded-lg bg-yellow-500 text-white text-center"
          >
            상태변경
          </button>
        </div>
      </li>
    </ul>
  </div>
</template>

<script setup>
import { ref, computed } from "vue";
import reservationsData from "@/data/reservations_2025_12.json";

// 현재 년 / 월 기본값
const today = new Date();
const selectedDate = ref(new Date(today));
const viewDate = ref(new Date(today.getFullYear(), today.getMonth(), 1));
const statusFilter = ref("all");

// reservations 데이터를 jobs 형식으로 변환
const jobs = computed(() => {
  return reservationsData.reservations.map((r) => {
    // dropoffTime에서 시간 추출
    const dropoffDate = r.dropoffTime ? new Date(r.dropoffTime) : null;
    const timeStr = dropoffDate
      ? `${String(dropoffDate.getHours()).padStart(2, "0")}:${String(dropoffDate.getMinutes()).padStart(2, "0")}`
      : "";

    // 상태 변환 (예약중 -> scheduled, 완료 -> done)
    let status = "scheduled";
    if (r.status === "완료" || r.deliveryStatus === "완료") {
      status = "done";
    } else if (r.deliveryStatus === "배송중") {
      status = "onroute";
    } else if (r.status === "예약중") {
      status = "scheduled";
    }

    // 타입 결정 (itemType 기반)
    const type = r.itemType === "식품(상온)" ? "ice" : "luggage";

    return {
      id: r.id,
      date: r.eventDate || (r.dropoffTime ? r.dropoffTime.split("T")[0] : ""),
      type: type,
      customerName: r.customerName,
      time: timeStr,
      address: r.deliveryAddress || r.eventVenue || "",
      phone: r.customerPhone,
      status: status,
      memo: r.specialRequest || "",
      eventName: r.eventName, // 행사명 추가
      // 원본 데이터 보존
      original: r,
    };
  });
});

const year = computed(() => viewDate.value.getFullYear());
const month = computed(() => viewDate.value.getMonth());

// 날짜 key 포맷 함수
function fmtKey(d) {
  const y = d.getFullYear();
  const m = String(d.getMonth() + 1).padStart(2, "0");
  const day = String(d.getDate()).padStart(2, "0");
  return `${y}-${m}-${day}`;
}

const calendarDays = computed(() => {
  const start = new Date(year.value, month.value, 1);
  const end = new Date(year.value, month.value + 1, 0);
  const startWeekday = start.getDay();

  const days = [];
  // 이전 달 채우기
  for (let i = 0; i < startWeekday; i++) {
    const d = new Date(start);
    d.setDate(d.getDate() - (startWeekday - i));
    days.push({ date: d, key: fmtKey(d), outside: true });
  }
  // 이번 달
  for (let d = 1; d <= end.getDate(); d++) {
    const cur = new Date(year.value, month.value, d);
    days.push({ date: cur, key: fmtKey(cur), outside: false });
  }
  // 다음 달 채우기 (42칸)
  while (days.length < 42) {
    const last = days[days.length - 1].date;
    const next = new Date(last);
    next.setDate(next.getDate() + 1);
    days.push({ date: next, key: fmtKey(next), outside: true });
  }
  return days;
});

function dayClass(d) {
  const isToday = fmtKey(d.date) === fmtKey(today);
  const isSelected = fmtKey(d.date) === fmtKey(selectedDate.value);
  return [
    d.outside
      ? "text-gray-400 dark:text-gray-600"
      : "text-gray-900 dark:text-gray-100",
    isToday ? "ring-1 ring-blue-500 dark:ring-blue-400" : "",
    isSelected
      ? "bg-blue-600 dark:bg-blue-500 text-white"
      : "bg-white dark:bg-gray-800",
  ];
}

// 이전 클릭
function prevMonth() {
  viewDate.value = new Date(year.value, month.value - 1, 1);
}

function nextMonth() {
  viewDate.value = new Date(year.value, month.value + 1, 1);
}

const countJobs = computed(() => {
  const acc = {};
  for (const j of jobs.value) {
    if (j.date) {
      acc[j.date] = (acc[j.date] || 0) + 1;
    }
  }
  return acc;
});

// 선택한 날짜
function selectDate(d) {
  selectedDate.value = new Date(d.date);
}

// 선택날짜
const selectedDateLabel = computed(() => {
  const d = selectedDate.value;
  return `${d.getMonth() + 1}월${d.getDate()}일`;
});

// 작업 상태
const jobsSelected = computed(() => {
  const key = fmtKey(selectedDate.value);
  return jobs.value.filter((j) => {
    return j.date === key;
  });
});

// 작업상태 필터링
const filteredJobsSelected = computed(() => {
  if (statusFilter.value === "all") return jobsSelected.value;

  return jobsSelected.value.filter((j) => j.status === statusFilter.value);
});

// 작업상태 글자 변경
function statusText(status) {
  switch (status) {
    case "scheduled":
      return "예약";
    case "onroute":
      return "이동중";
    case "working":
      return "작업중";
    case "done":
      return "완료";
    default:
      return status;
  }
}

//길찾기
function mapLink(address) {
  const q = encodeURIComponent(address);
  return `https://map.kakao.com/?q=${q}`;
}

function advance(job) {
  const order = ["scheduled", "onroute", "working", "done"];
  const idx = order.indexOf(job.status);
  if (idx < order.length - 1) {
    const nextStatus = order[idx + 1];
    job.status = nextStatus;

    // 원본 데이터도 업데이트
    if (job.original) {
      if (nextStatus === "done") {
        job.original.status = "완료";
        job.original.deliveryStatus = "완료";
      } else if (nextStatus === "onroute") {
        job.original.deliveryStatus = "배송중";
      } else if (nextStatus === "working") {
        job.original.status = "작업중";
      }
    }
  }
}
</script>
