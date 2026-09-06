# Analysis Plan 001 — Turkish ASR Post-Editing:
## System A (Haiku 4.5) vs System B (Sonnet 5), default configurations

**Status:** DRAFT — not frozen. Blanks marked `[DECIDE]` must be filled before
any study data is collected. The freeze tag in section 11 is not created until
every blank is closed; a pre-registration with open blanks pre-registers
nothing.

**Pre-registration principle:** every choice in sections 4-10 is made without
looking at outcome data. A choice made after seeing results is not an analysis,
it is a selection.

---

## 1. Question

Two deployable systems, built on models from the same family with a known but
modest expected quality gap, convert raw Turkish ASR output into readable text. The small gap is the point,
not an inconvenience: it is the regime where evaluation practice usually fails.

- **S1 (comparison):** Is the gap between Sonnet 5 and Haiku 4.5 detectable at a
  realistic evaluation size?
- **S2 (judge validation):** How closely does an out-of-family LLM judge track
  human judgment, and how closely do two humans track each other — separately
  for relative preference and for absolute rating?

S2 is not subordinate. If human-human agreement is low, S1 is uninterpretable
regardless of its p-value.

## 2. Systems under comparison

**Estimand — what is being compared.** Two deployable systems, not two model
architectures. Sonnet 5 rejects `temperature`, `top_p` and `top_k`, and its
adaptive thinking cannot be turned off; Haiku 4.5 accepts sampling parameters
and does not think unless given a thinking budget. The two configurations
therefore cannot be equalised with this model pair, and a design that insisted
on equalising them would have to swap in a pair nobody deploys. What is measured
here is the quality difference a person deploying these two systems today, at
their default settings, would see. The configuration difference — adaptive
thinking on B, none on A — is part of the object being measured, and is declared
rather than hidden.

The comparison unit is a system, so no conclusion of the form "B is better
because it is the larger model" is available from this design.

| Role | System | Settings |
|---|---|---|
| System A | Haiku 4.5, default configuration | no sampling parameter sent; no thinking budget |
| System B | Sonnet 5, default configuration | no sampling parameter sent; adaptive thinking, not disableable |
| Judge | `[DECIDE: out-of-family model]` | `[DECIDE: settings]`, recorded in the manifest |

**Model identity is not written from memory.** Exact model ids are read from the
Models API at run time and copied verbatim into the run manifest, alongside the
settings actually sent. Six months from now the manifest is the only record of
which version produced the data.

Both systems receive the identical prompt and the identical input list in the
identical order, one generation per item. The prompt is committed alongside this
plan and does not change during the study.

**Run-to-run variance check — mandatory, and two-armed.** Neither system is
deterministic, because neither is given a sampling parameter. Re-run **both**
systems on `[DECIDE: n]` items and report each system's disagreement with itself
separately. Adaptive thinking may make B's run-to-run variance visibly larger
than A's, and in a paired design that asymmetry matters: one side of the pair is
noisier than the other. If a system's disagreement with itself approaches the
A-vs-B difference, that is the study's answer, and a strong one.

## 3. Materials

**Source strategy (decided):** Common Voice Turkish is used for pipeline
warm-up and blinding-harness testing only, and contributes no item to the study.
Read-aloud short sentences lack disfluency, repetition and natural sentence
boundaries, so they exercise only half of the post-editing task. The study
corpus is natural, unscripted speech.

**Study corpus (decided): own recordings.** 40 speakers, each recorded for at
least 7 minutes of unprepared Turkish speech, contributing 3 items. Holding the
rights removes the licence question entirely, and it removes half of the
exclusion rules with it: there is no music bed, no jingle, no applause and no
second speaker to screen for, because the recording is made without them.
Speaker metadata is defined rather than inferred, which hands section 8 a
subgroup variable that found material cannot supply, and Project B needs clean
source material for its acoustic conditions regardless — the recordings are made
once and serve both projects.

**TEDx was eliminated on licence grounds, not editorial ones.** TED publishes
TED and TEDx talks under CC BY-NC-ND 4.0, and the binding restriction is ND, not
NC. The usage policy states that "no derivative works are permitted so you cannot
edit, remix, create, modify or alter the form of the TED Talks in any way", that
one "may not edit TED Talks, or alter them in any way, including by sharing
truncated versions or clips", and that "copyright on the transcripts is owned by
TED". This study's central operation on a recording is to cut clips from it,
derive a transcript, have two systems rewrite that transcript, and publish the
material so the result can be reproduced — which is that prohibited set, item by
item. The conflict is sharpest exactly where the study's value lies. A CC BY
marking on a TEDx upload on a video platform is not a safe basis either: the
local organiser may not hold the right to relicense.

