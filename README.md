# roirprt

I basically just git initted in my plover dir and started committing WIPs

## Contents

### `caret-*.json`

Introduces `^` to represent a pre-initial schwa.
Requires the [`plover-stenotype-extended`](https://github.com/sammdot/plover-stenotype-extended) plugin.

So you can see why this might be useful:

* `pend: PEPBD (PEND)`
* `spend: SPEPBD (SPEND)`
* `append: ^PEPBD (^PEND)`
* `expend: KPEPBD (XEND)`
* `extend: ^STEPBD (^STEND)`

More:

* `sent: SEPBT (SENT)`
* `assent: ^SEPBT (^SENT)`
* `accent: ^KPEPBT (^XENT)`
* `stent: STEPBT (STENT)`
* `extent: ^STEPBT (^STENT)`
* `competent: KPEPBT (KPENT)`
* `scent: SKEPBT (SKENT)` or `SKREPBT (SCENT)`
* `consent: SK*EPBT (SK*ENT)`

Sometimes the conceit is stretched to include
any pre-initial vowel if convenient, even if stressed,
such as `era: ^RA`, or if it would be annoying to write out.
But words like `efficacy` are probably not in scope.
(I'll move these into caret-stressed.json, okay)

Sometimes the dictionary includes:

* shifty inversions, 
such as `album: ^PWHRUPL (^BLUM)` or `abduct: ^TKPWUBGT (^DBUKT)`
* fingery conveniences,
such as `elected: ^HREBGD (^LEKD)` for canonical `^HREBGTD (^LEKTD)` –
as per the `main.json` entry `AOE/HREBGD (EE/LEKD)`
* ~~misstrokes~~ actually just manual data entry errors at this point
* generous brainfarty fallbacks,
such as `active: ^TWEUF` for canonical `^TW` (core of the `activ-` word family)
* redundant redundancies that I'll never actually use but are there for completionism's sake,
such as `upon: ^POPB (^PON)`
* opinionated briefs,
such as pretty much most of the dictionary (I had an example but it slipped my mind)
* or orphans,
such as `apple: ^PHR (^PL)` because before I got deep into this whole rabbit hole I tried defining it as `WAPL` although I guess that conflicts with `wam` so it was cute while it lasted

#### Compound sounds

In development (not really)

Looking for permanent homes for:

* ang-
* abs-/obs-

#### Conflict theory

Tries to use `*` to more or less resolve conflicts
based on an informal hierarchy of differently colored schwas:

* Spelled with `a` etc. or pronounced with a low-mid vowel or schwa ("schwa") /ə æ ʌ/ etc.
* Spelled with `e`, `i`, etc. or pronounced with a front vowel or i-colored schwa (["schwi"](https://en.wikipedia.org/wiki/Schwi)) /i ɪ ɨ ᵻ ɛ/ etc.
* Spelled with `o`, `au`, etc. or pronounced with a back vowel or u-colored schwa (["schwu"](https://en.wikipedia.org/wiki/Schwu)) /ɵ ᵿ oʊ ɔ ɒ/ etc.

So for example:

* **a**ddition: `^TKEUGS (^DISHUN)`
* **e**dition: `^TK*EUGS (^D*ISHUN)`
* ~~**au**dition~~ would be next in line but alas the overworked `*` key only allows distinguishing one bit of conflict

Another example:

* ~~**a** mission~~ would be first in line if this phrase were actually needed, but the two worthier words below take more priority
* **e**mission: `^PHEUGS (^MISHUN)`
* **o**mission: `^PH*EUGS (^M*ISHUN)`

The farther the vowel is from mid central, the lower the priority:

* **e**licit: `^HREUS/EUT (^LIS/IT)`
* **i**llicit: `^HR*EUS/EUT (^L*IS/IT)`

But derivations of asterisked words can be unasterisked if there is no longer a conflict:

* **a**llusion: `^HRAOUGS (^LUUSHUN)`
* **i**llusion: `^HRAO*UGS (^L*UUSHUN)`
* **i**llusory: both `^HRAOUS/REU (^LUUS/RI)` and `^HRAO*US/REU (^L*UUS/RI)` because \*allusory isn't a word

The `a lot` / `allot` and `a lot of` / `aloft` conflicts are resolved by using `AU` for the latters.
Although per the above, `allotment` is both `^HRAUPLT (^LAUMT)` and `^HROPLT (^LOMT)`.

Not yet consistent, might try to keep word families together.
TODO figure out better `efficient`/`officiate` and `acceptable`/`accessible`

#### Pseudosteno

When relevant, the `^` can be written in pseudosteno as initial `a` `e` or `o` instead. For example, `^DISHUN` → `aDISHUN`, `^D*ISHUN` → `eD*ISHUN` or whatever. I guess `^sT` for `ext: ^ST` can work too

### `*-prefixes.json`

Contains non-word prefixes such as `extens: ^STENS` to make longer words from parts. For example, `extensible` does not need to be explicitly defined as it can be formed from `extens` + `-able: -BL`. (Wait, this is a bad example oof)

Though some entries are arguably independent words (`anon: ^TPHOPB (^NON)`, `admin: ^TKPHEUPB (^DMIN)`), I put them here due to their intentional function of taking suffixes. For this reason, these entries are not literally prefixes of the form `{blah^}`.

### `*-phrasing.json`

Multi-word entries that would be considered part of a more memorization-heavy "phrasing" system.

Half the entries are just short mandatories + `^` that give the word `a` appended on either before or after, such as `a bit: ^PWEUT (^BIT)` or `from a: ^TPR (^FR)`

Highly attested phrasings that seem wholly uncontroversial, such as `akin to: ^KEUPBT (^KINT)` or `according to: ^KORGT`, are in the non-phrasing dictionaries instead.

### `caret-as-s.json`

Definitions for shape-based outlines that relied on top S with `^` instead of `S`

### `caret-trying-out.json`

Testing ground for some guys I'm trying out, will see how it feels

### `user-*.json`

I mean sure? but probably of little interest until [Chordial](https://chordial.app/)

### `user-main-overrides.json`

Cause I really don't like these defaults. Also includes some prefixes, such as `zee: SAO*E (ZEE)` or `ob: OB (OB)`, but I put them in this file because the intent is entirely to cover up annoying defaults that confuse me
when ~~typing~~ ~~stroking~~ ~~outlining~~ writing longer words

## License

Code in `plugins/` and `main.json` is not my own, it's just
version controlled here to record my modifications
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
* Dictionary generator/preprocessor to define e.g. `accustom` in terms of `^` + `{custom}`
* If I ever do all that I'll name my ~~baby~~ theory plonkver
