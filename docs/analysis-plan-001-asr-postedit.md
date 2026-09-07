# Analysis Plan 001 — Turkish ASR Post-Editing:
## System A (Haiku 4.5) vs System B (Sonnet 5), default configurations

**Status:** DRAFT — not frozen. Blanks marked `[DECIDE]` must be filled before
any study data is collected. The freeze tag in section 11 is not created until
every blank is closed; a pre-registration with open blanks pre-registers
nothing.

**The study runs in two arms** — see section 3.0. Arm 1 (synthetic degradation of
openly licensed Turkish text) is active. Arm 2 (real ASR output from own
recordings) is deferred pending ethics-committee approval and is frozen with the
rest of this plan rather than designed later. Both arms' `[DECIDE]` blanks close
before the freeze, including Arm 2's.

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

- **S3 (arm equivalence, secondary):** Can synthetic degradation of written
  Turkish stand in for real ASR output as material for evaluating post-editing?
  Answerable only once both arms of section 3 have run.

S2 is not subordinate. If human-human agreement is low, S1 is uninterpretable
regardless of its p-value.

S3 is subordinate to both, and is stated as a research question rather than a
caveat because the arm split of section 3.0 makes it measurable. Two warnings
travel with it and are pre-registered here rather than added in discussion:

1. **It is an equivalence question, not a difference question.** Failing to
   detect a difference between the arms is not evidence that the arms agree. The
   claim requires an equivalence procedure and a pre-stated equivalence margin,
   both `[DECIDE]` in section 7.5.
2. **The arms still differ in more than one thing.** The D4 decision in 3.1.2
   removes the largest confound — both arms' items are output from the same
   recogniser, so a cross-arm difference cannot be blamed on invented errors —
   and that is what lifts S3 above a coarse consistency check. **Register and run
   date remain confounded with arm**, and any S3 claim states so in the claim
   itself. See 7.5.

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

**With two arms months apart, that record is no longer sufficient on its own.**
If the models change between Arm 1 and Arm 2, arm and model version are perfectly
confounded and no cross-arm comparison means anything. The mitigation is decided
in section 3.5, not here, but the requirement originates in this section: the
manifest must make the confound *visible*, and section 3.5 must make it
*measurable*.

Both systems receive the identical prompt and the identical input list in the
identical order, one generation per item. The prompt is committed alongside this
plan and does not change during the study.

**Run-to-run variance check — mandatory, and run on both systems.**
("Arm" from section 3 onwards means an arm of the *study*, not a system.) Neither system is
deterministic, because neither is given a sampling parameter. Re-run **both**
systems on `[DECIDE: n]` items and report each system's disagreement with itself
separately. Adaptive thinking may make B's run-to-run variance visibly larger
than A's, and in a paired design that asymmetry matters: one side of the pair is
noisier than the other. If a system's disagreement with itself approaches the
A-vs-B difference, that is the study's answer, and a strong one.

## 3. Materials

### 3.0 Two arms, one study

The task is the same in both arms: turn unpunctuated, irregular Turkish text into
readable text. What differs is only where the input comes from.

| Arm | Input | Status |
|---|---|---|
| **Arm 1 — synthetic** | Openly licensed Turkish text, degraded to a spoken-form transcript | **active** |
| **Arm 2 — real ASR** | Own recordings, transcribed by a fixed ASR system | **deferred — awaiting ethics approval** |

**Why the arms exist.** The audio arm requires ethics-committee approval for
human-subject recording, and that approval is measured in weeks with no
guaranteed date. Arm 1 removes the study's dependence on a decision the study
does not control. It is not a downgrade of Arm 2 and not a replacement for it:
Arm 2 is deferred, not cancelled.

**Arm 2's design below is frozen with the rest of this plan, not written later.**
When approval arrives the arm is executed, not designed. A materials section
rewritten after Arm 1's results are known would no longer be pre-registered, and
the whole point of section 11 is that nothing downstream of results gets to
change anything upstream of them.

Sections 4-11 apply to both arms unless a subsection says otherwise. Cross-arm
integrity requirements are in 3.5; they are not optional, because an arm run six
months after the other is exposed to drift the single-arm design never faced.

**Binding condition on the rubric.** The anchors derived in 4.2 are carried into
Arm 2 **unchanged**. They are not revised, retuned or re-derived when real ASR
output turns out to sit differently against them. If the instrument changes
between the arms, the arms are measuring different things and no comparison
between them — S3 included — means anything. A poor fit of the frozen anchors to
Arm 2's material is itself a finding and is reported as one; it is not a licence
to move the anchors.

**Arm is a subgroup variable, not a nuisance.** It is declared in section 8 and
carried per item in the manifest. The question of whether synthetic degradation
can stand in for real ASR error is the study's secondary research question S3,
not a caveat in a discussion section.

### 3.1 Arm 1 — synthetic degradation of licensed text (active)

#### 3.1.1 Source and licence — read from the source, not from memory

**Corpus:** Turkish Wikipedia (Vikipedi) article text.

**Licence, verified against the Wikimedia Foundation Terms of Use and the
Vikipedi copyright page rather than from recollection:** text contributions are
licensed under **CC BY-SA 4.0** and, dually, the unversioned GFDL with no
invariant sections; the Terms state that "reusers may comply with either license
or both". Attribution is satisfied by a hyperlink or URL to the article's history
page, by a link to an alternative stable copy, or by listing the authors.

