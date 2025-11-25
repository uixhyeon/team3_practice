<template>
  <div class="pb-20">
    <!-- 날짜 (카드 위) -->
    <div class="mx-4 mt-4 mb-2">
      <div class="text-lg font-semibold text-gray-900">
        {{ formatDate(new Date()) }}
      </div>
    </div>

    <!-- 위치 정보 카드 -->
    <div class="bg-white rounded-2xl shadow-sm mx-4 p-5">
      <div class="text-base text-gray-700 mb-3">
        {{ currentLocation }}
      </div>
      <div class="border-t border-dashed border-gray-300 pt-3">
        <div class="text-sm text-gray-600">{{ arrivalTime }} 도착</div>
      </div>
    </div>

    <!-- 지도 섹션 -->
    <div class="mx-4 mt-4 relative">
      <div
        class="bg-white rounded-2xl shadow-sm overflow-hidden"
        style="height: 400px"
      >
        <!-- 지도 영역 (실제 지도 API 연동 시 여기에 지도 컴포넌트 추가) -->
        <div
          class="w-full h-full bg-gray-200 flex items-center justify-center relative"
        >
          <div class="text-gray-500 text-sm">지도 영역</div>

          <!-- 지도 상단 정보 -->
          <div
            class="absolute top-4 left-4 bg-white/90 backdrop-blur-sm rounded-lg p-2 shadow-md"
          >
            <div class="flex items-center gap-2">
              <i class="fi fi-rr-marker text-blue-600"></i>
              <div class="text-xs">
                <div class="font-semibold">주변</div>
                <div class="text-gray-600">서울특별시 > 송파구 > 잠실동</div>
                <div class="text-gray-500">13°C</div>
              </div>
            </div>
          </div>

          <!-- 장소 보기 버튼 -->
          <button
            class="absolute top-4 right-4 bg-blue-600 text-white px-4 py-2 rounded-lg shadow-lg hover:bg-blue-700 transition-colors"
          >
            장소 보기
          </button>

          <!-- 네비게이션 아이콘 -->
          <div
            class="absolute bottom-4 right-4 bg-yellow-400 w-12 h-12 rounded-full flex items-center justify-center shadow-lg"
          >
            <i class="fi fi-rr-arrow-right text-blue-600 text-xl"></i>
          </div>
        </div>
      </div>
    </div>

    <!-- 액션 버튼 -->
    <div class="mx-4 mt-4 flex gap-4">
      <!-- 진행 인원 버튼 -->
      <button
        @click="showParticipantsModal = true"
        class="flex-1 bg-white rounded-2xl shadow-sm p-5 text-left hover:shadow-md transition-shadow"
      >
        <div class="text-sm text-gray-600 mb-2">진행 인원</div>
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
      class="w-full mx-4 mt-4 bg-white rounded-2xl shadow-sm p-5 text-left hover:shadow-md transition-shadow"
    >
      <div class="text-lg font-semibold text-gray-900 mb-4">오늘 일정</div>

      <div class="border-t border-dashed border-gray-300 pt-4">
        <div class="text-base font-semibold text-gray-900 mb-3">
          {{ todaySchedule.title }}
        </div>

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
      class="fixed inset-0 z-50 bg-black/50 flex items-center justify-center"
      @click.self="showParticipantsModal = false"
    >
      <div
        class="w-full max-w-[480px] bg-white rounded-t-3xl mx-auto max-h-[80vh] overflow-y-auto"
      >
        <div
          class="sticky top-0 bg-white border-b border-gray-200 p-4 flex justify-between items-center rounded-t-3xl"
        >
          <h2 class="text-xl font-bold text-gray-900">진행 인원</h2>
          <button
            @click="showParticipantsModal = false"
            class="text-gray-500 hover:text-gray-700 text-2xl"
          >
            ×
          </button>
        </div>
        <div class="p-6">
          <div class="text-center mb-6">
            <div class="text-5xl font-bold text-blue-600 mb-2">
              {{ currentParticipants }}/{{ totalCapacity }}
            </div>
            <div class="text-gray-600">현재 진행 중인 인원</div>
          </div>
          <!-- 인원 목록 등 추가 정보 표시 가능 -->
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
          class="sticky top-0 bg-black/80 backdrop-blur-sm border-b border-gray-700 p-4 flex justify-between items-center z-10"
        >
          <h2 class="text-xl font-bold text-white">바코드 스캔</h2>
          <button
            @click="closeBarcodeModal"
            class="text-white hover:text-gray-300 text-2xl w-10 h-10 flex items-center justify-center"
          >
            ×
          </button>
        </div>
        <div class="flex-1 flex flex-col items-center justify-center relative">
          <!-- 카메라 영역 -->
          <div
            id="barcode-scanner"
            class="w-full h-full flex items-center justify-center"
          ></div>

          <!-- 스캔 안내 -->
          <div
            v-if="!isScanning"
            class="absolute inset-0 flex flex-col items-center justify-center bg-black/50"
          >
            <div class="text-white text-center mb-4">
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
            class="absolute top-4 left-1/2 -translate-x-1/2 bg-black/70 text-white px-4 py-2 rounded-lg text-sm"
          >
            바코드를 스캔 중...
          </div>

          <!-- 스캔 결과 -->
          <div
            v-if="scannedCode"
            class="absolute bottom-20 left-4 right-4 bg-green-500 text-white p-4 rounded-lg"
          >
            <p class="font-semibold mb-1">스캔 완료!</p>
            <p class="text-sm">{{ scannedCode }}</p>
            <button
              @click="resetScan"
              class="mt-2 bg-white text-green-500 px-4 py-2 rounded text-sm font-semibold hover:bg-gray-100"
            >
              다시 스캔
            </button>
          </div>
        </div>
      </div>
    </div>

    <!-- 오늘 일정 모달 -->
    <div
      v-if="showScheduleModal"
      class="fixed inset-0 z-50 bg-black/50 flex items-center justify-center"
      @click.self="showScheduleModal = false"
    >
      <div
        class="w-full max-w-[480px] bg-white rounded-t-3xl mx-auto max-h-[80vh] overflow-y-auto"
      >
        <div
          class="sticky top-0 bg-white border-b border-gray-200 p-4 flex justify-between items-center rounded-t-3xl"
        >
          <h2 class="text-xl font-bold text-gray-900">오늘 일정</h2>
          <button
            @click="showScheduleModal = false"
            class="text-gray-500 hover:text-gray-700 text-2xl"
          >
            ×
          </button>
        </div>
        <div class="p-6">
          <div class="mb-6">
            <div class="text-2xl font-bold text-gray-900 mb-4">
              {{ todaySchedule.title }}
            </div>

            <div class="space-y-4">
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
  </div>
