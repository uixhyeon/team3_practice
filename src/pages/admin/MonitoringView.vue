<template>
  <div class="p-8 bg-slate-50 dark:bg-slate-900 min-h-screen">
    <!-- 리포트 & 통계 헤더 -->
    <div class="mb-8">
      <h1 class="text-2xl font-bold mb-6" style="color: #1E293B">리포트 & 통계</h1>
      
      <!-- 날짜 범위 선택기 -->
      <div class="flex items-center justify-center gap-4 mb-8">
        <button 
          @click="prevDateRange"
          class="p-2 hover:bg-slate-200 dark:hover:bg-slate-700 rounded-lg transition-colors"
        >
          <i class="fi fi-rr-angle-left text-xl"></i>
        </button>
        <div class="text-lg font-semibold text-slate-900 dark:text-slate-100 px-4">
          {{ formatDateRange(dateRange.start) }} ~ {{ formatDateRange(dateRange.end) }}
        </div>
        <button 
          @click="nextDateRange"
          class="p-2 hover:bg-slate-200 dark:hover:bg-slate-700 rounded-lg transition-colors"
        >
          <i class="fi fi-rr-angle-right text-xl"></i>
        </button>
      </div>
    </div>

    <!-- 왼쪽/오른쪽 2분할 레이아웃 -->
    <div class="grid grid-cols-1 lg:grid-cols-2 gap-6 mb-6">
      <!-- 왼쪽 컬럼 -->
      <div class="space-y-6">
        <!-- 주요 지표 -->
        <section>
          <h2 class="text-lg font-semibold mb-6" style="color: #1E293B">주요 지표</h2>
          <div class="grid grid-cols-1 md:grid-cols-3 gap-4">
            <!-- 매출 카드 -->
            <div class="text-white p-6 rounded-3xl shadow-sm" style="background: linear-gradient(135deg, #007AFF 0%, #007AFF 100%)">
              <div class="flex justify-between items-start mb-4">
                <div>
                  <div class="text-sm font-medium opacity-90">매출</div>
                  <div class="text-3xl font-bold mt-2">{{ formatCurrency(keyMetrics.revenue) }}</div>
                  <div class="text-sm mt-2 text-green-200">
                    <i class="fi fi-rr-arrow-up mr-1"></i>{{ keyMetrics.revenueChange }}%
                  </div>
                </div>
                <i class="fi fi-rr-arrow-up-right text-xl"></i>
              </div>
            </div>

            <!-- 이용객 카드 -->
            <div class="text-white p-6 rounded-3xl shadow-sm" style="background: linear-gradient(135deg, #000000 0%, #000000 100%)">
              <div class="flex justify-between items-start mb-4">
                <div>
                  <div class="text-sm font-medium opacity-90">이용객</div>
                  <div class="text-3xl font-bold mt-2">{{ formatNumber(keyMetrics.users) }}명</div>
                  <div class="text-sm mt-2 text-green-200">
                    <i class="fi fi-rr-arrow-up mr-1"></i>{{ keyMetrics.usersChange }}%
                  </div>
                </div>
                <i class="fi fi-rr-arrow-up-right text-xl"></i>
              </div>
            </div>

            <!-- 이용률 카드 -->
            <div class="text-white p-6 rounded-3xl shadow-sm" style="background: linear-gradient(135deg, #007AFF 0%, #007AFF 100%)">
              <div class="flex justify-between items-start mb-4">
                <div>
                  <div class="text-sm font-medium opacity-90">이용률</div>
                  <div class="text-3xl font-bold mt-2">{{ keyMetrics.utilizationRate }}%</div>
                  <div class="text-sm mt-2 text-red-200">
                    <i class="fi fi-rr-arrow-down mr-1"></i>{{ Math.abs(keyMetrics.utilizationChange) }}%
                  </div>
                </div>
                <i class="fi fi-rr-arrow-down-left text-xl"></i>
              </div>
            </div>
          </div>
        </section>

        <!-- 재방문율 & 홈 배송 선택률 카드 -->
        <div class="grid grid-cols-1 md:grid-cols-2 gap-4">
          <!-- 재방문율 카드 -->
          <div class="text-slate-900 p-6 rounded-3xl shadow-sm" style="background: linear-gradient(135deg, #fbbf24 0%, #fbbf24 100%)">
            <div class="flex justify-between items-start mb-4">
              <div>
                <div class="text-sm font-medium opacity-90">재방문율</div>
                <div class="text-3xl font-bold mt-2">{{ additionalMetrics.revisitRate }}%</div>
                <div class="text-sm mt-2 text-green-700">
                  <i class="fi fi-rr-arrow-up mr-1"></i>{{ additionalMetrics.revisitChange }}%
                </div>
              </div>
              <i class="fi fi-rr-arrow-up-right text-xl"></i>
            </div>
          </div>

          <!-- 홈 배송 선택률 카드 -->
          <div class="text-white p-6 rounded-3xl shadow-sm" style="background: linear-gradient(135deg, #f59e0b 0%, #f59e0b 100%)">
            <div class="flex justify-between items-start mb-4">
              <div>
                <div class="text-sm font-medium opacity-90">홈 배송 선택률</div>
                <div class="text-3xl font-bold mt-2">{{ additionalMetrics.deliveryRate }}%</div>
                <div class="text-sm mt-2 text-green-200">
                  <i class="fi fi-rr-arrow-up mr-1"></i>{{ additionalMetrics.deliveryChange }}%
                </div>
              </div>
              <i class="fi fi-rr-arrow-up-right text-xl"></i>
            </div>
          </div>
        </div>
        <!-- 행사 유형별 매출 -->
        <section>
          <h2 class="text-lg font-semibold mb-4" style="color: #1E293B">행사 유형별 매출</h2>
          <div class="bg-white dark:bg-slate-800 rounded-2xl shadow-sm p-6">
            <div class="h-64 relative">
            <!-- Y축 라벨 -->
            <div class="absolute left-0 top-0 h-full flex flex-col justify-between text-xs text-slate-500 dark:text-slate-400 pr-2">
              <span>1,200</span>
              <span>900</span>
              <span>600</span>
              <span>300</span>
              <span>100</span>
            </div>
            <!-- 차트 영역 -->
            <div class="ml-8 h-full flex items-end justify-center gap-4">
              <div v-for="(item, index) in eventTypeSales" :key="item.type" class="flex flex-col items-center">
                <div 
                  class="w-16 rounded-t-lg transition-all hover:opacity-80"
                  :style="{ 
                    height: `${((item.value - 100) / (maxEventValue - 100)) * 200}px`,
                    backgroundColor: item.color
                  }"
                ></div>
                <div class="mt-2 text-xs text-slate-600 dark:text-slate-400 text-center">
                  <div class="font-semibold">{{ item.type }}</div>
                  <div>{{ item.percentage }}%</div>
                </div>
              </div>
            </div>
            </div>
            <div class="text-center text-sm text-slate-500 dark:text-slate-400 mt-4">11월 매출</div>
          </div>
        </section>

        <!-- 결제 수단 -->
        <section>
          <h2 class="text-lg font-semibold mb-4" style="color: #1E293B">결제 수단</h2>
          <div class="bg-white dark:bg-slate-800 rounded-2xl shadow-sm p-6">
            <div class="space-y-4">
            <div class="flex items-center gap-3">
              <div class="text-sm font-medium text-slate-700 dark:text-slate-300 w-20">카드</div>
              <div class="flex-1 h-8 bg-slate-200 dark:bg-slate-700 rounded-lg overflow-hidden relative">
                <div 
                  class="h-full rounded-lg flex items-center justify-end pr-2"
                  style="width: 35%; background-color: #fbbf24;"
                >
                  <span class="text-xs font-semibold text-white">35%</span>
                </div>
              </div>
            </div>
            <div class="flex items-center gap-3">
              <div class="text-sm font-medium text-slate-700 dark:text-slate-300 w-20">기타</div>
              <div class="flex-1 h-8 bg-slate-200 dark:bg-slate-700 rounded-lg overflow-hidden relative">
                <div 
                  class="h-full rounded-lg flex items-center justify-end pr-2"
                  style="width: 65%; background-color: #3b82f6;"
                >
                  <span class="text-xs font-semibold text-white">65%</span>
                </div>
              </div>
            </div>
            </div>
          </div>
        </section>

        <!-- 사이즈별 비율 -->
        <section>
          <h2 class="text-lg font-semibold mb-4" style="color: #1E293B">사이즈별 비율</h2>
          <div class="bg-white dark:bg-slate-800 rounded-2xl shadow-sm p-6">
            <div class="flex items-center justify-center gap-6">
            <div class="relative w-32 h-32">
              <svg class="w-full h-full transform -rotate-90" viewBox="0 0 100 100">
                <circle
                  v-for="(segment, index) in sizeRatio"
                  :key="segment.size"
                  :cx="50"
                  :cy="50"
                  :r="40"
                  :stroke="segment.color"
                  :stroke-width="20"
                  :stroke-dasharray="`${segment.percentage * 2.513} 251.3`"
                  :stroke-dashoffset="getPieOffset(index)"
                  fill="none"
                  class="transition-all"
                />
              </svg>
            </div>
            <div class="space-y-2">
              <div v-for="segment in sizeRatio" :key="segment.size" class="flex items-center gap-2">
                <div 
                  class="w-4 h-4 rounded-full"
                  :style="{ backgroundColor: segment.color }"
                ></div>
                <span class="text-sm text-slate-700 dark:text-slate-300">
                  {{ segment.size }} : {{ segment.percentage }}%
                </span>
              </div>
            </div>
            </div>
          </div>
        </section>
      </div>

      <!-- 오른쪽 컬럼 -->
      <div class="space-y-6">
        <!-- 피크타임 분석 -->
        <section>
          <h2 class="text-lg font-semibold mb-4" style="color: #1E293B">피크타임 분석</h2>
          <div class="bg-white dark:bg-slate-800 rounded-2xl shadow-sm p-6">
            <div class="h-64 relative">
            <svg class="w-full h-full" viewBox="0 0 400 200" preserveAspectRatio="none">
              <!-- Y축 그리드 -->
              <line v-for="i in 5" :key="i" 
                :x1="40" :y1="i * 40" 
                :x2="400" :y2="i * 40" 
                stroke="#e2e8f0" stroke-width="1" 
                class="dark:stroke-slate-700"/>
              
              <!-- Y축 라벨 -->
              <g v-for="(label, index) in [450, 360, 270, 180, 90, 0]" :key="label">
                <text 
                  :x="35" 
                  :y="20 + index * 40" 
                  fill="#64748b" 
                  font-size="10" 
                  text-anchor="end"
                  class="dark:fill-slate-400"
                >{{ label }}</text>
              </g>
              
              <!-- 기기(store) 라인 -->
              <polyline
                :points="peakTimeData.storeLine"
                fill="none"
                stroke="#60a5fa"
                stroke-width="2"
              />
              
              <!-- 찾기(find) 라인 -->
              <polyline
                :points="peakTimeData.findLine"
                fill="none"
                stroke="#10b981"
                stroke-width="2"
              />
              
              <!-- 범례 -->
              <g transform="translate(250, 20)">
                <line x1="0" y1="0" x2="20" y2="0" stroke="#60a5fa" stroke-width="2"/>
                <text x="25" y="5" fill="#64748b" font-size="12" class="dark:fill-slate-400">기기(store)</text>
                <line x1="0" y1="15" x2="20" y2="15" stroke="#10b981" stroke-width="2"/>
                <text x="25" y="20" fill="#64748b" font-size="12" class="dark:fill-slate-400">찾기(find)</text>
              </g>
              
              <!-- X축 라벨 -->
              <g v-for="(hour, index) in peakTimeData.hours" :key="hour" transform="translate(50 + index * 50, 180)">
                <text :x="0" :y="0" fill="#64748b" font-size="10" text-anchor="middle" class="dark:fill-slate-400">{{ hour }}시</text>
              </g>
            </svg>
            </div>
          </div>
        </section>

        <!-- 지역별 배송 -->
        <section>
          <h2 class="text-lg font-semibold mb-4" style="color: #1E293B">지역별 배송</h2>
          <div class="bg-white dark:bg-slate-800 rounded-2xl shadow-sm p-6">
            <!-- 히트맵 스타일 지도 -->
            <div class="flex flex-col items-center gap-2 mb-4">
              <!-- 1행: 2개 카드 -->
              <div class="flex justify-center gap-2 w-full">
                <div 
                  :class="getHeatmapColor(deliveryHeatmap[0].count)"
                  class="h-20 w-28 min-w-28 max-w-28 flex-shrink-0 rounded-lg flex items-center justify-center text-slate-900 font-semibold cursor-pointer hover:opacity-80 transition-opacity text-center text-xs px-2"
                  @click="selectRegion(deliveryHeatmap[0])"
                >
                  {{ deliveryHeatmap[0].name }}
                </div>
                <div 
                  :class="getHeatmapColor(deliveryHeatmap[2].count)"
                  class="h-20 w-28 min-w-28 max-w-28 flex-shrink-0 rounded-lg flex items-center justify-center text-slate-900 font-semibold cursor-pointer hover:opacity-80 transition-opacity text-center text-xs px-2"
                  @click="selectRegion(deliveryHeatmap[2])"
                >
                  {{ deliveryHeatmap[2].name }}
                </div>
              </div>
              
              <!-- 2행: 3개 카드 -->
              <div class="flex justify-center gap-2 w-full">
                <div 
                  :class="getHeatmapColor(deliveryHeatmap[3].count)"
                  class="h-20 w-28 min-w-28 max-w-28 flex-shrink-0 rounded-lg flex items-center justify-center text-slate-900 font-semibold cursor-pointer hover:opacity-80 transition-opacity text-center text-xs px-2"
                  @click="selectRegion(deliveryHeatmap[3])"
                >
                  {{ deliveryHeatmap[3].name }}
                </div>
                <div 
                  :class="getHeatmapColor(deliveryHeatmap[1].count)"
                  class="h-20 w-28 min-w-28 max-w-28 flex-shrink-0 rounded-lg flex items-center justify-center text-slate-900 font-semibold cursor-pointer hover:opacity-80 transition-opacity text-center text-xs px-2"
                  @click="selectRegion(deliveryHeatmap[1])"
                >
                  {{ deliveryHeatmap[1].name }}
                </div>
                <div 
                  :class="getHeatmapColor(deliveryHeatmap[4].count)"
                  class="h-20 w-28 min-w-28 max-w-28 flex-shrink-0 rounded-lg flex items-center justify-center text-slate-900 font-semibold cursor-pointer hover:opacity-80 transition-opacity text-center text-xs px-2"
                  @click="selectRegion(deliveryHeatmap[4])"
                >
                  {{ deliveryHeatmap[4].name }}
                </div>
              </div>
              
              <!-- 3행: 2개 카드 -->
              <div class="flex justify-center gap-2 w-full">
                <div 
                  :class="getHeatmapColor(deliveryHeatmap[5].count)"
                  class="h-20 w-28 min-w-28 max-w-28 flex-shrink-0 rounded-lg flex items-center justify-center text-slate-900 font-semibold cursor-pointer hover:opacity-80 transition-opacity text-center text-xs px-2"
                  @click="selectRegion(deliveryHeatmap[5])"
                >
                  {{ deliveryHeatmap[5].name }}
                </div>
                <div 
                  :class="getHeatmapColor(deliveryHeatmap[6].count)"
                  class="h-20 w-28 min-w-28 max-w-28 flex-shrink-0 rounded-lg flex items-center justify-center text-slate-900 font-semibold cursor-pointer hover:opacity-80 transition-opacity text-center text-xs px-2"
                  @click="selectRegion(deliveryHeatmap[6])"
                >
                  {{ deliveryHeatmap[6].name }}
                </div>
              </div>
            </div>
            
            <!-- Top 3 리스트 -->
            <div class="bg-slate-50 dark:bg-slate-900 rounded-lg p-4">
              <div class="text-sm font-semibold mb-3" style="color: #1E293B">Top 3</div>
              <div v-for="(region, index) in deliveryRegions" :key="index" class="text-sm mb-2 text-slate-700 dark:text-slate-300">
                {{ region.name }} : {{ region.percentage }}%
              </div>
              <button class="mt-3 px-4 py-2 bg-yellow-400 hover:bg-yellow-500 text-slate-900 rounded-lg text-sm font-medium transition-colors">
                그 외
              </button>
            </div>
          </div>
        </section>

        <!-- 인사이트 -->
        <section>
          <h2 class="text-lg font-semibold mb-4" style="color: #1E293B">인사이트</h2>
          <div class="bg-white dark:bg-slate-800 rounded-2xl shadow-sm p-6">
            <div class="space-y-3">
            <div 
              v-for="(insight, index) in insights" 
              :key="index"
              class="flex items-start gap-3 p-3 bg-slate-50 dark:bg-slate-900 rounded-lg"
            >
              <div class="w-2 h-2 rounded-full bg-blue-500 mt-2 flex-shrink-0"></div>
              <p class="text-sm text-slate-700 dark:text-slate-300">{{ insight }}</p>
            </div>
            </div>
          </div>
        </section>
      </div>
    </div>

    <!-- 액션 버튼 -->
    <div class="flex justify-end gap-4">
      <button class="px-6 py-3 bg-white dark:bg-slate-800 text-slate-700 dark:text-slate-300 rounded-lg shadow-sm hover:shadow-md transition-all flex items-center gap-2">
        <i class="fi fi-rr-download"></i>
        PDF 다운로드
      </button>
      <button class="px-6 py-3 bg-white dark:bg-slate-800 text-slate-700 dark:text-slate-300 rounded-lg shadow-sm hover:shadow-md transition-all flex items-center gap-2">
        <i class="fi fi-rr-envelope"></i>
        이메일 발송
      </button>
    </div>
  </div>
