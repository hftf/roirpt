# Declarative open phrasing engine

## Background

A stenographic phrasing system allows for systematically writing commonly-encountered phrases,
and especially ones that combine a starter (pronoun, optional relativizer),
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
The starter <kbd>KPWH</kbd> specifies the pronoun <samp>it</samp>;
the medial <kbd>A</kbd> specifies the modal <samp>can</samp>,
the medial <kbd>EU</kbd> specifies the perfect progressive aspect,
the medial <kbd>^</kbd> specifies subject–auxiliary inversion;
the ender <kbd>PZ</kbd> specifies the main verb <samp>happen</samp>
and paired with <kbd>T</kbd> specifies the extra word <samp>to</samp>,
and the ender <kbd>D</kbd> specifies past tense.
So altogether, pressing <kbd>^KPWHAEUPTDZ</kbd> gives the phrase <samp>could it have been happening to</samp>.

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
(key mappings are independent of conjugation data, for example)
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
and code that is basically self-documenting.

Admittedly, hardcoding as a strategy can make a reverse lookup algorithm easier to write,
and replacing hard-coded data with routines that generate the same data may add lines of code.
But I believe the readability and extensibility trade-off is worth it.

### Automated testing

Automated testing increases confidence in making changes and contributions
as you can instantly check whether changes introduce regressions.
Note that test cases and harnesses are not included when judging total lines of code.

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

Verb | Ender | Jeff’s | Explanation
-|-|-|-
|||| </tr><tr><td colspan="4" align="center"><kbd>-F</kbd> as F or V</td></tr></tbody><tbody><tr><td>
<samp>feel</samp>   | <kbd>FL</kbd>    | <kbd><del>LT</del></kbd>    | **F**ee**L**
<samp>find</samp>   | <kbd>FPB</kbd>   | <kbd><del>PBLG</del></kbd>  | **F**i**N**d
<samp>forget</samp> | <kbd>FRG</kbd>   | <kbd><del>RG</del></kbd>    | **F**o**RG**et
<samp>have</samp>   | <kbd>F</kbd>     | <kbd><del>T</del></kbd>     | ha**V**e</td></tr></tbody><tbody><tr><td colspan="4" align="center"><kbd>-FR</kbd> as M</td>
<samp>mean</samp>   | <kbd>FR</kbd>    | <kbd><del>PBL</del></kbd>   | **M**ean
<samp>mind</samp>   | <kbd>FRPB</kbd>  | <kbd><del>PBLS</del></kbd>  | **M**i**N**d</td></tr></tbody><tbody><tr><td colspan="4" align="center"><kbd>-F</kbd> as early fricative (S, H, CH, X)</td>
<samp>ask</samp>    | <kbd>FBG</kbd>   | <kbd><del>RB</del></kbd>    | a**SK**
<samp>set</samp>    | <kbd>FT</kbd>    | <kbd><del>BLS</del></kbd>   | **S**e**T**
<samp>seem</samp>   | <kbd>FPL</kbd>   | <kbd><del>PLS</del></kbd>   | **S**ee**M**
<samp>change</samp> | <kbd>FPG</kbd>   | <kbd><del>PBGZ</del></kbd>  | **CH**an**G**e
<samp>expect</samp> | <kbd>FPGT</kbd>  | <kbd><del>PGS</del></kbd>   | ek**SP**e**CT**
<samp>hope</samp>   | <kbd>FP</kbd>    | <kbd><del>RPS</del></kbd>   | **H**o**P**e
<samp>help</samp>   | <kbd>FPL</kbd>   | <kbd><del>PLGS</del></kbd>  | **H**e**L↶P**
<samp>leave</samp>  | <kbd>FLZ</kbd>   | <kbd><del>LGZ</del></kbd>   | **L**ea**↶V**e + <kbd>-Z</kbd></td></tr></tbody><tfoot><tr><td colspan="4" align="right">↶ = inversion</td>

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
(and duplicate asterisk keys provide no extra bits).
Accounting for the most necessary bits of information, we need all of them:

Feature | Number | Bits required
-|-|-
Subject     | 7–13 | 3–4 (but free only among 7 keys)
Modal       | 4+   | 2+
Aspect      | 4    | 2
Tense       | 2    | 1
Negation    | 2    | 1
Inversion   | 2    | 1
Contraction | 2    | 1
Verbs       | 64+  | 6+
Extra word  | 2    | 1</td></tr><tr><td colspan="2">Redundancy for<br>ergonomic pinky shapes</td><td>1</td></tr></tbody><tfoot><tr><th colspan="2">Total</th><th>20+ (but free only among 23 keys)

There are also 8+ relativizers (4+ bits),
but the bits from modal, aspect, and negation are cannibalized.

