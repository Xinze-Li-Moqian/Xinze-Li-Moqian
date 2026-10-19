# Contribution landscape

The profile's SVG shows **365 consecutive calendar dates**, ending today in `America/Toronto`. Dates and counts come from GitHub's unauthenticated public contribution calendar for `Xinze-Li-Moqian`; no personal access token or new secret is required.

Each tile is one day, arranged in Sunday-first weeks. Equal-scale isometric axes give the columns their depth. For nonzero days, height is `8 + 72 × √(count / peak)` in drawing units, keeping low activity visible; zero-count days stay flat. Ice blue and gold distinguish lower and higher activity. The displayed total is the exact sum of the included days, rather than a count inferred from GitHub's color levels.

## Update locally

Python 3.11 or later with the system IANA timezone database is sufficient. No packages are required.

```sh
python3 -m unittest discover -s tests -p test_contributions.py
python3 scripts/render_contributions.py
```

To reproduce a date window, pass `--end 2026-10-19`. `--timezone` accepts an IANA name and chooses the current date with daylight-saving transitions handled by Python's `zoneinfo`; it does not reinterpret GitHub's daily date labels. `--output` selects another SVG destination.

## Data and validation

The source is `https://github.com/users/Xinze-Li-Moqian/contributions?from=YYYY-01-01&to=YYYY-12-31`. GitHub currently returns whole calendar years even when a query crosses years. The script fetches each required year separately, pairs each dated calendar cell with its accessible tooltip, checks every date and the calendar's annual total, then selects the rolling window and sums its counts.

Missing dates, duplicate dates or IDs, unexpected tooltip text, inconsistent counts, network failures, and invalid XML all prevent publication. The new SVG replaces the previous image atomically only after successful validation. An unchanged render is not rewritten. The script makes no authenticated requests and stores no HTML or repository-level activity.

These are **GitHub contributions**, not exclusively commits or contributions to public repositories. GitHub may include anonymized private activity according to the user's visibility settings. Today's count is partial, and GitHub's updates can lag. The public HTML endpoint is not a versioned API; a markup change may require a parser update. On failure, the existing image and its date range remain visible.

## Automation

The workflow runs daily at **10:23 UTC**, or through **Actions → Update contribution landscape → Run workflow**. It tests the parser, fetches the public calendar, and commits only `assets/contributions.svg` when changed. Pushes do not trigger this workflow, so its own commits do not cause a loop.

The job uses the repository's existing `GITHUB_TOKEN` with only `contents: write` to check out and push to the default branch. It never force-pushes; branch protection or a concurrent conflicting edit can cause a safe failure. No PAT or manually created secret is needed. `actions/checkout` is pinned to the official [v7.0.1 release](https://github.com/actions/checkout/releases/tag/v7.0.1) commit.

## 中文说明

这张图使用 GitHub 公开贡献日历的真实每日计数，展示截至多伦多当天的连续 365 天。每格代表一天，柱高按贡献数的平方根缩放，顶部合计为区间内每日计数之和。计数可能包含用户选择公开的匿名私有贡献，因此统一标注为 GitHub contributions；当天数据尚未完整。

脚本分别读取所需年份，核验日期、提示文本及年度合计后生成矢量图。无需额外密钥，抓取或校验失败时保留旧图。Actions 每天更新，也可手动运行；只在图片内容变化时提交该图片，不会由自己的提交触发循环。
