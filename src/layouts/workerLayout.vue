<template>
  <div
    class="h-screen w-full max-w-[480px] fixed top-0 left-1/2 -translate-x-1/2 overflow-hidden bg-white dark:bg-black"
  >
    <!-- 헤더 -->
    <header
      class="fixed top-0 left-1/2 -translate-x-1/2 w-full max-w-[480px] z-20"
      style="background: linear-gradient(135deg, #1e3a8a 0%, #1e40af 100%)"
    >
      <div class="flex items-center gap-3 justify-between p-4">
        <!-- 왼쪽: 아이콘 + 이름 (클릭 시 홈으로 이동) -->
        <button
          @click="goToHome"
          class="flex items-center gap-3 hover:opacity-80 transition-opacity cursor-pointer"
        >
          <div class="flex items-center gap-1">
            <div class="w-3 h-3 bg-blue-400 rounded-sm"></div>
            <div class="w-3 h-3 bg-cyan-300 rounded-sm"></div>
          </div>
          <span class="text-white font-medium"
            >{{ authStore.user?.name || "김운전" }}님</span
          >
        </button>

        <!-- 오른쪽: 날씨 + 설정 버튼 -->
        <div class="flex items-center gap-3">
          <div class="flex items-center gap-2 text-white text-sm">
            <div class="flex items-center gap-1">
              <span>☁️</span>
              <span>강수 19%</span>
            </div>
            <span>8°C/12°C</span>
          </div>
          <button
            @click="showProfile = true"
            class="text-white hover:bg-white/20 p-2 rounded-lg transition-colors"
          >
            <i class="fi fi-rr-settings text-xl"></i>
          </button>
        </div>
      </div>
    </header>
    <!-- 메인 -->
    <main
      class="bg-gray-100 overflow-y-auto overflow-x-hidden w-full max-h-[calc(100vh-68px)] pt-[68px] dark:bg-gray-900"
    >
      <router-view></router-view>
    </main>

    <!-- 프로필 모달 -->
    <WorkerProfile v-if="showProfile" @close="showProfile = false" />
    <!-- 하단 탭바 -->
    <nav
      class="fixed bottom-0 left-1/2 -translate-x-1/2 w-full max-w-[480px] bg-white/95 dark:bg-gray-900/95 backdrop-blur border-t border-gray-200 dark:border-gray-700 h-[68px] z-10"
    >
      <div class="h-full grid grid-cols-3">
        <router-link
          class="relative flex flex-col items-center justify-center text-xs"
          :to="{ name: 'MobileJobs' }"
          :class="
            $route.name === 'MobileJobs'
              ? 'text-blue-600 dark:text-blue-400'
              : 'text-gray-500 dark:text-gray-400'
          "
        >
          <span
            class="w-7 h-7 rounded-xl bg-blue-50 dark:bg-blue-900/50 flex items-center justify-center shadow-inner"
            >📋</span
          >
          작업목록
          <span
            v-if="$route.name === 'MobileJobs'"
            class="absolute -top-1 w-12 h-1 rounded-full bg-blue-600/80 dark:bg-blue-400/80"
          ></span>
        </router-link>
        <router-link
          class="relative flex flex-col items-center justify-center text-xs"
          :to="{ name: 'MobileCalendar' }"
          :class="
            $route.name === 'MobileCalendar'
              ? 'text-blue-600 dark:text-blue-400'
              : 'text-gray-500 dark:text-gray-400'
          "
          ><span
            class="w-7 h-7 rounded-xl bg-blue-50 dark:bg-blue-900/50 flex items-center justify-center shadow-inner"
            >🗓️</span
          >캘린더<span
            v-if="$route.name === 'MobileCalendar'"
            class="absolute -top-1 w-12 h-1 rounded-full bg-blue-600/80 dark:bg-blue-400/80"
          ></span
        ></router-link>
        <router-link
          class="relative flex flex-col items-center justify-center text-xs"
          :to="{ name: 'MobilePayment' }"
          :class="
            $route.name === 'MobilePayment'
              ? 'text-blue-600 dark:text-blue-400'
              : 'text-gray-500 dark:text-gray-400'
          "
        >
          <span
            class="w-7 h-7 rounded-xl bg-green-50 dark:bg-green-900/50 flex items-center justify-center shadow-inner"
            >💰</span
          >정산내역<span
            v-if="$route.name === 'MobilePayment'"
            class="absolute -top-1 w-12 h-1 rounded-full bg-blue-600/80 dark:bg-blue-400/80"
          ></span
        ></router-link>
      </div>
    </nav>
  </div>
</template>
<script setup>
import DarkModeToggle from "@/components/common/DarkModeToggle.vue";
import ApiDebugPanel from "@/components/dev/ApiDebugPanel.vue";
import { ref, computed } from "vue";
import { useAuthStore } from "@/stores/auth";
import { RouterLink, RouterView, useRoute, useRouter } from "vue-router";
import WorkerProfile from "@/components/worker/WorkerProfile.vue";

const router = useRouter();
const route = useRoute();
const authStore = useAuthStore();
const isProfileMenuOpen = ref(false);
const showProfile = ref(false);

const confirmLogout = () => {
  const isConfirmed = window.confirm("정말 로그아웃하시겠습니까?");
  if (isConfirmed) {
    handleLogout();
  }
};

const handleLogout = () => {
  isProfileMenuOpen.value = false;
  authStore.logout();
  router.push("/login");
};

const goToHome = () => {
  router.push({ name: "MobileJobs" });
};

const todayText = new Date().toLocaleDateString("ko-KR", {
  weekday: "long",
  year: "numeric",
  month: "long",
  day: "numeric",
});
</script>
