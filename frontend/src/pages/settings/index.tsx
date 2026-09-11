import { useState } from 'react'
import { Card, Tabs, Table, Tag, Button, Space, Input, Modal, Form, message, Empty } from 'antd'
import {
  PlusOutlined,
  ApiOutlined,
  ToolOutlined,
  FileTextOutlined,
  DeleteOutlined,
  EditOutlined,
} from '@ant-design/icons'
import type { TabsProps } from 'antd'
import './index.scss'

interface McpItem {
  key: string
  name: string
  endpoint: string
  status: 'active' | 'inactive'
}

interface SkillItem {
  key: string
  name: string
  description: string
  category: string
}

interface PromptItem {
  key: string
  name: string
  content: string
  category: string
}

const mockMcp: McpItem[] = [
  { key: '1', name: '飞书 MCP', endpoint: 'https://mcp.feishu.cn', status: 'active' },
  { key: '2', name: 'GitHub MCP', endpoint: 'https://mcp.github.com', status: 'inactive' },
]

const mockSkills: SkillItem[] = [
  { key: '1', name: '代码审查', description: '自动审查代码质量和规范', category: '开发' },
  { key: '2', name: 'Bug 调查', description: '系统化调试和问题定位', category: '调试' },
  { key: '3', name: '前端规范', description: 'React+TS+Vite 编码规范', category: '开发' },
]

const mockPrompts: PromptItem[] = [
  { key: '1', name: '代码生成', content: '你是一个资深开发者...', category: '开发' },
  { key: '2', name: 'Bug 修复', content: '请按照以下步骤排查问题...', category: '调试' },
]

function SettingsPage() {
  const [mcpData] = useState(mockMcp)
  const [skillData] = useState(mockSkills)
  const [promptData] = useState(mockPrompts)

  const tabItems: TabsProps['items'] = [
    {
      key: 'mcp',
      label: (
        <span>
          <ApiOutlined />
          MCP 配置
        </span>
      ),
      children: (
        <div className="settings-tab-content">
          <div className="tab-header">
            <h3>MCP 服务管理</h3>
            <Button type="primary" icon={<PlusOutlined />}>
              添加 MCP
            </Button>
          </div>
          <Table
            columns={[
              { title: '名称', dataIndex: 'name', key: 'name' },
              { title: '端点', dataIndex: 'endpoint', key: 'endpoint' },
              {
                title: '状态',
                dataIndex: 'status',
                key: 'status',
                render: (status: string) => (
                  <Tag color={status === 'active' ? 'green' : 'default'}>
                    {status === 'active' ? '已连接' : '未连接'}
                  </Tag>
                ),
              },
              {
                title: '操作',
                key: 'action',
                render: () => (
                  <Space>
                    <Button type="link" icon={<EditOutlined />}>编辑</Button>
                    <Button type="link" danger icon={<DeleteOutlined />}>删除</Button>
                  </Space>
                ),
              },
            ]}
            dataSource={mcpData}
            pagination={false}
          />
        </div>
      ),
    },
    {
      key: 'skill',
      label: (
        <span>
          <ToolOutlined />
          Skill 管理
        </span>
      ),
      children: (
        <div className="settings-tab-content">
          <div className="tab-header">
            <h3>Skill 技能管理</h3>
            <Button type="primary" icon={<PlusOutlined />}>
              添加 Skill
            </Button>
          </div>
          <Table
            columns={[
              { title: '名称', dataIndex: 'name', key: 'name' },
              { title: '描述', dataIndex: 'description', key: 'description' },
              {
                title: '分类',
                dataIndex: 'category',
                key: 'category',
                render: (cat: string) => <Tag>{cat}</Tag>,
              },
              {
                title: '操作',
                key: 'action',
                render: () => (
                  <Space>
                    <Button type="link" icon={<EditOutlined />}>编辑</Button>
                    <Button type="link" danger icon={<DeleteOutlined />}>删除</Button>
                  </Space>
                ),
              },
            ]}
            dataSource={skillData}
            pagination={false}
          />
        </div>
      ),
    },
    {
      key: 'prompt',
      label: (
        <span>
          <FileTextOutlined />
          Prompt 模板
        </span>
      ),
      children: (
        <div className="settings-tab-content">
          <div className="tab-header">
            <h3>Prompt 模板管理</h3>
            <Button type="primary" icon={<PlusOutlined />}>
              添加 Prompt
            </Button>
          </div>
          <Table
            columns={[
              { title: '名称', dataIndex: 'name', key: 'name' },
              {
                title: '内容',
                dataIndex: 'content',
                key: 'content',
                ellipsis: true,
              },
              {
                title: '分类',
                dataIndex: 'category',
                key: 'category',
                render: (cat: string) => <Tag>{cat}</Tag>,
              },
              {
                title: '操作',
                key: 'action',
                render: () => (
                  <Space>
                    <Button type="link" icon={<EditOutlined />}>编辑</Button>
                    <Button type="link" danger icon={<DeleteOutlined />}>删除</Button>
                  </Space>
                ),
              },
            ]}
            dataSource={promptData}
            pagination={false}
          />
        </div>
      ),
    },
  ]

  return (
    <div className="settings-page">
      <div className="settings-page-header">
        <h2>设置</h2>
        <p className="settings-desc">管理 MCP 服务、Skill 技能和 Prompt 模板</p>
      </div>
      <Card className="settings-card">
        <Tabs defaultActiveKey="mcp" items={tabItems} />
      </Card>
    </div>
  )
}

export default SettingsPage
