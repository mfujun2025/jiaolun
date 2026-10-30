# -*- coding: utf-8 -*-
"""将 caster-comprehensive-guide.md 转换为置顶长文 HTML 页面"""
import re

MD = 'drafts/caster-comprehensive-guide.md'
OUT = 'news/caster-comprehensive-guide.html'

s = open(MD, encoding='utf-8').read()
lines = s.split('\n')

# 提取元数据（主关键词 / 长尾关键词）
long_kws = []
for i, ln in enumerate(lines):
    if '长尾关键词' in ln:
        long_kws = [k.strip() for k in ln.replace('长尾关键词：', '').split('、')]
        break

# 跳过 markdown 头部（# 标题、blockquote 元数据），从正文第一个小标题开始
body_lines = []
started = False
for ln in lines:
    if ln.startswith('>') or ln.startswith('# '):
        continue
    if ln.startswith('## '):
        started = True
    if started:
        body_lines.append(ln)

title = '脚轮完全指南：种类、材质、应用与选购维护一文讲透 - 脚轮.cn'
description = '脚轮完全指南：种类、材质、应用场景、选购要点与维护保养一文讲透。本文面向采购与工业应用读者，系统讲解脚轮、万向轮、工业脚轮、聚氨酯脚轮、静音脚轮、重型脚轮的专业知识。'
keywords = '脚轮,脚轮种类,脚轮材质,脚轮选购,脚轮维护,工业脚轮,万向轮,聚氨酯脚轮,静音脚轮,重型脚轮'


def md_to_html(blocks):
    out = []
    i = 0
    n = len(blocks)
    while i < n:
        ln = blocks[i].rstrip()
        if not ln.strip():
            i += 1
            continue
        if ln.startswith('### '):
            out.append('<h3>' + inline(ln[4:]) + '</h3>')
            i += 1
        elif ln.startswith('## '):
            out.append('<h2>' + inline(ln[3:]) + '</h2>')
            i += 1
        elif ln.startswith('- '):
            # 收集连续列表项
            items = []
            while i < n and blocks[i].strip().startswith('- '):
                items.append('<li>' + inline(blocks[i].strip()[2:]) + '</li>')
                i += 1
            out.append('<ul>' + ''.join(items) + '</ul>')
        elif ln.startswith('|'):
            # 表格
            tbl = []
            while i < n and blocks[i].strip().startswith('|'):
                tbl.append(blocks[i].strip())
                i += 1
            # 跳过分隔行 |---|---|
            rows = [r for r in tbl if not re.match(r'^\|[\s\-:|]+\|$', r)]
            html = '<table class="article-table">'
            for r_idx, r in enumerate(rows):
                cells = [c.strip() for c in r.strip('|').split('|')]
                tag = 'th' if r_idx == 0 else 'td'
                html += '<tr>' + ''.join('<%s>%s</%s>' % (tag, inline(c), tag) for c in cells) + '</tr>'
            html += '</table>'
            out.append(html)
        elif ln.startswith('**') and '**' in ln[2:]:
            # 粗体开头的段落（小标题式）
            out.append('<p><strong>' + inline(ln) + '</strong></p>')
            i += 1
        else:
            out.append('<p>' + inline(ln) + '</p>')
            i += 1
    return '\n\n'.join(out)


def inline(t):
    t = t.replace('&', '&amp;').replace('<', '&lt;').replace('>', '&gt;')
    t = re.sub(r'\*\*(.+?)\*\*', r'<strong>\1</strong>', t)
    return t


content = md_to_html(body_lines)

CSS = '''
.article-banner { padding: calc(var(--header-h) + 50px) 20px 40px; background: linear-gradient(135deg, var(--primary-dark), var(--primary)); color: #fff; text-align: center; }
.article-banner h1 { font-size: 2rem; font-weight: 800; margin-bottom: 12px; line-height: 1.5; max-width: 900px; margin-left: auto; margin-right: auto; }
.article-banner .meta { display: flex; gap: 20px; justify-content: center; font-size: .85rem; opacity: .9; flex-wrap: wrap; }
.article-banner .meta span { display: inline-flex; align-items: center; gap: 4px; }
.article-banner .pin { display: inline-flex; align-items: center; gap: 6px; background: var(--accent); color: #fff; font-size: .8rem; font-weight: 700; padding: 4px 14px; border-radius: 20px; margin-bottom: 12px; }
.breadcrumb { margin-top: 16px; font-size: .85rem; opacity: .75; }
.breadcrumb a { color: #fff; }
.breadcrumb span { margin: 0 8px; opacity: .5; }
.article-content { max-width: 820px; margin: 0 auto; padding: 40px 20px; }
.article-content h1 { display: none; }
.article-content h2 { font-size: 1.5rem; font-weight: 800; color: var(--text-dark); margin: 44px 0 16px; padding-bottom: 8px; border-bottom: 2px solid var(--primary-light); }
.article-content h3 { font-size: 1.15rem; font-weight: 700; color: var(--text-dark); margin: 26px 0 12px; }
.article-content p { margin-bottom: 16px; font-size: .95rem; line-height: 1.9; color: var(--text-body); }
.article-content ul { margin: 16px 0; padding-left: 20px; }
.article-content li { margin-bottom: 8px; font-size: .95rem; line-height: 1.8; color: var(--text-body); }
.article-content strong { color: var(--text-dark); }
.article-keywords { background: var(--primary-light); border-left: 4px solid var(--primary); padding: 16px 20px; margin: 24px 0; border-radius: 0 8px 8px 0; }
.article-keywords p { margin-bottom: 6px; font-size: .9rem; color: var(--text-body); }
.article-keywords strong { color: var(--primary-dark); }
.article-table { width: 100%; border-collapse: collapse; margin: 20px 0; font-size: .88rem; }
.article-table th { background: var(--primary); color: #fff; padding: 10px 12px; text-align: left; font-weight: 600; }
.article-table td { padding: 10px 12px; border: 1px solid var(--border); }
.article-table tr:nth-child(even) { background: var(--bg-light); }
.article-footer-cta { background: linear-gradient(135deg, var(--primary-dark), var(--primary)); color: #fff; text-align: center; padding: 40px 20px; margin: 40px -20px 0; border-radius: 12px; }
.article-footer-cta h3 { font-size: 1.3rem; font-weight: 800; margin-bottom: 10px; }
.article-footer-cta p { opacity: .9; margin-bottom: 20px; }
@media (max-width: 768px) {
  .article-banner h1 { font-size: 1.4rem; }
  .article-content { padding: 30px 16px; }
  .article-content h2 { font-size: 1.25rem; }
  .article-content p { font-size: .9rem; }
}
'''