</template>

<script setup>
import { ref, computed } from 'vue'

// 날짜 범위 관리 (주간 설정)
const dateRange = ref({
  start: new Date(2025, 10, 17), // 2025-11-17
  end: new Date(2025, 10, 23)    // 2025-11-23 (7일 범위)
})

const formatDateRange = (date) => {
  const year = date.getFullYear()
  const month = String(date.getMonth() + 1).padStart(2, '0')
  const day = String(date.getDate()).padStart(2, '0')
  return `${year}-${month}-${day}`
}

const prevDateRange = () => {
  const days = 7 // 주간(7일) 범위
  dateRange.value.start = new Date(dateRange.value.start.getTime() - days * 24 * 60 * 60 * 1000)
  dateRange.value.end = new Date(dateRange.value.end.getTime() - days * 24 * 60 * 60 * 1000)
}

const nextDateRange = () => {
  const days = 7 // 주간(7일) 범위
  dateRange.value.start = new Date(dateRange.value.start.getTime() + days * 24 * 60 * 60 * 1000)
  dateRange.value.end = new Date(dateRange.value.end.getTime() + days * 24 * 60 * 60 * 1000)
}

// 주요 지표 (더미 데이터 - 나중에 props나 composable로 교체)
const keyMetrics = ref({
  revenue: 28000000,
  revenueChange: 12,
  users: 2100,
  usersChange: 8,
  utilizationRate: 3.2,
  utilizationChange: -0.5
})

