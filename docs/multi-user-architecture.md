# CUI 多用户并发架构详解

## 🎯 核心问题回答

**问题:** 三个用户同时访问,系统如何运作?能否区分不同用户的对话?是否互不干扰?

**答案:** ✅ 完全支持!每个用户、每个对话都有独立的进程和标识符,完全隔离!

---

## 📊 系统架构概览

```
┌─────────────────────────────────────────────────────────────────┐
│                    CUI Server (单一实例)                          │
│                                                                   │
│  ┌─────────────────────────────────────────────────────────┐    │
│  │ Auth Token: abc123 (所有用户共享同一个 token)             │    │
│  └─────────────────────────────────────────────────────────┘    │
│                                                                   │
│  ┌──────────────────────────────────────────────────────────┐   │
│  │           StreamManager (流管理器)                         │   │
│  │   Map<streamingId, Set<Response>>                         │   │
│  │   - streamingId_1 → [User1's HTTP Response]              │   │
│  │   - streamingId_2 → [User2's HTTP Response]              │   │
│  │   - streamingId_3 → [User3's HTTP Response]              │   │
│  └──────────────────────────────────────────────────────────┘   │
│                                                                   │
│  ┌──────────────────────────────────────────────────────────┐   │
│  │       ClaudeProcessManager (进程管理器)                    │   │
│  │   Map<streamingId, ChildProcess>                          │   │
│  │   - streamingId_1 → Claude Process A (PID: 1001)         │   │
│  │   - streamingId_2 → Claude Process B (PID: 1002)         │   │
│  │   - streamingId_3 → Claude Process C (PID: 1003)         │   │
│  └──────────────────────────────────────────────────────────┘   │
└─────────────────────────────────────────────────────────────────┘
```

---

## 👥 三个用户同时访问的完整流程

### 场景设置
- **用户 A**: 张三,想分析代码
- **用户 B**: 李四,想重构项目
- **用户 C**: 王五,想写测试

### 时间线

```
时间  │ 用户 A (张三)                  │ 用户 B (李四)                 │ 用户 C (王五)
──────┼──────────────────────────────┼─────────────────────────────┼──────────────────────────
10:00 │ 访问 http://server:3001/     │                              │
      │ #abc123                      │                              │
      │                              │                              │
10:01 │ 发送消息: "分析代码"          │ 访问 http://server:3001/    │
      │ ↓                            │ #abc123                      │
      │ 服务器创建:                   │                              │
      │ - streamingId: uuid-AAA      │                              │
      │ - sessionId: sess_001        │                              │
      │ - spawn Claude (PID: 1001)   │                              │
      │                              │                              │
10:02 │ 收到流式响应...              │ 发送消息: "重构项目"          │ 访问 http://server:3001/
      │ {"type":"assistant"...}      │ ↓                            │ #abc123
      │                              │ 服务器创建:                   │
      │                              │ - streamingId: uuid-BBB      │
      │                              │ - sessionId: sess_002        │
      │                              │ - spawn Claude (PID: 1002)   │
      │                              │                              │
10:03 │ 继续收到响应...              │ 收到流式响应...              │ 发送消息: "写测试"
      │                              │                              │ ↓
      │                              │                              │ 服务器创建:
      │                              │                              │ - streamingId: uuid-CCC
      │                              │                              │ - sessionId: sess_003
      │                              │                              │ - spawn Claude (PID: 1003)
      │                              │                              │
10:04 │ ✅ 对话完成                  │ 继续收到响应...              │ 收到流式响应...
      │ Claude 进程 1001 退出        │                              │
      │                              │                              │
10:05 │ 开始新对话: "继续优化"       │ ✅ 对话完成                  │ 继续收到响应...
      │ ↓                            │ Claude 进程 1002 退出        │
      │ 服务器创建:                   │                              │
      │ - streamingId: uuid-DDD      │                              │
      │ - sessionId: sess_004        │                              │
      │ - spawn Claude (PID: 1004)   │                              │
      │                              │                              │
```

---

## 🔑 关键隔离机制

### 1. **streamingId (流标识符)**

每个对话都有唯一的 UUID:

```typescript
// 从 claude-process-manager.ts
const streamingId = uuidv4(); // 例如: "a1b2c3d4-e5f6-..."

// 用于:
// 1. 标识 Claude 子进程
this.processes.set(streamingId, claudeProcess);

// 2. 标识 HTTP 流连接
this.streamManager.addClient(streamingId, response);

// 3. 路由输出到正确的客户端
this.streamManager.broadcast(streamingId, event);
```

### 2. **sessionId (会话标识符)**

Claude CLI 生成的永久会话 ID:

```typescript
// Claude CLI 返回的第一条消息
{
  "type": "system",
  "subtype": "init",
  "session_id": "1234567890abcdef",  // ← Claude 内部 ID
  "cwd": "/path/to/project",
  "model": "claude-sonnet-4.5"
}

// 用于:
// 1. 恢复历史对话
claude --resume 1234567890abcdef "继续聊天"

// 2. 读取对话历史
~/.claude/sessions/1234567890abcdef/
```

### 3. **Auth Token (认证令牌)**

单个 token,所有用户共享:

```typescript
// 从 auth.ts
const token = authHeader.substring(7); // 提取 Bearer token
const expectedToken = ConfigService.getInstance().getConfig().authToken;

if (token !== expectedToken) {
  res.status(401).json({ error: 'Unauthorized' });
  return;
}
```

**重要:** 这是**单用户系统**!所有知道 token 的人共享同一个服务器。

### 4. **StreamManager (流管理器)**

负责将正确的输出发送给正确的客户端:

