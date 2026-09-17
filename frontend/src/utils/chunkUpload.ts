/**
 * 分片上传工具函数（完整版）
 * 包含：文件切片、MD5计算、并发控制、断点续传、进度回调
 */

import SparkMD5 from 'spark-md5'
import { requestClient } from '@/api/request'

// ============ 配置 ============
const CHUNK_SIZE = 2 * 1024 * 1024 // 2MB 分片大小
const CONCURRENCY = 3 // 并发上传数

// ============ 类型定义 ============
export interface ChunkUploadOptions {
  file: File
  onProgress?: (progress: number) => void
  onChunkComplete?: (chunkIndex: number, totalChunks: number) => void
}

export interface UploadResult {
  fileId: string
  fileName: string
  fileSize: number
  fileMd5: string
  fileUrl: string
  totalChunks: number
}

interface InitUploadResponse {
  fileId: string
  uploadedChunks: number[] // 已上传的分片索引
}

interface CompleteUploadResponse {
  fileUrl: string
}

// ============ 核心函数 ============

/**
 * 计算文件 MD5
 */
async function calculateFileMd5(file: File): Promise<string> {
  return new Promise((resolve, reject) => {
    const blobSlice = File.prototype.slice
    const chunkSize = 2 * 1024 * 1024 // 2MB chunks for MD5 calculation
    const chunks = Math.ceil(file.size / chunkSize)
    let currentChunk = 0
    const spark = new SparkMD5.ArrayBuffer()
    const reader = new FileReader()

    reader.onload = (e) => {
      spark.append(e.target?.result as ArrayBuffer)
      currentChunk++

      if (currentChunk < chunks) {
        loadNext()
      } else {
        resolve(spark.end())
      }
    }

    reader.onerror = () => {
      reject(new Error('文件读取失败'))
    }

    const loadNext = () => {
      const start = currentChunk * chunkSize
      const end = Math.min(start + chunkSize, file.size)
      reader.readAsArrayBuffer(blobSlice.call(file, start, end))
    }

    loadNext()
  })
}

/**
 * 初始化上传（调用后端接口）
 * 后端检查文件是否已存在，返回已上传的分片列表（用于断点续传）
 */
async function initUpload(
  fileName: string,
  fileSize: number,
  fileMd5: string,
  totalChunks: number,
): Promise<InitUploadResponse> {
  const response = await requestClient.post<InitUploadResponse>('/v1/files/init', {
    fileName,
    fileSize,
    fileMd5,
    totalChunks,
  })
  return response as InitUploadResponse
}

/**
 * 上传单个分片（调用后端接口）
 */
async function uploadChunk(
  fileId: string,
  chunkIndex: number,
  chunk: Blob,
): Promise<{ etag: string }> {
  const formData = new FormData()
  formData.append('chunk', chunk)
  formData.append('chunkIndex', chunkIndex.toString())

  const response = await requestClient.post<{ etag: string }>(
    `/v1/files/${fileId}/chunk`,
    formData,
    {
      headers: { 'Content-Type': 'multipart/form-data' },
    },
  )
  return response as { etag: string }
}

/**
 * 完成上传（调用后端接口，合并分片）
 */
async function completeUpload(fileId: string): Promise<CompleteUploadResponse> {
  const response = await requestClient.post<CompleteUploadResponse>(`/v1/files/${fileId}/complete`)
  return response as CompleteUploadResponse
}

/**
 * 并发控制执行任务
 */
async function runWithConcurrency<T>(
  tasks: Array<() => Promise<T>>,
  limit: number,
): Promise<T[]> {
  const results: T[] = []
  let nextIndex = 0

  async function worker(): Promise<void> {
    while (nextIndex < tasks.length) {
      const index = nextIndex++
      results[index] = await tasks[index]()
    }
  }

  const workers = Array.from({ length: Math.min(limit, tasks.length) }, worker)
  await Promise.all(workers)

  return results
}

/**
 * 分片上传主函数（支持断点续传）
 */
export async function chunkUpload(options: ChunkUploadOptions): Promise<UploadResult> {
  const { file, onProgress, onChunkComplete } = options

  // 1. 计算文件 MD5
  const fileMd5 = await calculateFileMd5(file)

  // 2. 计算分片数量
  const totalChunks = Math.ceil(file.size / CHUNK_SIZE)

  // 3. 初始化上传（获取已上传的分片列表）
  const { fileId, uploadedChunks } = await initUpload(file.name, file.size, fileMd5, totalChunks)

  // 4. 找出需要上传的分片
  const chunksToUpload = Array.from({ length: totalChunks }, (_, i) => i).filter(
    (i) => !uploadedChunks.includes(i),
  )

  // 5. 如果没有需要上传的分片，直接完成
  if (chunksToUpload.length === 0) {
    const { fileUrl } = await completeUpload(fileId)
    return {
      fileId,
      fileName: file.name,
      fileSize: file.size,
      fileMd5,
      fileUrl,
      totalChunks,
    }
  }

  // 6. 准备分片上传任务
  let completedChunks = uploadedChunks.length
  const partEtags: { PartNumber: number; ETag: string }[] = []

  const uploadTasks = chunksToUpload.map((chunkIndex) => {
    return async () => {
      const start = chunkIndex * CHUNK_SIZE
      const end = Math.min(start + CHUNK_SIZE, file.size)
      const chunk = file.slice(start, end)

      // 上传分片
      const { etag } = await uploadChunk(fileId, chunkIndex, chunk)

      // 记录 etag
      partEtags.push({ PartNumber: chunkIndex + 1, ETag: etag })

      // 更新进度
      completedChunks++
      const progress = Math.round((completedChunks / totalChunks) * 100)
      onProgress?.(progress)
      onChunkComplete?.(chunkIndex, totalChunks)
    }
  })

  // 7. 并发上传分片
  await runWithConcurrency(uploadTasks, CONCURRENCY)

  // 8. 完成上传（合并分片）
  const { fileUrl } = await completeUpload(fileId)

  return {
    fileId,
    fileName: file.name,
    fileSize: file.size,
    fileMd5,
    fileUrl,
    totalChunks,
  }
}
