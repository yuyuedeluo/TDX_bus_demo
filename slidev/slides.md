---
theme: default
title: Git 入門
info: |
  本課程：Git 基礎概念與核心指令（本地工作流）
author: yuyuedeluo
layout: cover
class: text-left
---

<div class="max-w-3xl">
  <div class="text-6xl font-bold leading-tight">
    Git 入門
  </div>

  <div class="text-3xl opacity-80 mt-4">
    版本控制的第一堂課
  </div>

  <div class="mt-8 grid grid-cols-2 gap-4">
    <div class="p-5 rounded-2xl bg-white/5 border border-white/10">
      <div class="text-base opacity-70">Day 1</div>
      <div class="text-xl font-semibold mt-1">Git + GitHub（2 小時）</div>
      <div class="text-sm opacity-70 mt-2">
        clone / commit / push<br>
        branch / PR / review
      </div>
    </div>
    <div class="p-5 rounded-2xl bg-white/5 border border-white/10">
      <div class="text-base opacity-70">Day 2</div>
      <div class="text-xl font-semibold mt-1">專案競賽（6 小時）</div>
      <div class="text-sm opacity-70 mt-2">
        Issue 分工 / PR 合併<br>
        Demo + 成果展示
      </div>
    </div>
  </div>

  <div class="mt-8 text-base opacity-70">
    講師：yuyuedeluo　|　版本：v1.0
  </div>
</div>

<!--
各位同學大家好，今天我們用非常務實的方式，從零開始認識 Git。
你不需要先懂任何指令，只要跟著操作，就會知道怎麼把程式碼保存成可回溯的版本。
今天先把「本地 Git」練扎實，之後再接 GitHub 協作。
-->

---
layout: default
---

# Git 是什麼？

<div class="grid grid-cols-2 gap-10 mt-10">

  <div class="p-6 rounded-2xl bg-white/5 border border-white/10">
    <div class="text-2xl font-semibold mb-4">沒有 Git </div>
    <ul class="space-y-3 text-lg leading-relaxed">
      <li>改壞了不知道哪裡壞</li>
      <li>檔名雜亂：final / final(1) / final(2)</li>
      <li>多人合作互相覆蓋，合併痛苦</li>
    </ul>
  </div>

  <div class="p-6 rounded-2xl  bg-white/5 border border-white/10">
    <div class="text-2xl font-semibold mb-4">有 Git 你會得到</div>
    <ul class="space-y-3 text-lg leading-relaxed">
      <li>改動可追溯、可回溯</li>
      <li>協作流程更穩（分支 / PR）</li>
      <li>每個版本都有紀錄（時間、作者、內容）</li>
    </ul>
  </div>

</div>

<div class="mt-8 text-sm opacity-70">
  <span class="font-medium">一句話：</span>
  Git 是版本控制工具
  <span class="mx-2">|</span>
  詳細說明：<a class="underline" href="https://git-scm.com/book/en/v2/Getting-Started-What-is-Git%3F" target="_blank">What is Git?</a>
</div>

<!--
先想像一下，你正在寫報告或做專案。
如果沒有 Git：你不小心改壞一個檔案，專案壞掉但不知道哪一步壞的。
你為了保留不同版本開始複製檔案，最後桌面出現「最終版」「最終版v2」「真的最終版」。
多人合作時每個人都改一份，合併才發現互相覆蓋，溝通成本爆炸。

有了 Git：每次改動都有記錄可以追，錯了能回到任何一個良好狀態。
也能支援多人協作流程。

提醒：Git 不是雲端服務，它是裝在你電腦本地的版本控制引擎。
GitHub 是把 Git 專案放到網路上的地方，方便遠端協作與分享。
-->

---
layout: default
---

# Git 的架構

