<template>
  <div class="pb-20">
    <!-- 컨텐츠 영역 -->
    <div class="px-4 py-4">
      <!-- 프로필 정보 카드 -->
      <div class="bg-white rounded-2xl shadow-sm p-5">
        <div class="flex items-center gap-4">
          <!-- 프로필 이미지 -->
          <div
            class="w-20 h-20 rounded-full bg-gray-200 flex items-center justify-center overflow-hidden flex-shrink-0"
          >
            <img
              v-if="userInfo.profileImage"
              :src="userInfo.profileImage"
              alt="프로필"
              class="w-full h-full object-cover"
            />
            <span v-else class="text-3xl text-gray-400">👤</span>
          </div>

          <!-- 프로필 정보 -->
          <div class="flex-1">
            <div class="text-lg font-bold text-gray-900 mb-1">
              {{ userInfo.displayName }}
            </div>
            <div class="text-sm text-gray-600 mb-1">{{ userInfo.phone }}</div>
            <div class="text-sm text-gray-600">{{ userInfo.email }}</div>
          </div>
        </div>

        <!-- 내정보 수정 링크 -->
        <div class="mt-4 text-right">
          <button
            @click="goToEditProfile"
            class="text-blue-600 text-sm font-bold"
          >
            내정보 수정 >
          </button>
        </div>
      </div>

      <!-- 일정 정보 카드 -->
      <div class="bg-white rounded-2xl shadow-sm mt-4 p-5">
        <div class="text-lg font-bold text-gray-900 mb-3">
          전체 운영 일정
        </div>

        <div class="space-y-3">
          <div class="flex justify-between items-center">
            <span class="text-sm text-gray-600">오늘 행사</span>
            <span class="text-base font-bold text-gray-900"
              >{{ todayScheduleCount }}건</span
            >
          </div>
          <div class="flex justify-between items-center">
            <span class="text-sm text-gray-600">이번 주 행사</span>
            <span class="text-base font-bold text-gray-900"
              >{{ weekScheduleCount }}건</span
            >
          </div>
          <div class="flex justify-between items-center">
            <span class="text-sm text-gray-600">이번 달 행사</span>
            <span class="text-base font-bold text-gray-900"
              >{{ monthScheduleCount }}건</span
            >
          </div>
          <div class="flex justify-end mt-2">
            <button
              @click="goToCalendar"
              class="text-blue-600 text-sm font-bold"
            >
              자세히 보기 >
            </button>
          </div>
        </div>
      </div>

      <!-- 기사 급여 카드 -->
      <div class="bg-white rounded-2xl shadow-sm mt-4 p-5">
        <div class="text-lg font-bold text-gray-900 mb-3">
          내 급여 현황
        </div>

        <div class="space-y-3">
          <div class="flex justify-between items-center">
            <span class="text-sm text-gray-600">오늘</span>
            <span class="text-base font-bold text-gray-900"
              >-원</span
            >
          </div>
          <div class="flex justify-between items-center">
            <span class="text-sm text-gray-600">이번 주</span>
            <span class="text-base font-bold text-gray-900"
              >-원</span
            >
          </div>
          <div class="flex justify-between items-center">
            <span class="text-sm text-gray-600">이번 달</span>
            <span class="text-base font-bold text-gray-900"
              >-원</span
            >
          </div>
          <div class="flex justify-end mt-2">
            <button
              @click="goToSalaryDetail"
              class="text-blue-600 text-sm font-bold"
            >
              자세히 보기 >
            </button>
          </div>
        </div>
      </div>

      <!-- 로그아웃 버튼 -->
      <div class="mt-4 mb-4 flex justify-end">
        <button
          @click="handleLogout"
          class="bg-white dark:bg-gray-800 text-gray-900 dark:text-gray-100 px-4 py-2 rounded-lg text-sm font-bold shadow-sm hover:shadow-md transition-all flex items-center gap-2 border border-gray-200 dark:border-gray-700"
        >
          <i class="fi fi-rr-sign-out-alt"></i>
          <span>로그아웃</span>
        </button>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed } from "vue";
import { useAuthStore } from "@/stores/auth";
import { useRouter } from "vue-router";
import reservationsData from "@/data/reservations_2025_12.json";

const authStore = useAuthStore();
const router = useRouter();

const goToHome = () => {
  router.push({ name: "WorkerWork" });
};

const goToCalendar = () => {
  router.push({ name: "WorkerCalendar" });
};

