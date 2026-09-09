import type { AxiosRequestConfig, AxiosResponse } from 'axios';

// 请求配置扩展
export interface RequestClientConfig extends AxiosRequestConfig {
  // 是否跳过响应拦截器的错误提示
  skipErrorHandler?: boolean;
  // 是否返回原始响应数据
  returnRaw?: boolean;
}

// 请求客户端配置
export interface RequestClientOptions extends AxiosRequestConfig {
  // 默认超时时间
  timeout?: number;
  // 响应数据返回格式
  responseReturn?: 'data' | 'raw';
}

// 后端统一响应格式
export interface ApiResponse<T = unknown> {
  code: number;
  data: T;
  msg: string;
}

// 分页请求参数
export interface PaginationParams {
  current: number;
  pageSize: number;
}

// 分页响应数据
export interface PaginationData<T> {
  list: T[];
  total: number;
  current: number;
  pageSize: number;
}

// 拦截器钩子
export interface InterceptorHook<T = AxiosResponse> {
  fulfilled?: (value: T) => T | Promise<T>;
  rejected?: (error: unknown) => unknown;
}
