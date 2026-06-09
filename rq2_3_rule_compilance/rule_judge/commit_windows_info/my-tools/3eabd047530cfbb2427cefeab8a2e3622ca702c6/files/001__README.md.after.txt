# 前言
这是一个完全靠 cursor 开发的应用，程序员不参与任何编码！

# Electron Tools

基于 Electron Forge 和 Vite + TypeScript 的 Electron 应用。

## 环境要求

- Node.js ≥ v16.4.0
- pnpm ≥ 9.0.0

## 安装依赖

```bash
pnpm install
```

## 开发

启动开发模式：
```bash
pnpm start
```

## 构建

打包应用：
```bash
pnpm run package
```

创建分发包：
```bash
pnpm run make
```

发布应用：
```bash
pnpm run publish
```

## 代码检查

```bash
pnpm run lint
```

## 技术栈

- **Electron** - 跨平台桌面应用框架
- **Vite** - 快速构建工具
- **TypeScript** - 类型安全的 JavaScript
- **Electron Forge** - 完整的构建和分发工具链
- **pnpm** - 快速、节省磁盘空间的包管理器

## 项目结构

- `src/main.ts` - 主进程代码
- `src/renderer.ts` - 渲染进程代码
- `src/preload.ts` - 预加载脚本
- `index.html` - 应用 HTML 模板
- `forge.config.ts` - Electron Forge 配置 