<div class="grid grid-cols-2 gap-10 items-center mt-6">

  <!-- Left: Image -->
  <div>
    <img
      src="/images/git-flow.png"
      class="w-full max-w-xl mx-auto rounded-lg shadow-md"
      style="object-fit: contain;"
    />
    <p class="text-sm opacity-60 text-center mt-2">
      Working Directory → Staging Area → Repository
    </p>
  </div>

  <!-- Right: Cards -->
  <div class="space-y-5">
    <div class="p-5 rounded-2xl bg-white/5 border border-white/10">
      <div class="text-lg font-semibold">工作區（Working Directory）</div>
      <div class="text-base opacity-80 mt-1">
        你正在編輯的檔案，改動還沒被記錄
      </div>
      <div class="text-sm opacity-60 mt-2">
        常見動作：編輯 / 儲存 / git status
      </div>
    </div>
    <div class="p-5 rounded-2xl bg-white/5 border border-white/10">
      <div class="text-lg font-semibold">暫存區（Staging Area）</div>
      <div class="text-base opacity-80 mt-1">
        本次提交要包含哪些改動
      </div>
      <div class="text-sm opacity-60 mt-2">
        常見動作：git add（把改動放進來）
      </div>
    </div>
    <div class="p-5 rounded-2xl bg-white/5 border border-white/10">
      <div class="text-lg font-semibold">版本庫（Repository / .git）</div>
      <div class="text-base opacity-80 mt-1">
        提交後的歷史版本紀錄
      </div>
      <div class="text-sm opacity-60 mt-2">
        常見動作：git commit / git log
      </div>
    </div>

  </div>
</div>

<!--
這頁是 Git 的核心世界觀：工作區、暫存區、版本庫。
工作區就是你電腦裡真正存在、你正在改的檔案。
暫存區像待發布清單，你可以只挑一部分改動放進去，這就是 git add。
版本庫是 commit 後形成的歷史版本集合，之後想回到任何一個版本都做得到。

一句話記住：add 是挑選上台的人，commit 是拍照存檔。
-->

---
layout: default
---

# 準備工作

<div class="grid grid-cols-3 gap-6 mt-10">

  <!-- Card 1 -->
  <div class="p-6 rounded-2xl bg-white/5 border border-white/10">
    <div class="text-xl font-semibold mb-4">安裝 Git</div>
    <div class="text-sm opacity-70 mb-2">Windows</div>
    <div class="text-base">
      Git for Windows
    </div>
    <div class="mt-4 text-sm opacity-70 mb-2">macOS</div>
    <div class="text-base">
      <code>git --version</code><br />
      <span class="text-sm opacity-70">沒有就安裝 Command Line Tools</span>
    </div>
    <div class="mt-4 text-sm opacity-70 mb-2">Linux</div>
    <div class="text-base">
      <code>sudo apt install git</code>
    </div>
  </div>

  <!-- Card 2 -->
  <div class="p-6 rounded-2xl bg-white/5 border border-white/10">
    <div class="text-xl font-semibold mb-4">編輯器</div>
    <div class="text-base">
      VS Code（建議）
    </div>
    <div class="mt-4 text-sm opacity-70">
      方便看差異、操作 Git、整合終端機
    </div>
  </div>

  <!-- Card 3 -->
  <div class="p-6 rounded-2xl bg-white/5 border border-white/10">
    <div class="text-xl font-semibold mb-4">專案資料夾建議</div>
    <ul class="space-y-3 text-base">
      <li>一個專案，一個資料夾</li>
      <li>路徑盡量簡短</li>
      <li>避免特殊符號與長路徑</li>
    </ul>
    <div class="mt-4 text-sm opacity-70">
      範例：<code>D:\Projects\my-app</code>
    </div>
  </div>

</div>

<div class="mt-8 text-sm opacity-70">
  檢查：<code>git --version</code> 有出現版本號就代表已經安裝了
</div>

<!--
進入實作前先準備工具。
安裝 Git：各系統方式不同，裝好後用 git --version 確認有版本號。
建議用 VS Code，對 Git 很友善。
專案資料夾建議獨立管理，路徑簡潔避免麻煩。
工具到位我們就開始操作。
-->

---
layout: default
---

# Git常用指令

