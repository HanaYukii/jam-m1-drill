# JAM ecosystem research notes (public sources) — for M1 examination-interview prep

Compiled 2026-08-25 from public web sources (WebSearch + WebFetch only; ~50 searches, ~140 page fetches).
Gray Paper (GP) current version: **0.8.0, released 3 June 2026** (github.com/gavofyork/graypaper/releases/tag/v0.8.0).

Conventions: "GP" = Gray Paper. Quotes are verbatim from the cited page unless marked *(paraphrase)*. Where a number
came through a summarising fetch and could not be re-verified against the LaTeX source it is marked **[verify]**.

> **Headline on examination notes (section A.6):** No published M1 examination transcript, question list or
> grading report was found anywhere public. What *is* public: (1) rule 12 / T&C 6.1 (interview clause), (2) the
> milestone-delivery template clause "we agree to a recorded interview by the Polkadot Technical Fellowship",
> (3) the observable three-stage M1 pipeline in the w3f/jam-milestone-delivery PRs (W3F 1M-step fuzz audit ->
> Parity Technologies audit -> Fellowship interview), and (4) four Fellowship referenda (#595–#598, 20 Aug 2026)
> titled "M1 interview approval <TEAM>" whose on-chain remark reads "The Polkadot Technical Fellowship approves
> **in full** JAM Prize Milestone 1 for team …" — the "in full" wording is consistent with graded outcomes
> (rule 12: "INABILITY TO PROVE THIS EXPERTISE MAY RESULT IN A REDUCED PRIZE OR FULL DISQUALIFICATION").
> Gavin Wood's August 2026 PSA (chapters 3–13 + appendices; three extra portions: architecture, design rationale,
> PVM/other appendix; P/M/D/U/F grading) was described by the requester; it lives in the #jam:polkadot.io Matrix
> room, whose public archive page (paritytech.github.io/matrix-archiver) is a single ~2-year page that the fetcher
> truncates at July 2024, so the PSA text itself could not be retrieved here.

---

## A. The JAM Prize

### A.1 Official prize page — jam.web3.foundation (https://jam.web3.foundation/)

- "The Web3 Foundation is offering "a total prize pool of 10 million DOT and 100,000 KSM" to support JAM client
  implementations." "JAM is the Join-Accumulate Machine, a new protocol designed to succeed the Polkadot relay chain."
- **Path 1 — Validating Node Path** (max "500,000 DOT + 5,000 KSM"), five milestones, each 100,000 DOT + 1,000 KSM:
  - **(M1) IMPORTER**: "State-transitioning conformance tests pass and can import blocks"
  - **(M2) AUTHORER**: "Fully conformant and can produce blocks (incl networking, off-chain)"
  - **(M3) HALF-SPEED**: "Conformance and 50% of required performance (including PVM impl)"
  - **(M4) FULL-SPEED**: "Conformance and 100% of required performance (including PVM impl)"
  - **(M5) SECURE**: "Fully audited"
- **Path 2 — Non-PVM Validating Node Path** (max "350,000 DOT and 3,500 KSM"): MN1–MN5, same M1 baseline; "Only half of
  the regular milestone prizes are paid for this path's Milestones 3, 4 and 5." Option for an additional
  "100,000 DOT + 1,000 KSM" on later submitting a full PVM implementation.
- **Path 3 — Light-Node Path** (max "250,000 DOT and 2,500 KSM"): ML1 IMPORTER (100k DOT + 1k KSM), ML2 FULL-SPEED
  ("Conformance and 100% of required performance", 50k DOT + 500 KSM), ML3 SECURE ("Fully audited", 100k DOT + 1k KSM).
  "4 ML2 payments are reserved in each language group"; "Exactly 2 ML3 payments are available in each language group."
- **Language sets** (verbatim from the page table):
  - Set A "Company code": Java, AspectJ, Kotlin, C#, Go
  - Set B "Native code": C, C++, D, Rust, Swift, Zig, Carbon, Fortran
  - Set C "Concise code": Scheme, Common Lisp, Prolog, Haskell, ML, Perl, Python, Ruby, Javascript, Groovy, Dart
  - Set D "Correct code": Ada, Julia, Erlang/Elixir, Ocaml, Smalltalk, F#, Scala, APL
  - Set Z "Mad": Brainfuck, Whitespace, Minecraft Red-stone — "Maximum prize per milestone … 5,000 KSM"
  - Sets A–D: "Maximum prize per milestone (dependent on path and judgment): 100,000 DOT + 1,000 KSM"
  - Per Gav's HackMD notes: each of sets A–D has a pot of 2,500,000 DOT + 20,000 KSM; set Z only 20,000 KSM.
- Other page text: "Third-party libraries permitted": "cryptographic primitives (erasure-coding, Bandersnatch, Ed25519),
  binary codec, databases, low-level networking stack". "Members of the Polkadot Fellowship will judge submissions".
  "Following the accepted completion of each milestone, one developer may be promoted to the rank commensurate with
  their code and protocol contributions" (up to III Dan). "Cooperation between teams is essential but anything which
  goes beyond trivial misunderstandings of the graypaper should be documented".
- Links: Rules https://jam.web3.foundation/rules · Milestone delivery https://github.com/w3f/jam-milestone-delivery ·
  Contact jam@web3.foundation.

### A.2 The 30 rules — https://jam.web3.foundation/rules (verbatim)

1. "Third-party libraries for cryptographic primitives (erasure-coding, Bandersnatch, Ed25519), codecs (e.g. SCALE), and networking (e.g. QUIC) are acceptable."
2. "Only languages defined in one of the language sets are eligible for the prize."
3. "For languages not in the set, an application may be made, including the set you propose and arguments why that set is sensible and why the language is sufficiently different from the others to be valuable."
4. "Code must be idiomatic for languages which define idiom."
5. "Gas, trie/DB, signature-verification, and availability (EC/DB) performance tests are requirements and will be run on standard hardware (only applicable for paths 1 and 2)."
6. "Clean-room implementation using the Graypaper and public implementers' channel as the only resources. (Additional materials may be added here at a later stage.)"
7. "Any JAM-implementation code which is viewed before or during implementation must be declared."
8. "Relevant private (not in the public implementers' channel) conversations with other implementers must be declared and summarised in reports to the Fellowship."
9. "Generative AI must not be used in any substantive way."
10. "The prize may be reduced in case collusion may be sufficient to reduce network security."
11. "If concerned, then declarations may be stated up-front and the maximum reduction set; as long as declarations are accurate and no further collusion happens, then the reduction proportion will be the maximum."
12. **"An interview may be requested after submission to ensure team members are the legitimate authors of the code. This precludes the use of generative AI. The interview will seek to ensure the individual has definitive expertise on both the Graypaper and their own codebase. INABILITY TO PROVE THIS EXPERTISE MAY RESULT IN A REDUCED PRIZE OR FULL DISQUALIFICATION."**
13. "Following the accepted completion of each milestone, teams may nominate one Fellowship candidate/member to be promoted directly to rank III and (optionally) a second candidate/member to rank II …"
14. "A clear Git history and public, credibly timestamped commits are necessary in order to help evidence organic code development by the team/s."
15. "Timestamps may be by virtue of pushing code to GitHub on a timely basis."
16. "For code developed in private, commit hashes should be placed, in a timely fashion, on a major public blockchain and readily visible on a block explorer."
17. "Any individual may only be part of one team's prize-claim per milestone only. …"
18. "Apparent lack of originality, undeclared collusion, and suspected plagiarism may result in disqualification entirely at the discretion of the judges."
19. "Appeals may be made through a governance referendum on the Polkadot Wish For Change track, and the result will be respected by Polkadot Fellowship."
20. "Implementations must pass all relevant public and private conformance/performance tests. These will be shared in the near future."
21. "Prizes are paid no earlier than the ratification by the Polkadot Fellowship of version 1.0 of the JAM protocol. Payment … is conditional upon the successful completion of all KYC/AML processes."
22. "Prizes are paid to the earliest Polkadot/Kusama account IDs stated in the repository's README. In the case of a tie, payment is split equally. …"
23. "The prize pool is limited. Prizes will be awarded on a first-come, first-served basis, based on the order of valid submissions received. … Prize pools may be redistributed and reallocated if a pot is nearing depletion, subject to … (i) a 3-month notice period … (ii) no more than 25% of the prize pool may be scheduled for redistribution at any one time."
24. "Each team is only allowed to work on one implementation."
25. IP warranty / employer-IP advice (long clause).
26. "The repository must be public and include a clear and permissive open-source license." *(Note: PR threads from Feb 2026 show rule 26 was amended so that a private repo with reviewer access + permissive licence is acceptable — see A.5; JamZig and JAM DUNA reverted to private "in accordance with the updated Rule 26".)*
27. "The prize will be paid out in the form of 25% unlocked and 75% locked DOTs with a two-year linear vesting via the on-chain vesting module."
28. "One full milestone prize (100,000 DOT + 1,000 KSM) will be reserved for Milestone 5 (M5) in each language set; two full milestone prizes for M4 in each language set, three full milestone prizes for M3, four full milestone prizes for M2."
29. "The language set of an implementation is determined as the language in which its business logic is written. Peripheral, performance-bottleneck components of an implementation may be written in a higher-performance language without any impact on the consideration of the language set. A non-exhaustive list of such components includes: PVM, Database, Erasure (de-)coding."
30. "Additional or modified rules may apply as specified in the documentation relevant for specific paths."

### A.3 JAM Prize Terms & Conditions (Updated February 2026) — https://raw.githubusercontent.com/w3f/jam-milestone-delivery/main/docs/T%26Cs.md

