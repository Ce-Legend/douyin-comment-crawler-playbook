# 06. GitHub 可发现性设置

这个项目要让别人搜索“抖音爬虫”“抖音评论爬虫”“Douyin crawler”时更容易找到，所以发布时不能只写一个抽象项目名。

## 推荐仓库名

```text
douyin-comment-crawler-playbook
```

原因：

- `douyin` 命中英文搜索。
- `comment` 明确是评论，不是下载视频。
- `crawler` 命中爬虫搜索。
- `playbook` 表示最佳实践和项目复盘，不是单纯脚本。

## 推荐 Description

```text
抖音评论爬虫与短视频评论采集最佳实践：真实项目复盘，覆盖需求边界、登录态、验证码、低量样本、别名搜索、质量校验和交付模板。
```

备选英文版：

```text
Douyin comment crawler playbook: a real-world case study for short video comment collection, login sessions, CAPTCHA handling, aliases, validation, and delivery.
```

## 推荐 Topics

```text
douyin
douyin-crawler
douyin-comments
comment-crawler
web-scraping
playwright
data-collection
social-media-analysis
crawler-playbook
data-delivery
best-practices
```

## README 首屏原则

首屏必须包含：

- `抖音爬虫`
- `抖音评论爬虫`
- `Douyin crawler`
- `Douyin comment crawler`
- `短视频评论采集`
- `评论数据采集`

但不能堆砌关键词。更好的方式是把关键词放进自然描述：

```md
一个真实抖音评论爬虫 / Douyin crawler 项目的脱敏复盘：从需求边界、错误路线、登录态、验证码、低量样本、车型别名，到最终可验证交付。
```

## 内容定位

不要把项目定位成：

```text
最强抖音爬虫，一键抓取所有评论
```

更好的定位是：

```text
抖音评论采集项目的最佳实践和工程复盘。
```

这样更安全，也更有长期价值。

## 发布后检查

发布后可以用这些搜索验证：

```text
抖音评论爬虫 site:github.com
douyin comment crawler site:github.com
douyin crawler playbook site:github.com
```

GitHub 站内可以搜：

```text
douyin comment crawler in:name,description,readme
抖音 评论 爬虫
topic:douyin crawler
```

如果搜不到，优先检查：

- 仓库是否 public。
- 仓库名是否包含 `douyin` / `crawler`。
- Description 是否写了中文核心词。
- Topics 是否设置。
- README 首屏是否包含目标关键词。