kw_block = '<div class="article-keywords">\n<p><strong>主关键词：</strong>脚轮</p>\n<p><strong>长尾关键词：</strong>' + '、'.join(long_kws) + '</p>\n</div>'

HTML = f'''<!DOCTYPE html>
<html lang="zh-CN">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>{title}</title>
  <meta name="description" content="{description}">
  <meta name="keywords" content="{keywords}">
  <link rel="stylesheet" href="../css/style.css">
  <style>{CSS}</style>
</head>
<body>

  <header class="site-header" id="header">
    <div class="header-inner">
      <a href="../index.html" class="logo">
        <span class="logo-icon">轮</span>
        <span class="logo-text">脚轮.cn<small>专业脚轮制造商</small></span>
      </a>
      <button class="nav-toggle" id="navToggle" aria-label="菜单">&#9776;</button>
      <nav class="nav-menu" id="navMenu">
        <a href="../index.html">首页</a>
        <a href="../products.html">产品中心</a>
        <a href="../about.html">关于我们</a>
        <a href="../news.html" class="active">新闻资讯</a>
        <a href="../contact.html">联系方式</a>
        <a href="../contact.html" class="nav-cta">在线咨询</a>
      </nav>
    </div>
  </header>

  <section class="article-banner">
    <div class="pin">&#128204; 置顶推荐</div>
    <h1>脚轮完全指南：种类、材质、应用与选购维护一文讲透</h1>
    <div class="meta">
      <span>&#128197; 2026-10-30</span>
      <span>&#128214; 置顶长文</span>
      <span>&#128269; 脚轮知识库</span>
    </div>
    <div class="breadcrumb"><a href="../index.html">首页</a><span>/</span><a href="../news.html">新闻资讯</a><span>/</span>脚轮完全指南</div>
  </section>

  <div class="article-content">
    {kw_block}
    {content}
    <div class="article-footer-cta">
      <h3>需要专业的脚轮选型建议？</h3>
      <p>我们的工程师团队随时为您提供选型建议、材质推荐与报价方案</p>
      <a href="../contact.html" class="btn btn-primary">立即咨询 &rarr;</a>
    </div>
  </div>

  <footer class="site-footer">
    <div class="container">
      <div class="footer-grid">
        <div class="footer-brand">
          <a href="../index.html" class="logo">
            <span class="logo-icon">轮</span>
            <span class="logo-text" style="color:#fff">脚轮.cn<small>专业脚轮制造商</small></span>
          </a>
          <p>脚轮.cn是专业脚轮生产厂家，拥有20年行业经验，500+款产品型号，服务全国1000+客户，为您提供高品质脚轮产品和定制解决方案。</p>
        </div>
        <div class="footer-col">
          <h4>产品中心</h4>
          <a href="../products.html">工业脚轮</a>
          <a href="../products.html">万向轮</a>
          <a href="../products.html">叉车轮</a>
          <a href="../products.html">耐高温脚轮</a>
          <a href="../products.html">静音脚轮</a>
        </div>
        <div class="footer-col">
          <h4>快速导航</h4>
          <a href="../index.html">首页</a>
          <a href="../products.html">产品中心</a>
          <a href="../about.html">关于我们</a>
          <a href="../news.html">新闻资讯</a>
          <a href="../contact.html">联系方式</a>
        </div>
        <div class="footer-col">
          <h4>联系我们</h4>
          <a href="tel:400-888-9999">&#128222; 400-888-9999</a>
          <a href="mailto:info@jiaolun.cn">&#9993; info@jiaolun.cn</a>
          <a href="../contact.html">&#128205; 广东省东莞市XX工业园</a>
        </div>
      </div>
      <div class="footer-bottom">
        <p>&copy; 2026 脚轮.cn 版权所有 &nbsp;|&nbsp; 粤ICP备2026XXXXXX号</p>
      </div>
    </div>
  </footer>

  <button class="back-top" id="backTop" aria-label="返回顶部">&#8593;</button>
  <script src="../js/main.js"></script>
</body>
</html>
'''

open(OUT, 'w', encoding='utf-8').write(HTML)
print('生成:', OUT)