```typescript
// 从 stream-manager.ts
class StreamManager {
  // 存储: streamingId → Set<Response>
  private clients: Map<string, Set<Response>> = new Map();

  broadcast(streamingId: string, event: StreamEvent): void {
    const clients = this.clients.get(streamingId);
    if (!clients) return;

    // 发送给所有监听这个 streamingId 的客户端
    for (const client of clients) {
      this.sendSSEEvent(client, event);
    }
  }
}
```

---

## 🎨 可视化示例

### 服务器内部状态 (10:03 时刻)

```javascript
// ProcessManager.processes
Map {
  "uuid-AAA" => ChildProcess { pid: 1001, ... },  // 张三的进程
  "uuid-BBB" => ChildProcess { pid: 1002, ... },  // 李四的进程
  "uuid-CCC" => ChildProcess { pid: 1003, ... }   // 王五的进程
}

// StreamManager.clients
Map {
  "uuid-AAA" => Set [ Response对象A ],  // 张三的 HTTP 连接
  "uuid-BBB" => Set [ Response对象B ],  // 李四的 HTTP 连接
  "uuid-CCC" => Set [ Response对象C ]   // 王五的 HTTP 连接
}
```

### 系统进程列表

```bash
$ ps aux | grep claude

user  1001  0.5  2.3  claude -p chat "分析代码" ...        # 张三的
user  1002  0.8  2.1  claude -p chat "重构项目" ...        # 李四的
user  1003  0.3  1.9  claude -p chat "写测试" ...          # 王五的
```

---

## ✅ 隔离保证

### 1. **进程隔离**
```
每个对话 = 独立的 Claude CLI 进程
进程 A 崩溃 ❌ → 不影响进程 B 和 C ✅
```

### 2. **数据隔离**
```
每个 sessionId 有独立的目录:
~/.claude/sessions/
├── 1234567890abcdef/  (张三的对话)
│   ├── conversation.jsonl
│   └── metadata.json
├── 2345678901bcdefg/  (李四的对话)
│   ├── conversation.jsonl
│   └── metadata.json
└── 3456789012cdefgh/  (王五的对话)
    ├── conversation.jsonl
    └── metadata.json
```

### 3. **流输出隔离**
```typescript
// Claude 进程 A 输出 → 只发给 uuid-AAA 的客户端
claudeProcess.stdout.on('data', (data) => {
  const streamingId = "uuid-AAA";
  this.streamManager.broadcast(streamingId, parsedEvent);
  // ↑ 只发给张三,不会发给李四和王五
});
```

### 4. **工作目录隔离**
```typescript
// 每个进程在不同的目录运行
spawn('claude', args, {
  cwd: '/home/user/project-A'  // 张三的项目
});

spawn('claude', args, {
  cwd: '/home/user/project-B'  // 李四的项目
});

spawn('claude', args, {
  cwd: '/home/user/project-C'  // 王五的项目
});
```

---

## 🔒 安全考虑

### 当前设计: 单用户多会话

```
一个 Auth Token → 多个人共享 → 所有人看到相同的:
- 文件系统
- 对话历史列表
- API keys
```

**适用场景:**
- ✅ 个人使用 (多个浏览器标签页)
- ✅ 团队共享 (信任的团队成员)
- ❌ 公开服务 (需要多用户系统)

### 如果要支持真正的多用户

需要添加:
```typescript
// 1. 用户管理系统
interface User {
  id: string;
  username: string;
  password: string;  // hashed
  sessions: string[];  // 只能访问自己的 sessions
}

// 2. 基于用户的 token
authToken = `user_${userId}_${randomToken}`;

// 3. 数据隔离
~/.cui/users/
├── user_zhang/
│   └── sessions/
├── user_li/
│   └── sessions/
└── user_wang/
    └── sessions/
```

---

## 📊 性能考虑

### 并发限制

```typescript
// 每个 Claude 进程占用资源:
- CPU: ~10-20%
- Memory: ~200-500 MB
- 网络: 持续 API 调用

// 服务器承载能力示例:
4 核 8GB RAM 服务器 → 约 10-15 个并发对话
8 核 16GB RAM 服务器 → 约 30-50 个并发对话
```

### 资源清理

```typescript
// 对话结束后自动清理
claudeProcess.on('close', (code) => {
  this.processes.delete(streamingId);  // 删除进程引用
  this.outputBuffers.delete(streamingId);  // 清理缓冲区
  this.streamManager.removeClient(streamingId, response);  // 关闭连接
});
```

---

## 🎯 总结

| 问题 | 答案 |
|------|------|
| 支持多用户同时访问? | ✅ 是的 |
| 能区分不同用户的对话? | ✅ 每个对话有唯一的 streamingId |
| 对话之间互不干扰? | ✅ 独立进程 + 独立数据 + 独立流 |
| 支持多用户账号系统? | ❌ 当前是单 token 共享模式 |
| 一个用户可以多个对话? | ✅ 可以,每个对话独立 |
| 对话可以后台运行? | ✅ 可以关闭浏览器,进程继续执行 |

---

## 🔬 验证方法

想亲自验证?试试这个:

```bash
# 终端 1: 启动服务器
npm run dev

# 终端 2: 开始对话 A
curl -X POST http://localhost:3001/api/conversations/start \
  -H "Authorization: Bearer abc123" \
  -H "Content-Type: application/json" \
  -d '{"message": "分析代码", "workingDirectory": "/tmp/project-a"}'

# 终端 3: 同时开始对话 B
curl -X POST http://localhost:3001/api/conversations/start \
  -H "Authorization: Bearer abc123" \
  -H "Content-Type: application/json" \
  -d '{"message": "写测试", "workingDirectory": "/tmp/project-b"}'

# 终端 4: 查看进程
ps aux | grep claude
# 你会看到两个独立的 claude 进程!
```
