module.exports = {
  extends: ['@commitlint/config-conventional'],
  rules: {
    'type-enum': [
      2,
      'always',
      [
        'feat',     // 新功能
        'fix',      // 修复 bug
        'docs',     // 文档变更
        'style',    // 代码格式（不影响功能）
        'refactor', // 代码重构
        'perf',     // 性能优化
        'test',     // 测试相关
        'build',    // 构建系统或外部依赖
        'ci',       // CI 配置
        'chore',    // 其他不修改源码的变更
        'revert',   // 回退提交
      ],
    ],
    'type-case': [2, 'always', 'lower-case'],
    'type-empty': [2, 'never'],
    'subject-empty': [2, 'never'],
    'subject-full-stop': [2, 'never', '.'],
  },
}