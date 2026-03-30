# MkDocs + Material + GitHub Pages 专业课笔记博客搭建手册

这份手册按 `Windows + PowerShell + GitHub Pages` 的实际使用场景来写，目标是帮你从零搭一个“像 OI Wiki 那样适合记知识点、写课程笔记、长期维护”的纯静态博客/笔记站。

你最终会得到这样一套流程：

`本地写 Markdown -> 本地预览 -> 提交到 GitHub -> GitHub Pages 自动发布`

---

## 0. 先说结论：我推荐你走这条路线

如果你只是想稳定、长期地维护专业课笔记博客，我建议直接用下面这套组合：

- `MkDocs`
- `Material for MkDocs`
- `GitHub Pages`
- `GitHub Actions` 自动部署

原因很简单：

- 写作成本低，核心就是 Markdown
- 主题成熟，搜索、导航、代码块、目录、夜间模式都很好用
- 纯静态站点，没有数据库，不需要后端
- GitHub Pages 免费、够稳、适合个人知识站
- 以后迁移到 Vercel、Nginx、对象存储也很容易

---

## 1. 版本说明和一个很重要的提醒

截至 `2026-03-30`，Material for MkDocs 官方仍建议使用 `9.x` 主版本。

另外，Material 官方在 `2026-03-10` 的更新里明确提到：从 `9.7.5` 开始，它已经把 `MkDocs` 的依赖限制为 `<2`，用来避免 `MkDocs 2.0` 带来的不兼容问题。

所以这份手册的建议是：

- 安装 `mkdocs-material==9.*`
- 第一次安装完成后执行一次 `pip freeze > requirements.txt`
- 之后本地和 GitHub Actions 都用 `requirements.txt` 安装，保证环境稳定可复现

也就是说，本文默认你用的是：

- `Material for MkDocs 9.x`
- 与之兼容的 `MkDocs 1.x`
- 配置文件仍然是经典的 `mkdocs.yml`

---

## 2. 你需要提前准备什么

至少准备下面这些：

- 一个 GitHub 账号
- `Python 3.11` 或 `Python 3.12`
- `Git`
- 一个编辑器，推荐 `VS Code`

### 2.1 安装 Python

去 Python 官网下载安装包：

- <https://www.python.org/downloads/>

安装时务必勾选：

- `Add python.exe to PATH`

安装好后，在 PowerShell 里检查：

```powershell
python --version
pip --version
```

### 2.2 安装 Git

Git 官网：

- <https://git-scm.com/download/win>

安装完成后检查：

```powershell
git --version
```

### 2.3 可选：安装 VS Code

VS Code 官网：

- <https://code.visualstudio.com/>

推荐顺手装两个扩展：

- `Markdown All in One`
- `YAML`

---

## 3. 在本地创建博客项目

假设你打算把整个博客就放在一个文件夹里。

### 3.1 进入项目目录

```powershell
cd "你的项目目录"
```

如果你还没有目录，可以先新建：

```powershell
mkdir my-notes-blog
cd .\my-notes-blog
```

### 3.2 创建虚拟环境

```powershell
python -m venv .venv
```

激活：

```powershell
.\.venv\Scripts\Activate.ps1
```

如果 PowerShell 提示脚本执行被禁用，可以先执行：

```powershell
Set-ExecutionPolicy -Scope CurrentUser RemoteSigned
```

然后重新打开 PowerShell 再激活虚拟环境。

### 3.3 安装 MkDocs 和 Material

```powershell
python -m pip install --upgrade pip
pip install "mkdocs-material==9.*"
```

安装完成后，把当前环境锁定下来：

```powershell
pip freeze > requirements.txt
```

以后别人或者 GitHub Actions 只要执行：

```powershell
pip install -r requirements.txt
```

就能装到和你本机一致的版本。

### 3.4 初始化站点

在项目根目录执行：

```powershell
mkdocs new .
```

执行后，目录通常会变成这样：

```text
.
├─ docs/
│  └─ index.md
└─ mkdocs.yml
```

---

## 4. 建议你一开始就整理成这样的目录结构

对于“专业课笔记博客”，我推荐文件夹名尽量用英文或拼音，页面标题再写中文。这样 URL 更稳，后续迁移也更省心。

推荐结构示例：

