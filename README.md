# 走进大学，学会与世界相处

> 基于《大学生社会化的网络认知模型与自主行动逻辑》（SSCM）的大学生成长与行动读物。

**公开发布候选版：v1.4.1（基于 v1.4 内容，完成发布技术与制度核验准备）。** v1.0原始内容已保留在历史交付包中。

这是一套**全新撰写**的大学生社会化成长读物，不沿用此前24章读物的正文。它面向大学生活中的真实事务：课程学习、师生沟通、宿舍与家庭、朋友与亲密关系、社团和公共参与、科研与实习、网络生活、升学就业、权益保障及长期成长。

## 内容

- 十辑、**50章完整正文**，每章包含情境、解释、五维观察、四项行动、**两种条件分支**、表达示例、边界和复盘；**50章均包含展开的深度情境推演**（v1.2完成全部章节的基础推演）。
- **12张可编辑、可打印的行动工具卡**，提供事实核实、五维观察、合作分工、沟通协商、权益记录等支架。
- **12个延伸情境案例**，演示相似现象为什么可能需要不同判断。
- **12组情境分流练习**，不要求输入个人信息，面对条件差异直接获得有针对性的阅读入口与行动建议。
- `BOOK_FULL.md`：适合在 GitHub 直接阅读和进一步编辑的全书连续版。
- `content/guides/decision-lab.md`：12组情境分流练习及情境判断分支。
- `PILOT_READING_GUIDE.md`：读者试用、认知检验和匿名反馈建议（网页为 `docs/pilot.html`）。
- `EDITORIAL_AUDIT_v1.4.md`：上一版编辑改动、理论核对与未完成工作。
- `docs/`：可以直接通过 GitHub Pages 发布的静态阅读网站，支持章节搜索、移动端浏览、打印和本地已读状态。

## 阅读入口

- 在线站点首页：`docs/index.html`（发布后对应 GitHub Pages 根路径）
- 全书：`BOOK_FULL.md`
- **目录与覆盖矩阵**：`CONTENT_MATRIX.md`
- 从现实难题快速进入：`docs/decision-lab.html`。
- **21个模拟学生任务**：`docs/reader-lab.html`，可先做判断再展开参考答案。
- 模型理论与使用边界：`content/guides/model.md`
- 校园制度的核验方法与典型高校官方入口：`docs/campus-policies.html`
- 阅读导言：`content/guides/preface.md`

## 发布到 GitHub Pages

1. 在 GitHub 上创建一个仓库，例如 `campus-socialization-guide`。
2. 将本项目所有文件上传到仓库的 `main` 分支。
3. 进入仓库 `Settings → Pages`。
4. 在 `Build and deployment` 中选择 `Deploy from a branch`，分支 `main`，目录 `/docs`，然后保存。
5. 等待 GitHub Pages 显示网站地址。项目网站通常会是 `https://<用户名>.github.io/campus-socialization-guide/`，请以 GitHub 页面显示的实际地址为准。

以上步骤只涉及静态网页，不需要后端、数据库、第三方账号登录或追踪服务。更详细操作见 `PUBLISHING.md`；发布后请按 `RELEASE_CHECKLIST.md` 做在线回归验收。

## 如何修订章节

`content/part01/` 至 `content/part10/` 中的 `.md` 文件是**权威可编辑正文**。不要直接把生成的 `docs/book/*.html` 当成源稿。

本地安装 Python 3.13（与 GitHub Actions 校验版本一致）：

```bash
python -m pip install -r requirements.txt
python build.py
python extras.py
python decision_lab.py
python reader_lab.py
python tools/validate.py
python tools/release_audit.py
node tools/simulated_reader_trial.js
```

- `build.py` 根据 Markdown 章节生成网页、搜索索引和连续阅读版。
- `extras.py` 根据工具卡、案例库源数据生成相应页面。
- `decision_lab.py` 根据12组情境分流配置生成网站练习页和 `content/guides/decision-lab.md`。
- `reader_lab.py` 根据21个虚构学生问题生成 `docs/reader-lab.html` 和可编辑Markdown。
- `content/search/intent-routes.json` 是可编辑的21条自然语言阅读路径表；`docs/assets/search-core.js` 与 `tools/simulated_reader_trial.js` 使用同一排序规则。
- 提交修订时同时提交 Markdown 源稿与重新生成的 `docs/` 网站文件。
- 工作纸与案例内容目前以 `extras.py` 为生成源；修改它们时请编辑该脚本的数据区，然后运行 `python extras.py`。

完整内容可供浏览和讨论。**公开仓库不自动授予改编或商业使用许可**。目前不授予复制、改编、分发的开放许可；详见 `COPYRIGHT.md`。如果作者希望开放改编或商业使用，应明确选择许可证并单独发布新版本。

## 重要声明

SSCM 是情境化的概念认知模型，不是经过完整验证的成长量表，不用于人格评级、心理诊断或给学生打分。案例均为构造的教学情境；本书不能替代医疗、法律、金融或紧急安全方面的专业服务。规则以具体学校、地区和时间的正式制度为准。

本站不收集或上传个人填写信息。“已读”标记只以章节编号保存在当前浏览器本地；工作纸不会自动保存所填文本，也不要求输入敏感信息。


## v1.3 新增：以读者问题为入口的深读专题

- 在 `content/deep/` 中新增七篇独立专题：课程求助、宿舍生活、科研、学生组织、亲密关系、就业实习、权益与安全。
- 17个重点章节增补不重复的条件推理，明确学生责任、组织支持、现实边界；50章目录保持不变。
- 重建网站后，从首页、主导航以及相关章节可进入 `/docs/deep/index.html`。
- 新增内容仅为编辑构造的教学情境，并非真实学生试读或已验证的干预研究。正式发布前请复核适用学校制度、处理渠道与地区法律。
- 推荐下一步先开展匿名、知情自愿的真实读者试用，再继续迭代。

## v1.4 本轮改动与限制

以七类常见困难构造21个模拟学生问题，新增20条转述检索、8条模糊问题误路由检查；七个章节和七篇专题作定点修订。旧版对21条完整问句均没有直接命中，新版对21条均将预设主题排第一；20条转述中19条第一、1条前三。**这些词句和答案都由编辑构造，不是人类学生试读数据**。当前静态代码只做离线关键词路由，不会准确理解所有自然语言，复杂问题请人工核实。完整记录见 `EDITORIAL_AUDIT_v1.4.md`。

所有上传文件仍需主动避开个人和第三方敏感信息；GitHub Issue是公开页面，不能用于危机求助。新版尚未完成浏览器视觉验收，未正式部署 GitHub Pages。

## 发布前与维护

- `PUBLISHING.md`：新仓库初始化和 GitHub Pages 配置。
- `RELEASE_CHECKLIST.md`：上线前/上线后验收表及当前剩余条件。
- `COPYRIGHT.md`：阅读与再利用的权利边界（**暂未采用开源许可**）。
- `CONTRIBUTING.md`：如何反馈或修订，避免公开敏感信息。
- `SECURITY.md`：静态网站安全、敏感信息和风险通报说明。

实际发布地址只能在新仓库创建及 Pages 部署成功后确认。校规与伦理内容的判断不构成法律、医疗或学校办事保证；请以适用正式制度为准。