// 추가 지표 (재방문율, 홈 배송 선택률)
const additionalMetrics = ref({
  revisitRate: 45.2,
  revisitChange: 5.3,
  deliveryRate: 19.0,
  deliveryChange: 2.1
})

const formatCurrency = (value) => {
  const 만 = Math.floor(value / 10000)
  return `${만}만`
}

const formatNumber = (value) => {
  return value.toLocaleString('ko-KR')
}

// 피크타임 분석 데이터
const peakTimeData = computed(() => {
  const hours = [16, 17, 18, 19, 20, 21, 22, 23]
  const storeValues = [80, 120, 180, 220, 280, 320, 380, 350]
  const findValues = [50, 90, 150, 200, 280, 400, 420, 380]
  
  const maxValue = 450
  const width = 400
  const height = 200
  
  const storePoints = hours.map((hour, index) => {
    const x = 50 + (index * (width - 100) / (hours.length - 1))
    const y = height - 20 - (storeValues[index] / maxValue) * (height - 40)
    return `${x},${y}`
  }).join(' ')
  
  const findPoints = hours.map((hour, index) => {
    const x = 50 + (index * (width - 100) / (hours.length - 1))
    const y = height - 20 - (findValues[index] / maxValue) * (height - 40)
    return `${x},${y}`
  }).join(' ')
  
  return {
    hours,
    storeLine: storePoints,
    findLine: findPoints
  }
})

