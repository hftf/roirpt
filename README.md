# roirprt

## Contents

### `caret-*.json`

Introduces `^` to represent a pre-initial schwa.
Requires the `plover-stenotype-extended` plugin.

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
such as `era: ^RA`, if it would be annoying to write out.
But words like `efficacy` are probably not in scope.

Sometimes the dictionary includes:

* shifty inversions, 
such as `album: ^PWHRUPL (^BLUM)` or `abduct: ^TKPWUBGT (^DBUKT)`
* fingery conveniences,
such as `elected: ^HREBGD (^LEKD)` for canonical `^HREBGTD (^LEKTD)` –
as per the `main.json` entry `AOE/HREBGD (EE/LEKD)`
* ~~misstrokes~~ actually just manual data entry errors at this point
* generous brainfarty fallbacks
such as `active: ^TWEUF` for canonical `^TW` (and core of `activ-` word family)
* redundant redundancies that I'll never actually use but are there for completionism's sake, such as `upon: ^POPB (^PON)`
* opinionated briefs, such as pretty much most of the dictionary (I had an example but it slipped my mind)
* or orphans, such as `apple: ^PHR (^PL)` because before I got deep into this whole rabbit hole I tried defining it as `WAPL` although I guess that conflicts with `wam` so it was cute while it lasted

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
* Spelled with `o`, `au`, etc. or pronounced with a back or rounded vowel or u-colored schwa (["schwu"](https://en.wikipedia.org/wiki/Schwu)) /ɵ ᵿ oʊ ɔ ɒ/ etc.

So for example:

* **a**ddition: `^TKEUGS (^DISHUN)`,
* **e**dition: `^TK*EUGS (^D*ISHUN)`,
* ~~**au**dition~~ would be next in line but alas the overworked `*` key only allows distinguishing one bit of conflict

Another example:

* ~~**a** mission~~ would be first in line if this phrase were actually needed, but the two worthier words below take more priority
* **e**mission: `^PHEUGS (^MISHUN)`
* **o**mission: `^PH*EUGS (^M*ISHUN)`

The farther the vowel is from mid central, the lower the priority:

* **e**licit: `^HREUS/EUT (^LIS/IT)`
* **i**llicit: `^HR^EUS/EUT (^L*IS/IT)`

But derivations of asterisked words can be unasterisked if there is no conflict:

* **a**llusion: `^HRAOUGS (^LUUSHUN)`
* **i**llusion: `^HRAO*UGS (^L*UUSHUN)`
* **i**llusory: both `^HRAOUS/REU (^LUUS/RI)` and `^HRAO*US/REU (^L*UUS/RI)`

The `a lot` / `allot` and `a lot of` / `aloft` conflicts are resolved by using `AU` for the latters.

Per the above, `allotment: ^HRAUPLT (^LAUMT)` or `^HROPLT (^LOMT)`.

Not yet consistent, might try to keep word families together.
TODO figure out better `efficient`/`officiate` and `acceptable`/`accessible`

#### Pseudosteno

When relevant, the `^` can be written in pseudosteno as initial `a` `e` or `o` instead. For example, `^DISHUN` → `aDISHUN`, `^D*ISHUN` → `eD*ISHUN` or whatever. I guess `^sT` for `ext: ^ST` can work too

### `*-prefixes.json`

Contains non-word prefixes such as `extens: ^STENS` to make longer words from parts. For example, `extensible` does not need to be explicitly defined as it can be formed from `extens` + `-able: -BL`. (Wait, this is a bad example oof)

Though some entries are arguably independent words (`anon: ^TPHOPB (^NON)`, `admin: ^TKPHEUPB (^DMIN)`), I put them here due to their intentional function of taking suffixes. For this reason, these entries are not literally prefixes of the form `{blah^}`.

### `*-phrasing.json`

Multi-word entries that would be considered part of a more memorization-heavy "phrasing" system.

Highly attested phrasings that seem wholly uncontroversial, such as `akin to: ^KEUPBT (^KINT)` or `according to: ^KORGT`, are in the non-phrasing dictionaries instead.

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
