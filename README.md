# roirpt

I basically just git initted in my plover dir and started committing WIPs

This README is better viewed [in full width](https://github.com/hftf/roirpt/blob/master/README.md) (> 1100 pixels)

## Contents

### `caret-*.json`

Introduces <kbd>^</kbd> to represent a pre-initial schwa.
Requires the [`plover-stenotype-extended`](https://github.com/sammdot/plover-stenotype-extended) plugin.

A few groups of rhymes so you can see why this might be useful:

Group | Word | Steno | Pseudosteno | Plover default entries
-|-|-|-|-
-end | <samp>pend</samp>   | <kbd>PEPBD</kbd>    | `(PEND)`   | <kbd>PEPBD</kbd>
|| <samp>spend</samp>      | <kbd>SPEPBD</kbd>   | `(SPEND)`  | <kbd>SPEPBD</kbd>
|| <samp>append</samp>     | <kbd>^PEPBD</kbd>   | `(^PEND)`  | <kbd>A(P)/PEPBD</kbd>
|| <samp>expend</samp>     | <kbd>KPEPBD</kbd>   | `(XEND)`   | <kbd>KPEPBD</kbd> or <kbd>EBGS/PEPBD</kbd>
|| <samp>extend</samp>     | <kbd>^STEPBD</kbd>  | `(^STEND)` | <kbd>EBGS/(S)TEPBD</kbd>
-ent | <samp>sent</samp>   | <kbd>SEPBT</kbd>    | `(SENT)`   | <kbd>SEPBT</kbd>
|| <samp>assent</samp>     | <kbd>^SEPBT</kbd>   | `(^SENT)`  | <kbd>AS/SEPBT</kbd>
|| <samp>ascent</samp>     | <kbd>^SKREPBT</kbd> | `(^SCENT)` | <kbd>AS/KREPBT</kbd>
|| <samp>accent</samp>     | <kbd>^KPEPBT</kbd>  | `(^XENT)`  | <kbd>ABG/SENT</kbd> or <kbd>ABGS/EPBT</kbd> or <kbd>KP\*EPBT</kbd>
|| <samp>stent</samp>      | <kbd>STEPBT</kbd>   | `(STENT)`  | <kbd>STEPBT</kbd>
|| <samp>extent</samp>     | <kbd>^STEPBT</kbd>  | `(^STENT)` | <kbd>EBGS/((S)T)EPBT</kbd>
|| <samp>competent</samp>  | <kbd>KPEPBT</kbd>   | `(KPENT)`  | <kbd>KPEPBT</kbd> or <kbd>KPE/TEPBT</kbd> or <kbd>KOFRP/TEPBT</kbd> etc.
|| <samp>scent</samp>      | <kbd>SKEPBT</kbd> or<br><kbd>SKREPBT</kbd> | `(SKENT)` or<br>`(SCENT)` | <kbd>SKEPBT</kbd> or<br><kbd>SKREPBT</kbd>
|| <samp>consent</samp>    | <kbd>SK\*EPBT</kbd> | `(SK*ENT)` | <kbd>SK\*EPBT</kbd> or <kbd>KAUPB/SEPBT</kbd> etc.
-ent | <samp>intent</samp> | <kbd>SPWEPBT</kbd>  | `(INTENT)` | <kbd>SPWEPBT</kbd> or <kbd>EUPB/TEPBT</kbd>
|| <samp>absent</samp>     | <kbd>^SPWEPBT</kbd> | `(^SBENT)` | <kbd>AB/SEPBT</kbd>

#### The <samp>ex-</samp>/<samp>comp-</samp> conflict, etc.

These dictionaries do not claim to solve the <samp>ex-</samp>/<samp>comp-</samp> conflict systematically or completely,
but represent the general direction I was going for.
In the case of a conflict, usually the leftmost option or the more common word gets priority.

no prefix | prefixed with <kbd>S</kbd> | prefixed with <kbd>^</kbd> | prefixed with <kbd>^S</kbd>
-|-|-|-
<kbd>T </kbd> <samp>t-</samp> | <kbd>ST </kbd>  <samp>st-</samp>  | <kbd>^T </kbd>  <samp>att-</samp>  | <kbd>^ST </kbd>  <samp>est-</samp>¹ or <samp>ext-</samp>
<kbd>P </kbd> <samp>p-</samp> | <kbd>SP </kbd>  <samp>sp-</samp>  | <kbd>^P </kbd>  <samp>app-</samp>  | <kbd>^SP </kbd>  <samp>esp-</samp>  or <samp>exp-</samp>
<kbd>K </kbd> <samp>c-</samp> | <kbd>SK </kbd>  <samp>sc-</samp>  | <kbd>^K </kbd>  <samp>acc-</samp>  | <kbd>^SK </kbd>  <samp>esc-</samp>  or <samp>exc-</samp>
<kbd>KP</kbd> <samp>comp-</samp> or <samp>ex-</samp> | <kbd>SKP</kbd> <samp>and-</samp> | <kbd>^KP</kbd> <samp>ex-</samp> or <samp>exC-</samp>² | <kbd>^SKP</kbd>           

Note that this table is designed to be mnemonic, not comprehensive. For example:
1. <kbd>^ST</kbd>: “<samp>est-</samp>” is shorthand for “<samp>ast-</samp>, <samp>aust-</samp>, <samp>est-</samp>, <samp>ist-</samp>, etc.”
(as in <samp><b>ast</b>ute</samp>, <samp><b>aust</b>ere</samp>, <samp><b>est</b>ate</samp>, <samp><b>Ist</b>anbul</samp>)
2. <kbd>^KP</kbd>: is <samp>ext-</samp> or <samp>exp-</samp> or <samp>exc-</samp> when used with <kbd>R</kbd> (as in <samp><b>ext</b>ra</samp> <kbd>^KPRA</kbd>, <samp><b>exp</b>ress</samp> <kbd>^KPRES</kbd>)

#### Compound initial sounds

In development (not really). Looking for permanent homes for certain starters (marked with ? for now).

For certain other combinations (stop, fricative + stop, stop + fricative, stop + fricative + stop),
see the table under [the <samp>ex-</samp>/<samp>comp-</samp> conflict](#the-ex-comp--conflict-etc).

Type | Starter | Steno | Pseudo | Starter | Steno | Pseudo
-|-|-|-|-|-|-
||||||| </tr><tr><td></td><td colspan="3" align="center">**no prefix**</td><td colspan="3" align="center">**with K-**</td></tr></tbody><tbody><tr><td colspan="7">**Nasal + nasal**
MM | <samp>amm-</samp> <samp>emm-</samp> <samp>imm-</samp> | <kbd>^PH</kbd>  | `(^M)`  | <samp>comm-</samp> | <kbd>KPH</kbd>  | `(KM)`
NN | <samp>ann-</samp> <samp>enn-</samp> <samp>inn-</samp> | <kbd>^TPH</kbd> | `(^N)`  | <samp>conn-</samp> | <kbd>K</kbd>    | `(K)`</td></tr></tbody><tbody><tr><td colspan="7">**Nasal + stop**
MP | <samp>amp-</samp> <samp>emp-</samp> <samp>imp-</samp> | <kbd>KPW</kbd>  | `(IMP)` | <samp>comp-</samp> | <kbd>KP</kbd>   | `(KP)`
MB | <samp>amb-</samp> <samp>emb-</samp> <samp>imb-</samp> | <kbd>KPW</kbd>  | `(IMP)` | <samp>comb-</samp> | <kbd>KPW</kbd>  | `(KB)`
NT | <samp>ant-</samp> <samp>ent-</samp> <samp>int-</samp> | <kbd>SPW</kbd>  | `(INT)` | <samp>cont-</samp> | <kbd>K</kbd>    | `(K)`
ND | <samp>and-</samp> <samp>end-</samp> <samp>ind-</samp> | <kbd>SKP</kbd>  | `(AND)` | <samp>cond-</samp> | <kbd>K</kbd>    | `(K)`
NK | <samp>anc-</samp> <samp>enc-</samp> <samp>inc-</samp><br /><samp>ank-</samp> <samp>enk-</samp> <samp>ink-</samp> | ? | | <samp>conc-</samp><br /><samp>conk-</samp> | <kbd>K</kbd> | `(K)`
NG | <samp>ang-</samp> <samp>eng-</samp> <samp>ing-</samp> | ?                            |        | <samp>cong-</samp> | <kbd>K</kbd> | `(K)`</td></tr></tbody><tbody><tr><td colspan="7">**Nasal + fricative**
NF | <samp>    </samp> <samp>enf-</samp> <samp>inf-</samp> | ?                            |        | <samp>comf-</samp><br /><samp>conf-</samp> | <kbd>TKP</kbd> or<br /><nobr><kbd>TKP*</kbd>¹</nobr> | `(KF)` or<br /><nobr>`(KF*)`¹</nobr>
NV | <samp>    </samp> <samp>env-</samp> <samp>inv-</samp> | <kbd>TPWH</kbd>              | `(NW)` | <samp>conv-</samp> | <kbd>KW</kbd> | `(KW)`
NS | <samp>ans-</samp> <samp>ens-</samp> <samp>ins-</samp><br /><samp>anc-</samp> <samp>enc-</samp> <samp>inc-</samp> | <kbd>STPH</kbd>              | `(SN)` | <samp>cons-</samp><br /><samp>conc-</samp> | <kbd>SK</kbd> | `(SK)`</td></tr></tbody><tbody><tr><td colspan="7">**Nasal + fricative + stop**
NST| <samp>    </samp><samp>    </samp> <samp>inst-</samp>| <kbd>STPH</kbd>    | `(SN)` | <samp>const-</samp> | ? |</td></tr></tbody><tbody><tr><td colspan="7">**Nasal + affricate**
NJ | <samp>ang-</samp> <samp>eng-</samp> <samp>ing-</samp><br /><samp>    </samp> <samp>enj-</samp> <samp>inj-</samp> | ? | | <samp>cong-</samp><br /><samp>conj-</samp> | ? | </td></tr></tbody><tbody><tr><td colspan="7">**Stop + fricative**
BS | <samp>abs-</samp> <samp>obs-</samp>                   | <kbd>SPW</kbd> or<br /><kbd>^SPW</kbd>²     | `(SB)` or<br />`(^SB)`² | 
DF |                   <samp>def-</samp> <samp>dif-</samp> | <kbd>TKP</kbd>                        | `(DF)` | 
DV |                   <samp>dev-</samp> <samp>div-</samp> | <kbd>TKW</kbd>                        | `(DW)` | 
DS |                   <samp>des-</samp> <samp>dis-</samp><br /><samp>dec-</samp><br /><samp>desc-</samp> <samp>disc-</samp><br /> | <kbd>STK</kbd> | `(DS)` | | | </td></tr></tbody><tbody><tr><td colspan="7">**Fricative + fricative**
SF |                  <samp>suff-</samp> <samp>surf-</samp>| <kbd>STP</kbd>                        | `(SF)` | 
SV |                  <samp>subv-</samp> <samp>surv-</samp>| <kbd>SW</kbd>                         | `(SW)` | 

1. when it conflicts with <samp>dep-</samp> <kbd>TKP</kbd> `(DP)`
2. when it conflicts with <samp>int-</samp> <kbd>SPW</kbd> `(INT)`

<!-- consequence cons- vs. sequence -->
<!-- shr- simp- sus- dist- disg- -->
<!-- constr- SKR vs. const- ST? -->
<!-- See http://cheapandsleazy.net/filez/A_Stroke_in_Time_by_Paul_Simone.pdf -->

#### Caveats

Sometimes the dictionary includes:

* shifty inversions, 
such as <samp>album</samp> <kbd>^PWHRUPL</kbd> `(^BLUM)`
or <samp>abduct</samp> <kbd>^TKPWUBGT</kbd> `(^DBUKT)`
* fingery conveniences,
such as <samp>elected</samp> <kbd>^HREBGD</kbd> `(^LEKD)`
for canonical <kbd>^HREBGTD</kbd> `(^LEKTD)` –
as per the `main.json` entry <kbd>AOE/HREBGD</kbd> `(EE/LEKD)`
* ~~misstrokes~~ actually just manual data entry errors at this point
* generous brainfarty fallbacks,
such as <samp>active</samp> <kbd>^TWEUF</kbd>
for canonical <kbd>^TW</kbd> (core of the <samp>activ-</samp> word family)
* redundant redundancies that I’ll never actually use but are there for completionism’s sake,
such as <samp>upon</samp> <kbd>^POPB</kbd> `(^PON)`
* opinionated briefs,
such as pretty much most of the dictionary (I had an example but it slipped my mind)
* or orphans,
such as <samp>apple</samp> <kbd>^PHR</kbd> `(^PL)`
because before I got deep into this whole rabbit hole I tried defining it as <kbd>WAPL</kbd>
although I guess that conflicts with <samp>wam</samp> so it was cute while it lasted

#### Stressed pre-initials

Sometimes the conceit is stretched to include
any pre-initial vowel if convenient, even if stressed,
such as <samp>era</samp> <kbd>^RA</kbd>, or if it would be annoying to write out.
But words like <samp>efficacy</samp> are probably not in scope.
(I’ll move these into `caret-stressed.json`, okay)

Words without initial stress take precedence,
so even the misstroke <samp>eleventh</samp> <kbd>^HREFPBT</kbd>
precedes <samp>elephant</samp>.

Word families are kept together in the core part of the dictionary,
even if one word happens to be stress-initial.
For example, <samp>illustrate</samp> and <samp>illustrative</samp>.
Similarly, words with ambiguous initial stress are kept in core,
such as <samp>apparatus</samp>.

#### Word family starters

Starter | Steno | Pseudosteno | Example
-|-|-|-
<samp>activ</samp> | <kbd>^TW</kbd> | `(^TW)` | <samp>activate</samp> <kbd>^TWAEUT</kbd><br /><samp>activity</samp> <kbd>^TWEUT</kbd>
<samp>autom</samp><br /><samp>autonom</samp> | <kbd>^TPWH</kbd> | `(^TWM)` | <samp>automate</samp> <kbd>^TPWHAEUT</kbd><br /><samp>autonomy</samp> <kbd>^TPWHEU</kbd>
<samp>electr</samp> | <kbd>^TWR</kbd> | `(^TWR)` | <samp>electron</samp> <kbd>^TWROPB</kbd><br /><samp>electric</samp> <kbd>^TWREUBG</kbd>

#### Conflict theory

Tries to use <kbd>\*</kbd> to more or less resolve conflicts
based on an informal hierarchy of differently colored schwas:

* Spelled with <samp>a</samp> etc. or pronounced with a low-mid vowel
or schwa (“schwa”) /ə æ ʌ/ etc.
* Spelled with <samp>e</samp>, <samp>i</samp>, etc. or pronounced with a front vowel
or i-colored schwa ([“schwi”](https://en.wikipedia.org/wiki/Schwi)) /i ɪ ɨ ᵻ ɛ/ etc.
* Spelled with <samp>o</samp>, <samp>au</samp>, etc. or pronounced with a back vowel
or u-colored schwa ([“schwu”](https://en.wikipedia.org/wiki/Schwu)) /ɵ ᵿ oʊ ɔ ɒ/ etc.

So for example:

* <samp><b>a</b>ddition</samp> <kbd>^TKEUGS</kbd> `(^DISHUN)`
* <samp><b>e</b>dition</samp> <kbd>^TK\*EUGS</kbd> `(^D*ISHUN)`
* ~~<samp><b>au</b>dition</samp>~~ would be next in line
but alas the overworked <kbd>\*</kbd> key only allows
distinguishing one bit of conflict

Another example:

* ~~<samp><b>a</b> mission</samp>~~ would be first in line
if this phrase were actually needed,
but the two worthier words below take more priority
* <samp><b>e</b>mission</samp> <kbd>^PHEUGS</kbd> `(^MISHUN)`
* <samp><b>o</b>mission</samp> <kbd>^PH\*EUGS</kbd> `(^M*ISHUN)`

The farther the vowel is from mid central, the lower the priority:

* <samp><b>e</b>licit</samp> <kbd>^HREUS/EUT</kbd> `(^LIS/IT)`
* <samp><b>i</b>llicit</samp> <kbd>^HR\*EUS/EUT</kbd> `(^L*IS/IT)`

But derivations of asterisked words can be unasterisked
if there is no longer a conflict:

* <samp><b>a</b>llusion</samp> <kbd>^HRAOUGS</kbd> `(^LUUSHUN)`
* <samp><b>i</b>llusion</samp> <kbd>^HRAO\*UGS</kbd> `(^L*UUSHUN)`
* <samp><b>i</b>llusory</samp>: both <kbd>^HRAOUS/REU</kbd> `(^LUUS/RI)`
and <kbd>^HRAO\*US/REU</kbd> `(^L*UUS/RI)`
because \*<samp>allusory</samp> isn’t a word

The <samp>a lot</samp>/<samp>allot</samp>
and <samp>a lot of</samp>/<samp>aloft</samp> conflicts
are resolved by using <kbd>AU</kbd> for the latters.
Although per the above, <samp>allotment</samp> is both
<kbd>^HRAUPLT</kbd> `(^LAUMT)` and <kbd>^HROPLT</kbd> `(^LOMT)`.

Not yet consistent, might try to keep word families together.
TODO figure out better <samp>efficient</samp>/<samp>officiate</samp>
and <samp>acceptable</samp>/<samp>accessible</samp>

#### Pseudosteno

When relevant, `^` can be written in pseudosteno
as initial `a` `e` or `o` instead.
For example, `^DISHUN` → `aDISHUN`, `^D*ISHUN` → `eD*ISHUN` or whatever.
I guess `^sT` for <samp>ext</samp> <kbd>^ST</kbd> can work too

### `*-prefix-word-parts.json`

Contains non-word prefixes such as <samp>extens</samp> <kbd>^STENS</kbd>
to make longer words from parts.
For example, <samp>extensible</samp> does not need to be explicitly defined
as it can be formed from <samp>extens</samp> + <samp>-able</samp> <kbd>-BL</kbd>.
(Wait, this is a bad example oof)

Though some entries are arguably independent words,
such as <samp>anon</samp> <kbd>^TPHOPB</kbd> `(^NON)`
or <samp>admin</samp> <kbd>^TKPHEUPB</kbd> `(^DMIN)`,
I put them here due to their intentional function of taking suffixes.
For this reason, these entries are not literally prefixes of the form `{blah^}`.
Those affixes (prefixes and suffixes) are in `*-affixes.json`.

### `*-phrasing.json`

Multi-word entries that could be considered part of
a more memorization-heavy “phrasing” system.

Half the entries are just short mandatories + <kbd>^</kbd>
that give the word <samp>a</samp> appended on either before or after,
such as <samp>a bit</samp> <kbd>^PWEUT</kbd> `(^BIT)`
or <samp>from a</samp> <kbd>^TPR</kbd> `(^FR)`

Highly attested phrasings that seem wholly uncontroversial,
such as <samp>akin to</samp> <kbd>^KEUPBT</kbd> `(^KINT)`
or <samp>according to</samp> <kbd>^KORGT</kbd>,
are in the non-phrasing dictionaries instead.

### `caret-as-s.json`

Shape-based outlines that relied on top <kbd>S</kbd>
have been redefined with <kbd>^</kbd> in place of <kbd>S</kbd>

### `caret-trying-out.json`

Testing ground for some guys I’m trying out, will see how it feels

### `user-*.json`

I mean sure? but probably of little interest until [Chordial](https://chordial.app/) exists

### `user-main-overrides.json`

Cause I really don’t like these defaults.
Also includes some prefixes,
such as <samp>zee</samp> <kbd>SAO\*E</kbd> `(ZEE)`
or <samp>ob</samp> <kbd>OB</kbd> `(OB)`,
but I put them in this file because the intent is entirely
to cover up annoying defaults that confuse me
when ~~typing~~ ~~stroking~~ ~~outlining~~ writing longer words

### `user-punctuation.json`

“Sentence” means sentence-contextual (built-in feature that attaches punctuation to preceding word).
Add <kbd>\*</kbd> to the first four (Period, Comma, Question, Exclamation) for unspaced versions.

I envision <samp>?</samp> <kbd>KW-PL</kbd> and <samp>!</samp> <kbd>TP-BG</kbd> as shape-based complements of each other:
the shape of <kbd>KW-PL</kbd> ascends from left to right like a question’s intonation rising ↗︎, and
the shape of <kbd>TP-BG</kbd> descends like the inflection of an exclamation falling ↘︎.
([See also](https://www.paulfioravanti.com/blog/plover-for-the-record/#ending-punctuation))

Code | Command | Spacing | Steno | Shape | Explanation | Plover default
-|-|-|-|-|-|-
<samp>\{.}</samp>    | Period      | Sentence  | <kbd>TP-PL</kbd>     | <ins>⠈⠁</ins>⠀<ins>⠀⠉⠀</ins> | middle+ring, also **F**u**LL** sto**P**                                | yes
<samp>\{,}</samp>    | Comma       | Sentence  | <kbd>KW-BG</kbd>     | <ins>⠐⠂</ins>⠀<ins>⠀⠒⠀</ins> | low mnemonic for descender                                             | yes
<samp>\{?}</samp>    | Question    | Sentence  | <kbd>KW-PL</kbd>     | <ins>⠐⠂</ins>⠀<ins>⠀⠉⠀</ins> | shaped like rising intonation,<br>also quasi-p. **QU**estion **M**ark  | yes
<samp>\{!}</samp>    | Exclamation | Sentence  | <kbd>TP-BG</kbd>     | <ins>⠈⠁</ins>⠀<ins>⠀⠒⠀</ins> | shaped like falling intonation,<br>also quasi-phonetic **B**an**G**    | yes
<samp>\{^:^}</samp>  | Colon       | Unspaced  | <kbd>TH-FL</kbd>     | <ins>⠈⠈</ins>⠀<ins>⠈⠈⠀</ins> | dot pairs, on upper row like <samp>.</samp> | <kbd>KHR-PB</kbd> (**C**o**L**o**N**)
<samp>\{:}</samp>    | Colon       | Sentence  | <kbd>^P-PT</kbd>     | <ins>⠁⠁</ins>⠀<ins>⠀⠁⠁</ins> | same but further out                          | <kbd>STPH-FPLT</kbd>
<samp>\{^;^}</samp>  | Semicolon   | Unspaced  | <kbd>KR-RG</kbd>     | <ins>⠐⠐</ins>⠀<ins>⠐⠐⠀</ins> | dot pairs, on lower row like <samp>,</samp> | <kbd>TH-FL</kbd>
<samp>\{;}</samp>    | Semicolon   | Sentence  | <kbd>SW-BS</kbd>     | <ins>⠂⠂</ins>⠀<ins>⠀⠂⠂</ins> | same but further out                          | <kbd>STPH\*FPLT</kbd>, <kbd>SP-PT</kbd>
<samp>\{^…}</samp>   | Ellipsis    | After     | <kbd>SW*</kbd>       | <ins>⠂⠂</ins>⠂<ins>⠀⠀⠀</ins> | three dots on lower left row                  | <kbd>HR-PS</kbd> (e**L**li**PS**is)
<samp>\{^\_^}</samp> | Underscore  | Unspaced  | <kbd>KWR-RBG</kbd>   | <ins>⠐⠒</ins>⠀<ins>⠐⠒⠀</ins> | low line, index-middle-ring                   | <kbd>RUPBD</kbd> (**UND**e**R**)
<samp>\{^-^}</samp>  | Hyphen      | Unspaced  | <kbd>H-F</kbd>       | <ins>⠀⠈</ins>⠀<ins>⠁⠀⠀</ins> | tiny line across upper row                    | <kbd>H-PB</kbd> (**H**yphe**N**)
<samp>\-</samp>      | Dash        | Spaced    | <kbd>PH-FP</kbd>     | <ins>⠀⠉</ins>⠀<ins>⠉⠀⠀</ins> | short line across upper row                   | <kbd>H*PB</kbd>
–                    | En dash     | Spaced    | <kbd>TPH-FPL</kbd>   | <ins>⠈⠉</ins>⠀<ins>⠉⠁⠀</ins> | longer line across upper row                  | <kbd>TPH-RB</kbd> (**N**da**SH**)
—                    | Em dash     | Spaced    | <kbd>^TPH-FPLT</kbd> | <ins>⠉⠉</ins>⠀<ins>⠉⠉⠀</ins> | longest line across upper row                 | <kbd>PH-RB</kbd> (**M**da**SH**)

### `user-punctuation-paired.json`

For paired punctuation, such as (opening and closing) brackets and quotation marks.

I prefer outlines based on iconic symbol shapes to outlines based on symbol names.
Outlines for the opening/closing square brackets, curly braces, and angle brackets
use exclusively the left/right key banks respectively.
To avoid conflicts, the main outlines for opening/closing parentheses use both banks,
with vowels <kbd>A</kbd> and <kbd>U</kbd> meaning opening/closing respectively.
When I want to type symbols, I don’t want my hands to feel like they’re typing real words,
and vice versa.

For aesthetic reasons, the vowel keys in the diagrams below
are positioned to line up with the <kbd>WR</kbd> and <kbd>RG</kbd> keys,
although by default the Uni lines them up with <kbd>R\*₂</kbd> and <kbd>\*₄R</kbd>.
This layout decision does not apply to other sections of this document.

Code | Command | Spacing | Steno | Shape | Explanation | Plover default
-|-|-|-|-|-|-
<samp>\{~\|(^}</samp>               | Paren open     | Before  | <kbd>KPAPG</kbd>     | <ins>⠐⠅</ins>⠀<ins>⠀⠑⠀</ins> | shaped like parenthesis,<br />left vowel for open   | <kbd>PREPB</kbd> (**P**a**REN**)
<samp>\{^~\|)}</samp>               | Paren close    | After   | <kbd>KPUPG</kbd>     | <ins>⠐⠁</ins>⠀<ins>⠀⠕⠀</ins> | shaped like parenthesis,<br />right vowel for close | <kbd>PR*EPB</kbd>
<samp>\{~\|()^}<br />\{#Left}</samp>| Paren both     | Before  | <kbd>KPAUPG</kbd>    | <ins>⠐⠅</ins>⠀<ins>⠀⠕⠀</ins> | shaped like parentheses,<br />cursor in between     | <kbd>PR*EPBS</kbd> (meant for code,<br />not prose)</tbody>
<samp>\{[^}</samp>                  | Bracket open   | Before  | <kbd>TKPA</kbd>      | <ins>⠘⠅</ins>⠀<ins>⠀⠀⠀</ins> | shaped like square bracket           | <kbd>PWR-BGT</kbd> (**BR**ac**K**e**T**)
<samp>\{^]}</samp>                  | Bracket close  | After   | <kbd>UPLG</kbd>      | <ins>⠀⠀</ins>⠀<ins>⠀⠝⠀</ins> | shaped like square bracket                          | <kbd>PWR*BGT</kbd>
<samp>\{~\|[]^}<br />\{#Left}</samp>| Bracket both   | Before  | <kbd>TKPAUPLG</kbd>  | <ins>⠘⠅</ins>⠀<ins>⠀⠝⠀</ins> | shaped like square bracket                          | none</tbody>
<samp>\{[^}</samp>                  | Brace open     | Before  | <kbd>SKPWA</kbd>     | <ins>⠒⠅</ins>⠀<ins>⠀⠀⠀</ins> | left  brace protruding out                          | <kbd>TPR-BGT</kbd> (**FR**ench brac**K**e**T**)
<samp>\{^]}</samp>                  | Brace close    | After   | <kbd>UPBGS</kbd>     | <ins>⠀⠀</ins>⠀<ins>⠀⠕⠂</ins> | right brace protruding out                          | <kbd>TPR*BGT</kbd>
<samp><\{^}</samp>                  | Angle open     | Before  | <kbd>TKWA</kbd>      | <ins>⠘⠆</ins>⠀<ins>⠀⠀⠀</ins> | left  angle tilted 45° CCW ⤺                        | <kbd>PWRABG</kbd> (**BRACK**et)
<samp>\{^}></samp>                  | Angle close    | After   | <kbd>UBLG</kbd>      | <ins>⠀⠀</ins>⠀<ins>⠀⠞⠀</ins> | right angle tilted 45° CW  ⤸                        | <kbd>PWRA*BG</kbd>
<samp>\{\'^}</samp>                 | Quote open     | Before  | <kbd>KW-LT</kbd>     | <ins>⠐⠂</ins>⠀<ins>⠀⠈⠁</ins> | analog of <kbd>KW-GS</kbd> for <samp>"</samp>  open,<br />top row mnemonic for <samp>\'</samp> form;<br />also quasi-p. **QU**ote **L**ef**T**                | <kbd>SKW-T</kbd> (**S**ingle **QU**o**T**e)
<samp>\{^\'}</samp>                 | Quote close    | After   | <kbd>KR-LT</kbd>     | <ins>⠐⠐</ins>⠀<ins>⠀⠈⠁</ins> | analog of <kbd>KR-GS</kbd> for <samp>"</samp> close,<br />top row mnemonic for <samp>\'</samp> form;<br />also quasi-p. **Q**uote **R**igh**T**                | <kbd>SKW*T</kbd>, <kbd>-PBT</kbd>


Some alternate versions:

Code | Command | Spacing | Steno | Shape | Explanation
-|-|-|-|-|-
<samp>\{~\|(^} </samp>         | Paren open     | Before   | <kbd>STKPWA</kbd>    | <ins>⠚⠇</ins>⠀<ins>⠀⠀⠀</ins> | shaped like thicker paren
<samp>\{^~\|)} </samp>         | Paren close    | After    | <kbd>UPBLGS</kbd>    | <ins>⠀⠀</ins>⠀<ins>⠀⠟⠂</ins> | shaped like thicker paren
<samp><\{^}</samp>                  | Angle open     | Before   | <kbd>TPWA</kbd>      | <ins>⠈⠇</ins>⠀<ins>⠀⠀⠀</ins> | left  angle tilted 135° CW ⤸
<samp>\{^}></samp>                  | Angle close    | After    | <kbd>UPBL</kbd>      | <ins>⠀⠀</ins>⠀<ins>⠀⠏⠀</ins> | right angle tilted 135° CCW ⤺


Add <kbd>\*</kbd> for unspaced versions.

Code | Command | Spacing | Steno | Shape | Explanation | Plover default
-|-|-|-|-|-|-
<samp>\{^}(\{^}</samp>         | Paren open     | Unspaced | <kbd>STKPWA\*</kbd>  | <ins>⠚⠇</ins>⠀<ins>⠂⠀⠀</ins> | shaped like thicker paren      | <kbd>P\*PB</kbd> (**P**are**N**)
<samp>\{^})\{^}</samp>         | Paren close    | Unspaced | <kbd>\*UPBLGS</kbd>  | <ins>⠀⠀</ins>⠂<ins>⠀⠟⠂</ins> | shaped like thicker paren      | <kbd>P\*PBT</kbd> (**P**are**NT**hesis)
etc.

### `user-commands.json`

#### Retroactives

Left side of the board is mnemonic for “retroactive.”

Code | Command | Steno | Pseudosteno | Shape | Explanation
-|-|-|-|-|-
<samp>\{\*+}</samp> | [Repeat Last Stroke](https://github.com/openstenoproject/plover/wiki/Dictionary-Format#retroactively-delete-space) | <kbd>#</kbd>    | `#`                        || wiki default |
<samp>\{\*}</samp>  | [Toggle Asterisk](https://github.com/openstenoproject/plover/wiki/Dictionary-Format#retroactively-delete-space) | <kbd>#\*</kbd>  | `#*`                       || wiki default |
<samp>\{\*?}</samp> | [Retro Add Space](https://github.com/openstenoproject/plover/wiki/Dictionary-Format#retroactively-add-space) | <kbd>#SK</kbd>   | i.e. <kbd>#SK</kbd>   | <ins>⠒⠄</ins>⠀<ins>⠀⠀⠀</ins> | horizontal is mnemonic for add space
<samp>\{\*!}</samp> | [Retro Delete Space](https://github.com/openstenoproject/plover/wiki/Dictionary-Format#retroactively-delete-space) | <kbd>2K</kbd>   | i.e. <kbd>#TK</kbd>   | <ins>⠘⠄</ins>⠀<ins>⠀⠀⠀</ins> | vertical is mnemonic for no gap
<samp>#NOOP</samp> || <kbd>2K3W</kbd> | i.e. <kbd>#TKPW</kbd> | <ins>⠘⠇</ins>⠀<ins>⠀⠀⠀</ins> | used for notes-to-self

#### Spacing control

Need to add backspace

Code | Command | Steno | Shape | Explanation | Plover default
-|-|-|-|-|-
<samp>\{^^}</samp> | [Suppress Next Space](https://github.com/openstenoproject/plover/wiki/Dictionary-Format#suppress-next-space)  | <kbd>TK-TS</kbd> | <ins>⠘⠀</ins>⠀<ins>⠀⠀⠃</ins> | 2nd-furthest columns     | <kbd>TK-LS</kbd> (**D**e**L**ete **S**pace)
<samp>\{^^}</samp> | Suppress Next Space | <kbd>TK-LG</kbd> | <ins>⠘⠀</ins>⠀<ins>⠀⠘⠀</ins> | both ring fingers | <kbd>TK-LS</kbd> (**D**e**L**ete **S**pace)

#### Capitalization

I'm going to change most of these into shape-based briefs

Code | Command | Steno | Pseudosteno | Explanation | Plover default
-|-|-|-|-|-
<samp>\{\*-\|}</samp>     | Retro Capitalize | <kbd>KPA\*D</kbd>    | `KPA*D`  | + **-D** past tense    | yes
<samp>\{>}</samp>         | Next Lower       | <kbd>HRO\*ER</kbd>   | `LO*ER`  | **LO**w**ER**case          | yes
<samp>\{\*>}</samp>       | Retro Lower      | <kbd>HRO\*ERD</kbd>  | `LO*ERD` | + **-D** past tense    | yes
<samp>\{<}</samp>         | Next All Caps    | <kbd>KPA\*L</kbd>    | `KPA*L`  | **C**a**P ALL**                | yes
<samp>\{\*<}</samp>       | Retro All Caps   | <kbd>\*UPD</kbd>     | `*UPD`   | **UP**percase + **-D** | yes
<samp>\{MODE:CAPS}</samp> | All Caps On      | <kbd>KA\*PS</kbd>    | `KA*PS`  | all **CAPS**           | yes

#### OS cursor movement and shortcuts

Code | Command | Steno | Pseudosteno | Explanation
-|-|-|-|-
<samp>\{#Control_L(a)}</samp> | <kbd>⌃A</kbd> (like <kbd>Home</kbd> on Mac) | <kbd>^H\*FT</kbd>    | `^H*FT`  | <kbd>\*</kbd> + <kbd>SH-FT</kbd> for <kbd>Home</kbd>, with <kbd>^</kbd> for top <kbd>S</kbd>
<samp>\{#Control_L(e)}</samp> | <kbd>⌃E</kbd> (like <kbd>End</kbd> on Mac)  | <kbd>SR\*RS</kbd>    | `SR*RS`  | <kbd>\*</kbd> + <kbd>SR-RS</kbd> for <kbd>End</kbd>
<samp>\{#Shift_L(Tab)}</samp> | <kbd>⇧⇥</kbd>               | <kbd>STA\*B</kbd>    | `STA*B`  | **S**hift + Tab
<samp>\{#Super_L(f)}</samp>   | <kbd>⌘F</kbd>               | <kbd>KPH-F</kbd>     | `KPH-F`  |
<samp>\{#Super_L(s)}</samp>   | <kbd>⌘S</kbd>               | <kbd>KPH-S</kbd>     | `KPH-S`  |

#### Plover dictionary and GUI/plugin manipulation

Code | Command | Steno | Pseudo/Shape | Explanation | Plover default
-|-|-|-|-|-
<samp>\{PLOVER:LOOKUP}</samp> | Lookup                        | <kbd>HR-FR</kbd>     | <ins>⠀⠘</ins>⠀<ins>⠃⠀⠀</ins>  | both index fingers | <kbd>PHR*UP</kbd>
<samp>\{PLOVER:ADD_T…}</samp> | Add Translation               | <kbd>PWHR-FRPB</kbd> | <ins>⠀⠛</ins>⠀<ins>⠛⠀⠀</ins>  | both index+middle | <kbd>TKUPT</kbd>
<samp>\{PLOVER:FOCUS}</samp>  | Show Plover                   | <kbd>PHROERB</kbd>   | `PLOESH` | **PL**over **SHOW** | <kbd>PHROFBGS</kbd>
<samp>\{PLOVER:FOCUS}{#<br>Super(Shift(K))}</samp> | Open Word Tray†               | <kbd>PHRORTD</kbd>   | `PLORDT` | **PL**over w**ORD T**ray
<samp>\{PLOVER:FOCUS}{#<br>Super(Shift(L))}</samp> | Open Spectra Lexer            | <kbd>PHRERBGT</kbd>  | `PLERKT` | **PL**over sp**EKTR**a
<samp>\{PLOVER:FOCUS}{#<br>Super(Shift(S))}</samp> | Open SVG Layout†              | <kbd>PHROFGS</kbd>   | `PLOSFG` | **PL**over **SVG**
<samp>=wt_prev_page</samp>    | Word Tray Prev   | <kbd>#-RB</kbd>      | <ins>⠀⠄</ins>⠀<ins>⠐⠂⠀</ins>   | plugin-suggested
<samp>=wt_next_page</samp>    | Word Tray Next   | <kbd>#-GS</kbd>      | <ins>⠀⠄</ins>⠀<ins>⠀⠐⠂</ins>   | plugin-suggested
<samp>=wt_reload</samp>       | Word Tray Reload | <kbd>#-RBGS</kbd>    | <ins>⠀⠄</ins>⠀<ins>⠐⠒⠂</ins> | plugin-suggested

† To use, patch `word_tray_ui.py` by adding `SHORTCUT = "Ctrl+Shift+K"` in `class WordTrayUI`
and `SHORTCUT = "Ctrl+Shift+S"` in `layout_ui.py`

## License

Code in `plugins/`, `third-party-dictionaries/`, and `main.json` is not my own.
It’s just version controlled here to record my modifications
in order to prevent any updates from overwriting them.

OERZ TKO WHAFRT TPUBG UPT

^TR-BGS WELG

## Contributing

KR-BGS WELG

## TODO

* Document repo contents
* Methodology (how I went about finding what words to include)
* Split user.json into phrasing, plurals/edge-cases, prefixes, glaring-omissions
* Add one-liners, scripts, exploratory research (with documentation)
* Dictionary generator/preprocessor
to define e.g. `accustom` in terms of <kbd>^</kbd> + `{custom}`
* If I ever do all that I’ll name my ~~baby~~ theory <s>plonkver</s> thoeur (pronounced /θwɑːɹ/)
