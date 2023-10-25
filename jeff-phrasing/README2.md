# Declarative open phrasing engine

## Background

A stenographic phrasing system allows for systematically writing commonly-encountered phrases,
and especially ones that combine a starter (subject pronoun, optional relativizer),
a medial (auxiliary, modal, negation, adverb, etc.),
and an ender (verb and tense).
For example, the phrase “<samp>who could it have been happening to</samp>” has
two starters (relativizer <samp>who</samp>, pronoun <samp>it</samp>),
four medials (modal <samp>can</samp>, perfect aspect <samp>have</samp>,
progressive/continuous aspect <samp>been</samp>, and subject–auxiliary inversion),
and three enders (main verb <samp>happen</samp>, extra word <samp>to</samp>,
and clause-level past tense turning <samp>can</samp> into <samp>could</samp>).

Phrasing systems encode meaning in key chords, and are primarily built around the few (10ish) available starter chords
that are unused by and therefore do not conflict with other dictionaries that the user requires.
Since the range of licit phrases is combinatorially complete,
stenographic phrasing systems are usually implemented as programmatic dictionaries
(written in Python, so requiring a [plugin](https://github.com/openstenoproject/plover_python_dictionary))
rather than static JSON dictionaries as the latter would be unnecessarily large (> 10 MB) and very hard to adjust.

The user presses a combination of keys to specify all the starters, medials, and enders,
and the phrasing system handles conjugation, word ordering, and so on.
For example,
the starter <kbd>KPWH</kbd> specifies the pronoun <samp>it</samp>;
the medial <kbd>A</kbd> specifies the modal <samp>can</samp>,
the medial <kbd>EU</kbd> specifies the perfect progressive aspect,
the medial <kbd>^</kbd> specifies subject–auxiliary inversion;
the ender <kbd>PZ</kbd> specifies the main verb <samp>happen</samp>
and paired with <kbd>T</kbd> specifies the extra word <samp>to</samp>,
and the ender <kbd>D</kbd> specifies past tense.
So altogether, pressing <kbd>^KPWHAEUPTDZ</kbd> gives the phrase <samp>could it have been happening to</samp>.
Since relativizers and modals are mutually exclusive (they share the same keyspace) –
that is, <samp>who</samp> cannot be used with <samp>can</samp> in the same phrase –
the earlier example requires two strokes: e.g. <kbd>WHO/^KPWHAEUPTDZ</kbd>.

Important precursors of this project include the phrasing systems of
[Aerick](https://github.com/aerickt/aerick-phrasing),
[Jade](https://github.com/Jade-GG/plover_phrasing),
[Jeff](https://github.com/jthlim/jeff-phrasing),
[Josiah](https://github.com/Josiah-tan/jeff-phrasing),
and other inspirations, and it began as a fork and rewrite of Jeff’s.
Further background and motivations are found in READMEs of precursor projects.

## Motivation

This is an **engine** for designing and customizing a stenographic phrasing system.
The distinction between a system and an engine lies mainly in the separation of concerns.
In a system, practically any code that gets the job done will do; 
an engine, however, is a backbone layer and allows for
tweaking individual modules that live apart in the source code
(for example, key mappings are independent of conjugation data,
which are decoupled from grammatical rules and the lookup algorithm),
with the expectation that changing one part won’t break anything else.

The distinction is not a concrete one, so it is really more about progress in relative terms,
such as refactoring 1,000 lines of code into more manageable, separate files –
a welcome novelty for Python dictionaries that get executed as <code>eval</code> jank.

## Improvements on other programmatic phrasing systems

At the time of writing, these are mainly goals for the project
rather than accurate representations of its current status.

### Replace large-scale hard-coding with automatic generation

A major goal is to minimize code and eliminate hard-coded data that are entirely predictable,
like conjugations and phrase structures.
Such repetitive programs are hard to check, change, and maintain,
and allow for typos to easily creep in.
This means far greater use of declarative programming, unbundling control flow,
passing state via objects, and code that is basically self-documenting.

Let's say you wanted to modify Jeff phrasing to remove contractions:
it requires editing strings in dozens of places, which is error-prone.
In contrast, you would only need to change one rule to do so in the engine.

Admittedly, hardcoding as a strategy can make a reverse lookup algorithm easier to write,
and replacing hard-coded data with routines that generate the same data may add lines of code.
But I believe the readability and extensibility trade-off is worth it.

### Automated testing

Automated testing increases confidence in making changes and contributions
as you can instantly check whether changes introduce regressions.
Test cases and harnesses are not included when judging total lines of code.

### Automatically handle conjugation, contraction, negation, and subject–auxiliary question inversion

While Jeff phrasing already achieves this goal,
it can still output ungrammatical forms, such as <kbd>TWRUPL</kbd> → `do we may`.

### Follow Pythonic conventions

Replace hyphens in filenames with underscores
and name variables more carefully to avoid clobbering built-ins like `dict`.
Tabular code is also space-aligned for readability.

### Centralize

Despite the ease of making a GitHub repository,
patches to phrasing systems have often been distributed as file uploads.
It should be easier to share modifications (and documentations of conflicts)
in the form of a separate “userspace” config file or even file footer,
rather than wholesale file replacements that are difficult to audit and interoperate,
if not just as forks.

---

### Reclaim the <kbd>-F</kbd> key for more iconic verb enders

Jeff phrasing uses <kbd>-F</kbd> for perfect aspect, a good choice due to its left position and
[iconicity](https://en.wikipedia.org/wiki/Iconicity) of the auxiliary verb “have.”

However, the lack of <kbd>-F</kbd> in ender space makes many enders unmemorable
and the task of learning the phrasing system far more about memorizing arbitrary shapes.
On top of training the hands on an entirely new ergonomics for phrasing,
learning over 75 enders and their possible extra words is more than memorization enough.

With <kbd>-F</kbd> as an ender key, many more enders are iconic of the way they sound
(e.g. <samp>feel</samp> = <kbd>-FL</kbd>).
This also opens up two more avenues to leverage:
<kbd>-F</kbd> as an early S (or fricative sound in general),
and <kbd>-FR</kbd> as another M (in many theories, <kbd>-FR</kbd> is already an early M,
particularly in the right-bank compounds MB and MP).
Some verb enders that benefit are:

<table>
<thead><tr><th>Verb</th><th>Ender</th><th>Jeff’s</th><th>Explanation</th></tr></thead>
<tbody><tr><th colspan="4"><kbd>-F</kbd> as F or V</th></tr>
<tr><td><samp>feel</samp>  </td><td><kbd>FL</kbd>   </td><td><kbd><del>LT</del></kbd>   </td><td><b>F</b>ee<b>L</b></td></tr>
<tr><td><samp>find</samp>  </td><td><kbd>FPB</kbd>  </td><td><kbd><del>PBLG</del></kbd> </td><td><b>F</b>i<b>N</b>d</td></tr>
<tr><td><samp>forget</samp></td><td><kbd>FRG</kbd>  </td><td><kbd><del>RG</del></kbd>   </td><td><b>F</b>o<b>RG</b>et</td></tr>
<tr><td><samp>have</samp>  </td><td><kbd>F</kbd>    </td><td><kbd><del>T</del></kbd>    </td><td>ha<b>V</b>e</td></tr>
</tbody>
<tbody><tr><th colspan="4"><kbd>-FR</kbd> as M</th></tr>
<tr><td><samp>mean</samp>  </td><td><kbd>FR</kbd>   </td><td><kbd><del>PBL</del></kbd>  </td><td><b>M</b>ean</td></tr>
<tr><td><samp>mind</samp>  </td><td><kbd>FRPB</kbd> </td><td><kbd><del>PBLS</del></kbd> </td><td><b>M</b>i<b>N</b>d</td></tr>
</tbody>
<tbody><tr><th colspan="4"><kbd>-F</kbd> as early fricative (S, H, CH, X)</th></tr>
<tr><td><samp>ask</samp>   </td><td><kbd>FBG</kbd>  </td><td><kbd><del>RB</del></kbd>   </td><td>a<b>SK</b></td></tr>
<tr><td><samp>set</samp>   </td><td><kbd>FS</kbd>   </td><td><kbd><del>BLS</del></kbd>  </td><td><b>S</b>et + <kbd>S</kbd></td></tr>
<tr><td><samp>change</samp></td><td><kbd>FPG</kbd>  </td><td><kbd><del>PBGZ</del></kbd> </td><td><b>CH</b>an<b>G</b>e</td></tr>
<tr><td><samp>expect</samp></td><td><kbd>FPGT</kbd> </td><td><kbd><del>PGS</del></kbd>  </td><td>e<b>XP</b>e<b>CT</b></td></tr>
<tr><td><samp>hope</samp>  </td><td><kbd>FP</kbd>   </td><td><kbd><del>RPS</del></kbd>  </td><td><b>H</b>o<b>P</b>e</td></tr>
<tr><td><samp>help</samp>  </td><td><kbd>FPL</kbd>  </td><td><kbd><del>PLGS</del></kbd> </td><td><b>H</b>e<b>L↶P</b></del></td></tr>
<tr><td><samp>leave</samp> </td><td><kbd>FLZ</kbd>  </td><td><kbd><del>LGZ</del></kbd>  </td><td><b>L</b>ea<b>↶V</b>e + <kbd>Z</kbd></td></tr></tbody>
<tfoot><tr><td colspan="4" align="right">↶ = inversion</td></tr></tfoot>
</table>

While this change may not make optimal use of keyboard space,
as there aren’t too many more enders to include,
the freed up room could potentially be used for extra words.

### Make right pinky shifting optional

In [Jeff phrasing](https://github.com/jthlim/jeff-phrasing/tree/main#verbs-and-suffix-words),
to avoid diagonal shapes <kbd>-TZ</kbd> and <kbd>-SD</kbd> on the right pinky keys,
verbs ending in <kbd>-S</kbd> always use <kbd>-SZ</kbd> (rather than <kbd>-SD</kbd>) for past tense,
and verbs ending in <kbd>-S</kbd> or <kbd>-Z</kbd> with extra word <kbd>-T</kbd> always use
<kbd>-TSDZ</kbd> for past tense.

These ergonomic exceptions are now optional (rather than mandatory)
to increase flexibility for users comfortable with shifting
and to prevent ungrammatical outputs (see the following section).

### Produce no ungrammatical output

The goal of the phrasing engine is not to produce any ungrammatical forms,
and to produce exactly all grammatical forms;
that is, it is [generative](https://en.wikipedia.org/wiki/Generative_grammar).
Stenography-system-level suffix keys (<kbd>-D</kbd>, <kbd>-G</kbd>, <kbd>-S</kbd>, <kbd>-Z</kbd>)
in the same stroke should be prevented from having an unwanted effect (see also above section).

### Reserve keys for single function (instead of overload with select adverbs)

We still have a need to write phrases in perfect and progressive aspects with question inversion.

### Use a retroactive second stroke for other features (adverbs, passive voice)

Some phrasing systems and extensions aspire to do too many things at once in a stroke:
control several adverbs, passive voice, suffixed object pronouns, and contractions.
Remember, a stenographic keyboard typically has only 23–28 keys
(and duplicate asterisk keys provide no extra bits),
all of which are needed after accounting for the most necessary bits of information:

Feature | Number | Bits required (log₂ N)
-|-|-
Subject     | 8–15 | 3–4 (but free only among 7 keys)
Modal       | 4+   | 2+
Aspect      | 4    | 2
Tense       | 2    | 1
Negation    | 2    | 1
Inversion   | 2    | 1
Contraction | 2    | 1
Verbs       | 64+  | 6+
Extra word  | 2    | 1</td></tr><tr><td colspan="2">Redundancy for<br>ergonomic pinky shapes</td><td>1</td></tr></tbody><tfoot><tr><th colspan="2">Total</th><th>20+ (but free only among 23 keys)

There are also 8+ relativizers (3+ bits),
but the bits from modal, aspect, and negation are cannibalized.

<!-- 
irrealis/subjunctive, defective
possible: gonna, gotta, 
maybe ^STKPWHRURD - being run
EU + /+-P -> having been run - passive present participle, perfect aspect
-->

### Better learning resources and terminology

In my opinion, phrasing resources suffer from two key issues, aside from practice materials:
organization and terminology.

I find many existing phrasing resources confusingly organized and too shape-focused;
many infographic explainers [omit key labels](https://steno.sammdot.ca/aerick-phrasing.png)!
Learning resources should distinguish iconic from [arbitrary](https://discord.com/channels/136953735426473984/827241377020379186/1134593088287936602) chords,
and prefer meaningful over alphabetical ordering.
It should also be possible to generate documentation and learning resources from code (code-as-data).

Phrasing resources often misuse linguistic terminology
(e.g. misuse “plural” to refer to the third-person *singular* inflection <samp>-s</samp>)
or are counterintuitive (e.g. “simple form”).
Using mainstream linguistic terminology helps understand the reasons behind the system’s design.
The algorithm itself should be based on linguistic principles.
Something like [do-support](https://en.wikipedia.org/wiki/Do-support) should really not need to be documented in a table,
since the use of do-support should already be intuitive to the user (do what I mean).
Similarly, contractions and irregular verb forms are implementation details and do not need full documentation.

While tables of starters and enders are useful, tables of phrase structures are hard to remember.
Iconic and pictorial diagrams (not just infographic – information spatially arranged into a graphic)
would be most helpful for visual learners.

### Eventual convergence through experimentation and divergence

Paradoxically, the ultimate end goal of this project
is not for each user to customize and tweak their phrasing system or design their own,
but, through it, once enough people have done so,
to converge closer to a single optimal English phrasing system design.
People need to try diverse possibilities for us to collectively reach the best ideas.

## Phrasing system (default design)

The system is designed for the key layout below.
(The <kbd>^</kbd> and <kbd>+</kbd> keys require the
[`plover-stenotype-extended`](https://github.com/sammdot/plover-stenotype-extended) plugin.)

<pre><code><table><tbody align="center">
<tr><td>^</td><td>T</td><td>P</td><td>H</td><td>*</td><td>F</td><td>P</td><td>L</td><td>T</td><td>D</td></tr>
<tr><td>S</td><td>K</td><td>W</td><td>R</td><td>*</td><td>R</td><td>B</td><td>G</td><td>S</td><td>Z</td></tr>
<tr><td></td><td>#</td><td>A</td><td>O</td><td></td><td>E</td><td>U</td><td>+</td><td></td><td></td></tr>
</tbody></table></code></pre>

Unless otherwise stated, assume that most design aspects are identical to Jeff phrasing.
At the moment, while documentation is incomplete, it may be more useful to read the code.
Look for dicts in files named `*_data.py`.

> [!WARNING]
> At this time, the key layout above is assumed,
> so chords may not have comfortable shapes for everyone.
> This will be made more customizable at some point.

### Pictographic key layout

There are two types of phrase:
phrases without a relativizer, and phrases with a relativizer.
In Jeff phrasing, these are called “full form” and “simple form” respectively.

Each region of the keyboard controls a different feature of the phrase.
These regions are mapped below.
Nuances are discussed in later sections.

<table>
<thead><tr><th>Subject<br>(“full form”)</th><th>Relativizer + Subject<br>(“simple form”)</th></tr></thead>
<tbody valign="top" align="center"><tr><td><h2><blockquote>

```
❓🚻🚻🚻⛔🆚🆚🆚🆙🔙
🚻🚻🚻🚻⛔🆚🆚🆚🆚🆚
　#️⃣Ⓜ️Ⓜ️　🏧⛎🗜　　
```
</blockquote></h2>

Symbol | Keys | Usage (oversimplified)
-|-|-
<del>#️⃣</del> | <kbd><del>#</del></kbd> | <del>number key</del> (unused)
🚻 | <kbd>STKPWHR</kbd>  | [subject pronoun](#subject-pronoun)
Ⓜ️ | <kbd>AO</kbd>       | [modal](#modality)
⛔ | <kbd>*</kbd>        | [negation](#polarity)
🏧 | <kbd>E</kbd>        | [perfect aspect](#aspect) (<samp>have</samp>)
⛎ | <kbd>U</kbd>        | [progressive aspect](#aspect) (<samp>be</samp>)
🔙 | <kbd>D</kbd>        | [tense](#tense)
🗜 | <kbd>+</kbd>        | [contraction](#contraction)
❓ | <kbd>^</kbd>        | [inversion](#subjectauxiliary-question-inversion)
🆚 | <kbd>FRPBLGSZ</kbd> | [main verb](#main-verb-or-other-ender)
🆙 | <kbd>T</kbd>        | [extra word](#extra-word)
</td>
<td>

<h2><blockquote>

```
❓🚾🚾🚾🚹🆚🆚🆚🆙🔙
🚾🚾🚾🚾🚹🆚🆚🆚🆚🆚
　#️⃣🚾🚾　🚹🚹🗜　　
```
</blockquote></h2>

<table>
<thead><tr><th>Symbol</th><th>Keys</th><th>Usage (oversimplified)</th></tr></thead>
<tbody valign="center">
<tr><td  align="center" colspan="3">Ⓜ️, ⛔, 🏧, ⛎ are invalid</td></tr>
<tr height="74"><td>🚾</td><td><kbd>STKPWHRAO</kbd></td><td><a href="#relativizer">relativizer</a></td></tr>
<tr height="111"><td>🚹</td><td><kbd>*EU</kbd></td><td><a href="#user-content-simple-subject">simple subject pronoun</a></td></tr>
<tr><td colspan="3" height="185" align="center">same</td></tr>
</tbody></table>
</tbody></table>

### Relativizer

For phrasing purposes, a relativizer is effectively an extra word prefixed before the subject.
Relativizers can be coordinators (e.g. <samp>and</samp>, <samp>but</samp>)
or subordinators (e.g. <samp>if</samp>, <samp>that</samp>, <samp>when</samp>, <samp>who</samp>).
A relativizer may also be called a conjunction, preposition, complementizer, or relative pronoun.
Relativizers are so named because they introduce a relative (or subordinate) clause –
also called a wh-clause as it often begins with a wh-word (what, who, which, when, where, why, how).

**Relativizers cannot be used with modality, aspect, or negation,**
as they overload the keyspace used by both “full form” subject pronouns and modals,
and are used in conjunction with a limited set of subject pronouns that overload aspect and negation.
This limitation may be why it is counterintuitively called “simple form” in Jeff phrasing,
despite adding an extra initial word.

<table>
<thead><tr><th colspan="2">Subordinators</th><th colspan="2">Coordinators</th></tr></thead>
<tbody>
<tr><td><kbd>STPA  </kbd></td><td><samp>if</samp>*†  </td><td><kbd>SPWH</kbd></td><td><samp>but</samp></td></tr>
<tr><td><kbd>STHA  </kbd></td><td><samp>that</samp>* </td><td><kbd>SKP </kbd></td><td><samp>and</samp></td></tr>
<tr><td><kbd>SWH   </kbd></td><td><samp>when</samp>† </td><td><kbd>SKPR</kbd></td><td><samp>or</samp></td></tr>
<tr><td><kbd>SWHR  </kbd></td><td><samp>where</samp>†</td><td colspan="2" rowspan="5"></td></tr>
<tr><td><kbd>SWHA  </kbd></td><td><samp>what</samp>  </td></tr>
<tr><td><kbd>SWHO  </kbd></td><td><samp>who</samp>   </td></tr>
<tr><td><kbd>SWHAO </kbd></td><td><samp>why</samp>†  </td></tr>
<tr><td><kbd>SWHRAO</kbd></td><td><samp>how</samp>   </td></tr>
</tbody><tfoot><tr><td colspan="2">* forbids inversion</td><td colspan="2">† requires subject</td></tr></tfoot></table>

### Subject pronoun

Subjects specify the person (first, second, third) and number (singular, plural) of the phrase.
These features surface as inflections on the tensed (finite) verb,
which is a phenomenon called subject–verb agreement (concord).

Two third-person null subjects exist in “full form”:
<kbd>STWR</kbd> (singular) and <kbd>STKPWHR</kbd> (plural).

<table>
<thead><tr><th><ins>Subjects</ins></th><th colspan="2">Singular</th><th colspan="2">Plural</th></tr></thead>
<tbody valign="top" align="left">
<tr><th>First  person</th><td><kbd>SWR</kbd></td><td><samp>I</samp></td><td><kbd>TWR </kbd></td><td><samp>we </samp></td></tr>
<tr><th>Second person</th><td><kbd>KPWR</kbd></td><td colspan="3"><samp>you</samp></td></tr>
<tr><th rowspan="7">Third person</th><td><kbd>KWHR</kbd></td><td><samp>he</samp></td><td rowspan="3"><kbd>TWH</kbd></td><td rowspan="3"><samp>they</samp></tr>
<tr><td><kbd>SKWHR</kbd></td><td><samp>she </samp></td></tr>
<tr><td><kbd>KPWH </kbd></td><td><samp>it  </samp></td></tr>
<tr><td><kbd>STKH</kbd></td><td><samp>this </samp></td><td><kbd>STKWH</kbd></td><td><samp>these</samp></td></tr>
<tr><td><kbd>STWH</kbd></td><td><samp>that </samp></td><td></td><td></td></tr>
<tr><td><kbd>STHR</kbd></td><td><samp>there</samp></td><td><kbd>STPHR</kbd></td><td><samp>there</samp>₂</td></tr>
<tr><td><kbd>STKPWHR</kbd></td><td>(null)</td><td><kbd>STWR</kbd></td><td>(null)₂</td></tr>
</tbody></table>

> [!NOTE]
> 💡 Memorization tip:
Both of the first-person subjects <samp>I</samp> <kbd>SWR</kbd> and <samp>we</samp> <kbd>TWR</kbd>
contain the keys <kbd>WR</kbd>.

<a name="simple-subject"></a>
Only eight subjects total exist in “simple form”:

<table>
<thead><tr><th><ins>Simple subjects</ins></th><th colspan="2">Singular</th><th colspan="2">Plural</th></tr></thead>
<tbody valign="top" align="left">
<tr><th>First  person</th><td><kbd>EU</kbd></td><td><samp>I</samp></td><td><kbd>*EU </kbd></td><td><samp>we </samp></td></tr>
<tr><th>Second person</th><td><kbd>U</kbd></td><td colspan="3"><samp>you</samp></td></tr>
<tr><th rowspan="7">Third person</th><td><kbd>E</kbd></td><td><samp>he</samp></td><td rowspan="3"><kbd>*U</kbd></td><td rowspan="3"><samp>they</samp></tr>
<tr><td><kbd>*E</kbd></td><td><samp>she </samp></td></tr>
<tr><td><kbd>* </kbd></td><td><samp>it  </samp></td></tr>
<tr><td><kbd> </kbd></td><td>(null)</td><td></td><td></td></tr>
</tbody></table>

### Tense

Phrases can be in present (non-past) or past tense.

> [!NOTE]
> Tense applies to the first verb in the clause, not the main verb.

|| Tense
-|-
<kbd> </kbd> | Present (non-past)
<kbd>D</kbd>      | Past

### Aspect

English has two axes of aspect:
imperfect vs. perfect (auxiliary <samp>have</samp>),
and simple vs. progressive (auxiliary <samp>be</samp>).

Perfect aspect generally indicates completed actions,
and progressive aspect indicates continuous actions.

<table>
<thead><tr><th><ins>Aspect</ins></th><th colspan="2">Imperfect</th><th colspan="2">Perfect</th></tr></thead>
<tbody valign="top" align="left">
<tr><th>Simple</th><td><kbd> </kbd></td><td>Simple</td><td><kbd>E</kbd></td><td>Perfect (<samp>have V·en</samp>)</td></tr>
<tr><th>Progressive</th><td><kbd>U</kbd></td><td>Progressive (<samp>be V·ing</samp>)</td><td><kbd>EU</kbd></td><td>Perfect progressive (<samp>have been V·ing</samp>)</td></tr>
</tbody></table>

### Modality

The modality (or mood) can be <samp>can</samp>, <samp>will</samp>, <samp>shall</samp>, or null.
The forms <samp>could</samp>, <samp>would</samp>, <samp>should</samp> are selected by past tense.
(Other modals in English include <samp>may</samp>/<samp>might</samp>, <samp>must</samp>,
<samp>need to</samp>, <samp>be able to</samp>, etc.,
but these are not available as phrase-level modals, only as ad-hoc enders.)

Modals are usually defective verbs (so can only be finite, inflecting for tense).

> [!NOTE]
> The so-called “future tense” is treated here as a <samp>will</samp> modal, not a tense,
which is consistent with the approach taken in many English grammars.

|| Modal
-|-
<kbd> </kbd>  | (null)
<kbd>A</kbd>  | <samp>can</samp>
<kbd>AO</kbd> | <samp>will</samp>
<kbd>O</kbd>  | <samp>shall</samp>

### Subject–auxiliary question inversion

Subject–auxiliary inversion is the main feature of questions or interrogative phrases.
When an auxiliary is absent, there is do-support (a dummy <samp>do</samp> acts like an auxiliary).
Interrogatives are contrasted with declarative (or indicative) statements.

|| Inversion
-|-
<kbd> </kbd> | Declarative (no inversion)
<kbd>^</kbd> | Subject–auxiliary inversion

### Polarity

Phrases are positive (affirmative) or negative.
When an auxiliary is absent in a negative phrase, there is do-support.

Negation is only implemented for the matrix (main) clause,
and so it is governed by (attaches after) the first verb.
This means that e.g. <samp>he could not have gone</samp> is possible in the phrasing system,
while <samp>\*he could have not gone</samp> is not.

A similar rule applies to negated infinitives:
<samp>not to go</samp> is possible, but <samp>\*to not go</samp> is not.

|| Polarity
-|-
<kbd> </kbd> | Positive
<kbd>*</kbd> | Negative

### Contraction

TODO/Self-explanatory.
Multiple contractions (e.g. <samp>couldn’t’ve</samp>) can technically be supported by the engine,
but no interface exists for applying them yet.

> [!NOTE]
> <samp>aren’t</samp> is the exceptional contracted form of <samp>am</samp> + <samp>not</samp>
(which only appears in interrogatives).

|| Contraction
-|-
<kbd> </kbd> | No contraction
<kbd>+</kbd> | Contraction

### Main verb (or other ender)

TODO/Self-explanatory.

Some defective verbs and non-verbs (common adverbs) are also available.

> [!NOTE]
> Main-verb <samp>have</samp> can rarely take do-support (e.g. <samp>have you no shame</samp>),
but this is archaic in most English dialects, so is not supported.

### Extra word

The extra word depends entirely on the main verb.
It tries to be the most frequent collocation or most useful otherwise.

Some examples of extra words:
<samp>a</samp>, <samp>it</samp>, <samp>to</samp>, <samp>the</samp>, <samp>that</samp>, <samp>like</samp>, <samp>on</samp>.

The verb enders are defined in [`verb_data.py:135`](./verb_data.py#L135).
The following table shows the defaults.

### Verb ender table

<table>
<thead><tr><th>Verb</th><th colspan="2">Extra word</th><th>Ender</th><th>Jeff’s</th><th>Explanation</th><th>Notes</th></tr></thead>
<tbody>
<tr><td width="1">(null)                 </td><td align="right" colspan="2">→ <var>talk</var> <kbd>T</kbd></td><td><kbd> </kbd></td><td>=</td><td></td><td></td></tr>
</tbody>
<tbody>
<tr><th align="left" colspan="7">Modal verbs (auxiliary verbs)</th></tr>
<tr><td colspan="2"><samp>can       </samp></td><td>                 </td><td rowspan="3">n/a  </td><td><kbd><del>BGS </del></kbd></td><td></td><td rowspan="3">unavailable but listed here for completion; only useful in “simple form”</td></tr>
<tr><td colspan="2"><samp>will      </samp></td><td>                 </td>                          <td><kbd><del>RBGS</del></kbd></td><td></td></tr>
<tr><td colspan="2"><samp>shall     </samp></td><td>                 </td>                          <td><kbd><del>RBL </del></kbd></td><td></td></tr>
<tr><td colspan="2"><samp>may       </samp></td><td><samp>be  </samp></td><td><kbd>PL</kbd>    </td><td>=                         </td><td><b>M</b>ay</td><td>past tense: <samp>might</samp></td></tr>
<tr><td colspan="2"><samp>must      </samp></td><td><samp>be  </samp></td><td><kbd>PBLGS</kbd> </td><td>=                         </td><td><b>M</b>u<b>S</b>t + just’s <b>J</b></td><td>defective (no past tense): taken by <samp>just</samp></td></tr>
</tbody>
<tbody>
<tr><th align="left" colspan="7">Adverbs (non-verbs)</th></tr>
<tr><td colspan="2"><samp>just      </samp></td><td>                 </td><td><kbd>PBLGSZ</kbd></td><td>=                         </td><td><b>J</b>u<b>SZ</b>t</td><td>listed after <samp>must</samp>: overrides its past tense</td></tr>
<tr><td colspan="2"><samp>really    </samp></td><td>                 </td><td><kbd>RLG</kbd>   </td><td>=                         </td><td><b>R</b>eal<b>LY</b><sup><var>LG (i.e. -liȝ)</var></sup></td><td></td></tr>
</tbody>
<tbody>
<tr><th align="left" colspan="7">Common verbs</th></tr>
<tr><td colspan="2"><samp>be        </samp></td><td><samp>a   </samp></td><td><kbd>B</kbd>     </td><td>=                         </td><td><b>B</b>e</td><td></td></tr>
<tr><td colspan="2"><samp>have      </samp></td><td><samp>to  </samp></td><td><kbd>F</kbd>     </td><td><kbd><del>T   </del></kbd></td><td>ha<b>V</b>e</td><td></td></tr>
<tr><td colspan="2"><samp>do        </samp></td><td><samp>it  </samp></td><td><kbd>RP</kbd>    </td><td>=                         </td><td>arb.†</td><td></td></tr>
<tr><td colspan="2"><samp>go        </samp></td><td><samp>to  </samp></td><td><kbd>G</kbd>     </td><td>=                         </td><td><b>G</b>o</td><td></td></tr>
<tr><td colspan="2"><samp>get       </samp></td><td><samp>to  </samp></td><td><kbd>GS</kbd>    </td><td>=                         </td><td><b>G</b>et + <kbd>S</kbd></td><td>past participle: <samp>got</samp>; passive voice: <samp>gotten</samp><br><samp>he had got to</samp> (obligation) available<br><samp>he had gotten</samp> (obtained) unavailable</td></tr>
<tr><td colspan="2"><samp>say       </samp></td><td><samp>that</samp></td><td><kbd>BS</kbd>    </td><td>=                         </td><td>from common <kbd>BS</kbd>*</td><td></td></tr>
<tr><td><samp>use       </samp></td><td align="right" colspan="2">→ <var>used to</var> <kbd>TZ</kbd><br></td><td><kbd>Z</kbd></td><td>=             </td><td>u<b>Z</b>e</td><td></td></tr>
<tr><td colspan="2"><samp>used to   </samp></td><td>                 </td><td><kbd>TZ</kbd>    </td><td>=                         </td><td>u<b>Z</b>ed <b>T</b>o</td><td>special case: really acts as <samp>use</samp> + <samp>to</samp> <kbd>T</kbd></td></tr>
</tbody>
<tbody>
<tr><th align="left" colspan="7">Verbs of cognition</th></tr>
<tr><td colspan="2"><samp>know      </samp></td><td><samp>that</samp></td><td><kbd>PB</kbd>    </td><td>=                         </td><td>k<b>N</b>ow</td><td></td></tr>
<tr><td colspan="2"><samp>think     </samp></td><td><samp>that</samp></td><td><kbd>PBG</kbd>   </td><td>=                         </td><td>thi<b>NG</b>k</td><td></td></tr>
<tr><td colspan="2"><samp>remember  </samp></td><td><samp>that</samp></td><td><kbd>RPL</kbd>   </td><td>=                         </td><td><b>R</b>e<b>M</b>ember</td><td></td></tr>
<tr><td colspan="2"><samp>understand</samp></td><td><samp>the </samp></td><td><kbd>RPB</kbd>   </td><td>=                         </td><td>unde<b>R</b>sta<b>N</b>d</td><td></td></tr>
<tr><td colspan="2"><samp>believe   </samp></td><td><samp>that</samp></td><td><kbd>BL</kbd>    </td><td>=                         </td><td><b>B</b>e<b>L</b>ieve</td><td></td></tr>
<tr><td colspan="2"><samp>imagine   </samp></td><td><samp>that</samp></td><td><kbd>PLG</kbd>   </td><td>=                         </td><td>i<b>M</b>a<b>G</b>ine</td><td></td></tr>
<tr><td colspan="2"><samp>forget    </samp></td><td><samp>to  </samp></td><td><kbd>FRG</kbd>   </td><td><kbd><del>RG  </del></kbd></td><td><b>F</b>o<b>RG</b>et</td><td></td></tr>
<tr><td colspan="2"><samp>mean      </samp></td><td><samp>to  </samp></td><td><kbd>FR</kbd>    </td><td><kbd><del>PBL </del></kbd></td><td><b>M</b><sup><var>FR</var></sup>ean</td><td></td></tr>
<tr><td colspan="2"><samp>learn     </samp></td><td><samp>to  </samp></td><td><kbd>RPBL</kbd>  </td><td><kbd><del>RPBS</del></kbd></td><td><b>L</b>ea<b>↶RN</b></td><td></td></tr>
<tr><td colspan="2"><samp>seem      </samp></td><td><samp>to  </samp></td><td><kbd>PLS</kbd>   </td><td>=                         </td><td><b>S</b>ee<b>↶M</b></td><td></td></tr>
<tr><td colspan="2"><samp>expect    </samp></td><td><samp>that</samp></td><td><kbd>FPGT</kbd>  </td><td><kbd><del>PGS </del></kbd></td><td>e<b>XP</b>e<b>C</b><sup><var>G</var></sup><b>T</b></td><td></td></tr>
<tr><td colspan="2"><samp>realize   </samp></td><td><samp>that</samp></td><td><kbd>RLZ</kbd>   </td><td><kbd><del>RLS </del></kbd></td><td><b>R</b>ea<b>L</b>i<b>Z</b>e</td><td></td></tr>
<tr><td colspan="2"><samp>mind      </samp></td><td>                 </td><td><kbd>FRPB</kbd>  </td><td><kbd><del>PBLS</del></kbd></td><td><b>M</b>i<b>N</b>d</td><td></td></tr>
<tr><td colspan="2"><samp>suppose   </samp></td><td><samp>that</samp></td><td><kbd>FPZ</kbd>   </td><td>🆕                        </td><td><b>S</b>u<b>PP</b>o<b>Z</b>e</td><td></td></tr>
</tbody>
<tbody>
<tr><th align="left" colspan="7">Verbs of desire</th></tr>
<tr><td colspan="2"><samp>want      </samp></td><td><samp>to  </samp></td><td><kbd>P</kbd>     </td><td>=                         </td><td>from common <kbd>PT</kbd>*</td><td></td></tr>
<tr><td colspan="2"><samp>wish      </samp></td><td><samp>to  </samp></td><td><kbd>RBS</kbd>   </td><td>=                         </td><td>wi<b>SH</b> + <kbd>S</kbd></td><td></td></tr>
<tr><td colspan="2"><samp>need      </samp></td><td><samp>to  </samp></td><td><kbd>PBL</kbd>   </td><td><kbd><del>RPG </del></kbd></td><td><b>N</b>eed + dental <kbd>L</kbd></td><td></td></tr>
<tr><td colspan="2"><samp>hope      </samp></td><td><samp>to  </samp></td><td><kbd>FP</kbd>    </td><td><kbd><del>RPS </del></kbd></td><td><b>H</b>o<b>P</b>e</td><td></td></tr>
<tr><td colspan="2"><samp>like      </samp></td><td><samp>to  </samp></td><td><kbd>LG</kbd>    </td><td><kbd><del>BLG </del></kbd></td><td><b>L</b>i<b>K</b><sup><var>G</var></sup>e</td><td></td></tr>
<tr><td colspan="2"><samp>love      </samp></td><td><samp>to  </samp></td><td><kbd>LGZ</kbd>   </td><td><kbd><del>LG  </del></kbd></td><td><b>L</b>o<b>V</b><sup><var>Z</var></sup>e + like’s <kbd>G</kbd></td><td></td></tr>
<tr><td colspan="2"><samp>care      </samp></td><td>                 </td><td><kbd>RG</kbd>    </td><td><kbd><del>RZ  </del></kbd></td><td><b>C</b><sup><var>G</var></sup>a<b>↶R</b>e</td><td></td></tr>
</tbody>
<tbody>
<tr><th align="left" colspan="7">More verbs</th></tr>
<tr><td colspan="2"><samp>become    </samp></td><td><samp>a   </samp></td><td><kbd>BGS</kbd>   </td><td><kbd><del>RPBG</del></kbd></td><td><b>B</b>e<b>K</b>ome + <kbd>S</kbd></td><td></td></tr>
<tr><td><samp>change    </samp></td><td align="right" colspan="2">→ <var>expect</var> <kbd>FPGT</kbd><br></td><td><kbd>FPG</kbd>   </td><td><kbd><del>PBGZ</del></kbd></td><td><b>CH</b>an<b>G</b>e</td><td></td></tr>
<tr><td colspan="2"><samp>consider  </samp></td><td>                 </td><td><kbd>RBGS</kbd>  </td><td><kbd><del>RBGZ</del></kbd></td><td><b>K</b>on<b>S</b>ide↶<b>R</b></td><td></td></tr>
<tr><td colspan="2"><samp>find      </samp></td><td><samp>that</samp></td><td><kbd>FPB</kbd>   </td><td><kbd><del>PBLG</del></kbd></td><td><b>F</b>i<b>N</b>d</td><td></td></tr>
<tr><td colspan="2"><samp>happen    </samp></td><td><samp>to  </samp></td><td><kbd>PZ</kbd>    </td><td>=                         </td><td>ha<b>PP</b>en + <kbd>Z</kbd></td><td></td></tr>
<tr><td colspan="2"><samp>try       </samp></td><td><samp>to  </samp></td><td><kbd>RT</kbd>    </td><td>=                         </td><td><b>T↶R</b>y</td><td></td></tr>
<tr><td colspan="2"><samp>make      </samp></td><td><samp>a   </samp></td><td><kbd>PBLG</kbd>  </td><td><kbd><del>RPBL</del></kbd></td><td><b>M</b>a<b>K</b>e</td><td></td></tr>
<tr><td colspan="2"><samp>work      </samp></td><td><samp>on  </samp></td><td><kbd>RBG</kbd>   </td><td>=                         </td><td>wo<b>RK</b></td><td></td></tr>
<tr><td colspan="2"><samp>play      </samp></td><td><samp>with</samp></td><td><kbd>PLGS</kbd>  </td><td>🆕                        </td><td><b>PL</b>a<b>Y</b><sup><var>G</var></sup> + <kbd>S</kbd></td><td></td></tr>
<tr><td colspan="2"><samp>start     </samp></td><td><samp>to  </samp></td><td><kbd>FRS</kbd>   </td><td>🆕                        </td><td><b>S</b><sup><var>F</var></sup>ta<b>R</b>t + <kbd>S</kbd></td><td></td></tr>
<tr><td colspan="2"><samp>choose    </samp></td><td><samp>to  </samp></td><td><kbd>FPS</kbd>   </td><td>🆕                        </td><td><b>CH</b>oo<b>S</b>e</td><td></td></tr>
</tbody>
<tbody>
<tr><th align="left" colspan="7">Verbs of placement</th></tr>
<tr><td colspan="2"><samp>put       </samp></td><td><samp>it  </samp></td><td><kbd>PS</kbd>    </td><td>=                         </td><td><b>P</b>ut + <kbd>S</kbd></td><td></td></tr>
<tr><td colspan="2"><samp>set       </samp></td><td>                 </td><td><kbd>FS</kbd>    </td><td><kbd><del>BLS </del></kbd></td><td><b>S</b>et + <kbd>S</kbd></td><td></td></tr>
<tr><td colspan="2"><samp>let       </samp></td><td>                 </td><td><kbd>LS</kbd>    </td><td>=                         </td><td><b>L</b>et + <kbd>S</kbd></td><td></td></tr>
<tr><td colspan="2"><samp>give      </samp></td><td>                 </td><td><kbd>GZ</kbd>    </td><td>=                         </td><td><b>G</b>i<b>V</b><sup><var>Z</var></sup>e</td><td></td></tr>
<tr><td colspan="2"><samp>take      </samp></td><td>                 </td><td><kbd>RBT</kbd>   </td><td>=                         </td><td>arb.†</td><td></td></tr>
<tr><td colspan="2"><samp>keep      </samp></td><td>                 </td><td><kbd>PG</kbd>    </td><td>=                         </td><td><b>K</b><sup><var>G</var></sup>ee<b>↶P</b></td><td></td></tr>
<tr><td colspan="2"><samp>bring     </samp></td><td>                 </td><td><kbd>RPBG</kbd>  </td><td>=                         </td><td><b>B↶R</b>i<b>NG</b></td><td></td></tr>
<tr><td colspan="2"><samp>provide   </samp></td><td>                 </td><td><kbd>RPZ</kbd>   </td><td>=                         </td><td><b>P↶R</b>o<b>V</b><sup><var>Z</var></sup>ide</td><td></td></tr>
</tbody>
<tbody>
<tr><th align="left" colspan="7">Verbs of action, communication</th></tr>
<tr><td colspan="2"><samp>come      </samp></td><td><samp>to  </samp></td><td><kbd>BG</kbd>    </td><td>=                         </td><td><b>K</b>ome</td><td></td></tr>
<tr><td colspan="2"><samp>live      </samp></td><td>                 </td><td><kbd>LZ</kbd>    </td><td>=                         </td><td><b>L</b>i<b>V</b><sup><var>Z</var></sup>e</td><td></td></tr>
<tr><td colspan="2"><samp>move      </samp></td><td>                 </td><td><kbd>PLZ</kbd>   </td><td>=                         </td><td><b>M</b>o<b>V</b><sup><var>Z</var></sup>e</td><td></td></tr>
<tr><td colspan="2"><samp>leave     </samp></td><td>                 </td><td><kbd>FLZ</kbd>   </td><td><kbd><del>LGZ </del></kbd></td><td><b>L</b>ea<b>↶V<sup><var>Z</var></sup></b>e</td><td></td></tr>
<tr><td colspan="2"><samp>remain    </samp></td><td>                 </td><td><kbd>RPLS</kbd>  </td><td>=                         </td><td><b>R</b>e<b>M</b>ain + <kbd>S</kbd></td><td></td></tr>
<tr><td colspan="2"><samp>call      </samp></td><td>                 </td><td><kbd>BLG</kbd>   </td><td><kbd><del>RBLG</del></kbd></td><td><b>K</b>a<b>LL</b></td><td></td></tr>
<tr><td colspan="2"><samp>recall    </samp></td><td>                 </td><td><kbd>RL</kbd>    </td><td>=                         </td><td><b>R</b>eca<b>LL</b></td><td></td></tr>
<tr><td colspan="2"><samp>read      </samp></td><td>                 </td><td><kbd>RS</kbd>    </td><td>=                         </td><td><b>R</b>ead + <kbd>S</kbd></td><td></td></tr>
<tr><td><samp>run       </samp></td><td align="right" colspan="2">→ <var>try</var> <kbd>RT</kbd><br></td><td><kbd>R</kbd>     </td><td>=                         </td><td><b>R</b>un</td><td></td></tr>
<tr><td colspan="2"><samp>show      </samp></td><td>                 </td><td><kbd>RB</kbd>    </td><td><kbd><del>RBZ </del></kbd></td><td><b>SH</b>ow</td><td></td></tr>
<tr><td colspan="2"><samp>ask       </samp></td><td>                 </td><td><kbd>FBG</kbd>   </td><td><kbd><del>RB  </del></kbd></td><td>a<b>SK</b></td><td></td></tr>
<tr><td colspan="2"><samp>tell      </samp></td><td>                 </td><td><kbd>LT</kbd>    </td><td><kbd><del>RLT </del></kbd></td><td><b>T</b>e<b>↶LL</b></td><td></td></tr>
<tr><td colspan="2"><samp>talk      </samp></td><td><samp>to  </samp></td><td><kbd>T</kbd>     </td><td>🆕                        </td><td><b>T</b>alk</td><td></td></tr>
<tr><td colspan="2"><samp>help      </samp></td><td>                 </td><td><kbd>FPL</kbd>   </td><td>🆕                        </td><td><b>H</b>e<b>L↶P</b></td><td></td></tr>
</tbody>
<tbody>
<tr><th align="left" colspan="7">Verbs of perception</th></tr>
<tr><td colspan="2"><samp>feel      </samp></td><td><samp>like</samp></td><td><kbd>FL</kbd>    </td><td><kbd><del>LT  </del></kbd></td><td><b>F</b>ee<b>L</b></td><td></td></tr>
<tr><td colspan="2"><samp>hear      </samp></td><td><samp>that</samp></td><td><kbd>FRP</kbd>   </td><td>=                         </td><td><b>H</b>ea<b>R</b> + <kbd>P</kbd></td><td></td></tr>
<tr><td><samp>see       </samp></td><td align="right" colspan="2">→ <var>talk to</var> <kbd>TS</kbd><br></td><td><kbd>S</kbd>     </td><td>=                         </td><td><b>S</b>ee</td><td></td></tr>
<tr><td><samp>look      </samp></td><td align="right" colspan="2">→ <var>tell</var> <kbd>LT</kbd><br></td><td><kbd>L</kbd>     </td><td>=                         </td><td><b>L</b>ook</td><td></td></tr>
<tr><td colspan="2"><samp>notice    </samp></td><td><samp>that</samp></td><td><kbd>PBS</kbd>   </td><td>🆕                        </td><td><b>N</b>oti<b>S</b>e</td><td></td></tr>
<tr><td colspan="2"><samp>recognize </samp></td><td><samp>that</samp></td><td><kbd>RGZ</kbd>   </td><td>🆕                        </td><td><b>R</b>eco<b>G</b>ni<b>Z</b>e</td><td></td></tr>
</tbody>
<tfoot>
<tr><th rowspan="3">Key</th><td colspan="3">† arbitrarily assigned chord</td><td>= same</td><td>↶ inversion</td><td><b>X</b><sup><var>Y</var></sup>: <kbd>Y</kbd> key represents variant of X sound</td></tr>
<tr/>
<tr><td colspan="4">→ <var>no extra word due to other ender</var></td><td colspan="2">* right-bank abbreviation already widely used in stenography</td></tr>
</tfoot>
</table>

### Infinitive

The infinitive (or non-finite) form is selected by a null subject with inversion (<kbd>^</kbd>).
This makes sense as there cannot be inversion without a subject.
Verbs have only one infinitive form, which follows <samp>to</samp>,
thus <kbd>STWR</kbd> and <kbd>STKPWHR</kbd> neutralize (behave identically) in this context.
<!-- however it could probably be used to invert to/not -->

> [!NOTE]
> Defective verbs (modals and non-verbs) do not have an infinitive form.

### Passive voice

Passive voice effectively inserts auxiliary <samp>be</samp> before the main verb
and selects the past participle form of the main verb.

A test implementation currently uses a retroactive second stroke <kbd>+-P</kbd>
(i.e. press <kbd>+</kbd> and <kbd>P</kbd> after the first stroke).

### Adverb

Not yet implemented.
Adverbs can include medial <samp>just</samp>, <samp>really</samp>, <samp>even</samp>, <samp>still</samp>, <samp>always</samp>, <samp>never</samp>, etc.
There is extra complexity because adverbs may exhibit free positioning.

### Fallback second stroke for conflicts

If a higher-priority dictionary overrides the phrasing system,
then adding the second stroke <kbd>+</kbd> is available as a fallback.
For example, <kbd>SKP-LD</kbd> is defined as <samp>and would</samp> in `main.json`,
so <kbd>SKP-LD</kbd> would not available for phrasing <samp>and looked</samp>,
but <kbd>SKP-LD/+</kbd> is available as a fallback for <samp>and looked</samp>.

### Summary of differences with other phrasing systems

<table>
<thead><tr><th>Feature</th><th width="88">Jeff</th><th width="88">Josiah</th><th>Default</th></tr></thead>
<tbody align="left">
<tr><td>Perfect     aspect (<samp>have</samp>)</td><td colspan="2"><kbd>F</kbd></td><td><kbd>E</kbd></td></tr>
<tr><td>Progressive aspect (<samp>be</samp>)  </td><td colspan="2"><kbd>E</kbd></td><td><kbd>U</kbd></td></tr>
<tr><td>Subject–auxiliary inversion</td><td colspan="2"><kbd>U</kbd></td><td><kbd>^</kbd></td></tr>
<tr><td>Past tense of ender containing <kbd>-S</kbd></td><td colspan="2"><kbd>-SZ</kbd></td><td>Both <kbd>-SZ</kbd> or <kbd>-SD</kbd></td></tr>
<tr><td>Contraction       </td><td colspan="2">Hard-coded only</td><td>Controlled by <kbd>+</kbd></td></tr>
<tr><td>Passive voice     </td><td colspan="2">Not implemented</td><td>Second stroke <kbd>+-P</kbd></td></tr>
<tr><td>Adverbs (<samp>just</samp>, <samp>even</samp>, <samp>still</samp>, <samp>always</samp>, <samp>never</samp>)</td><td colspan="2">Overloaded <kbd>*EUF</kbd></td><td>Not implemented</td></tr>
<tr><td>Reverse lookup    </td><td colspan="2">Ready</td><td>Partly implemented </td></tr>
<tr><td>Chord assignments</td><td colspan="3" align="center">May differ variously</td></tr>
<tr><td>Chord assignments: verb enders</td><td colspan="2">Cannot use <kbd>F</kbd></td><td>Can use <kbd>F</kbd></td></tr>
<tr><td>“Simple form” subject keys</td><td><kbd>*EU</kbd></td><td><kbd>^EU</kbd></td><td><kbd>*EU</kbd></td></tr>
<tr><td>“Simple form” negation    </td><td>n/a    </td><td><kbd>*</kbd>  </td><td>n/a</td></tr>
<tr><td>“Simple form” inversion   </td><td>n/a    </td><td>n/a   </td><td><kbd>^</kbd></td></tr>
<tr><td>“Simple form” allows empty subject</td><td>no    </td><td>yes   </td><td>yes</td></tr>
</tbody></table>

## Learning and practice

Materials or curricula for specifically practicing a phrasing system do not really exist yet.
However, a drill on [Steno Jig](https://joshuagrams.github.io/steno-jig/) often gives
many sentences with high-frequency phrases:
[Markov-chain (randomly) generated sentences](https://joshuagrams.github.io/steno-jig/markov.html?word_count=100&seed=0.99831923480476&hints=1&show_timer=1).

The phrasing system should be relatively straightforward to pick up;
just read this documentation, then start using it.
It is recommended to make liberal use of the suggestions window
and [tapey-tape](https://github.com/rabbitgrowth/plover-tapey-tape).

### How to learn a phrasing system

1. Read/skim the documentation once. (20 minutes)
2. Go back over the documentation and pick out some of the examples.
Break up the outlines into their constituent parts to confirm you understand them. (20 minutes)
3. Read/skim the code once. (optional)
4. Come up with some pictographics or mnemonics, or create a cheat sheet,
to arrange some of what you learned from the above in your head. (20 minutes)
5. Write some text while consulting any of Plover’s lookup panels and stroke-saving suggestions in `tapey_tape.txt`.
6. Practice on the Steno Jig drill linked above.
7. Repeat any of the above steps as desired.
<!-- Brush up on linguistic concepts and terminology if needed;
	the internet abounds with resources for this -->

You can probably get acquainted with a phrasing system to a basic level in as little as one day this way.

## Installation

At this time, the project is still in very early development
and is not quite ready to work out of the box.
However, you are welcome to try it if you can get it to work.

1. Ensure all dependencies are installed:
`plover_python_dictionary`, `plover-stenotype-extended`, `appdirs`.
2. Clone or download this folder (currently called `jeff-phrasing`)
and put it as a subdirectory inside `plover`.
3. Open Plover and add `jeff-phrasing/my_phrasing.py` as a dictionary.
(The other `.py` files need to be in the same folder as `my_phrasing.py`,
but do not add them to Plover as they are not dictionaries themselves.)

### Troubleshooting

If the module resolution at the top of `my_phrasing.py` is not working
(errors like `No module named 'noun_data'` appear),

https://github.com/hftf/roirpt/blob/38adfd827fed6e5df50f9a9580334401c865a948/jeff-phrasing/my_phrasing.py#L1-L10

then, for now, you can try to replace it with a hard-coded path:

```diff
-try:
-	import plover
-	plover_dir = plover.oslayer.config.CONFIG_DIR
-except:
-	import appdirs
-	plover_dir = appdirs.user_data_dir('plover', 'plover')
+plover_dir = '/home/path/to/my/plover/appdir'
```

## To-do list

### Short-term

* Write installation instructions
	* Mention dictionary priority
* Write testing instructions
* Consider dropping the terms starter/medial/ender entirely
	* For “chord”?
* Consider grouping verbs by arbitrary added key (e.g. <kbd>S</kbd>, <kbd>Z</kbd>)
* Add some Josiah extensions
* Add examples in readme

### Long-term

* Create better resources
	* Video lessons? Interactive lessons?
* Handle unwanted suffix keys
* Fix conflicts with my dictionaries
* Singular/plural distinction in relativizers
* Irrealis (so-called “past subjunctive”) with <samp>if</samp>
	* Could repurpose <samp>if</samp> + past tense
* Adverb medials (<samp>just</samp>, <samp>really</samp>, <samp>even</samp>, <samp>still</samp>, <samp>always</samp>, <samp>never</samp>)
* Consider reprioritizing low-frequency combos to make fingerwork more convenient
(<samp>can have</samp>, <samp>shall have</samp> are less common than
<samp>could have</samp>, <samp>should have</samp>,
so maybe we can avoid needing to press <kbd>-D</kbd> to make <samp>could</samp>, <samp>should</samp>)

## About

* Started learning Jeff phrasing on September 25, 2023
* Started rewrite on September 26, 2023
* First published on October 13, 2023