Three consequences, and none of them is cosmetic:

1. **Derivative works are permitted.** This is the exact clause TEDx failed. The
   study's central operation — cut, derive, rewrite, publish so that others can
   reproduce — is licensed here and prohibited there. The source changed because
   the licence changed, not because the content is better.
2. **Share-alike binds the output, and the decision is to embrace it.**
   **Everything this study publishes goes out under CC BY-SA 4.0**: the source
   extracts, the synthesised audio, the ASR transcripts and the two systems'
   post-edited outputs. The question of whether the model outputs are legally
   derivative works of the source text is therefore not answered, it is made
   irrelevant — the answer would change nothing about what is published. The
   decision costs nothing and closes a dispute that could otherwise have run
   until publication day.
3. **Wikipedia text changes.** The **revision id** of every sourced article is
   pinned and written to the run manifest alongside the article URL, the fetch
   timestamp and the SHA-256 of the extracted text. An article cited without a
   revision id is not reproducible; a reader six months later would fetch
   different text. This is the same rule that governs model ids in section 2.

**Markup extraction is pre-registered, not improvised.** Wikitext carries
infoboxes, tables, lists, section headers, reference markers, image captions,
navigation boxes and templates, and none of them is prose a person would ever
speak. The extraction rule — which elements are dropped, which are kept, and how
inline templates are resolved — is written down and committed before any item is
drawn, because "clean it up until it looks right" is a rule that adapts itself to
what the cleaner sees.

**Register is Arm 1's structural limitation, and it is stated here rather than
discovered later.** Wikipedia is written language. Its syntax is written syntax:
long subordinate chains, no false starts, no abandoned constructions, a
propositional density no speaker sustains. Degradation can strip the *formatting*
of written language and can add the *surface* of speech, but it does not convert
written syntax into spoken syntax. Whatever degradation protocol is chosen in
3.1.2, Arm 1's items remain written prose wearing a transcript's clothes. This
bounds S3 in advance: a match between the arms would be informative, and a
mismatch would not identify which of several differences caused it. See 3.4.

#### 3.1.2 Degradation protocol (decided): D2 disfluency injection, then TTS, then ASR

**Decided: D4 — a TTS-to-ASR round trip — carrying D2 disfluency injection ahead
of synthesis, with a controlled acoustic degradation layer between synthesis and
recognition.**

The chain is:

```
licensed text → D2 disfluency injection → TTS synthesis → acoustic degradation
              → 30-second window selection (VAD) → Whisper large-v3-turbo → item
```

From the window-selection step onward this is byte-for-byte the Arm 2 chain.
`segmentation.py`, the speech-ratio threshold, the one-window-per-third rule and
the edge-word rule are therefore **not shelved: they are used immediately**, in
Arm 1, months before Arm 2 needs them.

**Why this option rather than a rate table.**

1. **The obstacle removed was human subjects, not audio.** Ethics approval,
   informed consent and 40 recruited speakers are what put Arm 2 on an
   uncontrollable timeline. D4 has audio and no human subjects. It is the removal
   of the actual blocker, not a retreat from the audio task.
2. **It makes the two arms structurally identical.** Both arms cut in seconds,
   both run VAD, both feed the same recogniser. The item-length question that
   would otherwise have needed a words-versus-sentences decision (options L1-L3,
   now closed) does not arise: the item is a 30-second window in both arms
   because the material is audio in both arms.
3. **Hallucination stays measurable.** Under D1-D3 nothing gives a system a
   reason to fabricate, so the rubric's most important category — fluent but
   fabricated text, the distinction WER cannot express — would have had no
   material at all. Real recogniser output on degraded audio can.
4. **The errors come from the mechanism, not from an assumption.** They are
   produced by the same Whisper checkpoint Arm 2 uses, so S3 is not comparing an
   invented error distribution against a real one.
5. **It puts the study owner's audio-engineering knowledge inside Arm 1** rather
   than parking it until Arm 2.

**Why the punctuation finding does not bite here.** 3.1.1's constraint was that
stripping punctuation from written text would present Arm 1 with a different task
from Arm 2, because Whisper emits punctuated, capitalised, numeral-formatted
output of its own. Under D4 the question dissolves: Arm 1's items are Whisper
output, produced by the same checkpoint, so whatever formatting behaviour it has
is present in both arms by construction rather than by imitation.

**Two layers against the headroom risk.** Synthetic speech is clean and
hyper-articulated, so a naive round trip would produce near-perfect transcripts
and leave nothing to post-edit — the same failure the `large-v3-turbo` choice was
made to avoid.

- **Layer 1 — disfluency before synthesis (D2).** Filled pauses, repetition,
  false starts and restarts are injected into the *text*, so the TTS speaks them
  and the recogniser meets them as audio. Injected after synthesis they would be
  a text artefact; injected before, they are speech.
- **Layer 2 — acoustic degradation.** Applied to the synthesised audio before
  recognition:

  | Knob | Parameter | Value |
  |---|---|---|
  | Additive noise | SNR in dB, noise type | `[DECIDE]` |
  | Band limiting | telephone band, 8 kHz | `[DECIDE: applied to all / a proportion]` |
  | Reverberation | convolution with an impulse response at a measured RT60 | `[DECIDE: RT60 values]` |

  **Being synthetic is the advantage here.** In Arm 2 the acoustic condition is
  whatever the room gave; in Arm 1 it is a dial. The values are study-owner
  decisions, recorded per item in the manifest so they are available as a
  covariate, and set before any item is drawn.