```text
.
├─ .github/
│  └─ workflows/
│     └─ deploy.yml
├─ docs/
│  ├─ index.md
│  ├─ professional/
│  │  ├─ index.md
│  │  ├─ digital-logic.md
│  │  └─ computer-organization.md
│  ├─ algorithms/
│  │  ├─ index.md
│  │  └─ graph.md
│  ├─ blog/
│  │  ├─ index.md
│  │  └─ posts/
│  │     └─ 2026-03-30-my-first-post.md
│  ├─ assets/
│  │  ├─ logo.png
│  │  └─ favicon.png
│  └─ stylesheets/
│     └─ extra.css
├─ .gitignore
├─ mkdocs.yml
└─ requirements.txt
```

说明：

- `docs/` 里放你所有 Markdown 内容
- `professional/` 放专业课笔记
- `algorithms/` 放算法、刷题、方法总结
- `blog/posts/` 放偏“文章式”的博文
- `stylesheets/extra.css` 放你自己的主题微调
- `.github/workflows/deploy.yml` 用于自动部署到 GitHub Pages

---

## 5. 先写一版可直接用的 `mkdocs.yml`

把 `mkdocs.yml` 改成下面这样。你可以先直接照抄，后面再一点点改。

```yaml
site_name: 我的专业课笔记
site_description: 课程笔记、知识总结与学习记录
site_author: 你的名字
site_url: https://<你的GitHub用户名>.github.io/<仓库名>/
repo_url: https://github.com/<你的GitHub用户名>/<仓库名>
repo_name: <你的GitHub用户名>/<仓库名>
edit_uri: edit/main/docs/

theme:
  name: material
  language: zh
  font: false
  icon:
    logo: material/book-open-page-variant
    repo: fontawesome/brands/github
  features:
    - navigation.tabs
    - navigation.sections
    - navigation.indexes
    - navigation.top
    - content.code.copy
    - content.action.edit
    - search.suggest
    - search.highlight
  palette:
    - media: "(prefers-color-scheme)"
      toggle:
        icon: material/brightness-auto
        name: 跟随系统
    - media: "(prefers-color-scheme: light)"
      scheme: default
      primary: blue grey
      accent: indigo
      toggle:
        icon: material/weather-night
        name: 切换到深色模式
    - media: "(prefers-color-scheme: dark)"
      scheme: slate
      primary: black
      accent: lime
      toggle:
        icon: material/weather-sunny
        name: 切换到浅色模式

nav:
  - 首页: index.md
  - 专业课:
    - professional/index.md
    - 数字电路与逻辑设计: professional/digital-logic.md
    - 计算机组成原理: professional/computer-organization.md
  - 算法:
    - algorithms/index.md
    - 图论: algorithms/graph.md
  - 博客:
    - blog/index.md

plugins:
  - search
  - blog:
      blog_dir: blog

markdown_extensions:
  - admonition
  - attr_list
  - md_in_html
  - tables
  - toc:
      permalink: true
  - pymdownx.details
  - pymdownx.superfences
  - pymdownx.highlight:
      anchor_linenums: true
  - pymdownx.inlinehilite
  - pymdownx.emoji:
      emoji_index: !!python/name:material.extensions.emoji.twemoji
      emoji_generator: !!python/name:material.extensions.emoji.to_svg

extra_css:
  - stylesheets/extra.css

extra:
  social:
    - icon: fontawesome/brands/github
      link: https://github.com/<你的GitHub用户名>

copyright: Copyright &copy; 2026 你的名字
```

### 5.1 这里面最重要的几个字段

`site_url`

- 如果你的仓库名不是 `<用户名>.github.io`
- 那么它通常应该写成 `https://<用户名>.github.io/<仓库名>/`
- 这个路径后面的仓库名和最后那个斜杠都不要漏

`repo_url`

- 填你的 GitHub 仓库地址
- 这样站点右上角会出现仓库入口

`edit_uri`

- 配合 `content.action.edit` 使用
- 页面右上角会出现“编辑此页”按钮
- 点进去能直接跳到 GitHub 上对应 Markdown 文件

`font: false`

- 这是我比较推荐的配置
- 因为 Material 默认会使用 Google Fonts
- 如果你更想稳定一些，或者不想依赖外部字体，可以先关闭自动加载，然后用自己的 CSS 字体栈

---

## 6. 先把基础页面补齐

按上面的 `nav`，你至少需要先创建这些文件：

```text
docs/index.md
docs/professional/index.md
docs/professional/digital-logic.md
docs/professional/computer-organization.md
docs/algorithms/index.md
docs/algorithms/graph.md
docs/blog/index.md
docs/blog/posts/2026-03-30-my-first-post.md
docs/stylesheets/extra.css
```

