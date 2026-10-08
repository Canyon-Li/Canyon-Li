<picture>
  <source media="(prefers-color-scheme: dark)" srcset="https://raw.githubusercontent.com/Canyon-Li/Canyon-Li/main/assets/banner-dark.svg" />
  <img width="100%" src="https://raw.githubusercontent.com/Canyon-Li/Canyon-Li/main/assets/banner.svg" alt="Canyon-Li — AI Agent Developer" />
</picture>

<div align="center">

<a href="https://git.io/typing-svg"><picture>
  <source media="(prefers-color-scheme: dark)" srcset="https://readme-typing-svg.demolab.com/?font=Fira+Code&size=22&pause=1200&color=B7A8DA&center=true&vCenter=true&width=620&lines=Auditing+AI+agents+for+measurable+security;Turning+complex+systems+into+little+plays;AI+Agent+%2F+RAG+%2F+MCP" />
  <img src="https://readme-typing-svg.demolab.com/?font=Fira+Code&size=22&pause=1200&color=8E7BB8&center=true&vCenter=true&width=620&lines=Auditing+AI+agents+for+measurable+security;Turning+complex+systems+into+little+plays;AI+Agent+%2F+RAG+%2F+MCP" alt="Typing SVG" />
</picture></a>

</div>

## ✦ 项目



### [Peregrine](https://github.com/Canyon-Li/Peregrine) — 本地优先的对话式 Agent 工作台

后端是一套完整的 Agent 运行时，前端是对话 / 任务可视化 / 设置界面，中间走 WebSocket RPC。工具审批门控、两层上下文压缩、长期记忆、技能沉淀都在里面，数据全部落在本地，不依赖外部托管服务。

> **工具审批门控 · 两层上下文压缩 · 长期记忆 · 技能沉淀**
> 数据全落本地（SQLite + `.peregrine/`）· `Python` `FastAPI` `React` `TypeScript` `MIT`

### [JeRAG](https://github.com/Canyon-Li/JeRAG) — 按问题难度自适应分配算力的本地文献 RAG

Je = Just Enough。检索轮数、查询改写、终止时机都由模型在运行时自己判断：简单题首轮即停，难题才继续追。面向全英文学术论文语料，多栏 / 表格 / 公式交给 Docling 结构化提取，难直接召回的内容用 VLM 生成 caption 单独成 chunk。

> **简单题首轮即停 · 闲聊零检索 · 信息不够自动追问**
> 正对单步 RAG 的三个结构性缺陷 · `Python` `Chroma` `BM25` `Docling` `MIT`

同源于 [RAG-MCP](https://github.com/Canyon-Li/RAG-MCP)——把检索能力封装成带 3 个工具的 MCP server。JeRAG 复用了它的解析与检索层，在其上重写为 Agentic RAG，让检索轮数和终止时机改由模型自己判断。


### [Mini-Play](https://github.com/Canyon-Li/Mini-Play) — 把技术概念演成人人看得懂的小剧场

一组 Claude Code skill，用角色扮演对话解释复杂概念。不是聊天记录整理器，而是一套剧本 DSL：角色、台词、旁白、谢幕都是结构化字段，能校验、能 lint、能渲染成 Markdown 或自包含 HTML。

> `Python` `Claude Code Skill` `MIT`

## ✦ 上游贡献

- **[CyberClaw](https://github.com/ttguy0707/CyberClaw) — [PR #18](https://github.com/ttguy0707/CyberClaw/pull/18) · [PR #19](https://github.com/ttguy0707/CyberClaw/pull/19) 已合并**

  审计出 calculator 工具的 `eval` 注入，以及 `execute_office_shell` 正则拦截可被绕过的问题，修复后回流上游。

## ✦ 关于我

- 关注 **AI Agent / RAG / MCP** 的工程实现与安全边界
- 在读 letta / llama_index / ragflow 源码 —— 读到边界问题会提 PR 回去，上面那条 CyberClaw 就是这么来的
- 喜欢把难解释的东西做成能上手的工具，Mini-Play 就是这么来的

## ✦ 技术栈

<div align="center">

<img src="https://skillicons.dev/icons?i=py,ts,react,fastapi,docker,git,githubactions,vscode,linux&perline=9" alt="Skills"/>

</div>

## ✦ GitHub Stats

<div align="center">

<picture>
  <source media="(prefers-color-scheme: dark)" srcset="https://raw.githubusercontent.com/Canyon-Li/Canyon-Li/main/assets/stats-dark.svg" />
  <img src="https://raw.githubusercontent.com/Canyon-Li/Canyon-Li/main/assets/stats-light.svg" alt="GitHub stats" height="206" />
</picture>
&nbsp;
<picture>
  <source media="(prefers-color-scheme: dark)" srcset="https://raw.githubusercontent.com/Canyon-Li/Canyon-Li/main/assets/streak-dark.svg" />
  <img src="https://raw.githubusercontent.com/Canyon-Li/Canyon-Li/main/assets/streak-light.svg" alt="Contribution streak" height="206" />
</picture>

<br/><br/>

<picture>
  <source media="(prefers-color-scheme: dark)" srcset="https://raw.githubusercontent.com/Canyon-Li/Canyon-Li/main/assets/trophies-dark.svg" />
  <img src="https://raw.githubusercontent.com/Canyon-Li/Canyon-Li/main/assets/trophies-light.svg" alt="Trophies" height="150" />
</picture>

</div>

## ✦ 贡献贪吃蛇

<div align="center">

<picture>
  <source media="(prefers-color-scheme: dark)" srcset="https://raw.githubusercontent.com/Canyon-Li/Canyon-Li/output/github-contribution-grid-snake-dark.svg" />
  <source media="(prefers-color-scheme: light)" srcset="https://raw.githubusercontent.com/Canyon-Li/Canyon-Li/output/github-contribution-grid-snake.svg" />
  <img alt="contribution snake" src="https://raw.githubusercontent.com/Canyon-Li/Canyon-Li/output/github-contribution-grid-snake.svg" />
</picture>

</div>

<br/>

<div align="center">

<picture>
  <source media="(prefers-color-scheme: dark)" srcset="https://raw.githubusercontent.com/Canyon-Li/Canyon-Li/main/assets/footer-dark.svg" />
  <img width="100%" src="https://raw.githubusercontent.com/Canyon-Li/Canyon-Li/main/assets/footer.svg" alt="Canyon-Li · AI Agent Developer" />
</picture>

<img src="https://komarev.com/ghpvc/?username=Canyon-Li&style=flat-square&color=8e7bb8&label=Profile+Views" alt="Profile views"/>

</div>