**De-risking gate — pre-registered, threshold written before the data.**

1. Run a **5-article D4 pilot** through the full chain.
2. Measure Whisper WER against the pre-synthesis reference text.
3. **If WER < 8%**, the post-editing task is too easy for the comparison to have
   anything to separate. Harden the acoustic degradation layer and repeat.
4. **After two hardening rounds**, if WER is still below the threshold, the D4
   arm is abandoned and the study falls back to **D1 + D2** — pure text
   degradation, with the hallucination category then declared unmeasurable in
   Arm 1.

The 8% threshold and the two-round limit are fixed here, before any WER is
observed. A threshold set after seeing the first number would be a selection
rule. The gate's outcome — pass, harden, or fall back — is recorded in the
manifest either way, including the WER at each round.

The 5 gate articles are burned: they enter no set that is rated, and
`burned.py` records them.

**Seeding.** The disfluency injection seed, the acoustic degradation seed, the
TTS sampling seed where the model exposes one, and the window-selection seed are
each recorded in the run manifest. The whole chain regenerates from them.

**What the protocol must still fix, `[DECIDE]`:**

- The disfluency inventory and its rates. No Turkish spontaneous-speech
  disfluency corpus surfaced (3.1.3), so this has no off-the-shelf empirical
  basis and the rates are the study owner's, declared rather than derived.
- Whether acoustic parameters are **fixed** across items or **varied** over a
  pre-registered range. Varied is closer to Arm 2 and adds a per-item covariate;
  fixed makes the arm homogeneous and understates real variance.
- **Speaker variation — see 3.1.6.** Arm 2 has 40 speakers. A single-voice Arm 1
  would remove speaker identity as an error driver entirely, which changes ρ and
  weakens S3.

#### 3.1.3 What the literature does and does not supply


Searched at source rather than recalled; the summary is deliberately short
because the material is thin.

- **Turkish punctuation and capitalisation restoration** has a directly relevant
  recent result. In a Turkish news corpus (`batubayk/TR-News`, 760 MB) used for
  BERT-based punctuation and capitalisation correction, the training-set class
  distribution is period 3.7M, comma 3.3M, **apostrophe 2.3M**, hyphen 276K,
  colon 152K, question mark 71K, semicolon 57K, exclamation 15K. The apostrophe
  ranking third is a Turkish-specific fact with direct bearing on D1: apostrophes
  separate suffixes from proper nouns (*Ankara'ya*, *TBMM'nin*), so removing them
  is not a cosmetic strip — it destroys a morpheme boundary the post-editor must
  reconstruct. Capitalisation is treated as a three-class problem (lowercase /
  initial capital / all caps).
- **Turkish ASR error taxonomies are not well covered.** Reported Whisper WER for
  Turkish spans roughly 4.3%-14.2% depending on corpus and checkpoint, with a
  fine-tuned Whisper Small reported at 12.89%. These are aggregate rates, not
  category breakdowns. No Turkish study with a quantified per-category error
  taxonomy surfaced.
- **For morphologically rich languages generally**, error analysis reports
  word-final morphological suffix confusion and phoneme substitution as dominant
  failure modes, with character-level substitutions inside otherwise-known words
  contributing substantially to WER — the mechanism being that a single
  word-final character changes case, tense or agreement.
- **No Turkish spontaneous-speech disfluency corpus** with filled-pause and
  repetition annotation surfaced. Disfluency annotation schemes exist for
  English, French and Spanish. D2's inventory and rates therefore have no Turkish
  empirical basis available off the shelf.
- **On synthetic versus real ASR error**, the existing work cuts both ways.
  Controlled injection at fixed target WER is used precisely because real ASR
  error rates are uneven and confound error magnitude with error structure.
  Against that, work such as MEDSAGE treats the realism of synthetic ASR errors
  as something to be *validated* against real transcripts rather than assumed,
  and TTS-then-ASR round-tripping is used as the more faithful alternative — the
  D4 option above. The stated caveat in that literature is exactly S3's question:
  validity depends on whether the synthetic error distribution matches the real
  one.

The honest reading: the literature supports D1's formatting transforms with real
Turkish data, gives D3's suffix-error emphasis a general-linguistic
justification, gives D2 almost nothing Turkish-specific, and independently
suggests D4 as the way to stop guessing.

#### 3.1.4 Cluster unit (decided) and item construction

**Cluster unit: the article (C1).** Three items per article, drawn from different
sections. The article is the structural analogue of the recording — one topic,
one register, one authorial voice — so section 3.4's design effect, section 9's
`n_eff` argument and the `cluster=` case study carry over unchanged.

The two rejected candidates are recorded with their reasons, because a rejected
option without a reason gets re-proposed:

- **The section (C2) was rejected as anti-conservative.** Sections inside an
  article still share topic and vocabulary, so article-level correlation would
  remain unmodelled and the intervals would be too narrow — precisely the error
  cluster-robust inference exists to prevent.
- **The topic domain (C3) was rejected on cluster count.** Roughly eight clusters
  does not give cluster resampling enough units to produce a usable interval.

**Clustering in Arm 1 is a choice, not a constraint, and is recorded as one.**
Articles are nearly free, so 120 articles at one item each would remove the
design effect and give `n_eff = 120` rather than 86-100. Three items per cluster
is kept anyway, for two reasons: the arms must share a design for S3 to compare
them, and the clustered case is what `evalstat` exists to demonstrate. The price
is roughly 20 to 34 effective items, paid knowingly.