// 행사 유형별 매출
const eventTypeSales = ref([
  { type: '콘서트', value: 1200, percentage: 45, color: '#3b82f6' },
  { type: '대구', value: 800, percentage: 30, color: '#10b981' },
  { type: '축구', value: 500, percentage: 19, color: '#f59e0b' },
  { type: '기타', value: 200, percentage: 6, color: '#ef4444' }
])

const maxEventValue = computed(() => {
  return Math.max(...eventTypeSales.value.map(item => item.value))
})

// 지역별 배송 (Top 3)
const deliveryRegions = ref([
  { name: '서울 강남권', percentage: 35 },
  { name: '서울 강북권', percentage: 25 },
  { name: '경기 남부', percentage: 20 }
])

// 지역별 배송 히트맵 데이터
const deliveryHeatmap = ref([
  { name: '서북권', count: 180, percentage: 15 }, // 마포구 등
  { name: '도심권', count: 320, percentage: 27 }, // 종로구 등
  { name: '동북권', count: 150, percentage: 13 }, // 노원구 등
  { name: '서남권', count: 200, percentage: 17 }, // 영등포구 등
  { name: '동남권', count: 380, percentage: 32 }, // 강남구 등
  { name: '경기/인천', count: 120, percentage: 10 },
  { name: '그외 지방', count: 50, percentage: 4 }
])

