# roirprt

I basically just git initted in my plover dir and started committing WIPs

## Contents

### `caret-*.json`

Introduces <kbd>^</kbd> to represent a pre-initial schwa.
Requires the [`plover-stenotype-extended`](https://github.com/sammdot/plover-stenotype-extended) plugin.

So you can see why this might be useful:

* <samp>pend</samp> <kbd>PEPBD</kbd> `(PEND)`
* <samp>spend</samp> <kbd>SPEPBD</kbd> `(SPEND)`
* <samp>append</samp> <kbd>^PEPBD</kbd> `(^PEND)`
* <samp>expend</samp> <kbd>KPEPBD</kbd> `(XEND)`
* <samp>extend</samp> <kbd>^STEPBD</kbd> `(^STEND)`

More:

* <samp>sent</samp> <kbd>SEPBT</kbd> `(SENT)`
* <samp>assent</samp> <kbd>^SEPBT</kbd> `(^SENT)`
* <samp>accent</samp> <kbd>^KPEPBT</kbd> `(^XENT)`
* <samp>stent</samp> <kbd>STEPBT</kbd> `(STENT)`
* <samp>extent</samp> <kbd>^STEPBT</kbd> `(^STENT)`
* <samp>competent</samp> <kbd>KPEPBT</kbd> `(KPENT)`
* <samp>scent</samp> <kbd>SKEPBT</kbd> `(SKENT)` or <kbd>SKREPBT</kbd> `(SCENT)`
* <samp>consent</samp> <kbd>SK\*EPBT</kbd> `(SK*ENT)`

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

### Stressed pre-initials

Sometimes the conceit is stretched to include
any pre-initial vowel if convenient, even if stressed,
such as <samp>era</samp> <kbd>^RA</kbd>, or if it would be annoying to write out.
But words like <samp>efficacy</samp> are probably not in scope.
(I’ll move these into caret-stressed.json, okay)

#### Compound sounds

In development (not really)

Looking for permanent homes for:

* ang-
* abs-/obs-

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
* <samp><b>i</b>llusory</samp> both <kbd>^HRAOUS/REU</kbd> `(^LUUS/RI)`
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

### `*-prefixes.json`

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

I mean sure? but probably of little interest until [Chordial](https://chordial.app/)

### `user-main-overrides.json`

Cause I really don’t like these defaults.
Also includes some prefixes,
such as <samp>zee</samp> <kbd>SAO\*E</kbd> `(ZEE)`
or <samp>ob</samp> <kbd>OB</kbd> `(OB)`,
but I put them in this file because the intent is entirely
to cover up annoying defaults that confuse me
when ~~typing~~ ~~stroking~~ ~~outlining~~ writing longer words

## License

Code in `plugins/` and `main.json` is not my own.
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
* If I ever do all that I’ll name my ~~baby~~ theory plonkver