**Item construction: identical to Arm 2.** Because D4 produces audio, the item is
a 30-second window of synthesised speech, selected by `segmentation.py` under the
same rules as 3.2 — seeded random offsets restricted to VAD speech regions, one
window per third, the pre-registered speech-ratio threshold, and the edge rule
that cuts at the clock and drops the leading and trailing partial word from the
ASR output.

**The item-length question is therefore closed.** Options L1 (match word count),
L2 (match error opportunity) and L3 (match sentence count) existed only because a
text arm has no seconds to cut on. Under D4 both arms cut in seconds, so no
matching rule is needed and the "counted before or after degradation" fork does
not arise either.

**Minimum article length.** The Arm 2 constraint — three 30-second windows at
90-second separation need about 7 minutes of audio, with 7 chosen over 5 to leave
room for windows the speech-ratio threshold rejects — becomes a minimum *synthesis
duration*, and therefore a minimum article word count at the chosen TTS speaking
rate. The rate is measured on the gate articles of 3.1.2 and the resulting word
threshold is pre-registered before selection, not applied after seeing which
articles fail.

**Two Wikipedia-specific hazards for the drawing rule:**

- **The lead section is a different register** from the body: summary-dense, high
  proper-noun and date density, short sentences. Drawing one item from the lead
  and two from the body would put systematic heterogeneity inside every cluster.
  `[DECIDE]`: exclude the lead throughout, or include it throughout. Either is
  defensible; letting it fall out of the sampler is not.
- **Section separation** is the analogue of the 90-second gap and exists for the
  same reason — adjacent material shares topic and vocabulary, raising ρ. Under
  D4 the 90-second rule applies directly to the synthesised audio, so this is
  handled by `segmentation.py` rather than by a paragraph-distance rule. What
  remains `[DECIDE]` is whether an article is synthesised whole, or section by
  section with the sections concatenated.

#### 3.1.5 `[DECIDE]` — TTS selection, with licences read at source

**The selection rule, before the candidates.** A TTS licence matters here in a
way it usually does not, because the generated audio is *published* as part of a
CC BY-SA 4.0 corpus. The question is therefore not "may I run this model" but
**"does this licence reach the model's output?"** Most software licences do not:
running a GPL-3.0 program does not make its output GPL, and an MIT model licence
does not bind generated audio. Some model licences do reach outputs explicitly.
That distinction, not the licence's general permissiveness, decides the field.

A second rule follows from case 9 of the setup retrospective: a licence marking
is only as good as the marker's right to grant it. A permissive tag on a model
fine-tuned from non-commercial base weights is the same failure shape as a CC BY
marking placed on a TEDx upload by an organiser who did not hold the right.

Candidates, with licences read from the model card, LICENSE file or dataset card
rather than from recollection:

| Candidate | Licence, as read at source | Turkish | Status |
|---|---|---|---|
| **Chatterbox** (Resemble AI) | **MIT** on the model card; languages list includes `tr` | yes, in the multilingual model | **No licence blocker.** But every generated file carries Resemble AI's "Perth" neural watermark — the card states the watermark is imperceptible and survives compression and editing. Not a restriction, but a property of published audio that must be declared in the dataset card. It arguably helps: it marks the corpus as synthetic |
| **eSpeak NG** | **GPL-3.0** (`COPYING`); Turkish listed in `docs/languages.md` as `trk`/`tr` | yes | **No licence blocker** — a GPL licence on the synthesiser does not reach its audio output. Formant synthesis, deliberately robotic. Under the 3.1.2 headroom gate that is a **feature**: it is the candidate least likely to floor the WER |
| **Orkhon-TTS** (hcsolakoglu) | Model card declares **Apache-2.0**; architecture is F5-TTS | yes, Turkish-specific, alpha, single speaker | **Licence chain unresolved.** The F5-TTS base weights (`SWivid/F5-TTS`) are **CC-BY-NC-4.0**. If Orkhon was fine-tuned from those weights rather than trained from scratch, the Apache-2.0 marking may exceed what the author could grant. Resolve with the author before use; do not resolve by assuming |
| **`Omarrran/turkish_finetuned_speecht5_tts`** | Model **MIT**, base `microsoft/speecht5_tts` MIT | yes | **Provenance problem.** Its training set `erenfazlioglu/turkishvoicedataset` carries **no licence field at all** and is tagged `synthetic-voice` — TTS output used to train TTS, upstream unknown. The card also states it was made "for review purposes only… not a production-ready model" |
| **Coqui XTTS-v2** | **CPML**, quoted verbatim: *"This license allows only non-commercial use of a machine learning model **and its outputs**"* | yes, 17 languages including `tr` | **Eliminated.** The licence reaches the output by its own first line, so the audio cannot be published under CC BY-SA 4.0. Same wall as TEDx, a different clause |
| **`facebook/mms-tts-tur`** | **CC-BY-NC-4.0**, stated on the model card | yes, Turkish-specific VITS | **Eliminated.** NC cannot be relicensed as BY-SA |
| **Piper `tr_TR-dfki-medium`** | Engine MIT (archived repo) / GPL-3.0 (active fork). The voice's `MODEL_CARD` names its dataset as `marytts/dfki-ot-data` under **CC BY-NC-SA 4.0** | yes — the only Turkish Piper voice | **NC-SA in the chain**, and BY-NC-SA cannot be relicensed as BY-SA. Also fine-tuned from a US English voice, so accent artefacts are plausible |
| **Kokoro-82M** | Apache-2.0 | **no** — model card lists `language: en` only | Eliminated: no Turkish |
| **Zonos-v0.1** | Apache-2.0 | **no** — README: English, Japanese, Chinese, French, German | Eliminated: no Turkish |
| Commercial APIs (Google, Azure, ElevenLabs) | provider terms of service, not a public licence | yes | **Not assessed.** Permission to *use* an API is a different question from permission to *redistribute* the generated audio as a public dataset. Each provider's terms are read at source before it enters this table |