### 6.1 首页 `docs/index.md`

```markdown
# 欢迎来到我的笔记站

这里用来整理我的专业课笔记、算法总结和学习记录。

## 你可以从这里开始

- [专业课](professional/index.md)
- [算法](algorithms/index.md)
- [博客](blog/index.md)
```

### 6.2 专业课栏目首页 `docs/professional/index.md`

```markdown
# 专业课

这里集中整理课程笔记、概念总结、期末复习材料和配套图示。

## 当前栏目

- [数字电路与逻辑设计](digital-logic.md)
- [计算机组成原理](computer-organization.md)
```

### 6.3 一篇课程笔记示例 `docs/professional/digital-logic.md`

```markdown
# 数字电路与逻辑设计

## 课程定位

这门课主要讨论：

- 数制与编码
- 逻辑代数
- 组合逻辑电路
- 时序逻辑电路

## 一个小例子

!!! note "复习提示"
    先把组合逻辑和时序逻辑的区别记牢，再去刷题会轻松很多。

## 后续计划

- [ ] 补 Karnaugh 图
- [ ] 补编码器与译码器
- [ ] 补触发器与寄存器
```

### 6.4 博客首页 `docs/blog/index.md`

```markdown
# 博客

这里放偏文章式的内容，比如学习周报、阶段总结、课程复盘、踩坑记录等。
```

### 6.5 第一篇博文 `docs/blog/posts/2026-03-30-my-first-post.md`

```markdown
---
date: 2026-03-30
categories:
  - 学习记录
  - 建站
draft: false
---

# 我的第一篇文章

今天把基于 MkDocs 的个人笔记博客搭起来了。

<!-- more -->

后面我会在这里持续整理专业课笔记、算法总结和复习资料。
```

### 6.6 自定义样式 `docs/stylesheets/extra.css`

```css
:root {
  --md-text-font: "PingFang SC", "Hiragino Sans GB", "Microsoft YaHei",
    "Noto Sans CJK SC", sans-serif;
  --md-code-font: "JetBrains Mono", "Cascadia Code", "Consolas", monospace;
  --md-primary-fg-color: #334155;
  --md-accent-fg-color: #2563eb;
}

.md-typeset h1,
.md-typeset h2,
.md-typeset h3 {
  font-weight: 700;
}

.md-typeset code {
  border-radius: 0.35rem;
}
```

---

## 7. 本地预览博客

在项目根目录执行：

```powershell
mkdocs serve
```

浏览器打开：

- <http://127.0.0.1:8000/>

以后你每次改 Markdown，网页通常会自动刷新。

如果项目内容越来越多、热更新变慢，可以试试：

```powershell
mkdocs serve --dirtyreload
```

---

## 8. 以后怎么写新内容

你日常真正要做的事情，其实主要只有两种：

- 新增一篇“课程笔记页”
- 新增一篇“博客文章”

### 8.1 新增课程笔记页

假设你要新增“操作系统”栏目下的一篇页面。

第一步，创建文件：

```text
docs/professional/operating-system.md
```

第二步，写内容：

```markdown
# 操作系统

## 章节目录

- 进程与线程
- 同步与互斥
- 内存管理
- 文件系统
```

第三步，把它挂到 `mkdocs.yml` 的 `nav` 里：

```yaml
nav:
  - 首页: index.md
  - 专业课:
    - professional/index.md
    - 数字电路与逻辑设计: professional/digital-logic.md
    - 计算机组成原理: professional/computer-organization.md
    - 操作系统: professional/operating-system.md
```

第四步，本地预览：

```powershell
mkdocs serve
```

### 8.2 新增一篇博客文章

如果你想写一篇更像“文章”的内容，就放到：

```text
docs/blog/posts/
```

比如新建：

```text
docs/blog/posts/2026-04-01-digital-logic-review.md
```

内容示例：

```markdown
---
date:
  created: 2026-04-01
  updated: 2026-04-02
categories:
  - 数字电路
  - 复习总结
draft: false
---

# 数字电路第一轮复习总结

这篇文章记录我复习数字电路第一轮时整理出的高频考点。

<!-- more -->

## 组合逻辑

...
```

注意：

- 博客文章不需要手动写到 `nav` 里
- Material 官方文档明确建议：有了 `blog/index.md` 之后，只把博客首页挂到导航里，不要把每篇文章都塞进 `nav`

