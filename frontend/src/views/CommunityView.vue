<script setup>
import { ref, computed, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import { useAuthStore } from '@/stores/auth'
import axios from 'axios'
import Sidebar from '@/components/SideBar.vue'

const router = useRouter()
const authStore = useAuthStore()

// 상태
const posts = ref([])
const isLoading = ref(true)
const isSubmitting = ref(false)
const newPostContent = ref('')
const showWriteForm = ref(false)

// 수정 모드
const editingPostId = ref(null)
const editingContent = ref('')

// 댓글 관련
const expandedPostId = ref(null)
const newCommentContent = ref('')
const editingCommentId = ref(null)
const editingCommentContent = ref('')

// 사이드바
const isMenuOpen = ref(false)
const toggleMenu = () => {
  isMenuOpen.value = !isMenuOpen.value
}

// 사용자 정보
const user = computed(() => authStore.user)
const isLoggedIn = computed(() => authStore.isAuthenticated)
const displayName = computed(() => {
  if (user.value?.nickname) return user.value.nickname
  if (user.value?.first_name) {
    return user.value.last_name 
      ? `${user.value.last_name}${user.value.first_name}` 
      : user.value.first_name
  }
  return '사용자'
})

// 게시글 목록 조회
const fetchPosts = async () => {
  try {
    const res = await axios.get('/api/community/posts/')
    posts.value = res.data
  } catch (err) {
    console.error('게시글 로드 실패:', err)
  } finally {
    isLoading.value = false
  }
}

// 게시글 작성
const createPost = async () => {
  if (!newPostContent.value.trim()) {
    alert('내용을 입력해주세요.')
    return
  }

  isSubmitting.value = true
  try {
    const res = await axios.post('/api/community/posts/', {
      content: newPostContent.value
    })
    posts.value.unshift(res.data)
    newPostContent.value = ''
    showWriteForm.value = false
  } catch (err) {
    console.error('게시글 작성 실패:', err)
    alert('게시글 작성에 실패했습니다.')
  } finally {
    isSubmitting.value = false
  }
}

// 게시글 수정 모드 시작
const startEdit = (post) => {
  editingPostId.value = post.id
  editingContent.value = post.content
}

// 게시글 수정 취소
const cancelEdit = () => {
  editingPostId.value = null
  editingContent.value = ''
}

// 게시글 수정 저장
const saveEdit = async (postId) => {
  if (!editingContent.value.trim()) {
    alert('내용을 입력해주세요.')
    return
  }

  try {
    const res = await axios.patch(`/api/community/posts/${postId}/`, {
      content: editingContent.value
    })
    const index = posts.value.findIndex(p => p.id === postId)
    if (index !== -1) {
      posts.value[index] = { ...posts.value[index], ...res.data }
    }
    cancelEdit()
  } catch (err) {
    console.error('게시글 수정 실패:', err)
    alert('게시글 수정에 실패했습니다.')
  }
}

// 게시글 삭제
const deletePost = async (postId) => {
  if (!confirm('정말 삭제하시겠습니까?')) return

  try {
    await axios.delete(`/api/community/posts/${postId}/`)
    posts.value = posts.value.filter(p => p.id !== postId)
  } catch (err) {
    console.error('게시글 삭제 실패:', err)
    alert('게시글 삭제에 실패했습니다.')
  }
}

// 좋아요 토글
const toggleLike = async (post) => {
  if (!isLoggedIn.value) {
    alert('로그인이 필요합니다.')
    router.push('/login')
    return
  }

  try {
    const res = await axios.post(`/api/community/posts/${post.id}/like/`)
    post.is_liked = res.data.is_liked
    post.like_count = res.data.like_count
  } catch (err) {
    console.error('좋아요 실패:', err)
  }
}

// 댓글 펼치기/접기
const toggleComments = async (post) => {
  if (expandedPostId.value === post.id) {
    expandedPostId.value = null
  } else {
    expandedPostId.value = post.id
    // 댓글 목록 조회
    if (!post.comments) {
      try {
        const res = await axios.get(`/api/community/posts/${post.id}/comments/`)
        post.comments = res.data
      } catch (err) {
        console.error('댓글 로드 실패:', err)
      }
    }
  }
}

// 댓글 작성
const createComment = async (post) => {
  if (!newCommentContent.value.trim()) {
    alert('댓글 내용을 입력해주세요.')
    return
  }

  try {
    const res = await axios.post(`/api/community/posts/${post.id}/comments/`, {
      content: newCommentContent.value
    })
    if (!post.comments) post.comments = []
    post.comments.push(res.data)
    post.comment_count++
    newCommentContent.value = ''
  } catch (err) {
    console.error('댓글 작성 실패:', err)
    alert('댓글 작성에 실패했습니다.')
  }
}

// 댓글 수정 모드 시작
const startEditComment = (comment) => {
  editingCommentId.value = comment.id
  editingCommentContent.value = comment.content
}

// 댓글 수정 취소
const cancelEditComment = () => {
  editingCommentId.value = null
  editingCommentContent.value = ''
}

// 댓글 수정 저장
const saveEditComment = async (post, commentId) => {
  if (!editingCommentContent.value.trim()) {
    alert('댓글 내용을 입력해주세요.')
    return
  }

  try {
    const res = await axios.patch(`/api/community/posts/${post.id}/comments/${commentId}/`, {
      content: editingCommentContent.value
    })
    const comment = post.comments.find(c => c.id === commentId)
    if (comment) {
      comment.content = res.data.content
      comment.updated_at = res.data.updated_at
    }
    cancelEditComment()
  } catch (err) {
    console.error('댓글 수정 실패:', err)
    alert('댓글 수정에 실패했습니다.')
  }
}

// 댓글 삭제
const deleteComment = async (post, commentId) => {
  if (!confirm('댓글을 삭제하시겠습니까?')) return

  try {
    await axios.delete(`/api/community/posts/${post.id}/comments/${commentId}/`)
    post.comments = post.comments.filter(c => c.id !== commentId)
    post.comment_count--
  } catch (err) {
    console.error('댓글 삭제 실패:', err)
    alert('댓글 삭제에 실패했습니다.')
  }
}

// 시간 포맷
const formatTime = (dateString) => {
  const date = new Date(dateString)
  const now = new Date()
  const diff = Math.floor((now - date) / 1000)

  if (diff < 60) return '방금 전'
  if (diff < 3600) return `${Math.floor(diff / 60)}분 전`
  if (diff < 86400) return `${Math.floor(diff / 3600)}시간 전`
  if (diff < 604800) return `${Math.floor(diff / 86400)}일 전`
  
  return date.toLocaleDateString('ko-KR', {
    month: 'long',
    day: 'numeric'
  })
}

// 로그아웃
const handleLogout = async () => {
  if (confirm("로그아웃 하시겠습니까?")) {
    await authStore.logOut()
    alert("로그아웃 되었습니다.")
    router.push('/')
  }
}

onMounted(() => {
  fetchPosts()
})
</script>

<template>
  <div class="w-full min-h-screen flex flex-col relative overflow-hidden text-primary font-pretendard transition-colors duration-300">
    
    <!-- 배경 -->
    <div class="absolute inset-0 animate-gradient-bg -z-10"></div>
    <div class="absolute top-1/4 left-1/4 w-[500px] h-[500px] bg-indigo-600/20 rounded-full blur-[120px] -z-10 opacity-0 dark:opacity-60"></div>
    <div class="absolute bottom-1/4 right-1/4 w-[500px] h-[500px] bg-violet-600/20 rounded-full blur-[120px] -z-10 opacity-0 dark:opacity-60"></div>

    <!-- 헤더 -->
    <header class="w-full p-6 md:p-8 flex justify-between items-center z-50 fixed top-0 left-0 bg-transparent">
      <div class="flex items-center gap-4">
        <button @click="toggleMenu" class="p-2 hover:bg-black/5 dark:hover:bg-white/10 rounded-full transition-colors">
          <svg xmlns="http://www.w3.org/2000/svg" class="w-6 h-6 text-primary" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="2">
            <path stroke-linecap="round" stroke-linejoin="round" d="M4 6h16M4 12h16M4 18h16" />
          </svg>
        </button>
        <h2 v-if="isLoggedIn" class="text-lg md:text-xl font-bold tracking-tight text-primary">
          {{ displayName }}님, 안녕하세요.
        </h2>
      </div>

      <div class="flex items-center gap-4">
        <template v-if="isLoggedIn">
          <button @click="handleLogout" class="text-sm text-secondary hover:text-primary transition-colors">
            로그아웃
          </button>
        </template>
        <template v-else>
          <router-link to="/login" class="text-sm text-secondary hover:text-primary transition-colors">
            로그인
          </router-link>
        </template>
      </div>
    </header>

    <!-- 사이드바 -->
    <Sidebar :isOpen="isMenuOpen" @close="isMenuOpen = false" />

    <!-- 메인 컨텐츠 -->
    <main class="flex-1 w-full max-w-2xl mx-auto px-4 pt-28 pb-24 z-10">
      
      <!-- 타이틀 -->
      <div class="mb-6">
        <h1 class="text-2xl font-black text-primary flex items-center gap-2">
          🔥 디딤 피드
        </h1>
        <p class="text-secondary text-sm mt-1">사용자들과 금융에 대해 자유롭게 소통해보세요</p>
      </div>

      <!-- 글쓰기 폼 -->
      <div v-if="isLoggedIn" class="glass-panel rounded-2xl p-4 mb-6">
        <div v-if="!showWriteForm" @click="showWriteForm = true" class="flex items-center gap-3 cursor-pointer">
          <div class="w-10 h-10 rounded-full bg-indigo-600 flex items-center justify-center text-white font-bold">
            {{ user?.display_initial || '?' }}
          </div>
          <div class="flex-1 py-3 px-4 bg-gray-100 dark:bg-white/5 rounded-full text-secondary text-sm">
            무슨 생각을 하고 계신가요?
          </div>
        </div>

        <div v-else class="space-y-3">
          <div class="flex items-start gap-3">
            <div class="w-10 h-10 rounded-full bg-indigo-600 flex items-center justify-center text-white font-bold shrink-0">
              {{ user?.display_initial || '?' }}
            </div>
            <textarea
              v-model="newPostContent"
              rows="3"
              placeholder="무슨 생각을 하고 계신가요?"
              class="flex-1 p-3 bg-gray-100 dark:bg-white/5 rounded-xl text-primary placeholder-gray-400 resize-none focus:outline-none focus:ring-2 focus:ring-indigo-500"
            ></textarea>
          </div>
          <div class="flex justify-end gap-2">
            <button
              @click="showWriteForm = false; newPostContent = ''"
              class="px-4 py-2 text-sm text-secondary hover:text-primary transition-colors"
            >
              취소
            </button>
            <button
              @click="createPost"
              :disabled="isSubmitting || !newPostContent.trim()"
              class="px-6 py-2 bg-indigo-600 hover:bg-indigo-700 disabled:bg-indigo-400 text-white text-sm font-bold rounded-full transition-colors"
            >
              {{ isSubmitting ? '게시 중...' : '게시하기' }}
            </button>
          </div>
        </div>
      </div>

      <!-- 로그인 유도 -->
      <div v-else class="glass-panel rounded-2xl p-6 mb-6 text-center">
        <p class="text-secondary mb-3">로그인하고 커뮤니티에 참여해보세요!</p>
        <router-link to="/login" class="inline-block px-6 py-2 bg-indigo-600 hover:bg-indigo-700 text-white text-sm font-bold rounded-full transition-colors">
          로그인하기
        </router-link>
      </div>

      <!-- 로딩 -->
      <div v-if="isLoading" class="text-center py-12">
        <div class="animate-spin w-8 h-8 border-2 border-indigo-500 border-t-transparent rounded-full mx-auto"></div>
        <p class="text-secondary mt-4">로딩 중...</p>
      </div>

      <!-- 게시글 목록 -->
      <div v-else class="space-y-4">
        <div v-if="posts.length === 0" class="text-center py-12 text-secondary">
          아직 게시글이 없습니다. 첫 번째 글을 작성해보세요!
        </div>

        <div
          v-for="post in posts"
          :key="post.id"
          class="glass-panel rounded-2xl p-5 transition-all hover:shadow-lg"
        >
          <!-- 작성자 정보 -->
          <div class="flex items-center justify-between mb-3">
            <div class="flex items-center gap-3">
              <div class="w-10 h-10 rounded-full bg-indigo-600 flex items-center justify-center overflow-hidden">
                <img
                  v-if="post.author.profile_image_url"
                  :src="post.author.profile_image_url"
                  alt="프로필"
                  class="w-full h-full object-cover"
                >
                <span v-else class="text-white font-bold">{{ post.author.display_initial }}</span>
              </div>
              <div>
                <p class="font-bold text-primary text-sm">{{ post.author.nickname || '익명' }}</p>
                <p class="text-xs text-secondary">{{ formatTime(post.created_at) }}</p>
              </div>
            </div>

            <!-- 수정/삭제 버튼 -->
            <div v-if="post.is_owner" class="flex items-center gap-2">
              <button
                @click="startEdit(post)"
                class="text-xs text-secondary hover:text-indigo-500 transition-colors"
              >
                수정
              </button>
              <button
                @click="deletePost(post.id)"
                class="text-xs text-secondary hover:text-red-500 transition-colors"
              >
                삭제
              </button>
            </div>
          </div>

          <!-- 글 내용 (수정 모드) -->
          <div v-if="editingPostId === post.id" class="mb-4">
            <textarea
              v-model="editingContent"
              rows="3"
              class="w-full p-3 bg-gray-100 dark:bg-white/5 rounded-xl text-primary resize-none focus:outline-none focus:ring-2 focus:ring-indigo-500"
            ></textarea>
            <div class="flex justify-end gap-2 mt-2">
              <button @click="cancelEdit" class="px-3 py-1 text-sm text-secondary hover:text-primary">
                취소
              </button>
              <button
                @click="saveEdit(post.id)"
                class="px-4 py-1 bg-indigo-600 text-white text-sm rounded-full hover:bg-indigo-700"
              >
                저장
              </button>
            </div>
          </div>

          <!-- 글 내용 (일반 모드) -->
          <p v-else class="text-primary mb-4 whitespace-pre-wrap">{{ post.content }}</p>

          <!-- 좋아요, 댓글 버튼 -->
          <div class="flex items-center gap-4 pt-3 border-t border-gray-100 dark:border-white/5">
            <button
              @click="toggleLike(post)"
              :class="[
                'flex items-center gap-1.5 text-sm transition-colors',
                post.is_liked ? 'text-rose-500' : 'text-secondary hover:text-rose-500'
              ]"
            >
              <svg xmlns="http://www.w3.org/2000/svg" class="w-5 h-5" :fill="post.is_liked ? 'currentColor' : 'none'" viewBox="0 0 24 24" stroke="currentColor" stroke-width="2">
                <path stroke-linecap="round" stroke-linejoin="round" d="M4.318 6.318a4.5 4.5 0 000 6.364L12 20.364l7.682-7.682a4.5 4.5 0 00-6.364-6.364L12 7.636l-1.318-1.318a4.5 4.5 0 00-6.364 0z" />
              </svg>
              {{ post.like_count }}
            </button>

            <button
              @click="toggleComments(post)"
              class="flex items-center gap-1.5 text-sm text-secondary hover:text-indigo-500 transition-colors"
            >
              <svg xmlns="http://www.w3.org/2000/svg" class="w-5 h-5" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="2">
                <path stroke-linecap="round" stroke-linejoin="round" d="M8 12h.01M12 12h.01M16 12h.01M21 12c0 4.418-4.03 8-9 8a9.863 9.863 0 01-4.255-.949L3 20l1.395-3.72C3.512 15.042 3 13.574 3 12c0-4.418 4.03-8 9-8s9 3.582 9 8z" />
              </svg>
              {{ post.comment_count }}
            </button>
          </div>

          <!-- 댓글 섹션 -->
          <div v-if="expandedPostId === post.id" class="mt-4 pt-4 border-t border-gray-100 dark:border-white/5">
            
            <!-- 댓글 목록 -->
            <div v-if="post.comments && post.comments.length > 0" class="space-y-3 mb-4">
              <div
                v-for="comment in post.comments"
                :key="comment.id"
                class="flex gap-3"
              >
                <div class="w-8 h-8 rounded-full bg-gray-300 dark:bg-gray-600 flex items-center justify-center shrink-0 overflow-hidden">
                  <img
                    v-if="comment.author.profile_image_url"
                    :src="comment.author.profile_image_url"
                    alt="프로필"
                    class="w-full h-full object-cover"
                  >
                  <span v-else class="text-xs font-bold text-white">{{ comment.author.display_initial }}</span>
                </div>
                <div class="flex-1">
                  <div class="bg-gray-100 dark:bg-white/5 rounded-xl px-3 py-2">
                    <p class="text-xs font-bold text-primary">{{ comment.author.nickname || '익명' }}</p>
                    
                    <!-- 댓글 수정 모드 -->
                    <div v-if="editingCommentId === comment.id">
                      <textarea
                        v-model="editingCommentContent"
                        rows="2"
                        class="w-full mt-1 p-2 bg-white dark:bg-slate-800 rounded-lg text-sm text-primary resize-none focus:outline-none"
                      ></textarea>
                      <div class="flex justify-end gap-2 mt-1">
                        <button @click="cancelEditComment" class="text-xs text-secondary">취소</button>
                        <button @click="saveEditComment(post, comment.id)" class="text-xs text-indigo-500">저장</button>
                      </div>
                    </div>
                    <p v-else class="text-sm text-primary mt-0.5">{{ comment.content }}</p>
                  </div>
                  <div class="flex items-center gap-3 mt-1 ml-1">
                    <span class="text-xs text-secondary">{{ formatTime(comment.created_at) }}</span>
                    <template v-if="comment.is_owner">
                      <button @click="startEditComment(comment)" class="text-xs text-secondary hover:text-indigo-500">수정</button>
                      <button @click="deleteComment(post, comment.id)" class="text-xs text-secondary hover:text-red-500">삭제</button>
                    </template>
                  </div>
                </div>
              </div>
            </div>

            <!-- 댓글 작성 -->
            <div v-if="isLoggedIn" class="flex gap-2">
              <input
                v-model="newCommentContent"
                type="text"
                placeholder="댓글을 입력하세요..."
                class="flex-1 px-4 py-2 bg-gray-100 dark:bg-white/5 rounded-full text-sm text-primary placeholder-gray-400 focus:outline-none focus:ring-2 focus:ring-indigo-500"
                @keydown.enter="createComment(post)"
              >
              <button
                @click="createComment(post)"
                :disabled="!newCommentContent.trim()"
                class="px-4 py-2 bg-indigo-600 hover:bg-indigo-700 disabled:bg-indigo-400 text-white text-sm font-bold rounded-full transition-colors"
              >
                등록
              </button>
            </div>
            <p v-else class="text-sm text-secondary text-center">
              <router-link to="/login" class="text-indigo-500 hover:underline">로그인</router-link>하고 댓글을 작성해보세요
            </p>
          </div>
        </div>
      </div>
    </main>

    <!-- 플로팅 버튼 -->
    <div class="fixed bottom-8 right-8 z-50">
      <button class="w-14 h-14 bg-indigo-600 hover:bg-indigo-500 rounded-full flex items-center justify-center shadow-2xl hover:-translate-y-1 transition-all duration-300">
        <svg xmlns="http://www.w3.org/2000/svg" class="w-7 h-7 text-white" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="2">
          <path d="M21 15a2 2 0 0 1-2 2H7l-4 4V5a2 2 0 0 1 2-2h14a2 2 0 0 1 2 2z"/>
        </svg>
      </button>
    </div>
  </div>
</template>