Two candidates survive with no licence blocker: **Chatterbox** and **eSpeak NG**.
They fail in opposite directions — Chatterbox is natural enough to risk flooring
the WER at the 3.1.2 gate, eSpeak NG is robotic enough to risk making the task
unrepresentatively hard — and they can be used together, with synthesiser
recorded per item as a covariate. **The choice is `[DECIDE]`.**

**Speaker variation is an open decision and a real threat to S3.** Arm 2 has 40
speakers; speaker identity is one of the largest drivers of ASR error. An Arm 1
built on a single voice removes that driver entirely, which lowers between-cluster
variance, changes ρ, and makes the arms differ in one more way than intended.
`[DECIDE]` among:

- one voice for all items, with the limitation declared;
- eSpeak NG voice variants — crude parametric variation in pitch and rate;
- Chatterbox voice cloning from reference clips, which needs a licensed source of
  reference voices. **Common Voice Turkish is the obvious candidate and its terms
  must be re-read at source**: as of October 2025 Mozilla moved Common Voice
  distribution to the Mozilla Data Collective, so the licence this plan relies on
  for warm-up material in 3.3 is itself due for verification. Using recordings of
  real people as cloning references also reopens, in a smaller form, the consent
  question the arm split was made to avoid.

#### 3.1.6 Item budget and burned sets


The structure of section 3.2's budget is retained: a rubric-derivation set that
is burned, a pilot that is burned, and 120 study items.

| Set | Size | Used for | Enters analysis |
|---|---|---|---|
| **D4 headroom gate** | **5 articles** | the WER gate of 3.1.2; fixing the acoustic degradation level | **no — burned** |
| Rubric derivation | 30 items | deriving the anchors in 4.2 | no — burned |
| Pilot | `[DECIDE: 20-30]` items | variance, tie rate and ρ estimates for section 9 | no — burned |
| Study | 120 items | S1 and S2 | yes |

Clusters are disjoint across all four sets, not merely items: two items from one
article landing in different sets would leak the rubric into the study through
shared vocabulary and topic. Under C1 the requirement is at least
`5 + 40 + 10 + [pilot/3]` distinct articles.

The gate set is burned for a stronger reason than the others: its whole purpose
is to *tune the acoustic degradation level against observed WER*. Items whose
difficulty was set by looking at them cannot then be rated as study items.

The rubric-derivation set cannot double as the pilot, for the reason already
given in 3.2: those items shaped the rubric, so ratings on them are
optimistically consistent with it. `burned.py` enforces the disjointness.

**Shakedown.** Arm 2's rule — run the first 10 speakers end to end before
recording the rest — has an Arm 1 analogue that costs almost nothing: after the
5-article gate passes, the next 10 articles are run end to end through the full
chain, both systems and the blinded sheet, before the remaining articles are
drawn. A pipeline fault then costs 10 articles to discover. Those 10 articles
yield exactly the 30 rubric-derivation items, which are burned in any case.

**Selection:** items are drawn by `[DECIDE: sampling rule]` before any model is
run. The rule covers article selection (domain balance, length filter, quality
filter) as well as window selection within an article. No item is dropped after
its outputs are seen.

### 3.2 Arm 2 — real ASR from own recordings (deferred, awaiting ethics approval)

> **Status: deferred, awaiting ethics-committee approval. Not cancelled and not
> revised.** Everything below was decided before the arm split and is retained at
> full strength, including the reasoning behind decisions that are now dormant.
> The reasoning for a closed decision is not deleted when the decision is
> shelved: without it, the decision would be re-litigated from scratch on the day
> approval arrives.
>
> **What is deferred is the human-subject recording, and only that.** The
> ethics-committee dependency is consent, recruitment and 40 recorded people —
> not audio. Under the D4 decision in 3.1.2 the audio machinery below (window
> selection, the VAD threshold, the edge rule, the Whisper checkpoint) is in use
> from Arm 1 onward. The deferral is narrower than it looks.

**Study corpus (decided): own recordings.** 40 speakers, each recorded for at
least 7 minutes of unprepared Turkish speech, contributing 3 items. Holding the
rights removes the licence question entirely, and it removes half of the
exclusion rules with it: there is no music bed, no jingle, no applause and no
second speaker to screen for, because the recording is made without them.
Speaker metadata is defined rather than inferred, which hands section 8 a
subgroup variable that found material cannot supply, and Project B needs clean
source material for its acoustic conditions regardless — the recordings are made
once and serve both projects.

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
  before the study runs. **Added at the arm split:** the checkpoint's actual
  punctuation, capitalisation and number-formatting behaviour is recorded from
  observed output before the rubric is frozen — see 3.1.2, where it constrains
  Arm 1's degradation target.

