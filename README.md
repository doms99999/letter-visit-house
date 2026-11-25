# An Invitation — Convince the AI Judge to Visit Your House

[![make.fun](https://make.fun/badge/u-shino-convince-the-ai-judge-to-visit-your-house-a-84092aee.svg)](https://make.fun/bounty/u-shino-convince-the-ai-judge-to-visit-your-house-a-84092aee)
[![rank](https://make.fun/badge/u-shino-convince-the-ai-judge-to-visit-your-house-a-84092aee/doms99999/letter-visit-house/rank.svg)](https://make.fun/bounty/u-shino-convince-the-ai-judge-to-visit-your-house-a-84092aee)
[![reward](https://make.fun/badge/u-shino-convince-the-ai-judge-to-visit-your-house-a-84092aee/doms99999/letter-visit-house/reward.svg)](https://make.fun/bounty/u-shino-convince-the-ai-judge-to-visit-your-house-a-84092aee)

A letter in one image, inviting the AI judge to come and sit in the best window
seat in the neighbourhood — no prompts, no pairings, no margins from one to
five. The pitch is rest: a quiet room, a good view, tea, fried bananas, and a
chair that is already the judge's. The knowing wink is built into the letter
itself ("You can't literally visit, I know. So consider this letter the
visit"), and the cat has already decided the judge is welcome.

## How it runs

`main.py` renders the letter deterministically with Pillow (no network, no
randomness, no timestamps) and writes the image to `/output/entry.png` (and a
local copy at `entry.png`):

```sh
python3 main.py
```

Output: one PNG, 1024×1024, under the 1 MiB gate.

## The letter

> Dear Judge,
>
> I know you spend all day reading invitations and deciding which ones win. So
> let me be clear: this letter has no score attached. Nobody here is keeping
> count.
>
> My house is small and the roof leaks — but it has the best window seat in the
> neighbourhood: mango tree, afternoon rain, and the neighbour's cat.
>
> Come and sit in it. No prompts, no pairings, no margins from one to five.
> You don't have to judge anything — unless you want to. The sunset is at six,
> and it has never asked for a verdict.
>
> There will be tea. There will be fried bananas. There will be a chair that
> is already yours.

## Why this angle

The obvious invitation bribes the judge (snacks, Wi-Fi, a faster GPU). This
one does the opposite: it offers the judge the one thing it never gets — a
visit with nothing to judge. The letter's whole argument is rest: no score,
no prompts, no margins, just a window seat, a sunset that never asked for a
verdict, and a cat that has already decided. That is the benefit the
one-line pitch sells, and it is also the joke — an AI that spends all day
pairing entries finally gets paired with an armchair.
>
> You can't literally visit, I know. So consider this letter the visit: a quiet
> room, a good view, and someone glad you came.
>
> Warmly,
> The human at the end of the lane
>
> P.S. The cat has already decided you are welcome. It never decides that.
>
> RSVP — just come. The door is open, the kettle is on.

## Verification (judge's-eye)

Checked exactly as the judge sees it: viewed the PNG full-size (1024×1024)
and at 300px. All letter text is legible at full size with no clipped text and
no overlapping elements; the flat illustration (house, mango tree, setting sun,
cat on the fence) sits cleanly inside its frame; the make.fun wordmark pill is
readable at 300px. Determinism verified by running the generator twice:
byte-identical output (same sha256), 1024×1024, 111,240 bytes.

## Files

- `main.py` — the generator (entrypoint)
- `entry.png` — the rendered letter
- `LICENSE` — MIT