TBMM transcripts were rejected earlier despite being the best content fit —
natural, unprepared, speaker-diverse, and already carrying a reference
transcript. Parliamentary material is dense in proper nouns and institution
names, and the two systems may behave differently on political content. That is
a variable this study does not want to measure and cannot control, and it would
sit inside the primary comparison rather than beside it.

**Podcast material under written permission is a secondary arm, not a
prerequisite.** Recordings may be added if a rights holder grants permission
covering all four of: segmentation, derivation of transcripts, publication of
those derived transcripts, and reproduction by third parties. Permission that
covers use but not redistribution is of no use to a study whose point is
reproducibility. Where such material is added, the source is recorded per item in
the manifest as a subgroup variable — a difference between own recordings and
podcast material would otherwise sit unlabelled inside the primary comparison.

**Consent is recorded in two tiers, per speaker, in the manifest:**

1. transcripts and derived text may be published;
2. the audio may be published as well.

A speaker who declines the second tier still supplies items under the first. A
single-tier form would cost speakers, and speakers are the scarcest resource in
this design — section 9 shows the effective sample size bounded by their number
rather than by the item count.

- **Speakers and items (decided):** 40 speakers × 3 items = 120 study items. The
  rubric-derivation set takes 10 further speakers and the pilot 7-10 more,
  disjoint from the study and from each other, so the collection target is **at
  least 57 speakers** at 7+ minutes each. The speaker count, not the item count,
  is both the collection cost and the statistical ceiling.
- **ASR system producing the raw output (decided):** Whisper `large-v3-turbo`,
  identical for every item, with the exact checkpoint recorded in the run
  manifest. Which ASR is used is not this study's question — the comparison is
  between post-editors, not recognisers — but it must be fixed. If it varies,
  post-editing difficulty varies with it and enters the analysis as noise inside
  the primary comparison. The turbo checkpoint is chosen over `large-v3` for
  headroom: output clean enough to need no post-editing would floor both systems
  and leave nothing for the comparison to separate. Whether the headroom is in
  fact adequate is a listening judgement made on the rubric-derivation set,
  before the study runs.

**Item budget — at least 170 items from at least 57 speakers:**

| Set | Size | Used for | Enters analysis |
|---|---|---|---|
| Rubric derivation | 30 | deriving the anchors in 4.2 | no — burned |
| Pilot | `[DECIDE: 20-30]` | variance and tie-rate estimates for section 9 | no — burned |
| Study | 120 | S1 and S2 | yes |

The rubric-derivation set cannot double as the pilot: those items shaped the
rubric, so ratings on them are optimistically consistent with it.

**Collection order.** The first 10 speakers are recorded and run end to end —
segmentation, ASR, both systems, blinded sheet — before the remaining 47 are
recorded. A pipeline fault then costs 10 speakers to discover instead of 57.
Those 10 speakers yield exactly the 30 items the rubric-derivation set needs, and that set is burned in any case, so the shakedown consumes nothing the
study could otherwise have used.

**Segment construction (decided).** Every item is a 30-second window of one
recording.

- **Length: 30 seconds**, roughly 60-75 words of natural Turkish. Shorter windows
  were rejected. At 15-20 seconds the material stops exercising suffix agreement
  across clauses, sentence-boundary restoration and reference resolution — most
  of the Turkish-specific categories in 4.2. Shrinking the window to fit the
  rating budget would not have measured the task cheaply; it would have measured
  a smaller task.
- **Offsets: seeded random, restricted to speech regions found by voice activity
  detection.** The seed goes in the run manifest, so segmentation is
  reproducible. Minimum proportion of speech inside a candidate window:
  `[DECIDE: threshold]`, pre-registered — a threshold chosen after seeing which
  windows it rejects is a selection rule, not a filter.
