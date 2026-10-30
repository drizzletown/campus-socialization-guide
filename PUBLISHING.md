# GitHub Pages 发布操作（新仓库）

此项目按 **GitHub Pages: main 分支、/docs 目录** 制作，`docs/.nojekyll` 已包含，无需部署密钥。

1. 进入 GitHub 并创建**新的公开仓库**（建议 `campus-socialization-guide`），不要覆盖已有的个人网站或无关项目。
2. 将本目录所有文件放在仓库根目录：`README.md`、`build.py`、`content/`、`docs/`、`.github/` 等；不要额外套一层目录。保持所有 Markdown、JSON、HTML 的 UTF-8 编码。
3. 确认默认分支为 `main`，等待 `.github/workflows/verify.yml` 完成自动检查；本地也可运行 README 的构建和校验命令。
4. 仓库 `Settings → Pages → Build and deployment` 选择 `Deploy from a branch`、分支 `main`、文件夹 `/docs`，保存。
5. 在 `Actions` 中确认 Pages 部署成功，并打开 GitHub 显示的最终网址。若仓库名采用上述建议，**预期形式**为 `https://<owner>.github.io/campus-socialization-guide/`，只有成功部署后才可称为正式网址。
6. 用桌面和手机打开网站首页、章节、搜索、模拟试读、工作纸、校规核验页，检查搜索与本地已读状态；不要只检查构建通过。
7. 正式公开推广前由作者确认署名、版权许可及至少一轮人工内容复核；对仍未验证的学校政策在网站保持明确的适用边界。

本项目不含 CNAME。没有为未确定的域名伪造站点地图或 canonical URL。项目采用相对路径，可由 Pages 项目子路径托管。
