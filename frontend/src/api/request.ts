import axios from 'axios';
import type { AxiosInstance, AxiosResponse, InternalAxiosRequestConfig } from 'axios';
import { message } from 'antd';
import type { RequestClientConfig, RequestClientOptions, ApiResponse, InterceptorHook } from './types';

class RequestClient {
  private instance: AxiosInstance;
  private requestInterceptors: InterceptorHook<InternalAxiosRequestConfig>[] = [];
  private responseInterceptors: InterceptorHook<AxiosResponse>[] = [];

  constructor(options: RequestClientOptions = {}) {
    const defaultConfig: RequestClientOptions = {
      timeout: 10000,
      headers: {
        'Content-Type': 'application/json;charset=utf-8',
      },
    };

    const mergedConfig = { ...defaultConfig, ...options };
    this.instance = axios.create(mergedConfig);

    this.setupInterceptors();
  }

  private setupInterceptors() {
    // 请求拦截器
    this.instance.interceptors.request.use(
      async (config) => {
        // 执行自定义的请求拦截器
        for (const interceptor of this.requestInterceptors) {
          if (interceptor.fulfilled) {
            config = await interceptor.fulfilled(config);
          }
        }

        // 添加 token（从 zustand store 获取）
        const { useUserStore } = await import('@/stores/userStore');
        const token = useUserStore.getState().token;
        if (token) {
          config.headers.Authorization = `Bearer ${token}`;
        }

        return config;
      },
      (error) => {
        return Promise.reject(error);
      }
    );

    // 响应拦截器
    this.instance.interceptors.response.use(
      async (response) => {
        // 执行自定义的响应拦截器
        for (const interceptor of this.responseInterceptors) {
          if (interceptor.fulfilled) {
            response = await interceptor.fulfilled(response);
          }
        }

        const { data } = response;
        const config = response.config as RequestClientConfig;

        // 如果配置了 returnRaw，直接返回原始响应
        if (config.returnRaw) {
          return response;
        }

        // 处理后端统一响应格式
        if (data && typeof data === 'object' && 'code' in data) {
          const apiResponse = data as ApiResponse;

          if (apiResponse.code === 200) {
            return apiResponse.data;
          }

          // 业务错误
          if (!config.skipErrorHandler) {
            message.error(apiResponse.msg || '请求失败');
          }

          return Promise.reject(new Error(apiResponse.msg || '请求失败'));
        }

        // 非标准格式，直接返回数据
        return data;
      },
      async (error) => {
        // 执行自定义的响应错误拦截器
        for (const interceptor of this.responseInterceptors) {
          if (interceptor.rejected) {
            const result = await interceptor.rejected(error);
            if (result !== undefined) {
              return Promise.reject(result);
            }
          }
        }

        // HTTP 错误处理
        const config = error.config as RequestClientConfig;
        if (error.response) {
          const { status, data } = error.response;

          // 401 未授权
          if (status === 401) {
            message.error('登录已过期，请重新登录');
            localStorage.removeItem('token');
            window.location.href = '/login';
            return Promise.reject(error);
          }

          // 403 禁止访问
          if (status === 403) {
            if (!config.skipErrorHandler) {
              message.error('没有权限访问');
            }
            return Promise.reject(error);
          }

          // 404 未找到
          if (status === 404) {
            if (!config.skipErrorHandler) {
              message.error('请求的资源不存在');
            }
            return Promise.reject(error);
          }

          // 500 服务器错误
          if (status === 500) {
            if (!config.skipErrorHandler) {
              message.error('服务器错误');
            }
            return Promise.reject(error);
          }

          // 其他错误，尝试提取后端消息
          if (data && typeof data === 'object' && 'msg' in data) {
            if (!config.skipErrorHandler) {
              message.error(data.msg || '请求失败');
            }
          } else if (!config.skipErrorHandler) {
            message.error(`请求失败 (${status})`);
          }
        } else if (error.request) {
          // 网络错误
          if (!config.skipErrorHandler) {
            message.error('网络错误，请检查网络连接');
          }
        } else {
          // 其他错误
          if (!config.skipErrorHandler) {
            message.error(error.message || '请求失败');
          }
        }

        return Promise.reject(error);
      }
    );
  }

  // 添加自定义请求拦截器
  addRequestInterceptor(hook: InterceptorHook<InternalAxiosRequestConfig>) {
    this.requestInterceptors.push(hook);
  }

  // 添加自定义响应拦截器
  addResponseInterceptor(hook: InterceptorHook<AxiosResponse>) {
    this.responseInterceptors.push(hook);
  }

  // GET 请求
  get<T>(url: string, config?: RequestClientConfig): Promise<T> {
    return this.instance.get(url, config) as Promise<T>;
  }

  // POST 请求
  post<T>(url: string, data?: unknown, config?: RequestClientConfig): Promise<T> {
    return this.instance.post(url, data, config) as Promise<T>;
  }

  // PUT 请求
  put<T>(url: string, data?: unknown, config?: RequestClientConfig): Promise<T> {
    return this.instance.put(url, data, config) as Promise<T>;
  }

  // DELETE 请求
  delete<T>(url: string, config?: RequestClientConfig): Promise<T> {
    return this.instance.delete(url, config) as Promise<T>;
  }

  // PATCH 请求
  patch<T>(url: string, data?: unknown, config?: RequestClientConfig): Promise<T> {
    return this.instance.patch(url, data, config) as Promise<T>;
  }
}

// 创建默认实例
export const requestClient = new RequestClient({
  baseURL: '/api',
  responseReturn: 'data',
});

export default RequestClient;
