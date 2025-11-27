<template>
  <div class="pb-20">
    <!-- 날짜와 날씨 (카드 위) -->
    <div class="mx-4 mt-4 mb-2 flex items-center justify-between">
      <div class="text-lg font-semibold text-gray-900">
        {{ formatDate(new Date()) }}
      </div>
      <!-- 날씨 정보 -->
      <div class="flex items-center gap-2 text-gray-600 text-sm">
        <div class="flex items-center gap-1">
          <span>☁️</span>
          <span>강수 19%</span>
        </div>
        <span>8°C/12°C</span>
      </div>
    </div>

    <!-- 위치 정보 카드 -->
    <div class="bg-white rounded-2xl shadow-sm mx-4 p-5">
      <div class="text-base text-gray-700 mb-3">
        {{ currentLocation }}
      </div>
      <div class="border-t border-dashed border-gray-300 pt-3">
        <div class="text-base text-gray-700">{{ arrivalTime }} 도착 예정</div>
      </div>
    </div>

    <!-- 지도 섹션 -->
    <div class="mx-4 mt-4 relative">
      <div
        class="bg-white rounded-2xl shadow-sm overflow-hidden"
        style="height: 400px"
      >
        <!-- 카카오 맵 영역 -->
        <div id="kakao-map" class="w-full h-full relative">
          <!-- 지도 상단 정보 -->
          <div
            class="absolute top-4 left-4 bg-white/90 backdrop-blur-sm rounded-lg p-2 shadow-md z-10"
          >
            <div class="flex items-center gap-2">
              <i class="fi fi-rr-marker text-blue-600"></i>
              <div class="text-xs text-gray-600">{{ parkingLocationAddress }}</div>
            </div>
          </div>

          <!-- 장소 보기 버튼 -->
          <button
            @click="showParkingModal = true"
            class="absolute top-4 right-4 bg-blue-600 text-white px-4 py-2 rounded-lg shadow-lg hover:bg-blue-700 transition-colors z-10"
          >
            장소 보기
          </button>

          <!-- 네비게이션 아이콘 -->
          <button
            @click="openKakaoNavigation"
            class="absolute bottom-4 right-4 bg-yellow-400 w-12 h-12 rounded-full flex items-center justify-center shadow-lg hover:bg-yellow-500 transition-colors z-10"
          >
            <i class="fi fi-rr-navigation text-blue-600 text-xl"></i>
          </button>
        </div>
      </div>
    </div>

    <!-- 액션 버튼 -->
    <div class="mx-4 mt-4 flex gap-4">
      <!-- 진행 인원 버튼 -->
      <button
        @click="showParticipantsModal = true"
        class="flex-1 bg-white rounded-2xl shadow-sm p-5 text-left transition-shadow"
      >
        <div class="text-sm text-gray-600 mb-2">남은 예약</div>
        <div class="text-2xl font-bold text-blue-600">
          {{ currentParticipants }}/{{ totalCapacity }}
        </div>
      </button>

      <!-- 바코드찍기 버튼 -->
      <button
        @click="showBarcodeModal = true"
        class="flex-1 bg-blue-600 text-white rounded-2xl shadow-sm p-5 font-semibold hover:bg-blue-700 transition-colors"
      >
        바코드찍기
      </button>
    </div>

    <!-- 오늘 일정 카드 -->
    <button
      @click="showScheduleModal = true"
      class="block w-[calc(100%-2rem)] mx-4 mt-4 bg-white rounded-2xl shadow-sm p-5 text-left transition-shadow"
    >
      <div class="flex justify-between items-center mb-4">
        <div class="text-lg font-semibold text-gray-900">오늘 일정</div>
        <div class="text-base font-semibold text-gray-900">
          {{ todaySchedule.title }}
        </div>
      </div>

      <div class="border-t border-dashed border-gray-300 pt-4">

        <div class="space-y-2 text-sm text-gray-600">
          <div class="flex justify-between">
            <span>장소</span>
            <span class="text-gray-900">{{ todaySchedule.location }}</span>
          </div>
          <div class="flex justify-between">
            <span>운영 시간</span>
            <span class="text-gray-900"
              >{{ todaySchedule.operatingHours }} ({{
                todaySchedule.duration
              }})</span
            >
          </div>
          <div class="flex justify-between">
            <span>예약 인원</span>
            <span class="text-gray-900"
              >{{ todaySchedule.bookedCapacity }}/{{
                todaySchedule.totalCapacity
              }}</span
            >
          </div>
          <div class="flex justify-between">
            <span>상태</span>
            <span class="text-gray-900">{{ todaySchedule.status }}</span>
          </div>
        </div>
      </div>
    </button>

    <!-- 진행 인원 모달 -->
    <div
      v-if="showParticipantsModal"
      class="fixed inset-0 z-50 bg-black/50 flex items-end justify-center px-4 pb-4"
      @click.self="showParticipantsModal = false"
    >
      <div
        class="w-full max-w-[480px] bg-white dark:bg-slate-800 rounded-t-3xl max-h-[85vh] overflow-hidden shadow-2xl flex flex-col"
      >
        <div
          class="sticky top-0 bg-white dark:bg-slate-800 border-b border-gray-200 dark:border-gray-700 p-5 flex justify-between items-center rounded-t-3xl z-10"
        >
          <h2 class="text-xl font-bold text-gray-900 dark:text-white">
            진행 인원
          </h2>
          <button
            @click="showParticipantsModal = false"
            class="text-gray-500 dark:text-gray-400 hover:text-gray-700 dark:hover:text-gray-200 text-2xl w-8 h-8 flex items-center justify-center rounded-full hover:bg-gray-100 dark:hover:bg-gray-700 transition-colors"
          >
            ×
          </button>
        </div>
        <div class="flex-1 overflow-hidden flex">
          <!-- 왼쪽: 예약번호 (진행중) -->
          <div
            class="flex-1 border-r border-gray-200 dark:border-gray-700 overflow-y-auto"
          >
            <div class="p-4 bg-blue-50 dark:bg-blue-900/20">
              <h3
                class="text-sm font-semibold text-blue-700 dark:text-blue-300 mb-1"
              >
                예약번호
              </h3>
              <div class="text-xs text-blue-600 dark:text-blue-400">
                {{ pendingReservations.length }}건
              </div>
            </div>
            <div class="p-4 space-y-2">
              <div
                v-for="reservation in pendingReservations"
                :key="reservation.id"
                class="p-3 bg-white dark:bg-slate-700 rounded-lg border border-gray-200 dark:border-gray-600 hover:border-blue-500 dark:hover:border-blue-400 transition-colors cursor-pointer"
                @click="selectedReservationForComplete = reservation"
              >
                <div class="flex items-center justify-between mb-2">
                  <span
                    class="text-sm font-semibold text-gray-900 dark:text-white"
                    >{{ reservation.id }}</span
                  >
                  <button
                    @click.stop="completeReservationFromList(reservation)"
                    class="text-xs bg-blue-600 text-white px-3 py-1 rounded-lg hover:bg-blue-700 transition-colors"
                  >
                    완료
                  </button>
                </div>
                <div class="text-xs text-gray-600 dark:text-gray-400">
                  {{ reservation.customerName }} · {{ reservation.time }}
                </div>
                <div
                  class="text-xs text-gray-500 dark:text-gray-500 mt-1 truncate"
                >
                  {{ reservation.address }}
                </div>
              </div>
              <div
                v-if="pendingReservations.length === 0"
                class="text-center text-gray-400 dark:text-gray-500 text-sm py-8"
              >
                예약이 없습니다
              </div>
            </div>
          </div>

          <!-- 오른쪽: 완료예약번호 -->
          <div class="flex-1 overflow-y-auto">
            <div class="p-4 bg-green-50 dark:bg-green-900/20">
              <h3
                class="text-sm font-semibold text-green-700 dark:text-green-300 mb-1"
              >
                완료예약번호
              </h3>
              <div class="text-xs text-green-600 dark:text-green-400">
                {{ completedReservations.length }}건
              </div>
            </div>
            <div class="p-4 space-y-2">
              <div
                v-for="reservation in completedReservations"
                :key="reservation.id"
                class="p-3 bg-white dark:bg-slate-700 rounded-lg border border-gray-200 dark:border-gray-600"
              >
                <div class="flex items-center justify-between mb-2">
                  <span
                    class="text-sm font-semibold text-gray-900 dark:text-white"
                    >{{ reservation.id }}</span
                  >
                  <span
                    class="text-xs bg-green-100 dark:bg-green-900/50 text-green-700 dark:text-green-300 px-2 py-1 rounded"
                  >
                    완료
                  </span>
                </div>
                <div class="text-xs text-gray-600 dark:text-gray-400">
                  {{ reservation.customerName }} · {{ reservation.time }}
                </div>
                <div
                  class="text-xs text-gray-500 dark:text-gray-500 mt-1 truncate"
                >
                  {{ reservation.address }}
                </div>
              </div>
              <div
                v-if="completedReservations.length === 0"
                class="text-center text-gray-400 dark:text-gray-500 text-sm py-8"
              >
                완료된 예약이 없습니다
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>

    <!-- 바코드찍기 모달 -->
    <div
      v-if="showBarcodeModal"
      class="fixed inset-0 z-50 bg-black flex items-center justify-center"
      @click.self="closeBarcodeModal"
    >
      <div class="w-full max-w-[480px] bg-black mx-auto h-full flex flex-col">
        <div
          class="sticky top-0 bg-gray-900 border-b border-gray-700 p-5 flex justify-between items-center z-10"
        >
          <h2 class="text-xl font-bold text-white">바코드 스캔</h2>
          <button
            @click="closeBarcodeModal"
            class="text-white hover:text-gray-300 text-2xl w-10 h-10 flex items-center justify-center rounded-full hover:bg-white/10 transition-colors"
          >
            ×
          </button>
        </div>

        <!-- 카메라 영역 (위쪽) -->
        <div class="flex-1 relative bg-black">
          <div
            id="barcode-scanner"
            class="w-full h-full flex items-center justify-center"
          ></div>

          <!-- 스캔 안내 -->
          <div
            v-if="!isScanning"
            class="absolute inset-0 flex flex-col items-center justify-center bg-black/60 backdrop-blur-sm"
          >
            <div class="text-white text-center mb-4">
              <div
                class="w-20 h-20 bg-blue-600/20 rounded-full flex items-center justify-center mb-4 mx-auto"
              >
                <i class="fi fi-rr-camera text-4xl text-blue-400"></i>
              </div>
              <p class="text-lg font-semibold mb-2">카메라 권한이 필요합니다</p>
              <p class="text-sm text-gray-300">바코드를 카메라에 맞춰주세요</p>
            </div>
            <button
              @click="startScanning"
              class="bg-blue-600 text-white px-6 py-3 rounded-lg font-semibold hover:bg-blue-700 transition-colors"
            >
              카메라 시작
            </button>
          </div>

          <!-- 스캔 중 표시 -->
          <div
            v-if="isScanning"
            class="absolute top-4 left-1/2 -translate-x-1/2 bg-black/80 backdrop-blur-sm text-white px-5 py-2.5 rounded-full text-sm shadow-lg z-20"
          >
            <div class="flex items-center gap-2">
              <div class="w-2 h-2 bg-blue-400 rounded-full animate-pulse"></div>
              바코드를 스캔 중...
            </div>
          </div>

          <!-- 스캔 결과 -->
          <div
            v-if="scannedCode"
            class="absolute top-4 left-4 right-4 bg-green-500 text-white p-4 rounded-xl shadow-lg z-20"
          >
            <div class="flex items-center gap-2 mb-2">
              <i class="fi fi-rr-check-circle text-xl"></i>
              <p class="font-semibold">스캔 완료!</p>
            </div>
            <p class="text-sm mb-3 bg-white/20 rounded-lg p-2 font-mono">
              {{ scannedCode }}
            </p>
            <button
              @click="handleScannedCode(scannedCode)"
              class="w-full bg-white text-green-600 px-4 py-2 rounded-lg text-sm font-semibold hover:bg-gray-100 transition-colors mb-2"
            >
              조회하기
            </button>
            <button
              @click="resetScan"
              class="w-full bg-white/20 text-white px-4 py-2 rounded-lg text-sm font-semibold hover:bg-white/30 transition-colors"
            >
              다시 스캔
            </button>
          </div>
        </div>

        <!-- 입력 영역 (아래쪽) -->
        <div class="bg-gray-900 border-t border-gray-700 p-5">
          <div class="mb-4">
            <div class="flex gap-2 mb-3">
              <button
                @click="searchType = 'reservation'"
                :class="[
                  'flex-1 py-2.5 rounded-lg font-medium transition-colors',
                  searchType === 'reservation'
                    ? 'bg-blue-600 text-white'
                    : 'bg-gray-800 text-gray-300 hover:bg-gray-700',
                ]"
              >
                예약번호
              </button>
              <button
                @click="searchType = 'phone'"
                :class="[
                  'flex-1 py-2.5 rounded-lg font-medium transition-colors',
                  searchType === 'phone'
                    ? 'bg-blue-600 text-white'
                    : 'bg-gray-800 text-gray-300 hover:bg-gray-700',
                ]"
              >
                전화번호
              </button>
            </div>
            <input
              v-model="searchInput"
              type="text"
              :placeholder="
                searchType === 'reservation'
                  ? '예약번호를 입력하세요'
                  : '전화번호를 입력하세요'
              "
              class="w-full px-4 py-3 bg-gray-800 text-white rounded-lg border border-gray-700 focus:border-blue-500 focus:outline-none"
              @keyup.enter="handleSearch"
            />
          </div>
          <div class="flex gap-3">
            <button
              @click="handleSearch"
              class="flex-1 bg-blue-600 text-white py-3 rounded-lg font-semibold hover:bg-blue-700 transition-colors"
            >
              조회
            </button>
            <button
              v-if="selectedReservation"
              @click="completeReservation"
              class="flex-1 bg-green-600 text-white py-3 rounded-lg font-semibold hover:bg-green-700 transition-colors"
            >
              완료
            </button>
          </div>

          <!-- 조회 결과 -->
          <div
            v-if="selectedReservation"
            class="mt-4 p-4 bg-gray-800 rounded-lg border border-gray-700"
          >
            <div class="text-white text-sm space-y-2">
              <div class="flex justify-between">
                <span class="text-gray-400">예약번호</span>
                <span class="font-semibold">{{ selectedReservation.id }}</span>
              </div>
              <div class="flex justify-between">
                <span class="text-gray-400">고객명</span>
                <span class="font-semibold">{{
                  selectedReservation.customerName
                }}</span>
              </div>
              <div class="flex justify-between">
                <span class="text-gray-400">전화번호</span>
                <span class="font-semibold">{{
                  selectedReservation.phone
                }}</span>
              </div>
              <div class="flex justify-between">
                <span class="text-gray-400">주소</span>
                <span class="font-semibold text-right">{{
                  selectedReservation.address
                }}</span>
              </div>
              <div class="flex justify-between">
                <span class="text-gray-400">하차 시간</span>
                <span class="font-semibold">{{
                  selectedReservation.time
                }}</span>
              </div>
              <div
                v-if="selectedReservation.original"
                class="flex justify-between"
              >
                <span class="text-gray-400">상태</span>
                <span
                  class="font-semibold"
                  :class="
                    selectedReservation.status === 'done'
                      ? 'text-green-400'
                      : 'text-yellow-400'
                  "
                >
                  {{
                    selectedReservation.status === "done" ? "완료" : "진행중"
                  }}
                </span>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>

    <!-- 오늘 일정 모달 -->
    <div
      v-if="showScheduleModal"
      class="fixed inset-0 z-50 bg-black/50 flex items-end justify-center px-4 pb-4"
      @click.self="showScheduleModal = false"
    >
      <div
        class="w-full max-w-[480px] bg-white rounded-t-3xl max-h-[85vh] overflow-y-auto shadow-2xl"
      >
        <div
          class="sticky top-0 bg-white border-b border-gray-200 p-5 flex justify-between items-center rounded-t-3xl"
        >
          <h2 class="text-xl font-bold text-gray-900">오늘 일정</h2>
          <button
            @click="showScheduleModal = false"
            class="text-gray-500 hover:text-gray-700 text-2xl w-8 h-8 flex items-center justify-center rounded-full hover:bg-gray-100 transition-colors"
          >
            ×
          </button>
        </div>
        <div class="p-6">
          <div class="mb-6">
            <div class="text-2xl font-bold text-gray-900 mb-4">
              {{ todaySchedule.title }}
            </div>

            <div class="space-y-3">
              <div
                class="flex justify-between items-center py-3 border-b border-gray-200"
              >
                <span class="text-gray-600 font-medium">장소</span>
                <span class="text-gray-900 font-semibold">{{
                  todaySchedule.location
                }}</span>
              </div>
              <div
                class="flex justify-between items-center py-3 border-b border-gray-200"
              >
                <span class="text-gray-600 font-medium">운영 시간</span>
                <span class="text-gray-900 font-semibold"
                  >{{ todaySchedule.operatingHours }} ({{
                    todaySchedule.duration
                  }})</span
                >
              </div>
              <div
                class="flex justify-between items-center py-3 border-b border-gray-200"
              >
                <span class="text-gray-600 font-medium">예약 인원</span>
                <span class="text-gray-900 font-semibold"
                  >{{ todaySchedule.bookedCapacity }}/{{
                    todaySchedule.totalCapacity
                  }}</span
                >
              </div>
              <div class="flex justify-between items-center py-3">
                <span class="text-gray-600 font-medium">상태</span>
                <span class="text-gray-900 font-semibold">{{
                  todaySchedule.status
                }}</span>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>

    <!-- 주차장 사진 모달 -->
    <div
      v-if="showParkingModal"
      class="fixed inset-0 z-50 bg-black/90 flex items-center justify-center"
      @click.self="showParkingModal = false"
    >
      <div class="w-full max-w-[480px] h-full bg-black mx-auto flex flex-col">
        <!-- 헤더 -->
        <div
          class="sticky top-0 bg-gray-900 border-b border-gray-700 p-5 flex justify-between items-center z-10"
        >
          <h2 class="text-xl font-bold text-white">주차장 위치</h2>
          <button
            @click="showParkingModal = false"
            class="text-white hover:text-gray-300 text-2xl w-10 h-10 flex items-center justify-center rounded-full hover:bg-white/10 transition-colors"
          >
            ×
          </button>
        </div>

        <!-- 이미지 슬라이더 -->
        <div class="flex-1 relative overflow-hidden">
          <div
            class="flex transition-transform duration-300 ease-in-out h-full"
            :style="{ transform: `translateX(-${currentImageIndex * 100}%)` }"
          >
            <div
              v-for="(image, index) in parkingImages"
              :key="index"
              class="w-full h-full flex-shrink-0 flex items-center justify-center"
            >
              <img
                :src="image"
                :alt="`주차장 사진 ${index + 1}`"
                class="w-full h-full object-contain"
              />
            </div>
          </div>

          <!-- 이전 버튼 -->
          <button
            v-if="currentImageIndex > 0"
            @click="prevImage"
            class="absolute left-4 top-1/2 -translate-y-1/2 bg-white/80 hover:bg-white text-gray-800 w-10 h-10 rounded-full flex items-center justify-center shadow-lg transition-colors"
          >
            <i class="fi fi-rr-angle-left text-xl"></i>
          </button>

          <!-- 다음 버튼 -->
          <button
            v-if="currentImageIndex < parkingImages.length - 1"
            @click="nextImage"
            class="absolute right-4 top-1/2 -translate-y-1/2 bg-white/80 hover:bg-white text-gray-800 w-10 h-10 rounded-full flex items-center justify-center shadow-lg transition-colors"
          >
            <i class="fi fi-rr-angle-right text-xl"></i>
          </button>

          <!-- 인디케이터 -->
          <div class="absolute bottom-4 left-1/2 -translate-x-1/2 flex gap-2">
            <div
              v-for="(image, index) in parkingImages"
              :key="index"
              class="w-2 h-2 rounded-full transition-colors"
              :class="currentImageIndex === index ? 'bg-white' : 'bg-white/50'"
            ></div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onUnmounted, watch, onMounted, nextTick, computed } from "vue";
