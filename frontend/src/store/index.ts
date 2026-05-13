import { createPinia } from 'pinia'
import type { App } from 'vue'
import { useAppStore } from './app'
import { useUserStore } from './user'
import { useProjectStore } from './project'
import { useCloudAssetStore } from './cloudAsset'
import { useSOWStore } from './sow'
import { useSLAStore } from './sla'
import { useKnowledgeStore } from './knowledge'

const pinia = createPinia()

// 注册Pinia到Vue应用
export function setupStore(app: App) {
  app.use(pinia)
}

// 导出所有store
export {
  useAppStore,
  useUserStore,
  useProjectStore,
  useCloudAssetStore,
  useSOWStore,
  useSLAStore,
  useKnowledgeStore
}

export default pinia