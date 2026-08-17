# Troubleshooting

Six things that go wrong, what each one actually means, and what to do.

**Run `doctor` before working through any of this.** It probes the installation live and reports what is genuinely connected. This page explains what the findings mean; `doctor` produces them. Guessing from symptoms is how an afternoon disappears.

The single most useful thing to know: **most "it's not working" is not a fault.** Four of the six below are the product working correctly with something missing that it told you about.

---

## "I didn't get an image"

**Almost always Python or Pillow.** Rendering is the one hard dependency — everything else is optional.

Run `doctor` and look at the "Making graphics" line. If it says Pillow is missing, the fix is one command:

```
pip install Pillow
```

**A note if you're on Windows:** `python3` may look like it exists and then fail when run — Windows ships a placeholder at that name. Use `python` instead. `doctor` checks this correctly and will tell you which one works on your machine.

**If graphics are working and you still got no image**, the run should have told you why in a plain sentence. It is written never to describe a picture that doesn't exist. If it went quiet instead, that's worth reporting.

---

## "The writing sounds generic"

**This is the most common complaint and it is almost never a fault.** It means the business profile is thin.

Everything written is grounded in `Business/[your-business]/context/`. If those files are still placeholders — or still say a starter pack wrote them and nobody confirmed it — the writing has nothing specific to hold on to, so it reaches for the generic.

Run `doctor`. Its first section lists every context file as **real**, **starter-pack default**, or **still placeholder**. Fix in this order:

1. **`brand-voice.md`** — the single biggest lever. Without it everything reads like marketing copy in general rather than you in particular.
2. **`audience.md`** — this is what makes a hook land. Posts that talk about the business instead of to the customer usually trace back here.
3. **`products.md`** — lets content name a real offer, and stops it over-claiming.

**The fastest fix:** say "update my brand profile" and answer the questions properly, especially the last one — *what do you believe about your industry that a lot of people in it would disagree with?* That answer does more for the writing than any other single input. Content with a point of view gets shared; content that agrees with everyone gets scrolled past.

---

## "It didn't publish"

Publishing needs Blotato, which is a separate paid account. Without it, nothing is lost except the scheduling step — you get the caption, hashtags, and the image path handed to you ready to paste.

Run `doctor` and check the "Publishing" line. If it says not connected and you expected otherwise, sign in to Blotato and connect your accounts, then run `doctor` again to confirm.

**If it says connected and a post still didn't go**, check that the specific platform account is connected inside Blotato — the connector can be live while a particular account isn't linked.

---

## "The menu is a plain list, not buttons"

**Working as intended.** Clickable cards need a renderer that isn't available on every setup. When it isn't there, you get a numbered list instead.

Every option works identically and the numbers stay in the same order between runs, so they're worth learning. Reply with a number, or just say what you want in plain English.

This is cosmetic. Nothing about what the product can do changes.

---

## "The performance numbers are empty"

Empty means *not measured*, and that is deliberate — you'll never see a zero standing in for a number that couldn't be fetched, because a real zero and a missing reading mean opposite things, and one fake zero skews every average after it.

Reading real reach and engagement needs a Meta connection, which is the hardest thing this product asks for and is best treated as an upgrade rather than part of setup. Without it you still get everything else; you just can't score a post against how your others actually did.

---

## "Is this broken, or am I doing it wrong?"

A fair question, and there's a quick way to tell.

**Probably the installation** — run `doctor`:
- Nothing saves between sessions
- No image at all, on any attempt
- A connector you set up reports as absent

**Probably the profile** — run "update my brand profile":
- Output is bland or could be about any business
- It won't name your actual services or prices
- The tone is wrong

**Probably the brief** — try again with more direction:
- One post came out weak but others were fine
- It picked an angle you didn't want
- It's technically fine but boring

That last case is worth saying out loud: a post that clears the quality bar can still be the wrong post. Say what you actually wanted and ask again. It is faster than editing something you didn't want in the first place.
