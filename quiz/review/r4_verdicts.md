# R4 blind review — §9 Service Accounts + Appendix D State Merklization (GP 0.8.0)

Ground truth: `/root/work/jam/gp-src/text/{accounts,merklization,serialization,definitions,pvm_invocations,reporting_assurance,notation}.tex`
plus `/root/work/jam/gp-src/preamble.tex` (0.8.0 symbol table) and `/root/work/jam/gp-raw.txt` (for rendered equation/appendix numbering).

Appendix lettering confirmed from `graypaper.tex` + `gp-raw.txt`:
A = PVM, B = VM Invocations, C = Serialization Codec, **D = State Merklization** (D.1 Serialization, D.2 Merklization,
D.2.1 Node Encoding and Trie Identification), E = General Merklization, F = Shuffling, G = Bandersnatch, H = Erasure Coding.
Rendered equation numbers confirmed: 9.1/9.2 = N_S and δ; **9.3 = the A tuple**; 9.5 = Λ domain; 9.6 = invariants;
9.7 = Λ/I; **9.8 = a_i, a_o, a_t**; 9.9–9.10 = χ.

---

## PHASE 1 — BLIND VERDICTS

### n=1 — `c3-ch09-expunge-delay`
- **My answer: index 2** — "Ω_H must return the same answer at every moment when auditing may still occur; the lookup anchor may itself be up to L = 14,400 timeslots older than recent history, so the period is that anchor age plus a further 4,800 slots (eight hours) of safety margin."
- **Confidence: HIGH**
- Settled by `pvm_invocations.tex:63–65` verbatim: *"The historical-lookup host-call function, Ω_H, is designed to give the same result regardless of the state of the chain for any time when auditing may occur (which we bound to be less than two epochs from being accumulated). The lookup anchor may be up to L timeslots before the recent history and therefore adds to the potential age at the time of audit. We therefore set D to have a safety margin of eight hours:"* followed by `D ≡ L + 4,800 = 19,200`. With `definitions.tex:273` L = 14,400 and `definitions.tex:262` D = 19,200. 4,800 slots × 6 s = 8 h. ✔
- Distractor notes: index 0 is *numerically* true (19,200 = 32 × E where E = 600) but ξ (`accumulated`) holds only E entries, and it is not the GP's stated reason. Index 1 is also numerically consistent (1,200 × 16) but is not stated anywhere and misstates the derivation.

### n=2 — `c3-ch09-service-info-leaf`
- **My answer: index 1** — "The service-info leaf carries a_i and a_o but not a_t, and it opens with a version octet 0; `info` has no version octet but does include a_t, laid out as E(a_c, E_8(a_b, a_t, a_g, a_m, a_o), E_4(a_i), E_8(a_f), E_4(a_r, a_a, a_p))."
- **Confidence: HIGH**
- `merklization.tex:87–103` (T(σ), row C(255, s)):
  `C(255,s) ↦ E( 0, a_c, E_8(a_b, a_g, a_m, a_o, a_f), E_4(a_i, a_r, a_a, a_p) )` — contains **a_o and a_i, not a_t**, and leads with a literal `0` (E(0) = one octet).
- `pvm_invocations.tex:499–517` (Ω_I, `info` = 6):
  `v = E( a_c, E_8(a_b, a_t, a_g, a_m, a_o), E_4(a_i), E_8(a_f), E_4(a_r, a_a, a_p) )` — **includes a_t**, no leading 0, and the field order differs from the leaf. Option 1's layout is a character-for-character match.
- So the two encodings are emphatically *not* byte-identical (index 0 wrong); a_i/a_o *are* serialized (index 2 wrong); the leaf does not carry a_t (index 3 wrong).
- Caveat to raise in Phase 2: the GP never calls the leading `0` a "version octet" — it just writes `0`. That naming is an implementation convention, not GP text.

### n=3 — `c3-ch09-write-threshold-go`
- **My answer: index 3** — "One storage entry costs 1 against a_i and 34 + |k| + |v| against a_o — both the key and the value are charged; when the post-write threshold exceeds the balance the call yields FULL and the account must be returned completely untouched…"
- **Confidence: HIGH**
- `accounts.tex:142–158` (eq. 9.8): `a_i ≡ 2·|a_l| + |a_s|` (so one storage entry = **1** item, one request entry = 2) and
  `a_o ≡ Σ_{(h,z)∈K(a_l)} 81 + z  +  Σ_{(x,y)∈a_s} 34 + |y| + |x|` — **the key |x| is charged as well as the value |y|**.
  This is decisive against the "34 + |v|" reading; do not settle it from the team's Go.
