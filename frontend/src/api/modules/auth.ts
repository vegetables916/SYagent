import { requestClient } from '../request';

// 登录请求参数
export interface LoginParams {
  username: string;
  password: string;
}

// 注册请求参数
export interface RegisterParams {
  username: string;
  email: string;
  password: string;
}

// 登录响应数据（匹配后端 TokenResponse）
export interface LoginResult {
  access_token: string;
  token_type: string;
}

// 认证相关接口
export const authApi = {
  // 登录
  async login(data: LoginParams): Promise<LoginResult> {
    return await requestClient.post('/v1/auth/login', data);
  },

  // 注册
  async register(data: RegisterParams): Promise<{ message: string }> {
    return await requestClient.post('/v1/auth/register', data);
  },

  // 获取当前用户信息
  async getMe(): Promise<{ id: number; username: string; email: string }> {
    return await requestClient.get('/v1/auth/me');
  },
};
