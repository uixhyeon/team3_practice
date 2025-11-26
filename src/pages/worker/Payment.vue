<template>
  <div class="pb-20">
    <!-- 헤더 -->
    <div
      class="bg-white border-b border-gray-200 dark:bg-gray-800 dark:border-gray-700"
    >
      <div class="flex items-center justify-between p-4">
        <div class="flex items-center gap-2">
          <i class="fi fi-rr-money-bill-wave text-blue-600 text-xl"></i>
          <h1 class="text-lg font-semibold text-gray-900 dark:text-white">
            정산
          </h1>
        </div>
        <button class="text-gray-600 dark:text-gray-300">
          <i class="fi fi-rr-menu-dots-vertical text-xl"></i>
        </button>
      </div>
      <div class="px-4 pb-3 text-sm text-gray-600 dark:text-gray-400">
        오늘 {{ formatDate(new Date()) }}
      </div>
    </div>

    <!-- 핵심 통계 카드 (3개) -->
    <div class="grid grid-cols-3 gap-3 mx-4 mt-4">
      <!-- 오늘 수익 -->
      <div
        class="bg-gradient-to-br from-blue-500 to-blue-600 rounded-2xl p-4 text-white"
      >
        <div class="text-xs opacity-90 mb-1">오늘 수익</div>
        <div class="text-xl font-bold">
          {{ formatCurrency(todaySummary.earnings) }}
        </div>
        <div class="text-xs opacity-75 mt-1">
          {{ todaySummary.workHours }}시간
        </div>
      </div>

      <!-- 이번 주 수익 -->
      <div
        class="bg-gradient-to-br from-green-500 to-green-600 rounded-2xl p-4 text-white"
      >
        <div class="text-xs opacity-90 mb-1">이번 주</div>
        <div class="text-xl font-bold">
          {{ formatCurrency(weekTotal) }}
        </div>
        <div class="text-xs opacity-75 mt-1">{{ weekTotalHours }}시간</div>
      </div>

      <!-- 이번 달 수익 -->
      <div
        class="bg-gradient-to-br from-purple-500 to-purple-600 rounded-2xl p-4 text-white"
      >
        <div class="text-xs opacity-90 mb-1">이번 달</div>
        <div class="text-xl font-bold">
          {{ formatCurrency(monthTotal) }}
        </div>
        <div class="text-xs opacity-75 mt-1">{{ monthTotalHours }}시간</div>
      </div>
    </div>

    <!-- 시급 정보 카드 -->
    <div class="bg-white rounded-2xl shadow-sm mx-4 mt-4 p-5">
      <div class="flex items-center justify-between mb-3">
        <div class="flex items-center gap-2">
          <i class="fi fi-rr-clock text-blue-600 text-sm"></i>
          <h2 class="text-base font-semibold text-gray-900">시급 정보</h2>
        </div>
        <span class="text-lg font-bold text-blue-600"
          >{{ formatCurrency(hourlyRate) }}원/시간</span
        >
      </div>
      <div class="bg-blue-50 rounded-lg p-3 text-sm text-gray-700">
        <div class="flex items-center gap-2">
          <i class="fi fi-rr-info text-blue-600"></i>
          <span>공연 시작 3시간 전부터 공연 종료 3시간 후까지 근무</span>
        </div>
      </div>
    </div>

    <!-- 근무 상세 내역 카드 -->
    <div class="bg-white rounded-2xl shadow-sm mx-4 mt-4 p-5">
      <div class="flex items-center gap-2 mb-4">
        <i class="fi fi-rr-clock text-blue-600 text-sm"></i>
        <h2 class="text-base font-semibold text-gray-900">근무 상세</h2>
      </div>
      <div class="space-y-3">
        <div
          v-for="detail in workDetails"
          :key="detail.date"
          class="flex items-center justify-between"
        >
          <div class="flex-1">
            <div class="text-sm font-semibold text-gray-900">
              {{ detail.eventName }}
            </div>
            <div class="text-xs text-gray-600 mt-1">
              {{ detail.workStart }} ~ {{ detail.workEnd }}
              <span class="text-gray-400">({{ detail.hours }}시간)</span>
            </div>
          </div>
          <div class="text-sm font-semibold text-blue-600">
            {{ formatCurrency(detail.earnings) }}원
          </div>
        </div>
        <div
          v-if="workDetails.length === 0"
          class="text-center text-gray-500 text-sm py-4"
        >
          오늘 근무 일정이 없습니다
        </div>
      </div>
    </div>

    <!-- 입금 예정 -->
    <div class="bg-white rounded-2xl shadow-sm mx-4 mt-4 p-5">
      <div class="flex items-center gap-2 mb-4">
        <i class="fi fi-rr-credit-card text-blue-600 text-sm"></i>
        <h2 class="text-base font-semibold text-gray-900">입금 예정</h2>
      </div>
      <div class="space-y-2">
        <div class="flex justify-between">
          <span class="text-sm text-gray-600">일자</span>
          <span class="text-sm font-semibold text-gray-900">{{
            scheduledDeposit.date
          }}</span>
        </div>
        <div class="flex justify-between">
          <span class="text-sm text-gray-600">계좌</span>
          <span class="text-sm font-semibold text-gray-900">{{
            scheduledDeposit.account
          }}</span>
        </div>
        <div class="flex justify-between">
          <span class="text-sm text-gray-600">금액</span>
          <span class="text-base font-bold text-blue-600">{{
            formatCurrency(scheduledDeposit.amount)
          }}</span>
        </div>
      </div>
    </div>

    <!-- 주간 수익 차트 -->
    <div class="bg-white rounded-2xl shadow-sm mx-4 mt-4 p-5">
      <div class="flex items-center gap-2 mb-4">
        <i class="fi fi-rr-chart-line-up text-blue-600 text-sm"></i>
        <h2 class="text-base font-semibold text-gray-900">이번 주 수익 추이</h2>
      </div>
      <div class="h-48">
        <canvas ref="weekChartRef"></canvas>
      </div>
      <div class="mt-4 space-y-2">
        <div
          v-for="day in weekSummary"
          :key="day.day"
          class="flex items-center justify-between text-sm"
        >
          <div class="flex items-center gap-3">
            <span class="text-gray-600 w-16">{{ day.day }}</span>
            <div class="flex-1 bg-gray-100 rounded-full h-2">
              <div
                class="bg-blue-600 h-2 rounded-full"
                :style="{ width: `${(day.earnings / weekMaxEarnings) * 100}%` }"
              ></div>
            </div>
          </div>
          <div class="text-right w-24">
            <div class="font-semibold text-gray-900">
              {{ formatCurrency(day.earnings) }}원
            </div>
            <div class="text-xs text-gray-500">{{ day.hours }}시간</div>
          </div>
        </div>
      </div>
    </div>

    <!-- 이번 달 통계 -->
    <div class="bg-white rounded-2xl shadow-sm mx-4 mt-4 p-5 mb-4">
      <div class="flex items-center gap-2 mb-4">
        <i class="fi fi-rr-calendar text-blue-600 text-sm"></i>
        <h2 class="text-base font-semibold text-gray-900">이번 달 통계</h2>
      </div>

      <!-- 통계 요약 -->
      <div class="grid grid-cols-2 gap-3 mb-4">
        <div class="bg-gray-50 rounded-lg p-3">
          <div class="text-xs text-gray-600 mb-1">평균 일 근무</div>
          <div class="text-lg font-bold text-gray-900">
            {{ averageDailyHours }}시간
          </div>
        </div>
        <div class="bg-gray-50 rounded-lg p-3">
          <div class="text-xs text-gray-600 mb-1">평균 일 수익</div>
          <div class="text-lg font-bold text-gray-900">
            {{ formatCurrency(averageDailyEarnings) }}원
          </div>
        </div>
      </div>

      <!-- 주차별 상세 -->
      <div class="space-y-3">
        <div
          v-for="week in monthSummary"
          :key="week.week"
          class="flex items-center justify-between p-3 bg-gray-50 rounded-lg"
        >
          <div>
            <div class="text-sm font-semibold text-gray-900">
              {{ week.week }}
            </div>
            <div class="text-xs text-gray-500 mt-1">
              {{ week.hours }}시간 근무
            </div>
          </div>
          <div class="text-right">
            <div class="text-sm font-bold text-blue-600">
              {{ formatCurrency(week.earnings) }}원
            </div>
          </div>
        </div>
        <div class="border-t border-gray-200 pt-3 mt-3">
          <div class="flex justify-between items-center mb-2">
            <span class="text-sm text-gray-600">총 근무 시간</span>
            <span class="text-sm font-semibold text-gray-900"
              >{{ monthTotalHours }}시간</span
            >
          </div>
          <div class="flex justify-between">
            <span class="text-sm font-semibold text-gray-900"
              >이번 달 합계</span
            >
            <span class="text-base font-bold text-blue-600"
              >{{ formatCurrency(monthTotal) }}원</span
            >
          </div>
        </div>
      </div>
    </div>

    <!-- 상세 내역 보기 링크 -->
    <div class="text-center mb-6">
      <button
        class="flex items-center justify-center gap-2 text-blue-600 text-sm font-medium"
      >
        <i class="fi fi-rr-document text-sm"></i>
        <span>[ 상세 내역 보기]</span>
      </button>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, onMounted, onUnmounted, nextTick, watch } from "vue";