- `pvm_invocations.tex:492` (Ω_W): `⟨continue, FULL, **s**⟩ otherwhen a_t > a_b` — on FULL the *prior* account `s` is returned, i.e. untouched. ✔
- Note the Go excerpt's `CalcStorageItemfootprint` returns `1, 34 + len(key) + len(data)` — this matches eq. 9.8.

### n=4 — `c3-ch09-forget-lifecycle`
- **My answer: index 0** — "[] → the request entry is dropped; [x] → [x, t]; [x, y] → the request entry and a_p[h] are both expunged, but only once y < t − D; [x, y, w] → [w, t], again only once y < t − D; every other case returns HUH."
- **Confidence: HIGH** (with one genuine GP under-specification, see below)
- `pvm_invocations.tex:970–998` (Ω_F, `forget` = 25), the `a` clause verbatim:
  - `K(a_l) = K(x_s,l) \ {(h,z)} , K(a_p) = K(x_s,p) \ {h}` **when** `(x_s)_l[h,z] ∈ {[], [x,y]}, y < t − D`
  - `a_l[h,z] = [x, t]` **when** `(x_s)_l[h,z] = [x]`
  - `a_l[h,z] = [w, t]` **when** `(x_s)_l[h,z] = [x,y,w], y < t − D`
  - `error` otherwise
  and the result clause: HUH when `z ∉ N_L`; panic when `h = error`; **HUH when `a = error`**; OK otherwise.
- **Under-specification (real, and worth flagging):** the first guard is written as one condition over the *set* `{[], [x,y]}` with the trailing `y < t − D`. In the `[]` shape nothing binds `y`, so the age condition is vacuous/undefined there. The universally-implemented reading — and the only one that makes `[]` reachable at all — is that `[]` is dropped immediately with no delay, which is what option 0 states. A pedant could argue the `[]` branch is undefined; no other option is even close, so the key is safe, but any explanation asserting "the GP explicitly exempts [] from the delay" would be an over-claim.
- Note also `eject` (Ω_J, `pvm_invocations.tex:915`) carries the same `y < t − D` gate — so the D-slot delay is *not* exclusive to `eject` (index 3 wrong). `expunge` (Ω_X, `pvm_invocations.tex:704–716`) is an unrelated *inner-PVM machine teardown* call, nothing to do with preimages.

### n=5 — `c3-ch09-new-service-index`
- **My answer: index 2** — "The context's next free id starts as check((E⁻¹_4(H(E(s, η′_0, H_t))) mod (2^32 − S − 2^8)) + S) with S = 2^16 … check linearly probes forward, i ↦ (i − S + 1) mod (2^32 − 2^8 − S) + S, until it lands on an index outside K(δ); the registrar alone may instead name any index below S."
- **Confidence: HIGH**
- `pvm_invocations.tex:186` (the context initializer I): `x_i = check((E⁻¹_4(H(E(x_s, η'_0, H_t))) mod (2^32 − S − 2^8)) + S)`.
- `pvm_invocations.tex:254–257` (eq. 9? — rendered eq. label `eq:newserviceindex`): `check(i) ≡ i when i ∉ K(δ*); else check((i − S + 1) mod (2^32 − 2^8 − S) + S)` — forward linear probe. ✔
- `definitions.tex:281`: `S = 2^16`, *"The minimum public service index. Services of indices below these may only be created by the Registrar."* ✔
- `pvm_invocations.tex:837–838` (Ω_N): FULL when `x_s = χ_R ∧ i < S ∧ i ∈ K(δ)`; otherwise the registrar's chosen `i < S` is used directly. ✔
- Note: the *successor* id after a successful `new` is `check(S + (x_i − S + **42**) mod (2^32 − S − 2^8))` (`pvm_invocations.tex:841`) — the `+42` stride applies to advancing the context's next-free-id, whereas `check`'s own probe step is `+1`. Option 2 describes both correctly and does not conflate them.