import { Html5Qrcode } from "html5-qrcode";
import reservationsData from "@/data/reservations_2025_12.json";

const currentLocation = ref("잠실실내체육관 남측 주차장");
const arrivalTime = ref("16:30");

// 네비게이션 출발지 (필요에 따라 변경 가능)
const navigationOrigin = ref("서울시 강남구");

const showParticipantsModal = ref(false);
const showBarcodeModal = ref(false);
const showScheduleModal = ref(false);
const showParkingModal = ref(false);

// 바코드 모달 관련
const searchType = ref("reservation"); // 'reservation' or 'phone'
const searchInput = ref("");
const selectedReservation = ref(null);

// 진행인원 모달 관련
// 오늘 날짜 확인
const today = new Date();
today.setHours(0, 0, 0, 0);
const todayStr = `${today.getFullYear()}-${String(today.getMonth() + 1).padStart(2, "0")}-${String(today.getDate()).padStart(2, "0")}`;

// reservations_2025_11.json 데이터를 워커 페이지 형식으로 변환
// 오늘 날짜의 예약만 필터링
const reservations = ref(
  reservationsData.reservations
    .filter((r) => {
      // dropoffTime 또는 eventDate 기준으로 오늘 날짜 확인
      if (r.dropoffTime) {
        const dropoffDate = new Date(r.dropoffTime);
        const dropoffDateStr = `${dropoffDate.getFullYear()}-${String(dropoffDate.getMonth() + 1).padStart(2, "0")}-${String(dropoffDate.getDate()).padStart(2, "0")}`;
        return dropoffDateStr === todayStr;
      }
      if (r.eventDate) {
        return r.eventDate === todayStr;
      }
      return false;
    })
    .map((r) => {
      // dropoffTime에서 시간 추출 (ISO 형식: "2025-11-01T15:33:00Z")
      const dropoffDate = r.dropoffTime ? new Date(r.dropoffTime) : null;
      const timeStr = dropoffDate
        ? `${String(dropoffDate.getHours()).padStart(2, "0")}:${String(dropoffDate.getMinutes()).padStart(2, "0")}`
        : "";

      // 모든 예약을 기본적으로 진행중으로 표시
      // (워커가 확인하고 완료 처리할 수 있도록)
      // 완료 버튼을 눌렀을 때만 완료 상태로 변경됨
      return {
        id: r.id,
        customerName: r.customerName,
        phone: r.customerPhone,
        address: r.deliveryAddress || r.eventVenue || "",
        time: timeStr,
        // 기본적으로 진행중으로 표시 (워커가 완료 처리할 수 있도록)
        status: "scheduled",
        // 원본 데이터도 함께 저장 (추가 정보 표시용)
        original: r,
      };
    })
);
const selectedReservationForComplete = ref(null);

