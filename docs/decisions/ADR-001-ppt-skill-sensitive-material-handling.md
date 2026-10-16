---
id: ADR-001
doc_kind: adr
status: accepted
scope: project
feature_refs:
  - F001-ppt-skill-privacy-boundary
decision_area: sensitive-material-handling
created: 2026-10-16
updated: 2026-10-16
---

# ADR-001: 对敏感 PPT 素材采用默认不外发策略

## Context

客户或内部技术架构参考图可能暴露系统拓扑、权限和观测边界。独立 PNG 还可能带有 C2PA `caBX` 溯源数据。仅依赖“不要复用业务事实”的内容提示，无法阻止受限材料被交给外部图像工具或随技能分发。本 ADR 规定处理策略，不替代用户对特定素材的实际分类。

## Decision

对无法明确公开属性的材料按内部或受限处理。受限材料默认不得传给外部服务；仅在用户明确确认已脱敏且允许外发后才可使用。发布版 PNG 清除 `caBX`、EXIF 和 PNG 文本元数据，并以脚本持续验证。

## Alternatives

- 仅在文档中提示“谨慎使用”：无法阻止外部处理和元数据残留，拒绝。
- 删除所有参考与图标：会破坏该技能的核心视觉复用价值，拒绝。
- 默认允许外发、由用户事后发现问题：风险不可逆，拒绝。

## Consequences

图像生成前可能需要用户确认分级，工作流多一个检查步骤；但内部信息不会因默认行为进入第三方服务，发布素材也不会携带不必要的溯源数据。若用户日后确认所有素材可公开，可调整分级并重新评估。

## Evidence

- `docs/features/F001-ppt-skill-privacy-boundary.md`
- `docs/evidence/EV-001-ppt-skill-privacy-hardening.md`