<!-- 
irrealis/subjunctive, defective
possible: gonna, gotta, 
maybe ^STKPWHRURD - being run
EU + /+-P -> having been run - passive present participle, perfect aspect
-->

### Better learning resources and terminology

In my opinion, phrasing resources suffer from two key issues: organization and terminology.

I find many existing resources confusingly organized and too shape-focused;
many infographic explainers [omit key labels](https://steno.sammdot.ca/aerick-phrasing.png)!
Learning resources should distinguish iconic from [arbitrary](https://discord.com/channels/136953735426473984/827241377020379186/1134593088287936602) chords.
It should also be possible to generate documentation and learning resources from code (code-as-data).

Phrasing resources often misuse of linguistic terminology
(e.g. “plural” to refer to the third-person singular inflection <samp>-s</samp>)
or are counterintuitive (e.g. “simple starter”).
Using mainstream linguistic terminology helps understand the reasons behind the system’s design.
The algorithm itself should be based on linguistic principles.
Something like do-support should really not need to be documented in a table,
since the use of do-support should already be intuitive to the user.

While tables of starters and enders are useful, tables of phrase structures but hard to remember.
Iconic and pictorial diagrams (not just infographics) would be most helpful for visual learners.

### Eventual convergence through divergence

Paradoxically, the ultimate end goal of this project
is not for each user to customize and tweak their phrasing system or design their own,
but, through it, once enough people have done so, to converge closer to a single ideal English phrasing system design.
People need to try diverse possibilities for us to collectively reach the best ideas.

## Phrasing system (default design)

The system is designed for the key layout below.
(The <kbd>^</kbd> and <kbd>+</kbd> keys require the
[`plover-stenotype-extended`](https://github.com/sammdot/plover-stenotype-extended) plugin.)

<table>
<tr><td>^</td><td>T</td><td>P</td><td>H</td><td>*</td><td>F</td><td>P</td><td>L</td><td>T</td><td>D</td></tr>
<tr><td>S</td><td>K</td><td>W</td><td>R</td><td>*</td><td>R</td><td>B</td><td>G</td><td>S</td><td>Z</td></tr>
<tr><td></td><td>#</td><td>A</td><td>O</td><td></td><td>E</td><td>U</td><td>+</td><td></td><td></td></tr>
</table>

Unless otherwise stated, assume that most design aspects are identical to Jeff phrasing.
At the moment, while documentation is incomplete, it may be more useful to read the code.
Look for dicts in files named `*_data.py`.

### Pictographic key layout

<table>
<thead><tr><th>Subject<br>(“full form”)</th><th>Relativizer + Subject<br>(“simple form”)</th></tr></thead>
<tbody valign="top" align="center"><tr><td><h2>

```
❓🚻🚻🚻⛔🆚🆚🆚🆙🔙
🚻🚻🚻🚻⛔🆚🆚🆚🆚🆚
　#️⃣Ⓜ️Ⓜ️　🏧⛎🗜　　
```
</h2>

Symbol | Keys | Usage (oversimplified)
-|-|-
<del>#️⃣</del> | <kbd><del>#</del></kbd> | <del>number key</del> (unused)
🚻 | <kbd>STKPWHR</kbd>  | subject pronoun
Ⓜ️ | <kbd>AO</kbd>       | modal
⛔ | <kbd>*</kbd>        | negation
🏧 | <kbd>E</kbd>        | perfect aspect (have)
⛎ | <kbd>U</kbd>        | progressive aspect (be)
🔙 | <kbd>D</kbd>        | tense
🗜 | <kbd>+</kbd>        | contraction
❓ | <kbd>^</kbd>        | inversion
🆚 | <kbd>FRPBLGSZ</kbd> | main verb
🆙 | <kbd>T</kbd>        | extra word
</td>
<td>

<h2>

```
❓🚾🚾🚾🚹🆚🆚🆚🆙🔙
🚾🚾🚾🚾🚹🆚🆚🆚🆚🆚
　#️⃣🚾🚾　🚹🚹🗜　　
```
</h2>

Symbol | Keys | Usage (oversimplified)
-|-|-
🚾 | <kbd>STKPWHRAO</kbd> | relativizer
🚹 | <kbd>*EU</kbd> | simple subject pronoun</td></tr><tr><td colspan="3" height="148" valign="center" align="center">Ⓜ️, ⛔, 🏧, ⛎ are invalid
</td></tr></table>

### Relativizer

Effectively an extra word prefixed before the subject.
Relativizers can be coordinators (e.g. <samp>and</samp>, <samp>but</samp>)
or subordinators (e.g. <samp>if</samp>, <samp>that</samp>, <samp>when</samp>, <samp>who</samp>).
A relativizer may also be called a conjunction, preposition, complementizer, or relative pronoun.

Overloads the keyspace used for both “full form” starters and modals,
so cannot be used with modals, aspect, or negation.
This may be why it is counterintuitively called “simple form” or “simple starters” in Jeff phrasing.

### Subject

Subjects specify the person (first, second, third) and number (singular, plural) of the phrase.

### Tense

Phrases can be in present or past tense.

Note that tense applies to the first verb in the clause, not the main verb.

### Aspect

English has two axes of aspect:
imperfect vs. perfect (<samp>have</samp>),
and simple vs. progressive (<samp>be</samp>).

### Modality (or mood)

The modality can be <samp>will</samp>, <samp>can</samp>, <samp>shall</samp>, or none.
The forms <samp>would</samp>, <samp>could</samp>, <samp>should</samp> are selected by past tense.
(Other modals in English include <samp>may</samp>, <samp>must</samp>, <samp>need to</samp>, etc.,
but these are not available as phrase-level modals, only as enders.)

Modals are defective verbs (so cannot inflect, except possibly for tense).

Note: the so-called “future tense” is treated here as a <samp>will</samp> modal, not a tense,
as seen in many English grammars.

### Subject–auxiliary question inversion

Subject–auxiliary inversion is the main feature of questions or interrogative phrases.
When an auxiliary is absent, there is do-support (a dummy <samp>do</samp> acts like an auxiliary).
Interrogatives are contrasted with declarative (or indicative) statements.

### Polarity

Phrases are positive (affirmative) or negative.
When an auxiliary is absent in a negative phrase, there is do-support.

Negation is only implemented for the matrix (main) clause,
and so it is governed by (attaches after) the first verb.
This means that <samp>he could not have gone</samp> is possible in the phrasing system,
while <samp>\*he could have not gone</samp> is not.

### Contraction

TODO/Self-explanatory.

Note: <samp>aren’t</samp> is the exceptional contracted form of <samp>am</samp> + <samp>not</samp>
(which only appears in interrogatives).

### Main verb (or other ender)

TODO/Self-explanatory.

Some defective verbs and non-verbs (common adverbs) are also available.

Note: main-verb <samp>have</samp> can take do-support, but this is rare in my dialect.

### Extra word

The extra word depends entirely on the main verb.
It tries to be the most frequent collocation or most useful otherwise.

Some examples of extra words:
<samp>a</samp>, <samp>it</samp>, <samp>to</samp>, <samp>the</samp>, <samp>that</samp>, <samp>like</samp>, <samp>on</samp>.

### Adverb

Not yet implemented.
Adverbs can include medial <samp>just</samp>, <samp>really</samp>, <samp>even</samp>, <samp>still</samp>, <samp>always</samp>, <samp>never</samp>, etc.
There is extra complexity because adverbs may exhibit free positioning.

### Passive voice

Passive voice effectively inserts <samp>be</samp> before the main verb
and selects the past participle form of the main verb.

A test implementation currently uses a retroactive second stroke <kbd>/+-P</kbd>
(i.e. press <kbd>+</kbd> and <kbd>P</kbd> after the first stroke).

## Learning and practice

Materials or curricula for specifically practicing a phrasing system do not really exist yet.
However, a drill on [Steno Jig](https://joshuagrams.github.io/steno-jig/) often gives
many sentences with high-frequency phrases:
[Markov-chain (randomly) generated sentences](https://joshuagrams.github.io/steno-jig/markov.html?word_count=100&seed=0.99831923480476&hints=1&show_timer=1).

Make use of the suggestions window and tapey-tape.

## Installation

TODO

## To-do list

### Short-term

* Write documentation
	* Write installation instructions
* Finish implementing reverse lookup
	* If multiple options, must yield all of them
	* As early as possible, must not yield any impossible options
* Mention <samp>have you got, did you get; got/gotten</samp>

### Long-term

* Create better resources
* Handle unwanted suffix keys
* Singular/plural distinction in relativizers
* Irrealis (so-called “past subjunctive”) with <samp>if</samp>
	* Could repurpose <samp>if</samp> + past tense
* Adverbs (<samp>just</samp>, <samp>really</samp>, <samp>even</samp>, <samp>still</samp>, <samp>always</samp>, <samp>never</samp>)
* Consider reprioritizing low-frequency combos to make fingerwork more convenient
(<samp>can have</samp>, <samp>shall have</samp> are less common than
<samp>could have</samp>, <samp>should have</samp>,
so maybe we can avoid needing to press <kbd>-D</kbd> to make <samp>could</samp>, <samp>should</samp>)

## About

* Started learning Jeff phrasing on September 25, 2023
* Started rewrite on September 26, 2023
* First published on October 13, 2023