// 진행중 예약 목록
const pendingReservations = computed(() => {
  return reservations.value.filter((r) => r.status !== "done");
});

// 완료된 예약 목록
const completedReservations = computed(() => {
  return reservations.value.filter((r) => r.status === "done");
});

// 진행 인원 수는 완료되지 않은 예약 수로 계산 (오늘 날짜 기준)
const currentParticipants = computed(() => {
  return pendingReservations.value.length;
});

// 전체 용량은 오늘 날짜의 전체 예약 수로 계산
const totalCapacity = computed(() => {
  return reservations.value.length;
});

// 주차장 사진 슬라이더
const parkingImages = ref([
  "https://images.unsplash.com/photo-1506905925346-21bda4d32df4?w=800&h=600&fit=crop",
  "https://images.unsplash.com/photo-1558618666-fcd25c85cd64?w=800&h=600&fit=crop",
  "https://images.unsplash.com/photo-1558618047-3c8c76ca7d13?w=800&h=600&fit=crop",
]);

const currentImageIndex = ref(0);

const nextImage = () => {
  if (currentImageIndex.value < parkingImages.value.length - 1) {
    currentImageIndex.value++;
  }
};

const prevImage = () => {
  if (currentImageIndex.value > 0) {
    currentImageIndex.value--;
  }
};