<div class="mt-10 grid grid-cols-2 gap-6">

  <div class="p-6 rounded-2xl bg-white/5 border border-white/10">
    <div class="text-xl font-semibold mb-3">建立與檢查</div>
    <ul class="space-y-3 text-lg">
      <li><code>git init</code>：初始化倉庫</li>
      <li><code>git status</code>：現況報告</li>
      <li><code>git log --oneline</code>：看歷史版本</li>
    </ul>
  </div>

  <div class="p-6 rounded-2xl bg-white/5 border border-white/10">
    <div class="text-xl font-semibold mb-3">提交流程</div>
    <ul class="space-y-3 text-lg">
      <li><code>git add</code>：放入暫存區</li>
      <li><code>git commit</code>：提交成版本</li>
    </ul>
  </div>
  <div class="mt-6 text-sm opacity-70">記憶順序：<code>init → status → add → commit → log</code>
    </div>

</div>

<!--
Git 指令很多，但初學者先掌握最核心四個就能開始管理版本。
git status 是你的現況報告，慌了先打它。
git add 決定這次提交要包含哪些內容。
git commit 把暫存區寫入版本庫，形成里程碑。
git log --oneline 用一行一筆快速瀏覽歷史。
-->

---
layout: default
---

# Demo：初始化新專案

<div class="grid grid-cols-2 gap-8 mt-10">

  <div class="p-6 rounded-2xl bg-white/5 border border-white/10">
    <div class="text-xl font-semibold mb-3">建立資料夾 + 初始化</div>

```bash
mkdir my-first-git
cd my-first-git
git init
````

<div class="text-sm opacity-70 mt-3">
  <code>git init</code> 會建立 <code>.git</code>版本庫
</div>

  </div>

  <div class="p-6 rounded-2xl bg-white/5 border border-white/10">
    <div class="text-xl font-semibold mb-3">建立 README 後第一次提交</div>

```bash
git status
git add README.md
git commit -m "init: add README"
git log
```

<div class="text-sm opacity-70 mt-3">
  <code>init → status → add → commit → log</code>
</div>

  </div>

</div>
   
<br>

#####  做完你應該會看到：   
##### <code>git log</code> 至少一筆 commit

---
layout: default
---

# 改動復原

<div class="grid grid-cols-2 gap-2 mt-2">

  <div class="p-6 rounded-2xl bg-white/5 border border-white/10">
    <div class="text-xl font-semibold mb-2">情境 A：還沒 add</div>
    <div class="text-sm opacity-70 mb-4">
      取消工作區改動，回到上一個狀態
    </div>

```bash
git restore <file>
````

<div class="mt-3 text-sm opacity-70">
  例：<code>git restore README.md</code>
</div>

  </div>

  <div class="p-6 rounded-2xl bg-white/5 border border-white/10">
    <div class="text-xl font-semibold mb-2">情境 B：已 add 但還沒 commit</div>
    <div class="text-sm opacity-70 mb-4">
      把檔案從暫存區移除（保留工作區修改）
    </div>

```bash
git restore --staged <file>
```

  <div class="mt-3 text-sm opacity-70">
    例：<code>git restore --staged README.md</code>
  </div>

  </div>

</div>


<div class="mt-2 p-6 rounded-2xl bg-white/5 border border-white/10">
  <div class="text-xl font-semibold mb-2">情境 C：已 commit，想回復到之前版本</div>
  <div class="text-sm opacity-70 mb-4">
    用 <code>git revert</code> 產生一個「反向 commit」，保留歷史紀錄，最適合團隊協作
  </div>