import { Chart } from "chart.js/auto";
import reservationsData from "@/data/reservations_2025_12.json";

// 트럭 운전 기사 시급 (후하게)
const hourlyRate = 25000;

const formatDate = (date) => {
  const month = date.getMonth() + 1;
  const day = date.getDate();
  return `${month}월 ${day}일`;
};

const formatCurrency = (amount) => {
  return amount.toLocaleString("ko-KR");
};

const formatTime = (date) => {
  if (!date) return "";
  return `${String(date.getHours()).padStart(2, "0")}:${String(date.getMinutes()).padStart(2, "0")}`;
};

// 공연 시간 기준으로 근무 시간 계산 (공연 시작 3시간 전 ~ 공연 종료 3시간 후)
const calculateWorkHours = (eventStartTime, eventEndTime) => {
  if (!eventStartTime || !eventEndTime) return 0;

  const start = new Date(eventStartTime);
  const end = new Date(eventEndTime);

  // 공연 시작 3시간 전
  const workStart = new Date(start);
  workStart.setHours(workStart.getHours() - 3);

  // 공연 종료 3시간 후
  const workEnd = new Date(end);
  workEnd.setHours(workEnd.getHours() + 3);

  // 근무 시간 계산 (시간 단위)
  const diff = workEnd.getTime() - workStart.getTime();
  const hours = diff / (1000 * 60 * 60);

  return Math.round(hours * 10) / 10; // 소수점 첫째 자리까지
};