### n=6 — `c3-ch09-privilege-mutation`
- **My answer: index 3** — "Ω_B is the one host call that rewrites (χ_M, χ_A, χ_V, χ_R, χ_Z) wholesale, and it now yields HUH unless the caller is χ_M itself … a core's assigner may still hand over its own χ_A[c] through `assign`, and `new` yields HUH whenever f ≠ 0 and the caller is not the manager."
- **Confidence: HIGH**
- `pvm_invocations.tex:740–761` (Ω_B, `bless` = 15): the result assigns
  `(x_u)_{(m, a, v, r, z)}` i.e. `(χ_M, χ_A, χ_V, χ_R, χ_Z) ← ⟨m, a, v, r, z⟩` wholesale, with
  `⟨continue, HUH, …⟩ otherwhen x_s ≠ (x_e)_m` (line 755) — caller must be the manager. ✔ (tuple order in the option matches the GP's order exactly)
- `pvm_invocations.tex:762–782` (Ω_A, `assign` = 16): `HUH otherwhen x_s ≠ (x_e)_a[c]` (line 774); on OK sets **both** `(x_e)_q[c] ← q` and `(x_e)_a[c] ← a` — i.e. the assigner hands its own slot over. ✔
- `pvm_invocations.tex:835` (Ω_N): `⟨continue, HUH, …⟩ otherwhen f ≠ 0 ∧ x_s ≠ (x_e)_m`. ✔
- `accounts.tex:164`: χ_M *"is the service able to effect an alteration of χ from block to block as well as bestow services with storage deposit credits"*, and *"χ_R alone is able to create new service accounts with indices in the protected range"*. ✔
- Index 1 is wrong twice over: privilege is not conferred by sitting below S, and `upgrade` (Ω_U, `pvm_invocations.tex:848–866`) sets only a_c/a_g/a_m — it cannot touch a_f.

### n=7 — `c3-appD-key-31-octets`
- **My answer: index 1** — "A node is fixed at 512 bit, and a leaf must fit a one-octet discriminator-plus-size header, the key, and a full 32-octet field for either the value or its hash: 1 + 31 + 32 = 64."
- **Confidence: HIGH**
- `merklization.tex:128–136` (D.2.1): *"Nodes are fixed in size at 512 bit (64 bytes)… The first bit discriminate between these two types… Leaf nodes are further subdivided into embedded-value leaves and regular leaves. The second bit… In the case of an embedded-value leaf, the remaining 6 bits of the first byte are used to store the embedded value size. **The following 31 bytes are dedicated to the state key. The last 32 bytes are defined as the value**… In the case of a regular leaf, the remaining 6 bits of the first byte are zeroed. The following 31 bytes store the state key. The last 32 bytes store the hash of the value."*
- Formally `L(k, v)` at `merklization.tex:144–150`: `[1,0] ⌢ bits(E_1(|v|))[2:] ⌢ bits(k) ⌢ bits(v) ⌢ [0,0,…]` — 8 + 248 + 256 = 512. ✔
- Index 0 is wrong: the discriminator lives in the *node*'s first bit, not in the key. Index 3 is wrong: a branch is `[0] ⌢ bits(l)[1:] ⌢ bits(r)` = 1 + 255 + 256, exactly full, with no spare octet and only two children.

### n=8 — `c3-appD-service-subkeys`
- **My answer: index 2** — "A four-octet marker is prepended before hashing — E_4(2^32−1) ⌢ k for storage, E_4(2^32−2) ⌢ h for a preimage, and E_4(l) ⌢ h for the lookup-meta of declared length l — and C(s, ·) then interleaves the four octets of n = E_4(s) with the first four octets of a = H(·), appending a_4 … a_26."
- **Confidence: HIGH**
- `merklization.tex:15` (third form of C): `(s, h) ↦ [n_0, a_0, n_1, a_1, n_2, a_2, n_3, a_3, a_4, a_5, …, a_26] where n = E_4(s), a = H(h)` — 8 interleaved + 23 = **31 octets**. ✔
- `merklization.tex:104–111` (final three rows of T(σ)):
  storage `C(s, E_4(2^32−1) ⌢ k) ↦ v`; preimages `C(s, E_4(2^32−2) ⌢ h) ↦ p`; requests `C(s, E_4(l) ⌢ h) ↦ E(↕[E_4(x) | x ∈ t])`. ✔
- Index 1 is wrong: preimages/lookup-meta do **not** use the `C(i, s)` chapter form (that form is used only for `C(255, s)`, the service-info leaf). Index 3 is wrong: storage keys are arbitrary blobs (`a_s ∈ D⟨B → B⟩`, eq. 9.3), not 32 octets. Index 0 invents 0xFD/0xFE/0xFF markers that appear nowhere.

### n=9 — `c3-appD-rho-guarantee`
- **My answer: index 1** — "Per core an optional pair ⟨a_g, E_4(a_t)⟩ written with the ? option discriminator, where a_g is the entire guarantee G ≡ (w work-report, t timeslot, a credential of 2–3 (validator index, Ed25519 signature) pairs) — so the guarantors' signatures are now part of committed state."
- **Confidence: HIGH on the 0.8.0 content; MED on the "delta" framing** (see Phase 2 — I have no 0.7.2 source in this tree to prove what changed).
- `merklization.tex:52–58`: `C(10) ↦ E( [ ?(⟨a_g, E_4(a_t)⟩) | ⟨a_g, a_t⟩ ∈ ρ ] )`.
- `reporting_assurance.tex:16–24` (eq. 11.1, `eq:reportingstate`): `ρ ∈ [C]{ ?( g: G, t: N_T ) }` — the first member is a **G**, not a W.
- `reporting_assurance.tex:266–274` (rendered **eq. 11.24**): `G ≡ (r ∈ R, t ∈ N_T, a ∈ ⟦(N, V̄)⟧_{2:3})` — work-report, timeslot, credential of 2–3 (validator index, Ed25519 signature) pairs. ✔
  *(Transparency note: my blind draft first wrote this as `(w ∈ W, …, (N, E))` — the same stale symbols the item uses. Corrected here during Phase 2 against `preamble.tex`; see finding **F-9a**. My chosen option index was unaffected.)*
- Serialization of a G (`serialization.tex:243–247`): `E(g_w, E_4(g_t), ↕[(E_2(v), s) | (v,s) ∈ g_a])` — so yes, the credential signatures land in committed state.
- Index 3 is wrong: the whole report, not just the availability spec, is committed.

### n=10 — `c3-appD-merklize-bitorder`
- **My answer: index 3** — "bits(·) runs most-significant-bit first, so depth d branches on bit 7 − (d mod 8) of octet ⌊d/8⌋; the shape follows from key bit-prefixes alone and never from slice order… folding sorted leaves pairwise builds a balanced tree and a different root."
- **Confidence: HIGH**
- `notation.tex:143` verbatim: *"We use the function bits(B) ∈ b to denote the sequence of bits, **ordered with the most significant first**, which represent the octet sequence B, thus bits([160, 0]) = [1, 0, 1, 0, 0, …]."* (160 = 0b1010_0000 ⇒ MSB-first.) ✔
- `merklization.tex:155–164`: `M_σ(σ) ≡ M({bits(k) ↦ (k,v)})` and M recurses by splitting on `b_0`, i.e. successive *most-significant* bits of the key — a Patricia trie whose shape is a function of key bit-prefixes only.
- The Go excerpt's `bitMask := byte(1 << (7 - depth%8))` with `byteIdx := depth / 8` is exactly MSB-first and therefore **correct**.
- Index 1 is wrong: bit-sequence *encoding* E(b) at `serialization.tex:64–74` packs LSB-first, but that is the codec for `b ∈ b`, not `bits(·)`; the two must not be conflated.
- Index 0 is the trap: a sorted pairwise fold (M_B, `merklization.tex:213–223`) yields a *balanced* tree, whereas M is a *key-prefix* trie — different depths, different root.
- Index 2 is wrong twice: M_R (`preamble.tex:190`) is the MMR **super-peak** function, and the belt is appended by A (`\fnmmrappend`), not M_R; and the state root is not what is appended to the belt.

**Blind summary (0-based indices): n1=2, n2=1, n3=3, n4=0, n5=2, n6=3, n7=1, n8=2, n9=1, n10=3.**

---

## PHASE 2 — AUDIT against `items/c3_ch09_appD.py`

**Answer keys: 10 / 10 agree with my blind verdicts. No MISMATCH.**

| n | id | key | mine | verdict |
|---|----|-----|------|---------|
| 1 | c3-ch09-expunge-delay | 2 | 2 | EXPLANATION-DEFECT ×2 (low) |
| 2 | c3-ch09-service-info-leaf | 1 | 1 | EXPLANATION-DEFECT (low, stem) |
| 3 | c3-ch09-write-threshold-go | 3 | 3 | **OK** |
| 4 | c3-ch09-forget-lifecycle | 0 | 0 | AMBIGUOUS (med) |
| 5 | c3-ch09-new-service-index | 2 | 2 | EXPLANATION-DEFECT (low, gpRef) |
| 6 | c3-ch09-privilege-mutation | 3 | 3 | **OK** |
| 7 | c3-appD-key-31-octets | 1 | 1 | **OK** |
| 8 | c3-appD-service-subkeys | 2 | 2 | EXPLANATION-DEFECT (low) |
| 9 | c3-appD-rho-guarantee | 1 | 1 | EXPLANATION-DEFECT (**med-high**) |
| 10 | c3-appD-merklize-bitorder | 3 | 3 | EXPLANATION-DEFECT (**med**) |

### Adjudication of the five flagged claims

**(1) Account field set — the item's "derived not serialized" assertion is correct as far as it goes, but the stem overstates it.**
eq. 9.3 (`accounts.tex:12–27`) stores exactly: `a_s, a_p, a_l, a_f, a_c, a_b, a_g, a_m, a_r, a_a, a_p(parent)`.
(`preamble.tex:569–579`: s=storage, p=preimages, l=requests, f=gratis, c=codehash, b=balance, g=minaccgas, m=minmemogas, r=created, a=lastacc, p=parent.)
`a_i, a_o, a_t` (`preamble.tex:581–583`) are **not** in the tuple — correct. But §9.3 itself says a_i/a_o *"are expected to be found explicitly within the Merklized state data"*, and the C(255,s) row proves it: **a_i and a_o are serialized; a_t is not**. So "derived" ≠ "absent from state". The item gets this exactly right in option 1; only the stem's throwaway "purely from a_s and a_l" is loose (see F-2a). Nothing else the items name is misattributed — I checked every field against `accounts.tex`.

**(2) Expunge delay + the 4-state lifecycle — correct; the `[]` case is genuinely under-specified in the GP.** See F-4a. D = 19,200 and its rationale are right (F-1a/F-1b are citation/naming nits only).

**(3) Storage-item footprint — settled from the .tex: `34 + |k| + |v|`, not `34 + |v|`.**
`accounts.tex:148` (eq. 9.8): `+ \sum\limits_{\tup{x, y} \in \mathbf{a}_\sa¬storage} 34 + \len{y} + \len{x}` — the sum ranges over **pairs** (x=key, y=value) and adds **both** lengths. The key is charged even though the trie stores only `H(E_4(2^32−1) ⌢ k)`. The item's key (option 3) and the Go excerpt both match. **The item is right; nothing to fix.**

**(4) State-key construction — quoted exactly right.**
`merklization.tex:15`: `(s, h) ↦ [n_0, a_0, n_1, a_1, n_2, a_2, n_3, a_3, a_4, a_5, …, a_26]  where n = E_4(s), a = H(h)`. 8 interleaved + a_4…a_26 (23) = **31**.
Why 31 and not 32: `merklization.tex:128–136` — 512-bit node = 1 header octet + 31 key + 32 value/H(v). Both items (7 and 8) state this correctly.

**(5) ρ's C(10) row carrying the full guarantee — the delta is REAL.**
0.8.0 content verified: `merklization.tex:52–58` (`C(10) ↦ E([?(⟨g, E_4(t)⟩)])`), `reporting_assurance.tex:16–24` (eq. 11.1 `ρ ∈ ⟦(g ∈ G, t ∈ N_T)?⟧_C`), eq. 11.24 for G, `serialization.tex:243–247` for E(G) including the credential.
The *change* claim is corroborated independently of the item by `/root/work/jam/research/ecosystem-notes.md:377–378, 613–614`: GP 0.8.0 PR **#494 "Keep full guarantees in availability assignments state (rho)"**, motivated by needing the guarantors for direct bundle fetch and for constructing a disputes extrinsic. **DELTA is correct — not a DELTA-DEFECT.** Likewise item 6's delta (PR #519 "Restrict bless to manager service", 0.8.0; "Owned Privileges" #475 landed in 0.7.1) is corroborated at `ecosystem-notes.md:394–395, 608, 613`. **No DELTA-DEFECT anywhere in this batch.**

### Code items — Go excerpts verified against `/root/work/jam/team-repo/`

- **n=3** caption `PVM/host_call_general.go (write) + internal/service_account/service_account.go:207 (CalcStorageItemfootprint)`:
  `internal/service_account/service_account.go:207–209` is **verbatim** `func CalcStorageItemfootprint(...) { return 1, 34 + types.U64(len(storageRawKey)) + types.U64(len(storageData)) }` — line number exact. The write excerpt is a faithful condensation of `PVM/host_call_general.go:769–792` (the real file's comment there even reads *"check a_t > a_b first (GP: a_minbalance > a_balance → FULL, s' = s)"*). `CalcThresholdBalance` exists at `service_account.go:185`. ✔
- **n=10** caption `internal/utilities/merklization/merklization.go (partitionByBit, merklizeWithCache)`:
  `partitionByBit` at lines 44–55 and `merklizeWithCache` at 76–93 are **verbatim** (only comments/blank lines dropped). `LeafHashCache` is declared in `internal/utilities/merklization/merklization_with_cache.go:10`; `key_level_cache.go` exists at `internal/blockchain/key_level_cache.go`. ✔
- Team issue/fuzz references also check out against `/root/work/jam/research/issues-digest.md`: #979/#980 (write mutates StorageDict before the balance check; *"Detected by jam-conformance fuzzer seed 3785638964 step 15419"*, line 287) and #779/#780 (*"failed to decode expected service info from state key 0xffff0017…: EOF"*, lines 273/301). JIP-4's *"Each key is a 62-character hex string defining the 31-byte state key"* is corroborated at `ecosystem-notes.md:183`. ✔

---

## FINDINGS

### F-9a — `c3-appD-rho-guarantee` — EXPLANATION-DEFECT (stale / wrong 0.8.0 symbols) — **med-high**
The explanation writes the guarantee set as `G ≡ (w ∈ W, t ∈ N_T, a ∈ ⟦(N, E)⟧_{2:3})`. Three symbols are wrong against the 0.8.0 table, and two of them are *live symbols with different meanings*:
- work-report **field** is `r`, not `w` — `preamble.tex:520` `\g¬workreport = \¬workreport`, `preamble.tex:447` `\¬workreport = \mathbf{r}`. Rendered eq. 11.24: `G ≡ (r ∈ R, t ∈ N_T, a ∈ ⟦(N, V̄)⟧_{2∶3})`.
- work-report **set** is `R` (`preamble.tex:506` `\workreport = \mathbb{R}`). In 0.8.0 **`W` is the work-ITEM set** (`preamble.tex:495` `\workitem = \mathbb{W}`).
- Ed25519 signature set is **`V̄`** (`preamble.tex:384–385`). In 0.8.0 **`E` is the extrinsic** (`preamble.tex:684`) and **`𝔼` is the work-error set** (`preamble.tex:357`).
Memorising "w ∈ W" for a work-report is precisely the 0.7.x habit an examiner will test.

**Fix** — replace this exact substring in `items/c3_ch09_appD.py`:
```
G ≡ (w ∈ W, t ∈ N_T, a ∈ ⟦(N, E)⟧_{2:3})
```
with:
```
G ≡ (r ∈ R, t ∈ N_T, a ∈ ⟦(N, V̄)⟧_{2:3})（eq. 11.24；0.8.0 的 R 是 work-report 集合、W 是 work-item 集合、V̄ 是 Ed25519 簽章集合）
```

**Secondary fix (same item, option index 1)** — the correct option names the field `w`. Replace:
```
(w work-report, t timeslot
```
with:
```
(r work-report, t timeslot
```
(Does not change which option is correct.)

**Optional nit (same item, low):** the option and trap invent `a_g` / `a_t` for ρ's fields. The GP writes them bare (`⟨g, E_4(t)⟩` in the C(10) row; `ρ[c]_g`, `ρ[c]_t`), and `a_t` already means *threshold balance* in items 2 and 3 of this same batch. Consider `⟨g, E_4(t)⟩` / `ρ[c]_g`, `ρ[c]_t` throughout this item.

### F-10a — `c3-appD-merklize-bitorder` — EXPLANATION-DEFECT (false statement + 0.7.x leftover) — **med**
The explanation says the sorted-pairwise fold "是 M_B / 附錄 E 的做法，**用在 extrinsic 與 segment root**". Both examples are wrong in 0.8.0:
- **segment root** uses the *constant-depth* function `M` (`\fnmerklizecd`), not `M_B`: `work_packages_and_reports.tex:302` `\is{\as¬segroot}{\merklizecd{\mathbf{s}}}`.
- **extrinsic hash** is not a Merkle tree at all in 0.8.0: `header.tex:27–28` (rendered eq. 5.4) `H_X ≡ H(E(H^#(a)))` — Blake2b of the encoding of the sequence of component hashes. (0.8.0 PR #524 changed this definition; the M_B framing is a 0.7.x holdover — `ecosystem-notes.md:613–614`.)
- `M_B` *is* used for the accumulation-output root — `recent_history.tex:32` `β_B' ≡ A(β_B, M_B(s, keccak), keccak)` — and for the **erasure root** — `work_packages_and_reports.tex:308` `\as¬erasureroot = \merklizewb{…}`.

**Fix** — replace this exact substring:
```
用在 extrinsic 與 segment root
```
with:
```
用在 accumulation-output log 每區塊的 root（β_B′ ≡ A(β_B, M_B(s, keccak), keccak)）與 work-package 的 erasure root；segment root 用的是定深的 M（\mathcal{M}），而 0.8.0 的 extrinsic hash 根本不是 Merkle 樹：H_X ≡ H(E(H^#(a)))
```

### F-4a — `c3-ch09-forget-lifecycle` — AMBIGUOUS — **med**
The key (option 0) says `[]` is dropped **with no age condition**, while `[x, y]` is dropped **only once `y < t − D`**. The GP writes both shapes under **one** guard (`pvm_invocations.tex:987`):
`… when (x_s)_l[h,z] ∈ {[], [x,y]}, y < t − D`
— in the `[]` shape nothing binds `y`, so the age test is vacuous/undefined there. Two readings exist:
- (a) `[]` drops immediately (the key's reading, and the only implementable one — otherwise a service could never cancel a solicit that was never filled, and `[]` would be permanently stuck);
- (b) a literal reading in which the `[]` branch is simply undefined.
I could **not** find any passage in `accounts.tex`, `pvm_invocations.tex` or `definitions.tex` that resolves this explicitly — stating that plainly rather than pretending the GP settles it. The key is still the best answer (no other option is defensible), so this is AMBIGUOUS, not MISMATCH.
The concrete defect is that the **explanation contradicts its own key**: it reproduces the guard literally as "當 a_l[(h,z)] ∈ {[], [x,y]} **且** y < t − D", attaching the delay to `[]` as well.

**Fix** — replace this exact substring:
```
當 a_l[(h,z)] ∈ {[], [x,y]} 且 y < t − D
```
with:
```
當 a_l[(h,z)] ∈ {[], [x,y]} 且 y < t − D（GP 把兩種形狀寫在同一條 guard 裡，但 y 只在 [x, y] 這一支有綁定，所以 D 的等待期實際只約束 [x, y]；[] 是「已請求、從未供應」，直接刪除——否則 solicit 之後就永遠取消不掉。這一點 GP 並未明文釐清，是 0.8.0 已知的 under-specification）
```

### F-1a — `c3-ch09-expunge-delay` — EXPLANATION-DEFECT (placeholder citation) — **low**
The explanation cites "（eq. 12.x）" for ξ. The real reference is **eq. 12.1**: `accumulation.tex:27–28` `ξ ∈ ⟦{H}⟧_E` with the prose *"This history, ξ, is sufficiently large for an epoch worth of work-reports."* (rendered `gp-raw.txt:3544–3547`). The substantive claim (ξ holds one epoch, so the "32 epochs" distractor's premise is false) is correct.

**Fix** — replace `eq. 12.x` with `eq. 12.1`.

### F-1b — `c3-ch09-expunge-delay` trap — EXPLANATION-DEFECT (collides with a real 0.8.0 host call) — **low-med**
The trap says "**expunge 的實際動作**在 `forget`（自家）與 `eject`（別家）兩個 host call 裡". GP 0.8.0 has a host call **literally named `expunge` (Ω_X = 14)**, defined at `pvm_invocations.tex:704–716` with `CgasX = 335` (`definitions.tex:340`) — it is a **refine-only inner-PVM teardown** (`⟨φ'_7, m'⟩ ≡ ⟨WHO, m⟩ when n ∉ K(m); ⟨m[n]_pc, m \ n⟩ otherwise`) and has nothing whatever to do with preimages. A candidate who memorises this trap will answer "expunge" when asked which host call removes a preimage.

**Fix** — replace this exact substring:
```
expunge 的實際動作在 `forget`（自家）與 `eject`（別家）兩個 host call 裡
```
with:
```
真正把 preimage 從 state 移除的動作在 `forget`（自家，Ω_F = 25）與 `eject`（別家，Ω_J = 22）兩個 accumulate host call 裡——注意別跟 0.8.0 的 `expunge`（Ω_X = 14）混淆，那是 refine-only 的 inner-PVM 拆除呼叫，與 preimage 無關
```

### F-2a — `c3-ch09-service-info-leaf` stem — EXPLANATION-DEFECT (over-simplification) — **low**
Stem: "§9.3 defines them purely from a_s and a_l". True for a_i and a_o; **false for a_t**, which also reads the *stored* gratis field a_f: `accounts.tex:149–156` (eq. 9.8) `a_t ≡ max(0, B_S + B_I·a_i + B_L·a_o − a_f)`. A candidate could walk away believing a_t is independent of the gratis offset — the exact thing item 6 tests from the other side.

**Fix** — replace this exact substring:
```
§9.3 defines them purely from a_s and a_l
```
with:
```
§9.3 derives a_i and a_o from a_s and a_l, and a_t from those two plus the stored gratis offset a_f
```

*Non-defect note (checked, no change needed):* calling the leading `0` of C(255,s) a "version octet" is not 0.8.0 text — the GP just writes `0` — but the name is legitimate: the GP 0.7.1 release notes list *"version byte for accounts"* (`ecosystem-notes.md:608`). Leaving as-is.

### F-5a — `c3-ch09-new-service-index` gpRef — EXPLANATION-DEFECT (wrong cross-reference) — **low**
gpRef reads `§9.1 (N_S ≡ N_{2^32})`. `N_S ≡ N_{2^32}` is **eq. 9.1, in the §9 preamble**; **§9.1 is "Code and Gas"** (`gp-raw.txt:2245` prints `(9.1)` well before the `9.1. Code and Gas` heading; in the source, `accounts.tex:7` `\serviceid \equiv \Nbits{32}` sits in the section preamble, above `\subsection{Code and Gas}` at `accounts.tex:38`). The other two refs in that gpRef are correct: **eq. B.14 is `check`** (`gp-raw.txt:12928–12929`) and `S = 2^16` (`definitions.tex:281`).

**Fix** — replace this exact substring:
```
§9.1 (N_S ≡ N_{2^32})
```
with:
```
§9 eq. 9.1 (N_S ≡ N_{2^32})
```

### F-8a — `c3-appD-service-subkeys` — EXPLANATION-DEFECT (non-sequitur) — **low**
"…而 0.8.0（PR #520）已把 preimage 長度收進 N_L ≡ N_{2^32}，實務上 preimage 遠小於 4 GiB，**所以安全**。" `N_L ≡ N_{2^32}` = {0 … 2^32−1} (`notation.tex:57`) still **contains** both reserved marker values 2^32−1 and 2^32−2, so the type restriction does not remove the collision — only the practical size bound does. As written it implies the bound is formal.

**Fix** — replace this exact substring:
```
已把 preimage 長度收進 N_L ≡ N_{2^32}
```
with:
```
已把 preimage 長度收進 N_L ≡ N_{2^32}（注意這個型別**仍然包含** 2^32−1 與 2^32−2 兩個保留值，形式上並未排除碰撞，靠的是實務尺寸）
```

---

## OK items (nothing wrong found)

- **n=3 `c3-ch09-write-threshold-go`** — key, eq. 9.8 quotation, the `⟨continue, FULL, s⟩` quotation, the FULL-vs-CASH trap (verified: Ω_W `pvm_invocations.tex:492` and Ω_S `:965` → FULL; Ω_T `:885` and Ω_N `:836` → CASH), the Go excerpt, the file path **and line number**, and the fuzzer-bug provenance all check out.
- **n=6 `c3-ch09-privilege-mutation`** — every clause verified, including the symbols: `x_s` for the caller (`preamble.tex:462` `\im¬id = s`) and **`(x_e)` for the partial state** (`preamble.tex:463` `\im¬state = \¬partialstate`, `:438` `= \mathbf{e}`). These are current 0.8.0 symbols, **not** stale. Ω_B's tuple order `(χ_M, χ_A, χ_V, χ_R, χ_Z)` in the key matches the host call (and C(12) in T(σ)); eq. 9.9's abstract order is `(χ_M, χ_V, χ_R, χ_A, χ_Z)` — the option is describing Ω_B, so it is right as written.
- **n=7 `c3-appD-key-31-octets`** — quotation exact; the JIP-4 62-hex-char trap corroborated.

**Count marked OK: 3 of 10.** The other 7 keep their (correct) answer key; only explanation/stem/gpRef text needs the fixes above.

**Severity roll-up:** 0 MISMATCH · 0 DELTA-DEFECT · 1 AMBIGUOUS (n=4) · 7 EXPLANATION-DEFECTs across 6 items (2 of them substantive: F-9a, F-10a).