```bash
git log --oneline
git revert <commit>
# 只想撤銷上一筆：git revert HEAD
````

<div class="mt-3 text-sm opacity-70 leading-tight">
  <div>例：<code>git revert a1b2c3d</code>（會開編輯器讓你確認 commit 訊息，存檔後完成）</div>
  <div class="mt-1">※ 只想「暫時看看舊版本」：<code>git switch --detach &lt;commit&gt;</code>，看完用 <code>git switch -</code> 回來</div>
</div>

</div>

<!--
誰都會手滑。這頁只教不恐怖、最安全的撤回方式。
情境一：還沒 add，就用 git restore <file> 回到上一個狀態。
情境二：已 add 但還沒 commit，用 git restore --staged <file> 把檔案從暫存區移除，但保留工作區修改。
commit 後才發現錯會更複雜，之後講分支與協作流程再深入。
-->

---
layout: default
---

# Commit 訊息怎麼寫？

<div class="grid grid-cols-2 gap-10 mt-10">

  <!-- Left: rules -->
  <div class="p-6 rounded-2xl bg-white/5 border border-white/10">
    <div class="text-xl font-semibold mb-4">三個原則</div>
    <ul class="space-y-3 text-lg leading-relaxed">
      <li>小步提交：一次 commit 只做一件事</li>
      <li>動詞開頭、簡潔明瞭</li>
      <li>讓人一眼看懂改動</li>
    </ul>
    <div class="mt-6 text-sm opacity-70">
      推薦格式：<code>&lt;type&gt;: &lt;what&gt;</code>
    </div>
  </div>

<!-- Right: prefixes -->
<div class="p-6 rounded-2xl bg-white/5 border border-white/10">
  <div class="text-xl font-semibold mb-4">常見前綴（推薦）</div>
  
  <div class="grid grid-cols-2 gap-3 text-lg">
    <div class="flex items-center gap-2">
      <code class="px-2 py-1 rounded bg-white/5">feat:</code><span class="opacity-85">新功能</span>
    </div>
    <div class="flex items-center gap-2">
      <code class="px-2 py-1 rounded bg-white/5">fix:</code><span class="opacity-85">修 bug</span>
    </div>

  <div class="flex items-center gap-2">
    <code class="px-2 py-1 rounded bg-white/5">docs:</code><span class="opacity-85">文件</span>
  </div>
  <div class="flex items-center gap-2">
    <code class="px-2 py-1 rounded bg-white/5">chore:</code><span class="opacity-85">雜項/工具</span>
  </div>

  <div class="flex items-center gap-2">
    <code class="px-2 py-1 rounded bg-white/5">refactor:</code><span class="opacity-85">重構</span>
  </div>
  <div class="flex items-center gap-2">
    <code class="px-2 py-1 rounded bg-white/5">test:</code><span class="opacity-85">測試</span>
  </div>
</div>

  <div class="mt-6 text-sm opacity-70">
    commit沒有強制的規定，但重點是要清楚描述改動內容
  </div>
</div>

</div>

<div class="mt-8 p-5 rounded-2xl bg-white/5 border border-white/10">
  <div class="text-lg font-semibold mb-3">範例</div>

```bash
git commit -m "docs: update README.md"
```

</div>

<style>
pre { margin-top: 0.4rem !important; margin-bottom: 0.4rem !important; }
</style>

---
layout: two-cols-header
---

# 練習：完成兩次 Commit

### 任務 A

<div class="text-sm opacity-80">
目標：做出 <b>2 個 commit</b>，最後用 <code>git log --oneline</code> 看到兩筆紀錄
</div>

::left::
<div class="pr-10">    

1.確認你在專案資料夾

- 你應該能看到專案檔案，或看到 <code>.git</code> 資料夾  
- 如果不確定，先用下面指令確認目前路徑

```bash
# Windows (PowerShell)
pwd
# macOS / Linux
pwd
# 或用 dir 看目前資料夾內容
dir
````
</div>

::right::

<div class="pr-10">

2.建立 notes.txt

用 VS Code 新增檔案，打三行文字並儲存

```md
- git init 用於初始化倉庫
- git status 查看狀態
- git add 將檔案加入暫存區
```


<style>
pre { margin: .35rem 0 !important; }
</style>

</div>

---
layout: two-cols-header
---

::left::
<div class="pr-10">  

3.檢查狀態
```bash
git status
````

你會看到類似：
```powershell
On branch master

No commits yet

