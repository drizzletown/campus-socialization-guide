# 走进大学，学会与世界相处

**Entering University, Learning to Live with the World**

基于大学生社会化网络认知模型（Student Socialization Cognitive Model, SSCM）的中英文双语大学生活与成长行动读物。

A bilingual Chinese–English practical guide to learning, relationships, responsibility and informed action at university, based on SSCM.

## 在线阅读 · Read online

- **中文 / Chinese:** https://drizzletown.github.io/campus-socialization-guide/
- **English:** https://drizzletown.github.io/campus-socialization-guide/en/

每种语言均提供50章、七篇深读专题、12个情境案例、12张可填写的行动工具卡，以及情境判断与练习。页面顶部可切换语言，并返回当前对应的章节或功能页。

Both editions include 50 chapters, seven detailed guides, 12 cases, 12 editable worksheets and situation-based exercises. Use the language link in the top navigation to move between corresponding pages.

英文是按照相同主题和SSCM原则整理的**独立英文阅读版本**；部分表述较中文正文精简，并非逐句对应的法律效力或认证译文。

The English edition is a stand-alone, shorter adaptation following the same chapter sequence and SSCM principles; it is not a certified line-by-line translation of the Chinese text.

## 全书与来源 · Book and sources

- [中文连续阅读 / Chinese book](BOOK_FULL.md)
- [English complete reading edition](BOOK_EN.md)
- `content/part01/` – `content/part10/`：可编辑中文权威章节
- `content/en/part01/` – `content/en/part10/`：可编辑英文对应章节
- `content/deep/`、`content/en/deep/`：中英文专题
- `docs/`：GitHub Pages 静态网页；`docs/en/`：英文版网页

SSCM所采用的五个观察维度为个人能力、社会网络、社会角色、价值贡献与行动自主性；它们不构成测评总分。读者应核实事实与规则，区分不同解释，并在充分考虑安全、权责和现实条件的情况下行动。

SSCM examines capability, accessible networks, roles, actual contribution and autonomy. These are lenses for situated judgment, not scores or personality labels.

## 本地更新 · Local build

需要 Python 3.13、Node.js 22（检索回归测试使用），以及 `requirements.txt` 中的 Python 包。

```bash
python -m pip install -r requirements.txt
python build.py
python extras.py
python decision_lab.py
python reader_lab.py
python bilingual.py
python tools/validate.py
python tools/release_audit.py
node --check docs/en/site-en.js
node tools/simulated_reader_trial.js
```

构建后将源文件与生成的 `docs/` 一并提交到 `main`，GitHub Pages 使用 `/docs` 目录。不要直接手工修改生成的 HTML 页面后忘记同步对应的 Markdown 或数据源。

## 安全、隐私与版权 · Safety, privacy and rights

网站是纯静态页面，无需登录。已读标记仅存于浏览器，工具卡内容不自动上传或保存。案例是用于解释的假设情境，个人事务应以实际事实、现行制度和专业支持为准；出现紧急危险时优先求助当地紧急服务。

The site is static and requires no account. It does not upload worksheet entries. Illustrative cases are not individualized professional advice. Use current institutional rules and local emergency services where appropriate.

公开阅读不等于已授予复制、改编或商业使用许可。详见 [COPYRIGHT.md](COPYRIGHT.md)。欢迎提交不包含真实敏感信息的勘误和可用性建议，参见 [CONTRIBUTING.md](CONTRIBUTING.md)。
