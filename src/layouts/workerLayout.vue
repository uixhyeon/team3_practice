<template>
  <div
    class="h-screen w-full max-w-[480px] fixed top-0 left-1/2 -translate-x-1/2 overflow-hidden bg-white dark:bg-black"
  >
    <!-- 헤더 -->
    <header
      class="fixed top-0 left-1/2 -translate-x-1/2 w-full max-w-[480px] z-20"
      style="background: linear-gradient(135deg, #1e3a8a 0%, #1e40af 100%)"
    >
      <!-- 첫 번째 줄: 이름과 버튼들 -->
      <div class="flex items-center gap-3 justify-between p-4 pb-2">
        <!-- 왼쪽: 아이콘 + 이름 (클릭 시 홈으로 이동) -->
        <button
          @click="goToHome"
          class="flex items-center gap-3 hover:opacity-80 transition-opacity cursor-pointer"
        >
          <div class="flex items-center gap-1">
            <div class="w-3 h-3 bg-blue-400 rounded-sm"></div>
            <div class="w-3 h-3 bg-cyan-300 rounded-sm"></div>
          </div>
          <span class="text-white text-base"
            >{{ authStore.user?.name || "김운전" }}님</span
          >
        </button>

        <!-- 오른쪽: 다크모드 토글 + 설정 버튼 -->
        <div class="flex items-center gap-2">
          <DarkModeToggle />
          <button
            @click="goToProfile"
            class="text-white hover:bg-white/20 p-2 rounded-lg transition-colors"
          >
            <i class="fi fi-rr-settings text-xl"></i>
          </button>
        </div>
      </div>
    </header>
    <!-- 메인 -->
    <main
      class="bg-gray-100 overflow-y-auto overflow-x-hidden w-full h-full pt-[68px] dark:bg-gray-900"
    >
      <router-view></router-view>
    </main>
  </div>
</template>
<script setup>
import DarkModeToggle from "@/components/common/DarkModeToggle.vue";
import ApiDebugPanel from "@/components/dev/ApiDebugPanel.vue";
import { ref, computed } from "vue";
import { useAuthStore } from "@/stores/auth";
import { RouterLink, RouterView, useRoute, useRouter } from "vue-router";

const router = useRouter();
const route = useRoute();
const authStore = useAuthStore();
const isProfileMenuOpen = ref(false);

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
  router.push({ name: "WorkerWork" });
};

const goToProfile = () => {
  router.push({ name: "WorkerSettings" });
};

const todayText = new Date().toLocaleDateString("ko-KR", {
  weekday: "long",
  year: "numeric",
  month: "long",
  day: "numeric",
});
</script>