**Collection order.** The first 10 speakers are recorded and run end to end —
segmentation, ASR, both systems, blinded sheet — before the remaining 47 are
recorded. A pipeline fault then costs 10 speakers to discover instead of 57.
Those 10 speakers yield exactly the 30 items the rubric-derivation set needs, and
that set is burned in any case, so the shakedown consumes nothing the study could
otherwise have used.

**Segment construction (decided).** Every item is a 30-second window of one
recording. `segmentation.py` implements this and is retained unchanged — **and,
since the D4 decision in 3.1.2, it is not shelved at all.** Arm 1 produces audio,
so the same module, the same VAD threshold, the same one-window-per-third rule
and the same edge rule run in Arm 1 first and are exercised against real data
long before Arm 2 needs them. The rules below are written for Arm 2 and hold
verbatim in Arm 1.

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

**Cluster unit:** the recording. In a single-speaker talk the recording and the
speaker coincide. In a multi-speaker episode the speaker is nested inside the
episode, so every item is drawn from a single speaker and the cluster is the
episode — the larger unit, which is the conservative choice.

**Podcast material under written permission is a secondary source within this
arm, not a prerequisite.** Recordings may be added if a rights holder grants
permission covering all four of: segmentation, derivation of transcripts,
publication of those derived transcripts, and reproduction by third parties.
Permission that covers use but not redistribution is of no use to a study whose
point is reproducibility. Where such material is added, the source is recorded
per item in the manifest as a subgroup variable.

### 3.3 Sources eliminated, and why — retained

Closed decisions keep their reasoning. Each of these was a live candidate, and
each was closed for a reason that still holds.

**Common Voice Turkish** is used for pipeline warm-up and blinding-harness
testing only, and contributes no item to either arm's study set. Read-aloud short
sentences lack disfluency, repetition and natural sentence boundaries, so they
exercise only half of the post-editing task.

**Its terms are due for re-verification and are not assumed here.** As of October
2025 Mozilla moved Common Voice distribution to the Mozilla Data Collective, so
the licence under which this plan may use the corpus — for warm-up, and
potentially as a source of cloning reference voices under 3.1.5 — is read at the
current distributor before any such use, not carried over from what the licence
used to be. This is the same rule that governs the Wikipedia licence in 3.1.1 and
the TTS licences in 3.1.5.

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

This entry is why 3.1.1 reads the Wikipedia licence at source and quotes the
clause that permits derivatives. The failure in the TEDx case was not choosing
TEDx; it was marking the licence as something to check later and then not
checking it.

**TBMM transcripts** were rejected earlier despite being the best content fit —
natural, unprepared, speaker-diverse, and already carrying a reference
transcript. Parliamentary material is dense in proper nouns and institution
names, and the two systems may behave differently on political content. That is
a variable this study does not want to measure and cannot control, and it would
sit inside the primary comparison rather than beside it. **The same objection
applies to Arm 1's article selection:** a domain filter that lets politically
charged articles in reintroduces exactly this variable through the text arm.

### 3.4 Clustering — both arms

If more than one item comes from the same cluster, the unit of analysis is the
cluster, not the item. Items per cluster: 3, in both arms. Clustering is not
avoided, it is carried into section 7 as cluster-robust resampling — ignoring it
inflates significance.

| Arm | Cluster | Why that unit |
|---|---|---|
| Arm 1 | the article (decided, 3.1.4) | Shared topic, register, vocabulary and synthesised voice within the unit |
| Arm 2 | the recording | Shared topic, acoustic state and speaker energy within the unit |

At 3 items per cluster the design effect is `1 + 2ρ`, so the effective sample
size is `120 / (1 + 2ρ)`: 100 items at ρ = 0.1, 86 at ρ = 0.2. ρ is not known
before the pilot, which is why the pilot must itself be clustered (section 9),
and why each arm needs its own pilot (3.5).

**ρ is not assumed equal across arms.** Within-article correlation and
within-recording correlation are different quantities with no reason to coincide,
so the design effect is estimated separately per arm and the effective sample
sizes are reported separately.

### 3.5 Cross-arm integrity

Two arms separated by months are exposed to drift a single-arm study never faced.
These requirements exist so that S3 compares arms rather than comparing dates.

**Model version is confounded with arm, and this is the most serious of the
four.** Section 2 reads model ids from the Models API at run time. If Arm 2 runs
after a model update, the arm variable and the model version are perfectly
confounded, and any cross-arm difference is uninterpretable.

**Decided: X2 — a bridging set.** A pre-registered subset of Arm 1's items,
`[DECIDE: size]`, is re-run at Arm 2 time on whatever the current models are, and
re-rated under the frozen rubric. Any drift in Arm 1's own results is then
*measured* and can be separated from the arm effect.

Snapshot pinning (X1) was rejected as the primary mechanism, and the reason
generalises: it assumes the snapshot will still be servable months from now,
which is an assumption about an external system's future state held in the
plan's head rather than read from the system. That is the same rule violation as
writing a model id from memory — the manifest records what was read, and a design
must not rest on what has not been read yet. X1 is still recorded opportunistically:
if the identical snapshot ids happen to be available at Arm 2 time, that fact is
written to the manifest and strengthens the bridging comparison. It does not
replace it.

Declaring the confound and accepting it (X3) was rejected because it produces no
measurement.