const goToEditProfile = () => {
  router.push({ name: "WorkerEditProfile" });
};

const goToSalaryDetail = () => {
  router.push({ name: "WorkerSalaryDetail" });
};

const handleLogout = () => {
  const isConfirmed = window.confirm("정말 로그아웃하시겠습니까?");
  if (isConfirmed) {
    authStore.logout();
    router.push("/login");
  }
};

const userInfo = ref({
  name: authStore.user?.name || "김운전",
  displayName: "김기사",
  phone: "010-1234-5678",
  email: "driver@example.com",
  profileImage: null,
});

// 일정 통계 계산 (Calendar.vue와 동일한 방식)
const today = new Date();
today.setHours(0, 0, 0, 0);

// 날짜 key 포맷 함수 (Calendar.vue와 동일)
function fmtKey(d) {
  const y = d.getFullYear();
  const m = String(d.getMonth() + 1).padStart(2, "0");
  const day = String(d.getDate()).padStart(2, "0");
  return `${y}-${m}-${day}`;
}

// 예약 데이터를 jobs 형식으로 변환 (Calendar.vue와 동일)
const jobs = computed(() => {
  return reservationsData.reservations.map((r) => {
    // dropoffTime에서 시간 추출
    const dropoffDate = r.dropoffTime ? new Date(r.dropoffTime) : null;
    const timeStr = dropoffDate
      ? `${String(dropoffDate.getHours()).padStart(2, "0")}:${String(dropoffDate.getMinutes()).padStart(2, "0")}`
      : "";

    return {
      id: r.id,
      date: r.eventDate || (r.dropoffTime ? r.dropoffTime.split("T")[0] : ""),
      type: r.itemType === "식품(상온)" ? "ice" : "luggage",
      customerName: r.customerName,
      time: timeStr,
      address: r.deliveryAddress || r.eventVenue || "",
      phone: r.customerPhone,
      status: r.status === "완료" || r.deliveryStatus === "완료" ? "done" : r.deliveryStatus === "배송중" ? "onroute" : "scheduled",
      memo: r.specialRequest || "",
      original: r,
    };
  });
});

// 날짜별 행사 정보 계산 (Calendar.vue와 동일한 방식)
const eventsByDate = computed(() => {
  const eventsMap = {};
  
  // 예약 데이터를 날짜별로 그룹화하고 행사별로 집계
  jobs.value.forEach((job) => {
    if (!job.date) return;
    
    const eventName = job.original?.eventName || "행사";
    const eventVenue = job.original?.eventVenue || "-";
    const key = `${job.date}|${eventName}|${eventVenue}`;
    
    if (!eventsMap[key]) {
      eventsMap[key] = {
        date: job.date,
        eventName,
        eventVenue,
        key,
      };
    }
  });
  
  return eventsMap;
});

// 오늘 일정 수 (행사 건수)
const todayScheduleCount = computed(() => {
  const todayKey = fmtKey(today);
  let count = 0;
  for (const key in eventsByDate.value) {
    if (eventsByDate.value[key].date === todayKey) {
      count++;
    }
  }
  return count;
});

// 이번 주 일정 수 (행사 건수)
const weekScheduleCount = computed(() => {
  const weekStart = new Date(today);
  weekStart.setDate(today.getDate() - today.getDay()); // 이번 주 일요일
  const weekEnd = new Date(weekStart);
  weekEnd.setDate(weekStart.getDate() + 6); // 이번 주 토요일
  weekEnd.setHours(23, 59, 59, 999);

  let count = 0;
  for (const key in eventsByDate.value) {
    const event = eventsByDate.value[key];
    if (!event.date) continue;
    const eventDate = new Date(event.date);
    eventDate.setHours(0, 0, 0, 0);
    if (eventDate >= weekStart && eventDate <= weekEnd) {
      count++;
    }
  }
  return count;
});

// 이번 달 일정 수 (행사 건수)
const monthScheduleCount = computed(() => {
  const monthStart = new Date(today.getFullYear(), today.getMonth(), 1);
  const monthEnd = new Date(today.getFullYear(), today.getMonth() + 1, 0);
  monthEnd.setHours(23, 59, 59, 999);

  let count = 0;
  for (const key in eventsByDate.value) {
    const event = eventsByDate.value[key];
    if (!event.date) continue;
    const eventDate = new Date(event.date);
    eventDate.setHours(0, 0, 0, 0);
    if (eventDate >= monthStart && eventDate <= monthEnd) {
      count++;
    }
  }
  return count;
});
</script>

