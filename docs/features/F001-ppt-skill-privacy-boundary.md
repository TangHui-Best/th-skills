---
id: F001
doc_kind: feature
status: done
created: 2026-10-16
updated: 2026-10-16
---

# F001: th-ppt-skill 素材隐私边界

## Goal

让 th-ppt-skill 在复用参考图、生成图稿和交付 PPT 时，保护真正的内部架构与业务材料，不因视觉制作而外发敏感内容或残留不必要元数据；不将用户已确认的通用素材误标为受限。

## Vision Anchor

- 原始请求或来源：用户要求审视并修复 th-ppt-skill 的隐私风险。
- 用户痛点或工程问题：客户或内部架构参考图和 PNG 溯源数据可能随技能或外部图像工具调用泄露；通用素材则应以实际可见标识和用户分类为准。
- 期望结果：建立素材分级、外部处理授权、脱敏交付和可重复检查。
- 非目标或边界：不改变 PPT 的内容设计方法，不替用户判定具体客户材料是否可公开。
- Exit Gate 对照来源：本 Feature 的验收标准及 ADR-001。

## Current Status

Done。技能已具备敏感素材分级、外部工具门禁、PNG 元数据清理和可重复检查。

## Links

- [ADR-001：对敏感 PPT 素材采用默认不外发策略](../decisions/ADR-001-ppt-skill-sensitive-material-handling.md)
- [EV-001：th-ppt-skill 隐私加固验证](../evidence/EV-001-ppt-skill-privacy-hardening.md)

## Acceptance Criteria

- [x] 技能在处理材料与调用外部图像工具前明确分级和授权边界。
- [x] 参考架构图按用户确认的通用素材分类，并保留未来受限材料的外发门禁。
- [x] 发布版 PNG 不含 `caBX`、EXIF 或文本元数据载体。
- [x] 检查脚本能验证 PNG 元数据和常见明文凭据/邮箱模式。
- [x] 所有引用路径有效，检查脚本通过。

## Patch History

None yet

| Patch | Date | Commit | Symptom | Root Cause | Protection | Status |
| --- | --- | --- | --- | --- | --- | --- |

## Evidence

`docs/evidence/EV-001-ppt-skill-privacy-hardening.md` 记录元数据清理、脚本执行和文件引用验证结果。

## Next Step

如需公开发布，先由素材权利人确认独立图标与整页参考图的来源授权和可公开范围。
