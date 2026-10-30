# 走进大学，学会与世界相处

**Entering University, Learning to Live with the World**

基于大学生社会化网络认知模型（Student Socialization Cognitive Model，SSCM）的中英文双语大学生成长读物。全书以十辑五十章展开，贯通课程学习、生活与家庭、友谊和亲密关系、学生组织、科研和实习、数字社会、未来选择、权益风险与长期成长。

A bilingual university-life book grounded in the Student Socialization Cognitive Model (SSCM). Ten parts and fifty chapters examine learning, everyday life, relationships, organizations, research, professional practice, digital life, future choices, rights and sustained development.

## 在线阅读 · Read online

- [中文版 / Chinese](https://drizzletown.github.io/campus-socialization-guide/)
- [English edition](https://drizzletown.github.io/campus-socialization-guide/en/)

两个语言版本均有十辑导论、50章正文、全书结语、七篇专题、12个情境案例、12张行动工具卡和情境练习。语言入口可在对应页面间切换。英文版根据相同主题和理论原则独立编写，保留相同章节结构，但并非中文逐段等长直译。

Both editions include ten part introductions, 50 chapters, an afterword, seven detailed topic guides, 12 cases, 12 worksheets and scenario exercises. The English edition is a stand-alone adaptation, not a certified paragraph-for-paragraph translation.

## 阅读书稿 · Read the complete book

- [中文连续版 / Chinese complete text](BOOK_FULL.md)
- [English complete text](BOOK_EN.md)
- [十辑目录与应用索引 / Contents and thematic index](CONTENT_MATRIX.md)

中文权威正文位于 `content/part01` 至 `content/part10`，英文对应正文位于 `content/en/part01` 至 `content/en/part10`。每辑的导论分别位于 `content/volumes/` 和 `content/en/volumes/`。正式网站输出位于 `docs/` 与 `docs/en/`。

## 本书的使用边界 · Scope

SSCM从个人能力、可达关系、社会角色、实际贡献及行动自主性五个方面理解情境。这些维度不是人格测评或社会化排名。情境案例用于解释不同条件可能导致的不同选择，不代替对真实事实、现行制度和专业安全要求的核实。

SSCM provides lenses for situated judgment, not a maturity score. Illustrative cases are not individualized legal, medical, mental-health or institutional advice. Seek appropriate qualified or emergency support as necessary.

网站不要求注册，不向服务器提交工作纸内容。已读标记只保存在浏览器本地。任何公开反馈都不应包含可识别的个人隐私或他人资料。

The website requires no account; worksheet entries are not transmitted. Avoid identifiable or confidential information in public feedback.

## 网站生成 · Build the site

需要 Python 3.13；检索回归使用 Node.js 22。依赖见 `requirements.txt`。

```bash
python -m pip install -r requirements.txt
python build.py
python extras.py
python decision_lab.py
python reader_lab.py
python bilingual.py
python tools/validate.py
python tools/release_audit.py
node tools/simulated_reader_trial.js
```

在 GitHub Pages 选择 `main` 分支、`/docs` 目录。更多见 [PUBLISHING.md](PUBLISHING.md)。源文与生成的网页应一起提交，避免网站内容与书稿不一致。

## 版权 · Rights

公开阅读不自动授予复制、改编或商业再利用许可。请参阅 [COPYRIGHT.md](COPYRIGHT.md)。