// 카카오 맵 초기화
onMounted(() => {
  // 카카오 맵 스크립트 로드
  if (!window.kakao || !window.kakao.maps) {
    const kakaoApiKey = import.meta.env.VITE_KAKAO_MAP_API_KEY;
    if (!kakaoApiKey) {
      console.error("카카오맵 API 키가 설정되지 않았습니다. VITE_KAKAO_MAP_API_KEY 환경 변수를 설정해주세요.");
      return;
    }
    const script = document.createElement("script");
    script.src = `//dapi.kakao.com/v2/maps/sdk.js?appkey=${import.meta.env.VITE_KAKAO_MAP_APP_KEY}&autoload=false`;
    script.onload = () => {
      window.kakao.maps.load(() => {
        initMap();
      });
    };
    script.onerror = () => {
      console.error("카카오맵 스크립트를 로드할 수 없습니다.");
    };
    document.head.appendChild(script);
  } else {
    initMap();
  }
});

const initMap = () => {
  nextTick(() => {
    const container = document.getElementById("kakao-map");
    if (!container || !window.kakao?.maps) return;

    const options = {
      center: new window.kakao.maps.LatLng(37.5153, 127.1028), // 잠실실내체육관 좌표
      level: 3,
    };

    const map = new window.kakao.maps.Map(container, options);

    // 마커 생성
    const markerPosition = new window.kakao.maps.LatLng(37.5153, 127.1028);
    const marker = new window.kakao.maps.Marker({
      position: markerPosition,
    });
    marker.setMap(map);

    // 인포윈도우 생성
    const infowindow = new window.kakao.maps.InfoWindow({
      content:
        '<div style="padding:5px;font-size:12px;">잠실실내체육관 남측 주차장</div>',
    });
    infowindow.open(map, marker);
  });
};

