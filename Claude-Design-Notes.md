Yes, it does variations natively — here's the process:

**How it works**
1. Open a project at claude.ai/design — split screen with chat on the left, canvas on the right.
2. Feed it context before you prompt: upload screenshots, competitor references, or an existing deck, or link a code repo so it can read your components and styling. If your team has a design system set up, it's applied automatically.
3. Use chat (not inline comments) for requesting multiple variations — inline comments are for surgical, single-element tweaks.

**Asking for multiple at once**
Yes — it's built for exactly this. A prompt like "Three more variants, one minimal" takes about 30 seconds rather than the 30 minutes it'd take duplicating frames manually. The general guidance is: if you're unsure about a direction, ask Claude to show you 2–3 options, since comparing alternatives is faster than guessing.

**A prompt you could use for 3 variations:**
> "Show me 3 alternative layouts for [the screen]. Vary the [structure/hierarchy/tone] — e.g., one more minimal, one more content-dense, one image-led. Keep the same brand colors and components."

**For getting to 10 total**, the realistic path is iterative rather than one giant ask: Claude handles incremental requests much better than one monster brief — though it is capable of generating something like ten dashboard variations in ten minutes when pushed. A practical approach: ask for 3 at a time, pick the promising direction(s), then say "give me 3 more variants building on option 2, but try [different angle]" and repeat. That also gives you a paper trail of what you've tried rather than 10 things dumped at once.

One tip worth knowing: if you want to branch into a totally different direction without losing your current one, tell Claude "save what we have and try a completely different approach" — it'll save the current project and confirm where, which is the closest thing to version control the tool has right now.