**Rubric transfer: closed, not open.** The anchors derived on Arm 1 are carried
into Arm 2 unchanged, per the binding condition in 3.0. Deriving separate anchors
per arm was rejected outright: it would make the arms non-comparable and destroy
S3. Anchor misfit in Arm 2 is reported as a finding, not repaired by moving the
anchors.

**Pilot is not transferable.** ρ, the tie rate and the spread of per-item
differences are all properties of the material. An ρ estimated over articles says
nothing about ρ over recordings. Arm 2 runs its own pilot, burned, before its
study items are rated.

**Arm 2 is not blind to Arm 1.** By the time Arm 2 runs, Arm 1's results are
known to the person making Arm 2's primary judgement. Pre-registration is the
only remaining protection, which is why 3.0 requires Arm 2's design to be frozen
now rather than written on approval, and why any post-freeze change to it is
logged as a deviation in section 11 rather than made silently.

## 4. Rating protocol

### 4.1 Two-tier measurement

The absolute scale is not applied to all 240 outputs. Rating capacity is a
binding constraint on this study and spending it entirely on a noisy measure is
one of the likelier ways for it to die unfinished.

| Tier | Instrument | Coverage | Est. owner time |
|---|---|---|---|
| **Primary** | paired preference: A better / equal / B better | all 120 items | ~2-3 h |
| **Secondary** | absolute 1-5 rating, rubric-anchored | **40 items**, both systems | ~1 h per 40 ratings |

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

**Subset size (decided): 40 items, and the secondary tier is labelled
exploratory.** At 300 study items a 100-item absolute subset covered a third of
the study and the two tiers were plainly separate instruments. At 120 items that
same 100 would cover 83%, the tiers would nearly coincide, and the two-tier
design would stop being a way of spending capacity and become duplication. Forty
of 120 restores the one-third ratio and keeps the tiers distinct.

**The cost is stated here, before the data, so it cannot become an excuse
after it.** An agreement coefficient computed on 40 items carries a wide
confidence interval. That is accepted, and it is why the absolute tier and every
estimate resting on it — section 6's secondary outcome and section 7.3's absolute
agreement — are **labelled exploratory in the pre-registration**, not merely
"secondary". No claim in this study rests on the absolute tier alone. Reporting a
wide interval as though it were a null result, or discovering the width only at
write-up and offering it as a limitation, are both foreclosed by saying it now.

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
| Owner | 120 items | 40-item subset × 2 systems |
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

## 6. Secondary outcome — exploratory

Owner's absolute 1-5 rating on the **40-item** subset, paired by item. Reported
with its own effect estimate and interval, and labelled **exploratory** in every
report, per the decision in 4.1. Forty items is a third of the study, which keeps
the two tiers distinct; it is also few enough that the interval will be wide, and
that width is declared in advance rather than discovered at write-up.

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
| Cluster bootstrap / cluster permutation over clusters | either | clusters independent; correct clustering unit identified |

**Test:** `[DECIDE]`. Items **are** clustered — 3 per cluster in both arms,
section 3.4 — so the independence assumption of the exact binomial does not hold
and the cluster-robust variant is required: resampling clusters, not items. The
cluster is the article in Arm 1 and the recording in Arm 2; the resampling code
is the same, only the unit column differs. This constrains the choice but does
not make it; the candidate above is still to be selected with its assumptions
listed.

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

### 7.5 Arm equivalence (S3)

Runs only when both arms are complete. Nothing here is computed on Arm 1 alone.

**Arm is a between-cluster variable, not a within-item one.** The paired design
of 7.1 holds *inside* an arm: each item has an A output and a B output. Across
arms nothing is paired — no article corresponds to a recording — so the cross-arm
comparison is unpaired and its unit is the cluster, as in 7.1.

Quantities compared across arms:

- direction of the A-versus-B preference;
- magnitude of the effect, with its interval;
- tie rate;
- ρ and the resulting effective sample size;
- judge-human and human-human agreement from 7.3;
- distribution of error categories from 4.2.

**Test (decided): two one-sided tests (TOST) on the cross-arm difference, with
the equivalence margin fixed in the pre-registration.** A conventional difference
test answers the wrong question here: a wide, uninformative interval would
produce a non-significant result and could be misread as "the arms agree", which
is the failure mode this subsection exists to prevent.

| | Value |
|---|---|
| Equivalence margin, in preference units | `[DECIDE]` — fixed before either arm is analysed |
| Assumptions | clusters independent within arm; the two arms' cluster-level estimates are comparable in scale; margin predates all analysis |
| Resampling | cluster-robust, over articles in Arm 1 and recordings in Arm 2 |

The margin is the whole test. Set it after seeing the arms and TOST becomes a
selection rule wearing an equivalence test's clothes.

**What the resulting claim may and may not say.** D4 removes the error-mechanism
confound: both arms' items are output from the same recogniser, so a cross-arm
difference is no longer attributable to "one arm's errors were invented". That is
what lifts S3 above a qualitative consistency check. **Two confounds remain and
are declared in the claim itself, not in a footnote:**

- **Register.** Arm 1 is Wikipedia prose spoken by a synthesiser; Arm 2 is
  unprepared human speech. The syntax differs even when the error mechanism does
  not.
- **Date.** The arms run months apart. The bridging set of 3.5 measures the
  resulting drift but does not remove it.

Any equivalence claim from S3 is therefore stated as equivalence **between these
two arms as constituted**, not as a general finding that synthetic material
substitutes for real ASR output.

Assumption checks specific to S3, run before the comparison and recorded either
way:

