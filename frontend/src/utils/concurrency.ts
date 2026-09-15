/**
 * 并发控制工具函数
 * 用于限制同时执行的任务数量，适用于批量请求、文件上传等场景
 */

type Task<T> = () => Promise<T>;

/**
 * 限制并发执行任务
 *
 * @param tasks - 任务函数数组，每个函数返回 Promise
 * @param limit - 最大并发数
 * @returns 按输入顺序返回结果数组
 *
 * @example
 * const tasks = urls.map(url => () => fetch(url));
 * const results = await limitConcurrency(tasks, 3); // 最多3个并发
 */
export async function limitConcurrency<T>(
  tasks: Task<T>[],
  limit: number,
): Promise<T[]> {
  const result: T[] = [];
  let next = 0;

  async function worker(): Promise<void> {
    while (next < tasks.length) {
      const index = next++;
      result[index] = await tasks[index]();
    }
  }

  const workers = Array.from(
    { length: Math.min(limit, tasks.length) },
    worker,
  );

  await Promise.all(workers);

  return result;
}
