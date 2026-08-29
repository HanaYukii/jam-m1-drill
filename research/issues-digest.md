# New-JAMneration/JAM-Protocol — Issues/PR research digest (for M1 exam quiz prep)

Repo: https://github.com/New-JAMneration/JAM-Protocol (Go implementation of JAM; team "New JAMneration").
Compiled 2026-08-26 via WebFetch of github.com issue pages + api.github.com/search/issues (`in:title` keyword searches, 10 results/page).
Access notes: `?q=` search pages are robots-blocked; milestone pages only show the first 25 (JS "Load more"); core REST API rate-limited (403). Coverage is therefore keyword-driven, not exhaustive. Issue numbers run #1..#1046 (issues and PRs share the counter).

Milestones: "Milestone v1.0" (https://github.com/New-JAMneration/JAM-Protocol/milestone/4, 164 closed, 100%) and "Milestone v2.0" (milestone/6, 20 open / 12 closed as of fetch).
Open issues at fetch time (30): #1044, #1037, #1022, #1012, #974, #968, #967, #966, #965, #958, #953, #942, #847, #849, #850, #827(PR), #814, #773, #736, #641, #568, #567, #566, ...

---

## 1. Index of issues/PRs grouped by keyword (deduplicated; `#n | state | kind | title`)

### Safrole / tickets / sealing / entropy / epoch (GP ch.6)
- #1013 | closed | issue | feat(safrole): align GP v0.8.0 Chapter 6 Safrole
- #1025 | closed | PR | feat(safrole): dynamic ticket cap + per-block K cap (GP v0.8.0) (#1013)
- #1040 | closed | issue | refactor(safrole): ring verifier cache keyed by epoch forces rebuild on every fork-restore
- #1041 | closed | PR | refactor(safrole): cache ring verifier by validator-set hash, not epoch
- #1038 | closed | PR | feat(networking): Safrole timing from ConnectivityApplied and topology smoke harness
- #1035 | closed | PR | feat(codec): ticket entry-index encode[1] + validator-set var prefixes + original_shards(v) (GP v0.8.0) (part of #1022)
- #1031 | closed | PR | feat(header): BlockInfo timeslot + epoch-mark length prefix + preimage-hash extrinsic commitment (GP v0.8.0)
- #949 | closed | issue | feat(telemetry): safrole + preimage events (80-84, 190-199)
- #778 | closed | PR | 770 fix invalidepochmark preimage not required  (issue #770)
- #766 | closed | PR | refactor: Errorcode Shooting to Str, Implement-related Error Close Conn & include header entropy validation
- #730 | closed | issue | test: Traces Safrole Test Along w/ GP 0.7.1
- #536 | closed | PR | Feat: STF safrole and preimages
- #517 | closed | issue | feat: STF Safrole
- #277 | closed | issue | chore: demo for safrole
- #76 | closed | PR | feat : create extrinsic_controller, ticket, dispute controller
- (numbers lost by fetch, safrole search p.2): "Test: Check update_safrole.go Renew Along w/ GP 0.6.7"; "fix: use latest block instead of processing (update_safrole)"; "Bug: (GP 6.24) condition setup is wrong in safrole/sealing.go"; "[WIP] feat: add safrole functions in cmd for testing"; "refactor: add total state to substitue the safrole state"; "feat: create safrole type by asn.1"; "feat: align types of jam_types and safrole"

### Disputes / verdicts / culprits / faults (GP ch.10)
- #1017 | closed | issue | feat(disputes): align GP v0.8.0 disputes and judgments
- #1032 | closed | PR | feat(disputes): verdict judgment length prefix + extrinsic caps + drop culprits rule (GP v0.8.0) (#1017)
- #1042 | closed | PR | chore(v0.8.0): integrate reporting, header, disputes, and accumulation stack
- #665 | closed | issue | Test: Check update_dispute.go Renew Along w/ GP 0.7.0
- #653 | closed | PR | Fix assurance test & refactor dispute test
- #542 / #543 | closed | PR | 509 feat stf dispute(s)
- #509 | closed | issue | feat: STF Dispute
- #291 | closed | PR | 281 test dispute with all test vectors
- #529 | closed | issue | feat: GetJudgement into auditing flow — Ξ(p,c) re-execution & node integration
- #939 | closed | PR | fix/test: Stage 2 BuildJudgements key bug + tranche tests

### Reporting / guarantees / assurances / availability (GP ch.11)
- #1016 | closed | issue | feat(reporting): align GP v0.8.0 reporting and assurances
- #1027 | closed | PR | feat(reporting): add anchor_slot + lookup_anchor_state_root to RefineContext (GP v0.8.0) (#1016)
- #1026 | closed | PR | feat(work-package): add erasure_shards to WorkPackageSpec (GP v0.8.0)
- #869 | closed | PR | fix: update guarantees counting logic
- #863 | closed | issue | Fix: guarantor sorted and unique bug
- #864 | closed | PR | fix: guarantor unique
- #862 | closed | PR | fix: rename report-oversize to output-oversize
- #854 | closed | PR | feat: add ancestry to store and fix guarantee slot validation
- #853 | closed | issue | feat: using ancestry to validate reports and support fuzz feature
- #892 | closed | issue/PR | fix: add timeslot validation with ancestry
- #797 | closed | PR | Refactor/fuzz mismatch report
- #721 / #722 | closed | PR | 619 refactor update pvm invocation guarantee gp v071 (+ Revert)
- #619 | closed | issue | refactor: Update PVM Invocation, Guarantee GP v0.7.1
- #671 | closed | PR | 623 refactor update reporting assurance gp v071
- #623 | closed | issue | refactor/test: Update Reporting and Assurance GP v0.7.1 and STF Test
- #625 | closed | PR | refactor:test and update GP 0.6.7 reports stf
- #663 | closed | issue | Test: Check update_reports.go Renew Along w/ GP 0.7.0
- #664 | closed | issue | Test: Check update_assurance.go Renew Along w/ GP 0.7.0
- #607 | closed | issue | Test: Check update_assurances.go Renew Along w/ GP 0.6.7
- #624 | closed | PR | [WIP] fix: assurance json tests.
- #526 | closed | PR | Adding STF-based assurances tests.
- #280 | closed | PR | 244 test whole assurances
- #191 | closed | PR | feat: add guarantor_assignments 11.18 - 11.22
- #950 | closed | issue | feat(telemetry): guaranteeing events (90-113)
- #951 | closed | issue | feat(telemetry): availability + bundle events (120-153)
- #1007 | closed | PR | feat(telemetry): IsAuthorized/Refine cost sidecar to guarantor layer (#974 Phase 1a)

### Accumulation / deferred transfers / privileged services (GP ch.12, ch.9)
- #1019 | closed | issue | feat(accumulation): align GP v0.8.0 accumulation
- #1033 | closed | PR | fix(accumulation): eq:accseq gas budget + processed-transfers output (GP v0.8.0)
- #1024 | closed | PR | docs(accumulation): align ϑ/ready-queue comments with GP v0.8.0
- #838 | closed | issue | refactor: parallelize accumulation by goroutine
- #856 / #873 | closed | PR | feat: parallelize accumulation per core by goroutine
- #880 | closed | PR | fix: correct UnmatchedKeyVals merge semantics in parallelized accumulation
- #829 | closed | PR | fix: accumulate nil and {} comparison
- #977 | closed | PR | fix: bless-overflow and chi-assign initialization
- #882 | closed | PR | fix: filter DeferredTransfers for deleted services in tPrime
- #986 | closed | issue | Bug: CalcThresholdBalance missing - aF in return value (GP 9.8)
- #987 | closed | PR | fix: CalcThresholdBalance return value
- #656 | closed | PR | fix: remove transfers stats from service record
- #504 | closed | issue | refactor: Move Accumulation and DeferredTransfers Statistics into IntermediateStates
- #452 | closed | PR | chore: update some accumulate host call functions.
- #449 | closed | PR | chore : update service account
- #580 | closed | issue | refactor: Recent history and LastAccOut type and funcs, remain test

### Preimages / lookups / service storage (GP ch.9, 12.x)
- #741 | closed | issue | fix: Preimages Error Code 0
- #746 | closed | PR | fix: Preimages Error Code 0
- #728 | closed | issue | test: Traces Preimages / Preimages_light Test Along w/ GP 0.7.1
- #725 | closed | issue | test: STF Test Update Chapter 12 Preimages GP v0.7.1
- #805 | closed | PR | feat: track unmatched lookup keyvals in state parsing
- #985 | closed | PR | feat(tests): add preimage filtering tests and utility functions
- #779 | closed | issue | Bug: using 0xff to decode service-related field may occur error
- #780 | closed | PR | Fix 0xff prefix decode issue for service-related field
- #938 | closed | PR | Fix: cross-service storage loss in read host call causing state_root mismatch
- #979 | closed | issue | Write host call mutates StorageDict before balance check, causing state mismatch
- #980 | closed | PR | fix(pvm): move StorageDict mutation after balance check in write host call

### Statistics (GP ch.13)
- #1021 | closed | issue | feat(statistics): align GP v0.8.0 validator activity statistics
- #1034 | closed | PR | feat(statistics): assurances before rollover + 3-tuple accumulation stats + C(13) prefixes (GP v0.8.0) (#1021)
- #710 | closed | issue | Fix: Statistics GP 0.7.0 13.5 Just Follow Formula
- #711 | closed | PR | 710 fix statistics gp 070 135 just follow formula from696
- #621 | closed | issue | refactor: Update Statistics GP v0.7.1
- #514 | closed | issue | feat: STF Statistics
- #482 | closed | PR | feat: statistics v0.6.4
- #507 | closed | PR | refactor: Move statistics into intermediate state
- #515 | closed | PR | feat: Add statistics logic to cli

### Authorization (GP ch.8)
- #1020 | closed | issue | feat(authorization): align GP v0.8.0 authorization pool and queue
- #692 | closed | issue | Bug: Fix the logic of remove duplicate of AuthorizerHash GP 0.7.0  (PRs #693, #694)
- #468 | closed | issue | feat: chatper 8 Authorization (GP 0.6.5) ; #480 PR feat: chatper 8 authorization gp 065 ; #474 PR add the authorization Dump
- #512 | closed | issue | feat: STF Accumulate, History, Authorizations (PR #516)
- #646 | closed | PR | Feat/Test: Check update_history/authorizations/preimages Renew Along w/ GP 0.6.7

### Additional bug/fix issues found via "bug|mismatch|wrong|fix" title searches
- #284 | closed | issue | Bug: (GP 6.24) condition setup is wrong in safrole/sealing.go  (PR #285)
- #667 | closed | issue | bug: Fix the parallelized accumulation function. (PR #668)
- #703 | closed | PR | fix: Fix formula for LastAccumulationSlot in deferred transfers accumulation
- #705 | closed | PR | fix: Refactor: Update Accumulation GP v0.7.1 DeltaDoubleDagger by the deferred_transfer major logic change
- #712 | closed | issue | refactor: Update Accumulation GP v0.7.2 (PRs #812, #818)
- #652 | closed | PR | [WIP] Fix/update accumulation tests v067
- #783 | closed | PR | fix: wrong StateCommit timing
- #791 | closed | PR | feat: Add vrf verification unit test use posterior state to fix the key rotation bug
- #819 | closed | issue | refactor/fix: Opt Some Initialisation & Fix The Deepcopy Bug (PR #820) ; #865 PR Fix: deep copy bug
- #821 | closed | issue | bug: accumulation might get assign with zero length
- #825 | closed | issue | fix: UpdateEtaPrime0 index out of range
- #828 | closed | issue | fix: v0.7.1 to release
- #860 | closed | issue | fix: GP 0.7.2 Bugs
- #935 | closed | issue | fix: ComputeInitialAuditAssignment missing ValidatorID
- #940 | closed | issue | fix: BuildJudgements signs with public key
- #1014 | closed | issue | feat(header): align GP v0.8.0 header and recent history
- #1015 | closed | issue | feat(work-package): align GP v0.8.0 work packages and bundles
- #1018 | closed | issue | feat(auditing): align GP v0.8.0 auditing and best chain
- #925 | closed | PR | feat: Validator grid and UP/CE networking infrastructure
- #952 | closed | issue | feat(telemetry): segment recovery events (160-178)
- #739 | closed | issue | test/refactor: 0.7.0 Fuzzer Traces (PRs #738, #744) ; #840 refactor: pass trace/fuzzy ; #726/#727/#729 Traces tests (fallback, storage) GP 0.7.1
- #795 | closed | PR | Database package and redis replacement ; #660 Introduce db package
- #698 | closed | issue | Review: Check ⟼ operator (sequence subtraction) usage GP 0.7.0
- #697 | closed | issue | Test: Check update_accumulates.go test status after PVM stable GP 0.7.0
- #709 | closed | issue | refactor: Update GP v0.7.2 (umbrella) ; #713 Update WP related GP v0.7.2 ; #716 Update PVM Invocation GP v0.7.2
- #765 | closed (wontfix) | issue | fix: 6.17 Verification & Error Massage Return Check (PR #766)
- #763 | closed | issue | refactor: Errorcode Shooting to Str, Implement-related Error Close Conn
- #753 | closed | issue | fix: Designated Error (PR #755)
- #785 | closed | issue | fix: Fuzz error message response pre state root (PR #782)
- #798 | closed | issue | refactor: Mapping `examples/v1` error messages ; #837 refactor: introduce layered logging / error handling
- #836 | closed | issue | feat: support ancestor feature for M1 (PR #830)
- #991 | closed | issue | Fuzz target crashes with disk exhaustion after 361K steps (PR #990)
- #983 | closed | issue | fix: fuzz target OOM crash due to unbounded in-memory state data (PR #984)

### PVM / host calls / gas (GP App. A-B)
- #1046 | closed | PR | feat: PVM update 0.8.0
- #1036 | closed | PR | Feat/pvm-0.7.2-recompiler (x86-64 JIT backend, ~19% STF speedup)
- #995 | closed | issue | refactor: predecode PVM blocks and instructions  (PR #994)
- #997 | closed | issue | PVM OOG check off-by-one in SingleStepStateTransition / SingleStepInvokeDecodedBlocks (GP A.6)
- #998 | closed | PR | fix(pvm): correct off-by-one in OOG check (GP A.6: rho < 1)
- #993 | closed | issue | bug: missing OOG check in hostCallException causes state mismatch during fuzzing
- #992 | closed | PR | fix: add OOG check for unknown host calls (GP v0.7.2)
- #975 | closed | issue | PVM logHostCall (host call 100) crashes target due to missing isReadable check
- #976 | closed | PR | fix(pvm): add isReadable check to logHostCall preventing nil deref crash
- #974 | open | issue | feat(pvm): cost instrumentation for JIP-3 events 47 / 95 / 101
- #883 | closed | PR | fix: sign-extend-bug
- #866 | closed | issue | Fix: 0.7.2 PVM bugs   (PR #885 Fix/0.7.2 pvm bugs)
- #822 | closed | PR | fix: PVM bugs
- #898 | closed | PR | refactor: Perf/PVM 0.7.2
- #857 | closed | PR | refactor: PVM 0.7.2
- #715 | closed | issue | refactor: Update PVM GP v0.7.2
- #809 / #810 | closed | PR | Revert "refactor: update pvm 0.7.1"
- #733 | closed | PR | refactor: PVM gas charging and log host-call
- #907 | closed | PR | ref: GP 0.7.2 refine host call   (issue #903 refactor: refine host calls)
- #841 | closed | PR | refactor: logger and PVM logger
- #576 | closed | issue | refactor: update PVM(independent) GP 0.6.7   (PR #573 "562 update pvm independent gp 067")
- #403 | closed | PR | Added host call tests and some test vectors.
- #847 | open | issue | feat: Gas Model 0.8.0
- #849 | open | issue | feat: gas model STF functions
- #850 | open | issue | feat: implement gas cost tables and pass test-vectors
- #881 | PR | feat: gas model stf ; #848 | closed | issue | feat: investigate gas model and implement the initial state

### Codec / serialization (GP App. C)
- #1022 | open | issue | feat(codec): align GP v0.8.0 serialization, erasure coding, VRF, and PVM
- #1037 | open | issue | feat: support variable validator-set size (|κ| ≠ V) across validation and codecs
- #1035 | closed | PR | (see Safrole) ticket entry-index encode[1] + validator-set var prefixes + original_shards(v)
- #923 | closed | PR | refactor: update TicketAttempt codec methods to use compact encoding
- #955 | closed | PR | test: Stage 3 CE144/CE145 codec edge cases
- #981 / #982 | closed | issue/PR | refactor: migrate WorkReportSerialization callers to types.Encoder.Encode
- #973 | closed | PR | feat(up0): add UP 0 wire codec for handshake and announcement
- #946 | closed | issue | feat(telemetry): Block Outline type + codec
- #999 / #1000 | closed | perf(types): avoid eager fmt.Sprintf in disabled SCALE codec debug logs
- #901 | closed | PR | feat: refine encode delta key val
- #535 | closed | PR | Feat/encode decode trace
- #531 | closed | PR | Fix/block serialization 066
- #483 | closed | PR | fix: Create parent hash using encoder
- #488 | closed | PR | refactor: Generate extrinsic hash using encoder
- #714 | closed | issue | refactor: Update Merkle & Serialization GP v0.7.2

### Merklization / MMR / state root (GP App. D-E)
- #889 | closed | issue | refactor: Merkle / MMR Optimisation
- #895 | closed | PR | refactor: Memory & small optimizations for MMR and Merkle tree
- #897 | closed | PR | refactor: string key in merklization
- #918 / #919 | closed | issue/PR | refactor: DeepCopy Opt and Merkle Tree Refactor
- #920 / #921 | closed | issue/PR | fix: merklization unit tests broken after Merkle tree refactor
- #900 | closed | PR | refactor: Merkle Leaf Level Cache Opt
- #731 | closed | PR | Implement basic storage of Merkle path storage to support CE129
- #1001 / #1002 | closed | perf(fuzz): ImportBlock recomputes the whole-state root 3x per block

### Erasure coding / VRF / Bandersnatch
- #1026 | closed | PR | feat(work-package): add erasure_shards to WorkPackageSpec (GP v0.8.0)
- #956 | closed | issue | test: ComputeAnForValidator stochastic VRF threshold (GP §17.14-17.15)
- #784 | closed | issue | fix: Header VRF Verification Failure on some cases
- #832 | closed | PR | refactor: vrf integration, one ring only
- #806 | closed | issue | refactor: Opt rust_VRF ffi ; #835 [WIP] Improve vrf performance ; #868, #913 rust-vrf submodule updates ; #1011 docs Rust-VRF FFI

### Fuzz / conformance / test vectors
- #1044 | open | issue | chore(v0.8.0): complete deferred cross-phase conformance follow-ups
- #827 | open | PR | refactor: fuzz folder
- #991 | closed | issue | Fuzz target crashes with disk exhaustion after 361K steps  (PR #990 prune persistent storage)
- #983 / #984 / #996 / #1003 | closed | fuzz OOM (unbounded in-memory state; TestFuzzReportsTrace OOM >30GB; evict old state)
- #959 | closed | PR | feat: enhance fuzz testing support with Docker integration
- #916 | closed | feat: Handle SIGTERM Gracefully in Fuzz Target
- #797 | closed | PR | Refactor/fuzz mismatch report
- #686 | closed | Trace history
- #930 / #936 | closed | PR | Stage 1 audit unit tests + fix ValidatorID assignment bug
- #939 | closed | PR | fix/test: Stage 2 BuildJudgements key bug + tranche tests

### Networking / JIPs / node
- #773 | open | issue | JIPs
- #777 | closed | issue | JIP-5: Secret key derivation
- #958 | open | issue | feat(telemetry): JIP-3 domain events umbrella (#775)
- #942, #953 | open | telemetry status events / e2e against JamTART
- #962, #963, #964, #965, #966, #967, #968, #1029 | Node phases (QUIC+TLS identity; stream runtime; bootstrap; UP0; CE128; topology; validator duties)
- #565 | closed | feat: Peering Module ; #566/#567/#568 parent node issues (open)
- #969 | closed | refactor(cert): ALPN generation ; #766 error codes / close conn

### Version migration
- #1012 | open | issue | Update to v0.8.0 (umbrella: phases #1013 safrole, #1014, #1016 reporting, #1017 disputes, #1019 accumulation, #1021 statistics, #1022 codec/EC/VRF/PVM, #1042 integration, #1044 follow-ups)
- #906 | closed | chore: Rename Variables and Functions to Fit Latest GP Nomenclature
- #714 / #715 | GP v0.7.2 (Merkle & serialization; PVM)
- #619 / #621 / #623 / #725 / #728 / #730 | GP v0.7.1 updates
- #663 / #664 / #665 / #710 | GP v0.7.0 checks
- #576 / #607 / #625 | GP v0.6.7 ; #531 (0.6.6) ; #480 (0.6.5) ; #482 (0.6.4)
- #814 | open | refactor: Future ~M1/M2


---

## 2. Detailed notes on protocol-relevant issues/PRs (grouped by GP area)

Format: `#n title (state, date)` — problem; GP rule involved; resolution; Quiz angle.

### Safrole / ch.6

- **#284 Bug: (GP 6.24) condition setup is wrong in safrole/sealing.go (closed, 2025-02-20, author yu2C, label bug; fixed by PR #285 merged same day by YCC3741)** — problem: line 177 of `internal/safrole/sealing.go` used `if ePrime == e+1 {` as the condition for choosing the sealing-key/ticket regime; the issue references GP eq. 6.24 (γ_s' selection: tickets used only when `e' = e+1 ∧ m ≥ Y ∧ |γ_a| = E`, otherwise fallback F(η_2', κ')) and the fix commit is "fix 6.27 condition" plus "fix set gammaS to DB" (γ_s must be persisted). Resolution: condition corrected to follow the GP equation (check the ticket-accumulator/lottery-closure conditions rather than just epoch+1). Quiz angle: *when exactly are tickets (γ_a) used as the next epoch's sealing keys vs. the fallback key sequence F? What are the three conjuncts (e' = e+1, m ≥ Y, |γ_a| = E) and what happens on a skipped epoch?*

- **#784 fix: Header VRF Verification Failure on some cases (closed, 2025-11-18, HanaYukii, bug; fixed by PR #791 "Add vrf verification unit test use posterior state to fix the key rotation bug", merged 2025-11-28)** — problem: fuzzer traces (e.g. `1758621879/00000348.json`) were misjudged as "header validate error: 7"; root cause was verifying the header seal / entropy VRF with the *prior* κ and η instead of the posterior κ' and η' (after epoch rotation the block is sealed by the new validator set with the new entropy). Resolution: "Using posterior state Kappa & Eta for correct Bandersnatch IETF verification"; reproducible test vector added; reviewer yu2C insisted header validation not be moved after safrole processing ("other components need to be verified"). Quiz angle: *which validator set and which entropy value verify H_s (seal) and H_v (VRF) of a block that is the first in a new epoch? (GP 6.15–6.18: seal uses κ' and η_3' via γ_s'; entropy VRF uses η_3' too; the epoch-change rotation κ' ← γ_k happens before sealing checks).*

### Authorization / ch.8

- **#692 Bug: Fix the logic of remove duplicate of AuthorizerHash GP 0.7.0 (closed, 2025-09-06, HanaYukii; PR #694 merged 2025-09-08 by TwEricShen)** — problem: when computing the posterior auth pool α', the implementation removed *all* occurrences of a used authorizer hash instead of just one, and did not match the core index of the guaranteed report. Resolution: "match the core index from report in guarantees" and "remove only the leftmost instance" of the authorizer hash; all three authorization test vectors pass. Quiz angle: *GP eq. for α' (ch.8): α'_c = ←(α_c minus the authorizer used by the report guaranteed on core c this block) ++ φ'_c[...] — only one instance is removed (a pool is a sequence, not a set), the queue element appended is φ'_c[H_t mod Q], and the pool is truncated to O entries (O=8).*

### Statistics / ch.13

- **#710 Fix: Statistics GP 0.7.0 13.5 Just Follow Formula (closed, 2025-09-24, YCC3741, bug; PR #711 by HanaYukii merged same day; "will be merged into #696")** — problem: validator statistics counted a validator multiple times; fix commit: "follow formula on graypaper for statistics calculation by only counting once for each validator". Resolution: per-validator counters (blocks, tickets, preimages, guarantees, assurances) follow GP 13.5 exactly: e.g. guarantees count = number of reports in E_G whose credentials include the validator's key (each report counted once per validator), assurances count = 1 if validator has an assurance in E_A. Quiz angle: *what exactly does π (validator statistics) count per validator: b (blocks authored), t (tickets introduced by the author), p (preimages) and d (preimage bytes) — author-only — versus g (guarantees) and a (assurances) which are per-validator by signature; and why "count once per validator".*

### Preimages / service accounts / ch.9 & 12.x

- **#741 fix: Preimages Error Code 0 (closed, 2025-10-19, YCC3741, bug; PR #746 by yu2C merged 2025-10-20 into the fuzz branch)** — problem: the `extrinsic_preimage` validity check was implemented as "length of timeSlotSet == 0" instead of "the lookup key (hash, length) exists in the service's lookup dictionary a_l with an empty timeslot set". Fuzzer case `1757406079/00000010.json` solved; two other cases (`1757406441/00000117.json`, `1757843609/00000034.json`) showed "no difference between preState and postState" (i.e. the block should have been rejected with an error, not applied). Quiz angle: *the preimage-provision rule (GP 12.x "E_P"): a preimage p for service s is only accepted if a_l[(H(p), |p|)] = [] (requested but not yet provided) — an *unrequested* preimage and an *already-provided* one are both invalid; also E_P must be sorted/unique by (s, p).*

- **#779 Bug: using 0xff to decode service-related field may occur error (closed, 2025-11-17, yu2C, bug; PR #780 merged 2025-11-18)** — problem: the state-key decoder identified "service-info" keys purely by the `0xff` byte at position 0 of the 31-byte state key, but other service-related keys (storage/preimage/lookup keys, which encode the service id bytes interleaved) can also have `0xff` there, e.g. when a service id byte is 0xff. Resolution: "refactor service info key detection logic … aligned with specification section D.1". Quiz angle: *GP App. D.1 state-key construction: C(i) = [i,0,0…], C(i,s) = [i, s0, 0, s1, 0, s2, 0, s3, 0…] (service id bytes interleaved with zeros), C(s,h) = [s0,h0,s1,h1,s2,h2,s3,h3, h4…]; service account info lives under C(255, s); storage under C(s, H(E4(2^32−1) ++ k)) etc. — why byte 0 alone is ambiguous.*

### Service accounts / ch.9

- **#986 Bug: CalcThresholdBalance missing "- a_f" in return value (GP 9.8) (closed, 2026-05-23, YCC3741; PR #987)** — problem: `internal/service_account/service_account.go` returned `storage` instead of `storage - aF` when `storage >= aF`. GP rule quoted (v0.7.2 eq. `eq:deposits`, §9.8): **"a_t = max(0, B_S + B_I·a_i + B_L·a_o − a_f)"** where a_f is the "gratis"/DepositOffset field of the service account (set only by privileged `bless`/registrar paths). Root cause analysis: all 282 jam-conformance traces used DepositOffset = 0, masking the bug. Consequence: threshold balance inflated → host calls `write`, `transfer`, `solicit` could wrongly return FULL. Quiz angle: *state the threshold-balance formula and the meaning of B_S (base deposit, 100), B_I (per-item, 10), B_L (per-byte, 1), a_i (items count), a_o (octets), a_f (gratis storage offset); which host calls check `a_t > a_b` (FULL) and which check balance for transfers (`CASH`).*

- **#882 fix: filter DeferredTransfers for deleted services in tPrime (PR, HanaYukii, merged 2026-01-17)** — "A DeferredTransfer can only be valid if both sender and receiver services exist in dPrime"; "After calculating dPrime = (d ∩ n) ∩ m, filter tPrime to exclude transfers involving deleted services". Quiz angle: *in GP ch.12 the parallelized accumulation output (n = new services, m = removed services, t = deferred transfers) — what happens to a transfer whose destination service was ejected/deleted in the same accumulation round? (Per GP, transfers to non-existent services are dropped: "R(t, d) selects transfers whose destination d exists".)*

### Accumulation / ch.12

- **#880 fix: correct UnmatchedKeyVals merge semantics in parallelized accumulation (PR, HanaYukii, merged 2026-01-14 by TwEricShen)** — problem: in the Go port, parallel per-service accumulation each produce a partial state; the merged "unmatched key-vals" (raw state entries not parsed into typed fields) were unioned/overwritten. Fix: intersection semantics: "only keep keys that exist in ALL service outputs", citing GP §12 formula for removed services **m = ⋂ (K(d) ∩ K((∥s)_e.d))** ... i.e. deletion by any accumulating service must win. Quiz angle: *GP 12.16–12.19 parallel accumulation Δ*: how are the per-service posterior service dictionaries combined — d' = (d ∩ n... ) with n = ⋃ of new/altered accounts and m = the set of removed keys; what conflicts are impossible by construction (a service can only alter itself, create new services, and `eject` others under specific conditions).*

- **#938 Fix: cross-service storage loss in read host call causing state_root mismatch (PR, yu2C, merged 2026-04-24; bug id 1776702160_6218)** — problem: in Ω_R (`read`), when service A reads storage of service B (B not accumulating), A's PVM removed B's entry from its local UnmatchedKeyVals cache as an optimisation; B's updated partial state never reached d' and the intersection merge (#880) then deleted B's storage globally. Fix: cache-and-remove only when `callerServiceID == serviceID`; "cross-service reads truly side-effect-free per Gray Paper requirements". Quiz angle: *`read` host call semantics (GP B.x Ω_R): it takes a service index s (2^64−1 = self / current service), reads the *prior* state δ of other services (read-only) — only the accumulating service's own storage is writable; what value is returned for a missing key (NONE = 2^64−1).*

- **#979 Write host call mutates StorageDict before balance check, causing state mismatch (closed, 2026-05-22, YCC3741, bug; PR #980)** — Ω_W (`write`) in `PVM/host_call_general.go` mutated the storage map before the threshold check; Go map shallow copy shares the underlying map, so on FULL the write persisted. GP quoted: **"When a_minbalance (a_t) > a_balance (a_b), the spec requires s' = s (original, unmodified service account)"** and the return is FULL. Detected by jam-conformance fuzzer seed 3785638964 step 15419. Quiz angle: *`write` returns: previous value length (or NONE if none) on success; FULL if a_t of the *post-write* account exceeds its balance a_b — and in that case no state change; note that `write` with length 0 deletes the key.*

- **#821 bug: accumulation might get assign with zero length (closed, 2025-12-06, TwEricShen)** — fuzzer traces where the accumulation set/ordering was assigned a zero-length slice (edge case of no accumulatable reports / empty ready queue); no text beyond trace ids. Quiz angle: *what is the accumulation process on a block with no newly-available reports — ϑ and ξ still rotate (ready queue shifts by the number of elapsed slots) and W* may be empty.*

- **#667 bug: Fix the parallelized accumulation function (closed, 2025-09; PR #668)** & **#703 fix: Fix formula for LastAccumulationSlot in deferred transfers accumulation** & **#705 Update Accumulation GP v0.7.1 DeltaDoubleDagger by the deferred_transfer major logic change** — v0.7.1 reworked deferred transfers (on-transfer invocation folded into accumulate; `last accumulation slot` a_a updated only for services that were actually accumulated). Quiz angle: *GP 0.7.x removed the separate `on_transfer` entry point (transfers are delivered as inputs to `accumulate`); which services get their a_a (last-accumulation timeslot) updated?*

### PVM / host calls (App. A-B)

- **#997 PVM OOG check off-by-one in SingleStepStateTransition / SingleStepInvokeDecodedBlocks (GP A.6) (closed, 2026-05-28, YCC3741, bug; PR #998)** — the two dispatch loops used `if interp.Gas < 0` allowing one extra instruction at gas = 0 (e.g. a `jump_ind r0` at gas 0 branched into service code, producing spurious hashes/storage writes). GP quoted: **"OOG must trigger when ρ < 1 (i.e. gas insufficient for the next instruction)"** (A.6 single-step: exit ∞ (out-of-gas) if ρ < 1... after deducting the instruction's gas). Fix: `< 1` in both places; legacy `ExecuteInstructions` already correct. Verified: 1179 jam-conformance traces PASS. Quiz angle: *in GP A.6, is the gas check done before or after executing the instruction, and with what comparison? (ρ' = ρ − ε(ι) ... halt with ∞ if ρ' < 0? — the team's reading: check "ρ < 1" before executing, matching the reference PVM). Also: what is the gas cost per basic-block/instruction in 0.7.x (ε = 1 per instruction, until the gas model of 0.8.0/JIP)?*

- **#993 bug: missing OOG check in hostCallException causes state mismatch during fuzzing (closed, 2026-05-25, YCC3741, bug; PR #992 "add OOG check for unknown host calls (GP v0.7.2)")** — `hostCallException` deducted 10 gas for an unknown/invalid host-call index but never checked that gas stayed non-negative; GP v0.7.2 (gavofyork/graypaper#482) "mandates an explicit out-of-gas check for each invocation mutator default case". Reproduced with fuzzer session 8f50823b…, step 175662: service 0x6707fa2e invoked an invalid host function during accumulation; the reference (polkajam-fuzz) halted, ours continued → θ (LastAccOut), β (beefy root) and state root diverged. Quiz angle: *what happens when `ecalli` is invoked with an unknown host-call index h? (GP B: the "default" case charges 10 gas, sets ω_7 = WHAT (2^64−5), and continues — unless that charge exhausts gas, then ∞/out-of-gas.)*

- **#975 PVM logHostCall (host call 100) crashes target due to missing isReadable check (closed, 2026-05-21, YCC3741; PR #976)** — `ecalli 100` (log, JIP-1 non-consensus host call) read memory at (r10,r11)/(r8,r9) without `isReadable`, dereferencing unallocated pages → target process crash ("IO error: early eof (potential target crash)"), fuzz seed 309584898, tiny spec, safrole disabled. Fix: return OOB + continue. Quiz angle: *`log` (index 100) is defined in JIP-1 not the GP; what should a host call do on an inaccessible memory range — panic/PANIC exit vs. OOB return? (GP: a host call whose memory access fails → the machine halts with ☇ (panic); "OOB" (2^64−6... actually OOB is a return code for some calls like `read`/`fetch` when the *destination* range is unreadable: the call panics). Team's fix returns OOB+continue for log.*

- **#866 Fix: 0.7.2 PVM bugs (closed, 2025-12-25, TwEricShen; PR #865 "Fix: deep copy bug")** and **#860 fix: GP 0.7.2 Bugs (closed, 2025-12-25, YCC3741)** — #860 is a triage list of fuzzer traces failing after the 0.7.2 upgrade, grouped: (a) "Should return error": `reports error: not sorted or unique guarantors` (5 traces) and `block header verification failure: InvalidEpochMark` (4 traces); (b) encode/decode: "failed to decode expected service info from state key 0xffff0017…: EOF" (→ #779 0xff key ambiguity); (c) GammaZ (γ_z ring root) mismatches (6 traces); (d) statistics (guarantee counting, 5 traces → PR #869 "fix: guarantee reporters statistics"); (e) PVM (2 traces); (f) header state-root validation (10); (g) nil state root/protocol error (3, ancestry). Quiz angle: *list the guarantee-extrinsic validity rules that produce "not sorted or unique guarantors": credentials sorted by validator index, unique, 2 or 3 signatures, signers must be assigned to the report's core (current or previous rotation) — GP 11.24–11.26.*

### Reporting / guarantees (ch.11)

- **#863 Fix: guarantor sorted and unique bug (closed, 2025-12-25, TwEricShen; PR #864)** — implementation had not enforced that guarantor credentials in each guarantee are sorted ascending by validator index and unique (GP 11.25: "E_G guarantee credentials a ... sorted by validator index; |a| ∈ {2,3}"). Quiz angle: as above.

- **#869 fix: update guarantees counting logic (PR, YuChunTsao + TwEricShen, merged 2025-12-27)** — statistics π: guarantee count per validator counts *reports* the validator signed (each credential in each guarantee), verified with 5 fuzz traces. Quiz angle: *π_g (guarantees) for validator v = number of guarantees in E_G whose credential set contains v (GP 13.5).*

- **#853 feat: using ancestry to validate reports and support fuzz feature (closed, 2025-12-22, yu2C; PR #854 "add ancestry to store and fix guarantee slot validation")** — needed for the fuzzer's `Initialize`(SetState) message which carries an ancestry list; "Append the ancestry when using Initialize; append the ancestry if a block import is successful; update ValidateContext in guarantee". Related **#892 fix: add timeslot validation with ancestry**. Quiz angle: *refinement-context validity (GP 11.31–11.34): the anchor block must be within the recent history β (H = 8 blocks) with matching state root & beefy root; the lookup anchor must be within the last L = 14,400 slots and be an ancestor — checked against ancestry (the fuzzer's Initialize supplies an `ancestry` array of (slot, header hash) for this purpose).*

- **#825 fix: UpdateEtaPrime0 index out of range (closed, 2025-12-06, TwEricShen; PR #831)** — panic `index out of range [65535] with length 6` in `safrole/sealing.go:116` (`UpdateEtaPrime0`): the block author index H_i = 65535 (invalid, > |κ|) was used before validating the header's author index against the validator set (tiny: 6 validators). Quiz angle: *the header's author index H_i must satisfy H_i < V (tiny V = 6, full V = 1023); η_0' = H(η_0 ++ Y(H_v)) uses the VRF output of the author's key κ'[H_i].*

### Version migration: GP v0.8.0 umbrella (#1012) and its 10 phases (all authored by yu2C, 2026-06-23)

- **#1012 Update to v0.8.0 (open, 2026-06-23, yu2C)** — 10 sequential phases, one PR per sub-issue ("Part of #1012"); note: "Core state schema already uses `AvailabilityAssignments` (`rho`) and STF runs assurances before guarantees on `main`." Full conformance deferred until official v0.8.0 test vectors ship. Phases: 1 #1013 Safrole ✅; 2 #1014 header & recent history ✅; 3 #1015 work packages & bundles ✅; 4 #1016 reporting & assurances ✅; 5 #1017 disputes ✅; 6 #1018 auditing & best chain ✅; 7 #1019 accumulation ✅; 8 #1020 authorization ✅; 9 #1021 statistics ✅; 10 #1022 serialization/erasure/VRF/PVM ⏳ (open, assignee TwEricShen). Cross-phase follow-ups: #1037 (variable |κ|), #1044 (deferred conformance).

- **#1013 feat(safrole): align GP v0.8.0 Chapter 6 (closed via PR #1025)** — v0.8.0 renames the seal-key series to the **slot-sealer sequence γ_S**, treats validator keys as **ordered sequences**, and changes ticket rules: `eq:ticket` — entry index e ∈ ℕ (unbounded in state); `eq:ticketsextrinsic` — e ∈ ℕ_n with **n = ⌈2E / |γ'_K|⌉** (E = epoch length, γ'_K = pending validator sequence) — tiny: E=12, V=6 → n=4 (previously fixed N=2 "tickets per validator"); `eq:enforceticketlimit` — **|E_T| ≤ K when m' < Y, else the ticket extrinsic must be empty** (K = max tickets per block = 16, not V); new **`eq:valcount`: validator sequence length ∈ {3c | c ∈ [2, C+1]}** (a multiple of 3 between 6 and 3(C+1)). Code: `VerifyTicketsAttempt` uses n; `VerifyEpochTail` enforces K; `UpdateSlotKeySequence`, `FallbackKeySequence`, `sealing.go`, `markers.go`; equation refs 6.6, 6.13, 6.25–6.31. Quiz angle: *how many ticket attempts may a validator make per epoch in 0.7.x (N = 2) vs 0.8.0 (n = ⌈2E/|γ'_K|⌉ — e.g. tiny gives 4); what bounds |E_T| (K = 16 per block, and tickets only accepted before slot Y = 11 (tiny) / 500 (full) of the epoch).*

- **#1014 feat(header): align GP v0.8.0 header and recent history (closed)** — "v0.8.0 updates header markers (epoch, winning tickets) to align with Safrole slot-sealer terminology, and revises recent history types and commitment rules" (labels eq:recenthistoryspec, eq:recenthistorydef, sec:markers). Implemented by PR #1031 (BlockInfo gains a **timeslot** field; EpochMark validator sequence becomes **length-prefixed**; extrinsic-hash commitment changed to a **preimage-hash** based commitment). Quiz angle: *what is in β (recent history) per block in 0.8.0: header hash, accumulation-result MMR (β_B / "beefy"), state root (filled in by the *next* block), reported work-package hashes → segment roots, plus the new timeslot; and how H_x (extrinsic hash) is computed (hash of the concatenation of per-extrinsic hashes; the guarantee part hashes the encoded reports).*

- **#1015 feat(work-package): align GP v0.8.0 work packages and bundles (closed; PR #1026)** — v0.8.0 introduces explicit **make-bundle / compute-report** semantics (`eq:makebundle`, `eq:computereport`), updates **segment footprint** (`eq:segmentfootprint`: export-count basis) and work-package limits (`eq:wplimits`); PR #1026 adds **`erasure_shards` to WorkPackageSpec** (availability spec now carries the erasure shard count). Quiz angle: *fields of the availability specification S (package hash, bundle length, erasure root, segment root, segment count — and in 0.8.0 the erasure-shard count); size limits W_B (bundle ≤ 13.8 MB in 0.7.x... check current), W_M (max imports/exports 3072), W_T (max items 16).*

- **#1016 feat(reporting): align GP v0.8.0 reporting and assurances (closed; PR #1027)** — v0.8.0 introduces **availability assignments ρ** (guaranteed reports awaiting availability); assurances use the **active validator sequence length |κ| for index bounds and a > 2/3 threshold** (instead of fixed V); work context gains **anchor timeslot (`anchor_slot`) and lookup-anchor posterior state root (`lookup_anchor_state_root`)**; availability spec adds erasure shard count; guarantees: rotation boundaries, inactive-core rejection (`eq:guarantee`, `eq:guaranteesextrinsic`, `eq:guarantorsig`). Quiz angle: *availability threshold: a report becomes available when more than 2/3 of validators (> 2V/3, i.e. ≥ 2⌊V/3⌋+1... precisely "super-majority" ⌊2|κ|/3⌋+1) assure it; assurances must be anchored on the parent hash H_p, signed with the Ed25519 key, bitfield length ⌈C/8⌉, sorted by validator index, and only bits for cores that currently have a pending report may be set.*

- **#1017 feat(disputes): align GP v0.8.0 disputes and judgments (closed; PR #1032)** — v0.8.0 restructures the disputes extrinsic (verdicts + culprits + faults), requires **"exactly 2/3 + 1" validators per verdict** (⌊2|V|/3⌋+1 judgments per verdict), validates signatures from the **active or previous** validator set (κ or λ, chosen by the verdict's epoch index), adds **extrinsic offense limits**; good/bad/wonky set definitions (`eq:goodsetdef`, `eq:badsetdef`, `eq:wonkysetdef`), offender tracking (`eq:offendersdef`, `eq:removenonpositive`). PR #1032: "verdict judgment sequences now length-prefixed; extrinsic caps on verdicts/offenses (16 each); removal of the v0.7.x rule 'bad verdict ⇒ ≥ 2 culprits'". Quiz angle: *verdict outcome classes by positive-judgment count: |V|·2/3+1 → good; 0 → bad; exactly ⌊|V|/3⌋ → wonky; any other count is invalid. Faults must reference a good/bad verdict with the opposite judgment; culprits must be guarantors of a bad report. In 0.7.x a bad verdict needed ≥ 2 culprits — dropped in 0.8.0. Offenders ψ_o are never removed and their keys are zeroed in κ/λ (see #1037).*

- **#1018 feat(auditing): align GP v0.8.0 auditing and best chain (closed)** — v0.8.0 audit selection uses **proportion-based thresholds across the active validator sequence** (|κ|/3-based, not tiny-mode constants), revised judgment rules, and the best-chain rule: **exclude chains with invalid accumulated reports known to ≥ 1/3 of validators** (`eq:auditselection`, `eq:judgments`, `eq:latertranches`, GP ch.17). The best-chain disregard rule itself was deferred to #1044. Quiz angle: *ch.17 auditing: initial tranche selects 10 reports per validator via VRF on η_3'... (tiny differs); later tranches every A = 8 slots; a chain is "disregarded" (not built upon) once ≥ 1/3 of validators judge one of its accumulated reports invalid.*

- **#1019 feat(accumulation): align GP v0.8.0 accumulation (closed via PR #1024/#1033)** — accumulation now consumes reports from the availability-assignment pipeline; revised inputs (`eq:accinput`, `eq:accseq`), partial state, final state integration (`eq:finalstateaccumulation`); service-account and auth-queue outputs feed downstream authorization. PR #1033 "eq:accseq gas budget + processed-transfers output" (see below). Quiz angle: *order of the STF in 0.8.0: disputes → (safrole/tickets) → assurances (produce available reports W) → guarantees → accumulation (with gas limit G_A = per-block accumulation gas; G_T total) → deferred transfers → authorization pool update using φ' from accumulation → statistics.*

- **#1020 feat(authorization): align GP v0.8.0 authorization pool and queue (closed)** — "auth pool updates run after accumulation produces authqueue' (φ')"; when a work-package is guaranteed its authorizer is removed (leftmost match) from the pool; pool additions use **φ'[c][H_t mod Q]** per core (Q = 80 queue length, pool size O = 8). Quiz angle: *α' formula and ordering: it uses the *posterior* queue φ' produced by accumulation in the same block.*

- **#1021 feat(statistics): align GP v0.8.0 validator activity statistics (closed; PR #1034)** — `eq:activityspec`: statistics vectors sized to |κ| and |λ|; accumulation statistics become **service-indexed** (`eq:accumulationstatisticsdef/spec`). PR #1034: "assurances credited **before** epoch rollover", "**3-tuple** accumulation stats", "C(13) prefixes". Quiz angle: *π = (π_V current-epoch validator stats, π_L last-epoch, π_C per-core stats, π_S per-service stats); at an epoch change π_L ← π_V and π_V resets — but the current block's assurances/tickets etc. must be credited to the right epoch (in 0.8.0 assurances are counted before the rollover).*

- **#1022 feat(codec): align GP v0.8.0 serialization, erasure coding, VRF, and PVM (OPEN, assignee TwEricShen)** — cross-cutting phase: codecs for disputes/tickets/Safrole state/availability assignments; **erasure coding: replace fixed 342/1023 with `original_shards(v)` parameterised by validator count v** (code still has `DataShards=342`, `TotalShards=1023` in `internal/types/const.go`); Bandersnatch ring VRF context; PVM: program decode, **skip rules (`eq:skip`)**, instruction tables, **gas model (`eq:gascostforblock`, `eq:fnmemgas`)**, `eq:innerpvm`, `eq:accinvocation`, host calls. Acceptance: erasure encode/recover for tiny v=6 and full v=1023. Quiz angle: *erasure coding parameters: for V=1023, data shards = 342 (= ⌊V/3⌋+1... precisely W_E·… the GP uses 342 original shards, 1023 total, over GF(2^16) Reed–Solomon with 2-byte "points"; tiny V=6 → 2 original shards); a segment (W_G = 4104 bytes) is split into 6-byte pieces… why 342 × 6 = 2052? (each shard of a segment is 12 bytes: 4104/342).*

- **#1037 feat: support variable validator-set size (|κ| ≠ V) (open, 2026-07-05, HanaYukii)** — v0.8.0 reformulates bounds using |κ| rather than the constant V; the codebase treats them as equal because **"offender keys are zeroed in place, never removed"**, so |κ| ≡ |λ| ≡ ValidatorsCount holds. Full support would need chainspec-driven lengths, runtime `ValidatorsSuperMajority` from len(κ), EpochMark / ValidatorsStatistics length validation, core-assignment & rotation maths for non-3C multiples (`eq:valcount`). Blocked on official v0.8.0 vectors. Quiz angle: *what happens to an offender's entry in κ/λ (its keys are replaced by zero bytes; the set size is unchanged) and why guarantor assignment G = P(shuffle(…), …) assumes |κ| is a multiple of 3 (3 guarantors per core: V/C = 3).*

- **#1044 chore(v0.8.0): complete deferred cross-phase conformance follow-ups (open, 2026-07-15, YCC3741)** — three deferred items: (1) reflection codec registries / `internal/input/jam_types` mirror to official v0.8.0 state & extrinsic layouts; (2) **reconcile provisional reports/disputes error ordinals with the official v0.8.0 error enum**, update vendored test vectors, re-enable skipped STF/codec/trace/conformance tests; (3) **auditing best-chain disregard rule** (chains with invalid accumulated reports known to ≥ 1/3 of validators) incl. one-third boundary tests. Quiz angle: *error ordinals are part of the conformance protocol (fuzzer expects a specific error enum per failure class) — not part of consensus, but must match the reference.*

#### v0.8.0 implementing PRs (all by HanaYukii, reviewed by yu2C / YCC3741, merged 2026-07-05..07-15 into the stacked `1012-update-to-v080` branches)

- **#1025 feat(safrole): dynamic ticket cap + per-block K cap (GP v0.8.0) (merged 2026-07-05)** — Before: `attempt < 3 (fixed)`; after: `attempt < n, n = ⌈2E/|γ'_K|⌉` → tiny (E=12, 6 validators) n = 4 (entry-index 3 becomes valid); full (E=600, 1023) n = 2. Rationale: "fewer validators means larger caps, ensuring the lottery pool stays filled." `VerifyEpochTail`: pre-tail block ticket count capped by K (MaxTicketsPerBlock = 16) not V. Empty extrinsic with numV == 0 → nil, not `bad_ticket_attempt`. Legacy v0.7.2 vector `publish-tickets-no-mark-1` skipped via `IsV080IncompatibleVector`. Quiz angle: *the per-validator attempt count n and why it is derived from 2E/|γ'_K| (aim: ~2 tickets per slot of the epoch in expectation); ticket identifier = VRF output y of the Bandersnatch RingVRF over context "jam_ticket_seal" ++ η_2' ++ E1(attempt); tickets sorted by identifier; the block-ticket extrinsic must be sorted & unique and only contain valid ring proofs against the ring root γ_z.*

- **#1027 feat(reporting): add anchor_slot + lookup_anchor_state_root to RefineContext (merged 2026-07-06)** — RefineContext grows from 6 to 8 fields (`eq:workcontext`): **anchor, anchor_slot (u32), state_root, beefy_root, lookup_anchor, lookup_anchor_slot, lookup_anchor_state_root (H), prerequisites**. ρ now stores the **whole guarantee** `(guarantee, timestamp)` per core instead of `(workreport, timestamp)`: wire `report ++ E4(slot) ++ var(credential) ++ E4(timestamp)`. Review (yu2C) forced three spec fixes: assurance validator-index bound by `len(κ)` (`eq:xtassurances`); availability threshold computed as **`3*count > 2*len(κ)`** ("> 2/3 of the active sequence"); **ρ‡ clearing when |κ| ≠ |κ'|** (`eq:availassignmentspostassurancesdef`) implemented in `FilterAvailableReports`. Quiz angle: *why does 0.8.0 keep the guarantee (credentials) in ρ rather than only the report? (so that culprits/offenders can be identified later from state and so the assurance/audit pipeline knows the guarantors); which state transitions clear ρ entries: disputes (bad/wonky verdicts, ρ†), assurances making a report available or timing it out after U = 5 slots (ρ‡), new guarantees (ρ').*

- **#1031 feat(header): BlockInfo timeslot + epoch-mark length prefix + preimage-hash extrinsic commitment (merged 2026-07-15)** — (1) `BlockInfo` gets a 4-byte `timeslot` between `state_root` and `reported` (`eq:recenthistorydef`, carries H_t); (2) EpochMark validator-key sequence is length-prefixed `var{k}` (decode validates prefix == ValidatorsCount); (3) the extrinsic-hash preimage component becomes **`p = E(var[(E4(s), blake(d))])`** — each preimage blob committed by its Blake2b hash instead of the full encoding; block wire serialization (C.15) unchanged. Quiz angle: *H_x = H(E(E_T? …)) — in 0.8.0 the extrinsic hash is the hash of the encoding of the sequence of per-component hashes/commitments: tickets, preimages (as (service, blake(blob)) pairs), guarantees (with report hashes), assurances, disputes; why hash preimage blobs (large blobs shouldn't need to be re-serialised to check the header).*

- **#1032 feat(disputes): verdict judgment length prefix + extrinsic caps + drop culprits rule (merged 2026-07-15)** — (1) verdict judgment sequences length-prefixed instead of fixed ⌊2V/3⌋+1 entries; decode still validates the length equals `ValidatorsSuperMajority` (**5 tiny, 683 full**); (2) caps `|verdicts| ≤ 16`, `|culprits| ≤ 16`, `|faults| ≤ 16` (provisional errors `too_many_verdicts` / `too_many_offenses`), enforced in `DisputesExtrinsic.Validate()` at decode time; (3) the v0.7.x rule "bad verdict ⇒ ≥ 2 culprits" deleted — only "good verdict ⇒ ≥ 1 fault" remains (`NotEnoughCulprits` ordinal kept for conformance mapping). Verified unchanged: good/bad/wonky set updates, offender tracking, ρ clearing, age selection, judge-index bounds, sort/uniqueness rules. Quiz angle: *the judgment-count invariant per verdict (exactly ⌊2V/3⌋+1 judgments, sorted by validator index, unique); verdict age must be the current or previous epoch (determines κ vs λ for signature checks); signature contexts "jam_valid"/"jam_invalid" for judgments, "jam_guarantee" for culprits, "jam_audit"… for faults; the offender list ψ_o' gains culprit & fault keys.*

- **#1033 fix(accumulation): eq:accseq gas budget + processed-transfers output (merged 2026-07-15)** — consensus-critical: (1) **prefix selection budget**: from `Σ digest gas ≤ g` to **`Σ digest gas + Σ incoming transfer gas + Σ free-accumulation allowances ≤ g`**; (2) the transfer-gas term **g\*** now sums transfers *produced* by the current round (t*) rather than incoming; (3) fifth output: processed transfers `t ⌢ t†` (feeds statistics T(s)). Test `TestOuterAccumulation_V080RecursionBudgetAndProcessedTransfers` runs two recursion rounds. Quiz angle: *the outer accumulation Δ+ (eq:accseq): given gas limit g and the report sequence w, pick the longest prefix i such that the total gas (digest gas + transfer gas + free gas for privileged always-accumulate services) fits; recurse with remaining gas g − used; what is G_A (accumulation gas per block: 3.5 billion... check the constants: G_A = 10,000,000 per work-report accumulation? and G_T = 3,500,000,000 total per block) and how do deferred transfers consume gas (each transfer carries its own gas allowance g).*

- **#1034 feat(statistics): assurances before rollover + 3-tuple accumulation stats + C(13) prefixes (merged 2026-07-15)** — (1) **assurances credited to π_V† before the epoch rollover**, so on an epoch-boundary block they roll into π_L' rather than the fresh accumulator; the other five counters (blocks, tickets, preimages, preimage bytes, guarantees) remain post-rollover; (2) accumulation statistics per service become **3-tuples (N(s), T(s), G(s))**: number of accumulated reports/items, number of processed transfers to that service, gas used; transfer-only services now appear; zero tuples dropped; wire `ServiceActivityRecord` gains `AccumulateTransfersCount` between count and gas; (3) π_V and π_L encoded with **C(13) variable-length prefixes** (decode validates == ValidatorsCount). Quiz angle: *why are assurances treated differently at epoch boundaries? (assurances in block B refer to work from the previous slot(s) — they are attributed to the validator set that produced them in the ending epoch); the exact per-service statistics tuple.*

- **#1026 feat(work-package): add erasure_shards to WorkPackageSpec (merged 2026-07-06)** — `WorkPackageSpec` (availability spec) gains a u16 `erasure_shards` between `erasure_root` and `exports_root`: **v0.7.x: hash, length, erasure_root, exports_root, exports_count (5) → v0.8.0: hash, length, erasure_root, erasure_shards, exports_root, exports_count (6)** — changes the wire layout of every on-chain WorkReport. Producer sets ErasureShards = TotalShards. Segment-footprint parameter relabelled W_X (was W_M). Limit constants unchanged from v0.7.2 (W_F, W_B, I, T, G_A). Quiz angle: *enumerate the availability-spec fields in order and explain erasure_root (Merkle root over the erasure-coded shards of the bundle + segments) vs exports_root (segment root of exported segments) vs exports_count.*

- **#1035 feat(codec): ticket entry-index encode[1] + validator-set var prefixes + original_shards(v) (merged 2026-07-15)** — (1) **TicketAttempt is a fixed 1 byte (`encode[1]`)** — the earlier compact encoding diverged for values ≥ 128 (reachable in tiny mode where n could be 200); encoding rejects > 255; (2) ValidatorsData sequences (γ_p/pending, ι, κ, λ) get variable-length prefixes (decode validates == ValidatorsCount); (3) **`OriginalShards(v)`** derives DataShards/TotalShards from validator count: full 342:1023 (byte-identical), **tiny becomes 3:6** (was hard-coded 342/1023 even in tiny). Review (YCC3741) caught that erasure parameters went stale after chainspec/custom-mode validator-count changes → `SetErasureParameters(v)` + chainspec W_E/W_P validation. Quiz angle: *original shards = ⌊v/3⌋ + 1?? — for v=1023 → 342, for v=6 → 3: i.e. original_shards(v) = ⌈v/3⌉ (1023/3 = 341 → 342? no: ⌈1023/3⌉ = 341; ⌊1023/3⌋+1 = 342 ✓; ⌊6/3⌋+1 = 3 ✓) — so original_shards(v) = ⌊v/3⌋ + 1, the smallest number of shards that cannot all be withheld by a 1/3 dishonest minority... i.e. any ⌊v/3⌋+1 validators (a full third-plus-one) can reconstruct the data.*

- **#1046 feat: PVM update 0.8.0 (PR by TwEricShen, merged 2026-08-09, reviewed by YCC3741)** — aligns PVM with GP v0.8.0 App. A/B: **Appendix A**: basic-block boundary detection and a `gaschargedflag`; **A.9 ROB (re-order buffer) pipeline gas simulation with formula `max(cycles − 3, 1)`**; A.10 opcode cost tables; branch/jump dual-target validation and `deblob` validation; `unlikely` and trap instruction handling; **final blocks without a terminator are rejected** (v_blob rule). **Appendix B**: **host-call renumbering — `grow_heap` inserted at ID = 1** (shifting the general host calls); per-function linear gas constants (App. H); `invoke` gas refund; `machine` limited to 63 slots; updated `bless`, `designate`, `query` semantics. Shared gas engine (`GasCostForBlock`, `GasCostFromPC`) between interpreter and x86-64 recompiler; new test-vector submodule from koute/new-gas-cost-model (365 JSON vectors). Review fixes: (1) **mid-block resume must charge the full containing block cost L(i) first (GP A.4) — not just the suffix**; (2) **`transfer` host call: charge M_T first (always), then charge l (transfer gas) only on the OK path *before* state mutation** — no partial commits on OOG; also validate destination d ≤ MaxUint32 before lookup (register values > 2^32 aliased service ids); (3) removed the 100,000-step convergence cap of the ROB simulator (silent undercharging of long serial DIV/REM sequences); (4) ROB storage was O(N²) → trimmed; (5) `HeapMaxPages` must reserve the major guard zone; (6) `designate`/`query` machine-capacity check precedence: FULL before HUH. Quiz angle: *0.8.0 gas model: gas is charged per basic block at block entry (sum of per-instruction costs modelled by an out-of-order pipeline with 3-cycle latency baseline), plus per-host-call linear costs; name the new host call id 1 (grow_heap, replacing sbrk semantics), the memory-growth accounting, and why `transfer` charges its gas before mutating state.*

- **#1042 chore(v0.8.0): integrate reporting, header, disputes, and accumulation stack (PR by YCC3741, merged 2026-07-15)** — consolidates #1027/#1031/#1032/#1033 into `1012-update-to-v080`, with five follow-up verification commits: reporting (κ-derived assurance bounds and active-set disjunct), header (ancestry retention, history marker transitions), disputes (**fault equivalence enforcement and genesis-epoch guards**), accumulation (recursion budget semantics, transfer ordering). Deferred: #1037, reflection registries, official error ordinals, full conformance (needs official v0.8.0 vectors). Quiz angle: *"genesis epoch guard" — a verdict's epoch index must be the current or previous epoch, but at epoch 0 there is no previous epoch.*

- **#977 fix: bless-overflow and chi-assign initialization (PR, TwEricShen, merged 2026-05-21)** — overflow check in the `bless` host call (the sum of free-accumulation gas allowances / `z` map) and initialise χ_A (assigners, one per core) to CoresCount length. Quiz angle: *χ = (χ_M manager, χ_A per-core assigners, χ_V delegator/designate, χ_R registrar (0.8.0), χ_Z always-accumulate services with gas); `bless(m, a, v, r, n, o)` semantics and who may call it (0.8.0: only the manager — GP PR #519 closed a self-privilege exploit).*

- **#1024 docs(accumulation): align ϑ/ready-queue comments with GP v0.8.0 (HanaYukii, merged 2026-06-28)** — comment-only; clarifies that `blockchain.Vartheta` is the **per-epoch ready queue ϑ (GP `\ready`)** — "the cross-slot historical record awaiting accumulation", *not* the freshly-available reports from the assurance pipeline; ξ (accumulation history, GP `\accumulated`) is referenced through gas and write-back. Also flags naming drift: "Bless" → manager, "Vartheta" → ready. Quiz angle: *ϑ is a sequence of E (epoch-length) slots each holding (report, dependencies) pairs; ξ is E sets of accumulated work-package hashes; W* = reports whose prerequisites (work-package hashes in ξ) are satisfied are accumulated now; others wait in ϑ[H_t mod E]; a report waiting in ϑ is dropped after E slots.*

### Safrole / header markers (ch.6) — continued

- **#770 fix: InvalidEpochMark & preimage not required (closed, 2025-11-10, YCC3741, bug; PR #778 by weigen393, merged 2025-11-19)** — three fuzzer traces: (1) `InvalidEpochMark` (H_E, GP 6.27) — the epoch mark must be present iff the block is the first of a new epoch (e' > e) and must equal (η_0', η_1', [(bandersnatch, ed25519) of γ_k']) ; (2) "preimage not required" (GP 0.6.4 §12.36 → 0.7.0 §12.40) — a preimage extrinsic for a (hash,len) that was never solicited must be rejected; (3) `InvalidTicketsMark` (GP 6.28) — the winning-tickets mark H_W must be present iff e' = e ∧ m < Y ≤ m' ∧ |γ_a| = E and equal Z(γ_a) (the outside-in reordering of the sorted accumulator). Reviewer yu2C: "also add a verification for keys in Gamma_P? e.g. if the lens is equal to `types.ValidatorCount`". Quiz angle: *state precisely when H_E and H_W must be present/absent and what they contain; Z (outside-in sequencer): Z(s) = [s_0, s_{n-1}, s_1, s_{n-2}, …].*

- **#825 (see above), #791 (posterior κ'/η' for VRF), #284 (6.24 condition).**

### Auditing (ch.17) — outside the exam's core chapters but M1 code exists

- **#940 fix: BuildJudgements signs with public key (closed, 2026-04-26, HanaYukii, bug; PR #939)** — `BuildJudgements()` passed `Kappa[v].Ed25519` (32-byte public key) to `ed25519.Sign()` → panic "bad private key length: 32". GP §17.17 quoted: **j_n = { S_{κ[v]}^e ⟨X_e(w) ⌢ H(w)⟩ | (c, w) ∈ a_n }** — judgments are signed with the validator's Ed25519 *secret* key; X_e(w) is the "jam_valid"/"jam_invalid" context. Quiz angle: *judgment signature payload = context ("jam_valid" or "jam_invalid") ++ H(work report); the same signature format is what appears in the disputes extrinsic verdicts.*

- **#935 fix: ComputeInitialAuditAssignment missing ValidatorID (closed, 2026-04-12, HanaYukii; PR #934)** — audit reports built without ValidatorID (default 0) broke correlation between audit assignment and judging ("Rule 1" matching), leaving only super-majority passage ("Rule 2"). Quiz angle: *when is a report considered audited/finalizable: every assigned auditor has published a positive judgment (rule 1) or a super-majority (⌊2V/3⌋+1) positive judgments exist (rule 2).*

- **#956 test: ComputeAnForValidator stochastic VRF threshold (GP §17.14-17.15) (closed, 2026-04-27, HanaYukii)** — per-tranche stochastic audit assignment: context ⟨X_U ⌢ Y(H_v) ⌢ H(w) ⌢ n⟩, VRF-signed with the validator's Bandersnatch key; output s_n(w); threshold check **"s_n(w)[0] · V / (256 · F) < m_n"** with **F = BiasFactor = 2** (§17.16) so that audits recover cryptoeconomically when validators no-show; expected assigned count ≈ F · m_n. Quiz angle: *initial tranche a_0: each validator audits 10 reports chosen by a VRF-seeded shuffle; later tranches n ≥ 1: probability proportional to the number of no-shows m_n scaled by F=2; A = 8 slots per tranche.*

- **#529 feat: GetJudgement into auditing flow — Ξ(p,c) re-execution & node integration (closed, 2025-05-11 → PR #910)** — `GetJudgement()` was a stub returning true; per GP §17.16–17.17 auditors must fetch the work-package bundle, re-execute Ξ(p, c) (refine for all items → recompute the work report) and compare with the guaranteed report; bundle fetch from guarantors (CE 144/145 — audit announcement/judgment publication; CE 139/140 shard fetch for erasure reconstruction fallback needing ≥ 342 chunks). Quiz angle: *what an auditor compares: the full work-report (incl. results, gas used, output hashes, availability spec) must be byte-identical; any difference → negative judgment.*

- **#955 test: Stage 3 CE144/CE145 codec edge cases (PR, HanaYukii, merged 2026-06-14)** — CE144 (audit announcement: tranche 0 vs tranche>0 evidence, 98-byte minimum msg1, per-report Bandersnatch signatures + no-show lists), CE145 (judgment publication: Validity flag rules, guarantee included only when Validity = 0 / invalid). Quiz angle: JAMNP CE numbering (128 block request, 129 state request, 131/132 safrole ticket distribution, 133 work-package submission, 134 work-package sharing, 135 work-report distribution, 136 work-report request, 137 shard distribution, 138 audit shard request, 139/140 segment shard requests, 141 assurance distribution, 142 preimage announcement, 143 preimage request, 144 audit announcement, 145 judgment publication).

### PVM gas model (0.8.0, open)

- **#847 feat: Gas Model 0.8.0 (open, 2025-12-20, YCC3741; milestone v2.0)** / **#849 gas model STF functions** / **#850 implement gas cost tables and pass test-vectors (open, yu2C; PR #881)** — A.10 gas cost tables (helper functions, per-instruction modification, block-wise cost model), A.9 gas model STF on PR #881 "needs to check the implementation sticks to 0.8.0 GP"; test vectors from w3f/jamtestvectors PR #3 (koute's `new-gas-cost-model`). Later completed by PR #1046. Quiz angle: *0.7.x gas: every instruction costs 1 gas (ε = 1) and host calls have fixed costs (10 + …); 0.8.0: block-based pipelined cost model.*

- **#923 refactor: update TicketAttempt codec methods to use compact encoding (PR, yu2C, merged 2026-03-23)** — moved the ticket `attempt` field to compact (variable-length) encoding with U64 type; review caught silent truncation (256 → 0 when assigned to U8). **Reverted by #1035 in 0.8.0: `attempt` is a fixed single byte `encode[1]`.** Quiz angle: *in the ticket extrinsic E_T each entry is (attempt: 1 byte, proof: 784-byte Bandersnatch ring VRF proof); state tickets (γ_a, γ_s) are (id: 32-byte hash, attempt: 1 byte).*

### Node / fuzz infrastructure notes

- **#783 fix: wrong StateCommit timing (PR, Terryhung, merged 2025-11-19)** — StateCommit happened inside SetState so posterior = prior after commit; state-root comparison must use `GetPriorStates`; the error message had swapped "got/want" for parent state root. Quiz angle: *H_r (header state root) is the root of the *prior* state (the state after the parent block), not the posterior — "the state root of the parent's posterior state".*

- **#829 fix: accumulate nil and {} comparison (PR, yu2C, merged 2025-12-08)** — accumulate test vectors: empty-map vs nil comparison mismatch in Go (JSON `{}` vs absent) when comparing post-states (`make test-jam-test-vectors mode=accumulate size=tiny`). Quiz angle: none (test harness), but reminds that the accumulate STF vectors compare full ϑ/ξ/δ/χ maps.

### Safrole ring verifier / Bandersnatch (ch.6, App. G)

- **#1040 refactor(safrole): ring verifier cache keyed by epoch forces rebuild on every fork-restore (closed, 2026-07-07, YCC3741; PR #1041)** — `GetVerifier` cached the Bandersnatch ring verifier keyed by epoch and `ClearVerifierCache()` ran on every fork restore, forcing an expensive **KZG ring reconstruction** (`vrf.NewVerifier`) — dominating Safrole import time in fork-heavy fuzzing. Root cause: **"the ring commitment is a pure function of the validator Bandersnatch keys, not the epoch number"**. Fix: bounded map keyed by Blake2b(concat of validator Bandersnatch keys). Results: jam-conformance 1179 pass, jam-test-vectors 201 pass; p99 import latency −61…−90%. Quiz angle: *γ_z (the ring root / KZG commitment) is computed from γ_k (the *pending* validator set's Bandersnatch keys, with offenders' keys replaced by the padding point/zero) and only changes at epoch transitions; tickets in epoch e are verified against γ_z built from the *next* epoch's validators.*

### Version migration 0.7.1 (#828) and JIP-5

- **#828 fix: v0.7.1 to release (closed, 2025-12-08, yu2C)** — checklist after main moved to v0.7.1 in #617: pass `jam-test-vectors/stf` (accumulate nil-vs-{} → PR #829), `trace` (state root mismatch in 00000050.bin: expected 0x00…00 → i.e. the vector expects the block to be *rejected* (nil post-state root) but the node produced a state), `fuzzy` (#840), jam-conformance `fuzz/trace` (PR #822 PVM bug fixes; #825 UpdateEtaPrime0; **#836 ancestor feature support for M1**), mini-fuzzer skipped. Quiz angle: *in jam-conformance trace vectors, an all-zero expected post state root means "block import must fail"; the fuzzer protocol (`Initialize` with ancestry, `ImportBlock`, `GetState`) — M1 requires the ancestry feature.*

- **#777 JIP-5: Secret key derivation (closed, 2025-11-14, yu2C; PR #876)** — implement https://github.com/polkadot-fellows/JIPs/blob/main/JIP-5.md: Ed25519 secret = blake2b("jam_val_key_ed25519" ++ seed), Bandersnatch secret seed = blake2b("jam_val_key_bandersnatch" ++ seed); dev validators use trivial_seed(i) = repeat 8× E4(i). Quiz angle: *how dev/test validator keys are derived deterministically (JIP-5), and that BLS keys are not covered.*

- **#906 chore: Rename Variables and Functions to Fit Latest GP Nomenclature (closed, 2026-02-01, YCC3741; PR #909)** — e.g. Bless → manager, Vartheta → ready, seal-key series → slot-sealer sequence; nomenclature drift is tracked separately from behaviour changes.

### Node / networking / telemetry (open work; JAMNP & JIP-3 context)

- **#974 feat(pvm): cost instrumentation for JIP-3 events 47/95/101 (open, 2026-05-17, HanaYukii)** — AccumulateCost (47), IsAuthorizedCost (95), RefineCost (101) currently emitted as zeros; **"Cost data must remain observational only and cannot enter consensus-serialized structures (WorkReport, WorkResult, Guarantee)"** — sidecar structs + a reflect-based CI guard; Cost.Total via elapsed time + gas delta; event 47 sorted with a 500-service cap; 17 host calls mapped to 9 buckets (refine: historical_lookup, machine/expunge, peek/poke/pages, invoke; accumulate: read/write, lookup, query cluster, transfer, info cluster). Quiz angle: *distinguish consensus gas (deterministic, in the work result `gas used`) from telemetry cost (wall-clock, non-consensus).*

- **#968 Phase 6 – role-specific CE / validator duties (open, yu2C, 2026-05-08)** — guarantor chain CE 133 → 134 → 135 (work-package submission → sharing → work-report distribution), CE 146 bundle submission, CE 148 segment request; CE 141 assurance distribution after import; CE 131/132 ticket distribution; CE 139/140 (segment shards, justifications) without mock fallback; CE 144/145 audit publish. Refs JAMNP simple.md.
- **#967 Phase 5 – Topology Manager (open)** — JAMNP distinguishes **transport connectivity** (which QUIC connections must exist across epochs: prior/current/next validator sets) from **grid gossip** (which peers receive UP 0 / preimage streams); Preferred Initiator with 5 s fallback; **epoch transition: defer connectivity changes until the new epoch's first block is finalized and at least max(⌊E/30⌋, 1) slots elapse**; ~20 reserved `/builder` ALPN slots.
- **#966 CE 128 block request client + import hook (open)**; **#965 UP 0 block announcement (open, assignee Terryhung)** — UP 0 is grid-gossiped not flooded; handshake carries finalized block + known leaves; duplicate UP 0 streams → keep greatest stream ID; PRs #973 (wire codec), #1006 (leaf collection/skip helpers), #925 (validator grid infra).
- **#958 JIP-3 domain events umbrella (open, HanaYukii)** — 115 events / 8 domains: status 10–13 (#942), networking 20–28, block authoring/import 40–47, distribution 60–68, safrole+preimage 80–84/190–199 (#949), guaranteeing 90–113 (#950), availability+bundle 120–153 (#951), segment recovery 160–178 (#952). **#953 e2e against JamTART (open)**: docker-compose harness, 5 scenarios incl. 1-hour soak. **#942 status events 10–13 (open)**: event 10 every 2 s (peer counts, guarantees by core, shards, preimages), 11 best block changed, 12 finalized changed, 13 sync status.

### GP 0.7.1 / 0.7.2 migration details gleaned from PRs

- **#623 refactor/test: Update Reporting and Assurance GP v0.7.1 (closed, 2025-07-28, yu2C → weigen393; PR #671)** — body is three GP-diff screenshots captioned: **"ED25519 -> all keys"** (the guarantor/validator key check now covers all key types, i.e. a validator whose keys are in the offender set is identified by any key, not only Ed25519), **"remove duplicate -> not remove duplicate"**, "typo". Quiz angle: *which validator key is used where: Ed25519 for guarantees/assurances/judgments signatures; Bandersnatch for seals/tickets/audit VRFs; BLS reserved for BEEFY; the 336-byte validator key tuple (32 Bandersnatch + 32 Ed25519 + 144 BLS + 128 metadata).*

- **#619 refactor: Update PVM Invocation, Guarantee GP v0.7.1 (closed, 2025-07-28, yu2C → TwEricShen; PRs #719/#721, reverted by #722 then re-landed)** — screenshots: "New constant S", Ψ_R (refine) and guarantee formula changes, Ψ_A with a check function, Ω_Y (yield), Ω_B (bless), Ω_N (new), Ω_A… host-call changes. Quiz angle: *0.7.1 introduced `yield` (Ω_Y) to set the accumulation result hash and the constant S (max service code size / "S = 2^..."?) — check the 0.7.1 changelog; `new` in 0.7.x takes (code hash, code len, min gas g, min memo m, gratis f) and derives the new service index deterministically from the "next free id" state i ... (0.7.1: s = check(i), i' = next).*

- **#705 Update Accumulation GP v0.7.1 DeltaDoubleDagger by the deferred_transfer major logic change (PR, HanaYukii, merged 2025-10-12)** — "deferred_transfer, PVM.OnTransferInvoke no longer required" — in GP 0.7.1 the separate on-transfer PVM invocation (Ψ_T) was removed; deferred transfers are delivered as inputs to the receiver's `accumulate` in the next round; DeferredTransfersStatistics removed; review chased "service 2 issue" (statistics keyed by service must skip zero-activity entries — a service that only received transfers). **#656 fix: remove transfers stats from service record** (0.7.1: `ServiceActivityRecord` loses `OnTransfersCount`/`OnTransfersGasUsed`; 0.8.0 re-adds a transfer count as T(s) — see #1034). **#703 LastAccumulationSlot formula** (a_a of a service updated when it is accumulated, including when accumulated only because of incoming transfers). Quiz angle: *0.7.0 → 0.7.1: on_transfer removed; accumulate receives (timeslot, service id, sequence of operands, sequence of transfers)? — precisely: accumulation input in 0.7.x is a sequence of "operands" (work digests: package hash, exports root, authorizer hash, payload hash, gas, result) plus incoming deferred transfers; π_S counts per service (accumulate count/gas [+ transfers in 0.8.0]).*

- **#822 fix: PVM bugs (PR, TwEricShen, merged 2025-12-14)** — `query` host call now uses lookup items parsed from state; preimage lookup keys matched/deleted inside the PVM tracked via `priorKeyVals`/`postKeyVals`; renamed `operandOrDeferTransfers`; **bless code order correction**; RAM read returns nil when nothing read; **deferred transfers sorted before Ψ_A**; statistics per 0.7.2. Quiz angle: *`query(s, h, z)` returns the status of a preimage lookup (none / requested / available-since / unavailable-since… encoded as ω_7 = 0/1/2/3 plus timeslot values in ω_8); order of the (service-index, then?) sorting of deferred transfers: by sender? — GP: transfers to a service are ordered by sender service index then by order of creation (the "t" sequence is concatenated in order of accumulating services).*

- **#733 refactor: PVM gas charging and log host-call (PR, TwEricShen, merged 2025-10-11)** — added switchable per-instruction vs block-based gas charging (`GasChargingMode = "blockbased"`), and the JIP-1 `log` host call (index 100): "debugging message from the service/authorizer to the hosting environment for logging to the node operator" — shown only in debug mode. Quiz angle: *`log` takes (level, target ptr/len, message ptr/len) and has no consensus effect; per GP 0.7.x the gas charged for each instruction is 1 (ε), so per-instruction and per-block charging agree except for where OOG is detected.*

- **#992 fix: add OOG check for unknown host calls (GP v0.7.2) (PR, YCC3741, merged 2026-05-25)** — hostCallException: after deducting 10 gas, `gas < 0` → ExitOOG using `chargeGasAndCheck`, matching all other host calls; verification: minifuzz 4/4, picofuzz 4/4, jam-conformance 282/282. (See #993.)

- **#854 feat: add ancestry to store and fix guarantee slot validation (PR, yu2C, merged 2025-12-24)** — the fuzzer's `Initialize` supplies state + ancestry; "last two directory levels excluded from validation per GP 11.35"; reviewer maths for the lookup-anchor bound: **x_t ≥ H_T − L (GP 11.34)** negated as `L + x_t < H_T` → reject. Quiz angle: *lookup anchor must be no older than L = 14,400 timeslots (= 24 h × 3600 / 6 s) relative to H_T, and must be an ancestor (checked against the ancestry set A); anchor must be in β (last H = 8 blocks).*

- **#892 fix: add timeslot validation with ancestry (PR, TwEricShen, merged 2026-01-29)** — reject a block whose parent is not the current head/ancestry; proposed rejecting blocks with duplicate slots unless finalized; returns "block is already finalized" when the parent matches a finalized block. Related to fuzzer fork handling. Quiz angle: *H_T must be strictly greater than the parent's timeslot and not in the future (H_T ≤ current time T); the parent must be known.*

- **#797 Refactor/fuzz mismatch report (PR, yu2C, merged 2025-12-01)** — better state-diff diagnostics (decoded state keys), `-fuzzy` flag for jam-test-vectors, recent_history fix; two traces unresolved at the time (`1757423433/00000024.json` = InvalidTicketsMark, `1757062927/00000091.json`).

- **#883 fix: sign-extend-bug (PR, TwEricShen, 2026-01-15)** — "fix bug conformance/new-year-batch all passed!" — PVM sign-extension bug in a 32-bit arithmetic/load instruction (details not in PR). Quiz angle: *PVM 64-bit register semantics: 32-bit ops (add_32, sub_32, mul_32, shlo_l_32, …, load_i32) sign-extend their 32-bit result to 64 bits; load_u32 zero-extends; immediates are sign-extended from their encoded length (App. A "X" / Z functions).*

### Notation / codec / fuzz-harness lessons

- **#698 Review: Check ⟼ operator (sequence subtraction) usage GP 0.7.0 (closed, 2025-09-08, HanaYukii)** — GP defines the sequence-subtraction operator as removing **"only the left-most matching element in a sequence"**; code (see #692 auth pool) removed *all* matching instances. Issue asks for an audit of every use and tests with duplicate values. Quiz angle: *where does the GP use sequence subtraction (auth pool α' removes one instance of the used authorizer; the ready queue / accumulation edits …), and why the left-most-only semantics matters (an authorizer may be queued multiple times in the pool).*

- **#991 Fuzz target crashes with disk exhaustion after 361K steps (closed, 2026-05-25, YCC3741; PR #990)** — target new-jamneration v0.3.1 / GP v0.7.2, tiny spec; Pebble DB filled by `b:<hash>` blocks, `ht:<hash>` header→timeslot and `sd:<root>` state data never pruned; fix prunes in fuzz mode once ancestry exceeds **MaxLookupAge** (L = 14,400) thresholds. **#983 fuzz target OOM (closed, 2026-05-23; PR #984)** — in-memory repo kept every block's full serialized state (50–200 KB per block) → ring buffer of recent state roots bounded by MaxLookupAge; note "strawberry's conformance node maintains only 2–3 state snapshots". Quiz angle: *what state must a node keep for protocol correctness: the ancestry of header hashes for the last L slots (lookup-anchor checks), β (8 recent blocks), and the current state — plus forks for the fuzzer's fork-restore.*

- **#765 fix: 6.17 Verification & Error Message Return Check (closed wontfix, 2025-11-05; PR #766 refactor: Errorcode … & include header entropy validation)** — GP 6.17 concerns the header entropy VRF (H_v must be a valid Bandersnatch VRF signature by the author over context "jam_entropy" ++ η_3' with an *empty* message); PR #766 added header entropy validation and changed error codes to strings; "Implement-related Error Close Conn" = fuzzer protocol errors close the connection. Quiz angle: *distinguish the seal H_s (signs the unsigned header, context "jam_ticket_seal"/"jam_fallback_seal" with η_3' [and the ticket id/attempt]) from the entropy-VRF H_v (context "jam_entropy" ++ Y(H_s), empty message) — both by the author's Bandersnatch key.*

- **#753 fix: Designated Error (closed, 2025-10-26; PR #755)**, **#785 fix: Fuzz error message response pre state root (closed, 2025-11-18; PR #782)** — fuzz-protocol error response semantics: on a rejected block the target must respond with an error and the *pre*-state root (state unchanged). Quiz angle: *"nil/zero post-state root in traces means the block must be rejected" (cf. #828).*

- **#1035/#923 (ticket attempt byte), #779/#780 (state key layout D.1), #829 (nil vs {}), #1031 (extrinsic hash preimage commitment)** — codec facts summarised in section 3.

---

## 3. 30 most quiz-worthy facts / gotchas learned from this repo's history

1. **Sealing-key regime condition (GP 6.24/6.27):** tickets γ_a become γ_s' only when e' = e+1 ∧ m ≥ Y ∧ |γ_a| = E; otherwise the fallback sequence F(η_2', κ') is used; the team's first implementation only tested `e' == e+1` (#284).
2. **Header VRF/seal must be verified with the posterior κ' and η'** (after epoch rotation) — verifying with prior state fails on the first block of an epoch when keys rotate (#784/#791).
3. **Author index bound:** H_i must be < |κ| (tiny 6, full 1023); an unchecked index (65535) panics in η_0' update (#825).
4. **Epoch mark H_E present iff new epoch; tickets mark H_W present iff e' = e ∧ m < Y ≤ m' ∧ |γ_a| = E and equals Z(γ_a) (outside-in order)** — otherwise InvalidEpochMark / InvalidTicketsMark (#770, GP 6.27/6.28); the epoch mark's key list must have exactly V entries.
5. **0.8.0 ticket rules:** per-validator attempts n = ⌈2E/|γ'_K|⌉ (tiny → 4, full → 2, replacing fixed N); per-block |E_T| ≤ K = 16 (not V); empty extrinsic after slot Y (#1013/#1025). Ticket `attempt` is encoded as a fixed 1 byte (#1035 reverted the compact encoding of #923).
6. **0.8.0 `eq:valcount`:** the validator sequence length must be in {3c | c ∈ [2, C+1]}; offenders' keys are zeroed in place, never removed, so |κ| ≡ |λ| ≡ V in practice (#1037).
7. **Ring root γ_z depends only on the Bandersnatch keys of the pending set (KZG commitment), not on the epoch** — cache by key-hash (#1040).
8. **Sequence subtraction (⟼) removes only the left-most match** — the auth pool α' drops one instance of the consumed authorizer, matched by the report's core; then appends φ'[c][H_t mod Q] and truncates to O = 8; and in 0.8.0 the pool update runs *after* accumulation using the posterior queue φ' (#692/#694, #698, #1020).
9. **Guarantee credentials must be sorted by validator index and unique, 2–3 signatures**, signers assigned to the core in the current or previous rotation (error "not sorted or unique guarantors", #863/#860).
10. **Refinement context bounds:** anchor within the last H = 8 blocks of β with matching state/beefy roots; lookup anchor slot x_t ≥ H_T − L with L = 14,400 and must be an ancestor (needs an ancestry set — the fuzzer's Initialize supplies it) (#854, GP 11.34/11.35).
11. **0.8.0 RefineContext has 8 fields**: anchor, anchor_slot, state_root, beefy_root, lookup_anchor, lookup_anchor_slot, lookup_anchor_state_root, prerequisites (#1027).
12. **0.8.0 availability spec has 6 fields**: hash, length, erasure_root, erasure_shards (u16), exports_root, exports_count (#1026); ρ stores the whole guarantee (report, slot, credentials) + timestamp.
13. **Availability threshold in 0.8.0 is "> 2/3 of the active sequence" (3·count > 2·|κ|)**, assurance validator index bounded by |κ|; ρ‡ is cleared if |κ| ≠ |κ'| (#1027 review).
14. **Threshold balance a_t = max(0, B_S + B_I·a_i + B_L·a_o − a_f)** (GP 9.8, eq:deposits); the gratis offset a_f was silently untested because all conformance traces used DepositOffset = 0 (#986).
15. **`write` must not mutate storage when the post-write threshold exceeds the balance (returns FULL, s' = s)** — Go map aliasing caused a persisted write (#979).
16. **`read` of another service's storage must be side-effect-free**; cross-service reads must not touch the caller's cached key-vals (#938).
17. **Parallel accumulation merge:** removed keys are the intersection semantics (a deletion by any accumulating service wins; kept keys must exist in all outputs) — GP §12 m = ⋂ … (#880).
18. **Deferred transfers whose sender or receiver no longer exists in d' are dropped** (#882); 0.7.1 removed the separate on_transfer invocation — transfers are inputs to `accumulate`, and the receiver's last-accumulation slot updates (#705/#703).
19. **0.8.0 eq:accseq budget:** prefix selection counts digest gas + incoming transfer gas + free-accumulation allowances ≤ g; g* sums transfers *produced* in the round; a fifth output (processed transfers) feeds per-service statistics T(s) (#1033).
20. **0.8.0 statistics:** π_V/π_L are length-prefixed (C(13)); per-service accumulation stats are 3-tuples (N, T, G) with transfer-only services included; **assurances are credited before the epoch rollover** while the other five validator counters are credited after (#1034). 0.7.0 rule 13.5: count each validator once per report/extrinsic (#710/#711). 0.7.1 removed on-transfer stats from the service record (#656).
21. **Preimage extrinsic validity:** accept only if the (hash, len) is solicited and not yet provided (a_l[(h,l)] = []) — "preimage not required" otherwise (#741/#746, #770); E_P sorted & unique by (service, blob).
22. **State key layout (App. D.1):** service-info key is C(255, s) with the service-id bytes interleaved with zeros; storage/preimage/lookup keys interleave service id and hash bytes — a 0xff first byte does *not* identify a service-info key (#779/#780).
23. **0.8.0 codec changes:** BlockInfo gains a timeslot; EpochMark validator keys and verdict judgments are length-prefixed (decoder still validates 5/683 judgments); extrinsic hash commits preimages as (E4(service), blake2b(blob)) pairs (#1031/#1032).
24. **0.8.0 disputes:** caps of 16 verdicts / 16 culprits / 16 faults; the 0.7.x "bad verdict ⇒ ≥ 2 culprits" rule is gone, "good verdict ⇒ ≥ 1 fault" stays; verdict age must be current or previous epoch (genesis-epoch guard) selecting κ or λ; super-majority = ⌊2V/3⌋+1 = 5 (tiny) / 683 (full) (#1032, #1042).
25. **PVM out-of-gas is "ρ < 1" before executing the next instruction** (GP A.6) — `gas < 0` executes one instruction too many (#997/#998); an unknown host call charges 10 gas and must also check OOG (GP 0.7.2, gavofyork/graypaper#482; #993/#992).
26. **Host calls must bounds-check memory before reading** (`log` host call 100 (JIP-1) crashed the target) (#975/#976).
27. **0.8.0 PVM gas model (App. A.9/A.10):** per-basic-block charging with an out-of-order pipeline (ROB) simulation, cost `max(cycles − 3, 1)`; mid-block resume still charges the whole block (A.4); host-call renumbering inserts `grow_heap` at id 1; `transfer` charges M_T first and the transfer gas only on the OK path before state mutation; `machine` capped at 63 slots; programs whose final block lacks a terminator are invalid (#1046).
28. **Erasure coding is parameterised by validator count: original_shards(v) = ⌊v/3⌋+1 → 342 of 1023 (full), 3 of 6 (tiny)**; stale parameters after a chainspec change silently change erasure roots (#1035/#1022).
29. **Auditing (ch.17) signatures:** judgments j_n = S_{κ[v]}^e⟨X_e(w) ⌢ H(w)⟩ use the Ed25519 *secret* key with contexts jam_valid/jam_invalid; stochastic tranche assignment threshold s_n(w)[0]·V/(256·F) < m_n with bias F = 2 (#940, #956).
30. **Conformance harness semantics:** a zero expected post-state root in a trace means "block must be rejected"; the target must answer with an error + unchanged pre-state root; error ordinals must match the official enum (provisional 0.8.0 ordinals pending, #1044); fuzz-mode nodes must prune state older than MaxLookupAge (#828, #785, #991/#983).

---

## 4. Team members (GitHub handles) seen and apparent areas

- **yu2C** — most prolific issue author; wrote the entire v0.8.0 migration plan (#1012–#1022) and node-phase specs (#962–#968); codec/state-key decoding (#780), safrole sealing bug (#284/#285), preimages (#746), ancestry/fuzz harness (#797, #854), JIP-5 keys (#777), STF task issues (#509–#517). Reviewer on most 0.8.0 PRs (caught |κ| vs V and ρ‡ clearing issues).
- **HanaYukii** — implemented most of GP v0.8.0 (#1025–#1035), accumulation (parallelisation #856/#873, merge semantics #880, deferred transfers #882, 0.7.1 accumulation #703/#705), safrole/VRF (#791 posterior-state verification, #692/#694 auth pool), auditing tests/bugs (#935, #940, #956), disputes 0.8.0, telemetry/JIP-3 umbrella (#958, #974, #942–#953), variable validator-set issue (#1037), ⟼ operator review (#698).
- **YCC3741** — project lead / maintainer & merger; fuzz/conformance triage (#860, #770, #741, #710, #828-era), PVM correctness bugs found by fuzzing (#975, #979, #993, #997, #986, #992), fuzz-target performance and resource fixes (#983/#984, #991/#990, #1001/#1002, #1040/#1041), integration PR #1042, deferred conformance follow-ups (#1044), gas model 0.8.0 (#847), nomenclature (#906); rigorous reviewer of #1046 (gas model), #1035 (erasure params), #1033.
- **TwEricShen** — PVM owner: 0.7.2 PVM refactors/bugs (#715, #822, #857, #885, #866, #883 sign-extend, #733 gas charging + log host call, #907 refine host calls, #992 review), PVM 0.8.0 update (#1046) and x86-64 recompiler (#1036), bless/χ fixes (#977), guarantor uniqueness (#864), timeslot/ancestry validation (#892), UpdateEtaPrime0 (#825), reviews on accumulation PRs; assignee of #1022.
- **YuChunTsao** — statistics (#514/#515, #656 0.7.1 stats, #869 guarantee counting), report error naming (#862), state-key service-info detection commit in #780, reviewer on #854.
- **weigen393** — GP 0.7.2 refactor issues (#709, #712–#716), epoch/tickets-mark & preimage fixes (#778), disputes/assurance tests (#665, #623 assignee), gas model 0.8.0 co-assignee (#847).
- **Terryhung** — early guarantor assignments (#191, GP 11.18–11.22), StateCommit timing (#783), database/Redis backend, UP 0 block announcement (#965 assignee).
- (Occasional) reviewers/mergers otherwise: YCC3741, yu2C, TwEricShen.