// 3x3 그리드 구조로 매핑 (빈칸 위치: 4, 7)
const heatmapGrid = computed(() => {
  const grid = []
  const emptyPositions = [4, 7] // 2행 중앙, 3행 중앙
  
  for (let i = 0; i < 9; i++) {
    if (emptyPositions.includes(i)) {
      grid.push({ region: null })
    } else {
      const regionIndex = i < 4 ? i : i - 1 // 빈칸 위치를 제외한 인덱스
      grid.push({ 
        region: deliveryHeatmap.value[regionIndex] || null 
      })
    }
  }
  
  return grid
})

// 배송량에 따른 색상 클래스 반환
const getHeatmapColor = (count) => {
  if (count >= 300) return 'bg-orange-900'
  if (count >= 200) return 'bg-orange-700'
  if (count >= 100) return 'bg-orange-500'
  if (count >= 50) return 'bg-orange-300'
  return 'bg-orange-100'
}

// 권역 선택 핸들러
const selectRegion = (region) => {
  console.log('선택된 권역:', region)
  // 여기에 상세 정보 모달이나 페이지 이동 로직 추가 가능
}

// 결제 수단은 이미지에 따라 카드 35%, 기타 65%로 표시

// 사이즈별 비율
const sizeRatio = ref([
  { size: 'Medium', percentage: 65, color: '#3b82f6' },
  { size: 'Small', percentage: 20, color: '#ec4899' },
  { size: 'Large', percentage: 10, color: '#f59e0b' },
  { size: 'XLarge', percentage: 5, color: '#fbbf24' }
])

const getPieOffset = (index) => {
  let offset = 0
  for (let i = 0; i < index; i++) {
    offset += sizeRatio.value[i].percentage * 2.513
  }
  return -offset
}

// 인사이트
const insights = ref([
  '이용률 3.2%로 목표(5%) 미달 → 현장 마케팅 강화 필요',
  'Medium 사이즈 집중 (65%) → 재고 관리 최적화',
  '배송 신청 19% (증가 추세) → 배송 인프라 확대 검토'
])
</script>

<style scoped>
</style>