// 오늘 날짜
const today = new Date();
today.setHours(0, 0, 0, 0);
const todayStr = `${today.getFullYear()}-${String(today.getMonth() + 1).padStart(2, "0")}-${String(today.getDate()).padStart(2, "0")}`;

// 오늘 근무 일정
const todayWorkDetails = computed(() => {
  const todayReservations = reservationsData.reservations.filter((r) => {
    return r.eventDate === todayStr;
  });

  // 같은 날짜의 행사는 하나만 (하루에 하나의 행사장소)
  const uniqueEvents = {};
  todayReservations.forEach((r) => {
    const key = `${r.eventDate}-${r.eventVenue}`;
    if (!uniqueEvents[key]) {
      uniqueEvents[key] = r;
    }
  });

  return Object.values(uniqueEvents).map((r) => {
    const workHours = calculateWorkHours(r.eventStartTime, r.eventEndTime);
    const start = new Date(r.eventStartTime);
    start.setHours(start.getHours() - 3);
    const end = new Date(r.eventEndTime);
    end.setHours(end.getHours() + 3);

    return {
      date: r.eventDate,
      eventName: r.eventName,
      workStart: formatTime(start),
      workEnd: formatTime(end),
      hours: workHours,
      earnings: Math.round(workHours * hourlyRate),
    };
  });
});

