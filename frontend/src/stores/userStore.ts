import { create } from 'zustand'

interface UserInfo {
  id: number
  username: string
  email: string
}

interface UserState {
  token: string
  userInfo: UserInfo | null
  setToken: (token: string) => void
  setUserInfo: (info: UserInfo) => void
  logout: () => void
}

export const useUserStore = create<UserState>((set) => ({
  token: localStorage.getItem('token') || '',
  userInfo: null,
  setToken: (token: string) => {
    localStorage.setItem('token', token)
    set({ token })
  },
  setUserInfo: (info: UserInfo) => {
    set({ userInfo: info })
  },
  logout: () => {
    localStorage.removeItem('token')
    set({ token: '', userInfo: null })
  },
}))
