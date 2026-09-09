import { requestClient } from '../request';

// 登录请求参数
export interface LoginParams {
  username: string;
  password: string;
}

// 注册请求参数
export interface RegisterParams {
  username: string;
  password: string;
  confirmPassword: string;
}

// 登录响应数据
export interface LoginResult {
  token: string;
  userId: string;
  username: string;
}

// 认证相关接口
export const authApi = {
  // 登录
  async login(data: LoginParams): Promise<LoginResult> {
    return await requestClient.post('/auth/login', data);
  },

  // 注册
  async register(data: RegisterParams): Promise<void> {
    return await requestClient.post('/auth/register', data);
  },

  // 退出登录
  async logout(): Promise<void> {
    return await requestClient.post('/auth/logout');
  },
};