// 카카오 네비게이션 열기
const openKakaoNavigation = () => {
  // 목적지 (현재 위치)
  const destination = encodeURIComponent(currentLocation.value);

  // 카카오맵 앱 URL 스킴 (목적지만 지정, 앱에서 출발지 선택 가능)
  // 형식: kakaomap://route?ep=목적지
  const appUrl = `kakaomap://route?ep=${destination}`;

  // 카카오맵 웹 URL (길찾기)
  // 형식: https://map.kakao.com/link/to/목적지
  const webUrl = `https://map.kakao.com/link/to/${destination}`;

  // 앱이 설치되어 있는지 확인 후 앱 열기, 없으면 웹 열기
  const startTime = Date.now();
  const iframe = document.createElement("iframe");
  iframe.style.display = "none";
  iframe.src = appUrl;
  document.body.appendChild(iframe);

  setTimeout(() => {
    document.body.removeChild(iframe);
    const elapsed = Date.now() - startTime;

    // 앱이 열리지 않았으면 웹으로 이동
    if (elapsed < 2000) {
      window.location.href = webUrl;
    }
  }, 500);
};

// 바코드 스캔 관련
const isScanning = ref(false);
const scannedCode = ref("");
let html5QrCode = null;

const startScanning = async () => {
  try {
    isScanning.value = true;
    scannedCode.value = "";

    html5QrCode = new Html5Qrcode("barcode-scanner");

    // 카메라 시작
    await html5QrCode.start(
      { facingMode: "environment" }, // 후면 카메라 우선
      {
        fps: 10,
        qrbox: { width: 250, height: 250 },
        aspectRatio: 1.0,
      },
      (decodedText, decodedResult) => {
        // 바코드 스캔 성공
        scannedCode.value = decodedText;
        stopScanning();
        handleScannedCode(decodedText);
      },
      (errorMessage) => {
        // 스캔 중 에러 (일반적으로 무시)
      }
    );
  } catch (err) {
    console.error("카메라 시작 실패:", err);
    alert("카메라에 접근할 수 없습니다. 권한을 확인해주세요.");
    isScanning.value = false;
  }
};