---

## 9. 怎么“新建一个栏目”

这是你后面最常做的动作之一。流程非常固定。

假设你想新增一个“数学基础”栏目。

### 9.1 创建目录和首页

```text
docs/math/index.md
docs/math/discrete-math.md
docs/math/probability.md
```

`docs/math/index.md` 可以先写：

```markdown
# 数学基础

这里整理离散数学、概率论、线性代数等基础内容。

## 目录

- [离散数学](discrete-math.md)
- [概率论](probability.md)
```

### 9.2 在 `mkdocs.yml` 的 `nav` 里加进去

```yaml
nav:
  - 首页: index.md
  - 专业课:
    - professional/index.md
    - 数字电路与逻辑设计: professional/digital-logic.md
    - 计算机组成原理: professional/computer-organization.md
  - 数学基础:
    - math/index.md
    - 离散数学: math/discrete-math.md
    - 概率论: math/probability.md
  - 算法:
    - algorithms/index.md
    - 图论: algorithms/graph.md
  - 博客:
    - blog/index.md
```

### 9.3 本地检查效果

```powershell
mkdocs serve
```

只要目录和 `nav` 对应上了，一个新栏目就完成了。

---

## 10. 怎么自定义主题

你提到想做一些主题定制，这部分我按“从简单到进阶”的顺序讲。

### 10.1 改颜色

最简单的方法就是改 `theme.palette`。

例如把主色调改成更偏知识库、笔记站的冷色风格：

```yaml
theme:
  palette:
    - media: "(prefers-color-scheme: light)"
      scheme: default
      primary: blue grey
      accent: indigo
    - media: "(prefers-color-scheme: dark)"
      scheme: slate
      primary: black
      accent: lime
```

如果你想再进一步微调，可以在 `extra.css` 里覆盖 CSS 变量：

```css
:root {
  --md-primary-fg-color: #1e293b;
  --md-accent-fg-color: #0f766e;
}
```

### 10.2 改字体

因为前面我们用了：

```yaml
theme:
  font: false
```

所以字体主要通过 `extra.css` 控制：

```css
:root {
  --md-text-font: "PingFang SC", "Hiragino Sans GB", "Microsoft YaHei",
    "Noto Sans CJK SC", sans-serif;
  --md-code-font: "JetBrains Mono", "Cascadia Code", "Consolas", monospace;
}
```

如果你以后想自托管字体，也可以在 `extra.css` 里加 `@font-face`。

### 10.3 换 logo 和 favicon

把图片放到：

```text
docs/assets/logo.png
docs/assets/favicon.png
```

然后在 `mkdocs.yml` 里写：

```yaml
theme:
  logo: assets/logo.png
  favicon: assets/favicon.png
```

如果你不想用图片，也可以直接用 Material 内置图标：

```yaml
theme:
  icon:
    logo: material/book-open-page-variant
```

### 10.4 加一点更像“个人知识站”的样式

比如把正文区域稍微拉宽、标题更明显、表格和代码块更清爽：

```css
.md-grid {
  max-width: 1440px;
}

.md-content__inner {
  margin-bottom: 3rem;
}

.md-typeset table:not([class]) {
  font-size: 0.92rem;
}

.md-typeset h2 {
  border-bottom: 1px solid rgba(148, 163, 184, 0.25);
  padding-bottom: 0.35rem;
}
```

### 10.5 想更像 OI Wiki，可以怎么做

如果你只是想做“知识站感”更强的风格，下面几件事最有帮助：

- 顶部开 `navigation.tabs`
- 左侧开 `navigation.sections`
- 每个栏目都单独放 `index.md`
- 保持目录层级清晰，不要一股脑堆在首页
- 颜色不要太花，主色最好 1 到 2 个
- 重点内容多用提示块、代码块、表格、目录锚点

如果你以后想做更深的 HTML 模板级定制，可以使用 Material 的 `overrides` 机制：

```yaml
theme:
  name: material
  custom_dir: overrides
```

然后在项目根目录新建：

```text
overrides/
```

后面你就能覆盖主题局部模板，而不需要直接 fork 整个主题。

---

## 11. 发布到 GitHub Pages

这一段是整套流程里最关键的。

我建议你用：

- GitHub 仓库保存源码
- GitHub Actions 自动执行 `mkdocs gh-deploy --force`
- GitHub Pages 从 `gh-pages` 分支发布

这样最省心。