Untracked files:
  (use "git add <file>..." to include...
        note.txt
#看到 notes.txt 未追蹤
nothing added to commit but untracked files...
```

4.加入暫存區（stage）
```bash
git add notes.txt
```
</div>

::right::

<div class="pr-10">  

5.再檢查一次（應該看到 notes.txt 在 staged）
```bash
git status
```

你會看到類似：

```powershell
On branch master

No commits yet

Changes to be committed:
  (use "git rm --cached <file>..." to unstage)
        new file:   note.txt
```

6.提交（第一次 commit）
```bash
git commit -m "docs: add notes.txt"
```
你會看到類似：
```powershell
[master (root-commit) 1338eb8] docs: add notes.txt
 1 file changed, 3 insertions(+)
 create mode 100644 note.txt
```
</div>

<style>
pre { margin: .35rem 0 !important; }
</style>

---
layout: two-cols-header
---

### 任務 B：修改檔案並提交

<div class="text-sm opacity-80">
目標：在 <code>notes.txt</code> 再加 2 行 → 用 <code>git diff</code> 看差異 → add → commit
</div>

::left::
<div class="pr-10">

1.修改 `notes.txt` 

```md
- git commit 寫入歷史版本
- git log 則查看歷史紀錄
````

2.看看差異（改了哪些內容）

```bash
git diff
```
你會看到類似：
```powershell
diff --git a/note.txt b/note.txt
index be2aa87..bbf9a92 100644
--- a/note.txt
+++ b/note.txt
@@ -1,3 +1,5 @@
 - git init 用於初始化倉庫
 - git status 查看狀態
 - git add 將檔案加入暫存區
+- git commit 寫入歷史版本
+- git log 則查看歷史紀錄
\ No newline at end of file
```

</div>

::right::

<div class="pl-10">

3.加入暫存區（stage）

```bash
git add notes.txt
```

4.提交／第二次 commit

```bash
git commit -m "docs: update notes.txt"
```

你會看到類似：
```powershell
[master f1bcd00] docs: update notes.txt
 1 file changed, 2 insertions(+)
```

</div>

---
layout: two-cols-header
---

# 最後檢查：有沒有兩個 commit

::left::
<div class="pr-12">

1.列出歷史
```bash
git log --oneline
````

你應該看到兩筆 commit，像這樣：

```text
xxxxxxx (HEAD -> master) docs: update notes.txt
yyyyyyy docs: add notes.txt
```

</div>

::right::

<div class="pl-12">

常見錯誤

* `nothing to commit`：沒有改動 / 忘記存檔
* `changes not staged for commit`：有改檔，但忘了 `git add`
* `untracked files`：新檔案還沒 `git add`

補救流程

```bash
git status
```

</div>

---
layout: default
---

# 小結

<div class="text-lg opacity-85 mt-2">
你已經把 Git 的基本功學完了：能新增檔案、看狀態、提交紀錄，還知道怎麼安全撤回。
</div>

<div class="mt-10 grid grid-cols-3 gap-6">
  <div class="p-6 rounded-2xl bg-white/5 border border-white/10">
    <div class="text-xl font-semibold mb-2">你會了什麼</div>
    <ul class="text-base opacity-85 space-y-2 leading-relaxed">
      <li><code>git status</code> 看狀態</li>
      <li><code>git add</code> 暫存（stage）</li>
      <li><code>git commit</code> 提交</li>
    </ul>
  </div>

  <div class="p-6 rounded-2xl bg-white/5 border border-white/10">
    <div class="text-xl font-semibold mb-2">你練了什麼</div>
    <ul class="text-base opacity-85 space-y-2 leading-relaxed">
      <li>做了 2 次 commit</li>
      <li><code>git diff</code> 看差異</li>
      <li><code>git log --oneline</code>查詢紀錄</li>
    </ul>
  </div>

  <div class="p-6 rounded-2xl bg-white/5 border border-white/10">
    <div class="text-xl font-semibold mb-2">你能回溯版本</div>
    <ul class="text-base opacity-85 space-y-2 leading-relaxed">
      <li>還沒 add：<code>git restore</code></li>
      <li>已 add：<code>git restore --staged</code></li>
      <li>已 commit：<code>git revert</code></li>
    </ul>
  </div>
</div>

<div class="mt-10 text-lg">
下一步：GitHub 協作（<span class="opacity-90">branch / PR / review / merge</span>）
</div>

<!--
今天把本地 Git 的基本功練扎實了。
下一步我們會把同一套流程搬到 GitHub：分支、Pull Request、Review、合併、衝突處理與分工。
-->
