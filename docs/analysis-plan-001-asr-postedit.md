# Analysis Plan 001 — Turkish ASR Post-Editing: Haiku 4.5 vs Sonnet 5

**Status:** DRAFT — not frozen. Blanks marked `[DECIDE]` must be filled before
any study data is collected. The freeze tag in section 11 is not created until
every blank is closed; a pre-registration with open blanks pre-registers
nothing.

**Pre-registration principle:** every choice in sections 4-10 is made without
looking at outcome data. A choice made after seeing results is not an analysis,
it is a selection.

---

## 1. Question

Two models from the same family, with a known but modest expected quality gap,
convert raw Turkish ASR output into readable text. The small gap is the point,
not an inconvenience: it is the regime where evaluation practice usually fails.

- **S1 (comparison):** Is the gap between Sonnet 5 and Haiku 4.5 detectable at a
  realistic evaluation size?
- **S2 (judge validation):** How closely does an out-of-family LLM judge track
  human judgment, and how closely do two humans track each other — separately
  for relative preference and for absolute rating?

S2 is not subordinate. If human-human agreement is low, S1 is uninterpretable
regardless of its p-value.

## 2. Systems under comparison

| Role | System | Settings |
|---|---|---|
| System A | `claude-haiku-4-5-20251001` | temperature `[DECIDE]`, fixed for all items |
| System B | `claude-sonnet-5` | temperature `[DECIDE]`, byte-identical prompt to A |
| Judge | `[DECIDE: out-of-family model + exact version]` | temperature 0 |

Both systems receive the identical prompt and the identical input list in the
identical order, one generation per item. The prompt is committed alongside this
plan and does not change during the study.

**Run-to-run variance check:** if temperature > 0, re-run System A on
`[DECIDE: n]` items. The A-vs-A difference is a floor on any A-vs-B difference
the study can claim.

## 3. Materials

**Source strategy (decided):** Common Voice Turkish is used for pipeline
warm-up and blinding-harness testing only, and contributes no item to the study.
Read-aloud short sentences lack disfluency, repetition and natural sentence
boundaries, so they exercise only half of the post-editing task. The study
corpus is natural, unscripted speech.

- **Study corpus:** `[DECIDE: TBMM transcripts / podcast-TEDx / own recordings]`
- **Distinct recordings or speakers:** `[DECIDE]`
- **ASR system producing the raw output:** `[DECIDE: model + version]`, identical
  for every item.

**Item budget — the corpus must supply at least 360 items:**

| Set | Size | Used for | Enters analysis |
|---|---|---|---|
| Rubric derivation | 30 | deriving the anchors in 4.2 | no — burned |
| Pilot | `[DECIDE: 20-30]` | variance and tie-rate estimates for section 9 | no — burned |
| Study | 300 | S1 and S2 | yes |

The rubric-derivation set cannot double as the pilot: those items shaped the
rubric, so ratings on them are optimistically consistent with it.

**Clustering.** If more than one item comes from the same recording or speaker,
the unit of analysis is the recording, not the item. Number of items per
recording: `[DECIDE]`. Clustering is not avoided, it is carried into section 7
as cluster-robust resampling — ignoring it inflates significance.

**Selection:** items are drawn by `[DECIDE: sampling rule]` before any model is
run. No item is dropped after its outputs are seen.

## 4. Rating protocol

### 4.1 Two-tier measurement

The absolute scale is not applied to all 600 outputs. Rating capacity is the
binding constraint on this study and spending it entirely on a noisy measure is
the most likely way for it to die unfinished.

| Tier | Instrument | Coverage | Est. owner time |
|---|---|---|---|
| **Primary** | paired preference: A better / equal / B better | all 300 items | ~3-4 h |
| **Secondary** | absolute 1-5 rating, rubric-anchored | 100-item subset, both systems | ~5 h |

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

**Subset selection:** the 100 absolute-rated items are drawn at random before
rating begins, not chosen while rating.

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
| Owner | 300 items | 100 items × 2 systems |
| Second human | `[DECIDE]` items | `[DECIDE]` items |
| Judge | 300 items × 2 orders | 100 items × 2 systems |

**Open gap in the current design:** the second human was specified only for the
absolute scale, but the *primary* outcome is now preference — which would leave
the primary measure with no inter-rater agreement estimate at all. The second
rater must cover a preference subset. Suggested split, to be confirmed:
preference on 100 items (~1 h) plus absolute on the same 100 (~1.7 h).

The judge receives the same rubric text given to the humans, so all three raters
are measuring the same construct.

## 5. Primary outcome

**Primary comparison:** the owner's paired preference between System B and
System A across the 300 study items. One comparison, declared primary in
advance. Reported as: tie rate, and the proportion of non-tied items favouring
System B with a confidence interval.

**Practical significance threshold** `[DECIDE]`: the threshold must now be
stated in preference units — the smallest preference rate among non-tied items
that would change a deployment decision — because the primary instrument
changed. A threshold expressed in rating points no longer applies to the
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

**Test:** `[DECIDE]`. If items are clustered (section 3), the independence
assumption of the exact binomial fails and the cluster-robust variant is
required — resampling recordings, not items.

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

n is fixed by rating capacity, not by a power calculation, so the power question
is inverted: **what is the smallest difference detectable at n = 300?**

Pilot, run before the study and excluded from every analysis:

- Pilot size `[DECIDE: 20-30 items]`, rated under the final frozen rubric.
- Recorded: tie rate on the preference tier, split among non-tied items,
  spread of per-item differences on the absolute tier, and the clustering
  structure of the pilot items.
- Output: a minimum detectable effect curve over n, computed with `evalstat`.

The tie rate is the quantity that matters most: ties carry no information, so
the effective sample size is the number of non-tied items, not 300.

If the MDE at n = 300 exceeds the section 5 threshold, the study is underpowered
for its own question. That is reported as the finding, not repaired by adding
items afterwards.

## 10. Stopping rule and pre-written conclusions

n is fixed in advance. Collection does not stop early, does not continue past n,
and interim results are not inspected.

Both write-ups are titled before the data exists, so that neither outcome can be
retrofitted into the other:

- **If the difference is detected:** `[DECIDE: headline]`
- **If it is not:** `[DECIDE: headline]` — e.g. a finding that n = 300, a typical
  evaluation size, cannot separate two models whose gap is widely assumed to be
  obvious. Under Project A's thesis this is a result, not a failure.

## 11. Freeze record

- Frozen on: `[DATE — not yet frozen]`
- Commit: `[HASH]`
- Tag: `[analysis-plan-001-frozen — not yet created]`
- Deviations after freeze:
  - `(none)`