### 11.1 先创建 GitHub 仓库

去 GitHub 新建一个仓库，比如：

- 仓库名：`course-notes-blog`

如果你是普通个人账号，建议先用公开仓库，这样 GitHub Pages 最稳。

### 11.2 本地初始化 Git 并推上去

在项目根目录执行：

```powershell
git init
git branch -M main
git remote add origin https://github.com/<你的GitHub用户名>/<仓库名>.git
```

建议加一个 `.gitignore`：

```gitignore
.venv/
site/
__pycache__/
.cache/
```

然后第一次提交：

```powershell
git add .
git commit -m "init mkdocs notes blog"
git push -u origin main
```

### 11.3 添加 GitHub Actions 自动部署文件

在项目根目录创建：

```text
.github/workflows/deploy.yml
```

内容如下：

```yaml
name: deploy-mkdocs

on:
  push:
    branches:
      - main

permissions:
  contents: write

jobs:
  deploy:
    runs-on: ubuntu-latest
    steps:
      - name: Checkout
        uses: actions/checkout@v4

      - name: Configure Git Credentials
        run: |
          git config user.name github-actions[bot]
          git config user.email 41898282+github-actions[bot]@users.noreply.github.com

      - name: Set up Python
        uses: actions/setup-python@v5
        with:
          python-version: "3.12"

      - name: Install dependencies
        run: pip install -r requirements.txt

      - name: Deploy
        run: mkdocs gh-deploy --force
```

这个流程的含义是：

- 只要你往 `main` 推送内容
- GitHub 就会自动安装依赖
- 自动构建站点
- 自动把生成好的静态文件推到 `gh-pages` 分支

### 11.4 去 GitHub 仓库设置里打开 Pages

进入：

- `Settings`
- `Pages`

然后设置：

- `Source`: `Deploy from a branch`
- `Branch`: `gh-pages`
- `Folder`: `/(root)`

这里特别提醒一下：

- GitHub Pages 现在也支持 `GitHub Actions` 作为发布源
- 但本文这套流程用的是 Material 官方给出的 `mkdocs gh-deploy` 方案
- 这种方案会把产物推到 `gh-pages` 分支，所以 Pages 这里仍然要选 `Deploy from a branch`

### 11.5 再推一次代码触发部署

```powershell
git add .
git commit -m "add github pages deployment"
git push
```

等 GitHub Actions 跑完后，你的站点通常会出现在：

- `https://<你的GitHub用户名>.github.io/<仓库名>/`

如果你的仓库刚好叫：

- `<你的GitHub用户名>.github.io`

那么地址一般就是：

- `https://<你的GitHub用户名>.github.io/`

---

## 12. 以后怎么更新博客内容

你以后日常更新其实就是下面这套固定动作：

### 12.1 打开项目并激活环境

```powershell
cd "你的项目目录"
.\.venv\Scripts\Activate.ps1
```

### 12.2 本地预览

```powershell
mkdocs serve
```

### 12.3 新增或修改内容

例如：

- 改 `docs/professional/digital-logic.md`
- 新建 `docs/blog/posts/2026-04-10-os-review.md`
- 调整 `mkdocs.yml` 里的导航
- 修改 `docs/stylesheets/extra.css`

### 12.4 本地先检查一次构建

我建议每次推送前都跑一次：

```powershell
mkdocs build --strict
```

如果这里没报错，再提交：

```powershell
git add .
git commit -m "update notes"
git push
```

推上去以后，GitHub Actions 会自动部署。

---

## 13. 图片、附件、代码块怎么放

### 13.1 图片

推荐把图片统一放在：

```text
docs/assets/images/
```

例如：

```text
docs/assets/images/digital-logic/kmap-01.png
```

然后在 Markdown 里这样引用：

```markdown
![卡诺图示意](../assets/images/digital-logic/kmap-01.png)
```

如果当前页面和图片层级不同，注意相对路径要对应调整。

### 13.2 PDF 或课件

可以放在：

```text
docs/assets/files/
```

然后用 Markdown 链接：

```markdown
[下载课件](../assets/files/chapter1.pdf)
```

### 13.3 代码块

Material 对代码块支持很好，直接写：

````markdown
```cpp
#include <bits/stdc++.h>
using namespace std;

int main() {
    cout << "Hello, world!" << endl;
}
```
````

---

## 14. 常见问题排查

### 14.1 GitHub Pages 打开是 404

先检查这几项：