- **Separation: one segment per third of the recording, at least 90 seconds
  apart.** This is where the 7-minute minimum comes from: three 30-second windows
  with 90-second gaps do not fit below about 5 minutes, and 7 leaves room for
  candidate windows that the speech-ratio threshold rejects. The separation is
  not cosmetic. Adjacent segments share topic, acoustic state and speaker energy,
  which raises the within-recording correlation ρ, and ρ is what the design
  effect in section 9 turns on.
- **Edges: cut at the clock offset, then drop the leading and trailing partial
  word from the ASR output** before it reaches either system, uniformly for every
  item. Snapping the cut to the nearest pause instead would hand the post-editor a
  sentence boundary and pre-solve part of what 4.2 is trying to measure; cutting
  at the clock and leaving the edge would put a truncated word in every item as a
  systematic artefact. This is the middle path: the boundary work stays, the
  artefact does not.

**Clustering.** If more than one item comes from the same recording or speaker,
the unit of analysis is the recording, not the item. Number of items per
recording: 3. Clustering is not avoided, it is carried into section 7 as
cluster-robust resampling — ignoring it inflates significance.

**Cluster unit:** the recording. In a single-speaker talk the recording and the
speaker coincide. In a multi-speaker episode the speaker is nested inside the
episode, so every item is drawn from a single speaker and the cluster is the
episode — the larger unit, which is the conservative choice.

At 3 items per recording the design effect is `1 + 2ρ`, so the effective sample
size is `120 / (1 + 2ρ)`: 100 items at ρ = 0.1, 86 at ρ = 0.2. ρ is not known
before the pilot, which is why the pilot must itself be clustered (section 9).

**Selection:** items are drawn by `[DECIDE: sampling rule]` before any model is
run. No item is dropped after its outputs are seen.

## 4. Rating protocol

### 4.1 Two-tier measurement

The absolute scale is not applied to all 240 outputs. Rating capacity is a
binding constraint on this study and spending it entirely on a noisy measure is
one of the likelier ways for it to die unfinished.

| Tier | Instrument | Coverage | Est. owner time |
|---|---|---|---|
| **Primary** | paired preference: A better / equal / B better | all 120 items | ~2-3 h |
| **Secondary** | absolute 1-5 rating, rubric-anchored | `[DECIDE: subset size]` items, both systems | ~1 h per 40 ratings |

Time estimates assume a 30-second item, roughly 60-75 words per text: a
preference judgement reads the raw ASR plus both outputs, an absolute rating
reads the raw ASR plus one output.

Rationale for making preference primary: on a 5-point absolute scale the
decision between 3 and 4 is unstable and contributes noise, while "which of
these two is better" is a far more stable judgment. In a study that expects a
small true difference, the more stable instrument is the primary one.

Rationale for keeping the absolute tier: Project B must eventually answer "is
this good enough" against a fixed threshold, which is an absolute question that
preference data cannot answer. The subset preserves that capability.

**Graded preference:** `[DECIDE]` — whether preference is recorded on 3 levels
(A / equal / B) or 5 (A much better / A slightly better / equal / B slightly
better / B much better). This choice changes which test is available; see
section 7.1.

**Subset size is now an open decision, and it was not before.** At 300 study
items a 100-item absolute subset covered a third of the study, and the two tiers
were plainly separate instruments. At 120 items that same 100 would cover 83% of
the study, the tiers would nearly coincide, and the two-tier design would stop
being a way of spending capacity and become duplication. Section 6's secondary
outcome and section 7.3's absolute agreement estimate both rest on this number.

**Subset selection:** the absolute-rated items are drawn at random before rating
begins, not chosen while rating.

### 4.2 Rubric derivation — do not invent the anchors

Anchors written from imagination do not match the real error distribution; items
then pile up on 3 and 4 and discrimination is lost. Procedure, in order:

1. Read the 30 rubric-derivation outputs blind. **Do not score them** — record
   the errors observed.
2. Sort those 30 into three rough piles, worst to best.
3. Name the piles. The anchors come from the piles, not from the imagination.
4. Discard the 30 from the study.

Candidate error categories for Turkish ASR post-editing (from the study owner's
domain knowledge; severity assignment is a study-owner decision, not a default):

- Suffix errors — wrong case, possessive, plural. Changes meaning.
- `de`/`da` and `ki` written joined vs separate.
- Question particle `mi/mı/mu/mü` separation and vowel harmony.
- Proper-noun recognition and capitalization.
- Number, date, time and currency normalization.
- Abbreviation expansion (TL, TBMM, and similar).
- Sentence boundaries and punctuation.
- Filler and repetition removal.
- **Hallucination — content not present in the ASR input.**