const stopScanning = async () => {
  if (html5QrCode) {
    try {
      await html5QrCode.stop();
      await html5QrCode.clear();
    } catch (err) {
      console.error("스캔 중지 실패:", err);
    }
    html5QrCode = null;
  }
  isScanning.value = false;
};

const closeBarcodeModal = async () => {
  await stopScanning();
  scannedCode.value = "";
  searchInput.value = "";
  selectedReservation.value = null;
  showBarcodeModal.value = false;
};

const resetScan = async () => {
  scannedCode.value = "";
  await stopScanning();
  await startScanning();
};

// 예약번호/전화번호로 조회
const handleSearch = () => {
  if (!searchInput.value.trim()) return;

  let found = null;
  const searchTerm = searchInput.value.trim();
  if (searchType.value === "reservation") {
    found = reservations.value.find(
      (r) => r.id === searchTerm || r.id.includes(searchTerm)
    );
  } else {
    // 전화번호 검색 (하이픈 제거 후 비교)
    const normalizedSearch = searchTerm.replace(/-/g, "");
    found = reservations.value.find((r) => {
      const normalizedPhone = r.phone ? r.phone.replace(/-/g, "") : "";
      return (
        normalizedPhone.includes(normalizedSearch) ||
        normalizedSearch.includes(normalizedPhone)
      );
    });
  }

  if (found) {
    selectedReservation.value = found;
  } else {
    alert("예약을 찾을 수 없습니다.");
    selectedReservation.value = null;
  }
};

