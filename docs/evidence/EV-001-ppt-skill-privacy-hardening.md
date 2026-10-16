---
id: EV-001
doc_kind: evidence
scope: project
feature_refs:
  - F001-ppt-skill-privacy-boundary
created: 2026-10-16
---

# EV-001: th-ppt-skill 隐私加固验证

## Scope

验证 th-ppt-skill 的敏感素材门禁文案、架构参考的内部分类、四个独立 PNG 的元数据清理，以及本地检查脚本。

## Commands

```text
python th-ppt-skill/scripts/sanitize_png.py th-ppt-skill/assets/technical-architecture/agent.png th-ppt-skill/assets/technical-architecture/application-service.png th-ppt-skill/assets/technical-architecture/client.png th-ppt-skill/assets/technical-architecture/mcp-tools.png
python -m py_compile th-ppt-skill/scripts/sanitize_png.py th-ppt-skill/scripts/check_privacy_assets.py
python th-ppt-skill/scripts/check_privacy_assets.py
```

## Results

Pass。四个 PNG 的 `caBX` 溯源块均已清除；脚本检查通过；图标的尺寸、ARGB 格式和透明通道保留。`reference-slide.png` 不含该类元数据；用户已确认它和四个图标为通用素材，本次可见内容审视未发现华为标识、工号、客户名、账号或平台水印。

## AgentMentor Validation

已执行 `python C:\Users\HUAWEI\.codex\plugins\cache\personal\agentmentor\0.2.0+codex.20260604093000\skills\using-agentmentor\scripts\knowledge_check.py --root E:\Self-Project\th-skills --docs-path docs --strict`。Feature 链接修正后复验结果为 3 份 Markdown、3 个知识工件、0 error、0 warning。

## Artifacts

- `th-ppt-skill/SKILL.md`
- `th-ppt-skill/references/content-plan.md`
- `th-ppt-skill/references/technical-architecture.md`
- `th-ppt-skill/assets/technical-architecture/README.md`
- `th-ppt-skill/scripts/sanitize_png.py`
- `th-ppt-skill/scripts/check_privacy_assets.py`
- `docs/decisions/ADR-001-ppt-skill-sensitive-material-handling.md`

## Notes

补充审视：以原始分辨率查看五张 PNG，并对 PNG 二进制执行品牌/水印/工号/生成平台标识词扫描；未发现华为标识、工号、客户名、账号、平台水印或生成平台角标。PNG 块仅保留图像必要块，不含 C2PA、EXIF 或 PNG 文本元数据。

本验证不能替代素材权利或公开发布范围的人工确认；检查脚本也不能从位图内容自动判断业务架构是否敏感。