**The critical rubric decision** `[DECIDE]`: whether hallucination is a separate
category with its own ceiling rather than one error among many. Fluent but
fabricated text is worse than clumsy but faithful text, and that distinction is
precisely what WER cannot express. If the rubric does not encode it, the study
cannot detect it.

Final anchors:

- **5 —** `[DECIDE — from pile naming, not before]`
- **4 —** `[DECIDE]`
- **3 —** `[DECIDE]`
- **2 —** `[DECIDE]`
- **1 —** `[DECIDE]`

### 4.3 Blinding — mandatory

The primary judgment is made by the person who designed the study and who
expects System B to win. Blinding is what keeps that expectation out of the
measurement; no statistical method repairs its absence.

- Model identity is removed from every output.
- **Preference tier:** the two outputs of an item are shown side by side with
  left/right position randomized per item, independently of system.
- **Absolute tier:** outputs are shown one at a time, item order randomized, and
  the two outputs of the same item are never adjacent.
- The map from presented output to (item, system, position) is written to a key
  file that is not opened until every human rating is recorded.
- The second rater receives the same blinded material under the same protocol.
- The judge is run under the same randomization, and on the preference tier is
  run in **both** presentation orders so position bias is measured rather than
  assumed away.

### 4.4 Raters and coverage

| Rater | Preference tier | Absolute tier |
|---|---|---|
| Owner | 120 items | `[DECIDE]` subset × 2 systems |
| Second human | `[DECIDE]` items | `[DECIDE]` items |
| Judge | 120 items × 2 orders | same subset × 2 systems |

**Open gap in the current design:** the second human was specified only for the
absolute scale, but the *primary* outcome is now preference — which would leave
the primary measure with no inter-rater agreement estimate at all. The second
rater must cover a preference subset. The earlier suggestion of 100 items no
longer works: at 120 study items that is 83% of the study and not a subset in
any useful sense. The size is `[DECIDE]`, with the constraint that an agreement
estimate computed on very few items carries an interval too wide to act on.

The judge receives the same rubric text given to the humans, so all three raters
are measuring the same construct.

## 5. Primary outcome

**Primary comparison:** the owner's paired preference between System B and
System A across the 120 study items. One comparison, declared primary in
advance. Reported as: tie rate, and the proportion of non-tied items favouring
System B with a confidence interval.

**Practical significance threshold** `[DECIDE]`: the threshold must now be
stated in preference units — the smallest preference rate among non-tied items
that would change a deployment decision — because the primary instrument
changed. Under the section 2 estimand it is a decision about deploying these
two systems as configured, not about two models held at equal settings. A threshold expressed in rating points no longer applies to the
primary outcome.

## 6. Secondary outcome

Owner's absolute 1-5 rating on the 100-item subset, paired by item. Reported
with its own effect estimate and interval, labelled secondary in every report.

## 7. Statistical analysis

### 7.1 Primary — paired preference

**Note before choosing.** On a 3-level preference scale the per-item difference
takes values in {-1, 0, +1}. Wilcoxon signed-rank discards the zeros and ranks
the absolute differences — which are then all equal, all ranks tie, and the
statistic reduces exactly to the sign test. On 3 levels the two named candidates
are the same test, so there is no choice to make. Wilcoxon becomes a distinct
and more powerful option only if preference is recorded on the 5-level graded
scale of section 4.1, where magnitude exists to rank.

| Candidate | Requires | Assumptions |
|---|---|---|
| Sign test / exact binomial on non-tied items | 3-level preference | items independent; ties uninformative |
| Wilcoxon signed-rank | 5-level graded preference | above, plus symmetry of the difference distribution for a location claim |
| Cluster bootstrap / cluster permutation over recordings | either | clusters independent; correct clustering unit identified |

**Test:** `[DECIDE]`. Items **are** clustered — 3 per recording, section 3 — so
the independence assumption of the exact binomial does not hold and the
cluster-robust variant is required: resampling recordings, not items. This
constrains the choice but does not make it; the candidate above is still to be
selected with its assumptions listed.

Assumption checks, run before the test and recorded either way:

- [ ] Clustering unit confirmed and used.
- [ ] Both systems ran the identical item list with no dropouts.
- [ ] Tie rate recorded — it drives the effective sample size.
- [ ] Position-bias check on the judge's two presentation orders.

