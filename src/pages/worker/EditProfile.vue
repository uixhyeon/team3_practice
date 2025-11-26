<template>
  <div class="pb-20">
    <!-- 헤더 -->
    <div class="bg-white sticky top-0 z-10 border-b border-gray-200">
      <div class="flex items-center justify-between p-4">
        <div class="flex items-center gap-2">
          <button @click="goBack" class="text-gray-600">
            <i class="fi fi-rr-arrow-left text-xl"></i>
          </button>
          <h1 class="text-lg font-semibold text-gray-900">내정보 수정</h1>
        </div>
        <button 
          @click="saveProfile"
          class="text-blue-600 text-sm font-medium"
        >
          저장
        </button>
      </div>
    </div>

    <!-- 프로필 이미지 섹션 -->
    <div class="bg-white rounded-2xl shadow-sm mx-4 mt-4 p-5">
      <div class="flex flex-col items-center">
        <div class="relative">
          <div
            class="w-24 h-24 rounded-full bg-gray-200 flex items-center justify-center overflow-hidden flex-shrink-0 mb-3"
          >
            <img
              v-if="profileData.profileImage"
              :src="profileData.profileImage"
              alt="프로필"
              class="w-full h-full object-cover"
            />
            <span v-else class="text-4xl text-gray-400">👤</span>
          </div>
          <button
            @click="triggerFileInput"
            class="absolute bottom-0 right-0 bg-blue-600 text-white w-8 h-8 rounded-full flex items-center justify-center shadow-lg hover:bg-blue-700 transition-colors"
          >
            <i class="fi fi-rr-camera text-sm"></i>
          </button>
          <input
            ref="fileInput"
            type="file"
            accept="image/*"
            class="hidden"
            @change="handleImageUpload"
          />
        </div>
        <p class="text-sm text-gray-600">프로필 사진 변경</p>
      </div>
    </div>

    <!-- 기본 정보 섹션 -->
    <div class="bg-white rounded-2xl shadow-sm mx-4 mt-4 p-5">
      <h2 class="text-base font-semibold text-gray-900 mb-4">기본 정보</h2>
      
      <div class="space-y-4">
        <!-- 이름 -->
        <div>
          <label class="block text-sm font-medium text-gray-700 mb-2">
            이름
          </label>
          <input
            v-model="profileData.displayName"
            type="text"
            class="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-blue-500 outline-none"
            placeholder="이름을 입력하세요"
          />
        </div>

        <!-- 전화번호 -->
        <div>
          <label class="block text-sm font-medium text-gray-700 mb-2">
            전화번호
          </label>
          <input
            v-model="profileData.phone"
            type="tel"
            class="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-blue-500 outline-none"
            placeholder="010-1234-5678"
          />
        </div>

        <!-- 이메일 -->
        <div>
          <label class="block text-sm font-medium text-gray-700 mb-2">
            이메일
          </label>
          <input
            v-model="profileData.email"
            type="email"
            class="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-blue-500 outline-none"
            placeholder="email@example.com"
          />
        </div>
      </div>
    </div>

    <!-- 계좌 정보 섹션 -->
    <div class="bg-white rounded-2xl shadow-sm mx-4 mt-4 p-5">
      <h2 class="text-base font-semibold text-gray-900 mb-4">계좌 정보</h2>
      
      <div class="space-y-4">
        <!-- 은행 -->
        <div>
          <label class="block text-sm font-medium text-gray-700 mb-2">
            은행
          </label>
          <select
            v-model="profileData.bank"
            class="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-blue-500 outline-none"
          >
            <option value="">은행을 선택하세요</option>
            <option value="kb">국민은행</option>
            <option value="shinhan">신한은행</option>
            <option value="woori">우리은행</option>
            <option value="hana">하나은행</option>
            <option value="nh">농협은행</option>
            <option value="ibk">기업은행</option>
            <option value="kakao">카카오뱅크</option>
            <option value="toss">토스뱅크</option>
          </select>
        </div>

        <!-- 계좌번호 -->
        <div>
          <label class="block text-sm font-medium text-gray-700 mb-2">
            계좌번호
          </label>
          <input
            v-model="profileData.accountNumber"
            type="text"
            class="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-blue-500 outline-none"
            placeholder="계좌번호를 입력하세요"
          />
        </div>

        <!-- 예금주 -->
        <div>
          <label class="block text-sm font-medium text-gray-700 mb-2">
            예금주
          </label>
          <input
            v-model="profileData.accountHolder"
            type="text"
            class="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-blue-500 outline-none"
            placeholder="예금주명을 입력하세요"
          />
        </div>
      </div>
    </div>

    <!-- 비밀번호 변경 섹션 -->
    <div class="bg-white rounded-2xl shadow-sm mx-4 mt-4 p-5 mb-4">
      <h2 class="text-base font-semibold text-gray-900 mb-4">비밀번호 변경</h2>
      
      <div class="space-y-4">
        <!-- 현재 비밀번호 -->
        <div>
          <label class="block text-sm font-medium text-gray-700 mb-2">
            현재 비밀번호
          </label>
          <input
            v-model="passwordData.currentPassword"
            type="password"
            class="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-blue-500 outline-none"
            placeholder="현재 비밀번호를 입력하세요"
          />
        </div>

        <!-- 새 비밀번호 -->
        <div>
          <label class="block text-sm font-medium text-gray-700 mb-2">
            새 비밀번호
          </label>
          <input
            v-model="passwordData.newPassword"
            type="password"
            class="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-blue-500 outline-none"
            placeholder="새 비밀번호를 입력하세요"
          />
        </div>

        <!-- 새 비밀번호 확인 -->
        <div>
          <label class="block text-sm font-medium text-gray-700 mb-2">
            새 비밀번호 확인
          </label>
          <input
            v-model="passwordData.confirmPassword"
            type="password"
            class="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-blue-500 outline-none"
            placeholder="새 비밀번호를 다시 입력하세요"
          />
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref } from "vue";
import { useRouter } from "vue-router";
import { useAuthStore } from "@/stores/auth";

const router = useRouter();
const authStore = useAuthStore();
const fileInput = ref(null);

const profileData = ref({
  displayName: "김기사",
  phone: "010-1234-5678",
  email: "driver@example.com",
  profileImage: null,
  bank: "kb",
  accountNumber: "101-02***-***",
  accountHolder: "김기사",
});

const passwordData = ref({
  currentPassword: "",
  newPassword: "",
  confirmPassword: "",
});

const goBack = () => {
  router.back();
};

const triggerFileInput = () => {
  fileInput.value?.click();
};

const handleImageUpload = (event) => {
  const file = event.target.files[0];
  if (file) {
    const reader = new FileReader();
    reader.onload = (e) => {
      profileData.value.profileImage = e.target.result;
    };
    reader.readAsDataURL(file);
  }
};

const saveProfile = () => {
  // 비밀번호 변경 검증
  if (passwordData.value.newPassword) {
    if (passwordData.value.newPassword !== passwordData.value.confirmPassword) {
      alert("새 비밀번호가 일치하지 않습니다.");
      return;
    }
    if (passwordData.value.newPassword.length < 8) {
      alert("비밀번호는 8자 이상이어야 합니다.");
      return;
    }
  }

  // 프로필 저장 로직 (API 호출 등)
  console.log("프로필 저장:", profileData.value);
  if (passwordData.value.newPassword) {
    console.log("비밀번호 변경:", passwordData.value);
  }

  alert("정보가 저장되었습니다.");
  router.back();
};
</script>