// 오늘 요약
const todaySummary = computed(() => {
  const totalHours = todayWorkDetails.value.reduce(
    (sum, d) => sum + d.hours,
    0
  );
  const totalEarnings = todayWorkDetails.value.reduce(
    (sum, d) => sum + d.earnings,
    0
  );

  return {
    workHours: totalHours.toFixed(1),
    earnings: totalEarnings,
  };
});

// 근무 상세 내역
const workDetails = computed(() => {
  return todayWorkDetails.value;
});

// 입금 예정
const scheduledDeposit = computed(() => {
  const tomorrow = new Date(today);
  tomorrow.setDate(tomorrow.getDate() + 1);
  const month = tomorrow.getMonth() + 1;
  const day = tomorrow.getDate();
  const weekday = ["일", "월", "화", "수", "목", "금", "토"][tomorrow.getDay()];

  return {
    date: `${month}/${day}(${weekday})`,
    account: "국민 101-02***-***",
    amount: todaySummary.value.earnings,
  };
});

// 이번 주 요약
const weekSummary = computed(() => {
  const weekStart = new Date(today);
  weekStart.setDate(today.getDate() - today.getDay()); // 일요일
  const weekEnd = new Date(weekStart);
  weekEnd.setDate(weekStart.getDate() + 6); // 토요일

  const weekDays = [];
  for (let d = new Date(weekStart); d <= weekEnd; d.setDate(d.getDate() + 1)) {
    const dateStr = `${d.getFullYear()}-${String(d.getMonth() + 1).padStart(2, "0")}-${String(d.getDate()).padStart(2, "0")}`;
    const dayReservations = reservationsData.reservations.filter(
      (r) => r.eventDate === dateStr
    );

    // 같은 날짜의 행사는 하나만
    const uniqueEvents = {};
    dayReservations.forEach((r) => {
      const key = `${r.eventDate}-${r.eventVenue}`;
      if (!uniqueEvents[key]) {
        uniqueEvents[key] = r;
      }
    });

    const events = Object.values(uniqueEvents);
    let totalHours = 0;
    events.forEach((r) => {
      totalHours += calculateWorkHours(r.eventStartTime, r.eventEndTime);
    });

    const weekdayNames = [
      "일요일",
      "월요일",
      "화요일",
      "수요일",
      "목요일",
      "금요일",
      "토요일",
    ];
    weekDays.push({
      day: weekdayNames[d.getDay()],
      hours: Math.round(totalHours * 10) / 10,
      earnings: Math.round(totalHours * hourlyRate),
    });
  }

  return weekDays;
});

const weekTotal = computed(() => {
  return weekSummary.value.reduce((sum, day) => sum + day.earnings, 0);
});

const weekTotalHours = computed(() => {
  return weekSummary.value.reduce((sum, day) => sum + day.hours, 0).toFixed(1);
});

// 이번 달 요약
const monthSummary = computed(() => {
  const monthStart = new Date(today.getFullYear(), today.getMonth(), 1);
  const monthEnd = new Date(today.getFullYear(), today.getMonth() + 1, 0);

  const weeks = [];
  let currentWeekStart = new Date(monthStart);

  while (currentWeekStart <= monthEnd) {
    const weekEnd = new Date(currentWeekStart);
    weekEnd.setDate(currentWeekStart.getDate() + 6);
    if (weekEnd > monthEnd) weekEnd = new Date(monthEnd);

    let weekHours = 0;
    for (
      let d = new Date(currentWeekStart);
      d <= weekEnd;
      d.setDate(d.getDate() + 1)
    ) {
      const dateStr = `${d.getFullYear()}-${String(d.getMonth() + 1).padStart(2, "0")}-${String(d.getDate()).padStart(2, "0")}`;
      const dayReservations = reservationsData.reservations.filter(
        (r) => r.eventDate === dateStr
      );

      const uniqueEvents = {};
      dayReservations.forEach((r) => {
        const key = `${r.eventDate}-${r.eventVenue}`;
        if (!uniqueEvents[key]) {
          uniqueEvents[key] = r;
        }
      });

      Object.values(uniqueEvents).forEach((r) => {
        weekHours += calculateWorkHours(r.eventStartTime, r.eventEndTime);
      });
    }

    const weekNum = Math.floor((currentWeekStart.getDate() - 1) / 7) + 1;
    weeks.push({
      week: `${weekNum}주차`,
      hours: Math.round(weekHours * 10) / 10,
      earnings: Math.round(weekHours * hourlyRate),
    });

    currentWeekStart.setDate(currentWeekStart.getDate() + 7);
  }

  return weeks;
});