- [ ] Model versions across arms confirmed identical, or the bridging set of 3.5
      analysed and any drift reported.
- [ ] Rubric anchors confirmed unchanged across arms, or the drift logged as a
      section 11 deviation.
- [ ] ρ estimated separately per arm, not pooled.
- [ ] Equivalence margin confirmed to predate both arms' analyses.

## 8. Exploratory analyses and subgroup variables

Declared here so they cannot be invented later. None supports a claim alone.

### 8.1 Subgroup variables recorded per item

Every one of these is written into the manifest at generation time, not
reconstructed afterwards. A subgroup that has to be reconstructed from filenames
after results are seen is a subgroup that was chosen after results were seen.

| Variable | Values | Available in |
|---|---|---|
| **`source`** | `synthetic` / `real_asr` | both arms — this is the arm |
| `domain` | `[DECIDE: category list]` | Arm 1 |
| `tts_engine`, `tts_voice` | as selected in 3.1.5 | Arm 1 |
| `disfluency_rate` | as fixed by 3.1.2, if rates are varied | Arm 1 |
| `snr_db`, `band_limit`, `rt60` | acoustic degradation, per item | Arm 1 |
| `revision_id`, `article_url` | pinned per item | Arm 1 |
| speaker attributes | `[DECIDE: which]` | Arm 2 |
| `recording_source` | own recording / permitted podcast | Arm 2 |
| `consent_tier` | 1 / 2 | Arm 2 |
| `bridging` | true for the 3.5 re-run subset | Arm 1 items, re-run at Arm 2 time |

**`source` is the arm variable, and it is the reason S3 exists.** It was already
in the plan before the arm split — as own-recording versus permitted podcast
material — for the same reason it is here now: a difference between kinds of
material would otherwise sit unlabelled inside the primary comparison. The arm
split widens the variable rather than introducing it.

**A subgroup analysis over `source` is not S3.** The exploratory breakdown below
asks whether the A-versus-B preference *differs* by arm. S3, in section 7.5, asks
whether the two arms *agree* closely enough for one to substitute for the other.
Those are different questions with different tests, and only the second is
pre-registered as a research question.

### 8.2 Exploratory analyses

- Preference broken down by `source` (arm), when both arms are complete.
- Preference broken down by `[DECIDE: further subgroup variable]` within arm.
- The A-vs-B comparison under the judge's ratings rather than the owner's.
- Error-type breakdown of items where the two systems diverge most.
- Hallucination incidence per system, if 4.2 makes it a separate category.
  **Measurable in both arms**, which is one of the reasons D4 was chosen in
  3.1.2: real recogniser output on degraded audio gives a system something to
  fabricate from, and pure text degradation does not.
- Preference against the acoustic covariates of 3.1.2 within Arm 1 — whether the
  A-versus-B gap widens as SNR falls. Exploratory, and only available because
  Arm 1's acoustics are a dial rather than a given.

## 9. Sample size and minimum detectable effect

n is fixed by collection and rating capacity, not by a power calculation, so the
power question is inverted: **what is the smallest difference detectable at
n = 120, clustered in 40 units?** Computed separately per arm, because ρ is a
property of the material and the arms do not share it.

**In Arm 2 the binding constraint is collection; in Arm 1 it is rating.** The
argument below about spending effort on speakers rather than items was written
for Arm 2, where each speaker costs a recording session, consent and 7+ minutes
of audio. In Arm 1 clusters are nearly free, so 120 articles at one item each
would remove the design effect entirely and give `n_eff = 120`. Arm 1 keeps three
items per cluster anyway — see 3.1.4 — because the arms must share a design for
S3, and because the clustered case is what `evalstat` exists to demonstrate. That
is a decision, and it costs roughly 20 to 34 effective items.

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
  drawn at 3 items per cluster like the study itself. A pilot of one item per
  cluster cannot estimate ρ at all, and ρ is what the design effect turns on.
- Recorded: tie rate on the preference tier, split among non-tied items,
  spread of per-item differences on the absolute tier, and ρ within clusters.
- **Run once per arm.** Arm 1's pilot does not stand in for Arm 2's; see 3.5.
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

**The two-headline rule applies per arm, and per question.** Four headlines are
written before any data exists.

Arm 1 (S1):

- **If the difference is detected:** `[DECIDE: headline]`
- **If it is not:** `[DECIDE: headline]` — e.g. a finding that a 120-item study
  with an effective sample near 90, a size typical of real evaluation practice,
  cannot separate two systems whose gap is widely assumed to be obvious. Under Project A's thesis this is a result, not a failure.

S3, written now and not on the day Arm 2 finishes:

- **If the arms agree within the margin:** `[DECIDE: headline]`
- **If they do not:** `[DECIDE: headline]` — a finding that synthetic degradation
  of written text does not substitute for real ASR output is a result about
  evaluation practice, and a more useful one than the agreement case.

**Arm 2 does not stop early either, and it does not start early.** Arm 2 begins
when ethics approval arrives, not when Arm 1's results suggest it would be
interesting to check something. If approval never arrives, Arm 1 is reported
alone, with S3 reported as unanswered rather than quietly dropped from the list
of questions.

## 11. Freeze record

- Frozen on: `[DATE — not yet frozen]`
- Commit: `[HASH]`
- Tag: `[analysis-plan-001-frozen — not yet created]`
- Deviations after freeze:
  - `(none)`
