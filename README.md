# th-skills

我积累的各种 Skill 集合：学习、写作、投资等等。

每个 skill 是一个独立目录，遵循 [Claude SKILL.md 规范](https://docs.claude.com/en/docs/agents-and-tools/agent-skills)，可被 Claude Code / Qoder 等 CLI 直接加载。

## 目录约定

采用扁平结构，每个 skill 直接放在仓库根目录下：

```
<skill-name>/
├── SKILL.md          # 必需，含 YAML frontmatter（name / description）
├── resources/        # 可选，参考资料、模板、示例
└── scripts/          # 可选，可执行脚本
```

新建 skill 请复制 [`_template/SKILL.md`](_template/SKILL.md) 起步。

## 索引

- [`th-writer/`](th-writer/SKILL.md) — 撰写或改写中文博客长文（源码解读、技术解析、实践复盘、产品体验、观点文章）。
- [`th-ppt-skill/`](th-ppt-skill/SKILL.md) — 面向方案汇报、产品功能与技术分析的 PPT 内容设计和可编辑交付流程；含已审视的通用技术架构视觉参考，并提供素材分级规则。
