const DEFAULT_INTERVAL_MS = 5 * 60 * 1000

const resolveCurrentVersion = (providedVersion) => {
  if (providedVersion?.trim()) {
    return providedVersion
  }

  const envVersion = import.meta.env.VITE_APP_VERSION
  if (typeof envVersion === 'string' && envVersion.trim()) {
    return envVersion
  }

  return 'unknown'
}

const fetchRemoteVersion = async (manifestPath) => {
  try {
    const separator = manifestPath.includes('?') ? '&' : '?'
    const response = await fetch(`${manifestPath}${separator}t=${Date.now()}`, {
      cache: 'no-store',
      headers: {
        'Cache-Control': 'no-cache',
        Pragma: 'no-cache',
      },
    })

    if (!response.ok) {
      return null
    }

    const data = await response.json()
    if (!data.version || typeof data.version !== 'string') {
      return null
    }

    return {
      version: data.version,
      buildTime: data.buildTime,
    }
  } catch {
    return null
  }
}

export const startVersionChecker = ({
  checkIntervalMs = DEFAULT_INTERVAL_MS,
  manifestPath = `${import.meta.env.BASE_URL}version.json`,
  currentVersion,
  onVersionMismatch,
}) => {
  const appVersion = resolveCurrentVersion(currentVersion)
  let stopped = false
  let hasNotified = false
  let isChecking = false

  const check = async () => {
    if (stopped || hasNotified || isChecking) {
      return
    }

    isChecking = true

    try {
      const remote = await fetchRemoteVersion(manifestPath)
      if (!remote || remote.version === appVersion) {
        return
      }

      hasNotified = true
      onVersionMismatch({
        currentVersion: appVersion,
        remoteVersion: remote.version,
        remoteBuildTime: remote.buildTime,
      })
    } finally {
      isChecking = false
    }
  }

  void check()

  const timer = window.setInterval(() => {
    void check()
  }, checkIntervalMs)

  return () => {
    stopped = true
    window.clearInterval(timer)
  }
}