// 바코드 스캔 결과 처리
const handleScannedCode = (code) => {
  console.log("스캔된 바코드:", code);
  // 바코드가 예약번호인 경우
  const found = reservations.value.find((r) => r.id === code);
  if (found) {
    selectedReservation.value = found;
    searchInput.value = code;
  } else {
    alert("예약을 찾을 수 없습니다.");
  }
};

// 완료 처리
const completeReservation = () => {
  if (!selectedReservation.value) return;

  const index = reservations.value.findIndex(
    (r) => r.id === selectedReservation.value.id
  );
  if (index !== -1) {
    reservations.value[index].status = "done";
    alert("완료 처리되었습니다.");
    selectedReservation.value = null;
    searchInput.value = "";
    closeBarcodeModal();
  }
};

// 진행인원 모달에서 완료 처리
const completeReservationFromList = (reservation) => {
  const index = reservations.value.findIndex((r) => r.id === reservation.id);
  if (index !== -1) {
    reservations.value[index].status = "done";
  }
};

// 모달이 열릴 때 카메라 시작, 닫힐 때 정리
watch(showBarcodeModal, async (newVal) => {
  if (newVal) {
    // 모달이 열릴 때 약간의 딜레이 후 카메라 시작
    await nextTick();
    setTimeout(() => {
      startScanning();
    }, 300);
  } else {
    stopScanning();
  }
});

// 컴포넌트 언마운트 시 정리
onUnmounted(() => {
  stopScanning();
});