### 7.2 Secondary — absolute ratings

`[DECIDE]` from the same candidate set as the original plan (paired permutation
/ Wilcoxon signed-rank / paired t), with assumptions listed and checked.

### 7.3 Agreement (S2)

Computed separately for the two instruments, on the double-rated subsets:

- Preference agreement: human-human and human-judge.
- Absolute agreement: human-human and human-judge, with
  `[DECIDE: quadratic-weighted Cohen's kappa / Krippendorff's alpha]`. Weighted
  variants suit ordinal scales because a 4-vs-5 disagreement is not a 1-vs-5
  disagreement — confirm this is intended.

**Is the judge closer to humans on preference or on absolute rating?** This
comparison is declared here as a planned S2 outcome rather than an incidental
observation, because it is the part of this study with no established answer.

### 7.4 Multiplicity

One primary comparison, so no correction applies to it. Section 8 analyses are
exploratory, corrected with `[DECIDE: Holm / BH]`, and labelled exploratory in
every report.

**Alpha:** 0.05. **Target power:** 0.80.

## 8. Exploratory analyses

Declared here so they cannot be invented later. None supports a claim alone.

- Preference broken down by `[DECIDE: subgroup variable]`.
- The A-vs-B comparison under the judge's ratings rather than the owner's.
- Error-type breakdown of items where the two systems diverge most.
- Hallucination incidence per system, if 4.2 makes it a separate category.

## 9. Sample size and minimum detectable effect

n is fixed by collection and rating capacity, not by a power calculation, so the
power question is inverted: **what is the smallest difference detectable at
n = 120, clustered in 40 speakers?**

**Why the effort goes to speakers rather than to items.** With k speakers and m
items each, the effective sample size is

```
n_eff = k·m / (1 + (m − 1)ρ)
```

This rises with m, but is bounded above by `k / ρ` however large m becomes. At
k = 40 and ρ = 0.2 that ceiling is 200. Raising items per speaker from 3 to 15
multiplies the rating load fivefold and moves the effective sample from 86 to
158 — and it can never reach 200. Speakers buy statistical power; items past the
first few buy mostly rating work. Recruitment effort is therefore spent on
speakers, and the item count stays at 3.

**Expected effective n: 86-100.** At k = 40, m = 3: 100 items at ρ = 0.1, 86 at
ρ = 0.2. This band is written down before any data exists, and the minimum
detectable effect curve is built on it rather than on the nominal 120.

Pilot, run before the study and excluded from every analysis:

- Pilot size `[DECIDE: 20-30 items]`, rated under the final frozen rubric, and
  drawn at 3 items per speaker like the study itself. A pilot of one item per
  speaker cannot estimate ρ at all, and ρ is what the design effect turns on.
- Recorded: tie rate on the preference tier, split among non-tied items,
  spread of per-item differences on the absolute tier, and ρ within recordings.
- Output: a minimum detectable effect curve over n, computed with `evalstat`.

The tie rate is the quantity that matters most, and its effect compounds with
the design effect rather than replacing it: ties carry no information, so the
information actually available is the non-tied fraction of an already clustered
86-100, not of 120. A 40% tie rate at ρ = 0.2 would leave roughly 50 informative
items. That figure is an illustration, not a prediction — the pilot measures the
tie rate, and this plan does not assume one.

If the MDE at the expected effective n exceeds the section 5 threshold, the study
is underpowered for its own question. That is reported as the finding, not repaired by adding
items afterwards.

## 10. Stopping rule and pre-written conclusions

n is fixed in advance. Collection does not stop early, does not continue past n,
and interim results are not inspected.

Both write-ups are titled before the data exists, so that neither outcome can be
retrofitted into the other:

- **If the difference is detected:** `[DECIDE: headline]`
- **If it is not:** `[DECIDE: headline]` — e.g. a finding that a 120-item study
  with an effective sample near 90, a size typical of real evaluation practice,
  cannot separate two systems whose gap is widely assumed to be obvious. Under Project A's thesis this is a result, not a failure.

## 11. Freeze record

- Frozen on: `[DATE — not yet frozen]`
- Commit: `[HASH]`
- Tag: `[analysis-plan-001-frozen — not yet created]`
- Deviations after freeze:
  - `(none)`
