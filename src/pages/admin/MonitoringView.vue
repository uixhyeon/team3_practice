ㄱ
<template>
  <div
    class="p-8 bg-slate-50 dark:bg-slate-900 min-h-screen"
    @click="showCalendar = false"
  >
    <!-- 리포트 & 통계 헤더 -->
    <div class="mb-8">
      <h1 class="text-2xl font-bold mb-6" style="color: #1e293b">
        리포트 & 통계
      </h1>

      <!-- 날짜 범위 선택기 -->
      <div class="mb-8">
        <div class="flex items-center justify-center gap-4 relative">
          <button
            @click="prevDateRange"
            class="p-2.5 hover:bg-slate-200 dark:hover:bg-slate-700 rounded-lg transition-colors flex items-center justify-center"
            title="이전 주"
          >
            <i
              class="fi fi-rr-angle-left text-2xl text-slate-700 dark:text-slate-300"
            ></i>
          </button>
          <div
            @click.stop="showCalendar = !showCalendar"
            class="px-6 py-2 cursor-pointer hover:bg-slate-100 dark:hover:bg-slate-800 rounded-lg transition-colors flex flex-col items-center"
          >
            <div
              class="text-lg font-semibold text-slate-900 dark:text-slate-100"
            >
              {{ getWeekLabel(dateRange.start) }}
            </div>
            <div class="text-xs text-slate-500 dark:text-slate-400 mt-1">
              {{ formatDateRange(dateRange.start) }} ~
              {{ formatDateRange(dateRange.end) }}
            </div>
          </div>
          <button
            @click="nextDateRange"
            class="p-2.5 hover:bg-slate-200 dark:hover:bg-slate-700 rounded-lg transition-colors flex items-center justify-center"
            title="다음 주"
          >
            <i
              class="fi fi-rr-angle-right text-2xl text-slate-700 dark:text-slate-300"
            ></i>
          </button>

          <!-- 달력 모달 -->
          <div
            v-if="showCalendar"
            class="absolute top-full left-1/2 transform -translate-x-1/2 mt-3 bg-white dark:bg-slate-800 rounded-2xl shadow-2xl p-6 z-50 border border-slate-200 dark:border-slate-700 min-w-[320px]"
            @click.stop
          >
            <!-- 헤더 -->
            <div class="flex items-center justify-between mb-6">
              <button
                @click="prevCalendarMonth"
                class="p-2 rounded-lg hover:bg-slate-100 dark:hover:bg-slate-700 text-slate-600 dark:text-slate-300 transition-colors"
                title="이전 달"
              >
                <i class="fi fi-rr-angle-left text-lg"></i>
              </button>
              <div
                class="text-lg font-bold text-slate-900 dark:text-white px-4"
              >
                {{ calendarYear }}년
                {{ String(calendarMonth + 1).padStart(2, "0") }}월
              </div>
              <button
                @click="nextCalendarMonth"
                class="p-2 rounded-lg hover:bg-slate-100 dark:hover:bg-slate-700 text-slate-600 dark:text-slate-300 transition-colors"
                title="다음 달"
              >
                <i class="fi fi-rr-angle-right text-lg"></i>
              </button>
            </div>

            <!-- 요일 헤더 -->
            <div class="grid grid-cols-7 gap-1 mb-2">
              <div
                v-for="day in ['일', '월', '화', '수', '목', '금', '토']"
                :key="day"
                :class="[
                  'text-center text-xs font-semibold py-2',
                  day === '일' ? 'text-red-500 dark:text-red-400' : '',
                  day === '토' ? 'text-blue-500 dark:text-blue-400' : '',
                  day !== '일' && day !== '토'
                    ? 'text-slate-500 dark:text-slate-400'
                    : '',
                ]"
              >
                {{ day }}
              </div>
            </div>

            <!-- 달력 그리드 -->
            <div class="grid grid-cols-7 gap-0.5">
              <div
                v-for="d in calendarDays"
                :key="d.key"
                :class="[
                  'aspect-square flex items-center justify-center text-sm cursor-pointer select-none transition-all duration-200 relative',
                  d.outside
                    ? 'text-slate-300 dark:text-slate-600'
                    : isDateInRange(d.date)
                      ? 'bg-blue-100 dark:bg-blue-900/30 text-blue-700 dark:text-blue-300 font-semibold'
                      : 'text-slate-700 dark:text-slate-200 hover:bg-blue-50 dark:hover:bg-slate-700',
                  // 주간의 첫 번째 날짜 (월요일)
                  isDateInRange(d.date) && isWeekStart(d.date) && !d.outside
                    ? 'rounded-l-xl'
                    : '',
                  // 주간의 마지막 날짜 (일요일)
                  isDateInRange(d.date) && d.date.getDay() === 0 && !d.outside
                    ? 'rounded-r-xl'
                    : '',
                  // 주간의 중간 날짜들
                  isDateInRange(d.date) &&
                  !isWeekStart(d.date) &&
                  d.date.getDay() !== 0 &&
                  !d.outside
                    ? ''
                    : '',
                  // 선택되지 않은 날짜는 둥근 모서리
                  !isDateInRange(d.date) && !d.outside ? 'rounded-xl' : '',
                ]"
                @click="selectWeekFromDate(d.date)"
                @mouseenter="hoveredCalendarDate = d.date"
                @mouseleave="hoveredCalendarDate = null"
              >
                <span :class="['relative z-10']">
                  {{ d.date.getDate() }}
                </span>
                <!-- 오늘 표시 -->
                <span
                  v-if="isToday(d.date) && !isDateInRange(d.date)"
                  class="absolute bottom-1 left-1/2 transform -translate-x-1/2 w-1 h-1 rounded-full bg-blue-500"
                ></span>
              </div>
            </div>

            <!-- 선택된 주간 표시 -->
            <div
              v-if="dateRange"
              class="mt-4 pt-4 border-t border-slate-200 dark:border-slate-700"
            >
              <div
                class="text-xs text-slate-500 dark:text-slate-400 text-center"
              >
                선택된 주간
              </div>
              <div
                class="text-sm font-semibold text-slate-900 dark:text-white text-center mt-1"
              >
                {{ formatDateRange(dateRange.start) }} ~
                {{ formatDateRange(dateRange.end) }}
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>

    <!-- 왼쪽/오른쪽 2분할 레이아웃 -->
    <div class="grid grid-cols-1 lg:grid-cols-2 gap-6 mb-6">
      <!-- 왼쪽 컬럼 -->
      <div class="space-y-6">
        <!-- 주요 지표 -->
        <section>
          <h2 class="text-lg font-semibold mb-6" style="color: #1e293b">
            주요 지표
          </h2>
          <div class="grid grid-cols-1 md:grid-cols-3 gap-4">
            <!-- 매출 카드 -->
            <div
              class="text-white p-6 rounded-3xl shadow-sm"
              style="
                background: linear-gradient(135deg, #007aff 0%, #007aff 100%);
              "
            >
              <div class="flex justify-between items-start mb-4">
                <div>
                  <div class="text-sm font-medium opacity-90">매출</div>
                  <div class="text-3xl font-bold mt-2">
                    {{ formatCurrency(keyMetrics.revenue) }}
                  </div>
                  <div class="text-sm mt-2 text-green-200">
                    <i class="fi fi-rr-arrow-up mr-1"></i
                    >{{ keyMetrics.revenueChange }}%
                  </div>
                </div>
              </div>
            </div>

            <!-- 이용객 카드 -->
            <div
              class="text-white p-6 rounded-3xl shadow-sm"
              style="
                background: linear-gradient(135deg, #000000 0%, #000000 100%);
              "
            >
              <div class="flex justify-between items-start mb-4">
                <div>
                  <div class="text-sm font-medium opacity-90">이용객</div>
                  <div class="text-3xl font-bold mt-2">
                    {{ formatNumber(keyMetrics.users) }}명
                  </div>
                  <div class="text-sm mt-2 text-green-200">
                    <i class="fi fi-rr-arrow-up mr-1"></i
                    >{{ keyMetrics.usersChange }}%
                  </div>
                </div>
              </div>
            </div>

            <!-- 이용률 카드 -->
            <div
              class="text-white p-6 rounded-3xl shadow-sm"
              style="
                background: linear-gradient(135deg, #007aff 0%, #007aff 100%);
              "
            >
              <div class="flex justify-between items-start mb-4">
                <div>
                  <div class="text-sm font-medium opacity-90">이용률</div>
                  <div class="text-3xl font-bold mt-2">
                    {{ keyMetrics.utilizationRate }}%
                  </div>
                  <div class="text-sm mt-2 text-red-200">
                    <i class="fi fi-rr-arrow-down mr-1"></i
                    >{{ Math.abs(keyMetrics.utilizationChange) }}%
                  </div>
                </div>
              </div>
            </div>
          </div>
        </section>

        <!-- 재방문율 & 홈 배송 선택률 카드 -->
        <div class="grid grid-cols-1 md:grid-cols-2 gap-4">
          <!-- 재방문율 카드 -->
          <div
            class="text-slate-900 p-6 rounded-3xl shadow-sm"
            style="
              background: linear-gradient(135deg, #fbbf24 0%, #fbbf24 100%);
            "
          >
            <div class="flex justify-between items-start mb-4">
              <div>
                <div class="text-sm font-medium opacity-90">재방문율</div>
                <div class="text-3xl font-bold mt-2">
                  {{ additionalMetrics.revisitRate }}%
                </div>
                <div class="text-sm mt-2 text-green-700">
                  <i class="fi fi-rr-arrow-up mr-1"></i
                  >{{ additionalMetrics.revisitChange }}%
                </div>
              </div>
            </div>
          </div>

          <!-- 홈 배송 선택률 카드 -->
          <div
            class="text-white p-6 rounded-3xl shadow-sm"
            style="
              background: linear-gradient(135deg, #f59e0b 0%, #f59e0b 100%);
            "
          >
            <div class="flex justify-between items-start mb-4">
              <div>
                <div class="text-sm font-medium opacity-90">홈 배송 선택률</div>
                <div class="text-3xl font-bold mt-2">
                  {{ additionalMetrics.deliveryRate }}%
                </div>
                <div class="text-sm mt-2 text-green-200">
                  <i class="fi fi-rr-arrow-up mr-1"></i
                  >{{ additionalMetrics.deliveryChange }}%
                </div>
              </div>
            </div>
          </div>
        </div>
        <!-- 행사 유형별 매출 -->
        <section>
          <h2 class="text-lg font-semibold mb-4" style="color: #1e293b">
            행사 유형별 매출
          </h2>
          <div class="bg-white dark:bg-slate-800 rounded-2xl shadow-sm p-6">
            <div class="h-64 relative">
              <!-- Y축 라벨 (동적) -->
              <div
                class="absolute left-0 top-0 h-full flex flex-col justify-between text-xs text-slate-500 dark:text-slate-400 pr-2"
              >
                <span v-if="maxEventValue > 0">{{
                  formatNumber(Math.ceil(maxEventValue))
                }}</span>
                <span v-if="maxEventValue > 0">{{
                  formatNumber(Math.ceil(maxEventValue * 0.75))
                }}</span>
                <span v-if="maxEventValue > 0">{{
                  formatNumber(Math.ceil(maxEventValue * 0.5))
                }}</span>
                <span v-if="maxEventValue > 0">{{
                  formatNumber(Math.ceil(maxEventValue * 0.25))
                }}</span>
                <span>0</span>
              </div>
              <!-- 차트 영역 -->
              <div
                class="ml-8 h-full flex items-end justify-center gap-4 relative"
                @mouseleave="hoveredEventType = null"
              >
                <div
                  v-if="eventTypeSales.length === 0"
                  class="text-sm text-slate-500 dark:text-slate-400"
                >
                  데이터가 없습니다
                </div>
                <div
                  v-for="(item, index) in eventTypeSales"
                  :key="item.type"
                  class="flex flex-col items-center relative group"
                  @mouseenter="hoveredEventType = item"
                >
                  <div
                    class="w-16 rounded-t-lg transition-all hover:opacity-80 cursor-pointer min-h-[4px]"
                    :style="{
                      height:
                        maxEventValue > 0
                          ? `${Math.max((item.value / maxEventValue) * 200, 4)}px`
                          : '4px',
                      backgroundColor: item.color,
                    }"
                  ></div>
                  <div
                    class="mt-2 text-xs text-slate-600 dark:text-slate-400 text-center"
                  >
                    <div class="font-semibold">{{ item.type }}</div>
                    <div>{{ item.percentage }}%</div>
                  </div>

                  <!-- 툴팁 -->
                  <div
                    v-if="hoveredEventType?.type === item.type"
                    class="absolute bottom-full mb-2 left-1/2 transform -translate-x-1/2 bg-slate-900 dark:bg-slate-700 text-white text-xs rounded-lg p-3 shadow-lg z-10 whitespace-nowrap"
                  >
                    <div class="font-semibold mb-1">{{ item.type }}</div>
                    <div>매출: {{ formatNumber(item.value) }}원</div>
                    <div>비율: {{ item.percentage }}%</div>
                    <div>건수: {{ item.count || 0 }}건</div>
                  </div>
                </div>
              </div>
            </div>
            <div
              class="text-center text-sm text-slate-500 dark:text-slate-400 mt-4"
            >
              11월 매출
            </div>
          </div>
        </section>

        <!-- 결제 수단 -->
        <section>
          <h2 class="text-lg font-semibold mb-4" style="color: #1e293b">
            결제 수단
          </h2>
          <div class="bg-white dark:bg-slate-800 rounded-2xl shadow-sm p-6">
            <div class="space-y-4 relative">
              <div class="flex items-center gap-3">
                <div
                  class="text-sm font-medium text-slate-700 dark:text-slate-300 w-20"
                >
                  카드
                </div>
                <div
                  class="flex-1 h-8 bg-slate-200 dark:bg-slate-700 rounded-lg overflow-hidden relative"
                  @mouseenter="
                    (e) => {
                      hoveredPaymentMethod = {
                        name: '카드',
                        count: paymentMethods.card.count,
                        percentage: paymentMethods.card.percentage,
                      };
                      const rect = e.currentTarget.getBoundingClientRect();
                      paymentTooltipPosition.x = rect.left + rect.width / 2;
                      paymentTooltipPosition.y = rect.top - 10;
                    }
                  "
                  @mouseleave="hoveredPaymentMethod = null"
                >
                  <div
                    class="h-full rounded-lg flex items-center justify-between px-2"
                    :style="`width: ${paymentMethods.card.percentage}%; background-color: #fbbf24;`"
                  >
                    <span class="text-xs font-semibold text-white"
                      >{{ paymentMethods.card.count }}건</span
                    >
                    <span class="text-xs font-semibold text-white"
                      >{{ paymentMethods.card.percentage }}%</span
                    >
                  </div>
                  <!-- 바 밖 라벨 (퍼센트가 작을 때) -->
                  <div
                    v-if="paymentMethods.card.percentage < 15"
                    class="absolute left-0 top-0 h-full flex items-center pl-2"
                    :style="`left: ${paymentMethods.card.percentage}%;`"
                  >
                    <span
                      class="text-xs font-semibold text-slate-700 dark:text-slate-300 ml-2"
                      >{{ paymentMethods.card.count }}건 ({{
                        paymentMethods.card.percentage
                      }}%)</span
                    >
                  </div>
                </div>
              </div>
              <div class="flex items-center gap-3">
                <div
                  class="text-sm font-medium text-slate-700 dark:text-slate-300 w-20"
                >
                  기타
                </div>
                <div
                  class="flex-1 h-8 bg-slate-200 dark:bg-slate-700 rounded-lg overflow-hidden relative"
                  @mouseenter="
                    (e) => {
                      hoveredPaymentMethod = {
                        name: '기타',
                        count: paymentMethods.other.count,
                        percentage: paymentMethods.other.percentage,
                      };
                      const rect = e.currentTarget.getBoundingClientRect();
                      paymentTooltipPosition.x = rect.left + rect.width / 2;
                      paymentTooltipPosition.y = rect.top - 10;
                    }
                  "
                  @mouseleave="hoveredPaymentMethod = null"
                >
                  <div
                    class="h-full rounded-lg flex items-center justify-between px-2"
                    :style="`width: ${paymentMethods.other.percentage}%; background-color: #3b82f6;`"
                  >
                    <span class="text-xs font-semibold text-white"
                      >{{ paymentMethods.other.count }}건</span
                    >
                    <span class="text-xs font-semibold text-white"
                      >{{ paymentMethods.other.percentage }}%</span
                    >
                  </div>
                  <!-- 바 밖 라벨 (퍼센트가 작을 때) -->
                  <div
                    v-if="paymentMethods.other.percentage < 15"
                    class="absolute left-0 top-0 h-full flex items-center pl-2"
                    :style="`left: ${paymentMethods.other.percentage}%;`"
                  >
                    <span
                      class="text-xs font-semibold text-slate-700 dark:text-slate-300 ml-2"
                      >{{ paymentMethods.other.count }}건 ({{
                        paymentMethods.other.percentage
                      }}%)</span
                    >
                  </div>
                </div>
              </div>

              <!-- 결제 수단 툴팁 -->
              <div
                v-if="hoveredPaymentMethod"
                class="fixed bg-slate-900 dark:bg-slate-700 text-white text-xs rounded-lg p-3 shadow-lg z-50 pointer-events-none transform -translate-x-1/2 -translate-y-full"
                :style="{
                  left: `${paymentTooltipPosition.x}px`,
                  top: `${paymentTooltipPosition.y}px`,
                }"
              >
                <div class="font-semibold mb-2">
                  {{ hoveredPaymentMethod.name }}
                </div>
                <div class="mb-1">건수: {{ hoveredPaymentMethod.count }}건</div>
                <div class="mb-1">
                  비율: {{ hoveredPaymentMethod.percentage }}%
                </div>
              </div>
            </div>
          </div>
        </section>

        <!-- 사이즈별 비율 -->
        <section>
          <h2 class="text-lg font-semibold mb-4" style="color: #1e293b">
            사이즈별 비율
          </h2>
          <div class="bg-white dark:bg-slate-800 rounded-2xl shadow-sm p-6">
            <div
              class="flex items-center justify-center gap-6 relative"
              @mouseleave="hoveredSize = null"
            >
              <div class="relative w-32 h-32">
                <svg
                  class="w-full h-full transform -rotate-90"
                  viewBox="0 0 100 100"
                >
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
                    :class="
                      hoveredSize?.size === segment.size
                        ? 'opacity-100'
                        : 'opacity-80'
                    "
                    class="transition-all cursor-pointer"
                    @mouseenter="hoveredSize = segment"
                  />
                </svg>
              </div>
              <div class="space-y-2">
                <div
                  v-for="segment in sizeRatio"
                  :key="segment.size"
                  class="flex items-center gap-2 cursor-pointer transition-opacity"
                  :class="
                    hoveredSize?.size === segment.size
                      ? 'opacity-100'
                      : 'opacity-70'
                  "
                  @mouseenter="hoveredSize = segment"
                >
                  <div
                    class="w-4 h-4 rounded-full"
                    :style="{ backgroundColor: segment.color }"
                  ></div>
                  <span class="text-sm text-slate-700 dark:text-slate-300">
                    {{ segment.size }} : {{ segment.percentage }}%
                  </span>
                </div>
              </div>

              <!-- 툴팁 -->
              <div
                v-if="hoveredSize"
                class="absolute top-0 right-0 bg-slate-900 dark:bg-slate-700 text-white text-xs rounded-lg p-3 shadow-lg z-10"
              >
                <div class="font-semibold mb-1">{{ hoveredSize.size }}</div>
                <div>비율: {{ hoveredSize.percentage }}%</div>
                <div>건수: {{ hoveredSize.count }}건</div>
              </div>
            </div>
          </div>
        </section>
      </div>

      <!-- 오른쪽 컬럼 -->
      <div class="space-y-6">
        <!-- 피크타임 분석 -->
        <section>
          <h2 class="text-lg font-semibold mb-4" style="color: #1e293b">
            피크타임 분석
          </h2>
          <div class="bg-white dark:bg-slate-800 rounded-2xl shadow-sm p-6">
            <div class="h-64 relative" @mouseleave="hoveredHour = null">
              <svg
                class="w-full h-full"
                viewBox="0 0 400 200"
                preserveAspectRatio="none"
              >
                <!-- Y축 그리드 (수직선) -->
                <line
                  v-for="i in 5"
                  :key="i"
                  :x1="40"
                  :y1="i * 40"
                  :x2="400"
                  :y2="i * 40"
                  stroke="#e2e8f0"
                  stroke-width="1"
                  class="dark:stroke-slate-700"
                />

                <!-- Y축 라벨 (건수 - 최대값과 최소값만) -->
                <g v-if="peakTimeData.maxValue > 0">
                  <!-- 최대값 -->
                  <text
                    :x="35"
                    :y="25"
                    fill="#64748b"
                    font-size="10"
                    text-anchor="end"
                    class="dark:fill-slate-400 font-semibold"
                  >
                    {{ peakTimeData.maxValue }}건
                  </text>
                  <!-- 최소값 -->
                  <text
                    :x="35"
                    :y="195"
                    fill="#64748b"
                    font-size="10"
                    text-anchor="end"
                    class="dark:fill-slate-400 font-semibold"
                  >
                    0건
                  </text>
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

                <!-- 호버 영역 -->
                <g v-for="(hour, index) in peakTimeData.hours" :key="hour">
                  <rect
                    :x="
                      50 + index * (350 / (peakTimeData.hours.length - 1)) - 15
                    "
                    :y="10"
                    :width="30"
                    height="170"
                    fill="transparent"
                    @mouseenter="
                      (e) => {
                        hoveredHour = {
                          hour,
                          index,
                          store: peakTimeData.storeValues[index],
                          find: peakTimeData.findValues[index],
                        };
                        const rect = e.currentTarget.getBoundingClientRect();
                        tooltipPosition.x = rect.left + rect.width / 2;
                        tooltipPosition.y = rect.top - 10;
                      }
                    "
                    @mouseleave="hoveredHour = null"
                    class="cursor-pointer"
                  />
                </g>

                <!-- 범례 -->
                <g transform="translate(250, 20)">
                  <line
                    x1="0"
                    y1="0"
                    x2="20"
                    y2="0"
                    stroke="#60a5fa"
                    stroke-width="2"
                  />
                  <text
                    x="25"
                    y="5"
                    fill="#64748b"
                    font-size="12"
                    class="dark:fill-slate-400"
                  >
                    기기(store)
                  </text>
                  <line
                    x1="0"
                    y1="15"
                    x2="20"
                    y2="15"
                    stroke="#10b981"
                    stroke-width="2"
                  />
                  <text
                    x="25"
                    y="20"
                    fill="#64748b"
                    font-size="12"
                    class="dark:fill-slate-400"
                  >
                    찾기(find)
                  </text>
                </g>

                <!-- X축 라벨 (시간 - 모든 시간 표시) -->
                <g v-if="peakTimeData.hours.length > 0">
                  <text
                    v-for="(hour, index) in peakTimeData.hours"
                    :key="hour"
                    :x="50 + index * (350 / (peakTimeData.hours.length - 1))"
                    :y="195"
                    fill="#64748b"
                    font-size="10"
                    text-anchor="middle"
                    class="dark:fill-slate-400"
                  >
                    {{ hour }}
                  </text>
                </g>
              </svg>

              <!-- 툴팁 -->
              <div
                v-if="hoveredHour"
                class="fixed bg-slate-900 dark:bg-slate-700 text-white text-xs rounded-lg p-3 shadow-lg z-50 pointer-events-none transform -translate-x-1/2 -translate-y-full"
                :style="{
                  left: `${tooltipPosition.x}px`,
                  top: `${tooltipPosition.y}px`,
                }"
              >
                <div class="font-semibold mb-2">{{ hoveredHour.hour }}시</div>
                <div class="flex items-center gap-2 mb-1">
                  <div class="w-3 h-3 rounded-full bg-blue-400"></div>
                  <span>기기(store): {{ hoveredHour.store }}건</span>
                </div>
                <div class="flex items-center gap-2">
                  <div class="w-3 h-3 rounded-full bg-green-400"></div>
                  <span>찾기(find): {{ hoveredHour.find }}건</span>
                </div>
              </div>
            </div>
          </div>
        </section>

        <!-- 지역별 배송 -->
        <section>
          <h2 class="text-lg font-semibold mb-4" style="color: #1e293b">
            지역별 배송
          </h2>
          <div class="bg-white dark:bg-slate-800 rounded-2xl shadow-sm p-6">
            <!-- 히트맵 스타일 지도 -->
            <div class="flex flex-col items-center gap-2 mb-4">
              <!-- 1행: 서북권, 동북권 -->
              <div class="flex justify-center gap-2 w-full">
                <div
                  v-if="deliveryHeatmap[0]"
                  :class="getHeatmapColor(deliveryHeatmap[0].count || 0)"
                  class="h-20 w-28 min-w-28 max-w-28 flex-shrink-0 rounded-lg flex flex-col items-center justify-center text-slate-900 font-semibold cursor-pointer hover:opacity-80 transition-opacity text-center text-xs px-2 relative"
                  @click="selectRegion(deliveryHeatmap[0])"
                  @mouseenter="
                    (e) => {
                      hoveredRegion = deliveryHeatmap[0];
                      const rect = e.currentTarget.getBoundingClientRect();
                      regionTooltipPosition.x = rect.left + rect.width / 2;
                      regionTooltipPosition.y = rect.top - 10;
                    }
                  "
                  @mouseleave="hoveredRegion = null"
                >
                  <div class="font-bold">{{ deliveryHeatmap[0].name }}</div>
                  <div class="text-[9px] mt-1 opacity-75 leading-tight">
                    {{ getRegionDescription(deliveryHeatmap[0].name) }}
                  </div>
                </div>
                <div
                  v-if="deliveryHeatmap[1]"
                  :class="getHeatmapColor(deliveryHeatmap[1].count || 0)"
                  class="h-20 w-28 min-w-28 max-w-28 flex-shrink-0 rounded-lg flex flex-col items-center justify-center text-slate-900 font-semibold cursor-pointer hover:opacity-80 transition-opacity text-center text-xs px-2 relative"
                  @click="selectRegion(deliveryHeatmap[1])"
                  @mouseenter="
                    (e) => {
                      hoveredRegion = deliveryHeatmap[1];
                      const rect = e.currentTarget.getBoundingClientRect();
                      regionTooltipPosition.x = rect.left + rect.width / 2;
                      regionTooltipPosition.y = rect.top - 10;
                    }
                  "
                  @mouseleave="hoveredRegion = null"
                >
                  <div class="font-bold">{{ deliveryHeatmap[1].name }}</div>
                  <div class="text-[9px] mt-1 opacity-75 leading-tight">
                    {{ getRegionDescription(deliveryHeatmap[1].name) }}
                  </div>
                </div>
              </div>

              <!-- 2행: 서남권, 도심권, 동남권 -->
              <div class="flex justify-center gap-2 w-full">
                <div
                  v-if="deliveryHeatmap[2]"
                  :class="getHeatmapColor(deliveryHeatmap[2].count || 0)"
                  class="h-20 w-28 min-w-28 max-w-28 flex-shrink-0 rounded-lg flex flex-col items-center justify-center text-slate-900 font-semibold cursor-pointer hover:opacity-80 transition-opacity text-center text-xs px-2 relative"
                  @click="selectRegion(deliveryHeatmap[2])"
                  @mouseenter="
                    (e) => {
                      hoveredRegion = deliveryHeatmap[2];
                      const rect = e.currentTarget.getBoundingClientRect();
                      regionTooltipPosition.x = rect.left + rect.width / 2;
                      regionTooltipPosition.y = rect.top - 10;
                    }
                  "
                  @mouseleave="hoveredRegion = null"
                >
                  <div class="font-bold">{{ deliveryHeatmap[2].name }}</div>
                  <div class="text-[9px] mt-1 opacity-75 leading-tight">
                    {{ getRegionDescription(deliveryHeatmap[2].name) }}
                  </div>
                </div>
                <div
                  v-if="deliveryHeatmap[3]"
                  :class="getHeatmapColor(deliveryHeatmap[3].count || 0)"
                  class="h-20 w-28 min-w-28 max-w-28 flex-shrink-0 rounded-lg flex flex-col items-center justify-center text-slate-900 font-semibold cursor-pointer hover:opacity-80 transition-opacity text-center text-xs px-2 relative"
                  @click="selectRegion(deliveryHeatmap[3])"
                  @mouseenter="
                    (e) => {
                      hoveredRegion = deliveryHeatmap[3];
                      const rect = e.currentTarget.getBoundingClientRect();
                      regionTooltipPosition.x = rect.left + rect.width / 2;
                      regionTooltipPosition.y = rect.top - 10;
                    }
                  "
                  @mouseleave="hoveredRegion = null"
                >
                  <div class="font-bold">{{ deliveryHeatmap[3].name }}</div>
                  <div class="text-[9px] mt-1 opacity-75 leading-tight">
                    {{ getRegionDescription(deliveryHeatmap[3].name) }}
                  </div>
                </div>
                <div
                  v-if="deliveryHeatmap[4]"
                  :class="getHeatmapColor(deliveryHeatmap[4].count || 0)"
                  class="h-20 w-28 min-w-28 max-w-28 flex-shrink-0 rounded-lg flex flex-col items-center justify-center text-slate-900 font-semibold cursor-pointer hover:opacity-80 transition-opacity text-center text-xs px-2 relative"
                  @click="selectRegion(deliveryHeatmap[4])"
                  @mouseenter="
                    (e) => {
                      hoveredRegion = deliveryHeatmap[4];
                      const rect = e.currentTarget.getBoundingClientRect();
                      regionTooltipPosition.x = rect.left + rect.width / 2;
                      regionTooltipPosition.y = rect.top - 10;
                    }
                  "
                  @mouseleave="hoveredRegion = null"
                >
                  <div class="font-bold">{{ deliveryHeatmap[4].name }}</div>
                  <div class="text-[9px] mt-1 opacity-75 leading-tight">
                    {{ getRegionDescription(deliveryHeatmap[4].name) }}
                  </div>
                </div>
              </div>

              <!-- 3행: 인천&경기, 지방 -->
              <div class="flex justify-center gap-2 w-full">
                <div
                  v-if="deliveryHeatmap[5]"
                  :class="getHeatmapColor(deliveryHeatmap[5].count || 0)"
                  class="h-20 w-28 min-w-28 max-w-28 flex-shrink-0 rounded-lg flex flex-col items-center justify-center text-slate-900 font-semibold cursor-pointer hover:opacity-80 transition-opacity text-center text-xs px-2 relative"
                  @click="selectRegion(deliveryHeatmap[5])"
                  @mouseenter="
                    (e) => {
                      hoveredRegion = deliveryHeatmap[5];
                      const rect = e.currentTarget.getBoundingClientRect();
                      regionTooltipPosition.x = rect.left + rect.width / 2;
                      regionTooltipPosition.y = rect.top - 10;
                    }
                  "
                  @mouseleave="hoveredRegion = null"
                >
                  <div class="font-bold">{{ deliveryHeatmap[5].name }}</div>
                  <div class="text-[9px] mt-1 opacity-75 leading-tight">
                    {{ getRegionDescription(deliveryHeatmap[5].name) }}
                  </div>
                </div>
                <div
                  v-if="deliveryHeatmap[6]"
                  :class="getHeatmapColor(deliveryHeatmap[6].count || 0)"
                  class="h-20 w-28 min-w-28 max-w-28 flex-shrink-0 rounded-lg flex flex-col items-center justify-center text-slate-900 font-semibold cursor-pointer hover:opacity-80 transition-opacity text-center text-xs px-2 relative"
                  @click="selectRegion(deliveryHeatmap[6])"
                  @mouseenter="
                    (e) => {
                      hoveredRegion = deliveryHeatmap[6];
                      const rect = e.currentTarget.getBoundingClientRect();
                      regionTooltipPosition.x = rect.left + rect.width / 2;
                      regionTooltipPosition.y = rect.top - 10;
                    }
                  "
                  @mouseleave="hoveredRegion = null"
                >
                  <div class="font-bold">{{ deliveryHeatmap[6].name }}</div>
                  <div class="text-[9px] mt-1 opacity-75 leading-tight">
                    {{ getRegionDescription(deliveryHeatmap[6].name) }}
                  </div>
                </div>
              </div>

              <!-- 지역별 배송 툴팁 -->
              <div
                v-if="hoveredRegion"
                class="fixed bg-slate-900 dark:bg-slate-700 text-white text-xs rounded-lg p-3 shadow-lg z-50 pointer-events-none transform -translate-x-1/2 -translate-y-full"
                :style="{
                  left: `${regionTooltipPosition.x}px`,
                  top: `${regionTooltipPosition.y}px`,
                }"
              >
                <div class="font-semibold mb-2">{{ hoveredRegion.name }}</div>
                <div class="mb-1">건수: {{ hoveredRegion.count || 0 }}건</div>
                <div class="mb-1">비율: {{ hoveredRegion.percentage }}%</div>
              </div>
            </div>

            <!-- Top 3 리스트 -->
            <div class="mt-4">
              <div class="text-sm font-semibold mb-3" style="color: #1e293b">
                Top 3
              </div>
              <div class="grid grid-cols-1 md:grid-cols-3 gap-3">
                <div
                  v-for="(region, index) in deliveryRegions"
                  :key="index"
                  class="text-white p-4 rounded-2xl shadow-sm"
                  :style="
                    index === 0
                      ? 'background: linear-gradient(135deg, #007aff 0%, #007aff 100%);'
                      : index === 1
                        ? 'background: linear-gradient(135deg, #10b981 0%, #10b981 100%);'
                        : 'background: linear-gradient(135deg, #f59e0b 0%, #f59e0b 100%);'
                  "
                >
                  <div class="text-xs font-medium opacity-90 mb-1">
                    {{ index + 1 }}위
                  </div>
                  <div class="text-lg font-bold">{{ region.name }}</div>
                  <div class="text-xs mt-1 opacity-90">
                    {{ region.percentage }}%
                  </div>
                </div>
              </div>
            </div>
          </div>
        </section>

        <!-- 인사이트 -->
        <section>
          <h2 class="text-lg font-semibold mb-4" style="color: #1e293b">
            인사이트
          </h2>
          <div class="bg-white dark:bg-slate-800 rounded-2xl shadow-sm p-6">
            <div class="space-y-3">
              <div
                v-for="(insight, index) in insights"
                :key="index"
                class="flex items-start gap-3 p-3 bg-slate-50 dark:bg-slate-900 rounded-lg"
              >
                <div
                  class="w-2 h-2 rounded-full bg-blue-500 mt-2 flex-shrink-0"
                ></div>
                <p class="text-sm text-slate-700 dark:text-slate-300">
                  {{ insight }}
                </p>
              </div>
            </div>
          </div>
        </section>
      </div>
    </div>

    <!-- 액션 버튼 -->
    <div class="flex justify-end gap-4">
      <button
        class="px-6 py-3 bg-white dark:bg-slate-800 text-slate-700 dark:text-slate-300 rounded-lg shadow-sm hover:shadow-md transition-all flex items-center gap-2"
      >
        <i class="fi fi-rr-download"></i>
        PDF 다운로드
      </button>
      <button
        class="px-6 py-3 bg-white dark:bg-slate-800 text-slate-700 dark:text-slate-300 rounded-lg shadow-sm hover:shadow-md transition-all flex items-center gap-2"
      >
        <i class="fi fi-rr-envelope"></i>
        이메일 발송
      </button>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from "vue";
import reservationsData from "@/data/reservations_2025_11.json";

// 전체 예약 데이터
const allReservations = ref([]);

// 날짜 범위 관리 (주간 설정)
const dateRange = ref({
  start: new Date(2025, 10, 17), // 2025-11-17
  end: new Date(2025, 10, 23), // 2025-11-23 (7일 범위)
});

// 달력 표시 여부
const showCalendar = ref(false);

// 달력 호버 상태
const hoveredCalendarDate = ref(null);

// 달력 월 관리
const calendarViewDate = ref(new Date(2025, 10, 1)); // 2025년 11월

const calendarYear = computed(() => calendarViewDate.value.getFullYear());
const calendarMonth = computed(() => calendarViewDate.value.getMonth());

const formatDateRange = (date) => {
  const year = date.getFullYear();
  const month = String(date.getMonth() + 1).padStart(2, "0");
  const day = String(date.getDate()).padStart(2, "0");
  return `${year}-${month}-${day}`;
};

// 주차 레이블 생성 (예: "11월 첫째주")
const getWeekLabel = (date) => {
  const month = date.getMonth() + 1;
  const year = date.getFullYear();

  // 해당 월의 첫 번째 날짜
  const firstDayOfMonth = new Date(year, date.getMonth(), 1);
  const firstDayWeekday = firstDayOfMonth.getDay(); // 0(일) ~ 6(토)

  // 첫 번째 월요일 찾기
  const daysToFirstMonday = firstDayWeekday === 0 ? 6 : firstDayWeekday - 1;
  const firstMonday = new Date(firstDayOfMonth);
  firstMonday.setDate(firstMonday.getDate() + (7 - daysToFirstMonday));

  // 주차 계산
  const daysDiff = Math.floor(
    (date.getTime() - firstMonday.getTime()) / (1000 * 60 * 60 * 24)
  );
  let weekNumber = Math.floor(daysDiff / 7) + 1;

  // weekNumber가 0 이하인 경우 첫째주로 처리
  if (weekNumber <= 0) {
    weekNumber = 1;
  }

  // 주차 한글 표현
  const weekLabels = ["첫째", "둘째", "셋째", "넷째", "다섯째"];
  const weekLabel = weekLabels[weekNumber - 1] || `${weekNumber}째`;

  return `${month}월 ${weekLabel}주`;
};

const prevDateRange = () => {
  const days = 7; // 주간(7일) 범위
  const newStart = new Date(
    dateRange.value.start.getTime() - days * 24 * 60 * 60 * 1000
  );
  const newEnd = new Date(
    dateRange.value.end.getTime() - days * 24 * 60 * 60 * 1000
  );
  // 반응성을 보장하기 위해 새로운 객체 할당
  dateRange.value = {
    start: newStart,
    end: newEnd,
  };
};

const nextDateRange = () => {
  const days = 7; // 주간(7일) 범위
  const newStart = new Date(
    dateRange.value.start.getTime() + days * 24 * 60 * 60 * 1000
  );
  const newEnd = new Date(
    dateRange.value.end.getTime() + days * 24 * 60 * 60 * 1000
  );
  // 반응성을 보장하기 위해 새로운 객체 할당
  dateRange.value = {
    start: newStart,
    end: newEnd,
  };
};

// 달력 날짜 포맷 함수
const fmtKey = (d) => {
  const y = d.getFullYear();
  const m = String(d.getMonth() + 1).padStart(2, "0");
  const day = String(d.getDate()).padStart(2, "0");
  return `${y}-${m}-${day}`;
};

// 달력 날짜 생성
const calendarDays = computed(() => {
  const start = new Date(calendarYear.value, calendarMonth.value, 1);
  const end = new Date(calendarYear.value, calendarMonth.value + 1, 0);
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
    const cur = new Date(calendarYear.value, calendarMonth.value, d);
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

// 달력 월 이동
const prevCalendarMonth = () => {
  calendarViewDate.value = new Date(
    calendarYear.value,
    calendarMonth.value - 1,
    1
  );
};

const nextCalendarMonth = () => {
  calendarViewDate.value = new Date(
    calendarYear.value,
    calendarMonth.value + 1,
    1
  );
};

// 날짜가 현재 선택된 주간 범위에 있는지 확인
const isDateInRange = (date) => {
  const dateStr = fmtKey(date);
  const startStr = formatDateRange(dateRange.value.start);
  const endStr = formatDateRange(dateRange.value.end);
  return dateStr >= startStr && dateStr <= endStr;
};

// 주간 시작일인지 확인 (월요일)
const isWeekStart = (date) => {
  return date.getDay() === 1; // 월요일
};

// 오늘 날짜인지 확인
const isToday = (date) => {
  const today = new Date();
  return (
    date.getDate() === today.getDate() &&
    date.getMonth() === today.getMonth() &&
    date.getFullYear() === today.getFullYear()
  );
};

// 날짜 클릭 시 주간 선택
const selectWeekFromDate = (date) => {
  // 클릭한 날짜가 속한 주간 계산 (월요일~일요일)
  const dayOfWeek = date.getDay();
  const daysToMonday = dayOfWeek === 0 ? 6 : dayOfWeek - 1;

  const weekStart = new Date(date);
  weekStart.setDate(weekStart.getDate() - daysToMonday);

  const weekEnd = new Date(weekStart);
  weekEnd.setDate(weekEnd.getDate() + 6);

  dateRange.value = {
    start: weekStart,
    end: weekEnd,
  };

  showCalendar.value = false;
};

// 날짜 범위에 맞는 예약 필터링
const filteredReservations = computed(() => {
  if (!allReservations.value.length) return [];

  // dateRange.value를 명시적으로 참조하여 반응성 보장
  const range = dateRange.value;
  const startDate = formatDateRange(range.start);
  const endDate = formatDateRange(range.end);

  const filtered = allReservations.value.filter((reservation) => {
    const eventDate = reservation.eventDate;
    return eventDate >= startDate && eventDate <= endDate;
  });

  return filtered;
});

// 이전 기간 예약 필터링 (변화율 계산용)
const previousPeriodReservations = computed(() => {
  if (!allReservations.value.length) return [];

  // dateRange.value를 명시적으로 참조하여 반응성 보장
  const range = dateRange.value;
  const days = 7;
  const prevStart = new Date(
    range.start.getTime() - days * 24 * 60 * 60 * 1000
  );
  const prevEnd = new Date(range.end.getTime() - days * 24 * 60 * 60 * 1000);

  const startDate = formatDateRange(prevStart);
  const endDate = formatDateRange(prevEnd);

  return allReservations.value.filter((reservation) => {
    const eventDate = reservation.eventDate;
    return eventDate >= startDate && eventDate <= endDate;
  });
});

// 주요 지표 계산
const keyMetrics = computed(() => {
  const current = filteredReservations.value;
  const previous = previousPeriodReservations.value;

  // 현재 기간 매출
  const currentRevenue = current.reduce(
    (sum, r) => sum + (r.totalPrice || 0),
    0
  );
  // 이전 기간 매출
  const previousRevenue = previous.reduce(
    (sum, r) => sum + (r.totalPrice || 0),
    0
  );
  // 매출 변화율
  const revenueChange =
    previousRevenue > 0
      ? Math.round(((currentRevenue - previousRevenue) / previousRevenue) * 100)
      : 0;

  // 현재 기간 이용객 수 (고유 고객)
  const currentUsers = new Set(current.map((r) => r.customerPhone)).size;
  // 이전 기간 이용객 수
  const previousUsers = new Set(previous.map((r) => r.customerPhone)).size;
  // 이용객 변화율
  const usersChange =
    previousUsers > 0
      ? Math.round(((currentUsers - previousUsers) / previousUsers) * 100)
      : 0;

  // 이용률 계산 (예약 건수 / 전체 가능한 예약 수) - 간단히 예약 건수로 대체
  const currentUtilization = current.length;
  const previousUtilization = previous.length;
  const utilizationRate =
    currentUtilization > 0 ? ((currentUtilization / 1000) * 100).toFixed(1) : 0;
  const utilizationChange =
    previousUtilization > 0
      ? (
          ((currentUtilization - previousUtilization) / previousUtilization) *
          100
        ).toFixed(1)
      : 0;

  return {
    revenue: currentRevenue,
    revenueChange,
    users: currentUsers,
    usersChange,
    utilizationRate: parseFloat(utilizationRate),
    utilizationChange: parseFloat(utilizationChange),
  };
});

// 추가 지표 계산 (재방문율, 홈 배송 선택률)
const additionalMetrics = computed(() => {
  const current = filteredReservations.value;
  const previous = previousPeriodReservations.value;

  // 재방문율
  const currentReturning = current.filter((r) => r.isReturningCustomer).length;
  const currentRevisitRate =
    current.length > 0
      ? ((currentReturning / current.length) * 100).toFixed(1)
      : 0;
  const previousReturning = previous.filter(
    (r) => r.isReturningCustomer
  ).length;
  const previousRevisitRate =
    previous.length > 0
      ? ((previousReturning / previous.length) * 100).toFixed(1)
      : 0;
  const revisitChange =
    parseFloat(previousRevisitRate) > 0
      ? (
          parseFloat(currentRevisitRate) - parseFloat(previousRevisitRate)
        ).toFixed(1)
      : 0;

  // 홈 배송 선택률
  const currentDelivery = current.filter(
    (r) => r.deliveryType === "배송"
  ).length;
  const currentDeliveryRate =
    current.length > 0
      ? ((currentDelivery / current.length) * 100).toFixed(1)
      : 0;
  const previousDelivery = previous.filter(
    (r) => r.deliveryType === "배송"
  ).length;
  const previousDeliveryRate =
    previous.length > 0
      ? ((previousDelivery / previous.length) * 100).toFixed(1)
      : 0;
  const deliveryChange =
    parseFloat(previousDeliveryRate) > 0
      ? (
          parseFloat(currentDeliveryRate) - parseFloat(previousDeliveryRate)
        ).toFixed(1)
      : 0;

  return {
    revisitRate: parseFloat(currentRevisitRate),
    revisitChange: parseFloat(revisitChange),
    deliveryRate: parseFloat(currentDeliveryRate),
    deliveryChange: parseFloat(deliveryChange),
  };
});

const formatCurrency = (value) => {
  const 만 = Math.floor(value / 10000);
  return `${만}만`;
};

const formatNumber = (value) => {
  return value.toLocaleString("ko-KR");
};

// 호버된 시간대
const hoveredHour = ref(null);
const tooltipPosition = ref({ x: 0, y: 0 });
const hoveredRegion = ref(null);
const hoveredPaymentMethod = ref(null);
const paymentTooltipPosition = ref({ x: 0, y: 0 });
const regionTooltipPosition = ref({ x: 0, y: 0 });

// 호버된 행사 유형
const hoveredEventType = ref(null);

// 피크타임 분석 데이터
const peakTimeData = computed(() => {
  const reservations = filteredReservations.value;

  // 전체 시간대 (0-23시) 또는 데이터가 있는 시간대만
  const allHours = Array.from({ length: 24 }, (_, i) => i);

  // 시간대별 dropoffTime 기반 카운트 (기기)
  const storeValues = allHours.map((hour) => {
    return reservations.filter((r) => {
      if (!r.dropoffTime) return false;
      const dropoffDate = new Date(r.dropoffTime);
      return dropoffDate.getHours() === hour;
    }).length;
  });

  // 시간대별 reservedAt 기반 카운트 (찾기)
  const findValues = allHours.map((hour) => {
    return reservations.filter((r) => {
      if (!r.reservedAt) return false;
      const reservedDate = new Date(r.reservedAt);
      return reservedDate.getHours() === hour;
    }).length;
  });

  // 데이터가 있는 시간대만 필터링
  const hoursWithData = allHours.filter(
    (_, index) => storeValues[index] > 0 || findValues[index] > 0
  );

  // 데이터가 없으면 기본 시간대 사용 (9-23시)
  const hours =
    hoursWithData.length > 0
      ? hoursWithData
      : [9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23];

  // 시간대를 오름차순으로 정렬
  const sortedHours = [...hours].sort((a, b) => a - b);

  // 선택된 시간대의 값만 추출
  const filteredStoreValues = sortedHours.map((hour) => storeValues[hour]);
  const filteredFindValues = sortedHours.map((hour) => findValues[hour]);

  const maxValue = Math.max(...filteredStoreValues, ...filteredFindValues, 1);
  const width = 400;
  const height = 200;

  // 기기 최대/최소값
  const storeMax = Math.max(...filteredStoreValues, 0);
  const storeMin = Math.min(
    ...filteredStoreValues.filter((v) => v > 0),
    storeMax
  );

  // 찾기 최대/최소값
  const findMax = Math.max(...filteredFindValues, 0);
  const findMin = Math.min(...filteredFindValues.filter((v) => v > 0), findMax);

  // Y 좌표 계산
  const storeYValues = filteredStoreValues.map((value) => {
    return height - 20 - (value / maxValue) * (height - 40);
  });

  const findYValues = filteredFindValues.map((value) => {
    return height - 20 - (value / maxValue) * (height - 40);
  });

  // 라인 포인트 생성
  const storePoints = sortedHours
    .map((hour, index) => {
      const x = 50 + (index * (width - 100)) / (sortedHours.length - 1);
      return `${x},${storeYValues[index]}`;
    })
    .join(" ");

  const findPoints = sortedHours
    .map((hour, index) => {
      const x = 50 + (index * (width - 100)) / (sortedHours.length - 1);
      return `${x},${findYValues[index]}`;
    })
    .join(" ");

  return {
    hours: sortedHours,
    storeLine: storePoints,
    findLine: findPoints,
    storeValues: filteredStoreValues,
    findValues: filteredFindValues,
    storeYValues,
    findYValues,
    maxValue,
    storeMax,
    storeMin: storeMin === Infinity ? 0 : storeMin,
    findMax,
    findMin: findMin === Infinity ? 0 : findMin,
  };
});

// 행사 유형별 매출
const eventTypeSales = computed(() => {
  const reservations = filteredReservations.value;
  const typeMap = {};

  reservations.forEach((r) => {
    const type = r.eventType || "기타";
    if (!typeMap[type]) {
      typeMap[type] = { type, value: 0, count: 0 };
    }
    typeMap[type].value += r.totalPrice || 0;
    typeMap[type].count += 1;
  });

  const totalRevenue = Object.values(typeMap).reduce(
    (sum, item) => sum + item.value,
    0
  );

  // 실제 JSON 파일의 행사 유형에 맞는 색상 매핑
  const colors = {
    콘서트: "#3b82f6",
    대학축제: "#10b981",
    스포츠: "#f59e0b",
    페스티벌: "#ec4899",
    기타: "#94a3b8",
  };

  return Object.values(typeMap)
    .map((item) => ({
      type: item.type,
      value: item.value,
      count: item.count,
      percentage:
        totalRevenue > 0 ? Math.round((item.value / totalRevenue) * 100) : 0,
      color: colors[item.type] || colors["기타"],
    }))
    .sort((a, b) => b.value - a.value);
});

const maxEventValue = computed(() => {
  if (eventTypeSales.value.length === 0) return 1;
  return Math.max(...eventTypeSales.value.map((item) => item.value));
});

// 지역별 배송 (Top 3)
const deliveryRegions = computed(() => {
  const reservations = filteredReservations.value.filter(
    (r) => r.deliveryType === "배송"
  );
  const regionMap = {};

  reservations.forEach((r) => {
    const region = r.deliveryRegionGroup || "기타";
    if (!regionMap[region]) {
      regionMap[region] = { name: region, count: 0 };
    }
    regionMap[region].count += 1;
  });

  const total = reservations.length;
  const regions = Object.values(regionMap)
    .map((item) => ({
      name: item.name,
      percentage: total > 0 ? Math.round((item.count / total) * 100) : 0,
      count: item.count,
    }))
    .sort((a, b) => b.count - a.count)
    .slice(0, 3);

  return regions;
});

// 지역별 배송 히트맵 데이터
const deliveryHeatmap = computed(() => {
  const reservations = filteredReservations.value.filter(
    (r) => r.deliveryType === "배송"
  );
  const regionMap = {};

  // JSON 파일의 deliveryRegionGroup을 그대로 사용 (이미 수정된 값)
  reservations.forEach((r) => {
    const region = r.deliveryRegionGroup || "기타";
    if (!regionMap[region]) {
      regionMap[region] = { name: region, count: 0 };
    }
    regionMap[region].count += 1;
  });

  const total = reservations.length;

  // 고정된 순서로 지역 그룹 정의 (레이아웃 순서대로)
  const regionOrder = [
    "서북권", // 1행 첫번째
    "동북권", // 1행 두번째
    "서남권", // 2행 첫번째
    "도심권", // 2행 중앙
    "동남권", // 2행 세번째
    "인천&경기", // 3행 첫번째
    "지방", // 3행 두번째
  ];

  // 순서대로 지역 데이터 생성
  const mappedRegions = regionOrder.map((regionName) => {
    const regionData = regionMap[regionName];
    return {
      name: regionName,
      count: regionData ? regionData.count : 0,
      percentage:
        total > 0 ? Math.round(((regionData?.count || 0) / total) * 100) : 0,
    };
  });

  return mappedRegions;
});

// 3x3 그리드 구조로 매핑 (빈칸 위치: 4, 7)
const heatmapGrid = computed(() => {
  const grid = [];
  const emptyPositions = [4, 7]; // 2행 중앙, 3행 중앙

  for (let i = 0; i < 9; i++) {
    if (emptyPositions.includes(i)) {
      grid.push({ region: null });
    } else {
      const regionIndex = i < 4 ? i : i - 1; // 빈칸 위치를 제외한 인덱스
      grid.push({
        region: deliveryHeatmap.value[regionIndex] || null,
      });
    }
  }

  return grid;
});

// 배송량에 따른 색상 클래스 반환 (동적 계산)
const getHeatmapColor = (count) => {
  if (!deliveryHeatmap.value || deliveryHeatmap.value.length === 0) {
    return "bg-orange-100";
  }

  // 실제 데이터의 최대값과 최소값 계산
  const counts = deliveryHeatmap.value.map((r) => r.count || 0);
  const maxCount = Math.max(...counts, 1);
  const minCount = Math.min(...counts.filter((c) => c > 0), 0);

  // 빈 데이터인 경우
  if (maxCount === 0) return "bg-orange-100";

  // 최대값 기준으로 5단계로 나눔
  const step = (maxCount - minCount) / 5;

  if (count >= maxCount - step) return "bg-orange-900";
  if (count >= maxCount - step * 2) return "bg-orange-700";
  if (count >= maxCount - step * 3) return "bg-orange-500";
  if (count >= maxCount - step * 4) return "bg-orange-300";
  return "bg-orange-100";
};

// 권역 선택 핸들러
const selectRegion = (region) => {
  console.log("선택된 권역:", region);
  // 여기에 상세 정보 모달이나 페이지 이동 로직 추가 가능
};

// 지역 설명 반환 (포함된 구들)
const getRegionDescription = (regionName) => {
  const descriptions = {
    서북권: "마포·용산·영등포·종로·중구·성북",
    동북권: "노원",
    서남권: "동작·관악",
    도심권: "강남·서초·송파·강동",
    동남권: "강동 일부",
    "인천&경기": "인천·경기 전역",
    지방: "부산·대전·대구·광주·기타",
  };
  return descriptions[regionName] || "";
};

// 결제 수단 계산
const paymentMethods = computed(() => {
  const reservations = filteredReservations.value;
  const methodMap = {};

  reservations.forEach((r) => {
    const method = r.paymentMethod || "기타";
    if (!methodMap[method]) {
      methodMap[method] = 0;
    }
    methodMap[method] += 1;
  });

  const total = reservations.length;
  const methods = Object.entries(methodMap).map(([method, count]) => ({
    method,
    count,
    percentage: total > 0 ? Math.round((count / total) * 100) : 0,
  }));

  // 카드와 기타로 그룹화
  const cardMethods = ["카드", "신용카드", "체크카드"];
  const cardCount = methods
    .filter((m) => cardMethods.some((cm) => m.method.includes(cm)))
    .reduce((sum, m) => sum + m.count, 0);
  const otherCount = total - cardCount;

  return {
    card: {
      count: cardCount,
      percentage: total > 0 ? Math.round((cardCount / total) * 100) : 0,
    },
    other: {
      count: otherCount,
      percentage: total > 0 ? Math.round((otherCount / total) * 100) : 0,
    },
  };
});

// 호버된 사이즈
const hoveredSize = ref(null);

// 사이즈별 비율
const sizeRatio = computed(() => {
  const reservations = filteredReservations.value;
  const sizeMap = {};

  reservations.forEach((r) => {
    const size = r.itemSize || "기타";
    if (!sizeMap[size]) {
      sizeMap[size] = 0;
    }
    sizeMap[size] += 1;
  });

  const total = reservations.length;
  const colors = {
    Small: "#ec4899",
    Medium: "#3b82f6",
    Large: "#f59e0b",
    XLarge: "#fbbf24",
    기타: "#94a3b8",
  };

  return Object.entries(sizeMap)
    .map(([size, count]) => ({
      size,
      count,
      percentage: total > 0 ? Math.round((count / total) * 100) : 0,
      color: colors[size] || colors["기타"],
    }))
    .sort((a, b) => b.count - a.count);
});

const getPieOffset = (index) => {
  let offset = 0;
  for (let i = 0; i < index; i++) {
    offset += sizeRatio.value[i].percentage * 2.513;
  }
  return -offset;
};

// 인사이트
const insights = computed(() => {
  const reservations = filteredReservations.value;
  const utilizationRate = keyMetrics.value.utilizationRate;
  const deliveryRate = additionalMetrics.value.deliveryRate;
  const topSize = sizeRatio.value[0];

  const insightList = [];

  if (utilizationRate < 5) {
    insightList.push(
      `이용률 ${utilizationRate}%로 목표(5%) 미달 → 현장 마케팅 강화 필요`
    );
  }

  if (topSize) {
    insightList.push(
      `${topSize.size} 사이즈 집중 (${topSize.percentage}%) → 재고 관리 최적화`
    );
  }

  if (deliveryRate > 15) {
    insightList.push(
      `배송 신청 ${deliveryRate}% (증가 추세) → 배송 인프라 확대 검토`
    );
  }

  if (insightList.length === 0) {
    insightList.push("현재 운영 상태가 양호합니다.");
  }

  return insightList;
});

// 데이터 로드
onMounted(() => {
  if (reservationsData && reservationsData.reservations) {
    allReservations.value = reservationsData.reservations;
  }
});
</script>

<style scoped></style>
