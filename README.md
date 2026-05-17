# Douyin Comment Crawler Playbook | 抖音评论爬虫最佳实践

一个真实抖音评论爬虫 / Douyin crawler 项目的脱敏复盘：从需求边界、错误路线、登录态、验证码、低量样本、车型别名，到最终可验证交付。

这个仓库不是“万能抖音爬虫脚本”，也不鼓励绕过平台限制。它沉淀的是一套可复用的工程实践：当你接到一个真实的抖音评论采集、短视频评论采集、社媒公开评论分析需求时，如何先判断数据是否可信，如何在方案失效时转向，如何把结果做成客户或协作者可以复查的交付物。

> English keywords: Douyin crawler, Douyin comment crawler, short video comment scraping, social media comment collection, crawler playbook.

> 中文关键词：抖音爬虫、抖音评论爬虫、抖音评论采集、短视频评论采集、评论数据采集、爬虫项目复盘、数据交付最佳实践。

## GitHub 仓库信息建议

如果你要把这个项目发布到 GitHub，建议这样设置：

- Repository name：`douyin-comment-crawler-playbook`
- Description：`抖音评论爬虫与短视频评论采集最佳实践：真实项目复盘，覆盖需求边界、登录态、验证码、低量样本、别名搜索、质量校验和交付模板。`
- Website：可以先留空，后续放作品集项目页。
- Topics：

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

为什么要这样写：

- GitHub 搜索可以按仓库名、描述、Topics、README 命中。
- “抖音爬虫”和 “Douyin crawler” 都要在首屏出现。
- 标题负责被搜到，正文负责建立信任。
- Topics 用英文更利于 GitHub 站内聚合。

## 适合谁看

- 接外包数据采集任务的人。
- 需要做短视频、社媒、评论类公开数据研究的人。
- 想把一次临时脚本升级成可交付流程的人。
- 想了解真实采集项目中“为什么不是写完脚本就结束”的人。

## 这个项目解决什么问题

真实抖音爬虫需求通常不会像教程里那样干净。

这次项目的原始目标是：按一批车型名称，在短视频平台网页端采集近期评论，整理成 JSON。客户需要：

- 按车型组织数据。
- 每个视频下面挂评论列表。
- 每条评论保留真实评论时间。
- 每条视频保留可核对 URL。
- 过滤明显无关、重复、表情包、水军评论。
- 每个车型希望尽量达到目标评论量。
- 冷门车型按实际公开可见数据交付，不能硬凑。
- 先给样例确认，再推进全量。

这个需求表面看是“写一个抖音评论爬虫”，实际难点是：

- 搜索结果是否真实代表目标车型。
- 采集入口是否稳定。
- 登录态和验证码如何处理中断。
- 冷门车型和新车型是否天然低量。
- 车型名称是否存在别名、大小写、同形字符、版本名差异。
- 数据不足时如何解释，而不是伪造完整。
- 交付物如何让别人复查。

## 项目中真正有价值的转折

### 1. 跑得快不等于数据可信

第一版方案用了更自动化的批量搜索路线。它看起来很快，也没有明显报错，但出现了一个危险信号：

- 大量车型返回 0。
- 一些热门车型也没有评论。
- 日志没有明显失败。
- 这和常识冲突。

这里的关键判断是：不要把“脚本没报错”当成“数据真实为空”。

当采集结果和常识冲突时，优先怀疑采集入口、搜索结果、登录态、页面状态，而不是立刻向客户解释“没有数据”。

### 2. 从全自动批量搜索，转向已登录真实页面

后续方案改成复用已登录浏览器中的真实搜索页，通过浏览器调试接口连接现有页面，减少新页面、新会话、空壳页面和异常验证带来的不确定性。

这次转向的原则是：

- 先让人眼能看到页面上确实有相关视频。
- 再让脚本接管当前页面。
- 先跑少量车型验证增长。
- 再补低量车型。
- 遇到验证码时暂停等待人工处理，不盲目硬跑。

这不是技术上最“酷”的方案，但它更接近真实交付所需的稳定性。