Key clauses (verbatim):
- 3.5 "Submissions must be conformant to the latest Graypaper release. Conformance is assessed against the latest release in effect at the time of the Foundation's evaluation." (If GP updates while awaiting review, "the Participant must promptly modify its Submission".)
- 4.2 "Clean-room implementation using the Graypaper and public implementor chat channels as the only resource is mandatory."
- 4.5 "Implementations must pass all relevant public and private conformance/performance tests."
- **6.1 "An interview may be requested by the Foundation after the submission is made to provide further clarifications regarding the submission."**
- 6.2 rank III / rank II nominations after each accepted milestone.
- 7.1 Appeals via Wish-For-Change referendum "within two (2) weeks of receiving a decision".
- 8.1.1–8.1.5 First-come-first-served by "Submission Timestamp"; "Eligibility Thresholds"; a single **14-day "Cure Period"** for non-material deficiencies.
- 8.3 "at least 75% of the Prize … 'vested transfer' … vest linearly over a period of twenty-four (24) months".
- **8.4 "The Prize for all milestones (except milestone 1) of each 'Path to Implementation' will be awarded no earlier than the ratification by the Polkadot Fellowship of version 1.0 of the JAM protocol."** (i.e. M1 is payable before GP 1.0 — this was the Feb 2026 "early acceptance" change, PR #36 "introduce early acceptance T&Cs", https://github.com/w3f/jam-milestone-delivery/pull/36.)
- 9.3 Apache-2.0 or OSI-equivalent licence required.
- History: PR #16 (https://github.com/w3f/jam-milestone-delivery/pull/16) — gavofyork (Jan 21 2026): "Candidates must target the latest version at time of submission…Not sure if this is really clear when just '0.7' is written." koute: "it wouldn't make much sense to award the last milestone before JAM 1.0 is ready". koute on PR #36: "The only formal way of having the Fellowship as a whole to approve of something is … through a Fellowship Referenda."

### A.4 Milestone delivery process — https://github.com/w3f/jam-milestone-delivery

- README: KYC/KYB (Sumsub) before first submission; fork, create `deliveries/<project>/`, complete the template
  (`project_name-milestone_number.md`), open a PR; "Polkadot Fellows can (and usually do) issue questions, comments and
  may request changes on the pull request"; on approval an admin merges; invoice form for payment.
- **Template** (https://raw.githubusercontent.com/w3f/jam-milestone-delivery/main/deliveries/milestone-delivery-template.md) declaration checklist includes:
  - "we agree to a recorded interview by the *Polkadot Technical Fellowship* on any matter arising from this milestone submission."
  - "we understand that this milestone submission will need to be ratified with an on-chain remark by the *Polkadot Technical Fellowship* before it can be merged."
  - plus: KYC/KYB done; permissive licence; git history / timestamped commits; third-party libs used (crypto/codec/networking); perf tests provided (gas, trie/DB, sig-verification, EC/DB); JAM code viewed before/during; private conversations with implementers; collusion concerns; path + milestone; deliverables table with commit hashes.
- **Gav's Unofficial JAM Prize Notes** (https://hackmd.io/@polkadot/jamprize): "Judges: The Polkadot Fellowship, excluding members involved in the implementation being voted on." Advice: "Begin in order: 1. Block/header data structures and serialization 2. State data structures and serialization 3. In-memory DB and Merklization 4. Non-PVM block execution/state-transition 5. PVM instancing, execution and host-functions 6. Block-import tests". FAQ "Clean room?": "…anything which goes beyond trivial misunderstandings of the graypaper should be documented, either as issues in the GP repo or as side notes of the implementation to be submitted at the time of milestone review." "Code which appears to be a little too similar for it to have been independently written" is a concern, "the same bug popping up in two implementations" especially. FAQ: "Does my implementation need to exploit JAM's asynchrony?" — "It is up to implementations to decide this for themselves."

### A.5 The observable M1 evaluation pipeline (from the PR threads, Dec 2025 – Aug 2026)

Stage 1 — **W3F conformance fuzzing ("the 1 million steps benchmark")**, run by W3F staff (GitHub: PieWol, CrackTheCode016, midegdugarova, semuelle) against the team's fuzz target (Docker image / binary speaking the jam-conformance fuzz protocol, GP 0.7.2). Typical wording: "Your target managed to complete 1 million steps successfully!" (TSJam, Jan 29 2026); "Your target passed 10 consecutive runs at 100k steps each." (Jamixir, Mar 2 2026); "JamZig passed the m1 conformance testing. I just pushed the results of the last 10 runs, each correctly processing 100k steps." (Feb 16 2026). Failures come with "2-week grace period starts now" (SpaceJam, Jampy). Results are pushed to branches of w3f/jam-conformance (e.g. `fuzz-reports/0.7.2`). W3F then checks "all other rules of the JamPrize" and applies the `fellowship review` label.

Stage 2 — **Parity Technologies audit** (content not public). PyJAMaz: "now also passed the Parity Technologies Audit on 23 May 2026"; Jamixir: "we also passed the Parity's conformance tests" (May 26 2026). Related: jam-conformance discussion "Standardizing Target Packaging and Entry Points (Docker-based Submission)" (davxy, Apr 27 2026) and the `std` label on per-team issues; JamForge posted a jamtoaster attestation (May 25 2026) https://fuzz.jamtoaster.network/attestation/0x6f18f3cb….

Stage 3 — **Fellowship review = recorded interview/examination**, followed by an on-chain Fellowship referendum (Fellows track) with a `System.remark`. PyJAMaz: "Yesterday our team's M1 Submission passed the final hurdle of the Fellowship review" (emielsebastiaan, Aug 8 2026); Polkadot Forum digest 2026-08-09: "JAMdotTech passed the Fellowship interview for JAM Prize Milestone 1 after 25 months of work" (https://forum.polkadot.network/t/polkadot-socials-daily-digest-2026-08-09/18378). On Aug 18 2026 the `fellowship review` label was removed from many PRs (Jampy, JamZig, TSJam, JavaJAM, JamForge, Jamzilla, SpaceJam) — consistent with the review round being processed.

**Fellowship referenda (collectives.subsquare.io, all created 20 Aug 2026 by a rank-6 "Grand Architect" account 13fv…22E7, all "Deciding" with 13–14 ayes / 0 nays on 25 Aug):**
- #595 "M1 Interview Approval PyJAMaz" — remark: "The Polkadot Technical Fellowship approves in full JAM Prize Milestone 1 for team PYJAMAZ in category Python (Set C), address 146CmUoArEi1E2AogKCU5gkhBSN6BLDzxecFSCDAgVyEshra and DBPAKp9B2gpBr9YmvqXyewYkR4ZwTn9uJDt64zGcVjZeiGi." (https://collectives.subsquare.io/fellowship/referenda/595)
- #596 "M1 interview approval JAMBRAINS" — "…team JAMBRAINS in category Elixir (Set D)…" (JamBrains' client is **graymatter**; delivery file `graymatter-milestone_1.md`; team franciscoaguirre, kianenigma, ggwpez) (…/596)
- #597 "M1 interview approval TYPEBERRY" — "…team TYPEBERRY in category Typescript/Assembly script (Set C)…" (…/597)
- #598 "M1 interview approval JAMZIG" — "…team JAMZIG in category Zig (Set B)…" (…/598)
- API (JSON) endpoints used: https://collectives.subsquare.io/api/fellowship/referenda/595 (…/596, /597, /598). No comments on any of them.

**M1 submissions found in w3f/jam-milestone-delivery (PR#, team, language, opened, status as of 25 Aug 2026):**
| PR | Team / client | Lang | Opened | Public status |
|---|---|---|---|---|
| #5 | UniversalDot | Rust | Oct 6 2024 | closed ("doesn't seem to implement the jam spec") |
| #11 | UniversalDot | Rust | Jan 30 2025 | closed Jan 6 2026 ("Was this work primarily performed with generative AI?") |
| #12 | JamZig (boymaas) | Zig | Jun 28 2025 | fuzz passed Feb 16 2026; fellowship review; **ref #598** |
| #13 | SpaceJam (clearloop) | Rust | Jun 29 2025 | "SpaceJam passed one million steps" Feb 16 2026; fellowship review |
| #15 | Jampy (dakk) | Python | Aug 26 2025 | "passed 1 million steps!" Mar 17 2026; fellowship review |
| #18 | JamForge (philoniare) | Scala | Dec 17 2025 | 25.85% → 50.95% (Mar 2026); team-posted jamtoaster attestation May 25 2026 |
| #19 | TSJam (vekexasia) | TypeScript | Dec 17 2025 | 1M steps Jan 29 2026; fellowship review |
| #20 | PyJAMaz (JAMdot Technologies) | Python | Dec 17 2025 | W3F Feb 10; Parity May 23; **Fellowship passed Aug 7 2026; ref #595** |
| #21 | JavaJAM (jaymansfield) | Java | Dec 17 2025 | 1M steps Feb 9 2026; fellowship review |
| #22 | JAM DUNA (sourabhniyogi) | Go | Dec 18 2025 | private repo per amended rule 26; binary v0.7.2.15; no public result |
| #23 | Jamixir (danicuki, daiagi) | Elixir | Dec 19 2025 | W3F Mar 2 2026; Parity May 26 2026 |
| #24 | Jamzilla (ascrivener) | Go | Dec 19 2025 | "we might adjust the evaluation process a bit" (Mar 3 2026) |
| #25 | PeanutButterAndJAM (mikirov/Esscrypt) | TypeScript | Dec 19 2025 | no public result |
| #26 | Vinwolf (bloppan) | Rust | Dec 22 2025 | no public result |
| #27 | Boka (xlc / Laminar/Acala) | Swift | Dec 23 2025 | no public result |
| #28 | New JAMneration (YCC3741) | Go | Dec 28 2025 | no public result |
| #29 | typeberry (tomusdrw / Fluffy Labs) | TypeScript | Dec 31 2025 | **ref #597** |
| #30 | FastRoll (0xjunha) | Rust | Jan 12 2026 | no public result |
| #31 | JamBrains / graymatter | Elixir | Jan 16 2026 | **ref #596** |
| #32 | Jam4s | Scala | Jan 23 2026 | no public result |
| #33 | Tessera (Chainscore) | Python | Jan 23 2026 | no public result |
| #34 | Strawberry (Eiger/equilibriumco) | Go | Jan 29 2026 | no public result (README says M1 first submitted Nov 20 2024) |
| #40 | TurboJAM (sierkov / r2rationality) | C++ | Feb 10 2026 | no public result |
| #41 | Gossamer-Jam (ChainSafe) | Go | Feb 12 2026 | no public result |
| #42 | JOTL (polykrate, "Jam on the Lisp") | Common Lisp | Mar 4 2026 | no public result |
| #43 | Jambda (libingjiang47 / ArcheLabs) | ? | Mar 12 2026 | no public result |
| #44 | lasair (abutlabs) | ? | Jun 13 2026 | no public result |
(#1–#3, #10, #14, #16, #17, #35–#39 are admin PRs/issues; #45+ do not exist as of fetch.)

Context on delays: Forum thread "What is the status of JAM development?" (https://forum.polkadot.network/t/what-is-the-status-of-jam-development/17368): ~15 teams submitted M1; "payments aren't tied to submission alone - they only happen after the protocol gets properly ratified" (Mar 2026, later changed for M1 by T&C 8.4); "the Gray Paper evolved through '0.7.x line into 0.8'"; "team roster shrunk from 43 to 15". Polkadot Cloud blog "Inside the JAM Implementers Prize — 43 Teams, 15 Submissions, and the Road to JAM 1.0" (Mar 25 2026, https://polkadot.cloud/blog/en/polkadot-jam-implementers-prize — body not fetchable). Bitget/PolkaWorld interview (https://www.bitget.com/news/detail/12560605055985): 0xjunha: M1 = "a node client that can 'correctly import blocks'"; review uses "the JAM Conformance Fuzzer, which can automatically generate many blocks with random data and test whether each implementation can produce the same state root"; a "Gray Paper Editorial Committee … led by Gavin Wood, will collectively decide JAM protocol updates, priorities, and key decisions".

Ratification framework: Polkadot referendum 682 "Proposal for JAM Ratification, Conformance, Performance by Polkadot Fellows" (https://polkadot.subsquare.io/referenda/682): Fellows to ratify the final protocol and define conformance & performance tests; before the relay chain halts: independent professional audit of the spec, **three independent viable block-producing implementations**, all passing published conformance/performance tests, system parachains ready. Passed ~31.3M DOT aye.

### A.6 Search for published examination notes — result: none found

Searched (among others): "JAM Prize M1 examination", "JAM M1 interview notes", "jam prize examination notes", "graypaper examination", "JAM implementers interview", "jam prize interview recording", "Gray Paper Editorial Board", "M1 interview approval", "Fellowship interview JAM", P/M/D/U/F & pass/merit/distinction phrasing, site-restricted searches of GitHub/Forum/X, plus the #jam, #graypaper and #jam-conformance Matrix archives (paritytech.github.io/matrix-archiver — the #jam page is one file spanning 2024-04-20 → 2026-08-25; the fetch tool only returns the first ~3 months, and direct curl to *.github.io is blocked by the sandbox proxy policy). No transcript, question list, or grading report is public. Only indirect evidence exists (A.5). Team self-reports found: JAMdotTech's X post (https://x.com/JAMdotTech/status/2085878035077628061 — not fetchable) and PR #20 comment; the JamZig delivery doc's remark "Achieving graypaper conformance proved revelatory—precision at the bit-and-byte level demands rigorous discipline."

Practical inference for prep: the examination is per rule 12 an authorship + expertise check on *both* the Gray Paper and the team's own code; the delivery template makes it a *recorded* interview; results are ratified by a Fellows-track referendum whose remark records approval "in full" (so partial approval is presumably possible).

---

## B. JIPs — JAM Improvement Proposals (https://github.com/polkadot-fellows/JIPs)

Repo root lists JIP-1.md … JIP-5.md (26 stars, 81 commits at fetch). README index text (verbatim one-liners):

- **JIP-1: Debug message host call** — "A host call for passing a debugging message from the service/authorizer to the hosting environment for logging to the node operator." Spec: host-call **index 100, name `log`, gas cost 10**; inputs in registers φ7…φ11: level, target (ptr,len), message (ptr,len); output φ'7 = always `WHAT` (so behaviour is identical whether or not the node supports it; memory-access failure has no consequence). Levels: 0 fatal, 1 warning, 2 important, 3 helpful, 4 pedantic. Console format `<YYYY-MM-DD hh-mm-ss> <LEVEL>[@<CORE>]?[#<SERVICE_ID>]? [<TARGET>]? <MESSAGE>`; JSON alternative with time/level/message/target/service/core. (Test vectors' traces assume `log` costs 0 gas per JIP-1 — see C.1.)
- **JIP-2: Node RPC** — "RPC specification for JAM nodes to ensure JAM tooling which relies on being an RPC client is implementation-agnostic." JSON-RPC 2.0 over WebSockets, "typically on port 19800"; the spec says "RPCs are evil" (centralising) but are an interim solution until light clients. Encoding: Blob = base64 (RFC 4648); Hash = base64 32 bytes; Block Descriptor = {header_hash, slot}. Errors: 1 block unavailable, 2 work-report unavailable, 3 DA segment unavailable, 0 other. Methods: `parameters()`, `bestBlock()`, `finalizedBlock()`, `parent(h)`, `stateRoot(h)`, `beefyRoot(h)`, `statistics(h)`, `serviceData(h,id)`, `serviceValue(h,id,key)`, `servicePreimage(h,id,hash)`, `serviceRequest(h,id,hash,len)`, `listServices(h)`, `submitWorkPackage(core, package, extrinsics)`, `submitWorkPackageBundle(core, bundle)`, `workPackageStatus(h, hash, anchor)` (Reportable/Reported/Ready/Failed), `workReport(hash)`, `fetchWorkPackageSegments(wp_hash, indices)` / `fetchSegments(segment_root, indices)` (4104-byte blobs), `syncState()`, `submitPreimage(requester, preimage)`; subscriptions `subscribeBestBlock`, `subscribeFinalizedBlock`, `subscribeStatistics(finalized)`, `subscribeServiceData/Value/Preimage/Request`, `subscribeWorkPackageStatus`, `subscribeSyncStatus`. Best-chain subscriptions "may yield 'impossible' sequences if forks switch".
- **JIP-3: Telemetry** — "Specification for JAM node telemetry allowing integration into JAM Tart (Testing, Analytics and Research Telemetry)." TCP to `--telemetry HOST:PORT`; each message prefixed by little-endian u32 length ("matching the JAMNP-S encoding"); JAM codec with fixed-width ints; handshake = node-info message (protocol version 1, JAM parameters, genesis hash, peer id, address, implementation info, flags); ~90 events with a timestamp + single-byte discriminator and event-id sequencing: meta (dropped events), status (peers, block state, sync), networking, block authoring/importing, distribution, Safrole tickets, guaranteeing, availability (shards/assurances), bundle recovery, segment recovery, preimage distribution. Open PR #15 (alxmirap, Aug 24 2026) "Adds events for the Audit section."
- **JIP-4: Chainspec file** — "A chain specification collects information that describes a JAM-based network." JSON fields: `id` ("the machine-readable identifier for the network"), `bootnodes` (`<name>@<ip>:<port>`, name = 53-char DNS id: letter "e" + base-32 Ed25519 pubkey), `genesis_header` ("A hex string containing JAM-serialized genesis block header"), `genesis_state` ("Each key is a 62-character hex string defining the 31-byte state key", hex values), `protocol_parameters` ("A hex string containing JAM-serialized protocol parameters" in the encoding of the `fetch` host call).
- **JIP-5: Secret key derivation** — "A standard method for deriving a set of validator secret keys from a 32-byte seed." Ed25519 secret = `blake2b("jam_val_key_ed25519" ++ seed)`; Bandersnatch secret seed = `blake2b("jam_val_key_bandersnatch" ++ seed)` (32-byte BLAKE2b; Bandersnatch per the VRF spec appendix A.1). `trivial_seed(i) = repeat_8_times(encode_as_32bit_le(i))` for dev validators; test vectors for i = 0..5 plus one arbitrary seed. (BLS keys not covered.) PR #2 by zdave-parity.
- **JIP-6: Program metadata** — PR #3 by zdave-parity (opened May 27 2025; approved by arkpar Dec 9 2025; fetch reports it as merged though no `JIP-6.md` shows in the root listing — **[verify]**). Standardises metadata attached to PVM program blobs (service/authorizer code); discussion (igankevich vs gavofyork) on whether the metadata length must be bounded so that "each implementation would [not] establish its own potentially ambiguous boundaries." Referenced by JAMdotTech/pyjamaz.
- **JIP-7: PVM Ecalli Trace** — PR #14 by tomusdrw (Mar 20 2026, open): a text-based IO-level (host-call level) PVM trace format with example traces from the STF storage vectors and a TypeScript parser/encoder; complements instruction-level tracing.

---

## C. Test vectors & conformance

### C.1 w3f/jamtestvectors (https://github.com/w3f/jamtestvectors; CC0-1.0)

- README title: "Test Vectors for the JAM Protocol (0.7.1)" (master branch; no `0.8.0` branch existed at fetch time —
  raw.githubusercontent.com/w3f/jamtestvectors/0.8.0/README.md → 404). Classes: Codec, Erasure Coding, State Transition
  Function, Block Import Traces; binary + JSON, validated against ASN.1 schemas (`scripts/convert-all.sh` needs
  davxy/jam-types-py; `validate-all.sh` needs davxy/asn1tools fork). Directories: `codec/ erasure/ lib/ scripts/ shuffle/
  stf/ traces/ trie/ (+ pvm/ programs per PR #3)`.
- CHANGELOG: 0.6.5 (02-06-2025, inaugural) → 0.6.6 (25-06-2025; `fetch` variants, explicit `genesis.bin`) → 0.6.7
  (07-08-2025; PVM page admin, host-call renumbering, storage deposits, accumulation output storage) → 0.7.0 (26-08-2025;
  "moving all variable-length items to end") → 0.7.1 (08-10-2025; removed `on_transfer` from service stats, version byte
  for account serialization, registrar privileges).
- **Tiny vs full parameters (verbatim YAML from README):**
  ```
  tiny:  num_validators: 6   num_cores: 2   preimage_expunge_period: 32    slot_duration: 6  epoch_duration: 12
         contest_duration: 10  tickets_per_validator: 3  max_tickets_per_extrinsic: 3  rotation_period: 4
         num_ec_pieces_per_segment: 1026  max_block_gas: 20000000  max_refine_gas: 1000000000
  full:  num_validators: 1023 num_cores: 341 preimage_expunge_period: 19200 slot_duration: 6  epoch_duration: 600
         contest_duration: 500 tickets_per_validator: 2  max_tickets_per_extrinsic: 16 rotation_period: 10
         num_ec_pieces_per_segment: 6   max_block_gas: 3500000000  max_refine_gas: 5000000000
  ```
  Symbols per docs.jamcha.in/basics/chain-spec: V, C, D, P, E, Y (Y>0 ∧ Y<E), N ((2V/3+1)·N ≥ E), R, K (K>0), W_P,
  G_T (total accumulation gas), G_R (refine gas); "all other values are assumed to be set to the values of the Graypaper".
  Tiny ring size for Bandersnatch ring proofs = 6 (full = 1023), Zcash SRS.
- **STF categories** (`stf/<name>/README.md`; JSON = input / pre_state / output / post_state; error codes per ASN.1):
  - `safrole` — ticket accumulation, epoch transitions, VRF/ring proofs, fallback when insufficient tickets; "No threshold
    requirement for ticket scores", accumulator must be full; 23 tiny cases (epoch change w/o tickets ×4, skipping epochs ×2,
    publish tickets w/o marks ×6, with marks ×5, padding/ring commitment ×1); fail cases: bad attempt numbers, duplicate
    tickets, invalid proofs, etc.
  - `disputes` — verdicts sorted/unique/vote counts; culprits for bad verdicts; faults for good verdicts; invalid
    signatures/unexpected keys; availability-assignment invalidation after verdicts; epoch boundary validator set use.
    9 valid / 29 invalid.
  - `history` (β) — recent-blocks queue empty / partial / saturating / rotation; MMR update with accumulation root; inputs
    header hash, parent state root, work package hashes.
  - `assurances` — no_assurances, some_assurances (supermajority), stale report removal; failures: bad signature, bad
    validator index, not-engaged core, bad attestation parent, assurers not sorted/unique.
  - `preimages` — solicited vs unsolicited, already provided, ordering by service then by hash, duplicates; updates
    provided-count / provided-size stats.
  - `authorizations` — pool left-shift, consumption per core when guarantees present (simplified `CoreAuthorizer` input).
  - `accumulate` — ready queue / accumulation history: no_available_reports, process_one_immediate_report,
    enqueue_and_unlock_simple/with_sr_lookup/chain/chain_wraps (ring buffer), enqueue_self_referential,
    accumulate_ready_queued_reports, queues_are_shifted, ready_queue_editing, transfer_for_ejected_service,
    work_for_ejected_service; gas: 1 per instruction (vs GP), host calls 10, transfer 10+ω9, log 0 (JIP-1).
  - `reports` (guarantees) — valid: current/previous rotation guarantors, many reports, high gas, many deps, dependencies
    (mutual/self/from history), big outputs; invalid: anchor not recent, bad code hash/state root/Beefy root, bad core/
    validator index, unknown service, core unavailable, missing prerequisites, duplicate package (report or history),
    future/old report slot, bad/insufficient signatures, too much gas/deps/output, unsorted guarantors, unauthorized core,
    bad segment-tree-root lookup. Note: "This subsystem is **not responsible** for modifying the contents of the
    authorization pools".
  - `statistics` — validator stats π_V/π_L only: empty extrinsic, epoch change, some extrinsic.
- **traces/** — "full blocks starting from genesis, implementing the complete logic required of a block importer that
  complies with … Milestone 1 (M1)"; tiny config; eight sets: fallback, safrole, storage (≤6 items/report), storage_light
  (≤1), preimages, preimages_light, fuzzy, fuzzy_light; gas: 1/instruction, host calls 10 (transfer & log excepted);
  D = 32 (full 19,200).
- **codec/** — refine_context, work_item, work_package, work_result_0/1, work_report, tickets/disputes/preimages/assurance/
  guarantees extrinsics, header_0/1, extrinsic, block. "designed to be syntactically correct only" (random data, GP
  constraints violated). "JAM Codec resembles SCALE encoding but uses distinct variable-length integer compression".
- **shuffle/** — Fisher–Yates with 32-byte hash entropy (GP eq. for shuffle "Eq 331" in 0.4.3 numbering); lengths
  0,8,16,20,50,100,200,341.
- **erasure/** — README only a heading; vectors for the systematic RS code over GF(2^16).
- **trie/** — no README; state-merklization vectors.
- **pvm/** — initial vectors by koute (PR #3): JSON with `initial-regs, initial-pc, initial-page-map, initial-memory,
  initial-gas, program, expected-status, expected-regs, expected-pc, expected-memory, expected-gas`; "not every instruction
  is covered yet". Separate community suites: FluffyLabs pvm-debugger (https://github.com/fluffylabs/pvm-debugger), `@typeberry`.

### C.2 davxy/jam-conformance (https://github.com/davxy/jam-conformance)

- "This repository serves as a scratchpad for JAM protocol conformance testing materials, including: Fuzzer reports, PVM
  execution traces, Protocol conformance discussions and issues." "THIS IS NOT THE OFFICIAL AUDITING PROCESS."
  Dirs: `fuzz-proto` (spec), `fuzz-reports`, `fuzz-perf`, `pvm-traces`, `crypto` (incl. ed25519 vectors), `scripts`
  (`target.py` to manage targets), `conformance-criteria`, `test-vectors` (submodule). 726 commits.
- **Fuzz protocol** (`fuzz-proto/README.md`): "a synchronous **request-response** protocol over Unix domain sockets";
  target "must bind to a named `SOCK_STREAM` Unix domain socket … (e.g., `/tmp/jam_target.sock`)". "All messages are
  encoded according to the **JAM codec** format. Prior to transmission, each encoded message is prefixed with its length,
  represented as a **32-bit little-endian integer**." Messages: `PeerInfo`↔`PeerInfo` (handshake/versioning: fuzz version
  1; jam version e.g. 0.7.0; app version), `Initialize`→`StateRoot`, `ImportBlock`→`StateRoot`|`Error`, `GetState`→`State`.
  Discriminants e.g. 00 peer_info, 02 state_root, ff error. "Session features are determined by the intersection
  (bitwise-and) of the features listed in the `PeerInfo` message." **Mandatory M1 features: Ancestry** ("lookup anchors in
  guarantees are within last L imported headers") **and Forking** (fuzzer mutates blocks / forks). "After each block import,
  state roots are compared"; on mismatch "the fuzzer attempts to fetch the whole state from the target to produce a
  comprehensive fuzz report." Later extension discussed: a *refinement* extension for 0.7.1 (Aug 2025 conformance chat).
- **fuzz-reports/README**: GP 0.7.2 targets (23): boka (swift), fastroll (rust), gossamer (go), graymatter (elixir),
  jam4s (scala), jamduna (go), jamforge (scala), jamixir (elixir), jampy (python), jamzig (zig), jamzilla (go),
  javajam (java), new-jamneration (go), pbnjam (ts), polkajam (rust), pyjamaz (python), spacejam (rust), strawberry (go),
  tessera (python), tsjam (ts), turbojam (c++), typeberry (ts), vinwolf (rust). "reports are stored **per team**",
  "**disputed traces** are preserved permanently". No `0.8.0` report folder existed at fetch (404).
- Issues = one per team (labels `gp-0.7.2`, `std`): JOTL #196, Jambda #184, PeanutButterAndJAM #144, Jam4s #128,
  JamForge #126, New-JAMneration #123, Strawberry #101, Typeberry #81, Tessera #63, Gossamer-Jam #62, FastRoll #45,
  TSJam #35, Jampy #30, TurboJam #26 (Docker `r2rationality/turbojam-fuzz`, 3 preimage gas divergences), …
  Discussions: "Standardizing Target Packaging and Entry Points (Docker-based Submission)" (Apr 27 2026), recent_history
  (β) field order vs GP 0.7.2 (Mar 2026), state-root-mismatch traces.
- **Conformance dashboard** (https://paritytech.github.io/jam-conformance-dashboard/, repo paritytech/jam-conformance-dashboard):
  "a visual leaderboard" of import performance per implementation; score = weighted P50 35% / P90 25% / mean 20% / P99
  10% / stddev 10%, geometric mean across Safrole, Fallback, Storage, Storage-Light benchmarks; "Version 0.7.2; Updated May
  10, 2026; No implementations are fully conformant yet". Ranking (score, lower better): PolkaJam (Recompiler) 2.1,
  SpaceJam 2.6, PolkaJam 3.5, JAM DUNA 6.8, Jamzilla 7.9, Vinwolf 8.1, FastRoll 8.8, Strawberry 10.1, JamZig 14.6,
  Jamixir 17.2, JavaJAM 20.2, Boka 32.7, TSJam 43.0, Typeberry 46.8, PyJAMaz 47.8, GrayMatter 65.1, JamPy 75.7,
  New JAMneration 91.3, JAM Forge 119.3, Gossamer JAM 149.7.
- **jamtoaster**: https://fuzz.jamtoaster.network/ "JAM Submission App" (teams submit fuzz targets; produces
  `/attestation/0x…` links, e.g. JamForge May 2026). "JAM Toaster" per the Polkadot Wiki = "A large-scale test platform
  comprising 1,023 nodes" for full-scale performance/network behaviour. JAM DUNA ships a "PoC JAM Toaster testnet" release
  (GP 0.7.2, `jamduna` binary, `fib` service, `null_authorizer.pvm`, 6-validator tiny testnet via Makefile) in
  https://github.com/jam-duna/jamtestnet ("JAM DUNA Fuzzer") / jam-duna/coreplay ("Fuzzer + JAM Toaster Testnet").
- **JamTART** = "JAM Tart (Testing, Analytics and Research Telemetry)" (JIP-3) — the telemetry backend for the toaster.
- Community trackers: JAM Implementers DAO (docs.jamcha.in/dao — 19 members incl. JAM DUNA, Gossamer, Jamixir, JavaJAM,
  JamZig, JamPy, Vinwolf, TSJam, Boka, New JAMneration, MORUM, Tessera, typeberry, JamBrains, Clawbird, SpaceJam, Eiger,
  PeanutButterAndJAM); "JAM Implementers DAO Testnet Compliance" Google Sheet (columns: DUNA Go fallback / safrole /
  assurances / accumulation …).

---

## D. Design rationale & architecture materials

### D.1 The Gray Paper's own rationale (LaTeX source, github.com/gavofyork/graypaper/text/*.tex)

Chapter files in order (graypaper.tex): abstract, intro, previous_work, notation, overview, header, safrole,
recent_history, authorization, accounts, judgments, reporting_assurance, accumulation, statistics,
work_packages_and_reports, guaranteeing, assurance, auditing, beefy, best_chain, discussion, conclusion, ack; appendices:
pvm, pvm_invocations, serialization, merklization, utilities, bandersnatch, erasure_coding, definitions. (So "chapters
3–13" ≈ Overview … Accumulation/Statistics range in the numbered PDF; verify against the 0.8.0 PDF TOC.)

- **Abstract**: "We present a comprehensive and formal definition of Jam, a protocol combining elements of both Polkadot and
  Ethereum." "Jam introduces a decentralized hybrid system offering smart-contract functionality structured around a secure
  and scalable in-core/on-chain dualism." Anyone may "deploy code as a service on it for a fee commensurate with the
  resources this code utilizes"; a Polkadot-compatible **CoreChains** service is envisioned. Site tagline:
  "JOIN-ACCUMULATE MACHINE: A MOSTLY-COHERENT TRUSTLESS SUPERCOMPUTER".
- **Intro / nomenclature**: "An early, unrefined, version of this protocol was first proposed in Polkadot Fellowship RFC 31,
  known as CoreJam." "CoreJam takes its name after the collect/refine/join/accumulate model of computation at its heart."
  (On-chain only Join+Accumulate execute; Collect+Refine are off-chain — hence "JAM".)
- **Driving factors** (verbatim): "Resilience: highly resistant from being stopped, corrupted and censored." "Generality:
  able to perform Turing-complete computation." "Performance: able to perform computation quickly and at low cost."
  "Coherency: the causal relationship possible between different elements of state." "Accessibility: negligible
  barriers to innovation; easy, fast, cheap and permissionless."
- **Size–coherency antagonism**: "as the state-space of information systems grow, then the system necessarily becomes
  less coherent" *(fetch paraphrase of the intro)*; rooted in causality/light-speed limits. Fragmenting systems (Polkadot,
  Cosmos, scaled Ethereum) "typically rely on asynchronous and simplistic communication with settlement areas."
  **JAM's answer**: "We do this by introducing a new model of computation which pipelines a highly scalable, mostly
  coherent element to a synchronous, fully coherent element." "we substitute the crude partitioning we see in scalable
  systems so far with a form of cache affinity." (multi-CPU analogy).
- **Previous work (ch. 2)**: Polkadot — JAM "adopts Polkadot's game-theoretic and cryptographic machinery (ELVES)" but
  parachains are isolated; XCMP is "asynchronous, coarse-grained and practically limited by its reliance on a high-level
  slowly evolving interaction language"; Polkadot is "a collection of independent ecosystems with only limited opportunity
  for collaboration"; accessibility limited to ~50 auction slots. Ethereum — flat compute since 2015; Dank-sharding; rollup
  market with "heterogeneous communication … security … and economic properties". SNARK rollups — RISC-Zero "over 61,000
  times as long as simply recompiling and executing", "66,000,000x" cost; StarkWare "in fact centralized"; even "50,000x"
  is "several orders of magnitude greater than would be required to compete on a cost-basis with established
  crypto-economic techniques." Fragmented meta-networks (Cosmos/Avalanche) — no causal link between Byzantine actions;
  ELVES = "non-redundant partitioning, combine this with a proposal-and-auditing game". Solana — "11 significant outages
  … 15 days" since Jan 2022, "512 GB" RAM, data "onto a centralized database hosted by Google".
- **Overview (ch. 3)**: block = header + extrinsic (tickets, preimages, guarantees ("reports"), assurances, disputes);
  state partitioned into ~16 mostly independent components enabling parallel STF computation; Safrole minimises forks,
  Grandpa finalises: "It be generally unlikely for two heads to form. When two heads do form they be quickly resolved";
  time in 6-second slots, 600 per epoch; **JAM Common Era begins 1 Jan 2025 12:00 UTC**; balances u64 (≈18e9 tokens at
  10^-9 precision); PVM = 64-bit RISC-V-based, 13 registers, pageable 32-bit-addressable memory, gas metered, "simpler than
  EVM" and compatible with LLVM/Rust/C++; **in-core consensus** (only assigned validators execute → "approximately 300x"
  throughput) vs **on-chain** (all validators execute); services replace Ethereum's two account types, each with
  refinement code (stateless, off-chain, arbitrary inputs) and accumulation code (stateful, on-chain, can transfer);
  "This separation allows services to scale dramatically both in the size of their inputs and in the complexity of their
  computation" *(paraphrase)*; **coretime is bought in advance and assigned to authorizers**, decoupling authorisation
  from blockspace purchase and "enabling permissionless external input without identifying the originator".
- **Header (ch. 5)**: fields parent hash, **prior** state root, extrinsic hash, timeslot, epoch marker, winning-tickets
  marker, offenders marker, author index, entropy VRF signature, seal. "We do this to facilitate the pipelining of block
  computation and in particular of Merklization." Extrinsic hash is "a Merkle commitment to the block's extrinsic data,
  taking care to allow for the possibility of reports and preimages to individually have their inclusion proven" (0.8.0
  PR #524 changed the definition to allow per-extrinsic preimage checks).
- **Safrole (ch. 6)**: "a stateful system rather more complex than the Nakamoto consensus"; "a simplified variant" of
  Sassafras; "a novel RingVRF cryptographic scheme built on the Bandersnatch curve" giving "an unbiasable deterministic
  hash output"; under normal operation the future slot key-holder has "a very high degree of anonymity" and the design
  yields "a high-quality pool of entropy". Tickets accepted while slot phase < C_epochtailstart = 500; accumulator holds
  exactly E entries; outside-in sequencer Z = [s0, s(n-1), s1, s(n-2), …]; next epoch uses tickets iff e' = e+1, the prior
  slot was in the tail (m ≥ 500) and the accumulator is full — else **fallback keys** F(η2, validator keys); entropy
  rotation (η1', η2', η3') = (η0, η1, η2) at epoch change; η2 seeds fallback, η3 verifies seals; epoch marker (when
  e' > e: entropy + next validators' Bandersnatch/Ed25519 keys); winning-tickets marker (when e' = e and tickets close in
  this block with a saturated accumulator: Z(accumulator)); key sets ι staging, κ active, λ previous, γ_k pending, γ_z ring
  root; offenders' keys nulled at epoch change; **N = ⌈2·E / |γ_k|⌉** tickets per validator (0.8.0: "each validator is
  permitted more tickets" when there are fewer validators; the old constant was replaced by an equation ref, PR #527);
  seal contexts `$jam_ticket_seal` / `$jam_fallback_seal`, entropy context `$jam_entropy`.
- **Disputes (ch. 10)**: "The registration of a verdict is not expected to happen very often in practice, however it is an
  important security backstop for removing and banning invalid work-reports from the processing pipeline." "Having a
  persistent on-chain record of misbehavior is helpful in a number of ways." "Should Jam be used for a public network such
  as Polkadot, this would imply the slashing of the offending validator's stake on the staking parachain" — JAM records
  offenders; slashing is delegated. State: good-set, bad-set, wonky-set, offenders (Ed25519 keys). Extrinsic: verdicts
  (2/3+1 positive, ≤1/3 → "wonky"), culprits (guaranteed a bad report), faults (signed contradicting judgment). "Authoring a
  block with a non-positive verdict has the effect of cancelling its imminent accumulation". 0.8.0 (#525): hard limits
  C_maxextrinsicverdicts = 16, C_maxextrinsicoffenses = 16; culprits no longer mandatory for bad verdicts.
- **Reporting & assurance (ch. 11)**: ρ per core = "a work-report guarantee which has been reported but is not yet known to
  be available to a super-majority of validators, together with the time at which it was reported" (0.8.0 #494 keeps the
  *full guarantee incl. signatures* in ρ: needed "To determine the guarantors to try directly fetching the bundle from" and
  "In the case of a dispute, the guarantor signatures are needed to construct a disputes extrinsic"). Guarantor assignment
  by "a shuffle using epochal entropy and a periodic rotation" (rotation every 10 slots); 2 or 3 signatures from
  validators assigned "in the same rotation as this block's timeslot or in the previous rotation"; "Use of an inactive core
  is not permitted"; anchor within recent history (8 blocks); lookup anchor ≤ 14,400 slots old; ≤ 8 dependencies;
  authorizer must be in the core's pool; ≤ 10M accumulation gas per report; ≤ 48 KiB variable output; no duplicate
  packages. Assurances: bitfield ("A value of 1 … implies that the validator assures they are contributing to its
  availability"), anchored on parent; report available "if and only if there are a clear two-thirds super-majority";
  timeout after 5 slots (C_assurancetimeoutperiod) or validator-set change.
- **Accumulation (ch. 12)**: "Accumulation may be defined as some function whose arguments are [W] and [δ] together with
  selected portions of (at times partially transitioned) state and which yields the posterior service state … together with
  … ι', φ' and χ'". Reports with unmet prerequisites are deferred (ready queue ϑ) and cancelled if a dependency is invalid;
  ξ = one epoch of accumulated package hashes. Tension between sequential execution (true gas accounting) and per-service
  batching (amortise PVM setup) resolved via Δ_seq / Δ_par; **always-accumulate** privileged services first; deferred
  transfers partitioned so that "transfers to a service never execute in parallel with that service's supervisor Accumulate
  logic" *(paraphrase)*; output = accumulation output log θ (service, commitment) + gas stats. 0.7.1 merged `on_transfer`
  into `accumulate` (#457) and introduced "Owned Privileges" (#475); 0.8.0 (#519) `bless` restricted to the manager (attack:
  a service `bless`es itself manager → `new` with gratis storage; or registrar → low service id).
- **Work packages/reports (ch. 14)**: package = authorization token, auth service index, auth code hash, "a configuration
  blob", context, work items; **authorizer = hash(auth code hash ++ config)** (0.8.0 #522 aligned ch. 8 with ch. 14);
  items carry service, code hash, payload, refine & accumulate gas limits, imports (segment root + index), extrinsic
  hashes+lengths, export count; context = anchor (hash, state root, beefy root) + lookup anchor (hash, time) — 0.8.0 (#526)
  adds lookup-anchor posterior root and anchor slot; bundle ≤ 13,791,360 B ("2 MB/s/core D³L imports"); 3,072 imports /
  3,072 exports / 128 extrinsics; exports form a constant-depth binary Merkle tree (segment root), paged proofs stored in
  the long-term D³L ≥ 28 days.
- **Guaranteeing (ch. 15)**: steps — check authorization against pool, run is-authorized then refine per item, erasure-code
  and chunk, build & publish the report, distribute chunks, optionally serve the bundle; "With two guarantor signatures,
  the work-report may be distributed to the forthcoming Jam chain block author"; "Validators will be punished severely if
  they malfunction and commit to a report which does not faithfully represent the result of computereport"; advice to sign
  "no more than two work-reports per timeslot".
- **Availability assurance (ch. 16)**: assurers "issue a signed statement, called an assurance, indicating which of the
  current availability assignments the validator has received its erasure-coded shards for"; two shard types — the
  work-report bundle shard (audit DA) and segment shards (import DA, "retained for 28 days") — proven via the
  erasure-root + Merkle proof.
- **Auditing (ch. 17)**: each node must "fetch, evaluate and issue judgment on a random but deterministic set of
  work-reports"; VRF-selected initial tranche, new tranches every 8 s (C_trancheseconds) when "a negative judgment has been
  received" or "the number of judgments from the previous tranche is less than the number of announcements" (**no-shows**;
  C_auditbiasfactor = 2 extra auditors per no-show); audited when "positive judgments from greater than two-thirds"; bundle
  reconstruction needs "erasure-coded chunks from one-third of the validators". Security analysis: ELVES paper
  "Efficient Execution Auditing for Blockchains under Byzantine Assumptions" (https://eprint.iacr.org/2024/961).
- **BEEFY (ch. 18)**: "For each finalized block which a validator imports, said validator shall make a BLS signature on the
  BLS12-381 curve … affirming the Keccak hash of the block's most recent BEEFY MMR" (accumulation-output MMR super-peak);
  aggregated "to provide concise proofs of finality to third-party systems" (bridging).
- **Best chain (ch. 19)**: Grandpa; best block must have the finalized block as ancestor, be audited (isaudited = ⊤),
  contain no unfinalized equivocations, and prefer the chain "which contains the most ancestor blocks whose author used a
  slot-sealer ticket, rather than a fallback key"; Grandpa votes include the posterior state root so consumers "are able to
  verify the most recent chain state as possible".
- **Discussion (ch. 20)**: 1,023 validators, 3 per core, 341 packages/slot; reference hardware 16-core CPU, 64 GB RAM, 8 TB
  storage, 0.5 Gbps; CPU split audits 10/16, block execution 2/16, merklization 1/16, GRANDPA+BEEFY 1/16, erasure coding
  1/16, networking 1/16; bandwidth ≈387 MB/s out / 357 MB/s in; 2 PB network DA, ≤6 TB per node; RAM 20 GB auditing (2
  PVMs), 2 GB block exec, 40 GB state cache; a core ≈ a CPU core at 25–50% speed for 6 s with 2 MB/s I/O and 2 GB RAM,
  results ≤48 KB; vs Polkadot (80 parachains, ~13× native CPU, 67 MB/s DA) JAM models 85× compute and 682 MB/s DA; naive
  171k TPS, partitioned 1.4M TPS; EVM-equivalent 500–5,000 gas/µs per core vs L1's 1.25; drivers: spatial parallelism,
  temporal parallelism (pipelining), PVM/hardware alignment; "provisional modeling estimates".
- **Conclusion**: JAM is a "sweet spot" between fully-synchronous and persistently fragmented models; omitted by design:
  token/coretime sales/staking/smart-contract mechanics; future work: synchronous service calls in accumulate, transfer
  restrictions for parallelism, reserving extra compute, merklization of WP format, the networking protocol, on-chain
  validator performance tracking.

**Protocol constants (definitions.tex, GP 0.8.0 macros; verbatim descriptions):** C_corecount 341; C_epochlen 600;
C_slotseconds 6; C_trancheseconds 8; C_rotationperiod 10; C_expungeperiod 19,200; C_epochtailstart 500;
C_recenthistorylen 8; C_maxblocktickets 16; C_maxpackageitems 16; C_maxreportdeps 8; C_maxextrinsicverdicts 16;
C_maxextrinsicoffenses 16; C_authpoolsize 8; C_authqueuesize 80; C_minpublicindex 2^16; C_maxpackagexts 128;
C_maxpackageimports 3,072; C_maxpackageexports 3,072; C_maxbundlesize 13,791,360; C_maxreportvarsize 48·2^10;
C_maxauthcodesize 64,000; C_maxservicecodesize 4,000,000; C_segmentsize 4,104; C_segmentfootprint 4,488; C_memosize 128;
C_maxlookupanchorage 14,400; C_assurancetimeoutperiod 5; C_pvmpagesize 2^12; C_pvminitzonesize 2^16;
C_pvminitinputsize 2^24; C_pvmdynaddralign 2; C_basedeposit 100; C_itemdeposit 10; C_bytedeposit 1;
C_reportaccgas 10,000,000; C_packageauthgas 50,000,000; C_packagerefgas 5,000,000,000; C_blockaccgas 3,500,000,000;
C_auditbiasfactor 2. Host-call gas (0.8.0 new model): CgasG 48, CgasK (invoke) 968, CgasM (machine) 1862, CgasT
(transfer) 575, Cgasunknown 1000, CgasHconst 1125 + 264/KiB (historical_lookup), CgasLconst 600 + 248/KiB (lookup),
CgasGammamemconst 1862 (compile), CgasZallocconst 275 + 121/page (pages), CgasGeminilinear 121/page (grow_heap).
Validator count: 1023 in full config; 0.8.0 (#514) allows sets ≥ 6, multiple of 3, with "active" cores scaling
proportionally (341 total cores). Signing contexts: X_available, X_beefy, X_entropy, X_fallback, X_guarantee, X_announce,
X_ticket, X_audit, X_valid, X_invalid.

**PVM (appendix A/B) essentials**: 13 registers; page size 4 KiB; zones 64 KiB; init registers: r0 = 2^32−2^16 (return
address; a dynamic jump to it halts), r1 = 2^32 − 2·Z_Z − Z_I (stack pointer), r7 = 2^32 − Z_Z − Z_I (argument pointer),
r8 = |a| (argument length), others 0; pc = 0; memory layout: zone 0 inaccessible, read-only data at Z_Z, heap after
2·Z_Z + rounded len(o), stack below the args, args at 2^32 − Z_Z − Z_I. Blob = [len(j)] [z entry width] [len(c)] [jump
table] [code] [bitmask]; opcode bitmask marks instruction starts, skip ≤ 24; dynamic jump alignment 2 — LLVM footnote:
"The popular code generation backend LLVM requires and assumes in its code generation that dynamically computed jump
destinations always have a certain memory alignment. Since at present we depend on this for our tooling, we must acquiesce
to its assumptions." Exit reasons ε ∈ {halt, panic, oog} ∪ ({fault, host} × register). **0.8.0 gas model (#508, koute):**
per-basic-block charging ("No instruction is allowed to execute within a basic block unless the gas cost for the entire
basic block has been charged in advance"), simulated micro-architecture (32-entry reorder buffer; ALU/LOAD/STORE/MUL/DIV
units; 4 decodes and 5 starts per cycle), cost = max(cycles − 3, 1); `sbrk` replaced by `grow_heap` host call; opcodes
and host calls renumbered; blobs pre-validated; "Implementations now require an ahead-of-time whole-program recompiler for
PVM programs" *(PR summary)*; model "successfully implemented by at least 2 independent JAM teams". Host-call indices
(0.8.0): gas 0, grow_heap 1, fetch 2, lookup 3, read 4, write 5, info 6, historical_lookup 7, export 8, compile 9,
machine 10, peek 11, poke 12, pages 13, invoke 14, expunge 15, bless 16, assign 17, designate 18, checkpoint 19, new 20,
upgrade 21, transfer 22, eject 23, query 24, solicit 25, (forget/yield/provide follow **[verify]**), log 100 (JIP-1);
unknown index → charge Cgasunknown and return WHAT. Return codes: OK 0, NONE 2^64−1, WHAT −2, OOB −3, WHO −4, FULL −5,
CORE −6, CASH −7, LOW −8, HUH −9. Invocation types: Ψ_I is-authorized (stateless), Ψ_R refine (historical lookups, inner
VMs, export), Ψ_A accumulate (partial state, slot, service, gas, operands/deferred transfers) — "PVM has three invocation
types" (0.8.0 nit #511). `fetch` selectors 0..15: 0 protocol constants, 1/2 authorizer trace, 3/4 extrinsics, 5/6 imports,
7 encoded package, 8 auth config, 9 auth token, 10 context, 11/12 work-item summaries, 13 payload, 14/15 operands.
Deferred transfer = (source, destination, supervisor flag, amount, memo[128], gas). 0.8.0 also limits parallel inner VMs
in refine (#521).

**Erasure coding (appendix H)**: "a systematic Reed-Solomon erasure coding function in GF(2^16)", polynomial
x^16+x^5+x^3+x^2+1, Cantor basis; rate d(v):v with
`fnecoriginalshards(v) ≡ max({d | d ∈ N_{v/3+2}, C_segmentsize mod 2d = 0})` → 1023 validators: d = 342
("data-parallelism of order 6 with 1023 validators", i.e. 4104/(2·342) = 6 pieces of 2 bytes per validator per segment);
"we wish to be able to reconstruct even should almost two-thirds of the v validators be malicious or incapacitated";
systematic so "If the original d items are known then reconstruction is just their concatenation." (For a 6-validator
set the formula gives d = 3; the 0.7.x tiny vectors used W_P = 1026 ⇒ 2 data shards — expect this to differ in 0.8.0
vectors **[verify]**.)

**Merklization (appendix D)**: "a binary Patricia Merkle Trie with a format optimized for modern compute hardware";
31-byte keys; 512-bit nodes; branch = 1 bit + 255 bits of left child hash + 256 bits of right; leaf: embedded value if
≤ 32 bytes (6 size bits + 31-byte key + 32-byte value) else hash of value; Blake2b; state key constructor C(i) = [i,0…],
C(i, s) = [i, s-bytes, 0…], C(s, h) = [s-bytes ⨉ hash bytes]; state chapters C(1) α authorizer pool, C(2) φ auth queue,
C(3) β recent blocks, C(4) γ Safrole, C(5) ψ disputes, C(6) η entropy, C(7) ι validator queue, C(8) κ current validators,
C(9) λ previous validators, C(10) ρ assigned reports, C(11) τ time, C(12) χ privileges, C(13) π statistics, C(14) ϑ
accumulation queue, C(15) ξ accumulation history, C(16) θ accumulation output log, C(255, s) service metadata, C(s,·)
storage/preimage/lookup (docs.jamcha.in/advanced/storage/keys). "well-balanced binary Merkle tree" for extrinsics/segments;
MMR with super-peak. **Serialization (appendix C)**: compact natural encoding up to 2^64 (0 → single zero byte; 9-byte
form for large), fixed little-endian ints, length-prefixed sequences, dictionaries "as a sequence of pairs ordered by the
key", bit sequences LSB-first, option = 0 | (1, x); 0.7.0 moved all variable-length items to the end of encodings;
0.7.1 added a version byte prefix to account serialization.

### D.2 RFC-31 CoreJam (https://raw.githubusercontent.com/polkadot-fellows/RFCs/gav-corejam/text/0031-corejam.md; PR https://github.com/polkadot-fellows/RFCs/pull/31)

- "Work Packages are communicated, authorized, computed and verified, and their results gathered, combined and
  accumulated into particular parts of the Relay-chain's state."
- Motivation: "it seems short-sighted to assume other models could not exist for utilizing the Relay-chain's 'Core'
  resource"; goal "a future-proof platform allowing teams to build on it without fear of high maintenance burden,
  continuous bitrot or a technological rug-pull."
- Not exactly map-reduce: "the in-core processing code does not transform a set of inputs, but is rather used to refine
  entirely arbitrary input data collected by some third-party." Stages: Collect (backing groups acquire authorized
  packages) → Refine (in-core `refine` → work results) → Join (on-chain attestation + availability) → Accumulate
  (on-chain `accumulate` integrates results into service state).
- Split rationale: "Unlike with the computation in Collect-Refine which happens contemporaneously within one of many
  isolated cores, the consensus computation of Join-Accumulate is both entirely synchronous with all other computation."
- Authorizers: "Authorization logic is entirely arbitrary and need not be restricted to authorizing a single collator, Work
  Package builder, parachain or even a single Service." "Validators get rewarded for *any* such authorized Work Package,
  even one which ultimately panics or overruns on its evaluation."
- Early limits: ≤4 items/package, 5 MB package, 4 KB work output; accumulate weight ≈ relay_block_weight·3/4 ÷ max_cores;
  soft vs hard ordering; "We can already imagine three kinds of Service: *Parachain Validation* (as per Polkadot 1.0),
  *Actor Progression* (as per Coreplay), and Simple Ordering." "Being extensible, the Relay-chain becomes far more open to
  experimentation".

### D.3 Explainers & official docs

- **Kian Paimani, "Demystifying JAM"** (https://blog.kianenigma.com/posts/tech/demystifying-jam/; Parity repost
  https://www.parity.io/blog/JAM-demystified-explainer): "JAM is a new protocol, heavily inspired by Polkadot, and fully
  compatible with it, aiming to replace the Polkadot relay chain and make the usage of cores radically un-opinionated."
  "What was once called an L2/parachain is now called a service"; work-items replace blocks/transactions. "Join is fn
  refine(), when all Polkadot cores do a lot of work, all in parallel, for different services." In-core: "Abundance,
  scalable, as secure as on-chain execution through crypto-economics and ELVES." On-chain: "More expensive and constrained,
  as everyone is executing everything." Semi-coherence: "a semi-coherent system, one in which sub-systems that communicate
  often have a chance at creating a coherent environment with one another, whilst not enforcing the entire system to be
  coherent." PVM: "efficient metering" + "Ability to pause and resume execution" → **CorePlay** (actor calls are synchronous
  if the callee is on the same core in that block, otherwise paused and resumed later). **CoreChains** = first service,
  "The existing product offering of Polkadot will remain strong". Kernel analogy: JAM migration is "a kernel upgrade. The
  underlying hardware remains the same, and a large chunk of the old kernel is moved to the userland for simplicity."
- **Polkadot Wiki — JAM Chain** (https://wiki.polkadot.com/learn/learn-jam-chain/): name from CoreJAM "Collect Refine Join
  Accumulate"; "within the actual chain, only the Join and Accumulate functions are executed, while the Collect and Refine
  processes occur off-chain." Refine: up to 15 MB input per 6 s slot, ≤ 90 kB output *(older figure)*, ~6 s of PVM gas;
  Accumulate ≈ 10 ms per output. "The creation of a new service is permissionless, akin to deploying a smart contract."
  Transactionless: extrinsics are guarantees, assurances, judgments, preimages, tickets ("operating two epochs in advance"
  *(wiki wording)*). "SAFROLE will be as simple as possible…To follow in the footsteps of Ethereum yellow paper." PVM
  rationale: RISC-V "Easy transpilation to x86, x64, and ARM", "Strong LLVM tooling", "Deterministic, consensus-sensitive,
  and metering-friendly", "Handles stack continuations naturally within memory (unlike WebAssembly)". Pipelining: prior
  state root in header lets "~5%" of work run immediately and "~95%" (accumulation) afterwards → "approximately three to
  three and a half seconds of effective block computation time". Networking: QUIC, no gossip, "grid-diffusal". JAM vs
  Polkadot 1.0: "less opinionated, more generic"; "Non-upgradable chain; upgradability responsibility shifted to services";
  "JAM will be introduced as a comprehensive singular upgrade." XCMP mandated (HRMP limited to 4 kB); Accords; JAM Toaster
  = 1,023-node test platform. **FAQ** (https://wiki.polkadot.com/learn/learn-jam-faq/): "DOT will continue to be JAM's
  native token. No other native token will be issued."; parachains "will stay first-class citizens"; upgrade via OpenGov.
  **Safrole page** (https://wiki.polkadot.com/learn/learn-safrole/): "SAFROLE (formerly known as SASSAFRAS) is a SNARK-based
  block production algorithm that provides anonymity in the validator selection process"; "prove they are in the active set
  without revealing their identity"; "limiting the possibility of multiple valid authors per six-second timeslot".
- **JAM Docs / "JAM Brains"** (https://docs.jamcha.in/): chain-spec, dev accounts (JIP-5), genesis config, state keys,
  PVM ("PVM defines a fixed cost for each instruction (aka *gas*)"; "extremely fast Just-In-Time compilation speed"),
  JAMNP-S networking spec (https://docs.jamcha.in/knowledge/advanced/simple-networking/spec): QUIC + TLS 1.3, Ed25519 certs
  with alt-name derived from the key, ALPN `jamnp-s/V/H` (V=0, H = first 8 nibbles of genesis-header hash), validators of
  prev/current/next epoch fully connected, grid neighbours = same row or column, UP streams (unique persistent, from 0) vs
  CE streams (common ephemeral, from 128): UP0 block announcement; CE128 block request; CE129 state request; CE131/132 Safrole
  ticket distribution; CE133 work-package submission (builder→guarantor); CE134 WP sharing (guarantor↔guarantor); CE135
  work-report distribution; CE136 work-report request; CE137 shard distribution; CE138 audit shard request; CE139/140 segment
  shard request; CE141 assurance distribution; CE142 preimage announcement; CE143 preimage request; CE144 audit
  announcement; CE145 judgment publication; messages length-prefixed (u32 LE). "This version of the protocol will most
  likely not be formalized in the Graypaper."
- **Forum — "Introducing a new JAM Token?"** (Gavin, https://forum.polkadot.network/t/introducing-a-new-jam-token/13029/43):
  "I, personally, am not planning to launch a new token based on the JAM protocol." "The DOT token is the mainstay of the
  Polkadot product economy and I very much expect it to stay this way." JAM is "a Web3 *protocol*" that "is strictly and
  minimally specified and has no single reference implementation or single financial interest"; anyone may launch a JAM
  network. 2026: **JAMKB** = "a fixed-supply resource token to meter JAM's scarce in-RAM state — owned by the DOT DAO and
  explicitly not a new currency competing with DOT"; Polkadot ref 1926 burns 100% of DOT revenue from JAMKB sales (Aug 2026
  digests). **"Polkadot 3.0 – the JAM upgrade"** thread (https://forum.polkadot.network/t/polkadot-3-0-the-jam-upgrade/13834):
  "a CPU replacement"; brand Polkadot / tech JAM Chain / token DOT. **MiniJAM** (Jul 2026,
  https://forum.polkadot.network/t/minijam-a-parachain-running-a-streamlined-jam/18120): a parachain running streamlined
  JAM keeping "PVM, service, refine, and accumulate" but replacing consensus with parachain security, DA/D3L with the
  bulletin chain, and "assurance, guaranteeing, auditing, and adjudication … with an off-chain Worker mechanism".
- **Talks**: CoreJam RFC-31 (2023) → sub0 Asia (Bangkok, Mar 2024) keynote "JAM: A to Z" → **Gray Paper unveiled at
  Token2049 Dubai, 18 Apr 2024** (Decrypt, Apr 19 2024: "a more modular, minimalistic design", ~50 parachain slots barrier,
  PVM replaces Wasm, "852Mb/s" DA "roughly 42 times" Polkadot's, "150 billion gas per second", "20 to 60 months" to
  production, single switch-over rather than gradual rollout). JAM Tour lectures at universities
  2024–25 (graypaper.com/tour, /lectures: 1.1 Nomenclature, 1.2 Driving Factors…). Gray Paper interview (Key Pictures,
  https://www.youtube.com/watch?v=O3kRAVBTkfs). Decrypt: Wood on JAM as the "original concept" of a world computer,
  "500,000 times the EVM computation performance [...] maybe into the millions" (with "a very, very, very large pinch of
  salt"). Web3 Summit Berlin Jul 2025: "12 to 20 months" to JAM delivery; Proof-of-Personhood; token cap "π times
  1,000,000,000" with annual halving *(as reported by Bitget/PolkaWorld)*. Web3 Summit Jun 2026 (keynote "Polkadot, Human
  Web3", https://www.youtube.com/watch?v=0dqpx2kKdyA; second talk with byteboro: "JAM gives Polkadot collective compute").
  Sub0 Reset (2025): "within a year or so" *(forum paraphrase)*. JAMmed newsletter Feb 2025: GP 0.6 "signals a feature freeze
  on the JAM protocol … further development will be limited to tweaks, optimizations, and audits"; Jamixir "first to deploy
  a JAM node and start producing blocks".
- Other explainers: Polkadotters "Polkadot JAM Explained. Simply!" (transactionless; "~350 cores with 6s execution time &
  5Mb input each, totaling around 2.3Gbps"; "850MB" DA); Frank Mangone "Blockchain 101: JAM" (WASM "non-deterministic code
  baked into the specification. Things like floating-point"; PVM "disallow[s] all unneeded behaviors"); BlockEden Jan 2026
  (register machine ↔ hardware, 64-bit word, "850 MB/s", "150 billion gas per second", "3.4+ million TPS", 43 teams, "Q1
  2026" mainnet claim — treat as marketing); OpenGuild learn-jam (PolkaVM "300x compilation time faster than Wasmtime").
- **Bandersnatch VRF spec** (https://github.com/davxy/bandersnatch-vrf-spec): Tiny/Thin VRF (≈IETF ECVRF RFC-9381), Pedersen
  VRF (BCHSV23), Ring proof (CSSV22) over Bandersnatch (BLS12-381 scalar field, MSZ21); reference impl ark-vrf; ring test
  vectors with KZG SRS (Zcash).

### D.4 Gray Paper history & changelog (https://github.com/gavofyork/graypaper/releases)

Timeline: RFC-31 CoreJam (2023) → sub0 Asia "JAM: A to Z" keynote (Mar 2024) → **GP 0.1 unveiled at Token2049 Dubai
(18 Apr 2024)**; #graypaper:polkadot.io review room opens Apr 17 2024 → 0.2/0.3 (mid-2024, JAM Tour; first test vectors,
Safrole/erasure-coding debates Jul 2024) → 0.4.x (Sep–Oct 2024; 0.4.5 Oct 30 2024) → **0.5.0 (19 Nov 2024; "64-bit changes")** → 0.5.4 (8 Jan 2025) →
**0.6.0 (30 Jan 2025; `fetch` replaces `import`; memory-access exceptions formalised; "feature freeze")** → 0.6.1 (Feb 2) →
0.6.2 (Feb 6) → 0.6.3 (Mar 3; "AuthorizerHash is hash of codehash with param", metadata prefix for code blobs) → 0.6.4
(Mar 18; "Assurances are checked with the prior validator set", activity statistics, Ed25519 keys in epoch marker) → 0.6.5
(Apr 22; gas limit in operand tuples, `provide` host call, imports/exports separated) → 0.6.6 (May 5; max code sizes,
oversize reports handled, posterior state root finalised) → 0.6.7 (May 29; "super-fetch", "gratis storage", account
metadata, stricter opcode/jump validity) → **0.7.0 (25 Jun 2025; "Macrofication Marathon"; all variable-length items moved
to end of encodings; fixed-length validator-index serialization; MMR super-peak removal; W* depends on ρ†)** — the version
at which M1 evaluation could begin (PolkaWorld/0xjunha) → **0.7.1 (26 Jul 2025; `accumulate` combined with `on_transfer`;
core index added to refine args; version byte for accounts; "Small service IDs"; "Owned Privileges"; erasure-coding
equation fixes; guarantor assignments with full keys; core index removed from guarantee payload)** → **0.7.2 (15 Sep 2025;
info host call registers 9/10; preimage-integration simplification; explicit OOG checks per invocation; transfer gas
charge fix; WP size limits fix)** — the version used for the M1 fuzzing/conformance audits → **0.8.0 (3 Jun 2026)**:
"Add back processed transfer count to service statistics" (#502), "Support smaller validator sets" (#514), "Restrict
bless to manager service" (#519), "Update authorizer identification" (#522), "Keep full guarantees in availability
assignments state (rho)" (#494), "Propose change of extrinsic hash definition to allow checking for individual extrinsic
preimages" (#524), "Expose lookup anchor posterior root and anchor slot in refinement context" (#526); gas: "Charge gas
for illegal memory access instruction" (#497), "Add a new gas cost model" (#508), "Account for gas reserved by transfer
and always acc items" (#500), "Host function gas costs" (#517); smaller: "Safrole refinement" (#496), preimage length
< 2^32 (#520), "Limit the number of parallel inner VMs in refine" (#521), "Remove unused arguments from refine hostcalls"
(#528), ticket-entries constant → equation (#527), "Introduce hard-limits on the size of dispute extrinsics, and remove
culprits requirement" (#525); nits incl. "PVM has three invocation types" (#511). No release between 0.7.2 and 0.8.0.
GP Editorial Board/Committee (led by Gavin Wood) decides protocol updates (Bitget interview); 0.8.0 contributors include
zdave-parity, davxy, koute, arkpar, tomusdrw, bkchr, cheme, sierkov, alxmirap, 0xjunha.

---

## E. Implementations

### E.1 Registered clients (graypaper.com/clients — 45 entries; language set in brackets)
Go [A]: goberryjam (Rick Carback), Gossamer (ChainSafe), JAM DUNA (Sourabh Niyogi), Jamaica (rmagon), Jamgo (Marcus
Pang), Jamzilla (ascriv), New JAMneration, Strawberry (Eiger), subjam (nathanccxv). Java [A]: JavaJAM (javajam.io).
C/C++ [B]: Block Cowboys, Marmalade (sisco0), MORUM (qdrvm.io), TurboJAM (r2rationality — in conformance list, not on this
page). Rust [B]: FastRoll (0xjunha), Gooseberry (gilescope), Grey (sorpaas), Jamers/jam-rs (Shifting Pigeon), JamLiquor,
PolkaJam (Parity), SpaceJam (clearloop), UNIVERSALDOT, Vinwolf (vinsystems). Swift [B]: Boka (Acala/Laminar Labs),
Martlet (finsig). Zig [B]: Jam With Zig (rosarp), JamZig (jamzig.dev). Common Lisp [C]: Jam on the Lisp / JOTL (polykrate).
Haskell [C]: JAMLabs (mlabs). Python [C]: Jampy (DaKKK), PyJAMaz (JAM.tech / JAMdot Technologies), Tessera
(chainscore.finance), TRAM (Python+Rust). TypeScript [C]: @interweb/jamx, Clawbird (ltfschoen), PeanutButterAndJAM
(esscrypt), TSJam (prematurata/vekexasia), Typeberry (Fluffy Labs). Elixir [D]: Graymatter (JamBrains), Jamixir
(jamixir.org), Jelix (Block Dudes). Julia [D]: Blockage (OscarGB), Jelly (Zondax). OCaml [D]: Po-jam-l (Mark Petruska).
Scala [D]: JAM Forge (philoniare), Jam4s. Also Jambda (ArcheLabs), lasair (abutlabs) from the PR list. Set Z: none.

### E.2 Status & links (as of 25 Aug 2026)
- **Passed M1 Fellowship interview (referenda 595–598, deciding):** PyJAMaz (Python, https://github.com/JAMdotTech/pyjamaz;
  team Emiel/Arjan/Matthijs/Peter; "JAM Implementers #5" video https://www.youtube.com/watch?v=CCnexKXMtCk); JamBrains
  graymatter (Elixir; kianenigma, ggwpez, franciscoaguirre); Typeberry (TypeScript, https://github.com/FluffyLabs/typeberry —
  README: M1 complete (block import, W3F vectors, fuzzer, perf), M2 partial (networking, fast PVM); tools pvm-debugger,
  Gray Paper Reader https://graypaper.fluffylabs.dev/, state viewer, "Ananas" AssemblyScript PVM; "we do not accept any
  external PRs unless the contributor waives any claims to the prize"); JamZig (Zig, https://github.com/jamzig — solo dev
  Boy Maas; ~2,000 commits / 108 PRs Aug 2024–Dec 2025; "Development is currently happening in private"; side projects
  Polana (SVM on JAM) and Akasha Void).
- **Passed W3F 1M-step fuzzing:** SpaceJam (Rust, clearloop — fastest non-Parity on the dashboard, "11s → 0.6s"
  recompiler speedup), TSJam (vekexasia), JavaJAM (jaymansfield), Jampy (dakk, https://github.com/dakk — fuzzer-target
  releases), Jamixir (danicuki/daiagi, also passed Parity audit May 26 2026; "JAM Implementers #4" video
  https://www.youtube.com/watch?v=gKrWeXKorEM), JamForge (self-attested via jamtoaster).
- **Submitted, no public result:** JAM DUNA (Go; https://github.com/jam-duna/coreplay, jamtestnet; Sourabh Niyogi; also
  jam-etl Dune/BigQuery PoC), Jamzilla (ascrivener), PeanutButterAndJAM, Vinwolf (bloppan), Boka (Swift,
  https://github.com/open-web3-stack/boka "brought to you by Laminar Labs"; RPC 127.0.0.1:9955; RocksDB), New JAMneration,
  FastRoll (0xjunha, fastroll-jam org), Jam4s (celadari, tommyldev, sergey-astapov, subotic; jam4s.org blog incl. "Safrole
  Algorithm Demystified"), Tessera (Chainscore), Strawberry (Eiger, https://github.com/eigerco/strawberry — MIT; Docker
  fuzz mode; M1 first submitted Nov 20 2024), TurboJAM (C++, sierkov), Gossamer-Jam (ChainSafe, aang114), JOTL, Jambda,
  lasair.
- **PolkaJam (Parity, Rust):** https://github.com/paritytech/polkajam-releases — "All PolkaJam releases are currently binary
  only, to avoid intentional or unintentional violation of the JAM prize's clean-room rule"; source "will be released in the
  future, once the JAM prizes have been awarded"; 374 releases, latest nightly-2026-06-06; tops the conformance dashboard
  (recompiler); `polkajam` / `cargo-polkajam` / `jam-types` crates on crates.io.
- Public team write-ups on tricky GP parts found: Jam4s "Safrole Algorithm Demystified" (https://www.jam4s.org/blog/…);
  JamZig delivery doc ("precision at the bit-and-byte level demands rigorous discipline"); TurboJam issue #26 (gas
  divergences in preimages traces; request for PVM traces in fuzz reports); sierkov discussion on recent_history (β)
  serialization order vs GP 0.7.2; Fluffy Labs' Gray Paper Reader (version diffs/notes) & PVM debugger (Polkadot treasury
  retroactive funding post 2578); JAM DUNA docs (fuzzer, traces, 6-validator testnet). The JAM Implementers YouTube series
  (#4 Jamixir, #5 PyJAMaz) and the JAM0 implementers meetup (sub0/Devcon 7, Bangkok Nov 2024,
  https://forum.polkadot.network/t/jam0-jam-implementers-meetup-sub0-devcon-7-bangkok-nov-11-nov-16-2024/10866).

---

## F. 50 architecture / design-rationale facts likely to be probed (each with a source URL)

1. JAM = Join-Accumulate Machine; the name comes from CoreJam's collect/refine/join/accumulate model; only Join and Accumulate run on-chain, Collect and Refine are off-chain/in-core. — https://raw.githubusercontent.com/gavofyork/graypaper/main/text/intro.tex ; https://wiki.polkadot.com/learn/learn-jam-chain/
2. "An early, unrefined, version of this protocol was first proposed in Polkadot Fellowship RFC 31, known as CoreJam." — intro.tex; RFC text https://raw.githubusercontent.com/polkadot-fellows/RFCs/gav-corejam/text/0031-corejam.md
3. Five driving factors: Resilience, Generality, Performance, Coherency, Accessibility (verbatim definitions in D.1). — intro.tex
4. Size–coherency antagonism: bigger state-space ⇒ less coherence (causality/latency); JAM's answer "pipelines a highly scalable, mostly coherent element to a synchronous, fully coherent element" using "a form of cache affinity" instead of crude partitioning. — intro.tex
5. JAM is "a mostly-coherent trustless supercomputer" and "a sweet spot" between fully synchronous (Solana-style) and persistently fragmented (Polkadot/Cosmos/rollup) designs. — https://graypaper.com/ ; text/conclusion.tex
6. Why not SNARK rollups for scaling: RISC-Zero-style proving is "over 61,000 times" slower / "66,000,000x" costlier; even "50,000x" is "several orders of magnitude greater than would be required to compete on a cost-basis with established crypto-economic techniques"; SNARK sequencers tend to centralise. — text/previous_work.tex
7. Why not Polkadot 1.0 as-is: parachains are isolated, XCMP is "asynchronous, coarse-grained"; Polkadot is "a collection of independent ecosystems"; access limited to ~50 auction slots. — text/previous_work.tex
8. Why not Solana-style synchrony: outages ("11 significant outages … 15 days"), 512 GB RAM validators, centralised storage — sacrifices resilience/decentralisation. — text/previous_work.tex
9. In-core/on-chain dualism: in-core = only the assigned validators execute (≈300× throughput), secured by ELVES' guarantee/assure/audit/dispute game; on-chain = every validator executes (Accumulate). — text/overview.tex ; https://blog.kianenigma.com/posts/tech/demystifying-jam/
10. Refine is stateless (arbitrary input, big compute: 5×10^9 gas per package, ~13.6 MB bundle, 48 KiB output); Accumulate is stateful, small (10^7 gas per report; 3.5×10^9 per block) and sequential-ish — "This separation allows services to scale dramatically both in the size of their inputs and in the complexity of their computation." — text/overview.tex ; text/definitions.tex
11. Services replace Ethereum's account dichotomy: code + balance + state, permissionless to create ("akin to deploying a smart contract"), with entry points is-authorized / refine / accumulate (on_transfer merged into accumulate in GP 0.7.1). — https://wiki.polkadot.com/learn/learn-jam-chain/ ; https://github.com/gavofyork/graypaper/releases/tag/v0.7.1
12. JAM is transactionless: the only extrinsics are tickets, preimages, guarantees, assurances, disputes — all produced by validators; user input enters via work packages and coretime/authorizers. — text/overview.tex ; wiki
13. Coretime is purchased in advance and assigned to an *authorizer* (hash of auth code hash ++ config), decoupling "who may use the core" from "who signs" — "Authorization logic is entirely arbitrary…"; guarantors are paid for any authorized package even if refine panics. — RFC-31; text/work_packages_and_reports.tex; GP PR #522
14. Why the header carries the *prior* state root: "to facilitate the pipelining of block computation and in particular of Merklization" (≈5% of work up-front, ≈95% accumulation later; ~3–3.5 s effective compute per 6 s slot). — text/header.tex ; wiki
15. Timing: 6-second slots, 600-slot (1 h) epochs, JAM Common Era = 2025-01-01 12:00 UTC. — text/overview.tex ; text/definitions.tex
16. 1,023 validators, 341 cores, 3 guarantors per core, rotation every 10 slots; GP 0.8.0 allows smaller sets (≥6, multiple of 3; active cores scale). — text/discussion.tex ; https://github.com/gavofyork/graypaper/pull/514
17. Why Safrole (vs BABE): anonymous, ticket-based, "almost entirely fork-free" slot assignment using a Bandersnatch RingVRF; a slot's author has "a very high degree of anonymity", which resists targeted DoS and yields "a high-quality pool of entropy". — text/safrole.tex ; https://wiki.polkadot.com/learn/learn-safrole/
18. Safrole is "a simplified variant" of Sassafras — simplified "To follow in the footsteps of Ethereum yellow paper" (implementation diversity). — text/safrole.tex ; wiki
19. Ticket contest closes at slot 500 of 600 (C_epochtailstart); tickets sealed outside-in; fallback keys (from η2) if the accumulator isn't full; N = ⌈2E/|γk|⌉ tickets per validator; best-chain rule prefers chains with more ticket-sealed ancestors. — text/safrole.tex ; text/best_chain.tex
20. Entropy: four accumulators η0..η3; rotate at epoch change; VRF signature in every header feeds η0; seal/entropy contexts `$jam_ticket_seal`, `$jam_fallback_seal`, `$jam_entropy`. — text/safrole.tex
21. Grandpa provides finality; Beefy (BLS12-381 over Keccak of the accumulation-output MMR) provides "concise proofs of finality to third-party systems" for bridging. — text/best_chain.tex ; text/beefy.tex
22. Availability uses systematic Reed–Solomon in GF(2^16): 342 of 1,023 chunks reconstruct ("even should almost two-thirds of the v validators be malicious or incapacitated"); segment = 4,104 B ⇒ 6 two-byte pieces per validator. — text/erasure_coding.tex
23. Two DA systems: audit DA (work-package bundle shards, needed for auditing) and import/segment DA (exported segments, kept ≥28 days, 4,104-byte segments, ≤3,072 imports/exports per package). — text/assurance.tex ; text/work_packages_and_reports.tex
24. A report becomes available only with a 2/3+1 supermajority of assurances; unavailable reports time out after 5 slots (C_assurancetimeoutperiod). — text/reporting_assurance.tex
25. Why auditing: ELVES — random, deterministic VRF-selected auditors, tranches every 8 s, escalation on negative judgments or no-shows (bias factor 2); a report is audited at >2/3 positive judgments. — text/auditing.tex ; https://eprint.iacr.org/2024/961
26. Why disputes: "an important security backstop for removing and banning invalid work-reports from the processing pipeline"; JAM keeps an on-chain offenders record and delegates slashing to the staking layer. — text/judgments.tex
27. Verdict thresholds: positive needs 2/3+1; ≤1/3 positive ⇒ "wonky"; culprits (guaranteed a bad report) & faults (contradictory judgment); 0.8.0 caps verdicts/offenses at 16 per extrinsic. — text/judgments.tex ; GP PR #525
28. Guarantees: 2 of 3 guarantor signatures suffice; guarantors may be from the current or previous rotation; anchor must be within the 8-block recent history; lookup anchor ≤14,400 slots (24 h); no core may hold two pending reports. — text/reporting_assurance.tex
29. Why the accumulation queue: reports whose prerequisites/segment-root lookups are unmet are queued (ϑ) and later unlocked; accumulated hashes kept for one epoch (ξ); invalid dependencies cancel. — text/accumulation.tex ; jamtestvectors stf/accumulate
30. Why accumulate is gas-limited and ordered: per-block cap 3.5×10^9 gas, per-report 10^7; actual gas known only after execution ⇒ sequential Δ_seq vs batched-per-service Δ_par; always-accumulate privileged services go first; deferred transfers never run parallel with the recipient's supervisor logic. — text/accumulation.tex
31. Privileged services χ: manager (may `bless`), assigners (per core; `assign`), delegator (`designate`), registrar, always-accumulate set; GP 0.8.0 restricts `bless` to the manager after an identified self-privilege exploit. — GP PR #519 ; text/pvm_invocations.tex
32. Service economics: min balance = max(0, 100 + 10·items + 1·octets − gratis) with items = 2·|requests| + |storage|; balances are u64; deposits deter state bloat. — text/accounts.tex ; text/definitions.tex
33. Preimage lookup lifecycle encodes availability history as 0–3 timeslots ([] requested, [t0] available, [t0,t1] withdrawn, [t0,t1,t2] re-available); expunge after 19,200 slots (32 h) "so that any validator can verify whether a preimage was available at any time within the period where auditing may occur". — text/accounts.tex
34. State is ~16 largely independent components (α φ β γ ψ η ι κ λ ρ τ χ π ϑ ξ θ + δ services) keyed by a 31-byte state-key constructor C, enabling parallel STF computation. — text/overview.tex ; https://docs.jamcha.in/advanced/storage/keys
35. State Merklization: binary Patricia Merkle trie, 512-bit nodes, values ≤32 B embedded in the leaf, Blake2b — "a format optimized for modern compute hardware". — text/merklization.tex
36. Serialization is SCALE-like but with its own compact integer scheme; GP 0.7.0 moved all variable-length fields to the end of encodings (streaming/pipelining friendliness). — text/serialization.tex ; jamtestvectors codec README ; v0.7.0 release
37. Why PVM is RISC-V based (RV64EM-like: 64-bit, 13 registers, no floats): easy JIT/recompilation to x86-64/ARM, LLVM toolchain, determinism, metering-friendliness, and continuations/pause-resume (needed for CorePlay). — https://wiki.polkadot.com/learn/learn-jam-chain/ ; text/overview.tex ; Demystifying JAM
38. Why not Wasm: non-deterministic features baked in (floats), poor metering fit, stack handling; PVM "disallow[s] all unneeded behaviors". — https://medium.com/@francomangone18/blockchain-101-jam-2d64de1cab1d ; wiki
39. PVM exit conditions are exactly halt / panic / out-of-gas / page-fault(addr) / host-call(id); unknown host calls cost C_gasunknown = 1000 and return WHAT. — text/pvm.tex ; text/pvm_invocations.tex
40. PVM memory: 32-bit address space in 4 KiB pages, 64 KiB zones, standard init layout (RO data, heap, stack, args), register init r0 = 2^32−2^16 (halt address), r1 = SP, r7 = arg ptr, r8 = arg len. — text/pvm.tex
41. GP 0.8.0 gas model charges per basic block using a simulated micro-architecture (ROB, execution units, cycles) instead of 1 gas/instruction; `sbrk` → `grow_heap` host call; JIT-oriented. — https://github.com/gavofyork/graypaper/pull/508
42. Dynamic jumps must be 2-aligned because "LLVM requires and assumes … that dynamically computed jump destinations always have a certain memory alignment". — text/pvm.tex (footnote)
43. Three PVM invocation types (is-authorized, refine, accumulate) with distinct host-call sets; refine-only calls (historical_lookup, export, compile, machine, peek, poke, pages, invoke, expunge) enable nested PVMs; accumulate-only calls mutate state (bless, assign, designate, checkpoint, new, upgrade, transfer, eject, query, solicit, forget, yield, provide). — text/pvm_invocations.tex
44. `fetch` gives programs access to protocol constants and package/operand data (selectors 0–15) — the same encoding JIP-4 uses for `protocol_parameters`. — text/pvm_invocations.tex ; https://raw.githubusercontent.com/polkadot-fellows/JIPs/main/JIP-4.md
45. CoreChains service = Polkadot parachains on JAM (PVF retargeted from Wasm to PVM; full XCMP); CorePlay = synchronous-feeling actor smart contracts via pause/resume; CoreVM etc. are just services — JAM itself has no "parachain" concept. — wiki ; Demystifying JAM ; RFC-31
46. JAM is "less opinionated" than Polkadot 1.0 and *non-upgradable*: "upgradability responsibility shifted to services"; it ships as "a comprehensive singular upgrade" approved by OpenGov; DOT remains the native token ("No other native token will be issued"); JAMKB is a resource token, not a currency. — wiki JAM chain + FAQ ; forum 13029 ; Aug 2026 digests
47. Reference hardware & budgets: 16 cores / 64 GB / 8 TB / 0.5 Gbps; CPU 10/16 for audits; ~387 MB/s out, 357 MB/s in; ≈682 MB/s DA and 85× Polkadot compute; 171k–1.4M TPS models; EVM 500–5,000 gas/µs per core. — text/discussion.tex
48. Networking is deliberately outside the GP (JAMNP-S: QUIC/TLS1.3/Ed25519 certs, grid diffusion, UP/CE streams) and RPC (JIP-2, JSON-RPC/WebSocket 19800) is an interim "evil" — light clients are the goal. — https://docs.jamcha.in/knowledge/advanced/simple-networking/spec ; JIP-2
49. Multiple independent implementations are a security feature: W3F's prize ("a truly decentralized protocol should be able to support multiple client implementations"); ref 682 requires three independent block-producing implementations passing conformance/performance before the relay chain halts. — https://medium.com/web3foundation/announcing-the-jam-implementers-prize-e79f8ebc506d ; https://polkadot.subsquare.io/referenda/682
50. Conformance = same state root after every imported block under fuzzing (Unix-socket fuzz protocol; ancestry + forking features mandatory for M1; W3F's "1 million steps" benchmark), then Parity audit, then a recorded Fellowship interview ratified by an on-chain remark ("approves in full"). — https://raw.githubusercontent.com/davxy/jam-conformance/main/fuzz-proto/README.md ; https://github.com/w3f/jam-milestone-delivery/pull/20 ; https://collectives.subsquare.io/fellowship/referenda/595

---

## Source index (primary URLs used)
- https://jam.web3.foundation/ · https://jam.web3.foundation/rules · https://hackmd.io/@polkadot/jamprize
- https://github.com/w3f/jam-milestone-delivery (README, docs/T&Cs.md, deliveries/milestone-delivery-template.md, PRs #5–#44)
- https://collectives.subsquare.io/fellowship (referenda 595–598; API /api/fellowship/referenda/<n>)
- https://polkadot.subsquare.io/referenda/682 · https://forum.polkadot.network/t/what-is-the-status-of-jam-development/17368 · https://forum.polkadot.network/t/polkadot-socials-daily-digest-2026-08-09/18378
- https://github.com/polkadot-fellows/JIPs (JIP-1..5; PRs #3, #14, #15)
- https://github.com/w3f/jamtestvectors (README, CHANGELOG, stf/*/README.md, traces, codec, shuffle, pvm PR #3)
- https://github.com/davxy/jam-conformance (README, fuzz-proto, fuzz-reports, issues, discussions) · https://paritytech.github.io/jam-conformance-dashboard/ · https://fuzz.jamtoaster.network/ · https://github.com/jam-duna/jamtestnet
- https://graypaper.com/ (+/news, /resources, /clients, /tour, /lectures, /prize) · https://github.com/gavofyork/graypaper (releases v0.4.3…v0.8.0; PRs #494, #508, #514, #519, #522, #525, #526; text/*.tex)
- https://raw.githubusercontent.com/polkadot-fellows/RFCs/gav-corejam/text/0031-corejam.md
- https://blog.kianenigma.com/posts/tech/demystifying-jam/ · https://www.parity.io/blog/JAM-demystified-explainer · https://wiki.polkadot.com/learn/learn-jam-chain/ · https://wiki.polkadot.com/learn/learn-jam-faq/ · https://wiki.polkadot.com/learn/learn-safrole/ · https://docs.jamcha.in/
- https://forum.polkadot.network/t/introducing-a-new-jam-token/13029/43 · https://forum.polkadot.network/t/polkadot-3-0-the-jam-upgrade/13834 · https://forum.polkadot.network/t/minijam-a-parachain-running-a-streamlined-jam/18120
- https://decrypt.co/227221/… · https://decrypt.co/229293/… · https://decrypt.co/resources/what-is-jam-polkadots-biggest-ever-upgrade-explained · https://www.bitget.com/news/detail/12560605055985 · https://polkadotters.medium.com/polkadot-jam-explained-simply-825ec8b24607 · https://medium.com/@francomangone18/blockchain-101-jam-2d64de1cab1d · https://blockeden.xyz/blog/2026/01/16/… · https://github.com/openguild-labs/learn-jam
- https://github.com/davxy/bandersnatch-vrf-spec · https://eprint.iacr.org/2024/961
- Implementations: https://github.com/FluffyLabs/typeberry · https://github.com/paritytech/polkajam-releases · https://github.com/eigerco/strawberry · https://github.com/open-web3-stack/boka · https://github.com/JAMdotTech · https://github.com/jam-duna · https://jamzig.dev/ · https://jamixir.org/ · https://www.jam4s.org/
- Matrix archives (partially fetchable): https://paritytech.github.io/matrix-archiver/ (#jam:polkadot.io, #graypaper:polkadot.io, #jam-conformance:matrix.org)
