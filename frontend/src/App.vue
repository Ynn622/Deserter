<script setup>
import { onBeforeUnmount, onMounted } from 'vue'
import Swal from 'sweetalert2'
import { startVersionChecker } from './utilities/versionChecker'

const AUTO_RELOAD_DELAY_MS = 10 * 1000
const AUTO_RELOAD_DELAY_SEC = AUTO_RELOAD_DELAY_MS / 1000

let stopVersionCheck = null
let reloadTimer = null

const reloadPage = () => {
  if (reloadTimer) {
    window.clearTimeout(reloadTimer)
    reloadTimer = null
  }

  window.location.reload()
}

onMounted(() => {
  if (!import.meta.env.PROD) {
    return
  }

  stopVersionCheck = startVersionChecker({
    onVersionMismatch: ({ remoteVersion }) => {
      void Swal.fire({
        toast: true,
        position: 'top-end',
        icon: 'info',
        title: '偵測到網站新版本',
        text: `${AUTO_RELOAD_DELAY_SEC} 秒後將自動更新（${remoteVersion}）`,
        timer: AUTO_RELOAD_DELAY_MS,
        timerProgressBar: true,
        showConfirmButton: true,
        confirmButtonText: '立即更新',
      }).then((result) => {
        if (result.isConfirmed) {
          reloadPage()
        }
      })

      reloadTimer = window.setTimeout(reloadPage, AUTO_RELOAD_DELAY_MS)
    },
  })
})

onBeforeUnmount(() => {
  stopVersionCheck?.()
  stopVersionCheck = null

  if (reloadTimer) {
    window.clearTimeout(reloadTimer)
    reloadTimer = null
  }
})
</script>

<template>
  <router-view />
</template>

<style>
/* 全局樣式 */
</style>