### 3. 从“车型名精确搜索”，转向“原名落盘 + 别名搜索”

客户要求使用 Excel 里的车型名。实际执行中发现，平台内容里的标题和用户评论未必使用同一个名字。

常见问题：

- 英文大小写不一致。
- 数字和字母相似，例如 `O/0`。
- 用户更常用简称。
- 车型版本名、品牌名前缀、后缀混用。
- 新车、概念车、改款车公开内容天然较少。

因此更稳的做法是：

- 最终结果仍按客户原始车型名归档。
- 搜索时允许配置多个候选关键词。
- 每个关键词的来源和效果要记录。
- 低量车型不能简单判定失败，要保留实际尝试过的入口和理由。

### 4. 从“采到数据”升级为“可验收交付”

最后交付不能只给一个 JSON。

应该同步给：

- 主 JSON。
- 按车型拆分的 JSON。
- 车型统计表。
- 低量车型说明。
- 样例说明。
- 字段说明。
- 质量校验结果。

交付前至少检查：

- 重复评论。
- 缺失视频 URL。
- 缺失评论时间。
- 评论时间越界。
- 单视频评论数超限。
- 明显排序异常。
- 车型归档错误。
- 低量车型是否有解释。

## 和普通抖音爬虫项目有什么不同

很多开源仓库重点解决“怎么抓到数据”。

这个仓库重点解决“怎么把数据采集项目做可信、做可交付、做可复盘”。

| 常见抖音爬虫仓库 | 本仓库 |
|---|---|
| 强调接口、参数、下载、抓取能力 | 强调需求边界、异常判断、转向过程、验收标准 |
| 目标是让脚本跑起来 | 目标是让项目结果可解释、可复查、可交付 |
| 关注单次抓取成功 | 关注长任务里的登录态、验证码、低量、别名、质量校验 |
| 输出代码为主 | 输出方法论、模板、样例和校验脚本 |

所以它更适合作为：

- 抖音评论采集项目的前期方案参考。
- 评论数据交付项目的流程模板。
- 数据采集外包的需求澄清清单。
- 作品集项目中的工程复盘案例。

## 仓库结构

```text
.
├── README.md
├── docs/
│   ├── 01-requirement-boundary.md
│   ├── 02-failed-approaches.md
│   ├── 03-strategy-turning-points.md
│   ├── 04-quality-checklist.md
│   ├── 05-delivery-template.md
│   ├── 06-github-discoverability.md
│   └── 07-ethics-and-compliance.md
├── examples/
│   ├── input_models.sample.csv
│   └── comments.sample.json
└── scripts/
    ├── build_delivery_report.py
    └── validate_output.py
```

## 快速体验

校验脱敏样例数据：

```bash
python3 scripts/validate_output.py examples/comments.sample.json
```

生成交付报告草稿：

```bash
python3 scripts/build_delivery_report.py examples/comments.sample.json --output delivery_report.sample.md
```

## 输出 JSON 建议结构

这个项目推荐按“车型 -> 视频 -> 评论”的结构组织。

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
        "title": "Sample Model A real owner review",
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

## 推荐执行流程

### Step 1. 固化需求边界

在动脚本之前先写清楚：

- 采集对象是什么。
- 输入清单来自哪里。
- 输出格式是什么。
- 每条记录必须有哪些字段。
- 时间范围是什么。
- 什么算有效评论。
- 什么算无关评论。
- 低量数据如何解释。
- 客户是否需要脚本，还是只需要结果。

参考：[docs/01-requirement-boundary.md](docs/01-requirement-boundary.md)

### Step 2. 先做一个样例

不要一上来就全量跑。

先选 1 个目标：

- 跑出样例 JSON。
- 让对方确认字段和结构。
- 验证时间范围。
- 验证视频 URL 能回查。
- 验证过滤口径。

样例确认后，再进入全量。

### Step 3. 监控异常信号

下面这些信号出现时，要停下来判断，不要继续堆并发：

