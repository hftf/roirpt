# roirpt

(pronounced /ʁwaʁp/)

I basically just git initted in my plover dir and started committing WIPs

This README is better viewed [in full width](https://github.com/hftf/roirpt/blob/master/README.md) (> 1100 pixels)

## Contents

### A hundred dictionary files? Why so many?

File formats available for stenography dictionaries are extremely limited:
JSON is the default, while a few plugins allow for
Python scripts (dynamic dictionaries) or [Markdown documents](https://github.com/antistic/plover_markdown_dictionary)
(entries embedded in code blocks interweave with verbose comments
in [Literate Programming](https://en.wikipedia.org/wiki/Literate_programming) style)
to behave as dictionaries.
There is no systematic capability for well-structured dictionary data
with annotations, tags, or metadata
holding explanatory comments, multiple categories (such as domain or context of use), cross-references,
creation/modification dates, usage or misstroke statistics, review or conflict status,
preferred/prescribed outlines, or any other elaborating information.
This is not conducive to learning or communicating.

The only option is to maintain separate dictionaries.

There are many advantages:
Each dictionary’s filename labels its purpose.
It is easier to manually inspect and manipulate entries, since similar entries tend to be closer to each other.
Separate dictionaries can be reordered, enabled, or disabled at will.
Entries demonstrating one concept are found in a single file easily shared with others
(“here are all of, and only, the entries that follow the <kbd>AE</kbd> → <samp>ject</samp> pattern”)
that can be borrowed without worrying about massive conflicts.

Indeed, it is unwieldy to maintain a large number of dictionaries in Plover’s interface,
and not all entries cleanly fit within a single dictionary (but choosing one is not a science).

### `caret-*.json`

Introduces <kbd>^</kbd> to represent a pre-initial schwa.\*
Requires the [`plover-stenotype-extended`](https://github.com/sammdot/plover-stenotype-extended) plugin.

A few groups of rhymes so you can see why this might be useful:

Group | Word | Steno | Pseudosteno | Plover default entries
-|-|-|-|-
-end | <samp>pend</samp>   | <kbd>PEPBD</kbd>    | `(PEND)`   | <kbd>PEPBD</kbd>
|| <samp>spend</samp>      | <kbd>SPEPBD</kbd>   | `(SPEND)`  | <kbd>SPEPBD</kbd>
|| <samp>append</samp>     | <kbd>^PEPBD</kbd>   | `(^PEND)`  | <kbd>A(P)/PEPBD</kbd>
|| <samp>expend</samp>     | <kbd>KPEPBD</kbd> or<br><kbd>^SPEPBD</kbd>   | `(XEND)`  or<br>`(^SPEND)`  | <kbd>KPEPBD</kbd> or <kbd>EBGS/PEPBD</kbd>
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

\* 
Note: This is not a new idea; people have implemented similar ideas before in different ways
(see [phenrsteno](https://github.com/chambln/plover-phenrsteno) for where I got the inspiration).
I chose `^` since it looks like both a small superscript `A`
and also the IPA symbol ʌ, which is used to represent a (usually stressed) schwa in English.
I like using a punctuation character (rather than e.g. `a` or `e`)
because I like the ability to easily grep for steno strokes as strings of only uppercase letters or symbols,
and because in general-purpose search engines I can search for strokes and it will return results that ignore the symbol
(although that could eventually be a footgun).

> [!TIP]
>
> ### Crash-course glossary of phonetic terms used
>
> It is not necessary to know these terms,
> as their meaning can still be understood in context and through the examples.
>
> #### Manners of articulation
>
> <dl>
> <dt>Stop<dd>Consonant with sudden release after blocked airflow.
> (<samp>p</samp>, <samp>b</samp>, <samp>t</samp>, <samp>d</samp>, <samp>k</samp>, <samp>g</samp>)
> <dt>Nasal<dd>Consonant with continuous release and airflow through nose.
> (<samp>m</samp>, <samp>n</samp>)
> <dt>Fricative<dd>Consonant with continuous release and turbulent airflow.
> (<samp>f</samp>, <samp>v</samp>, <samp>s</samp>, <samp>z</samp>, <samp>sh</samp>, <samp>th</samp>, <samp>h</samp>)
> <dt>Affricate<dd>Consonant that combines stop followed by fricative.
> (<samp>ch</samp>, <samp>j</samp>)
> <dt>Liquid<dd>Consonant with continuous release and non-turbulent airflow.
> (<samp>l</samp>, <samp>r</samp>)
> </dl>
>
> #### Syllable parts
>
> <dl>
> <dt>Initial<dd>Consonant (or consonant cluster) forming the <a href="https://en.wikipedia.org/wiki/Syllable#Onset">onset</a> (beginning part) of a syllable.
> <dt>Pre-initial<dd><a href="https://en.wikipedia.org/wiki/Minor_syllable">Minor syllable</a> before main syllable part.
> Usually limited to weak, unstressed <a href="https://en.wikipedia.org/wiki/Syllable_weight">light syllables</a>
> (e.g. <samp><ins>a</ins>bout</samp>, <samp><ins>em</ins>bed</samp>).
> <dt>Schwa<dd>Neutral vowel “uh” (ə) common in English unstressed syllables.
> </dl>

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
1. <kbd>^ST</kbd>: “<samp>est-</samp>” is shorthand for “<samp>ast-</samp>, <samp>aust-</samp>, <samp>est-</samp>, <samp>ist-</samp>, <samp>ost-</samp>, etc.”
(as in <samp><b>ast</b>ute</samp>, <samp><b>aust</b>ere</samp>, <samp><b>est</b>ate</samp>, <samp><b>Ist</b>anbul</samp>, <samp><b>ost</b>ensible</samp>)
2. <kbd>^KP</kbd>: is <samp>ext-</samp> or <samp>exp-</samp> or <samp>exc-</samp> when used with <kbd>R</kbd> (as in <samp><b>ext</b>ra</samp> <kbd>^KPRA</kbd>, <samp><b>exp</b>ress</samp> <kbd>^KPRES</kbd>)

#### Compound initial sounds

In development (not really). Looking for permanent homes for certain starters (marked with ? for now).

For certain other combinations (stop, fricative + stop, stop + fricative, stop + fricative + stop),
see the table under [the <samp>ex-</samp>/<samp>comp-</samp> conflict](#the-ex-comp--conflict-etc).

<table>
<thead>
<tr>
<th>Type</th>
<th>Starter</th><th>Steno</th><th>Pseudo</th>
<th>Starter</th><th>Steno</th><th>Pseudo</th>
</tr>
</thead>
<tbody>
<tr></tr>
<tr>
<td></td>
<th colspan="3"><strong>no prefix</strong></td>
<th colspan="3"><strong>prefixed with <samp>com-</samp> <samp>con-</samp> <kbd>K-</kbd></strong></td>
</tr></tbody>
<tbody>
<tr><td colspan="7"><strong>Nasal + nasal</strong></td></tr>
<tr>
<td>MM</td>
<td><samp>amm-</samp> <samp>emm-</samp> <samp>imm-</samp></td>
<td><kbd>^PH</kbd></td>
<td><code>(^M)</code></td>
<td><samp>comm-</samp></td>
<td><kbd>KPH</kbd></td>
<td><code>(KM)</code></td>
</tr>
<tr>
<td>NN</td>
<td><samp>ann-</samp> <samp>enn-</samp> <samp>inn-</samp></td>
<td><kbd>^TPH</kbd></td>
<td><code>(^N)</code></td>
<td><samp>conn-</samp></td>
<td><kbd>K</kbd></td>
<td><code>(K)</code></td>
</tr>
</tbody>
<tbody>
<tr><td colspan="7"><strong>Nasal + stop</strong></td></tr>
<tr>
<td>MP</td>
<td><samp>amp-</samp> <samp>emp-</samp> <samp>imp-</samp></td>
<td><kbd>KPW</kbd></td>
<td><code>(IMP)</code></td>
<td><samp>comp-</samp></td>
<td><kbd>KP</kbd></td>
<td><code>(KP)</code></td>
</tr>
<tr>
<td>MB</td>
<td><samp>amb-</samp> <samp>emb-</samp> <samp>imb-</samp></td>
<td><kbd>KPW</kbd></td>
<td><code>(IMP)</code></td>
<td><samp>comb-</samp></td>
<td><kbd>KPW</kbd></td>
<td><code>(KB)</code></td>
</tr>
<tr>
<td>NT</td>
<td><samp>ant-</samp> <samp>ent-</samp> <samp>int-</samp></td>
<td><kbd>SPW</kbd></td>
<td><code>(INT)</code></td>
<td><samp>cont-</samp></td>
<td><kbd>K</kbd></td>
<td><code>(K)</code></td>
</tr>
<tr>
<td>ND</td>
<td><samp>and-</samp> <samp>end-</samp> <samp>ind-</samp></td>
<td><kbd>SKP</kbd></td>
<td><code>(AND)</code></td>
<td><samp>cond-</samp></td>
<td><kbd>K</kbd></td>
<td><code>(K)</code></td>
</tr>
<tr>
<td>NK</td>
<td><samp>anc-</samp> <samp>enc-</samp> <samp>inc-</samp><br><samp>ank-</samp> <samp>enk-</samp> <samp>ink-</samp></td>
<td><kbd>^TKP</kbd></td>
<td><code>(INK)</code></td>
<td><samp>conc-</samp><br><samp>conk-</samp></td>
<td><kbd>K</kbd></td>
<td><code>(K)</code></td>
</tr>
<tr>
<td>NG</td>
<td><samp>ang-</samp> <samp>eng-</samp> <samp>ing-</samp></td>
<td><kbd>^STKPW</kbd></td>
<td><code>(ING)</code></td>
<td><samp>cong-</samp></td>
<td><kbd>K</kbd></td>
<td><code>(K)</code></td>
</tr>
</tbody>
<tbody>
<tr><td colspan="7"><strong>Nasal + affricate</strong></td></tr>
<tr>
<td>NJ</td>
<td><samp>    </samp> <samp>enj-</samp> <samp>inj-</samp><br><samp>ang-</samp> <samp>eng-</samp> <samp>ing-</samp>³</td>
<td><kbd>^SKWHR</kbd></td>
<td><code>(INJ)</code></td>
<td><samp>conj-</samp><br><samp>cong-</samp>³</td>
<td>?</td>
<td></td>
</tr>
</tbody>
<tbody>
<tr><td colspan="7"><strong>Nasal + fricative</strong></td></tr>
<tr>
<td>NF</td>
<td><samp>    </samp> <samp>enf-</samp> <samp>inf-</samp></td>
<td><kbd>TPW</kbd></td>
<td><code>(INF)</code></td>
<td><samp>comf-</samp><br><samp>conf-</samp></td>
<td><kbd>TKP</kbd> or<br><kbd>TKP*</kbd>¹</td>
<td><code>(KF)</code> or<br><code>(KF*)</code>¹</td>
</tr>
<tr>
<td>NV</td>
<td><samp>    </samp> <samp>env-</samp> <samp>inv-</samp></td>
<td><kbd>TPWH</kbd></td>
<td><code>(NW)</code></td>
<td><samp>conv-</samp></td>
<td><kbd>KW</kbd></td>
<td><code>(KW)</code></td>
</tr>
<tr>
<td>NS</td>
<td><samp>ans-</samp> <samp>ens-</samp> <samp>ins-</samp><br><samp>anc-</samp> <samp>enc-</samp> <samp>inc-</samp>³</td>
<td><kbd>STPH</kbd></td>
<td><code>(SN)</code></td>
<td><samp>cons-</samp><br><samp>conc-</samp>³</td>
<td><kbd>SK</kbd></td>
<td><code>(SK)</code></td>
</tr>
</tbody>
<tbody>
<tr><td colspan="7"><strong>Nasal + fricative + stop</strong></td></tr>
<tr>
<td>NSP</td>
<td><samp>    </samp><samp>    </samp> <samp>insp-</samp></td>
<td><kbd>STPH</kbd></td>
<td><code>(SN)</code></td>
<td><samp>consp-</samp></td>
<td><kbd>SKP</kbd></td>
<td><code>(KSP)</code></td>
</tr>
<tr>
<td>NST</td>
<td><samp>    </samp><samp>    </samp> <samp>inst-</samp></td>
<td><kbd>STPH</kbd></td>
<td><code>(SN)</code></td>
<td><samp>const-</samp></td>
<td>?</td>
<td></td>
</tr>
<tr>
<td>NSK</td>
<td><samp>    </samp><samp>    </samp> <samp>insc-</samp></td>
<td><kbd>STPH</kbd></td>
<td><code>(SN)</code></td>
<td><samp>consc-</samp></td>
<td>?</td>
<td></td>
</tr>
</tbody>
<tbody>
<tr><td colspan="7"><strong>Stop + fricative</strong></td></tr>
<tr>
<td>BS</td>
<td><samp>abs-</samp> <samp>obs-</samp></td>
<td><kbd>SPW</kbd> or<br><kbd>^SPW</kbd>²</td>
<td><code>(SB)</code> or<br><code>(^SB)</code>²</td>
<td rowspan="4" colspan="3">n/a</td>
</tr>
<tr>
<td>DF</td>
<td><samp>def-</samp> <samp>dif-</samp></td>
<td><kbd>TKP</kbd> or<br><kbd>TKW</kbd>¹</td>
<td><code>(DF)</code> or<br><code>(DW)</code>¹</td>
</tr>
<tr>
<td>DV</td>
<td><samp>dev-</samp> <samp>div-</samp></td>
<td><kbd>TKW</kbd></td>
<td><code>(DW)</code></td>
</tr>
<tr>
<td>DS</td>
<td><samp>des-</samp> <samp>dis-</samp><br><samp>dec-</samp>³<br><samp>desc-</samp> <samp>disc-</samp>³</td>
<td><kbd>STK</kbd></td>
<td><code>(DS)</code></td>
</tr>
</tbody>
<tbody>
<tr><td colspan="7"><strong>Fricative + fricative</strong></td></tr>
<tr>
<td>SF</td>
<td><samp>suff-</samp> <samp>surf-</samp></td>
<td><kbd>STP</kbd></td>
<td><code>(SF)</code></td>
<td rowspan="2" colspan="3">n/a</td>
</tr>
<tr>
<td>SV</td>
<td><samp>subv-</samp> <samp>surv-</samp></td>
<td><kbd>SW</kbd></td>
<td><code>(SW)</code></td>
</tr>
</tbody>
</table>

1. when it conflicts with <samp>dep-</samp> <kbd>TKP</kbd> `(DP)`
2. when it conflicts with <samp>int-</samp> <kbd>SPW</kbd> `(INT)`
3. followed by a front vowel (<samp>e</samp>, <samp>i</samp>, <samp>y</samp>) only, i.e. “soft” pronunciations of <samp>c</samp> or <samp>g</samp>

<!-- consequence cons- vs. sequence -->
<!-- shr- simp- sus- dist- disg- -->
<!-- constr- SKR vs. const- ST? -->
<!-- See http://cheapandsleazy.net/filez/A_Stroke_in_Time_by_Paul_Simone.pdf -->

Example mnemonics for a few starters:

Starter | Steno | Explanation | Shape | Resembles
-|-|-|-|-
NK | <kbd>^TKP</kbd>   | `(K)` + <kbd>^TP</kbd>, like `(N)` shifted left | ▜▘ | ⚓️ **anc**hor 
NG | <kbd>^STKPW</kbd> | `(G)` + <kbd>^S</kbd> | █▌ | 🔳 quadr**ang**le 
NJ | <kbd>^SKWHR</kbd> | `(J)` + <kbd>^H</kbd> | ▙▟ | 🌉 **eng**ineer’s suspension bridge 
NF | <kbd>TPW</kbd>    | `(F)` + <kbd>W</kbd>  | <samp> </samp>▜ | ꟻ  an inverted F
NV | <kbd>TPWH</kbd>   | `(NW)`                | ▝▛ | ✉️ **env**elope

The pattern for the prefix <samp>con-</samp> plus a consonant can be thought of as
<kbd>K</kbd> alone when the consonant is a non-labial non-continuant, and
<kbd>K</kbd> overlapped with the consonant otherwise.
This is because in the former case, consonant chords already overlap with <kbd>K</kbd>.

<table>
<thead><tr><td colspan="2"></td>
<th colspan="2">Labial</th><th colspan="2">Coronal</th><th colspan="2">Velar</th>
</tr></thead>
<tbody align="center" valign="top">
<tr><th align="left" valign="middle" bgcolor="blue" rowspan="3">Non-continuants</th>
    <th align="left" valign="middle">Nasal</th><td></td><td><kbd>KPH</kbd><br><samp>comm-</samp></td><td></td><td><kbd>K</kbd><br><samp>conn-</samp></td><td></td><td></td></tr>
<tr><th align="left" valign="middle">Stop</th><td><kbd>KP</kbd><br><samp>comp-</samp></td><td><kbd>KPW</kbd><br><samp>comb-</samp></td><td><kbd>K</kbd><br><samp>cont-</samp></td><td><kbd>K</kbd><br><samp>cond-</samp></td><td><kbd>K</kbd><br><samp>conc-</samp><br><samp>conk-</samp></td><td><kbd>K</kbd><br><samp>cong-</samp></td></tr>
<tr><th align="left" valign="middle">Affricate</th>
<td></td><td></td><td></td><td><kbd>K</kbd><br><samp>conj-</samp><br><samp>cong-</samp>³</td><td></td><td></td></tr>
<tr><th align="left" valign="middle" rowspan="2">Continuants</th>
    <th align="left" valign="middle">Fricative</th>
<td><kbd>TKP</kbd><br><samp>comf-</samp><br><samp>conf-</samp></td><td><kbd>KW</kbd><br><samp>conv-</samp></td><td><kbd>SK</kbd><br><samp>cons-</samp><br><samp>conc-</samp>³</td><td></td><td></td><td></td></tr>
<tr><th align="left" valign="middle">Liquid</th>
<td></td><td></td><td><kbd>KHR</kbd><br><samp>coll-</samp></td><td><kbd>KR</kbd><br><samp>corr-</samp></td><td></td><td></td></tr>
</tbody>
</table>

#### More complex compound starters?

Recently thinking about adding a few more starters, inspired by [wooningeire](https://github.com/wooningeire/plover-dicts.pub/tree/pub). Most seem rare though (not counting productive prefixes like <samp>in-</samp>). My dictionary contains some ad-hoc solutions, e.g. <samp>anthology</samp> <kbd>SPWO\*LG</kbd> `(INT*OLG)` that try to get away with dropping consonants, e.g. <samp>enthusiast</samp> <kbd>^THAOUFT</kbd> `(^THUUſT)`, which I mostly dislike.

Type | Starter | Steno | Explanation | Example
-|-|-|-|-
MF   | <samp>amph-  emph-</samp>   | <kbd>KPWH</kbd><br /><kbd>TPW</kbd>  | <kbd>KPW</kbd>  + <kbd>H</kbd> | amphibious, emphatic
NTH  | <samp>anth-  enth-</samp>   | <kbd>SPWH</kbd>  | <kbd>SPW</kbd>  + <kbd>H</kbd> | anthem, anthology, anthropology, enthrone
NKP  | <samp>incap- incomp-</samp> | <kbd>^TKP</kbd>  | <kbd>^TKP</kbd> (<kbd>P</kbd> reused) | incapable, incapacitate, incompatible, incompliant
NKSP | <samp>inconsp-</samp>       | <kbd>^STKP</kbd> | <kbd>^TKP</kbd> + <kbd>S</kbd> | inconspicuous
NKV  | <samp>inconv-</samp>        | <kbd>^TKPW</kbd> | <kbd>^TKP</kbd> + <kbd>W</kbd> | inconvenient
NCH  | <samp>ench- incoh-</samp>   | <kbd>^TKPH</kbd> | <kbd>^TKP</kbd> + <kbd>H</kbd> | enchant, incoherent

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

Note that word family starters usually contain the primary stress (e.g. <samp>elèctr</samp>).
This is different from most other caret entries, which conventionally have unstressed starters.

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

### `caret-ipa-fingerspelling.json`

Fingerspelling dictionary for IPA symbols used in (American) English
as well as a selection of commonly used IPA symbols in general.
Omits ordinary letters, like <samp>s</samp>,
as they can be fingerspelled normally.
Intended to be iconic and useful, rather than comprehensive.

Like ordinary fingerspelling, the left bank is used for consonants
and the vowel bank is used for vowels,
but the right bank is used for some vowel variants and suprasegmentals as well.

<kbd>^\*-</kbd> is used for IPA fingerspelling, and
<kbd>^\*-P</kbd> for suprasegmental symbols.
The consonants follow the convention of
`H` for fricative (if the base is plosive)
or palato-alveolar (if the base is already fricative),
`R` for retroflex, and
`HR` for palatal (i.e. alveolo-palatal).
The vowels follow the convention of
`-F` for turned or barred variants.

<table>
<thead><tr><th>IPA</th><th>Chord</th><th>Base</th><th>Explanation</th></tr></thead>
<tbody>
<tr><th colspan="4">Suprasegmentals</th></tr>
<tr><td><samp>ʰ</samp>   </td><td><kbd>^-FPD</kbd>     </td><td><kbd>-P</kbd></td><td><kbd>-FD</kbd> <code>(-H)</code></td></tr>
<tr><td><samp>ˈ</samp>   </td><td><kbd>^-PD</kbd>      </td><td><kbd>-P</kbd></td><td><kbd>-D</kbd> top</td></tr>
<tr><td><samp>ː</samp>   </td><td><kbd>^-PDZ</kbd>     </td><td><kbd>-P</kbd></td><td><kbd>-DZ</kbd> top and bottom</td></tr>
<tr><td><samp>ˌ</samp>   </td><td><kbd>^-PZ</kbd>      </td><td><kbd>-P</kbd></td><td><kbd>-Z</kbd> bottom</td></tr>
</tbody>
<tbody>
<tr><th colspan="4">Consonants</th></tr>
<tr><td><samp>ɸ</samp>   </td><td><kbd>^TP*</kbd>     </td><td><kbd>TP</kbd> <code>(F)</code>     </td><td>F, since <kbd>^PH*</kbd> is used for <samp>ɱ</samp></tr>
<tr><td><samp>β</samp>   </td><td><kbd>^PWH*</kbd>    </td><td><kbd>PW</kbd> <code>(B)</code>     </td><td>B + fricative <code>H</code></td></tr>
<tr><td><samp>θ</samp>   </td><td><kbd>^TH*</kbd>     </td><td><kbd>T</kbd> <code>(T)</code>      </td><td>T + fricative <code>H</code></td></tr>
<tr><td><samp>ʈ</samp>   </td><td><kbd>^TR*</kbd>     </td><td><kbd>T</kbd> <code>(T)</code>      </td><td>T + retroflex <code>R</code></td></tr>
<tr><td><samp>ɬ</samp>   </td><td><kbd>^THR*</kbd>    </td><td><kbd>T</kbd> <code>(T)</code>      </td><td>T + <kbd>HR</kbd> <code>(L)</code></td></tr>
<tr><td><samp>ð</samp>   </td><td><kbd>^TKH*</kbd>    </td><td><kbd>TK</kbd> <code>(D)</code>     </td><td>D + fricative <code>H</code></td></tr>
<tr><td><samp>ɖ</samp>   </td><td><kbd>^TKR*</kbd>    </td><td><kbd>TK</kbd> <code>(D)</code>     </td><td>D + retroflex <code>R</code></td></tr>
<tr><td><samp>ɟ</samp>   </td><td><kbd>^TKHR*</kbd>   </td><td><kbd>TK</kbd> <code>(D)</code>     </td><td>D + palatal   <code>HR</code></td></tr>
<tr><td><samp>dʒ</samp>  </td><td><kbd>^SKWR*</kbd>   </td><td><kbd>SKWR</kbd> <code>(J)</code>   </td><td>convenient for <samp>d</samp> <kbd>TK*</kbd> + <samp>ʒ</samp></tr>
<tr><td><samp>ʃ</samp>   </td><td><kbd>^SH*</kbd>     </td><td><kbd>S</kbd> <code>(S)</code>      </td><td>S + fricative <code>H</code></td></tr>
<tr><td><samp>ʂ</samp>   </td><td><kbd>^SR*</kbd>     </td><td><kbd>S</kbd> <code>(S)</code>      </td><td>S + retroflex <code>R</code></td></tr>
<tr><td><samp>ɕ</samp>   </td><td><kbd>^SHR*</kbd>    </td><td><kbd>S</kbd> <code>(S)</code>      </td><td>S + palatal   <code>HR</code></td></tr>
<tr><td><samp>ʒ</samp>   </td><td><kbd>^STKPWH*</kbd> </td><td><kbd>STKPW</kbd> <code>(Z)</code>  </td><td>Z + fricative <code>H</code></td></tr>
<tr><td><samp>ʐ</samp>   </td><td><kbd>^STKPWR*</kbd> </td><td><kbd>STKPW</kbd> <code>(Z)</code>  </td><td>Z + retroflex <code>R</code></td></tr>
<tr><td><samp>ʑ</samp>   </td><td><kbd>^STKPWHR*</kbd></td><td><kbd>STKPW</kbd> <code>(Z)</code>  </td><td>Z + palatal   <code>HR</code></td></tr>
<tr><td><samp>χ</samp>   </td><td><kbd>^KH*</kbd>     </td><td><kbd>K</kbd> <code>(K)</code>      </td><td>K + fricative <code>H</code></td></tr>
<tr><td><samp>ç</samp>   </td><td><kbd>^KHR*</kbd>    </td><td><kbd>K</kbd> <code>(K)</code>      </td><td>K + palatal   <code>HR</code></td></tr>
<tr><td><samp>ɡ</samp>   </td><td><kbd>^TKPW*</kbd>   </td><td><kbd>TKPW</kbd> <code>(G)</code>   </td><td></tr>
<tr><td><samp>ɣ</samp>   </td><td><kbd>^TKPWH*</kbd>  </td><td><kbd>TKPW</kbd> <code>(G)</code>   </td><td>G + fricative <code>H</code></td></tr>
<tr><td><samp>ʁ</samp>   </td><td><kbd>^TKPWR*</kbd>  </td><td><kbd>TKPW</kbd> <code>(G)</code>   </td><td>ɢ’s uvularity + rhotic R</td></tr>
<tr><td><samp>ʔ</samp>   </td><td><kbd>^TKPWHR*</kbd> </td><td><kbd>TKPWHR</kbd> <code>(GL)</code></td><td><b>GL</b>ottal</td></tr>
<tr><td><samp>ɱ</samp>   </td><td><kbd>^PH*</kbd>     </td><td><kbd>PH</kbd> <code>(M)</code>     </td><td></tr>
<tr><td><samp>ŋ</samp>   </td><td><kbd>^TPH*</kbd>    </td><td><kbd>TPH</kbd> <code>(N)</code>    </td><td></tr>
<tr><td><samp>ɳ</samp>   </td><td><kbd>^TPHR*</kbd>   </td><td><kbd>TPH</kbd> <code>(N)</code>    </td><td>N + retroflex <code>R</code></td></tr>
<tr><td><samp>ɹ</samp>   </td><td><kbd>^R*</kbd>      </td><td><kbd>R</kbd> <code>(R)</code>      </td><td></tr>
</tbody>
<tbody>
<tr><th colspan="4">Semivowels</th></tr>
<tr><td><samp>ʍ</samp>   </td><td><kbd>^WH*</kbd>      </td><td><kbd>WH</kbd> <code>(WH)</code>    </td><td></tr>
<tr><td><samp>ɥ</samp>   </td><td><kbd>^WHR*</kbd>     </td><td><kbd>W</kbd> <code>(W)</code>      </td><td>W + palatal <code>HR</code></td></tr>
<tr><td><samp>ɰ</samp>   </td><td><kbd>^WR*</kbd>      </td><td><kbd>WR</kbd>           </td><td></tr>
</tbody>
<tbody>
<tr><th colspan="4">Long vowels and diphthongs</th></tr>
<tr><td><samp>iː</samp>  </td><td><kbd>^AO*E</kbd>    </td><td><kbd>AOE</kbd> <code>(EE)</code> </td><td></tr>
<tr><td><samp>ɪəɹ</samp> </td><td><kbd>^AO*ER</kbd>   </td><td><kbd>AOE</kbd> <code>(EE)</code> </td><td>+ <code>R</code></td></tr>
<tr><td><samp>eɪ</samp>  </td><td><kbd>^A*EU</kbd>    </td><td><kbd>AEU</kbd> <code>(AI)</code> </td><td></tr>
<tr><td><samp>ɛəɹ</samp> </td><td><kbd>^A*EUR</kbd>   </td><td><kbd>AEU</kbd> <code>(AI)</code> </td><td>+ <code>R</code></td></tr>
<tr><td><samp>aɪ</samp>  </td><td><kbd>^AO*EU</kbd>   </td><td><kbd>AOEU</kbd> <code>(II)</code></td><td></tr>
<tr><td><samp>aɪəɹ</samp></td><td><kbd>^AO*EUR</kbd>  </td><td><kbd>AOEU</kbd> <code>(II)</code></td><td>+ <code>R</code></td></tr>
<tr><td><samp>uː</samp>  </td><td><kbd>^AO*U</kbd>    </td><td><kbd>AOU</kbd> <code>(UU)</code> </td><td></tr>
<tr><td><samp>ʊəɹ</samp> </td><td><kbd>^AO*UR</kbd>   </td><td><kbd>AOU</kbd> <code>(UU)</code> </td><td>+ <code>R</code></td></tr>
<tr><td><samp>oʊ</samp>  </td><td><kbd>^O*E</kbd>     </td><td><kbd>OE</kbd> <code>(OE)</code>  </td><td></tr>
<tr><td><samp>ɔəɹ</samp> </td><td><kbd>^O*ER</kbd>    </td><td><kbd>OE</kbd> <code>(OE)</code>  </td><td>+ <code>R</code></td></tr>
<tr><td><samp>aʊ</samp>  </td><td><kbd>^O*U</kbd>     </td><td><kbd>OU</kbd> <code>(OU)</code>  </td><td></tr>
<tr><td><samp>aʊɹ</samp> </td><td><kbd>^O*UR</kbd>    </td><td><kbd>OU</kbd> <code>(OU)</code>  </td><td>+ <code>R</code></td></tr>
<tr><td><samp>ɔɪ</samp>  </td><td><kbd>^O*EU</kbd>    </td><td><kbd>OEU</kbd> <code>(OI)</code> </td><td></tr>
</tbody>
<tbody>
<tr><th colspan="4">Short vowels</th></tr>
<tr><td><samp>ɪ</samp>   </td><td><kbd>^*EU</kbd>     </td><td><kbd>EU</kbd> <code>(I)</code>   </td><td></tr>
<tr><td><samp>ɪəɹ</samp> </td><td><kbd>^*EUR</kbd>    </td><td><kbd>EU</kbd> <code>(I)</code>   </td><td>+ <code>R</code></td></tr>
<tr><td><samp>ɨ</samp>   </td><td><kbd>^*EUF</kbd>    </td><td><kbd>EU</kbd> <code>(I)</code>   </td><td>+ <code>F</code> for barred</td></tr>
<tr><td><samp>ɛ</samp>   </td><td><kbd>^*E</kbd>      </td><td><kbd>E</kbd> <code>(E)</code>    </td><td></tr>
<tr><td><samp>əɹ</samp>  </td><td><kbd>^*ER</kbd>     </td><td><kbd>E</kbd> <code>(E)</code>    </td><td>+ <code>R</code></td></tr>
<tr><td><samp>ə</samp>   </td><td><kbd>^*EF</kbd>     </td><td><kbd>E</kbd> <code>(E)</code>    </td><td>+ <code>F</code> for turned</td></tr>
<tr><td><samp>æ</samp>   </td><td><kbd>^A*</kbd>      </td><td><kbd>A</kbd> <code>(A)</code>    </td><td></tr>
<tr><td><samp>æ</samp>   </td><td><kbd>^A*E</kbd>     </td><td><kbd>AE</kbd> <code>(AE)</code>  </td><td>(redundant)</td></tr>
<tr><td><samp>ɑɹ</samp>  </td><td><kbd>^A*R</kbd>     </td><td><kbd>A</kbd> <code>(A)</code>    </td><td>+ <code>R</code> (redundant)</td></tr>
<tr><td><samp>ɐ</samp>   </td><td><kbd>^A*F</kbd>     </td><td><kbd>A</kbd> <code>(A)</code>    </td><td>+ <code>F</code> for turned</td></tr>
<tr><td><samp>ɑ</samp>   </td><td><kbd>^A*U</kbd>     </td><td><kbd>AU</kbd> <code>(AU)</code>  </td><td></tr>
<tr><td><samp>ɑɹ</samp>  </td><td><kbd>^A*UR</kbd>    </td><td><kbd>AU</kbd> <code>(AU)</code>  </td><td>+ <code>R</code></td></tr>
<tr><td><samp>ɒ</samp>   </td><td><kbd>^A*UF</kbd>    </td><td><kbd>AU</kbd> <code>(AU)</code>  </td><td>+ <code>F</code> for turned</td></tr>
<tr><td><samp>ɔ</samp>   </td><td><kbd>^O*</kbd>      </td><td><kbd>O</kbd> <code>(O)</code>    </td><td></tr>
<tr><td><samp>ɔɹ</samp>  </td><td><kbd>^O*R</kbd>     </td><td><kbd>O</kbd> <code>(O)</code>    </td><td>+ <code>R</code></td></tr>
<tr><td><samp>ɵ</samp>   </td><td><kbd>^O*F</kbd>     </td><td><kbd>O</kbd> <code>(O)</code>    </td><td>+ <code>F</code> for barred</td></tr>
<tr><td><samp>œ</samp>   </td><td><kbd>^O*EF</kbd>    </td><td><kbd>OE</kbd> <code>(OE)</code>  </td><td>+ <code>F</code> for ligature</td></tr>
<tr><td><samp>ʊ</samp>   </td><td><kbd>^AO*</kbd>     </td><td><kbd>AO</kbd> <code>(OO)</code>  </td><td></tr>
<tr><td><samp>ʌ</samp>   </td><td><kbd>^*U</kbd>      </td><td><kbd>U</kbd> <code>(U)</code>    </td><td></tr>
<tr><td><samp>ɜːɹ</samp> </td><td><kbd>^*UR</kbd>     </td><td><kbd>U</kbd> <code>(U)</code>    </td><td>+ <code>R</code></td></tr>
<tr><td><samp>ʉ</samp>   </td><td><kbd>^*UF</kbd>     </td><td><kbd>U</kbd> <code>(U)</code>    </td><td>+ <code>F</code> for barred</td></tr>
<!-- <tr><td><samp>ɚ</samp>   </td><td><kbd>^*R</kbd>      </td><td>                      </td><td>+ <code>R</code></td></tr> -->
<tr><td><samp>ɯ</samp>   </td><td><kbd>^PH*F</kbd>    </td><td><kbd>PH</kbd> <code>(M)</code>   </td><td>+ <code>F</code> for turned</td></tr>
</tbody>
</table>

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
