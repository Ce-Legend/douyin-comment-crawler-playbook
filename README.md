# Douyin Comment Crawler Playbook

抖音评论爬虫 / Douyin comment crawler 的一次真实项目复盘。一份踩坑地图：需求怎么问清楚、入口什么时候该换、低量数据怎么解释、最后怎么交付得让人能查。

![Python](https://img.shields.io/badge/Python-3.10%2B-3776AB?logo=python&logoColor=white)
![License](https://img.shields.io/badge/license-MIT-green)
![Type](https://img.shields.io/badge/type-playbook%20%2B%20templates-blue)

关键词：抖音爬虫、抖音评论爬虫、抖音评论采集、短视频评论采集、Douyin crawler、Douyin comment crawler、social media comment collection。

## 🌱 这个 repo 是什么

前阵子做过一个抖音车型评论采集项目。

一开始看起来很简单：给一批车型名，去抖音网页端搜评论，整理成 JSON。

真做起来才发现，真正麻烦的地方藏在这些环节：

- 有些方案跑得很快，但热门车型也采不到，结果明显不可信。
- 新开页面、复用登录页、前台页、后台页，稳定性完全不一样。
- 客户给的车型名经常和平台里的搜索词对不上，简称、别名、大小写差异都要处理。
- 冷门车型采不到 1000 条，仍然可以合格交付，前提是把原因说清楚。
- 最后交付不能只发一个 JSON，要有统计、低量说明、字段说明、校验结果。

所以我把这次项目里真正有用的部分抽出来，做成这个 playbook。以后你做抖音评论采集、短视频评论采集、社媒评论分析，至少可以少踩几个坑。

## 🚀 先跑一下

这个仓库只有脱敏样例和辅助脚本，不包含真实评论、不包含 cookie、不包含账号信息。

```bash
git clone https://github.com/Ce-Legend/douyin-comment-crawler-playbook.git
cd douyin-comment-crawler-playbook
```

校验样例数据：

```bash
python3 scripts/validate_output.py examples/comments.sample.json
```

生成一份交付报告草稿：

```bash
python3 scripts/build_delivery_report.py examples/comments.sample.json --output delivery_report.sample.md
```

## 📦 里面有什么

```text
.
├── README.md
├── docs/
│   ├── 01-requirement-boundary.md      # 需求边界怎么问
│   ├── 02-failed-approaches.md         # 跑得快但不可信，怎么判断
│   ├── 03-strategy-turning-points.md   # 几次关键转向
│   ├── 04-quality-checklist.md         # 交付前检查什么
│   ├── 05-delivery-template.md         # 交付说明模板
│   └── 07-ethics-and-compliance.md     # 合规和脱敏边界
├── examples/
│   ├── input_models.sample.csv
│   └── comments.sample.json
└── scripts/
    ├── build_delivery_report.py
    └── validate_output.py
```

## 🧭 我最想留下来的几个经验

### 1. 脚本没报错，数据也可能失真

第一版方案也能跑，文件也能生成，速度还挺快。

但问题是：大量车型返回 0，连一些常识上应该有讨论量的热门车型也没有数据。

这时候别急着解释平台上没数据。先停下来确认一件事：

到底是目标真的没数据，还是我的采集入口失真了？

这个问题救了后面一大截时间。

### 2. 入口比并发更重要

我后来放弃了盲目批量搜索，改成先复用已登录、肉眼确认过有内容的真实搜索页，再让脚本接管。

这个方案不酷，但更稳。

爬虫项目里经常会这样：你以为要加并发，其实应该先换入口。

### 3. 客户给的名字，不一定是平台里的搜索词

最终结果要按客户给的原始车型名归档，这没问题。

但搜索时最好允许别名：

```csv
canonical_name,search_keyword,reason
Sample Model A,Sample Model A,original input
Sample Model A,Brand A Model A,platform title pattern
Sample Model A,ModelA,common short name
```

这样既不乱改客户的字段，又能提高召回。

### 4. 低量要解释，不能硬凑

冷门车型、新车、概念车、时间范围很窄的时候，采不到目标量很正常。

更重要的是把这件事讲清楚：

- 尝试过哪些关键词。
- 有多少公开视频。
- 有多少有效评论。
- 为什么不继续补。
- 有没有用无关评论凑数。

比起假装补满，诚实的低量说明更有价值。

### 5. 好的交付包应该能被别人复查

最后不要只给一个 `comments.json`。

至少要有：

- 完整 JSON。
- 按目标拆分的 JSON。
- 每个目标的统计表。
- 低量目标说明。
- 字段说明。
- 质量校验报告。
- 来源 URL，方便抽样核对。

## 🧩 推荐输出结构

样例数据放在 [examples/comments.sample.json](examples/comments.sample.json)。

核心结构是：

```json
[
  {
    "model": "Sample Model A",
    "stats": {
      "validCommentCount": 2,
      "videoCount": 1
    },
    "videos": [
      {
        "videoId": "video_001",
        "title": "Sample Model A owner review",
        "videoUrl": "https://example.com/video/video_001",
        "createTime": "2026-05-01 10:00:00",
        "comments": [
          {
            "commentId": "comment_001",
            "content": "The cabin is quiet, but the rear row feels small.",
            "createTime": "2026-05-02 12:30:00"
          }
        ]
      }
    ]
  }
]
```

## ✅ 校验脚本会查什么

[scripts/validate_output.py](scripts/validate_output.py) 会做最基础的交付检查：

- 顶层 JSON 是否是列表。
- 每个目标是否有视频列表。
- 视频是否缺 `videoUrl`。
- 评论是否缺 `commentId`、`content`、`createTime`。
- 评论时间是否能解析。
- 评论时间是否越界。
- 同目标同视频下是否有重复评论。

示例：

```bash
python3 scripts/validate_output.py examples/comments.sample.json --start 2026-04-01 --end "2026-05-08 23:59:59"
```

## 📝 报告脚本会生成什么

[scripts/build_delivery_report.py](scripts/build_delivery_report.py) 会根据 JSON 生成一份 Markdown 报告草稿：

- 总目标数。
- 有数据 / 0 数据目标数。
- 视频数。
- 评论数。
- 缺 URL、缺时间、重复数。
- 每个目标的明细。
- 低量目标列表。

示例：

```bash
python3 scripts/build_delivery_report.py examples/comments.sample.json --output delivery_report.sample.md --low-threshold 100
```

## 🔒 开源时别放这些

这个 repo 只放方法、模板和脱敏样例。

不要把这些东西推上 GitHub：

- 真实评论数据。
- 客户原始 Excel。
- 微信聊天记录。
- cookie、账号、浏览器 profile。
- 验证码截图。
- `.env`、token、密钥。
- 可直接滥用的大规模采集配置。

详细边界见 [docs/07-ethics-and-compliance.md](docs/07-ethics-and-compliance.md)。

## 🙌 参考

写 README 的时候参考了一些成熟项目的组织方式：

- [yt-dlp](https://github.com/yt-dlp/yt-dlp)：首屏直接告诉你项目是什么，然后给安装和使用。
- [MediaCrawler](https://opendeep.wiki/NanmiCoder/MediaCrawler/getting-started)：多平台公开信息采集系统的结构参考。
- [Douyin_TikTok_Download_API](https://cnb.cool/ChaiKing0/v0020_Douyin_TikTok_Download_API/-/blob/main/README.en.md)：中英双语关键词和功能入口参考。
- [GitHub README docs](https://docs.github.com/en/repositories/managing-your-repositorys-settings-and-features/customizing-your-repository/about-readmes)：README 会被 GitHub 自动展示给仓库访问者。
- [GitHub repository search docs](https://github.com/github/docs/blob/main/content/search-github/searching-on-github/searching-for-repositories.md)：GitHub 搜索会用到仓库名、描述、topics 和 README。

## 📄 License

MIT
