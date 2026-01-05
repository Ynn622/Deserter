import { initializeApp } from 'firebase/app'
import { 
  getAuth, 
  GoogleAuthProvider, 
  signInWithPopup,
  signOut, 
  onAuthStateChanged 
} from 'firebase/auth'
import { 
  getFirestore, 
  collection, 
  addDoc, 
  deleteDoc,
  doc,
  query, 
  orderBy, 
  onSnapshot,
  serverTimestamp 
} from 'firebase/firestore'

// Firebase 配置 - 從環境變數讀取
const firebaseConfig = JSON.parse(import.meta.env.VITE_FIREBASE_CONFIG)

// 初始化 Firebase
const app = initializeApp(firebaseConfig)

// 初始化 Firebase Authentication
export const auth = getAuth(app)

// Google 登入提供者
const googleProvider = new GoogleAuthProvider()

// Google 登入 - 統一使用 Popup
export const loginWithGoogle = async () => {
  try {
    const result = await signInWithPopup(auth, googleProvider)
    return {
      success: true,
      user: result.user
    }
  } catch (error) {
    console.error('Google 登入錯誤:', error)
    
    // 處理特定錯誤碼
    let errorMessage = error.message
    let errorCode = null
    
    if (error.code) {
      errorCode = error.code
      switch (error.code) {
        case 'auth/cancelled-popup-request':
          errorMessage = '已有登入視窗開啟中'
          break
        case 'auth/popup-closed-by-user':
          errorMessage = '登入視窗已關閉'
          break
        case 'auth/popup-blocked':
          errorMessage = '彈出視窗被瀏覽器阻擋，請允許彈出視窗'
          break
        case 'auth/network-request-failed':
          errorMessage = '網路連線失敗，請檢查網路連線'
          break
        case 'auth/unauthorized-domain':
          errorMessage = '未授權的網域，請在 Firebase Console 中設定授權網域'
          break
        default:
          errorMessage = error.message
      }
    }
    
    return {
      success: false,
      error: errorMessage,
      errorCode: errorCode
    }
  }
}

// 登出
export const logout = async () => {
  try {
    await signOut(auth)
    return { success: true }
  } catch (error) {
    console.error('登出錯誤:', error)
    return {
      success: false,
      error: error.message
    }
  }
}

// 監聽認證狀態變化
export const onAuthChange = (callback) => {
  return onAuthStateChanged(auth, callback)
}

// 初始化 Firestore
export const db = getFirestore(app)

// === Firestore 評論功能 ===

// 新增評論
export const addComment = async (deserterId, content, user) => {
  try {
    const commentsRef = collection(db, 'comments', deserterId, 'messages')
    const docRef = await addDoc(commentsRef, {
      content: content,
      userId: user.uid,
      userName: user.name,
      userAvatar: user.avatar,
      createdAt: serverTimestamp()
    })
    
    return {
      success: true,
      commentId: docRef.id
    }
  } catch (error) {
    console.error('新增評論錯誤:', error)
    return {
      success: false,
      error: error.message
    }
  }
}

// 刪除評論
export const deleteComment = async (deserterId, commentId) => {
  try {
    const commentRef = doc(db, 'comments', deserterId, 'messages', commentId)
    await deleteDoc(commentRef)
    
    return { success: true }
  } catch (error) {
    console.error('刪除評論錯誤:', error)
    return {
      success: false,
      error: error.message
    }
  }
}

// 監聽評論變化
export const subscribeToComments = (deserterId, callback) => {
  const commentsRef = collection(db, 'comments', deserterId, 'messages')
  const q = query(commentsRef, orderBy('createdAt', 'desc'))
  
  return onSnapshot(q, (snapshot) => {
    const comments = []
    snapshot.forEach((doc) => {
      comments.push({
        id: doc.id,
        ...doc.data()
      })
    })
    callback(comments)
  }, (error) => {
    console.error('監聽評論錯誤:', error)
    callback([])
  })
}
