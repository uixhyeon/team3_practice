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
            <div class="text-lg font-semibold text-gray-900 mb-1">
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
            class="text-blue-600 text-sm font-medium hover:underline"
          >
            내정보 수정 >
          </button>
        </div>
      </div>

      <!-- 일정 정보 카드 -->
      <div class="bg-white rounded-2xl shadow-sm mt-4 p-5">
        <div class="flex items-center justify-between mb-3">
          <div class="text-lg font-semibold text-gray-900">일정 정보</div>
          <button
            @click="goToCalendar"
            class="text-blue-600 text-sm font-medium hover:underline"
          >
            전체 보기 >
          </button>
        </div>

        <div class="space-y-3">
          <div class="flex justify-between items-center">
            <span class="text-sm text-gray-600">오늘 일정</span>
            <span class="text-base font-semibold text-gray-900"
              >{{ todayScheduleCount }}건</span
            >
          </div>
          <div class="flex justify-between items-center">
            <span class="text-sm text-gray-600">이번 주 일정</span>
            <span class="text-base font-semibold text-gray-900"
              >{{ weekScheduleCount }}건</span
            >
          </div>
          <div class="flex justify-between items-center">
            <span class="text-sm text-gray-600">이번 달 일정</span>
            <span class="text-base font-semibold text-gray-900"
              >{{ monthScheduleCount }}건</span
            >
          </div>
        </div>
      </div>

      <!-- 이번달 운영 현황 카드 -->
      <div class="bg-white rounded-2xl shadow-sm mt-4 p-5">
        <div class="text-lg font-semibold text-gray-900 mb-4">
          이번달 운영 현황
        </div>

        <div class="space-y-3">
          <div class="flex justify-between items-center">
            <span class="text-sm text-gray-600">총 운행 일수</span>
            <span class="text-base font-semibold text-gray-900"
              >{{ monthlyStats.totalDays }}일</span
            >
          </div>
          <div class="flex justify-between items-center">
            <span class="text-sm text-gray-600">총 운영 시간</span>
            <span class="text-base font-semibold text-gray-900"
              >{{ monthlyStats.totalHours }}시간</span
            >
          </div>
          <div class="flex justify-between items-center">
            <span class="text-sm text-gray-600">예상 급여</span>
            <span class="text-base font-semibold text-gray-900"
              >{{ formatCurrency(monthlyStats.estimatedSalary) }}원</span
            >
          </div>
        </div>

        <!-- 정산 상세 링크 -->
        <div class="mt-4">
          <button
            @click="goToPayment"
            class="w-full text-blue-600 text-sm font-medium hover:bg-blue-50 dark:hover:bg-blue-900/20 py-2 px-3 rounded-lg transition-colors text-center cursor-pointer"
          >
            정산 상세 보기 >
          </button>
        </div>
      </div>

      <!-- 로그아웃 버튼 -->
      <div class="mt-4 mb-4">
        <button
          @click="handleLogout"
          class="w-full bg-red-500 text-white py-3 rounded-xl font-semibold hover:bg-red-600 transition-colors"
        >
          로그아웃
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

const goToPayment = () => {
  router.push("/worker/workerMain/payment");
};

const goToEditProfile = () => {
  router.push({ name: "WorkerEditProfile" });
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

// 일정 통계 계산
const today = new Date();
today.setHours(0, 0, 0, 0);
const todayKey = `${today.getFullYear()}-${String(today.getMonth() + 1).padStart(2, "0")}-${String(today.getDate()).padStart(2, "0")}`;

// 예약 데이터를 날짜 기준으로 변환
const reservations = computed(() => {
  return reservationsData.reservations.map((r) => {
    const eventDate =
      r.eventDate || (r.dropoffTime ? r.dropoffTime.split("T")[0] : null);
    return {
      ...r,
      date: eventDate,
    };
  });
});

// 오늘 일정 수
const todayScheduleCount = computed(() => {
  return reservations.value.filter((r) => r.date === todayKey).length;
});

// 이번 주 일정 수
const weekScheduleCount = computed(() => {
  const weekStart = new Date(today);
  weekStart.setDate(today.getDate() - today.getDay()); // 이번 주 일요일
  const weekEnd = new Date(weekStart);
  weekEnd.setDate(weekStart.getDate() + 6); // 이번 주 토요일
  weekEnd.setHours(23, 59, 59, 999);

  return reservations.value.filter((r) => {
    if (!r.date) return false;
    const jobDate = new Date(r.date);
    jobDate.setHours(0, 0, 0, 0);
    return jobDate >= weekStart && jobDate <= weekEnd;
  }).length;
});

// 이번 달 일정 수
const monthScheduleCount = computed(() => {
  const monthStart = new Date(today.getFullYear(), today.getMonth(), 1);
  const monthEnd = new Date(today.getFullYear(), today.getMonth() + 1, 0);
  monthEnd.setHours(23, 59, 59, 999);

  return reservations.value.filter((r) => {
    if (!r.date) return false;
    const jobDate = new Date(r.date);
    jobDate.setHours(0, 0, 0, 0);
    return jobDate >= monthStart && jobDate <= monthEnd;
  }).length;
});

// 이번달 운영 현황 계산
const monthlyStats = computed(() => {
  const monthStart = new Date(today.getFullYear(), today.getMonth(), 1);
  const monthEnd = new Date(today.getFullYear(), today.getMonth() + 1, 0);
  monthEnd.setHours(23, 59, 59, 999);

  // 이번 달 예약들
  const monthReservations = reservations.value.filter((r) => {
    if (!r.date) return false;
    const jobDate = new Date(r.date);
    jobDate.setHours(0, 0, 0, 0);
    return jobDate >= monthStart && jobDate <= monthEnd;
  });

  // 운행 일수 계산 (고유한 날짜 수)
  const uniqueDates = new Set();
  monthReservations.forEach((r) => {
    if (r.date) {
      uniqueDates.add(r.date);
    }
  });
  const totalDays = uniqueDates.size;

  // 총 운영 시간 계산 (행사 시간 합계)
  let totalMinutes = 0;
  monthReservations.forEach((r) => {
    if (r.eventStartTime && r.eventEndTime) {
      const start = new Date(r.eventStartTime);
      const end = new Date(r.eventEndTime);
      const diff = end.getTime() - start.getTime();
      const minutes = Math.floor(diff / (1000 * 60));
      totalMinutes += minutes;
    }
  });
  const totalHours = Math.round(totalMinutes / 60);

  // 예상 급여 계산 (예약당 평균 20,000원 가정, 또는 실제 totalPrice 합계)
  const estimatedSalary = monthReservations.reduce((sum, r) => {
    // 운전사 급여는 예약 금액의 일정 비율로 계산 (예: 30%)
    const driverFee = r.totalPrice ? Math.round(r.totalPrice * 0.3) : 20000;
    return sum + driverFee;
  }, 0);

  return {
    totalDays,
    totalHours,
    estimatedSalary,
  };
});

const formatCurrency = (amount) => {
  return amount.toLocaleString("ko-KR");
};
</script>