// 오늘 일정 계산 (오늘 날짜의 예약 데이터 기반)
const todaySchedule = computed(() => {
  const today = new Date();
  today.setHours(0, 0, 0, 0);
  const todayStr = `${today.getFullYear()}-${String(today.getMonth() + 1).padStart(2, "0")}-${String(today.getDate()).padStart(2, "0")}`;

  // 오늘 날짜의 예약들
  const todayReservations = reservations.value.filter((r) => {
    const reservationDate =
      r.original?.eventDate || r.original?.dropoffTime?.split("T")[0];
    return reservationDate === todayStr;
  });

  if (todayReservations.length === 0) {
    return {
      title: "오늘 예정된 행사가 없습니다",
      location: "-",
      operatingHours: "-",
      duration: "-",
      bookedCapacity: 0,
      totalCapacity: 0,
      status: "없음",
    };
  }

  // 행사별로 그룹화
  const eventsByVenue = {};
  todayReservations.forEach((r) => {
    const eventName = r.original?.eventName || "행사";
    const venue = r.original?.eventVenue || "-";
    const key = `${eventName}|${venue}`;

    if (!eventsByVenue[key]) {
      const eventStart = r.original?.eventStartTime
        ? new Date(r.original.eventStartTime)
        : null;
      const eventEnd = r.original?.eventEndTime
        ? new Date(r.original.eventEndTime)
        : null;

      eventsByVenue[key] = {
        eventName,
        venue,
        reservations: [],
        startTime: eventStart,
        endTime: eventEnd,
      };
    }
    eventsByVenue[key].reservations.push(r);
  });

  // 가장 많은 예약이 있는 행사 선택
  let mainEvent = null;
  let maxReservations = 0;
  for (const key in eventsByVenue) {
    if (eventsByVenue[key].reservations.length > maxReservations) {
      maxReservations = eventsByVenue[key].reservations.length;
      mainEvent = eventsByVenue[key];
    }
  }

  if (!mainEvent) {
    return {
      title: "오늘 예정된 행사가 없습니다",
      location: "-",
      operatingHours: "-",
      duration: "-",
      bookedCapacity: 0,
      totalCapacity: 0,
      status: "없음",
    };
  }

  // 시간 포맷팅
  const formatTime = (date) => {
    if (!date) return "";
    return `${String(date.getHours()).padStart(2, "0")}:${String(date.getMinutes()).padStart(2, "0")}`;
  };

  const startTime = formatTime(mainEvent.startTime);
  const endTime = formatTime(mainEvent.endTime);
  const operatingHours =
    startTime && endTime ? `${startTime} ~ ${endTime}` : "-";

  // 지속 시간 계산
  let duration = "-";
  if (mainEvent.startTime && mainEvent.endTime) {
    const diff = mainEvent.endTime.getTime() - mainEvent.startTime.getTime();
    const hours = Math.floor(diff / (1000 * 60 * 60));
    const minutes = Math.floor((diff % (1000 * 60 * 60)) / (1000 * 60));
    if (hours > 0) {
      duration = minutes > 0 ? `${hours}시간 ${minutes}분` : `${hours}시간`;
    } else {
      duration = `${minutes}분`;
    }
  }

  // 상태 결정
  const completedCount = mainEvent.reservations.filter(
    (r) => r.status === "done"
  ).length;
  const status =
    completedCount === 0
      ? "대기"
      : completedCount === mainEvent.reservations.length
        ? "완료"
        : "진행중";

  return {
    title: mainEvent.eventName,
    location: mainEvent.venue,
    operatingHours,
    duration,
    bookedCapacity: mainEvent.reservations.length,
    totalCapacity: mainEvent.reservations.length, // 실제 예약 수를 총 용량으로 표시
    status,
    venue: mainEvent.venue, // 행사 장소 정보 추가
  };
});

// 행사 장소별 주차장 주소 매핑
const venueToParkingAddress = {
  "잠실실내체육관": "서울특별시 > 송파구 > 잠실동",
  "KSPO돔": "서울특별시 > 송파구 > 올림픽로",
  // 다른 행사 장소도 추가 가능
};

// 오늘 일정의 행사 장소에 맞는 주차장 주소
const parkingLocationAddress = computed(() => {
  const venue = todaySchedule.value.venue;
  if (!venue || venue === "-") {
    return "서울특별시 > 송파구 > 잠실동"; // 기본값
  }
  return venueToParkingAddress[venue] || "서울특별시 > 송파구 > 잠실동"; // 매핑이 없으면 기본값
});

const formatDate = (date) => {
  const weekdays = [
    "일요일",
    "월요일",
    "화요일",
    "수요일",
    "목요일",
    "금요일",
    "토요일",
  ];
  const month = date.getMonth() + 1;
  const day = date.getDate();
  const weekday = weekdays[date.getDay()];
  return `${month}월 ${day}일 ${weekday}`;
};
</script>
