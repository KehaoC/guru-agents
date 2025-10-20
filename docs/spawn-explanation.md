# spawn 机制详解

## 核心代码解析

### 1. 启动子进程 (claude-process-manager.ts:791)

```typescript
const claudeProcess = spawn(executablePath, args, {
  cwd,      // 在哪个目录运行
  env,      // 环境变量 (API keys 等)
  stdio: ['inherit', 'pipe', 'pipe']
  //      ^^^^^^^^   ^^^^^^  ^^^^^^
  //      stdin      stdout  stderr
  //      继承输入   捕获输出 捕获错误
});
```

**参数说明:**
- `executablePath`: Claude CLI 的路径,如 `/Users/kehao/.local/bin/claude`
- `args`: 命令行参数数组,如 `['-p', 'chat', 'Hello']`
- `options`: 配置对象
  - `cwd`: 工作目录
  - `env`: 包含 `ANTHROPIC_API_KEY` 等环境变量
  - `stdio`: 标准输入输出配置

### 2. 监听进程输出

```typescript
// 当 Claude 输出数据时 (stdout)
claudeProcess.stdout.on('data', (data: Buffer) => {
  const output = data.toString();
  // output 可能是:
  // {"type":"assistant","text":"你好!"}
  // {"type":"assistant","text":"我能帮你什么?"}

  // 解析 JSONL 并发送给浏览器
  this.parseAndEmitEvents(streamingId, output);
});

// 当 Claude 报错时 (stderr)
claudeProcess.stderr.on('data', (data: Buffer) => {
  const error = data.toString();
  console.error('Claude error:', error);
});

// 当 Claude 进程结束时
claudeProcess.on('close', (code) => {
  console.log('Claude exited with code:', code);
});
```

### 3. 为什么需要长期运行?

```typescript
// Claude 的一次对话可能持续很久:
用户: "分析这个项目的架构"
  ↓
Claude: [读取文件]      // 10 秒
  ↓
Claude: [分析代码]      // 30 秒
  ↓
Claude: [生成报告]      // 20 秒
  ↓
总共: 60+ 秒

// Vercel Serverless: 最多 10-60 秒 ❌
// 传统服务器: 无限制 ✅
```

## Vercel 为什么不支持?

### Vercel 的架构

```
请求到来 → 启动容器 → 运行函数 → 返回响应 → 销毁容器
            (冷启动)   (最多60秒)           (所有数据丢失)
```

### 这个项目需要的架构

```
服务器启动 → Claude 进程 1 → 持续运行...
          ↘ Claude 进程 2 → 持续运行...
           ↘ Claude 进程 3 → 持续运行...
            (可能运行几小时)
```

## 实际例子

### 用户视角
```
你: "帮我重构这个项目"
   ↓
[等待 2 分钟]
   ↓
Claude: "我已经分析了代码,建议这样重构..."
```

### 服务器视角
```bash
# 服务器执行:
$ /usr/local/bin/claude -p chat "帮我重构这个项目" \
    --output-format stream-json \
    --verbose

# 输出流 (持续 2 分钟):
{"type":"system","subtype":"init","session_id":"abc123"}
{"type":"assistant","text":"我来分析你的项目"}
{"type":"tool_use","name":"read_file","args":{"path":"src/main.ts"}}
{"type":"tool_result","content":"..."}
{"type":"assistant","text":"建议重构为..."}
# ... 更多输出
```

## 类比说明

### spawn 就像

**不用 spawn (不可能):**
```
你: "写一篇长文章"
助手: 立即给你完整文章 (但 AI 做不到这样)
```

**用 spawn (实际情况):**
```
你: "写一篇长文章"
助手: "好的,我开始写了..." (启动子进程)
助手: "第一段是..." (流式输出)
助手: "第二段是..." (继续输出)
助手: "第三段是..." (继续输出)
你: [关闭浏览器]
助手: [继续在后台写] (进程仍在运行)
你: [第二天打开浏览器]
助手: "文章写完了!" (进程完成)
```

## 总结

`spawn` 的作用:
1. ✅ 启动独立的 Claude CLI 进程
2. ✅ 持续监听其输出
3. ✅ 支持长时间运行
4. ✅ 多个进程并行运行
5. ✅ 后台任务持续执行

Vercel 的限制:
1. ❌ 进程最多运行 60 秒
2. ❌ 无法保存状态
3. ❌ 无法后台运行
4. ❌ 每次都是全新容器

**结论:** 这个项目本质上是一个"长期运行的进程管理器",不适合无服务器(Serverless)平台。