- GitHub 仓库的 `Pages` 是否已经选成 `gh-pages / (root)`
- GitHub Actions 是否成功执行
- `site_url` 里有没有写错仓库名
- 仓库是不是刚创建不久，还没完全生效

### 14.2 样式没生效

检查：

- `mkdocs.yml` 里有没有写 `extra_css`
- 文件是不是放在 `docs/stylesheets/extra.css`
- 路径是不是写成了 `stylesheets/extra.css`

### 14.3 本地能跑，GitHub Actions 失败

优先检查：

- 你有没有把 `requirements.txt` 提交上去
- 本地是不是装了额外插件，但 `requirements.txt` 里没有
- `mkdocs.yml` 里引用了文件，但仓库里没提交

### 14.4 导航报错或页面丢失

检查：

- `nav` 里写的路径是否真实存在
- 大小写是否一致
- 文件是不是放错目录

### 14.5 中文字体不好看

可以继续微调 `extra.css` 里的字体栈，或者自己下载字体后用 `@font-face` 自托管。

---

## 15. 一个适合你长期维护的工作流

如果你是拿它存专业课笔记，我建议你把内容分成三层：

### 15.1 第一层：课程页

比如：

- 数字电路
- 计算机组成原理
- 操作系统
- 数据库

这层是“课程维度”。

### 15.2 第二层：专题页

比如在“数字电路”下面继续分：

- 数制与编码
- 逻辑代数
- 组合逻辑
- 时序逻辑

这层是“知识点维度”。

### 15.3 第三层：博客页

比如：

- 某门课复习总结
- 期中前 7 天冲刺记录
- 某次实验踩坑记录

这层更像“时间线维度”。

这样你的网站既像知识库，也保留博客感，后面内容多了也不会乱。

---

## 16. 你可以直接照着执行的最短路径

如果你想先快速跑起来，不想一下看太多，可以只做这 10 步：

1. 安装 Python、Git、VS Code
2. 新建项目文件夹
3. `python -m venv .venv`
4. `.\.venv\Scripts\Activate.ps1`
5. `pip install "mkdocs-material==9.*"`
6. `pip freeze > requirements.txt`
7. `mkdocs new .`
8. 按本文提供的 `mkdocs.yml` 改配置
9. `mkdocs serve` 本地预览
10. 配好 `.github/workflows/deploy.yml`，推到 GitHub，打开 Pages

做完这 10 步，你的站就已经能跑起来了。

---

## 17. 官方文档参考

下面这些都是我整理这份手册时重点参考的官方文档，后面你想继续深挖时可以直接看：

- MkDocs User Guide: <https://www.mkdocs.org/user-guide/>
- MkDocs 配置文档: <https://www.mkdocs.org/user-guide/configuration/>
- Material 安装文档: <https://squidfunk.github.io/mkdocs-material/getting-started/>
- Material 创建站点: <https://squidfunk.github.io/mkdocs-material/creating-your-site/>
- Material 发布站点: <https://squidfunk.github.io/mkdocs-material/publishing-your-site/>
- Material 颜色配置: <https://squidfunk.github.io/mkdocs-material/setup/changing-the-colors/>
- Material 字体配置: <https://squidfunk.github.io/mkdocs-material/setup/changing-the-fonts/>
- Material 自定义主题: <https://squidfunk.github.io/mkdocs-material/customization/>
- Material 博客插件: <https://squidfunk.github.io/mkdocs-material/setup/setting-up-a-blog/>
- Material logo / icon 配置: <https://squidfunk.github.io/mkdocs-material/setup/changing-the-logo-and-icons/>
- GitHub Pages 发布源设置: <https://docs.github.com/en/github/working-with-github-pages/configuring-a-publishing-source-for-your-github-pages-site>
- GitHub Pages 自定义工作流: <https://docs.github.com/en/pages/getting-started-with-github-pages/using-custom-workflows-with-github-pages>

---

## 18. 最后的建议

如果你的目标是“长期记专业课笔记”，那最重要的不是一开始把主题折腾得多华丽，而是先把这三件事固定下来：

- 文件命名规则
- 栏目结构
- 每周更新节奏

只要这三件事固定住，这个博客会越写越顺手。

如果你愿意，下一步最适合做的是：

1. 让我继续直接帮你把这个博客的初始目录和配置文件也一起搭出来
2. 或者让我先按你的专业课目录，帮你生成一版更贴近你课程体系的 `mkdocs.yml` 和 `docs/` 结构