const monthTotal = computed(() => {
  return monthSummary.value.reduce((sum, week) => sum + week.earnings, 0);
});

const monthTotalHours = computed(() => {
  return monthSummary.value
    .reduce((sum, week) => sum + week.hours, 0)
    .toFixed(1);
});

// 평균 일 근무 시간
const averageDailyHours = computed(() => {
  const workDays = weekSummary.value.filter((day) => day.hours > 0).length;
  if (workDays === 0) return "0.0";
  return (parseFloat(weekTotalHours.value) / workDays).toFixed(1);
});

// 평균 일 수익
const averageDailyEarnings = computed(() => {
  const workDays = weekSummary.value.filter((day) => day.earnings > 0).length;
  if (workDays === 0) return 0;
  return Math.round(weekTotal.value / workDays);
});

// 주간 최대 수익 (차트용)
const weekMaxEarnings = computed(() => {
  if (weekSummary.value.length === 0) return 1;
  return Math.max(...weekSummary.value.map((d) => d.earnings), 1);
});

// 주간 차트
const weekChartRef = ref(null);
let weekChart = null;

onMounted(() => {
  nextTick(() => {
    createWeekChart();
  });
});

onUnmounted(() => {
  if (weekChart) {
    weekChart.destroy();
  }
});

const createWeekChart = () => {
  if (!weekChartRef.value) return;

  const ctx = weekChartRef.value.getContext("2d");

  if (weekChart) {
    weekChart.destroy();
  }

  weekChart = new Chart(ctx, {
    type: "bar",
    data: {
      labels: weekSummary.value.map((d) => d.day.replace("요일", "")),
      datasets: [
        {
          label: "수익",
          data: weekSummary.value.map((d) => d.earnings),
          backgroundColor: "rgba(59, 130, 246, 0.6)",
          borderColor: "rgba(59, 130, 246, 1)",
          borderWidth: 2,
          borderRadius: 8,
        },
      ],
    },
    options: {
      responsive: true,
      maintainAspectRatio: false,
      plugins: {
        legend: {
          display: false,
        },
        tooltip: {
          callbacks: {
            label: function (context) {
              const day = weekSummary.value[context.dataIndex];
              return [
                `수익: ${formatCurrency(context.parsed.y)}원`,
                `근무: ${day.hours}시간`,
              ];
            },
          },
        },
      },
      scales: {
        y: {
          beginAtZero: true,
          ticks: {
            callback: function (value) {
              if (value >= 10000) {
                return value / 10000 + "만원";
              }
              return value + "원";
            },
          },
          grid: {
            color: "rgba(226, 232, 240, 1)",
          },
        },
        x: {
          grid: {
            display: false,
          },
        },
      },
    },
  });
};

// 주간 데이터 변경 시 차트 업데이트
watch(
  weekSummary,
  () => {
    nextTick(() => {
      if (weekChart && weekChartRef.value) {
        weekChart.data.labels = weekSummary.value.map((d) =>
          d.day.replace("요일", "")
        );
        weekChart.data.datasets[0].data = weekSummary.value.map(
          (d) => d.earnings
        );
        weekChart.update();
      }
    });
  },
  { deep: true }
);
</script>
