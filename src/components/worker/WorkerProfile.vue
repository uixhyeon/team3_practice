<template>
  <div 
    class="fixed inset-0 z-50 bg-black/50"
    @click.self="$emit('close')"
  >
    <div class="w-full max-w-[480px] h-full bg-gray-100 overflow-y-auto mx-auto">
      <!-- 헤더 -->
      <header
        class="sticky top-0 z-10"
        style="background: linear-gradient(135deg, #1e3a8a 0%, #1e40af 100%)"
      >
        <div class="flex items-center justify-between p-4">
          <button 
            @click="goToHome" 
            class="flex items-center gap-3 hover:opacity-80 transition-opacity cursor-pointer"
          >
            <div class="flex items-center gap-1">
              <div class="w-3 h-3 bg-blue-400 rounded-sm"></div>
              <div class="w-3 h-3 bg-cyan-300 rounded-sm"></div>
            </div>
            <span class="text-white font-medium">{{ userInfo.name }}님</span>
          </button>
          <button 
            @click="$emit('close')" 
            class="bg-white/20 text-white px-4 py-2 rounded-lg hover:bg-white/30 transition-colors text-sm"
          >
            로그아웃
          </button>
        </div>
      </header>

      <!-- 프로필 정보 카드 -->
      <div class="bg-white rounded-2xl shadow-sm mx-4 mt-4 p-5">
        <div class="flex items-center gap-4">
          <!-- 프로필 이미지 -->
          <div class="w-20 h-20 rounded-full bg-gray-200 flex items-center justify-center overflow-hidden flex-shrink-0">
            <img 
              v-if="userInfo.profileImage" 
              :src="userInfo.profileImage" 
              alt="프로필"
              class="w-full h-full object-cover"
            >
            <span v-else class="text-3xl text-gray-400">👤</span>
          </div>

          <!-- 프로필 정보 -->
          <div class="flex-1">
            <div class="text-lg font-semibold text-gray-900 mb-1">{{ userInfo.displayName }}</div>
            <div class="text-sm text-gray-600 mb-1">{{ userInfo.phone }}</div>
            <div class="text-sm text-gray-600">{{ userInfo.email }}</div>
          </div>
        </div>

        <!-- 트럭 정보 링크 -->
        <div class="mt-4 text-right">
          <button class="text-blue-600 text-sm font-medium hover:underline">
            트럭 정보 >
          </button>
        </div>
      </div>

      <!-- 이번달 운영 현황 카드 -->
      <div class="bg-white rounded-2xl shadow-sm mx-4 mt-4 p-5 mb-4">
        <div class="text-lg font-semibold text-gray-900 mb-4">이번달 운영 현황</div>
        
        <div class="space-y-3">
          <div class="flex justify-between items-center">
            <span class="text-sm text-gray-600">총 운행 일수</span>
            <span class="text-base font-semibold text-gray-900">{{ monthlyStats.totalDays }}일</span>
          </div>
          <div class="flex justify-between items-center">
            <span class="text-sm text-gray-600">총 운영 시간</span>
            <span class="text-base font-semibold text-gray-900">{{ monthlyStats.totalHours }}시간</span>
          </div>
          <div class="flex justify-between items-center">
            <span class="text-sm text-gray-600">예상 급여</span>
            <span class="text-base font-semibold text-gray-900">{{ formatCurrency(monthlyStats.estimatedSalary) }}원</span>
          </div>
        </div>

        <!-- 정산 상세 링크 -->
        <div class="mt-4 text-right">
          <button class="text-blue-600 text-sm font-medium hover:underline">
            정산 상세 >
          </button>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed } from 'vue'
import { useAuthStore } from '@/stores/auth'
import { useRouter } from 'vue-router'

const emit = defineEmits(['close'])
const authStore = useAuthStore()
const router = useRouter()

const goToHome = () => {
  emit('close')
  router.push({ name: 'MobileJobs' })
}

const userInfo = ref({
  name: authStore.user?.name || '김운전',
  displayName: '김기사',
  phone: '010-1234-5678',
  email: 'driver@example.com',
  profileImage: null
})

const monthlyStats = ref({
  totalDays: 12,
  totalHours: 78,
  estimatedSalary: 1560000
})

const formatCurrency = (amount) => {
  return amount.toLocaleString('ko-KR')
}
</script>

