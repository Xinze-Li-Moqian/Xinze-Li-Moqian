<img src="https://raw.githubusercontent.com/Xinze-Li-Moqian/Xinze-Li-Moqian/main/assets/moqian-qian-hero.png" width="100%" alt="墨謙 · Moqian, with the six-line 謙 hexagram — Build things. Help communities grow." />

# 墨謙 · Moqian

**English** · [简体中文](https://github.com/Xinze-Li-Moqian/Xinze-Li-Moqian/blob/main/README.zh-CN.md)<br>
[Website ↗](https://lixinze.xyz/) · [LinkedIn ↗](https://www.linkedin.com/in/lixinze/) · [X ↗](https://x.com/xinzelimoqian) · [Lean Zulip ↗](https://leanprover.zulipchat.com/#user/982434)

I'm **Xinze Li (墨謙 · Moqian)**, a PhD student at the **University of Toronto**. My research interests include geometric analysis, minimal surfaces, AI safety, and formal verification. Lean 4 is the language I use most, and I'm exploring how to build verifiable systems.

**Learning while building** is how I work. I need to put theory into practice to understand it. I share what I'm building here from the beginning: **open source since day one**. I share unfinished work and unanswered questions, and try to stay honest with myself about what I do and don't understand.

I also see myself as a **community grower**. I help people from different backgrounds build new communities, and I care about helping students develop work of their own that they can keep learning from and building on.

I enjoy talking with futurists, founders, and investors about emerging science and technology industries, finance, and fintech. These conversations help me understand what people are building and the practical problems they face.

---

<sub>01 / INTERESTS</sub>

## Explore.

- **Mathematics & AI** — tools that help us discover, understand, and work with mathematics.
- **Formal verification** — Lean, checkable proofs, and algorithms we can rely on in practice.
- **Algorithms, optimization & AI safety** — questions grounded in real problems.

---

<sub>02 / COMMUNITIES</sub>

## Help communities grow.

I care about the early work of a community: finding people to work with, sharing what we learn, and giving someone new a place to begin. Here are some of the places I help build.

<table>
<tr>
<td width="50%" valign="top">
<a href="https://github.com/CloK-Lab"><img src="https://avatars.githubusercontent.com/u/259413392?s=64&amp;v=4" width="40" height="40" alt="CloK" /></a>
<h3>CloK</h3>
<p>Making the structure of mathematical knowledge visible and easier to explore.</p>
<p>Start with <a href="https://www.clok.tech/astrolabe">Astrolabe</a>, or explore geometric analysis in <a href="https://github.com/CloK-Lab/OpenGA">OpenGA</a>.</p>
<a href="https://www.clok.tech/">Website ↗</a> · <a href="https://github.com/CloK-Lab">GitHub ↗</a>
</td>
<td width="50%" valign="top">
<a href="https://github.com/Varifold-Lab"><img src="https://avatars.githubusercontent.com/u/331409699?s=64&amp;v=4" width="40" height="40" alt="Varifold" /></a>
<h3>Varifold</h3>
<p>Open learning and research around AI safety and decentralized intelligence.</p>
<p>Explore mean field games in <a href="https://github.com/Varifold-Lab/LeanMFG">LeanMFG</a> and coordination models in <a href="https://github.com/Varifold-Lab/vdsi">ν-DSI</a>.</p>
<a href="https://varifold-lab.github.io/">Website ↗</a> · <a href="https://github.com/Varifold-Lab">GitHub ↗</a>
</td>
</tr>
<tr>
<td width="50%" valign="top">
<a href="https://github.com/indeed-lab"><img src="https://avatars.githubusercontent.com/u/340565723?s=64&amp;v=4" width="40" height="40" alt="Indeed Intelligence" /></a>
<h3>Indeed Intelligence · 确实智能</h3>
<p>Algorithms, optimization, and AI safety, starting from practical problems.</p>
<p>Meet <a href="https://indeed-lab.github.io/#indeed-bot">indeed-bot</a>: a small experiment with a Lean-verified reply selector.</p>
<a href="https://indeed-lab.github.io/">Website ↗</a> · <a href="https://github.com/indeed-lab">GitHub ↗</a>
</td>
<td width="50%" valign="top">
<a href="https://github.com/Slow-Research"><img src="https://avatars.githubusercontent.com/u/344167474?s=64&amp;v=4" width="40" height="40" alt="Slow Research" /></a>
<h3>Slow Research · 慢科研</h3>
<p>Sharing research tools, unfinished ideas, and a sense of humor.</p>
<p>Read the <a href="https://github.com/Slow-Research/.github/blob/main/MANIFESTO.md">manifesto</a> and explore the projects. Make Slow Research Faster!</p>
<a href="https://slow-research.github.io/">Website ↗</a> · <a href="https://github.com/Slow-Research">GitHub ↗</a>
</td>
</tr>
</table>

---

<sub>03 / SELECTED WORK</sub>

## Build & research.

### Finding your way through mathematics

**Astrolabe** turns a Lean project into an explorable 3D dependency graph. Follow a theorem's connections, browse namespaces, and see how a formalization fits together. I worked on the early prototype with [Alejandro Radisic](https://github.com/alerad).

<details>
<summary>View the Astrolabe interface</summary>

<a href="https://github.com/Xinze-Li-Moqian/Astrolabe"><img src="https://raw.githubusercontent.com/Xinze-Li-Moqian/Astrolabe/main/docs/images/screenshot-1.jpg" width="480" alt="Astrolabe prototype: an interactive 3D graph of dependencies in a Lean project" /></a>

</details>

[Early prototype ↗](https://github.com/Xinze-Li-Moqian/Astrolabe) · [Explore on CloK ↗](https://www.clok.tech/astrolabe)

For a broader view, **[awesome-ai4math](https://github.com/Xinze-Li-Moqian/awesome-ai4math)** collects tools, research, learning resources, and communities around AI for mathematics. It's a place to find useful work and people to learn from.

### Working from models to proofs

I'm interested in what happens when a mathematical model becomes something we can inspect, run, and check. These projects explore different parts of that process.

| Project | Question | Work to explore |
| --- | --- | --- |
| [OpenGA](https://github.com/CloK-Lab/OpenGA) | How can we express geometric analysis in Lean? | Foundations for geometric analysis and geometric measure theory. |
| [LeanMFG](https://github.com/Varifold-Lab/LeanMFG) | How can we formalize systems with many interacting agents? | Mean field game models, theory, and algorithms in Lean. |
| [ν-DSI](https://github.com/Varifold-Lab/vdsi) | How can participants coordinate in a decentralized system? | Lean formal models and executable coordination prototypes. |

### Leaving room for an experiment

**[indeed-bot](https://github.com/indeed-lab/indeed-bot)** detects your language, picks a short agreement, and agrees. Its reply selector is verified in Lean; the language detector and interface are separate from that proof.

> **Zero Reasoning. Infinite Agreement.**

[Try a conversation ↗](https://indeed-lab.github.io/#indeed-bot) · [Read the code and proofs ↗](https://github.com/indeed-lab/indeed-bot)

---

<sub>04 / ACTIVITY</sub>

## Work, over time.

<a href="https://github.com/Xinze-Li-Moqian?tab=overview"><img src="https://raw.githubusercontent.com/Xinze-Li-Moqian/Xinze-Li-Moqian/main/assets/contributions.svg" width="100%" alt="A year of GitHub contributions, shown as an isometric calendar; block height represents daily activity" /></a>

<sub>Generated from my public GitHub contribution calendar. [How this is made ↗](https://github.com/Xinze-Li-Moqian/Xinze-Li-Moqian/blob/main/docs/contributions.md)</sub>

---

## Let's grow something.

What are you building, and where could another pair of hands help?

Send me a project, a question, or an idea for a community. I'm especially interested in making a first contribution easier: a clearer explanation, a useful tool, or a problem people can work on together.

[Talk on Lean Zulip ↗](https://leanprover.zulipchat.com/#user/982434) · [LinkedIn ↗](https://www.linkedin.com/in/lixinze/) · [X ↗](https://x.com/xinzelimoqian)