</template>

<script setup>
import { ref, onUnmounted, watch } from "vue";
import { Html5Qrcode } from "html5-qrcode";

const currentLocation = ref("잠실실내체육관 남측 주차장");
const arrivalTime = ref("16:30분");
const currentParticipants = ref(120);
const totalCapacity = ref(360);

const showParticipantsModal = ref(false);
const showBarcodeModal = ref(false);
const showScheduleModal = ref(false);

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
  showBarcodeModal.value = false;
};

const resetScan = async () => {
  scannedCode.value = "";
  await stopScanning();
  await startScanning();
};

const handleScannedCode = (code) => {
  console.log("스캔된 바코드:", code);
  // 여기에 바코드 처리 로직 추가
  // 예: API 호출, 데이터 저장 등
};

// 모달이 닫힐 때 카메라 정리
watch(showBarcodeModal, (newVal) => {
  if (!newVal) {
    stopScanning();
  }
});

// 컴포넌트 언마운트 시 정리
onUnmounted(() => {
  stopScanning();
});

const todaySchedule = ref({
  title: "아이유 콘서트(잠실)",
  location: "잠실실내체육관",
  operatingHours: "17:00 ~ 23:00",
  duration: "6시간",
  bookedCapacity: 360,
  totalCapacity: 400,
  status: "대기",
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