- 大量目标都是 0。
- 热门目标也是 0。
- 日志没有报错但结果异常少。
- 同一关键词前后结果差异巨大。
- 页面肉眼可见有内容，但脚本拿不到。
- 新开页面比已登录页面更容易触发验证。

参考：[docs/02-failed-approaches.md](docs/02-failed-approaches.md)

### Step 4. 把转向记录成经验

每次改策略都要记录：

- 为什么原方案不可信。
- 新方案验证了什么。
- 哪个指标变好了。
- 哪些风险仍然存在。

这会让项目从“临时脚本”变成“可复用方法论”。

参考：[docs/03-strategy-turning-points.md](docs/03-strategy-turning-points.md)

### Step 5. 做质量校验和交付说明

交付不是把文件压缩发出去。

交付前要让对方知道：

- 总共采了多少。
- 每个目标多少。
- 哪些低量。
- 为什么低量。
- 有哪些字段可以核对。
- 哪些数据没有猜测或补全。
- 哪些限制需要接受。

参考：

- [docs/04-quality-checklist.md](docs/04-quality-checklist.md)
- [docs/05-delivery-template.md](docs/05-delivery-template.md)
- [docs/06-github-discoverability.md](docs/06-github-discoverability.md)
- [docs/07-ethics-and-compliance.md](docs/07-ethics-and-compliance.md)

## 最小质量标准

一个合格的评论采集交付至少满足：

- 每条视频有可访问来源 URL。
- 每条评论有唯一 ID 或可替代去重键。
- 每条评论有时间。
- 时间范围可验证。
- 目标归档可解释。
- 低量目标有说明。
- 重复、缺字段、越界记录可被脚本检查。
- 原始数据和处理结果分离。
- 交付包里有 README 或交付说明。

## 开源时应该放什么

可以放：

- 脱敏后的样例输入。
- 脱敏后的样例输出。
- 字段定义。
- 校验脚本。
- 交付报告模板。
- 需求澄清清单。
- 失败路线复盘。
- 策略转向记录。

不要放：

- 客户原始 Excel。
- 真实评论数据。
- 账号、cookie、浏览器 profile。
- 验证码截图。
- 任何密钥或 `.env`。
- 可直接滥用的批量攻击配置。
- 客户姓名、聊天记录、私有业务背景。

## 这个项目最想传达的经验

爬虫项目最难的不是写请求。

真正难的是：

- 判断结果为什么不可信。
- 在错误路线里及时刹车。
- 根据真实页面状态换入口。
- 把低量和缺失说清楚。
- 让最终交付能被复查。

如果你只交一个脚本，别人只能看你写了代码。

如果你交一套边界、转折、校验和复盘，别人才能参考你的工程判断。

## 参考过的优秀开源项目和文档

这些项目或文档给了本仓库结构上的参考：

- [GitHub Topics: douyin](https://github.com/topics/douyin)：观察同类项目如何使用 `douyin`、`crawler`、`tiktok` 等主题词。
- [MediaCrawler 入门指南](https://opendeep.wiki/NanmiCoder/MediaCrawler/getting-started)：多平台公开信息采集系统的架构说明，适合作为爬虫项目结构参考。
- [Douyin_TikTok_Download_API README](https://cnb.cool/ChaiKing0/v0020_Douyin_TikTok_Download_API/-/blob/main/README.en.md)：参考中英双语关键词、功能摘要和使用入口组织方式。
- [GitHub Docs: About READMEs](https://docs.github.com/en/repositories/managing-your-repositorys-settings-and-features/customizing-your-repository/about-readmes)：README 会被 GitHub 自动展示给仓库访问者。
- [GitHub Docs: Searching for repositories](https://github.com/github/docs/blob/main/content/search-github/searching-on-github/searching-for-repositories.md)：仓库搜索可按仓库名、描述、Topics、README 等范围检索。
- [GitHub Docs: Classifying your repository with topics](https://docs.github.com/articles/classifying-your-repository-with-topics)：Topics 可以帮助仓库进入相关主题页，提升站内发现概率。
