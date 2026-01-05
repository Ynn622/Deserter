import { ref } from 'vue'
import { onAuthChange } from '../services/firebase'

// 用戶狀態管理
export const currentUser = ref(null)
export const isLoggedIn = ref(false)

// 初始化認證狀態監聽
export const initAuth = async () => {
  // 監聽認證狀態變化
  return onAuthChange((user) => {
    if (user) {
      currentUser.value = {
        uid: user.uid,
        name: user.displayName,
        email: user.email,
        avatar: user.photoURL
      }
      isLoggedIn.value = true
    } else {
      currentUser.value = null
      isLoggedIn.value = false
    }
  })
}
