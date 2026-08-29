# New-JAMneration `JAM-Protocol` — Code Map for M1 Quiz Writers

Repository: `/root/work/jam/team-repo` (clone of `New-JAMneration/JAM-Protocol`, Go 1.25, HEAD = `c7fb743 Merge pull request #1036 from New-JAMneration/feat/PVM-recompiler`).
Declared target: `VERSION_GP = 0.7.2`, `VERSION_TARGET = 0.3.1`. The Gray Paper source used for cross-checks in this document is the **0.8.0** LaTeX at `/root/work/jam/gp-src/text/*.tex` (note: 0.8.0 adds `grow_heap`, a block-based gas model, a timeslot in β, and a per-core `assigners` list; the repo's comments/TODOs reference these as "0.8.0 work in progress").

All line numbers below are 1-based and were taken from the checked-out tree; excerpts are verbatim.

---

## 1. Architecture overview

### 1.1 Package layout

| Path | Role |
|---|---|
| `internal/types/` | Every GP type (σ, H, E, W, etc.), constants (`const.go`), the JAM codec (`encode.go` 3.1k lines / `decode.go` 3.5k lines, `encoder.go`, `decoder.go`), JSON loaders for test vectors (`unmarshal_json.go`), error codes per subsystem (`error_codes/{safrole,disputes,reports,assurances,preimages}`), chainspec protocol-parameter application (`protocol_parameters.go`). |
| `internal/stf/` | The state-transition function driver: `sft.go` (`RunSTF`), one `update_*.go` per subsystem, `validate_header.go`, `stf_timing.go`. |
| `internal/blockchain/` | The global `ChainState` singleton: prior/intermediate/posterior state containers, unfinalized blocks, ancestry cache, state-root cache, ring-verifier cache, persistence glue. |
| `internal/safrole/` | Chapter 6: entropy, key rotation, ticket extrinsic, seal/VRF validation, epoch/tickets/offenders markers. |
| `internal/recent_history/` | Chapter 7: β† and β′ (history + accumulation-output MMR / "beefy belt"). |
| `internal/authorization/` | Chapter 8: α′ from φ′ and E_G. |
| `internal/service_account/` | Chapter 9: historical lookup Λ, footprint (a_i, a_o), threshold balance a_t, code fetch. |
| `internal/extrinsic/` | Chapters 10 and 11: disputes (verdict/culprit/fault controllers), assurances, guarantees, guarantor assignment (shuffle + rotation). |
| `internal/accumulation/` | Chapter 12: W!, W_Q, W*, ∆+/∆*/∆1, ξ′/ϑ′ updates, preimage extrinsic integration, `Provide`. |
| `internal/statistics/` | Chapter 13: π_V/π_L/π_C/π_S. |
| `internal/work_package/` | Chapter 14 (guarantor side): Ψ_I + Ψ_R orchestration, work-report construction, erasure/exports roots, paged proofs. |
| `internal/auditing/` | Chapter 17 (partial, node side): tranche selection, judgments. |
| `internal/utilities/` | `hash/` (Blake2b, Keccak), `merkle_tree/` (E.1 binary Merkle: N, M_B, M, T, L_x, J_x), `mmr/` (E.2 MMR append + super-peak), `merklization/` (D.1 state keys, D.2 trie, `StateEncoder`, `StateKeyValsToState`), `shuffle/` (F.1–F.3), `block_serialization.go` (E_T/E_P/E_G/E_A/E_D hashing, H_x, E_U(H)), `serialization.go` (C.5/C.6 helpers). |
| `PVM/` | Appendix A + B: program deblob, opcode table, per-opcode interpreter semantics, standard program initialization (A.36), Ψ_M/Ψ_H/Ψ_I/Ψ_R/Ψ_A, all host calls (`host_call_general.go`, `host_call_refine.go`, `host_call_accumulate.go`). `PVM/interpreter/` = pure-Go backend; `PVM/recompiler/` = x86-64 JIT backend (linux/amd64 + cgo); `PVM/PVMtrace/` = execution trace tooling. |
| `pkg/codecs/scale/` | Legacy reflection-based SCALE-ish codec still used by `internal/input/jam_types` (older type set). The production codec is `internal/types/encode.go`+`decode.go`. |
| `pkg/erasure_coding/` | cgo wrapper around a Rust `reed-solomon-simd` static lib (`reed-solomon-ffi/src/lib.rs`), GF(2^16), 342:1023. |
| `pkg/Rust-VRF/` | git submodule (`New-JAMneration/Rust-VRF`), cgo wrapper `vrf-func-ffi` over ark-vrf: IETF VRF sign/verify/output, ring VRF verifier + batch verify, ring commitment (γ_z), JIP-5 key derivation helper. |
| `internal/networking/` | JAMNP-S: QUIC (`quic-go`), Ed25519 self-signed TLS certs with the `e<base32(pubkey)>` alt-name, grid topology, CE128–CE147 stream handlers. |
| `internal/fuzz/`, `internal/fuzzenv/`, `cmd/fuzz/` | JAM conformance fuzz-protocol target (PeerInfo/SetState/ImportBlock/GetState over a Unix socket) + trace/vector replay client. |
| `internal/chainspec/` | JIP-4 chainspec JSON (genesis header, genesis state key-vals, protocol parameters, bootnodes). |
| `internal/keystore/` | Ed25519/Bandersnatch key pairs, JIP-5 derivation (`jip5_key_derivation.go`), local file keystore. |
| `internal/telemetry/` | JIP-3 telemetry client (TCP, event discriminators, bridges). |
| `internal/store/`, `internal/database/` | Repository over pluggable DB providers (memory / pebble / redis) for blocks, states, segment maps, work-package bundles. |
| `cmd/node/` | Node CLI (`node`, `node test` to run jam-test-vectors/jamtestnet/traces). `cmd/pvmtrace/` = trace diff tool. |

### 1.2 How σ (the state) is represented

`internal/types/state.go:3-22` — one struct, one Greek letter per field, plus the state-key index map:

```go
// (4.4)
type State struct {
	Alpha    AuthPools               `json:"alpha"`
	Varphi   AuthQueues              `json:"varphi"`
	Beta     RecentBlocks            `json:"beta"`
	Gamma    SafroleState            `json:"gamma"`
	Psi      DisputesRecords         `json:"psi"`
	Eta      EntropyBuffer           `json:"eta"`
	Iota     ValidatorsData          `json:"iota"`
	Kappa    ValidatorsData          `json:"kappa"`
	Lambda   ValidatorsData          `json:"lambda"`
	Rho      AvailabilityAssignments `json:"rho"`
	Tau      TimeSlot                `json:"tau"`
	Chi      Privileges              `json:"chi"`
	Pi       Statistics              `json:"pi"`
	Vartheta ReadyQueue              `json:"theta"`
	Theta    LastAccOut
	Xi       AccumulatedQueue    `json:"xi"`
	Delta    ServiceAccountState `json:"accounts"`
}

// (6.3)
type SafroleState struct {
	GammaK ValidatorsData             `json:"gamma_k"`
	GammaZ BandersnatchRingCommitment `json:"gamma_z"`
	GammaS TicketsOrKeys              `json:"gamma_s"`
	GammaA TicketsAccumulator         `json:"gamma_a"`
}
```

Naming gotcha (quiz-worthy): the Go field `Vartheta` is the GP **ready queue ϑ (θ in some versions, JSON tag "theta")** and the Go field `Theta` is the GP **accumulation-output log θ (last acc out, state key 16)**. `internal/types/state.go:90-107` maps state-key index → name (`{14}: "vartheta"`, `{15}: "xi"`, `{16}: "theta"`).

Service accounts (`state.go:64-80`):

```go
// (9.2) delta
type ServiceAccountState map[ServiceID]ServiceAccount

// (9.3)
type ServiceAccount struct {
	ServiceInfo    ServiceInfo
	PreimageLookup PreimagesMapEntry  // a_p
	LookupDict     LookupMetaMapEntry // a_l
	StorageDict    Storage            // a_s
}

type LookupMetaMapkey struct {
	Hash   OpaqueHash
	Length U32
}

type TimeSlotSet []TimeSlot
```

`ServiceInfo` (`types.go:137-149`) carries a_c, a_b, a_g, a_m, a_o, a_f, a_i, a_r, a_a, a_p plus a `Version` byte (GP 0.7.1 service-info version prefix).

**Three copies of state live in `blockchain.ChainState`** (`internal/blockchain/chain_state.go:34-59`): `priorStates` (σ), `intermediateStates` (β†, ρ†, ρ‡, δ†, δ‡, W, W!, W_Q, W*, accumulation statistics), `posteriorStates` (σ′). Every STF step reads from prior/intermediate and writes into posterior via typed getters/setters (`prior_state.go`, `posterior_state.go`, `intermediate_state.go`). After a block is accepted, `StateCommit`/`StateCommitWithPreComputedState` (`chain_state.go:400-506`) copies posterior → prior and resets posterior.

`internal/blockchain/intermediate_state.go:54-73` names the intermediate values exactly as the GP daggers:

```go
type IntermediateState struct {
	BetaHDagger       types.BlocksHistory
	RhoDagger         types.AvailabilityAssignments
	RhoDoubleDagger   types.AvailabilityAssignments
	DeltaDagger       types.ServiceAccountState
	DeltaDoubleDagger types.ServiceAccountState
	// (11.16) \mathbf{W} GP 0.6.4
	AvailableWorkReports []types.WorkReport
	PresentWorkReports   []types.WorkReport
	// (12.4) \mathbf{W}^! GP 0.6.4
	AccumulatedWorkReports []types.WorkReport
	// (12.5) \mathbf{W}^Q GP 0.6.4
	QueuedWorkReports types.ReadyQueueItem
	// (12.11) \mathbf{W}^* GP 0.6.4
	AccumulatableWorkReports []types.WorkReport
	// (12.28) $\mathbf{S}$: accumulation statistics
	AccumulationStatistics types.AccumulationStatistics
	// (7.7) b: MR(β′_B) GP 0.6.7 Only used for test-vector
	MmrCommitment types.OpaqueHash
}
```

**"Unmatched key-vals"** — a key engineering decision. Because storage keys (a_s) and lookup keys (a_l) are hashed into the 31-byte state key (D.1 third form), a state restored from raw key-vals (fuzzer `SetState`) cannot always be rebuilt into `ServiceAccount` maps. `merklization.StateKeyValsToState` (`parse_state_key_vals.go:393-689`) decodes what it can and returns the leftovers; `ChainState` carries them as `preStateUnmatchedKeyVals` / `postStateUnmatchedKeyVals`, they are appended to the serialized state before merklizing (`fuzz/service.go:129-139`), and the accumulate host calls `read`/`write`/`query`/`solicit`/`forget`/`provide` and the preimage-extrinsic validation consult/remove them (`PVM/host_call_general.go:975-1016`, `accumulation/extrinsic_preimage.go:62-104`).

### 1.3 Block import entry points

* **Fuzz target / conformance:** `internal/fuzz/service.go:38-152` `FuzzServiceStub.ImportBlock` — computes the header hash, handles forks by `RestoreBlockAndState(parent)`, calls `cs.AddBlock(block)`, then `stf.RunSTF()` (or `RunSTFWithTiming`), then serializes σ′ (`m.StateEncoder`) + unmatched key-vals, merklizes with the key-level cache, and commits. Protocol errors (`*types.ErrorCode`) are reported to the fuzzer; runtime errors abort.
* **Test-vector runner:** `cmd/node/test.go` → `testdata/{jam_test_vector,jam_testnet,traces}/runner.go` call the individual `stf.Update*` functions (e.g. `UpdateHistory`, `UpdatePreimages` exist only for the per-subsystem STF vectors — see `stf/update_history.go:7-9`).
* **Node:** `cmd/node/main.go` loads chainspec/genesis; `internal/node/sync_manager.go:163-168` `importBlock` is still a `TODO`.

The entry-point `RunSTF` (`internal/stf/sft.go:34-156`) fixes the step order:

```go
// RunSTF executes the State Transition Function
// Returns:
//   - (true, error):  Protocol error - block is invalid but node should continue
//   - (false, error): Runtime error - unexpected bug, node should terminate
//   - (false, nil):   Success - block processed successfully
func RunSTF() (bool, error) {
	var (
		err              error
		cs               = blockchain.GetInstance()
		priorState       = cs.GetPriorStates().GetState()
		header           = cs.GetLatestBlock().Header
		extrinsic        = cs.GetLatestBlock().Extrinsic
		unmatchedKeyVals = cs.GetPriorStateUnmatchedKeyVals()
	)

	// Update timeslot
	cs.GetPosteriorStates().SetTau(header.Slot)

	// Validate Non-VRF Header(H_E, H_W, H_O, H_I)
	// For non-genesis blocks, validate the header
	if header.Parent != (types.HeaderHash{}) {
		err = ValidateNonVRFHeader(header, &priorState, extrinsic)
		if err != nil {
			errorMessage := SafroleErrorCodes.SafroleErrorCodeMessages[*err.(*types.ErrorCode)]
			return IsProtocolError(err), fmt.Errorf("%v", errorMessage)
		}
	}

	// update BetaH, GP 0.6.7 formula 4.6
	recent_history.STFBetaH2BetaHDagger()

	// Update Disputes
	err = UpdateDisputes()
	if err != nil {
		errorMessage := DisputesErrorCodes.DisputesErrorCodeMessages[*err.(*types.ErrorCode)]
		return IsProtocolError(err), fmt.Errorf("%v", errorMessage)
	}

	// Update Safrole
	err = UpdateSafrole()
	if err != nil {
		errorMessage := SafroleErrorCodes.SafroleErrorCodeMessages[*err.(*types.ErrorCode)]
		return IsProtocolError(err), fmt.Errorf("%v", errorMessage)
	}
	postState := cs.GetPosteriorStates().GetState()

	// After keyRotate
	err = ValidateHeaderVrf(header, &priorState, &postState)
	if err != nil {
		errorMessage := SafroleErrorCodes.SafroleErrorCodeMessages[*err.(*types.ErrorCode)]
		return IsProtocolError(err), fmt.Errorf("%v", errorMessage)
	}

	// Validate extrinsic
	err = ValidateExtrinsic(extrinsic, &priorState, unmatchedKeyVals)
	if err != nil {
		...
		return IsProtocolError(err), fmt.Errorf("%v", errorMessage)
	}

	// Update Assurances
	err = UpdateAssurances()
	...
	// Update Reports
	err = UpdateReports()
	...
	// Update Accumlate
	err = UpdateAccumlate()
	...
	// Update History (beta^dagger -> beta^prime)
	err = recent_history.STFBetaHDagger2BetaHPrime()
	...
	// Update Preimages
	err = accumulation.ProcessPreimageExtrinsics()
	...
	// Update Authorization
	err = UpdateAuthorizations()
	...
	// Update Statistics
	err = UpdateStatistics()
	...
	return false, nil
}
```

So the concrete ordering is:

1. τ′ ← H_t (`SetTau`)
2. Non-VRF header checks: H_W tickets mark, H_O offenders mark, H_x extrinsic hash, H_r parent state root (`ValidateNonVRFHeader`, `stf/validate_header.go:15-46`; note the state root is recomputed from the **prior** state + unmatched key-vals with `ComputeStateRootWithCache`), author index < |κ|.
3. β† (`STFBetaH2BetaHDagger`, GP eq. "correctlaststateroot": patch the last β entry's state root with H_r).
4. Disputes ψ′ and ρ† (`extrinsic.Disputes`).
5. Safrole: η′, γ′, κ′, λ′, γ′_s, γ′_a, epoch marker (`safrole.OuterUsedSafrole`).
6. VRF header checks with **posterior** state: H_E epoch mark, H_s seal, H_v entropy source (`ValidateHeaderVrf`).
7. E_P sortedness/need check against prior δ (`ValidateExtrinsic` → `accumulation.ValidatePreimageExtrinsics`).
8. Assurances → ρ‡ and W (`extrinsic.Assurance`).
9. Guarantees → ρ′ (`extrinsic.Guarantee`).
10. Accumulation: W!, W_Q, W*, ∆+, then δ‡, ξ′, ϑ′, θ′, χ′, ι′, φ′ (`UpdateAccumlate` = `ProcessAccumulation` + `DeferredTransfers`).
11. β′ (`STFBetaHDagger2BetaHPrime`, needs θ′ from step 10).
12. E_P integration into δ′ (`ProcessPreimageExtrinsics`).
13. α′ (`authorization.Authorization`, needs φ′ from step 10).
14. π′ (`statistics.UpdateValidatorActivityStatistics`).

This matches the GP dependency graph (`overview.tex:48-65`): β† ≺ (H, β); ψ′ before safrole (γ′ depends on ψ′_o via Φ); ρ† ≺ (E_D, ρ); ρ‡ ≺ (E_A, ρ†); ρ′ ≺ (E_G, ρ‡, κ, τ′); accumulation ≺ W*; β′ ≺ (H, E_G, β†, θ′); δ‡‡ (post-preimage) ≺ (E_P, δ‡, τ′); α′ ≺ (H, E_G, φ′, α); π′ last. The only deliberate reorderings are that seal/VRF validation is deferred until after key rotation (so it can use κ′, η′_3 and γ′_s) and that the preimage extrinsic is *validated* before assurances but *integrated* after accumulation (exactly the "merge and join" the GP describes).

`RunSTFWithTiming` (`stf/stf_timing.go:76-212`) is the same sequence instrumented with per-step durations; `STFTiming` field names (`stf_timing.go:22-37`) are a handy enumeration of the steps.

### 1.4 PVM: interpreter and recompiler

* **Core (`PVM/*.go`)** is backend-agnostic: `DeBlobProgramCode` (A.2: jump table `E(|j|) ++ E_1(z) ++ E(|c|) ++ j ++ c ++ k`), `preDecodeBlocks` (one-pass decode into `InstrMeta`/`BlockMeta`), `SingleInitializer` (A.36 memory layout and register init), opcode table `opcodeInfoTable` (A.5 categories, terminators, load/store), all 231 opcode semantics in `instructions.go` (`execInstructions` table) and their pre-decoded twins in `instructions_instrmeta.go`, `branch`/`djump` (A.17/A.18), `ExitReason` (a `uint64` whose top byte is the reason and low bytes carry the host-call id or the page-fault address), the host-call `Omega` functions and `Psi_M` dispatch.
* **Interpreter backend (`PVM/interpreter/`)** registers `PVM.Psi_M_interpreterHook` in `init()`; `Host.HostCall` (`interpreter/host.go:46-127`) is Ψ_H: run `SingleStepInvokeDecodedBlocks` until a non-CONTINUE exit; on HOST_CALL look up the `Omega` in the invocation's `Omegas` table, call it, and loop (or fall back to `HostCallException`/`HostCallOutOfGas` for unknown ids).
* **Recompiler backend (`PVM/recompiler/`, build tag `linux && amd64 && cgo`)** — PR #1036. `Psi_M_recompiler` (`psi_m_recompiler.go:16-137`) mmaps a 4 GB guest region (+4 KB control region below R15 +guard page), maps the A.36 segments with real `mprotect` permissions (`guest_memory.go:16-58`), deblobs the program (shared, hash-keyed program cache `GetOrDeblobProgram`), acquires a cached `CompiledProgram` keyed by `CodeHash`, and drives `host.HostCall` → `Recompiler.BlockBasedInvoke` (`recompiler.go:50-115`), which lazily compiles one basic block at a time (`Compiler.CompileBasicBlock`, `compiler.go`), writes machine code into dual-mapped `memfd` executable memory, and executes it through an entry trampoline. All 13 PVM registers are statically pinned to x86-64 registers (`register_map.go:17-30`, R15 = guest base, RCX = scratch). Memory faults are caught by a SIGSEGV handler that rewrites RIP/RSP back to Go (`x86signal/`), turning hardware faults into `ExitPageFault`/`ExitPanic`; `djump` is resolved natively via a PC→native dispatch table with Go fallback (`djump_native.go`); `sbrk` and `ecalli` exit to Go. Gas is charged 1 per instruction inline (`gas.go:25-28`), with block-based charging prepared but commented out for GP 0.8.0.
* Backend selection: `PVM.ExecutionBackend` (`argument_invocation.go:9-15`), `cmd/fuzz` `--pvm-backend` flag (`cmd/fuzz/main.go:278`); the interpreter is always linked (`accumulation/pvm_backend.go`), the recompiler only on linux/amd64.
* Inner PVMs for the `invoke` host call always use the plain single-step interpreter (`host_call_refine.go:392-410`), never the JIT.

### 1.5 Codec

Production codec = `internal/types/encoder.go` + `encode.go` + `decoder.go` + `decode.go`: every type implements `Encode(e *Encoder) error` / `Decode(d *Decoder) error`. `Encoder.EncodeUint` (`encoder.go:103-138`) is the C.6 variable-length natural encoding; `EncodeUintWithLength` (`encoder.go:88-100`) is C.5 fixed-length little-endian; `EncodeLength` = compact length prefix; optionals are a 0/1 byte prefix; dictionaries are sorted by key before encoding. A second, older reflection-based SCALE codec lives in `pkg/codecs/scale` (types registered by name, used by `internal/input/jam_types`). `internal/utilities/serialization.go` has a third, wrapper-style serializer (`SerializeU64`, `Discriminator`, `MapWarpper`) used by the MMR and some hashing paths.

### 1.6 Erasure coding

`pkg/erasure_coding/erasure_coding.go` is a cgo shim over `reed-solomon-ffi/src/lib.rs` (Rust crate `reed-solomon-simd` 3.0.1, `ReedSolomonEncoder::new(data_shard, parity_shard, 2)` i.e. 2-byte symbols = GF(2^16)). The Rust side pads data to a multiple of `2*data_shard`, transposes into per-2-byte-column codewords, encodes each column, and flattens shard-major; `EncodeDataShards` slices the flat output into `data+parity` shards. Constants: `types.DataShards = 342`, `types.TotalShards = 1023` (`const.go:187-190`), tiny tests use 2:6. Used by `internal/work_package/work_package.go` (erasure root, H.2 style) and the CE137–CE140 handlers.

### 1.7 Rust VRF FFI

`pkg/Rust-VRF/vrf-func-ffi/src` (submodule, not vendored in this checkout) exposes `NewVerifier(ring, ringSize)` → `GetCommitment()` (γ_z, the ring root O(k)), `RingVerifyBatch` (tickets), `IETFSign`/`IETFVerify`/`VRFIetfOutput` (seal H_s, entropy H_v, Y(·)), `GetPublicKeyFromSecret`, `NewHandler` for ring signing. `internal/blockchain/ring_verifier.go:52-96` caches verifiers keyed by `Blake2b(concat of γ_k bandersnatch keys)` (a pure function of the key set, so forks sharing a validator set hit the cache). See `READMERef/RUST_VRF_FFI_USAGE.md` for the ownership rules (`Free()`, `runtime.KeepAlive`, output capacity).

### 1.8 Networking

`internal/networking/quic` wraps `quic-go` (ALPN `jamnp-s/V/H`, `config.go:16-36`); `cert/generator.go` builds Ed25519 self-signed certs whose SAN is `"e" + base32(pubkey)` (alphabet `abcdefghijklmnopqrstuvwxyz234567`, 52 chars, `generator.go:36-73`); `validator/grid.go` implements the √V grid neighbourhood; `handler/ce/` implements CE128 (block request), CE129 (state request), CE131 (ticket distribution), CE133/134 (work-package submission/share), CE135 (work-report distribution), CE136 (work-report request), CE137/138 (EC/audit shard request), CE139/140 (segment shard request), CE141 (assurance distribution), CE142/143 (preimage announce/request), CE144 (audit announcement), CE145 (judgment publication), CE147 (bundle request). Wire sizes are in `handler/ce/constants.go`.

### 1.9 Fuzz / conformance harness

`internal/fuzz/messages.go:16-25` defines the fuzz protocol message types (PeerInfo=0, SetState=1, StateRoot=2, ImportBlock=3, GetState=4, State=5, Error=255); `server.go` serves them over a Unix socket; `service.go` implements the four operations; `cmd/fuzz/main.go` is both server (`serve`) and replay client (`test_folder`, traces, genesis fixtures); `cmd/fuzz/state_compare.go` diffs key-vals. `internal/fuzzenv` (`JAM_FUZZ` env) switches `ChainState` to an all-in-memory repository and prunes to `FuzzPersistentRetainBlocks = 24` blocks. `config.DefaultConfig().Info` (`config/config.go:101-113`) is the PeerInfo (`FuzzVersion: 1, FuzzFeatures: 2, JamVersion: "0.7.1", AppVersion "0.2.0", Name "new_jamneration"`).

### 1.10 Chainspec, keystore, telemetry

* `internal/chainspec` parses JIP-4 JSON (`id`, `bootnodes` as `<53-char e-name>@<ip>:<port>`, `genesis_header` hex, `genesis_state` map of 31-byte hex keys, `protocol_parameters` hex decoded into `types.ProtocolParameters`); `types.ApplyProtocolParameters` (`protocol_parameters.go:30-146`) asserts the compile-time constants match and overwrites the mode-dependent variables (C, D, E, G_R, G_T, K, L, N, R, V, W_E, W_P, Y).
* `internal/keystore/jip5_key_derivation.go:26-69`: ed25519 seed = Blake2b("jam_val_key_ed25519" ++ seed), bandersnatch seed = Blake2b("jam_val_key_bandersnatch" ++ seed); `TrivialSeed(i)` = 4-byte LE i repeated 8 times (tiny validators 0..5).
* `internal/telemetry`: JIP-3 client (`client.go`, `tcp.go`), event codec, `Bridge` helpers that never block or panic the caller (`bridge.go`), `BridgeContract` registry for nightly contract tests.


---

## 2. Gray Paper chapter → code mapping

| GP chapter / appendix | Go files (functions) |
|---|---|
| **3 Notation** (hash, blake/keccak, sequences, dictionaries) | `internal/utilities/hash/hash.go` (`Blake2bHash`, `Blake2bHashPartial`, `KeccakHash`, `ComputeBlockHeaderHash`); `internal/types/types.go` (`OpaqueHash`, `ByteSequence`, `Bitfield`, `TimeSlotSet`, `MmrPeak` = `*OpaqueHash` for optional). |
| **4 Overview** (σ, STF dependency graph, block/state commit) | `internal/types/state.go` (`State`), `internal/stf/sft.go` (`RunSTF`), `internal/blockchain/{prior_state,intermediate_state,posterior_state,chain_state}.go` (`StateCommit`). |
| **5 Header & block** (H fields, E ordering, H_x, E_U) | `internal/types/types.go:1468-1568` (`Header`, `Extrinsic`, `Block`), `internal/utilities/block_serialization.go` (`CreateExtrinsicHash`, `HeaderUSerialization`, `g`), `internal/stf/validate_header.go` (`ValidateNonVRFHeader`, `validateExtrinsicHash`), `internal/header/header_controller.go` (block-author side). |
| **6 Safrole** | `internal/safrole/safrole.go` (`R`, `KeyRotate`, `ReplaceOffenderKeys`=Φ, `OuterUsedSafrole`), `sealing.go` (`UpdateEtaPrime0`, `UpdateEntropy`, `UpdateSlotKeySequence`, `ValidateHeaderSeal`, `ValidateByTickets`, `ValidateByBandersnatchs`, `ValidateHeaderEntropy`, `SealingHeader`), `slot_key_sequence.go` (`OutsideInSequencer`=Z, `FallbackKeySequence`=F), `extrinsic_tickets.go` (`VerifyEpochTail`, `VerifyTicketsProof`, `VerifyTicketsOrder`, `VerifyTicketsDuplicate`, `VerifyTicketsAttempt`, `CreateNewTicketAccumulator`), `markers.go` (`CreateEpochMarker`, `CreateWinningTickets`, `ValidateHeaderEpochMark`, `ValidateHeaderTicketsMark`, `ValidateHeaderOffenderMarker`); error codes `internal/types/error_codes/safrole`. |
| **7 Recent history** | `internal/recent_history/recent_history_controller.go` (`History2HistoryDagger`, `AppendAndCommitMmr`, `MapWorkReportFromEg`, `AddItem2BetaHPrime`, `STFBetaH2BetaHDagger`, `STFBetaHDagger2BetaHPrime`), `internal/utilities/mmr/mmr.go`, `internal/types/types.go:632-678` (`Mmr`, `BlockInfo`, `RecentBlocks`). |
| **8 Authorization** | `internal/authorization/authorization.go` (`STFAlpha2AlphaPrime`, `updatePoolFromQueue`), `internal/types/types.go:245-316` (`AuthPool.RemoveLeftMostPairedValue`, `AuthQueue.Validate`). |
| **9 Service accounts** | `internal/service_account/service_account.go` (`HistoricalLookup`=Λ, `isValidTime`=I, `CalcKeys`=a_i, `CalcOctets`=a_o, `CalcThresholdBalance`=a_t, `FetchCodeByHash`, `DecodeMetaCode`), `internal/types/types.go:137-149` (`ServiceInfo`), `state.go:64-88` (`ServiceAccount`, `PrivilegedServices`), `types.go:1271-1277` (`Privileges` χ). |
| **10 Disputes** | `internal/extrinsic/dispute.go` (`Disputes` pipeline), `verdict_controller.go` (`VerifySignature`, `CheckSortUnique`, `SetDisjoint`, `GenerateVerdictSumSequence`, `ClearWorkReports`=ρ†), `dispute_controller.go` (`ValidateFaults`, `ValidateCulprits`, `CompareVerdictsWithPsi`, `UpdatePsiG/B/W`, `UpdatePsiO`, `HeaderOffenders`), `culprit_controller.go`, `fault_controller.go`; error codes `error_codes/disputes`. |
| **11 Reporting & assurance** | Assurances: `internal/extrinsic/assurance.go`, `assurance_controller.go` (`ValidateAnchor`, `CheckValidatorIndex`, `SortUnique`, `ValidateSignature`, `ValidateBitField`, `UpdateNewlyAvailableWorkReports`=W, `FilterAvailableReports`=ρ‡). Guarantees: `guarantee.go`, `guarantee_controller.go` (`Validate`, `Sort`, `ValidateSignatures`, `ValidateWorkReports`, `CardinalityCheck`, `ValidateContexts`, `ValidateWorkPackageHashes`, `CheckExtrinsicOrRecentHistory`, `CheckSegmentRootLookup`, `CheckWorkResult`, `TransitionWorkReport`=ρ′), `guarantor_assignments.go` (`permute`=P, `rotateCores`=R, `GFunc`=G, `GStarFunc`=G*). Types: `types.go:170-212` (ρ, `RefineContext`), `types.go:500-620` (`WorkResult`, `WorkPackageSpec`, `WorkReport` + size/dependency limits), `types.go:1007-1218` (assurance/guarantee extrinsics). |
| **12 Accumulation** | `internal/accumulation/accumulation.go` (`GetAccumulatedHashes`=©ξ, `UpdateImmediatelyAccumulateWorkReports`=W!, `UpdateQueuedWorkReports`=W_Q, `GetDependencyFromWorkReport`=D, `QueueEditingFunction`=E, `AccumulationPriorityQueue`=Q, `ExtractWorkReportHashes`=P, `UpdateAccumulatableWorkReports`=W*, `OuterAccumulation`=∆+, `ParallelizedAccumulation`=∆*, `SingleServiceAccumulation`=∆1, `R`), `deferred_transfers.go` (`calculateMaxGasUsed`, `executeOuterAccumulation`, `calculateAccumulationStatistics`, `updateDeltaDoubleDagger`, `updateXi`, `updateVartheta`, `DeferredTransfers`), `extrinsic_preimage.go` (`ShouldIntegratePreimage`, `ValidatePreimageExtrinsics`, `ProcessPreimageExtrinsics`, `Provide`), `types.go` (`ReadyQueue`, `AccumulatedQueue`, `PartialStateSet`, `Operand`, `DeferredTransfer`, `AccumulationStatistics`). PVM side: `PVM/accumulate_invocation.go` (`Psi_A`, `I`, `C`, `G`). |
| **13 Statistics** | `internal/statistics/statistics.go` (`UpdateValidatorActivityStatistics`, `UpdateCurrentStatistics`, `UpdateReportStatistics`, `UpdateCoreActivityStatistics`, `CalculateDALoad`, `CalculatePopularity`, `UpdateServiceActivityStatistics`, `GetAllServices`), `types.go:687-755`. |
| **14 Work packages & reports** | `internal/work_package/work_package.go` (`VerifyAuthorization` 14.9, `WorkReportCompute`=Ξ 14.11, `I`, `C` 14.8, `A` 14.16, `ComputeErasureRoot`, `PagedProofs` 14.10, `PadToMultiple` 14.17, `BuildWorkPackageBundle` 14.15), `work_package_controller.go`; `types.go:332-455` (`WorkItem`, `WorkPackage.Validate` 14.4–14.7). |
| **15/16/17 Guaranteeing, Availability, Auditing** (node side, partial) | `internal/networking/handler/ce/ce13x-14x.go`, `internal/store/work_package_bundle_store.go`, `internal/auditing/auditing.go` (17.x tranche/assignment), `internal/auditing/judgement.go`. |
| **A PVM** | `PVM/program_code.go` (`DeBlobProgramCode` A.2, `MakeBitMasks`, `skip` A.3, `ReadUintVariable`), `block_info.go` (`preDecodeBlocks`, `InstrMeta`, `BlockMeta`), `opcode_info.go` (A.5 table), `decode.go` (A.5.x operand decoders, `storeIntoMemory`/`loadFromMemory` incl. the `< 2^16 ⇒ panic` rule), `signed_unsigned_transitions.go` (A.12–A.16), `branch.go` + `exit_reason.go` (A.17 branch, A.18 djump, A.8/A.9 fault ordering), `instructions.go` (all opcodes), `single_initializer.go` (A.36 Y, `P`, `Z`, `DecodeSerializedValues`), `invocation.go` (A.1/A.6/A.7 single step), `argument_invocation.go` (`Psi_M` A.40, `R` A.41), `memory.go`, `guest_memory.go`, `interpreter/`, `recompiler/`. |
| **B PVM invocations / host calls** | `PVM/host_call_general.go` (`OperationType` numbering, `HostCallFunctions`, `gas`, `fetch` + 16 `fetchHandlers`, `lookup`, `read`, `write`, `info`, `logHostCall`, `check` B.14, `getFetchConstantsData`), `host_call_refine.go` (`historicalLookup`, `export`, `machine`, `peek`, `poke`, `pages`, `invoke`, `expunge`), `host_call_accumulate.go` (`bless`…`provide`), `host_call_invocation.go` (`AccumulateOmegas`/`RefineOmegas`/`IsAuthorizedOmegas` tables), `is_authorized_invocation.go` (`Psi_I`), `refine_invocation.go` (`RefineInvoke`=Ψ_R), `accumulate_invocation.go` (`Psi_A`, `I`, `C`, `G`), `pvm_types.go` (result constants OK/HUH/…/NONE, INNER* codes). |
| **C Serialization codec** | `internal/types/encoder.go` (`EncodeUint` C.6, `EncodeUintWithLength` C.5, `EncodeLength`), `encode.go` (`Header.Encode`, `WorkExecResult.Encode`, `TicketsOrKeys.Encode`, `Mmr.Encode`, `Storage.Encode`, …), `decoder.go`/`decode.go`, `internal/utilities/serialization.go` (`SerializeU64`, `SerializeFixedLength`), `pkg/codecs/scale/types/compact.go` (older compact codec). |
| **D State merklization** | `internal/utilities/merklization/state_key_constructor.go` (`StateWrapper`/`StateServiceWrapper`/`ServiceWrapper` = the three forms of C), `state_serialize.go` (`StateEncoder`=T, `encodeDelta1..4KeyVal`), `merklization.go` (`encodeBranchNode`, `encodeLeafNode`, `merklize`, `MerklizationSerializedState`), `state_deserialize.go`, `parse_state_key_vals.go` (`StateKeyValsToState`), `internal/blockchain/key_level_cache.go`. |
| **E General merklization / MMR** | `internal/utilities/merkle_tree/merkle_tree.go` (`N`, `Mb`=M_B, `M`=constant-depth, `T` trace, `Lx`, `Jx`, `C`, `VerifyMerkleProof`), `internal/utilities/mmr/mmr.go` (`P`=append, `Replace`=R, `SuperPeak`=M_R, `Serialize`). |
| **F Shuffle** | `internal/utilities/shuffle/shuffle.go` (`numericSequenceFromHash`=Q, `FisherYatesShuffle`=F, `Shuffle`). |
| **G Bandersnatch / ring VRF** | `pkg/Rust-VRF` (submodule), `internal/blockchain/ring_verifier.go`, `internal/safrole/safrole.go:67-101` (ring root O), `internal/keystore/bandersnatch.go`, `internal/safrole/sealing.go` (IETF sign/verify). |
| **H Erasure coding** | `pkg/erasure_coding/erasure_coding.go`, `reed-solomon-ffi/src/lib.rs`, `internal/work_package/work_package.go:249-331` (`buildBCloud`, `buildSCloud`, `Transpose`), `internal/types/const.go:185-190`. |
| **JIP-4 chainspec / JIP-5 keys / JIP-3 telemetry / JIP-1 log** | `internal/chainspec/*`, `internal/keystore/jip5_key_derivation.go`, `internal/telemetry/*`, `PVM/host_call_general.go:892-943` (`logHostCall`, id 100). |


---

## 3. Representative code excerpts by area

Each excerpt is verbatim. "Quiz angle" lines suggest the GP rule the code encodes and what a good question could probe.

### 3.1 Block & header (GP §5)

**3.1.1 Header struct — field ↔ GP symbol.** `internal/types/types.go:1466-1479`

```go
// Block header
// GP §5.1
type Header struct {
	Parent          HeaderHash               `json:"parent"`                 // $H_p$: Hash of the parent block header
	ParentStateRoot StateRoot                `json:"parent_state_root"`      // $H_r$: State root associated to the parent block
	ExtrinsicHash   OpaqueHash               `json:"extrinsic_hash"`         // $H_x$: Hash of the extrinsic data
	Slot            TimeSlot                 `json:"slot"`                   // $H_t$: Time slot of this block
	EpochMark       *EpochMark               `json:"epoch_mark,omitempty"`   // $H_e$: Mark for epoch transition
	TicketsMark     *TicketsMark             `json:"tickets_mark,omitempty"` // $H_w$: Mark for tickets
	AuthorIndex     ValidatorIndex           `json:"author_index"`           // $H_i$: Index of the validator who authored this block
	EntropySource   BandersnatchVrfSignature `json:"entropy_source"`         // $H_v$: Source of entropy for this block
	OffendersMark   OffendersMark            `json:"offenders_mark"`         // $H_o$: Mark for offenders
	Seal            BandersnatchVrfSignature `json:"seal"`                   // $H_s$: Seal signature for this block
}
```

Quiz angle: which fields are optional (pointer → 0/1 discriminator byte in `Header.Encode`, `encode.go:341-380`), and why `HeaderUSerialization` (E_U(H), the seal message) can simply drop the last 96 bytes of the full encoding (`block_serialization.go:357-372`: the seal is the last field and is fixed-size).

**3.1.2 Extrinsic hash H_x = H(E(H(E_T), H(E_P), H(E_G), H(E_A), H(E_D))).** `internal/utilities/block_serialization.go:293-340`

```go
func CreateExtrinsicHash(extrinsic types.Extrinsic) (extrinsicHash types.OpaqueHash, err error) {
	// Encode the extrinsic elements
	encodedTicketsExtrinsic, err := EncodeExtrinsicTickets(extrinsic.Tickets)
	...
	encodedDisputesExtrinsic, err := EncodeExtrinsicDisputes(extrinsic.Disputes)
	if err != nil {
		return types.OpaqueHash{}, err
	}

	// Hash encoded elements
	encodedTicketsHash := hash.Blake2bHash(encodedTicketsExtrinsic)
	encodedPreimagesHash := hash.Blake2bHash(encodedPreimagesExtrinsic)
	encodedGuaranteesHash := hash.Blake2bHash(encodedGuaranteesExtrinsic)
	encodedAssurancesHash := hash.Blake2bHash(encodedAssurancesExtrinsic)
	encodedDisputesHash := hash.Blake2bHash(encodedDisputesExtrinsic)

	// Concatenate the encoded elements
	encodedHash := types.ByteSequence{}
	encodedHash = append(encodedHash, types.ByteSequence(encodedTicketsHash[:])...)
	encodedHash = append(encodedHash, types.ByteSequence(encodedPreimagesHash[:])...)
	encodedHash = append(encodedHash, types.ByteSequence(encodedGuaranteesHash[:])...)
	encodedHash = append(encodedHash, types.ByteSequence(encodedAssurancesHash[:])...)
	encodedHash = append(encodedHash, types.ByteSequence(encodedDisputesHash[:])...)

	// Hash the encoded elements
	extrinsicHash = hash.Blake2bHash(encodedHash)

	return extrinsicHash, nil
}
```

And the special guarantee serialization for H_x (GP 5.6: guarantees contribute `H(w)` not `w`), `block_serialization.go:129-185`:

```go
// g (5.6)
// INFO: This is different between Appendix C (C.16) and (5.6).
func g(guaranteesExtrinsic types.GuaranteesExtrinsic) ([]byte, error) {
	encoder := types.GetEncoder()
	defer types.PutEncoder(encoder)

	// Encode the length of the guarantees
	guaranteesLength := uint64(len(guaranteesExtrinsic))
	encodedLength, err := encoder.EncodeUint(guaranteesLength)
	...
	for _, guarantee := range guaranteesExtrinsic {
		// encode the w
		encodedReport, err := encoder.Encode(&guarantee.Report)
		if err != nil {
			return nil, err
		}

		// hash the encoded report
		reportHash := hash.Blake2bHash(types.ByteSequence(encodedReport))
		encoded = append(encoded, reportHash[:]...)

		// encode the t (slot)
		encodedSlot, err := encoder.Encode(&(guarantee.Slot))
		...
		encoded = append(encoded, encodedSlot...)

		// encode the length of the guarantee.a
		signaturesLength := uint64(len(guarantee.Signatures))
		encodedSignaturesLength, err := encoder.EncodeUint(signaturesLength)
		...
		encoded = append(encoded, encodedSignaturesLength...)

		// encode the guarantee.a
		for _, signature := range guarantee.Signatures {
			encodedSignature, err := encoder.Encode(&signature)
			...
			encoded = append(encoded, encodedSignature...)
		}
	}

	return encoded, nil
}
```

Quiz angle: "Which extrinsic is hashed differently for H_x than for the block encoding and why?" (E_G: report hash instead of full report — the full block encoding of guarantees uses C.16).

**3.1.3 Non-VRF header validation and H_r.** `internal/stf/validate_header.go:14-46`

```go
// TODO: Align the official errorCode
func ValidateNonVRFHeader(header types.Header, priorState *types.State, extrinsic types.Extrinsic) error {
	if err := safrole.ValidateHeaderTicketsMark(header, priorState); err != nil {
		return err
	}

	if err := safrole.ValidateHeaderOffenderMarker(header, priorState); err != nil {
		return err
	}

	if err := validateExtrinsicHash(header, extrinsic); err != nil {
		return err
	}

	// H_R
	cs := blockchain.GetInstance()
	unmatchedKeyVals := cs.GetPriorStateUnmatchedKeyVals()
	serializedState, _ := m.StateEncoder(*priorState)
	fullStateKeyVals := append(serializedState, unmatchedKeyVals...)
	priorStateRoot := cs.ComputeStateRootWithCache(fullStateKeyVals)
	if header.ParentStateRoot != priorStateRoot {
		errCode := SafroleErrorCode.InvalidParentStateRoot
		return &errCode
	}

	// Validate author_index out of range.
	// NOTE: There is currently no official error code defined for this case.
	// We may need to update this once the spec updates.
	if header.AuthorIndex >= types.ValidatorIndex(len(priorState.Kappa)) {
		errCode := SafroleErrorCode.AuthorIndexOutOfRange
		return &errCode
	}
	return nil
}
```

Quiz angle: H_r is the **prior** state's root (posterior of the parent), which is why it is checked before any transition and why β† patches the last β entry with H_r (GP 7.5 / "correctlaststateroot"). Also: the ordering — this runs before disputes, and the offenders-mark check compares H_o with the culprit/fault keys of *this block's* E_D (`markers.go:177-220`).

**3.1.4 Block validity outcome classification.** `internal/stf/sft.go:17-32`

```go
// IsProtocolError checks if an error is a protocol-level error (defined ErrorCode)
// Returns:
//   - true:  Protocol error → block is invalid, but node should continue processing other blocks
//   - false: Runtime error → unexpected bug, node should terminate
func IsProtocolError(err error) bool {
	if err == nil {
		return false
	}
	if _, ok := err.(*types.ErrorCode); ok {
		// This is a protocol-level error → block invalid
		return true
	}

	// Runtime error → unexpected bug
	return false
}
```

### 3.2 Safrole (GP §6)

**3.2.1 Epoch/slot index (6.2) and the top-level order of operations.** `internal/safrole/safrole.go:29-35` and `132-244`

```go
// R function return the epoch and slot index
// Equation (6.2)
func R(time types.TimeSlot) (epoch types.TimeSlot, slotIndex types.TimeSlot) {
	epoch = time / types.TimeSlot(types.EpochLength)
	slotIndex = time % types.TimeSlot(types.EpochLength)
	return epoch, slotIndex
}
```

```go
// Outer Safrole function
// I made this function return ErrorCode only
func OuterUsedSafrole() *types.ErrorCode {
	defer timing.Track("safrole.OuterUsedSafrole")()

	// --- STEP 1 Get Epoch and Slot for safrole --- //
	var (
		err            error
		ringVerifier   *vrf.Verifier
		cs             = blockchain.GetInstance()
		tau            = cs.GetPriorStates().GetTau()
		tauPrime       = cs.GetPosteriorStates().GetTau()
		e, m           = R(tau)
		ePrime, mPrime = R(tauPrime)
	)

	// prior time slot must be less than posterior time slot
	if tau >= tauPrime {
		errCode := SafroleErrorCode.BadSlot
		return &errCode
	}

	// --- STEP 2 Update Entropy123 --- //
	// (GP 6.23)
	func() {
		defer timing.Track("safrole.UpdateEntropy")()
		UpdateEntropy(e, ePrime)
	}()

	// --- STEP 3 safrole.go (GP 6.2, 6.13, 6.14) --- //
	// (6.2, 6.13, 6.14)
	// This function will update GammaK, GammaZ, Lambda, Kappa
	func() {
		defer timing.Track("safrole.KeyRotate")()
		err = KeyRotate(e, ePrime)
	}()
	...
	// --- slot_key_sequence.go (GP 6.25, 6.26) --- //
	func() {
		defer timing.Track("safrole.UpdateSlotKeySequence")()
		UpdateSlotKeySequence(e, ePrime, m)
	}()

	// After KeyRotate, gammaK and kappa are updated
	postGammaK := cs.GetPosteriorStates().GetGammaK()

	func() {
		defer timing.Track("safrole.GetVerifier")()
		ringVerifier, err = blockchain.GetVerifier(postGammaK)
	}()
	...
	// Update GammaZ commitment (gammaZ)
	if ePrime > e {
		func() {
			defer timing.Track("safrole.GetCommitment")()
			commitment, err := ringVerifier.GetCommitment()
			if err != nil || len(commitment) == 0 {
				logger.Errorf("Failed to get commitment: %v", err)
			} else {
				cs.GetPosteriorStates().SetGammaZ(types.BandersnatchRingCommitment(commitment))
			}
		}()
	}

	// (GP 6.22)
	func() {
		defer timing.Track("safrole.UpdateEtaPrime0")()
		err = UpdateEtaPrime0()
	}()
	...
	// --- STEP 4 Check TicketExtrinsic --- //
	// --- extrinsic_tickets.go (GP 6.30~6.34) --- //
	var HtErrCode *types.ErrorCode
	func() {
		defer timing.Track("safrole.CreateNewTicketAccumulator")()
		HtErrCode = CreateNewTicketAccumulator(ringVerifier)
	}()
	if HtErrCode != nil {
		return HtErrCode
	}

	// (GP 6.28)
	func() {
		defer timing.Track("safrole.CreateWinningTickets")()
		CreateWinningTickets(e, ePrime, m, mPrime)
	}()
	...
	// (GP 6.27)
	func() {
		defer timing.Track("safrole.CreateEpochMarker")()
		CreateEpochMarker(e, ePrime)
	}()

	return nil
}
```

Quiz angle: the order matters — entropy rotation (η_1..3) first, key rotation, then γ′_s (which needs η′_2 and κ′), then the ring verifier for γ′_k (needed both for γ′_z and for verifying E_T against the *new* ring), then η′_0, then tickets. `BadSlot` (error 0) fires when τ ≥ τ′.

**3.2.2 Key rotation (6.13) and Φ (6.14).** `internal/safrole/safrole.go:43-61` and `103-128`

```go
// ReplaceOffenderKeys replaces the Ed25519 key of the validator with a null key
// Equation (6.14) Phi(k)
func ReplaceOffenderKeys(validators types.ValidatorsData) types.ValidatorsData {
	// Get offendersMark (Psi_O) from posterior state
	posteriorState := blockchain.GetInstance().GetPosteriorStates()
	offendersMark := posteriorState.GetPsiO()

	for i, validator := range validators {
		if ValidatorIsOffender(validator, offendersMark) {
			// Replace the validator's keys with a null key
			validators[i].Bandersnatch = types.BandersnatchPublic{}
			validators[i].Ed25519 = types.Ed25519Public{}
			validators[i].Bls = types.BlsPublic{}
			validators[i].Metadata = types.ValidatorMetadata{}
		}
	}

	return validators
}
```

```go
// KeyRotate rotates the keys
// Update the state with the new Safrole state
// (6.13)
func KeyRotate(e types.TimeSlot, ePrime types.TimeSlot) error {
	cs := blockchain.GetInstance()

	// Get prior state
	priorState := cs.GetPriorStates()
	if ePrime > e {
		// Update state to posterior state
		cs.GetPosteriorStates().SetGammaK(ReplaceOffenderKeys(priorState.GetIota()))
		cs.GetPosteriorStates().SetKappa(priorState.GetGammaK())
		cs.GetPosteriorStates().SetLambda(priorState.GetKappa())
		...
	} else {
		cs.GetPosteriorStates().SetGammaK(priorState.GetGammaK())
		cs.GetPosteriorStates().SetKappa(priorState.GetKappa())
		cs.GetPosteriorStates().SetLambda(priorState.GetLambda())
		cs.GetPosteriorStates().SetGammaZ(priorState.GetGammaZ())
	}
	return nil
}
```

Quiz angle: on e′ > e: γ′_k = Φ(ι), κ′ = γ_k, λ′ = κ; Φ uses ψ′_o (**posterior** offenders — disputes have already run). Note `ReplaceOffenderKeys` mutates the slice it is given (the prior ι slice) — a Go aliasing subtlety.

**3.2.3 Entropy accumulation (6.22–6.23).** `internal/safrole/sealing.go:106-143`

```go
func UpdateEtaPrime0() error {
	// (6.22) η′0 ≡ H(η0 ⌢ Y(Hv))

	cs := blockchain.GetInstance()

	priorState := cs.GetPriorStates()
	header := cs.GetLatestBlock().Header

	entropySource := header.EntropySource
	eta := priorState.GetEta()

	vrfOutput, err := vrf.VRFIetfOutput(entropySource[:])
	if err != nil {
		return fmt.Errorf("VRFIetfOutput: %w", err)
	}
	hashInput := append(eta[0][:], vrfOutput...)
	cs.GetPosteriorStates().SetEta0(types.Entropy(hash.Blake2bHash(hashInput)))
	return nil
}

func UpdateEntropy(e types.TimeSlot, ePrime types.TimeSlot) {
	/*
								(η0, η1, η2) if e′ > e
		(6.23) (η′1, η′2, η′3)
								(η1, η2, η3) otherwise
	*/

	cs := blockchain.GetInstance()
	eta := cs.GetPriorStates().GetEta()
	if ePrime > e {
		for i := 2; i >= 0; i-- {
			eta[i+1] = eta[i]
		}
	}
	// This make sure we won't overwrite eta0
	eta[0] = cs.GetPosteriorStates().GetEta0()
	cs.GetPosteriorStates().SetEta(eta)
}
```

Quiz angle: η′_0 = H(η_0 ⌢ Y(H_v)) uses the **prior** η_0 and the VRF *output* (not the signature) of H_v; η_1..3 shift only on epoch change (and shift the *prior* η_0 into η′_1).

**3.2.4 Slot-sealer sequence γ′_s (6.24), Z and F (6.25/6.26).** `internal/safrole/sealing.go:383-411`, `slot_key_sequence.go:9-53`

```go
// Calculate gamma^prime_s
func UpdateSlotKeySequence(e types.TimeSlot, ePrime types.TimeSlot, slotIndex types.TimeSlot) {
	/*
		Slot Key Sequence Update
						Z(γa) if e′ = e + 1 ∧ m ≥ Y ∧ ∣γa∣ = E
		(6.24) γ′s ≡    γs if e′ = e
						F(η′2, κ′) otherwise
	*/
	cs := blockchain.GetInstance()

	// Get prior state
	priorState := cs.GetPriorStates()
	gammaA := priorState.GetGammaA()

	// Get posterior state
	posteriorState := cs.GetPosteriorStates()
	etaPrime := posteriorState.GetEta()

	var newGammaS types.TicketsOrKeys

	if ePrime == e+1 && len(gammaA) == types.EpochLength && int(slotIndex) >= types.SlotSubmissionEnd { // Z(γa) if e′ = e + 1 ∧ m ≥ Y ∧ ∣γa∣ = E
		newGammaS.Tickets = OutsideInSequencer(&gammaA)
	} else if ePrime == e { // γs if e′ = e
		newGammaS = cs.GetPriorStates().GetGammaS()
	} else { // F(η′2, κ′) otherwise
		newGammaS.Keys = FallbackKeySequence(etaPrime[2], posteriorState.GetKappa())
	}
	posteriorState.SetGammaS(newGammaS)
}
```

```go
// OutsideInSequencer re-order the slice of ticketsBodies as in GP Eq. 6.25
func OutsideInSequencer(t *types.TicketsAccumulator) types.TicketsAccumulator {
	left := 0
	right := types.EpochLength - 1

	out := make(types.TicketsAccumulator, types.EpochLength)

	for i := 0; i < types.EpochLength; i++ {
		if i%2 == 0 {
			out[i] = (*t)[left]
			left++
		} else {
			out[i] = (*t)[right]
			right--
		}
	}

	return out
}

// FallbackKeySequence implements the fallback key sequence in GP Eq. 6.26
func FallbackKeySequence(entropy types.Entropy, validators types.ValidatorsData) []types.BandersnatchPublic {
	keys := make([]types.BandersnatchPublic, types.EpochLength)
	var i types.U32
	var epochLength types.U32 = types.U32(types.EpochLength)

	for i = 0; i < epochLength; i++ {
		// Get E_4(i)
		serial := utils.SerializeFixedLength(i, 4)
		// Concatenate  entropy with E_4(i)
		concatenation := append(entropy[:], serial...)
		// H4 : Keccak256(serializedBytes) -> See section 3.8 , take only the first 4 octets of the hash,
		hash := hash.Blake2bHashPartial(concatenation, 4)
		// E^(-1) deserialization
		validatorIndex, _ := utils.DeserializeFixedLength(types.ByteSequence(hash), types.U32(4))
		// validatorIndex : jamtypes.U64
		validatorIndex %= (types.U32(types.ValidatorsCount))
		// k[]_b : validatorData -> bandersnatch
		keys[i] = validators[validatorIndex].Bandersnatch
	}

	return keys
}
```

Quiz angle: the three cases of 6.24 and the exact conditions (e′ = e+1 **and** m ≥ Y **and** |γ_a| = E — skipping an epoch or an unsaturated accumulator falls back to F). F: k[decode_4(Blake2b(η′_2 ⌢ E_4(i))[..4]) mod V]_b (note the stale "Keccak256" comment; the code uses Blake2b as the GP says).

**3.2.5 Ticket extrinsic checks (6.30–6.34) and accumulator construction.** `internal/safrole/extrinsic_tickets.go:15-42`, `44-88`, `117-128`, `215-297`

```go
// (6.30)
// If the current time slot is in the epoch tail, we should not receive any
// tickets.
// Return error code: UnexpectedTicket
func VerifyEpochTail(tickets types.TicketsExtrinsic) *types.ErrorCode {
	cs := blockchain.GetInstance()

	// Get current time slot index
	tauPrime := cs.GetPosteriorStates().GetTau()

	// m'
	mPrime := GetSlotIndex(tauPrime)

	// m' < Y => |E_T| <= K
	if mPrime < types.TimeSlot(types.SlotSubmissionEnd) {
		if len(tickets) > types.ValidatorsCount {
			err := SafroleErrorCode.UnexpectedTicket
			return &err
		}
	} else {
		if len(tickets) != 0 {
			err := SafroleErrorCode.UnexpectedTicket
			return &err
		}
	}

	return nil
}
```

(Gotcha: the comment says `|E_T| ≤ K` but the code compares against `ValidatorsCount` (V), not `MaxTicketsPerBlock` (K). `TicketsExtrinsic.Validate` in `types.go:816-822` does enforce K at decode time.)

```go
// (6.31)
// VerifyTicketsProof verifies the proof of the tickets
// If the proof is valid, return the ticket bodies
func VerifyTicketsProof(ringVerifier *vrf.Verifier, tickets types.TicketsExtrinsic) (types.TicketsAccumulator, *types.ErrorCode) {
	cs := blockchain.GetInstance()
	posteriorEta := cs.GetPosteriorStates().GetEta()

	// Prepare batch items for verification
	items := make([]vrf.VerifyItem, 0, len(tickets))
	for _, ticket := range tickets {
		context := createSignatureContext(types.JamTicketSeal, posteriorEta[2], ticket.Attempt)
		message := []byte{}
		signature := ticket.Signature[:]

		items = append(items, vrf.VerifyItem{
			Context:   context,
			Message:   message,
			Signature: signature,
		})
	}

	// Perform batch verification
	results, err := ringVerifier.RingVerifyBatch(items)
	if err != nil {
		logger.Errorf("Failed to verify tickets proof: %v", err)
		e := SafroleErrorCode.BadTicketProof
		return nil, &e
	}

	// Collect verified tickets
	newTickets := make(types.TicketsAccumulator, 0, len(tickets))
	for i, result := range results {
		if result.Error != nil {
			e := SafroleErrorCode.BadTicketProof
			return nil, &e
		}

		newTickets = append(newTickets, types.TicketBody{
			ID:      types.TicketID(result.Output),
			Attempt: tickets[i].Attempt,
		})
	}

	return newTickets, nil
}
```

```go
// Tickets Attempt must be less than or equal to TicketsPerValidator
func VerifyTicketsAttempt(tickets types.TicketsExtrinsic) *types.ErrorCode {
	for _, ticket := range tickets {
		// ticket.Attempt is an entry index (0-based)
		if ticket.Attempt >= types.TicketAttempt(types.TicketsPerValidator) {
			err := SafroleErrorCode.BadTicketAttempt
			return &err
		}
	}

	return nil
}
```

```go
// (6.34)
// create gamma_a'(New ticket accumulator)
func CreateNewTicketAccumulator(ringVerifier *vrf.Verifier) *types.ErrorCode {
	...
	// (6.30) Verify the epoch tail
	err := VerifyEpochTail(extrinsicTickets)
	...
	// Verify the attempt of the tickets
	err = VerifyTicketsAttempt(extrinsicTickets)
	...
	// (6.31) Verify the tickets proof
	newTickets, err := VerifyTicketsProof(ringVerifier, extrinsicTickets)
	...
	// (6.32) Verify the new tickets order
	err = VerifyTicketsOrder(newTickets)
	...
	// (6.32) Verify the new tickets duplicate
	err = VerifyTicketsDuplicate(newTickets)
	...
	// (6.34) Get previous ticket accumulator
	previousTicketsAccumulator := GetPreviousTicketsAccumulator()

	// (6.34) Concatenate the new tickets and the previous ticket accumulator
	newTicketsAccumulator := append(newTickets, previousTicketsAccumulator...)

	// (6.34) sort the tickets by ticket id
	// We already verified the duplicate tickets, so the newTicketsAccumulator
	// should not contain any duplicate tickets
	sort.Slice(newTicketsAccumulator, func(i, j int) bool {
		return bytes.Compare(newTicketsAccumulator[i].ID[:], newTicketsAccumulator[j].ID[:]) < 0
	})

	// (6.33) Verify the new tickets accmuulator
	err = VerifyTicketsDuplicate(newTicketsAccumulator)
	if err != nil {
		// Found a ticket duplicate (Someone submitted the same ticket)
		return err
	}

	// (6.34) select E tickets from the sorted tickets for the new ticket accumulator
	maxTicketsAccumulatorSize := types.EpochLength
	if len(newTicketsAccumulator) > maxTicketsAccumulatorSize {
		newTicketsAccumulator = newTicketsAccumulator[:maxTicketsAccumulatorSize]
	}

	// (6.34) set the new ticket accumulator to the posterior state
	cs.GetPosteriorStates().SetGammaA(newTicketsAccumulator)

	return nil
}
```

Quiz angle: the ring-VRF context is `X_T ⌢ η′_2 ++ attempt` (`createSignatureContext`, `extrinsic_tickets.go:131-143`: "jam_ticket_seal" + 32-byte η′_2 + 1-byte attempt) with an empty message; the ticket id is the VRF *output*; ordering must be ascending by id; the accumulator keeps the **lowest E** ids (`[:E]` after ascending sort); `GetPreviousTicketsAccumulator` returns an empty accumulator when e′ > e (`extrinsic_tickets.go:194-213`).

**3.2.6 Seal validation: ticket vs fallback (6.15/6.16) and entropy source (6.17).** `internal/safrole/sealing.go:344-358`, `277-342`, `200-219`

```go
func ValidateHeaderSeal(header types.Header, state *types.State) *types.ErrorCode {
	gammaS := state.Gamma.GammaS
	if err := gammaS.Validate(); err != nil {
		logger.Errorf("ValidateHeaderSeal gammaS Validate: %v", err)
		errCode := SafroleErrorCode.VrfSealInvalid
		return &errCode
	}
	if len(gammaS.Tickets) > 0 {
		// logger.Debugf("Validating by tickets")
		return ValidateByTickets(header, state)
	} else {
		// logger.Debugf("Validating by bandersnatchs")
		return ValidateByBandersnatchs(header, state)
	}
}
```

```go
// Need test vectors to verify correctness
func ValidateByTickets(header types.Header, state *types.State) *types.ErrorCode {
	gammaSTickets := state.Gamma.GammaS.Tickets
	...
	index := uint(header.Slot) % uint(len(gammaSTickets))
	ticket := gammaSTickets[index]

	// i_y == Y(Hs)
	vrfOutput, err := vrf.VRFIetfOutput(header.Seal[:])
	...
	if !bytes.Equal(vrfOutput, ticket.ID[:]) {
		logger.Errorf("i_y != Y(Hs): %v", cmp.Diff(vrfOutput, ticket.ID[:]))
		errCode := SafroleErrorCode.VrfSealInvalid
		return &errCode
	}

	// Backup verification method
	message, err := utilities.HeaderUSerialization(header)
	...
	eta_prime := state.Eta

	// Pre-allocate context: JamTicketSeal (14) + eta_prime[3] (32) + ticket.Attempt (1) = 47 bytes
	context := make(types.ByteSequence, 0, len(types.JamTicketSeal)+32+1)
	context = append(context, types.ByteSequence(types.JamTicketSeal[:])...) // XT
	context = append(context, types.ByteSequence(eta_prime[3][:])...)        // η′3
	context = append(context, byte(ticket.Attempt))                          // ir (uint8)

	signature := header.Seal[:]

	signerKey := state.Kappa[header.AuthorIndex].Bandersnatch[:]
	_, err = vrf.IETFVerify(context, message, signature, signerKey)
	if err != nil {
		...
		errCode := SafroleErrorCode.VrfSealInvalid
		return &errCode
	}

	return nil
}
```

```go
func ValidateHeaderEntropy(header types.Header, priorState *types.State) *types.ErrorCode {
	seal := header.Seal
	var message types.ByteSequence // message: []
	// Pre-allocate context: JamEntropy (13) + VRF output (32) = 45 bytes
	context := make(types.ByteSequence, 0, len(types.JamEntropy)+32)
	context = append(context, types.ByteSequence(types.JamEntropy[:])...) // XE
	vrfOutput, err := vrf.VRFIetfOutput(seal[:])
	if err != nil {
		logger.Errorf("ValidateHeaderEntropy VRFIetfOutput: %v", err)
	}
	context = append(context, types.ByteSequence(vrfOutput)...) // Y(Hs)
	signature := header.EntropySource[:]                        // Hv
	signerKey := priorState.Kappa[header.AuthorIndex].Bandersnatch[:]
	_, err = vrf.IETFVerify(context, message, signature, signerKey)
	if err != nil {
		errCode := SafroleErrorCode.VrfEntropyInvalid
		return &errCode
	}
	return nil
}
```

Quiz angle: the seal is a plain (IETF) Bandersnatch VRF, not a ring VRF; the ticket case additionally requires Y(H_s) == ticket id (so the block author must own the ticket); the fallback case requires γ′_s[H_t mod E] == κ′[H_i]_b (`ValidateByBandersnatchs`, `sealing.go:221-274`, error `UnexpectedAuthor`); H_v is signed over context `X_E ⌢ Y(H_s)` with an **empty** message (so it's unbiasable given the seal). Both use η′_3 in the seal context. Although the parameter is named `priorState` in `ValidateHeaderEntropy`, `stf.ValidateHeaderVrf` passes the **posterior** state (`validate_header.go:49-59`).

**3.2.7 Markers: epoch mark (6.27), winning tickets (6.28), offenders (H_o).** `internal/safrole/markers.go:14-71`, `132-175`

```go
// CreateEpochMarker creates the epoch marker
// (6.27)
func CreateEpochMarker(e types.TimeSlot, ePrime types.TimeSlot) {
	cs := blockchain.GetInstance()

	if ePrime > e {
		// New epoch, create epoch marker
		// Get eta_0, eta_1
		eta := cs.GetPriorStates().GetEta()

		// Get gamma_k from posterior state
		gammaK := cs.GetPosteriorStates().GetGammaK()
		...
		epochMarker := &types.EpochMark{
			Entropy:        eta[0],
			TicketsEntropy: eta[1],
			Validators:     epochMarkValidatorKeys,
		}

		cs.GetProcessingBlockPointer().SetEpochMark(epochMarker)
	} else {
		// The epoch is the same
		var epochMarker *types.EpochMark = nil
		cs.GetProcessingBlockPointer().SetEpochMark(epochMarker)
	}
}

// CreateWinningTickets creates the winning tickets
// (6.28)
func CreateWinningTickets(e types.TimeSlot, ePrime types.TimeSlot, m types.TimeSlot, mPrime types.TimeSlot) {
	cs := blockchain.GetInstance()

	gammaA := cs.GetPriorStates().GetGammaA()

	condition1 := ePrime == e
	condition2 := m < types.TimeSlot(types.SlotSubmissionEnd) && mPrime >= types.TimeSlot(types.SlotSubmissionEnd)
	condition3 := len(gammaA) == types.EpochLength

	if condition1 && condition2 && condition3 {
		// Z(gamma_a)
		ticketsMark := types.TicketsMark(OutsideInSequencer(&gammaA))
		cs.GetProcessingBlockPointer().SetTicketsMark(&ticketsMark)
	} else {
		// The epoch is the same
		var ticketsMark *types.TicketsMark = nil
		cs.GetProcessingBlockPointer().SetTicketsMark(ticketsMark)
	}
}
```

Quiz angle: H_E carries (η_0, η_1 — the **prior** values, i.e. η′_1 and η′_2 after rotation) plus (bandersnatch, ed25519) of γ′_k; H_W appears exactly on the first block whose slot index crosses Y within the same epoch, and only when the accumulator is saturated. `ValidateHeaderEpochMark` (`markers.go:75-130`) enforces presence iff e′ > e and equality with η_0/η_1/γ′_k; `InvalidEpochMark` = code 9, `InvalidTicketsMark` = 10.

**3.2.8 Safrole error codes (fuzz-protocol aligned).** `internal/types/error_codes/safrole/safrole_error_code.go:5-22`

```go
const (
	BadSlot                types.ErrorCode = iota // 0 Timeslot value must be strictly monotonic
	UnexpectedTicket                              // 1 Received a ticket while in epoch's tail
	BadTicketOrder                                // 2 Tickets must be sorted
	BadTicketProof                                // 3 Invalid ticket ring proof
	BadTicketAttempt                              // 4 Invalid ticket attempt value
	Reserved                                      // 5 Reserved
	DuplicateTicket                               // 6 Found a ticket duplicate
	VrfSealInvalid                                // 7 VrfSealInvalid
	VrfEntropyInvalid                             // 8 VrfEntropyInvalid
	InvalidEpochMark                              // 9 InvalidEpochMark
	InvalidTicketsMark                            // 10 InvalidTicketsMark
	InvalidOffenderMarker                         // 11 InvalidOffenderMarker
	UnexpectedAuthor                              // 12 Block author is not the expected one
	AuthorIndexOutOfRange                         // 13 Author index is out of range (temporary, waiting for official code)
	InvalidExtrinsicHash                          // 14 Invalid extrinsic hash
	InvalidParentStateRoot                        // 15 Invalid parent state root
)
```

### 3.3 Recent history (GP §7)

**3.3.1 β† (7.5) and β′ (7.6–7.8).** `internal/recent_history/recent_history_controller.go:29-43`, `146-197`

```go
// Beta_H^dagger (7.5) GP 0.6.7
/*
	β†_H ≡ β_H except β†_H [|β_H| − 1]s = H_r
*/
func History2HistoryDagger(history types.BlocksHistory, parentStateRoot types.StateRoot) types.BlocksHistory {
	// Duplicate beta_H into beta_H^dagger
	historyDagger := history

	if len(history) != 0 {
		// Except for the stateroot need to be updated
		historyDagger[len(history)-1].StateRoot = parentStateRoot
	}

	return historyDagger
}
```

```go
// STF β′_H ≺ (H, EG, β†_H, C) (4.7)
func STFBetaHDagger2BetaHPrime() error {
	var (
		cs            = blockchain.GetInstance()
		historyDagger = cs.GetIntermediateStates().GetBetaHDagger()
		beefyBelt     = cs.GetPriorStates().GetBeta().Mmr
		lastAccOut    = cs.GetPosteriorStates().GetLastAccOut()
		block         = cs.GetLatestBlock()
		encoder       = types.NewEncoder()
	)
	// calculate beefyBeltPrime(β′_B) and commitment(b) from lastAccOut
	serializedLastAccOut, err := serLastAccOut(lastAccOut)
	if err != nil {
		return err
	}
	merkleRoot := lastAccOutRoot(serializedLastAccOut)
	beefyBeltPrime, commitment := AppendAndCommitMmr(beefyBelt, merkleRoot)

	// calculate workReportHash(p) from guarantees
	workReportHash := MapWorkReportFromEg(block.Extrinsic.Guarantees)

	// calculate header hash(h)
	headser, _ := encoder.Encode(&block.Header)
	hashed := hash.Blake2bHash(headser)

	// build item n = (h, b, s, p)
	item := NewItem(types.HeaderHash(hashed), workReportHash, commitment)

	// add item n to beta^prime
	historyPrime := AddItem2BetaHPrime(historyDagger, item)

	// Set beta_B^prime and beta_H^prime to store
	cs.GetPosteriorStates().SetBetaB(beefyBeltPrime)
	cs.GetPosteriorStates().SetBetaH(historyPrime)
	return nil
}
```

```go
// Merkle root from serializedLastAccOut (s) part of (7.7) GP 0.6.7
/*
	MB ( s, HK )
*/
func lastAccOutRoot(serializedLastAccOut []types.ByteSequence) types.OpaqueHash {
	return merkle.Mb(serializedLastAccOut, hash.KeccakHash)
}

// Append lastAccOutRoot to mmr and form commitment (7.7) GP 0.6.7
/*
	β′_B ≡ A( β_B , MB ( s, HK ), HK )

	b: MR(β′_B)
*/
func AppendAndCommitMmr(beefyBelt types.Mmr, merkleRoot types.OpaqueHash) (types.Mmr, types.OpaqueHash) {
	var m *mmr.MMR
	if len(beefyBelt.Peaks) == 0 {
		m = mmr.NewMMR(hash.KeccakHash)
	} else {
		m = mmr.NewMMRFromPeaks(beefyBelt.Peaks, hash.KeccakHash)
	}
	beefybeltPrime := m.AppendOne(types.MmrPeak(&merkleRoot))
	return types.Mmr{Peaks: beefybeltPrime}, m.SuperPeak(beefybeltPrime)
}
```

```go
// Update beta^dagger to beta^prime (7.8) GP 0.6.7
/*
	β′_H ≡ β†_H cat. ( p, h = H(H), b = MR(β′_B ), s = H^0 )
*/
func AddItem2BetaHPrime(historyDagger types.BlocksHistory, item types.BlockInfo) types.BlocksHistory {
	n := len(historyDagger)

	if n < maxBlocksHistory {
		historyPrime := make(types.BlocksHistory, n+1)
		copy(historyPrime, historyDagger)
		historyPrime[n] = item
		return historyPrime
	}

	// Ensure beta^prime's length not exceed maxBlocksHistory
	historyPrime := make(types.BlocksHistory, maxBlocksHistory)
	copy(historyPrime, historyDagger[1:])
	historyPrime[maxBlocksHistory-1] = item
	return historyPrime
}
```

Quiz angle: the accumulation-output belt uses **Keccak** (H_K) for both the M_B leaf root of θ′ and the MMR; the new β entry's state root is the zero hash (filled in by the *next* block's β† step); β keeps at most H=8 entries; `MapWorkReportFromEg` (`recent_history_controller.go:88-107`) builds p as (package hash → exports root) sorted by hash.

**3.3.2 MMR append (E.9) and super-peak M_R (E.10).** `internal/utilities/mmr/mmr.go:80-112`, `143-194`

```go
// P
func (m *MMR) P(peaks []types.MmrPeak, l types.MmrPeak, n int) []types.MmrPeak {
	// if n >= l
	if n >= len(peaks) {
		return append(peaks, l)
	}

	// 2. if peaks[n] is empty
	if peaks[n] == nil {
		return m.Replace(peaks, n, l)
	}

	// 3.
	current := peaks[n]
	// 3.1 clean the position n
	peaks = m.Replace(peaks, n, nil)
	// 3.2 new hash
	newHash := m.concatenateAndHash(current, l)
	// 3.3 next n+1
	return m.P(peaks, newHash, n+1)
}
```

```go
func (m *MMR) SuperPeak(peaks []types.MmrPeak) types.OpaqueHash {
	// Filter out nil and empty peaks to form h = [h | h <- b, h != ∅]
	h := make([]types.MmrPeak, 0, len(peaks))
	for _, peak := range peaks {
		if peak != nil {
			h = append(h, peak)
		}
	}

	switch len(h) {
	case 0:
		// No peaks => return H^0 (zero hash)
		empty := types.OpaqueHash{}
		return empty
	case 1:
		// Single peak => return it directly
		return *h[0]
	default:
		// H_K ( $peak ⌢ M_R( h_[...|h|-1] ) ⌢ h_[|h|-1] ) otherwise
		seq := make(types.ByteSequence, 0, 68)

		// Append the "peak" prefix
		seq = append(seq, []byte("peak")...)

		// "Fold" the first (n-1) peaks by recursively computing SuperPeak,
		// then combine the result with the final peak.
		partial := m.SuperPeak(h[:len(h)-1])
		// Append the partial hash
		seq = append(seq, partial[:]...)

		// Append the final peak
		finalPeak := h[len(h)-1][:]
		seq = append(seq, finalPeak...)

		result := hash.KeccakHash(seq)

		return result
	}
}
```

Quiz angle: peaks are `[]*OpaqueHash` (nil = ∅); append carries like binary addition; the super-peak uses the "peak" prefix and folds **left-to-right, last peak outermost**. Encoding of the MMR in state (`encode.go:1904-1930`) prefixes each peak with a 0/1 option byte.

### 3.4 Authorization (GP §8)

**3.4.1 α′ (8.2–8.3).** `internal/authorization/authorization.go:11-55` and `internal/types/types.go:254-265`

```go
func updatePoolFromQueue(coreIndex types.CoreIndex, eg types.ReportGuarantee, alpha types.AuthPools) (types.AuthPools, error) {
	pool := alpha[coreIndex]
	if pool == nil {
		return nil, fmt.Errorf("alpha[%d] is nil", coreIndex)
	}

	// (8.3)   remove (g_r)a from α[c]（leftmost match）
	authHashToRemoved := eg.Report.AuthorizerHash
	pool.RemoveLeftMostPairedValue(authHashToRemoved)

	alpha[coreIndex] = pool
	return alpha, nil
}

func STFAlpha2AlphaPrime(slot types.TimeSlot, guarantees types.GuaranteesExtrinsic, alpha types.AuthPools, varphi types.AuthQueues) (types.AuthPools, error) {
	// (8.3) Remove used authorizer from E_G
	for _, guarantee := range guarantees {
		updatedAlpha, err := updatePoolFromQueue(guarantee.Report.CoreIndex, guarantee, alpha)
		if err != nil || updatedAlpha == nil {
			return alpha, err
		}
		alpha = updatedAlpha
	}

	// (8.2) Append φ′[c][Ht↺] for each core
	// TODO: full mode we need to loop 341 times for each cores: optimization needed
	for coreIndex := range types.CoresCount {
		queue := varphi[coreIndex]
		if len(queue) == 0 {
			logger.Warnf("varphi[%d] is empty, skipping append", coreIndex)
			continue
		}
		index := int(slot) % len(queue)
		alpha[coreIndex] = append(alpha[coreIndex], queue[index])

		if len(alpha[coreIndex]) > types.AuthPoolMaxSize {
			alpha[coreIndex] = alpha[coreIndex][len(alpha[coreIndex])-types.AuthPoolMaxSize:]
		}
	}
	if err := alpha.Validate(); err != nil {
		return nil, fmt.Errorf("post alpha validation failed: %w", err)
	}

	return alpha, nil
}
```

```go
func (a *AuthPool) RemoveLeftMostPairedValue(h OpaqueHash) {
	result := (*a)[:0]
	removed := false
	for _, v := range *a {
		if removed || !bytes.Equal(v[:], h[:]) {
			result = append(result, v)
		} else {
			removed = true
		}
	}
	*a = result
}
```

Quiz angle: per core — first remove the **leftmost** occurrence of the used authorizer hash (only for cores that had a guarantee), then append φ′[c][H_t mod Q] (Q = 80), then keep the **last** O = 8 entries. The queue used is the **posterior** φ′ (set by accumulation's `assign` host call), so authorization runs after accumulation.

### 3.5 Service accounts (GP §9)

**3.5.1 Historical lookup Λ and the timeslot-set predicate I (9.5–9.7).** `internal/service_account/service_account.go:77-128`

```go
// (9.7) historicalLookup Lambda Λ, which is the exact definition of (9.5)
func HistoricalLookup(account types.ServiceAccount, timestamp types.TimeSlot, hash types.OpaqueHash) (bytes types.ByteSequence) {
	/*
		Λ(a, t, h) ≡
			a_p[h] if h ∈ Key(a_p) ∧ I( a_l[ h, |a_p[h]| ], t )
			∅      otherwise
	*/
	// h, |a_p[h]|
	lookupkey := types.LookupMetaMapkey{
		Hash:   hash,
		Length: types.U32(len(account.PreimageLookup[hash])),
	}

	// a_l[ h, |a_p[h]| ]
	l := account.LookupDict[lookupkey]

	// a_p[h] if h ∈ Key(a_p) ∧ I( a_l[ h, |a_p[h]| ], t )
	if bytes, exists := account.PreimageLookup[hash]; exists && isValidTime(l, timestamp) {
		return bytes
	}

	// ∅      otherwise
	return nil
}

// I
func isValidTime(l types.TimeSlotSet, t types.TimeSlot) bool {
	/*
		I(l, t) =
			false             if [] = l
			x ≤ t             if [x] = l
			x ≤ t < y         if [x, y] = l
			x ≤ t < y ∨ z ≤ t if [x, y, z] = l
	*/
	switch len(l) {
	case 0:
		return false
	case 1:
		return l[0] <= t
	case 2:
		return l[0] <= t && t < l[1]
	case 3:
		return (l[0] <= t && t < l[1]) || l[2] <= t
	default:
		// ⟦N_T⟧_{∶3}
		return false
	}
}
```

Quiz angle: the four status shapes of a_l[(h,l)]: `[]` requested-not-yet-provided, `[x]` available since x, `[x,y]` available x..y then forgotten, `[x,y,z]` re-requested at z. The `query` host call encodes exactly these into ω_7/ω_8 (`host_call_accumulate.go:618-633`).

**3.5.2 Footprint and threshold balance (9.8).** `internal/service_account/service_account.go:156-209`

```go
// a_i: calculate number of items(keys) in storage
func CalcKeys(account types.ServiceAccount) types.U32 {
	/*
		a_i ∈ N_2^32 ≡ 2*|a_l| + |a_s|
	*/
	return types.U32(2*len(account.LookupDict) + len(account.StorageDict))
}

// a_o: calculate total number of octets(datas) used in storage
func CalcOctets(account types.ServiceAccount) types.U64 {
	/*
		a_o ∈ N_2^64 ≡ [ ∑_{(h,z)∈Key(a_l)}  81 + z  ] + [ ∑_{x∈Value(a_s)}	34 + |x| ]
	*/
	// calculate all (81 + preiamge lookup length in keysize)
	keyContribution := 0
	for key := range account.LookupDict {
		keyContribution += 81 + int(key.Length)
	}

	//  calculate all [ 32(size of key) + size of data ]
	stateContribution := 0
	for x, y := range account.StorageDict {
		stateContribution += 34 + len(y) + len(x)
	}

	return types.U64(keyContribution + stateContribution)
}

// a_t: calculate threshold(minimum) balance needed for any account in terms of storage footprint
func CalcThresholdBalance(aI types.U32, aO types.U64, aF types.U64) types.U64 {
	/*
		a_t ∈ N_B ≡ B_S + B_I*a_i + B_L*a_o
	*/
	storage := types.U64(types.BasicMinBalance) + types.U64(types.U32(types.AdditionalMinBalancePerItem)*aI) + types.U64(types.AdditionalMinBalancePerOctet)*aO
	if storage < aF {
		// result < 0
		return 0
	}
	return storage - aF
}

/*
	a_i ∈ N_2^32 ≡ 2*|a_l| + |a_s|
	a_o ∈ N_2^64 ≡ [ ∑_{(h,z)∈Key(a_l)}  81 + z  ] + [ ∑_{x∈Value(a_s)}	34 + |x| ]
*/
// compute how many items a_i(keys) and a_o(ocetes) the lookupItem has
func CalcLookupItemfootprint(lookupItem types.LookupMetaMapkey) (types.U32, types.U64) {
	return 2, 81 + types.U64(lookupItem.Length)
}

// compute how many items a_i(keys) and a_o(ocetes) the storageItem has
func CalcStorageItemfootprint(storageRawKey string, storageData types.ByteSequence) (types.U32, types.U64) {
	return 1, 34 + types.U64(len(storageRawKey)) + types.U64(len(storageData))
}
```

Quiz angle: a lookup entry counts as **2 items and 81+z octets**; a storage entry as **1 item and 34+|k|+|v| octets**; a_t = max(0, B_S + B_I·a_i + B_L·a_o − a_f) with a_f the "deposit offset" (gratis storage). `Items`/`Bytes` are cached in `ServiceInfo` and maintained incrementally by `write`/`solicit`/`forget` rather than recomputed.

**3.5.3 Code/metadata fetch (9.4).** `internal/service_account/service_account.go:12-48` — `FetchCodeByHash` reads a_p[a_c] and `DecodeMetaCode` splits `E(↕metadata, code)`; `Psi_A` rejects when the code is missing or larger than W_C = 4,000,000 (`PVM/accumulate_invocation.go:69-79`).

### 3.6 Disputes (GP §10)

**3.6.1 The pipeline.** `internal/extrinsic/dispute.go:9-85` runs, in order: per-verdict signature check (`VerifySignature`, also age check), verdict sort/unique, disjointness from ψ (`already_judged`), verdict sums, `ValidateCulprits`, `ValidateFaults`, culprit/fault sort/unique, `ClearWorkReports` (ρ†), `UpdatePsiGBW`, `VerifyCulpritValidity`, `VerifyFaultValidity`, `UpdatePsiO`, `HeaderOffenders`.

**3.6.2 Judgment signatures & age (10.3–10.4).** `internal/extrinsic/verdict_controller.go:53-102`

```go
func (v *VerdictWrapper) VerifySignature() error {

	state := blockchain.GetInstance().GetPriorStates()

	a := types.U32(state.GetTau()) / types.U32(types.EpochLength)
	if v.Verdict.Age != a && v.Verdict.Age != a-1 {
		return errors.New("bad_judgement_age")
	}

	k := make(types.ValidatorsData, types.ValidatorsCount)
	if v.Verdict.Age == a {
		k = state.GetKappa()
	} else {
		k = state.GetLambda()
	}

	// check if the judgement is valid
	VoteNum := len(v.Verdict.Votes)
	target := v.Verdict.Target[:]

	// store the index of votes with invalid signature
	invalidVotes := make([]int, 0, VoteNum)

	for i := 0; i < VoteNum; i++ {
		if int(v.Verdict.Votes[i].Index) >= len(k) {
			return errors.New("bad_guarantor_key")
		}
		publicKey := k[v.Verdict.Votes[i].Index].Ed25519[:]
		// Pre-allocate capacity: vote type (1 byte) + target (32 bytes)
		message := make([]byte, 0, 33)
		if v.Verdict.Votes[i].Vote {
			message = append(message, []byte(types.JamValid)...)
		} else {
			message = append(message, []byte(types.JamInvalid)...)
		}

		message = append(message, target...)

		if !ed25519consensus.Verify(publicKey, message, v.Verdict.Votes[i].Signature[:]) {
			invalidVotes = append(invalidVotes, i)
		}
	}

	if len(invalidVotes) > 0 {
		return errors.New("bad_signature")
	}
	return nil
}
```

Quiz angle: the verdict `Age` must be the current epoch (→ κ) or the previous one (→ λ), computed from the **prior** τ; messages are `"jam_valid"`/`"jam_invalid"` ⌢ report hash; every verdict must carry exactly ⌊2V/3⌋+1 = `ValidatorsSuperMajority` votes (`Verdict.Validate`, `types.go:861-866`).

**3.6.3 Verdict thresholds (10.11–10.12) and ρ† (10.15).** `internal/extrinsic/dispute_controller.go:86-106`, `verdict_controller.go:253-277`

```go
func CompareVerdictsWithPsi(disputeState types.DisputesRecords, verdictSumSequence []VerdictSummary) (types.DisputesRecords, error) {
	var updates types.DisputesRecords
	...
	for _, verdict := range verdictSumSequence {
		switch verdict.PositiveJudgmentsSum {
		case types.ValidatorsCount*2/3 + 1:
			updates.Good = append(updates.Good, types.WorkReportHash(verdict.ReportHash))
		case 0:
			updates.Bad = append(updates.Bad, types.WorkReportHash(verdict.ReportHash))
		case types.ValidatorsCount * 1 / 3:
			updates.Wonky = append(updates.Wonky, types.WorkReportHash(verdict.ReportHash))
		default:
			return types.DisputesRecords{}, errors.New("bad_vote_split")
		}
	}
	return updates, nil
}
```

```go
// ClearWorkReports clear uncertain or invalid work reports from core | Eq. 10.15
func (v *VerdictController) ClearWorkReports(verdictSumSequence []VerdictSummary) {
	cs := blockchain.GetInstance()
	priorStatesRho := cs.GetPriorStates().GetRho()
	// Pre-allocate capacity: estimate that about half of verdicts need clearing
	clearReports := make(map[types.WorkReportHash]bool, len(verdictSumSequence)/2)
	for _, verdict := range verdictSumSequence {
		if verdict.PositiveJudgmentsSum < types.ValidatorsCount*2/3 {
			clearReports[verdict.ReportHash] = true
		}
	}
	for i := range priorStatesRho {
		if priorStatesRho[i] == nil {
			continue
		}
		encoder := types.GetEncoder()
		encoded, _ := encoder.Encode(&priorStatesRho[i].Report)
		types.PutEncoder(encoder)
		hashReport := hash.Blake2bHash(encoded)
		if clearReports[types.WorkReportHash(hashReport)] {
			priorStatesRho[i] = nil
		}
	}
	cs.GetIntermediateStates().SetRhoDagger(priorStatesRho)
}
```

Quiz angle: positive-vote count must be exactly ⌊2V/3⌋+1 (good), 0 (bad) or ⌊V/3⌋ (wonky) — in tiny: 5, 0, 2; in full: 683, 0, 341; anything else is `bad_vote_split`. Bad and wonky verdicts clear the core's pending report in ρ† (the report is identified by H(E(report))).

**3.6.4 Culprit/fault cardinality (10.13–10.14) and validity (10.5–10.6).** `dispute_controller.go:28-65`, `culprit_controller.go:47-91`, `fault_controller.go:82-110`

```go
// ValidateFaults validates the faults in the verdict | Eq. 10.13
func (d *DisputeController) ValidateFaults() error {
	faultMap := make(map[types.WorkReportHash]bool, len(d.FaultController.Faults))
	for _, report := range d.FaultController.Faults {
		faultMap[report.Target] = true
	}

	good := types.ValidatorsCount*2/3 + 1
	for _, report := range d.VerdictController.VerdictSumSequence {
		if report.PositiveJudgmentsSum == good {
			if !faultMap[types.WorkReportHash(report.ReportHash)] {
				return errors.New("not_enough_faults")
			}
		}
	}
	return nil
}

// ValidateCulprits validates the culprits in the verdict | Eq. 10.14
func (d *DisputeController) ValidateCulprits() error {
	culpritMap := make(map[types.WorkReportHash]int, len(d.CulpritController.Culprits))

	for _, report := range d.CulpritController.Culprits {
		culpritMap[report.Target]++
	}

	bad := 0
	for _, report := range d.VerdictController.VerdictSumSequence {
		if report.PositiveJudgmentsSum == bad {
			if culpritMap[types.WorkReportHash(report.ReportHash)] < 2 {
				return errors.New("not_enough_culprits")
			}
		}
	}
	return nil
}
```

```go
func (c *CulpritController) VerifyCulpritSignature() error {
	state := blockchain.GetInstance().GetPriorStates()
	posterior := blockchain.GetInstance().GetPosteriorStates()

	validators := append(state.GetKappa(), state.GetLambda()...)
	validKeySet := make(map[types.Ed25519Public]struct{})
	for _, v := range validators {
		validKeySet[v.Ed25519] = struct{}{}
	}

	psiO := posterior.GetPsiO()
	for _, offender := range psiO {
		delete(validKeySet, offender)
	}

	for _, culprit := range c.Culprits {
		if _, ok := validKeySet[culprit.Key]; !ok {
			return errors.New("bad_guarantor_key")
		}
		msg := []byte(types.JamGuarantee)
		msg = append(msg, culprit.Target[:]...)
		if !ed25519consensus.Verify(culprit.Key[:], msg, culprit.Signature[:]) {
			return errors.New("bad_signature")
		}
	}
	return nil
}
```

```go
// VerifyReportHashValidty verifies the validity of the reports
func (f *FaultController) VerifyReportHashValidty() error {
	posteriorStates := blockchain.GetInstance().GetPosteriorStates()
	psiBad := posteriorStates.GetPsiB()
	psiGood := posteriorStates.GetPsiG()
	...
	length := len(f.Faults)
	for i := 0; i < length; i++ {
		vote := f.Faults[i].Vote
		// if vote not contradict verdict, should not be in faults
		inGood := goodMap[f.Faults[i].Target] && !badMap[f.Faults[i].Target]
		inBad := !goodMap[f.Faults[i].Target] && badMap[f.Faults[i].Target]
		if (vote && inGood) || (!vote && inBad) {
			return errors.New("fault_verdict_wrong")
		}
	}
	return nil
}
```

Quiz angle: a good verdict needs ≥1 fault (a validator who voted the *opposite* way), a bad verdict needs ≥2 culprits (guarantors, signing `"jam_guarantee"` ⌢ hash); culprit/fault keys must be in κ ∪ λ and not already in ψ_o (`offender_already_reported`); culprits' targets must be in ψ′_b (`culprits_verdict_not_bad`). Culprits/faults are sorted+unique by **Ed25519 key**, verdicts by report hash, judgments by validator index.

**3.6.5 ψ′_o (10.19) and H_o (10.20).** `dispute_controller.go:149-195` — ψ′_o = sort(ψ_o ∪ new culprit keys ∪ new fault keys); H_o is the (unsorted) list of new culprit keys followed by fault keys, which `ValidateHeaderOffenderMarker` (`markers.go:177-220`) compares element-wise.


### 3.7 Reporting & assurance (GP §11)

**3.7.1 Assurance signature, bitfield and availability threshold (11.13–11.16).** `internal/extrinsic/assurance_controller.go:118-189`

```go
// ValidateSignature validates the signature of the AvailAssurance | Eq. 11.13, 11.14
func (a *AvailAssuranceController) ValidateSignature() *types.ErrorCode {
	kappa := blockchain.GetInstance().GetPriorStates().GetKappa()

	for _, availAssurance := range a.AvailAssurances {
		anchor := utilities.OpaqueHashWrapper{Value: types.OpaqueHash(availAssurance.Anchor)}.Serialize()
		bitfield := utilities.ByteSequenceWrapper{Value: types.ByteSequence(availAssurance.Bitfield.ToOctetSlice())}.Serialize()
		hashed := hash.Blake2bHash(append(anchor, bitfield...))
		message := []byte(types.JamAvailable)
		message = append(message, hashed[:]...)

		publicKey := kappa[availAssurance.ValidatorIndex].Ed25519
		if !ed25519consensus.Verify(publicKey[:], message, availAssurance.Signature[:]) {
			errCode := AssuranceErrorCode.BadSignature
			return &errCode
		}
	}

	return nil
}

// ValidateBitField | Eq. 11.15
func (a *AvailAssuranceController) ValidateBitField() *types.ErrorCode {
	rhoDagger := blockchain.GetInstance().GetIntermediateStates().GetRhoDagger()

	for i := 0; i < len(a.AvailAssurances); i++ {
		for j := 0; j < types.CoresCount; j++ {
			// rhoDagger[j] nil : core j has no report to be process
			// assurers can not set nil core
			if a.AvailAssurances[i].Bitfield.GetBit(j) == 1 && rhoDagger[j] == nil {
				errCode := AssuranceErrorCode.CoreNotEngaged
				return &errCode
			}
		}
	}
	return nil
}

// Filter newly available work reports | Eq. 11.16
func (a *AvailAssuranceController) UpdateNewlyAvailableWorkReports(rhoDagger types.AvailabilityAssignments) []types.WorkReport {
	// Filter newly available work reports from rhoDagger
	totalAvailable := make([]int, types.CoresCount)

	// compute total availability of a report | at this moment of the workflow, the bitfield is transformed into a binary sequence.
	for i := 0; i < len(a.AvailAssurances); i++ {
		for j := 0; j < types.CoresCount; j++ {
			if a.AvailAssurances[i].Bitfield.GetBit(j) == 1 {
				totalAvailable[j]++
			}
		}
	}

	availableWorkReports := make([]types.WorkReport, 0, types.CoresCount/2)
	for i := 0; i < types.CoresCount; i++ {
		// If the votes for this core are greater than the available number, add the work report to the available work reports
		if totalAvailable[i] >= types.ValidatorsSuperMajority {
			// Get work reports from rhoDagger
			if rhoDagger[i] == nil {
				continue
			}

			// Append the work report to the available work reports
			availableWorkReports = append(availableWorkReports, rhoDagger[i].Report)
		}
	}

	// Set the available work reports to the available work reports
	blockchain.GetInstance().GetIntermediateStates().SetAvailableWorkReports(availableWorkReports)

	return availableWorkReports
}
```

Quiz angle: the assurance message is `"jam_available"` ⌢ H(E(H_p, bitfield)); the signer is κ[v] (prior κ); a bit may only be set where ρ†[c] ≠ ∅ (`CoreNotEngaged` = code 2); a report becomes available with **> 2/3 V** assurances, implemented as `>= ValidatorsSuperMajority` (5 of 6 in tiny, 683 of 1023 in full). Anchor must equal H_p (`BadAttestationParent`), assurers strictly ascending by index (`NotSortedOrUniqueAssurers`).

**3.7.2 ρ‡: clearing available or timed-out reports (11.17, U = 5).** `assurance_controller.go:203-238`

```go
// FilterAvailableReports | Eq. 11.16 & 11.17
func (a *AvailAssuranceController) FilterAvailableReports() *types.ErrorCode {
	cs := blockchain.GetInstance()

	rhoDagger := cs.GetIntermediateStates().GetRhoDagger()
	rhoDoubleDagger := cs.GetIntermediateStates().GetRhoDoubleDagger()
	rho := cs.GetPriorStates().GetRho()

	// 11.17 Set available reports or timeout reports to nil
	// Make a copy to avoid aliasing with rhoDagger
	copy(rhoDoubleDagger, rhoDagger)
	headerTimeSlot := cs.GetLatestBlock().Header.Slot

	// (11.16) Filter newly available work reports
	availableWorkReports := a.UpdateNewlyAvailableWorkReports(rhoDagger)

	// Create a map of available work reports for faster lookup
	availableWorkReportsMap := a.CreateWorkReportMap(availableWorkReports)

	for coreIndex := 0; coreIndex < types.CoresCount; coreIndex++ {
		if rho[coreIndex] == nil {
			continue
		}

		reportIsAvailable := availableWorkReportsMap[rho[coreIndex].Report.CoreIndex]
		reportIsTimeout := headerTimeSlot >= rhoDagger[coreIndex].AssignedSlot+types.TimeSlot(types.WorkReportTimeout)

		if reportIsAvailable || reportIsTimeout {
			rhoDoubleDagger[coreIndex] = nil
		}
	}

	cs.GetIntermediateStates().SetRhoDoubleDagger(rhoDoubleDagger)

	return nil
}
```

Quiz angle: timeout is `H_t ≥ t_assigned + U` with `WorkReportTimeout = 5`; GP 0.8.0 also clears when |κ| ≠ |κ′| (not implemented here — consistent with 0.7.2). Note the subtle aliasing: the guard tests `rho[coreIndex]` (prior ρ) but dereferences `rhoDagger[coreIndex].AssignedSlot`; this is only safe because `ClearWorkReports` (§3.6.3) nils the entry inside the **prior** ρ's backing array, so both slices agree (see gotcha #4 in §5).

**3.7.3 Guarantee extrinsic validation order (11.23–11.43).** `internal/extrinsic/guarantee.go:5-76` shows the whole sequence: `Validate` (core index, ≤ C guarantees, 2–3 signatures, ≤ J dependencies, output size ≤ W_R) → `Sort` (ascending unique core index, ascending unique signer index) → `ValidateSignatures` → `ValidateWorkReports` → `CardinalityCheck` → `ValidateContexts` → `ValidateWorkPackageHashes` → `CheckExtrinsicOrRecentHistory` → `CheckSegmentRootLookup` → `CheckWorkResult` → `TransitionWorkReport`.

**3.7.4 Guarantor signatures, rotation period R and G/G* (11.24–11.26).** `guarantee_controller.go:92-159`

```go
// ValidateSignatures | Eq. 11.26
func (g *GuaranteeController) ValidateSignatures() error {
	tau := blockchain.GetInstance().GetPosteriorStates().GetTau()
	offenders := blockchain.GetInstance().GetPosteriorStates().GetPsiO()
	offendersMap := make(map[types.Ed25519Public]bool, len(offenders))
	for _, offender := range offenders {
		offendersMap[offender] = true
	}

	// Parallelize signature verifications across guarantees
	eg := new(errgroup.Group)
	eg.SetLimit(types.MaxWorkers)

	for _, guarantee := range g.Guarantees {
		guarantee := guarantee

		var guranatorAssignments GuranatorAssignments
		var err error
		if (int(tau))/types.RotationPeriod == int(guarantee.Slot)/types.RotationPeriod {
			guranatorAssignments, err = GFunc(offendersMap)
		} else {
			guranatorAssignments, err = GStarFunc(offendersMap)
		}

		if err != nil {
			return err
		}

		if !((int(tau)/types.RotationPeriod-1)*types.RotationPeriod <= int(guarantee.Slot)) {
			err := ReportsErrorCode.ReportEpochBeforeLast
			return &err
		}

		if !(int(guarantee.Slot) <= int(tau)) {
			err := ReportsErrorCode.FutureReportSlot
			return &err
		}

		message := []byte(jam_types.JamGuarantee)
		encoder := types.NewEncoder()

		reportSerial, err := encoder.Encode(&guarantee.Report)
		if err != nil {
			return err
		}
		hashed := hash.Blake2bHash(reportSerial)
		message = append(message, hashed[:]...)

		// Parallelize signature verifications
		for _, sig := range guarantee.Signatures {
			sig := sig

			eg.Go(func() error {
				if guranatorAssignments.CoreAssignments[sig.ValidatorIndex] != guarantee.Report.CoreIndex {
					err := ReportsErrorCode.WrongAssignment
					return &err
				}
				publicKey := guranatorAssignments.PublicKeys[sig.ValidatorIndex].Ed25519[:]
				if !ed25519consensus.Verify(publicKey, message, sig.Signature[:]) {
					err := ReportsErrorCode.BadSignature
					return &err
				}
				return nil
			})
		}
	}
	return eg.Wait()
}
```

Quiz angle: guarantee slot t must satisfy `R⌊τ′/R⌋ − R ≤ t ≤ τ′` (previous rotation at most); same rotation → G (η′_2, κ′, τ′), earlier rotation → G* (either (η′_2, κ′) or, if the previous rotation was in the previous epoch, (η′_3, λ′), with slot τ′ − R). The signed message is `"jam_guarantee"` ⌢ H(E(report)).

**3.7.5 Guarantor assignment P (11.19–11.22) via the shuffle.** `internal/extrinsic/guarantor_assignments.go:27-57`, `83-133`

```go
// (11.19) R(c, n) = [(x + n) mod C | x ∈ c]
func rotateCores(in []types.U32, n types.U32) []types.U32 {
	out := make([]types.U32, len(in))
	for i, x := range in {
		out[i] = (x + n) % types.U32(types.CoresCount)
	}
	return out
}

// (11.20)
func permute(e types.Entropy, currentSlot types.TimeSlot) []types.CoreIndex {
	base := make([]types.U32, types.ValidatorsCount)
	for i := 0; i < types.ValidatorsCount; i++ {
		c := (types.CoresCount * i) / types.ValidatorsCount
		base[i] = types.U32(c)
	}

	shuffled := shuffle.Shuffle(base, types.OpaqueHash(e))

	subEpoch := (int(currentSlot) % types.EpochLength) / types.RotationPeriod

	// R(...) call
	rotatedU32 := rotateCores(shuffled, types.U32(subEpoch))

	// Convert back to []types.CoreIndex
	rotated := make([]types.CoreIndex, len(rotatedU32))
	for i, v := range rotatedU32 {
		rotated[i] = types.CoreIndex(v)
	}
	return rotated
}
```

```go
// (11.22) G∗ ≡ (P (e, τ ′ − R), Φ(k))
func GStarFunc(offendersMap map[types.Ed25519Public]bool) (GuranatorAssignments, error) {
	state := blockchain.GetInstance().GetPosteriorStates()
	var e types.Entropy
	validators := make(types.ValidatorsData, types.ValidatorsCount)

	etaPrime := state.GetEta()
	if (int(state.GetTau())-types.RotationPeriod)/types.EpochLength == int(state.GetTau())/types.EpochLength {
		// (η′2, κ′)
		e = etaPrime[2]
		validators = state.GetKappa()
		...
	} else {
		// (η′3, λ′)
		e = etaPrime[3]
		validators = state.GetLambda()
		...
	}

	return NewGuranatorAssignments(e, state.GetTau()-types.TimeSlot(types.RotationPeriod), validators), nil
}
```

Quiz angle: base assignment is `⌊C·i/V⌋` for validator i, Fisher–Yates shuffled by η′_2 (F.3), then rotated by `⌊(slot mod E)/R⌋`; keys are Φ-filtered (offender keys nulled) so a guarantor in ψ′_o is rejected (`BannedValidator`, code 23). `GuaranteeMinCount = 2`, `GuaranteeMaxCount = 3`.

**3.7.6 Work-report validity vs state: core engaged, authorizer in pool, gas limits (11.29–11.30).** `guarantee_controller.go:171-205`

```go
// ValidateWorkReports | Eq. 11.29-11.30
func (g *GuaranteeController) ValidateWorkReports() error {
	workReports := g.WorkReportSet()
	alpha := blockchain.GetInstance().GetPriorStates().GetAlpha()
	delta := blockchain.GetInstance().GetPriorStates().GetDelta()
	rhoDoubleDagger := blockchain.GetInstance().GetIntermediateStates().GetRhoDoubleDagger()
	for _, workReport := range workReports {
		if rhoDoubleDagger[workReport.CoreIndex] != nil {
			err := ReportsErrorCode.CoreEngaged
			return &err
		}
		authPool := alpha[workReport.CoreIndex]
		if !isAuthPoolContains(authPool, workReport.AuthorizerHash) {
			err := ReportsErrorCode.CoreUnauthorized
			return &err
		}
		totalGas := types.U64(0)
		for _, workResult := range workReport.Results {
			totalGas += types.U64(workResult.AccumulateGas)
			if _, serviceExists := delta[workResult.ServiceID]; !serviceExists {
				err := ReportsErrorCode.BadServiceID
				return &err
			}
			if workResult.AccumulateGas < delta[workResult.ServiceID].ServiceInfo.MinItemGas {
				err := ReportsErrorCode.ServiceItemGasTooLow
				return &err
			}
		}
		if totalGas > types.U64(types.MaxAccumulateGas) {
			err := ReportsErrorCode.WorkReportGasTooHigh
			return &err
		}
	}
	return nil
}
```

Quiz angle: the authorizer must be in the **prior** α[c] (α′ is only computed later), the core must be free in ρ‡, each result's accumulate gas ≥ the service's a_g, and the sum ≤ G_A = 10,000,000.

**3.7.7 Context anchors and lookup-anchor age (11.33–11.35, L).** `guarantee_controller.go:253-323` — anchor must be in β† with matching state root and beefy root (`AnchorNotRecent` / `BadStateRoot` / `BadBeefyMmrRoot`), lookup anchor slot must satisfy `H_t − x_t ≤ L` (`MaxLookupAge`, 24 tiny / 14400 full; the code returns `ReportEpochBeforeLast` for this case), and if an ancestry set is loaded (fuzzer `SetState` ancestry) the lookup anchor hash must appear at that slot (`LookupAnchorNotRecent`).

**3.7.8 Duplicate packages and dependency resolution (11.36–11.41).** `guarantee_controller.go:325-455` — a package hash must not be in ϑ, ρ, ξ or β (`DuplicatePackage`); every prerequisite and every segment-root-lookup key must be either in this extrinsic or in β's reported packages (`DependencyMissing` / `SegmentRootLookupInvalid`); segment-root lookup values must equal the exports root recorded for that package (`CheckSegmentRootLookup`).

**3.7.9 ρ′ (11.43).** `guarantee_controller.go:472-490`

```go
// Transitioning for work reports | Eq. 11.43
func (g *GuaranteeController) TransitionWorkReport() {
	cs := blockchain.GetInstance()
	rhoDoubleDagger := cs.GetIntermediateStates().GetRhoDoubleDagger()
	posteriorTau := cs.GetPosteriorStates().GetTau()

	for _, guarantee := range g.Guarantees {
		rhoDoubleDagger[guarantee.Report.CoreIndex] = &types.AvailabilityAssignment{
			Report:       guarantee.Report,
			AssignedSlot: posteriorTau,
		}
	}

	cs.GetPosteriorStates().SetRho(rhoDoubleDagger)

	// Save the work reports to the store
	workReports := g.WorkReportSet()
	cs.GetIntermediateStates().SetPresentWorkReports(workReports)
}
```

Quiz angle: the assignment timestamp is τ′ (the block's slot), not the guarantee's slot t.

**3.7.10 Report-level limits.** `internal/types/types.go:577-603`

```go
// ValidateLookupDictAndPrerequisites checks the number of SegmentRootLookup and Prerequisites < J
// GP §11.3
func (w *WorkReport) ValidateLookupDictAndPrerequisites() error {
	if len(w.SegmentRootLookup)+len(w.Context.Prerequisites) > MaximumDependencyItems {
		logger.Warnf("SegmentRootLookup and Prerequisites must have a total at most %d, but got %d", MaximumDependencyItems, len(w.SegmentRootLookup)+len(w.Context.Prerequisites))
		return errors.New("too_many_dependencies")
	}
	return nil
}

// ValidateOutputSize checks the total size of the output
// GP §11.8
func (w *WorkReport) ValidateOutputSize() error {
	totalSize := len(w.AuthOutput)
	for _, result := range w.Results {
		// only compute $\mathcal{B}$ => ok
		if result.Result.Type == WorkExecResultOk {
			totalSize += len(result.Result.Data)
		}
	}

	if totalSize > WorkReportOutputBlobsMaximumSize {
		logger.Warnf("total size %d is greater than WorkReportOutputBlobsMaximumSize %d", totalSize, WorkReportOutputBlobsMaximumSize)
		return errors.New("work_report_too_big")
	}
	return nil
}
```

Quiz angle: J = 8 total dependencies (prerequisites + segment-root lookups), W_R = 48 KiB for auth output + all OK result blobs.

### 3.8 Accumulation (GP §12)

**3.8.1 Queue editing E, priority queue Q, D and P (12.6–12.9).** `internal/accumulation/accumulation.go:86-178`

```go
// (12.6) D(w) ≡ (w, {(wx)p} ∪ K(wl))
// Extract all dependencies from single work report
func GetDependencyFromWorkReport(report types.WorkReport) (output types.ReadyRecord) {
	output.Report = report
	totalDeps := len(report.Context.Prerequisites) + len(report.SegmentRootLookup)
	output.Dependencies = make([]types.WorkPackageHash, 0, totalDeps)
	// Add all explicit prerequisites (wx)p to the dependency list
	for _, hash := range report.Context.Prerequisites {
		output.Dependencies = append(output.Dependencies, types.WorkPackageHash(hash))
	}

	// Add all work package hashes found in the segment root lookup (i.e., K(wl))
	for _, segment := range report.SegmentRootLookup {
		output.Dependencies = append(output.Dependencies, types.WorkPackageHash(segment.WorkPackageHash))
	}
	return output
}

// (12.7)
func QueueEditingFunction(r types.ReadyQueueItem, x []types.WorkPackageHash) (newQueue types.ReadyQueueItem) {
	finishedReportHashes := make(map[types.WorkPackageHash]bool, len(x))
	for _, h := range x {
		finishedReportHashes[h] = true
	}
	for _, item := range r {
		// If the report itself is already accumulated, skip it, remove from queue
		if _, exist := finishedReportHashes[item.Report.PackageSpec.Hash]; exist {
			continue
		}
		// Otherwise, filter its dependencies: keep only those NOT in the finished set
		remainingDeps := make([]types.WorkPackageHash, 0, len(item.Dependencies))
		for _, dep := range item.Dependencies {
			if _, exist := finishedReportHashes[dep]; !exist {
				remainingDeps = append(remainingDeps, dep)
			}
		}

		// Update the item with pruned dependencies and keep it in the new queue
		item.Dependencies = remainingDeps
		newQueue = append(newQueue, item)
	}
	return newQueue
}

// (12.8) Q get accumulatable work reports

func AccumulationPriorityQueue(r types.ReadyQueueItem) (output []types.WorkReport) {
	g := make([]types.WorkReport, 0, len(r))

	// Collect all reports that are ready for accumulation (i.e., dependencies resolved)
	for _, item := range r {
		if len(item.Dependencies) == 0 {
			g = append(g, item.Report)
		}
	}

	// If no items are currently eligible, return empty result
	if len(g) == 0 {
		return output
	}

	output = g
	// Recursively prune the queue and resolve additional eligible reports
	hashes := ExtractWorkReportHashes(g)
	recursivelyReadyReports := AccumulationPriorityQueue(QueueEditingFunction(r, hashes))
	output = append(output, recursivelyReadyReports...)
	return output
}
```

**3.8.2 W! / W_Q / W* (12.4, 12.5, 12.10–12.12).** `accumulation.go:51-84`, `183-233`

```go
// (12.4) W! ≡ [w S w <− W, S(wx)pS = 0 ∧ wl = {}]
func UpdateImmediatelyAccumulateWorkReports() {
	intermediateState := blockchain.GetInstance().GetIntermediateStates()
	availableReports := intermediateState.GetAvailableWorkReports()

	accumulatableReports := make([]types.WorkReport, 0, len(availableReports)/2)
	for _, report := range availableReports {
		// Check for no prerequisites and no segment root lookup dependencies
		if len(report.Context.Prerequisites) == 0 && len(report.SegmentRootLookup) == 0 {
			accumulatableReports = append(accumulatableReports, report)
		}
	}
	// Store W! — immediately accumulatable work reports
	intermediateState.SetAccumulatedWorkReports(accumulatableReports)
}
```

```go
// (12.10) let m = Ht mod E(12.10)
// (12.11) W∗ ≡ W! ⌢ Q(q)
// (12.12) q = E(ϑm... ⌢ ϑ...m ⌢ WQ, P (W!))
func UpdateAccumulatableWorkReports() {
	cs := blockchain.GetInstance()

	// (12.10) Get current slot index 'm'
	slot := cs.GetLatestBlock().Header.Slot
	E := types.EpochLength
	m := int(slot) % E

	vartheta := cs.GetPriorStates().GetVartheta()
	WQ := cs.GetIntermediateStates().GetQueuedWorkReports()
	Wbang := cs.GetIntermediateStates().GetAccumulatedWorkReports()

	// E(ϑm... ⌢ ϑ...m ⌢ WQ)
	...
	composedQueue := make(types.ReadyQueueItem, 0, composedQueueCapacity)

	for _, record := range vartheta[m:] {
		composedQueue = append(composedQueue, record...)
	}

	for _, record := range vartheta[:m] {
		composedQueue = append(composedQueue, record...)
	}

	composedQueue = append(composedQueue, WQ...)

	accumulatedHashes := ExtractWorkReportHashes(Wbang)

	// (12.12) Compute q = E(..., P(W!))
	// Use accumulated hashes from W! to prune dependencies
	q := QueueEditingFunction(composedQueue, accumulatedHashes)

	// (12.11) W* ≡ W! ⌢ Q(q)
	// Reconstruct W* by appending newly-resolved reports to previously accumulated W!
	qResult := AccumulationPriorityQueue(q)
	WStar := make([]types.WorkReport, 0, len(Wbang)+len(qResult))
	WStar = append(WStar, Wbang...)
	WStar = append(WStar, qResult...)

	// Update W*
	cs.GetIntermediateStates().SetAccumulatableWorkReports(WStar)
}
```

Quiz angle: the ready queue is read **oldest-first starting at slot index m** (ϑ[m..] ⌢ ϑ[..m]), then this block's W_Q; the only hashes pruned before Q are P(W!) (W_Q itself was already pruned against ©ξ in `UpdateQueuedWorkReports`, `accumulation.go:69-84`).

**3.8.3 Outer accumulation ∆+ (12.16): gas-bounded prefix and recursion.** `accumulation.go:235-332`

```go
// (12.16) ∆+ outer accumulation function
func OuterAccumulation(input OuterAccumulationInput) (output OuterAccumulationOutput, err error) {
	defer timing.Track("accumulation.OuterAccumulation")()

	// input parameters
	g := input.GasLimit
	t := input.DeferredTransfers
	r := input.WorkReports
	e := input.InitPartialStateSet
	f := input.ServicesWithFreeAccumulation

	gasSum := types.Gas(0)
	i := 0

	// Determine the maximal prefix of reports that fits within the gas limit
	for idx, report := range r {
		for _, result := range report.Results {
			gasSum += result.AccumulateGas
		}
		if gasSum <= g {
			i = idx + 1
		} else {
			break
		}
	}
	// n = |t| + i + |f|
	n := len(t) + i + len(f)
	if n == 0 {
		output.NumberOfWorkResultsAccumulated = 0
		output.PartialStateSet = e
		output.AccumulatedServiceOutput = make(map[types.AccumulatedServiceHash]bool)
		output.ServiceGasUsedList = []types.ServiceGasUsed{}
		return output, nil
	}

	// Accumulate the first i reports in parallel across services (∆)
	//(e∗, t∗, b∗, u∗) = ∆∗(e, t, r...i, f)
	parallelInput := ParallelizedAccumulationInput{
		PartialStateSet:     e,
		DeferredTransfers:   t,
		WorkReports:         r[:i],
		AlwaysAccumulateMap: f,
	}

	parallelResult, err := ParallelizedAccumulation(parallelInput)
	eStar := parallelResult.PartialStateSet
	tStar := parallelResult.DeferredTransfers
	bStar := parallelResult.AccumulatedServiceOutput
	uStar := parallelResult.ServiceGasUsedList
	...
	// Recurse on the remaining reports with the remaining gas
	// (j, e′, b, u) = ∆+(g∗ − ∑(s,u)∈u∗(u), t∗, ri..., e∗, {})
	gStar := input.GasLimit
	for _, DeferredTransfer := range t {
		gStar += DeferredTransfer.GasLimit
	}

	gasLimitForRecursion := gStar
	for _, u := range uStar {
		gasLimitForRecursion -= u.Gas
	}
	recursiveOuterInput := OuterAccumulationInput{
		GasLimit:                     gasLimitForRecursion,
		DeferredTransfers:            tStar,
		WorkReports:                  r[i:],
		InitPartialStateSet:          eStar,
		ServicesWithFreeAccumulation: make(map[types.ServiceID]types.Gas), // {}
	}
	recursiveOuterOutput, err := OuterAccumulation(recursiveOuterInput)
	...
	{
		output.NumberOfWorkResultsAccumulated = types.U64(i) + j
		output.PartialStateSet = ePrime // need to set post state?
		// merge b_star and b
		bUnion := make(map[types.AccumulatedServiceHash]bool, len(bStar)+len(b))
		maps.Copy(bUnion, bStar)
		maps.Copy(bUnion, b)
		output.AccumulatedServiceOutput = bUnion
		combinedGasUsed := make(types.ServiceGasUsedList, 0, len(uStar)+len(u))
		combinedGasUsed = append(combinedGasUsed, uStar...)
		combinedGasUsed = append(combinedGasUsed, u...)
		output.ServiceGasUsedList = combinedGasUsed
	}

	return output, nil
}
```

Quiz angle: i = largest prefix whose summed accumulate-gas ≤ g; recursion passes **empty** free-accumulation map (privileged services accumulate only in the first round) and the gas limit reduced by actual gas used; deferred transfers from round k feed round k+1 (12.3 "deferred transfers and state integration" — note the file name `deferred_transfers.go` and the comment "v0.7.1 has removed deferred transfers & Ψ_T": transfers are now delivered as accumulate inputs, no separate on_transfer PVM invocation).

**3.8.4 Parallel accumulation ∆* (12.17): the privileged merge rule R and δ′ = (d ∪ n) \ m.** `accumulation.go:334-378`, `585-731`

```go
// (12.20)
func R[T comparable](o, a, b T) T {
	if a == o {
		return b
	} else {
		return a
	}
}
```

```go
	singleOutput, err := runSingleReplaceService(input.PartialStateSet.Bless, singleInput)
	if err != nil {
		return output, fmt.Errorf("single service accumulation for bless failed: %w", err)
	}
	// e∗ = ∆(m)e
	eStar := singleOutput.PartialStateSet
	// m′, z′ = e∗(m, z)
	mPrime := eStar.Bless
	zPrime := eStar.AlwaysAccum

	// ∀c ∈ NC ∶ a′c = R(ac, (e∗a)c, ((∆(ac)e)a)c)
	aPrime := make(types.ServiceIDList, types.CoresCount)
	...
			g.Go(func() error {
				singleOutput, err := runSingleReplaceService(serviceID, singleInput)
				...
				aPrime[c] = R(serviceID, eStar.Assign[c], singleOutput.PartialStateSet.Assign[c])
				return nil
			})
	...
	// v' = R(v, e∗v , (∆(v)e)v )
	var vPrime, rPrime types.ServiceID
	singleOutput, err = runSingleReplaceService(input.PartialStateSet.Designate, singleInput)
	...
	vPrime = R(input.PartialStateSet.Designate, eStar.Designate, singleOutput.PartialStateSet.Designate)

	// r′ = R(r, e∗r , (∆(r)e)r)
	singleOutput, err = runSingleReplaceService(input.PartialStateSet.CreateAcct, singleInput)
	...
	rPrime = R(input.PartialStateSet.CreateAcct, eStar.CreateAcct, singleOutput.PartialStateSet.CreateAcct)

	// i′ = (∆(v)e)i
	var iPrime types.ValidatorsData
	{
		singleOutput, err := runSingleReplaceService(input.PartialStateSet.Designate, singleInput)
		...
		iPrime = singleOutput.PartialStateSet.ValidatorKeys
	}

	// ∀c ∈ NC ∶ q′c = ((∆(ac)e)q)c
	var qPrime types.AuthQueues
	...
				qPrime[c] = singleOutput.PartialStateSet.Authorizers[c]
	...
	// (d ∪ n) ∖ m
	// d′ = P ((d ∪ n) ∖ m, ⋃ ∆(s)p)
	dPrime, err := Provide(merge(d, n, m), p)
	...
	// Set posterior state
	{
		cs := blockchain.GetInstance()
		cs.GetPosteriorStates().SetChi(types.Privileges{
			Bless:       mPrime,
			Assign:      aPrime,
			Designate:   vPrime,
			CreateAcct:  rPrime,
			AlwaysAccum: zPrime,
		})
		cs.GetPosteriorStates().SetVarphi(qPrime)
		cs.GetPosteriorStates().SetIota(iPrime)
		cs.GetPosteriorStates().SetDelta(dPrime)
	}
```

Quiz angle: each service in s = {services with results} ∪ K(f) ∪ {transfer recipients} is accumulated once (deduplicated with `singleflight`) on a **deep copy** of the partial state; the manager m's output decides m′ and z′ (always-accumulate map); assigner a_c / delegator v / registrar r each get "the privileged service's own value unless the manager changed it" (R(o,a,b) = b if a == o else a); ι′ comes from the designate service, φ′[c] from assigner c; new accounts n come from services' outputs, deleted accounts m are removed. `Provide` (`extrinsic_preimage.go:248-271`) integrates `provide`d preimages whose request slot-set is `[]`.

**3.8.5 Single-service accumulation ∆1 (12.20) → Ψ_A.** `accumulation.go:734-820`

```go
	// U(fs, 0)
	g := types.Gas(0)
	if preset, ok := f[input.ServiceID]; ok {
		g = preset
	}

	// iU: all accumulate work result operands for service s
	for _, r := range r {
		for _, d := range r.Results {
			if d.ServiceID == s {
				//    ∑(rg )
				// w∈w,r∈wr,rs=s
				g += d.AccumulateGas
				// Construct operand
				operand := types.Operand{
					PayloadHash:    d.PayloadHash,             // l: dl
					GasLimit:       d.AccumulateGas,           // g: dg
					Result:         d.Result,                  // y: dy
					AuthOutput:     r.AuthOutput,              // t: rt
					Hash:           r.PackageSpec.Hash,        // h: (rs)p — work package hash，
					ExportsRoot:    r.PackageSpec.ExportsRoot, // e: (rs)e — exports root
					AuthorizerHash: r.AuthorizerHash,          // a: ra — authorizer hash
				}
				iU = append(iU, operand)
			}
		}
	}

	// iT: all deferred transfers for service s
	for _, deferredTransfer := range t {
		if deferredTransfer.ReceiverID == input.ServiceID {
			iT = append(iT, deferredTransfer)
			g += deferredTransfer.GasLimit
		}
	}

	sort.Slice(iT, func(i, j int) bool {
		return iT[i].SenderID < iT[j].SenderID
	})

	//  iT ⌢ iU
	pvmItems := make([]types.OperandOrDeferredTransfer, 0, len(iT)+len(iU))
	...
	// (e, w, f , s)↦ ΨA(e, τ′, s, g, iT ⌢ iU )
	storageKeyVal := input.UnmatchedKeyVals
	var pvmResult PVM.Psi_A_ReturnType
	func() {
		defer timing.Track("PVM.Psi_A")()
		pvmResult = PVM.Psi_A(e, tauPrime, s, g, pvmItems, eta0, storageKeyVal)
	}()
```

Quiz angle: gas for service s = free-accumulation allowance f[s] + Σ accumulate-gas of its results + Σ gas of incoming transfers; inputs are transfers first (sorted by sender) then operands in report order.

**3.8.6 Ψ_A (B.8): argument encoding, balance credit, and result handling C (B.13).** `PVM/accumulate_invocation.go:21-143`, `159-191`

```go
	// s = e
	var balances uint64
	for _, v := range operandOrDeferTransfers {
		if v.DeferredTransfer != nil {
			balances += uint64(v.DeferredTransfer.Balance)
		}
	}
	s.ServiceInfo.Balance += types.U64(balances)
	partialState.ServiceAccounts[serviceId] = s

	// (9.4) E(↕m, c) = ap[ac]
	// Get actual code (c)
	codeHash := s.ServiceInfo.CodeHash
	_, code, err := service_account.FetchCodeByHash(s, codeHash)
	...
	// if c = ∅ or |c| > W_C
	if !ok || len(code) == 0 || len(code) > types.MaxServiceCodeSize {
		return Psi_A_ReturnType{...}
	}

	var serialized []byte
	encoder := types.NewEncoder()

	// Encode t
	encoded, err := encoder.EncodeUint(uint64(timeslot))
	...
	// Encode s
	encoded, err = encoder.EncodeUint(uint64(serviceId))
	...
	// Encode |o|
	encoded, err = encoder.EncodeUint(uint64(len(operandOrDeferTransfers)))
	...
	resultM := Psi_M(StandardCodeFormat(code), 5, types.Gas(gas), Argument(serialized), AccumulateOmegas, addition)
```

```go
// (B.13) C
func C(gas types.Gas, reasonOrBytes any, resultContext AccumulateArgs) (types.PartialStateSet, []types.DeferredTransfer, *types.OpaqueHash, types.Gas, types.ServiceBlobs, types.StateKeyVals) {
	serviceBlobs := make(types.ServiceBlobs, 0)
	switch reasonOrBytes := reasonOrBytes.(type) {
	case error: // system error
		...
		return resultContext.ResultContextY.PartialState, resultContext.ResultContextY.DeferredTransfers, resultContext.ResultContextY.Exception, gas, serviceBlobs, *resultContext.ResultContextY.StorageKeyVal
	case []byte:
		var h types.OpaqueHash
		if len(reasonOrBytes) != len(h) {
			return resultContext.ResultContextX.PartialState, resultContext.ResultContextX.DeferredTransfers, resultContext.ResultContextX.Exception, gas, serviceBlobs, *resultContext.ResultContextX.StorageKeyVal
		}
		copy(h[:], reasonOrBytes[:len(h)])
		opaqueHash := &h
		...
		return resultContext.ResultContextX.PartialState, resultContext.ResultContextX.DeferredTransfers, opaqueHash, gas, serviceBlobs, *resultContext.ResultContextX.StorageKeyVal
	default:
		if reasonOrBytes == OUT_OF_GAS || reasonOrBytes == PANIC {
			...
			return resultContext.ResultContextY.PartialState, resultContext.ResultContextY.DeferredTransfers, resultContext.ResultContextY.Exception, gas, serviceBlobs, *resultContext.ResultContextY.StorageKeyVal
		}
		...
		return resultContext.ResultContextX.PartialState, ...
	}
}
```

Quiz angle: the accumulate entry point is PC **5**; argument = E(τ′) ⌢ E(s) ⌢ E(|inputs|) (the inputs themselves are read through `fetch` 14/15); incoming transfer balances are credited **before** execution; on PANIC/OOG the **checkpointed** context Y is committed (`checkpoint` deep-copies X into Y, `host_call_accumulate.go:233-247`); a 32-byte return blob becomes the accumulation output hash (θ′/`yield` also sets `Exception`), any other length yields none.

**3.8.7 New service index derivation I (B.10) and `check` (B.14).** `PVM/accumulate_invocation.go:193-236`, `host_call_general.go:961-970`

```go
	hash := hash.Blake2bHash(serialized)

	var result types.ServiceID
	decoder := types.NewDecoder()
	err = decoder.Decode(hash[:], &result)
	...
	var modValue types.ServiceID = (1 << 32) - types.MinimumServiceIndex - (1 << 8) // 2^32 - S - 2^8
	var addValue types.ServiceID = types.MinimumServiceIndex                        // 2^8
	result = check((result%modValue)+addValue, partialState.ServiceAccounts)
```

```go
// B.14
func check(serviceID types.ServiceID, serviceAccountState types.ServiceAccountState) types.ServiceID {
	for {
		if _, accountExists := serviceAccountState[serviceID]; !accountExists {
			return serviceID
		}

		serviceID = (serviceID-types.MinimumServiceIndex+1)%(1<<32-(1<<8)-types.MinimumServiceIndex) + types.MinimumServiceIndex
	}
}
```

Quiz angle: i = check(decode_4(Blake2b(E(s) ⌢ η′_0 ⌢ E(τ′)))[..4] mod (2^32 − S − 2^8) + S) with S = `MinimumServiceIndex` = 65536 (2^16); `check` linearly probes for a free index. After `new` creates the account, the next candidate is `check(S + (i − S + 42) mod (2^32 − S − 2^8))` (`host_call_accumulate.go:356`).

**3.8.8 ξ′ and ϑ′ (12.31–12.33) and δ‡ last-accumulation slot.** `internal/accumulation/deferred_transfers.go:120-213`

```go
// (12.28) (12.29)
// Build delta double dagger (second intermediate state)
// NOTE: v0.7.1 has removed deferred transfers & Ψ_T
func updateDeltaDoubleDagger(cs *blockchain.ChainState, accumulationStatistics types.AccumulationStatistics) {
	deltaDagger := cs.GetIntermediateStates().GetDeltaDagger()
	tauPrime := cs.GetPosteriorStates().GetTau()

	deltaDoubleDagger := types.ServiceAccountState{}

	for serviceID, acc := range deltaDagger {
		// If this service was actually accumulated this round
		if _, ok := accumulationStatistics[serviceID]; ok {
			acc.ServiceInfo.LastAccumulationSlot = tauPrime
		}
		deltaDoubleDagger[serviceID] = acc
	}
	cs.GetIntermediateStates().SetDeltaDoubleDagger(deltaDoubleDagger)
}

// (12.31) (12.32)
// Update the AccumulatedQueue(AccumulatedQueue)
func updateXi(cs *blockchain.ChainState, n types.U64) {
	// Get W^* (accumulatable work-reports in this block)
	accumulatableWorkReports := cs.GetIntermediateStates().GetAccumulatableWorkReports()

	priorXi := cs.GetPriorStates().GetXi()
	posteriorXi := cs.GetPosteriorStates().GetXi()

	// (12.31) Update the last element
	posteriorXi[types.EpochLength-1] = ExtractWorkReportHashes(accumulatableWorkReports[:n])

	// (12.32)
	// Update the rest of the elements
	for i := 0; i < types.EpochLength-1; i++ {
		posteriorXi[i] = priorXi[i+1]
	}
	// WONDER: this sort is not mentioned in the graypaper
	for _, x := range posteriorXi {
		slices.SortFunc(x, func(a, b types.WorkPackageHash) int {
			return bytes.Compare(a[:], b[:])
		})
	}

	// Update posteriorXi to cs
	cs.GetPosteriorStates().SetXi(posteriorXi)
}

// (12.33)
// Update ReadyQueue(Vartheta)
func updateVartheta(cs *blockchain.ChainState) {
	// (12.10) let m = H_t mode E
	headerSlot := cs.GetLatestBlock().Header.Slot
	m := int(headerSlot) % types.EpochLength
	...
	tauOffset := tauPrime - tau
	...
	for i := 0; i < types.EpochLength; i++ {
		// s[i]↺ ≡ s[ i % ∣s∣ ]
		index := (m - i + types.EpochLength) % types.EpochLength
		index = index % len(posteriorVartheta)

		firstCondition := i == 0
		secondCondition := (1 <= i) && (i < int(tauOffset))
		thirdCondition := i >= int(tauOffset)

		if firstCondition {
			posteriorVartheta[index] = QueueEditingFunction(queueWorkReports, posteriorXi[types.EpochLength-1])
		} else if secondCondition {
			posteriorVartheta[index] = types.ReadyQueueItem{}
		} else if thirdCondition {
			posteriorVartheta[index] = QueueEditingFunction(priorVartheta[index], posteriorXi[types.EpochLength-1])
		}
	}

	// Update posterior Vartheta
	cs.GetPosteriorStates().SetVartheta(posteriorVartheta)
}
```

Quiz angle: ξ is a length-E ring: shift left, put the hashes of the first n accumulated reports of W* in the last slot (ξ is a *set* per slot — the code sorts, "WONDER" comment); ϑ′[m] = E(W_Q, ξ′[E−1]); slots for skipped timeslots (1 ≤ i < τ′−τ) are emptied; older slots are pruned with E against the just-accumulated set.

**3.8.9 Gas ceiling for a block (12.20) and accumulation statistics (12.28–12.29).** `deferred_transfers.go:22-31`, `92-118`

```go
// Calculate max gas used v0.6.4 (12.20)
func calculateMaxGasUsed(alwaysAccumulateMap types.AlwaysAccumulateMap) types.Gas {
	GT := types.Gas(types.TotalGas)
	GA := types.Gas(types.MaxAccumulateGas)
	C := types.Gas(types.CoresCount)

	sum := sumPrivilegesGas(alwaysAccumulateMap)

	return max(GT, GA*C+sum)
}
```

Quiz angle: g = max(G_T, G_A·C + Σ χ_g gas). S(s) = (Σ gas used by s, number of work results for s among the first n reports) and only services with a nonzero entry appear (feeds π_S "accumulate_count / accumulate_gas_used").

**3.8.10 Preimage extrinsic (12.35–12.43).** `internal/accumulation/extrinsic_preimage.go:28-60`, `106-150`, `183-242`

```go
// v0.6.4 (12.36) R function determines whether a preimage should be integrated
func ShouldIntegratePreimage(d types.ServiceAccountState, s types.ServiceID, h types.OpaqueHash, l types.U32, keyVals *types.StateKeyVals, parseToState bool) bool {
	// Check for existence of the service account
	account, isInAccount := d[s]
	if !isInAccount || account.PreimageLookup == nil || account.LookupDict == nil {
		return false
	}

	// Check if the preimage hash is not in the service account's preimage map
	_, isInPreimageMap := account.PreimageLookup[h]

	// Construct lookup key
	lookupKey := types.LookupMetaMapkey{
		Hash:   h,
		Length: l,
	}

	// Check if the lookupKey have been set before(time slot set is not empty)
	timeSlotSet, lookupKeyExists := account.LookupDict[lookupKey]
	if !lookupKeyExists {
		if parseToState {
			return lookupAndRemoveKeyVal(keyVals, lookupKey, s)
			// only parseToState == true (filter deltaDoubleDagger) needs to remove keyVal and parse to service lookupDict
		} else {
			return lookupInKeyVal(*keyVals, lookupKey, s)
		}
	}

	// Condition: hash does not exist in preimage map, and lookup time slot set is empty
	return !isInPreimageMap && (len(timeSlotSet) == 0)
}
```

```go
// v0.7.0 (12.39)
func validateSortUnique(eps types.PreimagesExtrinsic) *types.ErrorCode {
	// If eps is not sorted, return error
	for i := 1; i < len(eps); i++ {
		if eps[i-1].Requester > eps[i].Requester {
			errCode := PreimageErrorCode.PrimagesNotSortedUnique
			return &errCode
		}

		if eps[i-1].Requester == eps[i].Requester && bytes.Compare(eps[i-1].Blob, eps[i].Blob) >= 0 {
			errCode := PreimageErrorCode.PrimagesNotSortedUnique
			return &errCode
		}
	}

	return nil
}
```

```go
// UpdateDeltaWithExtrinsicPreimage updates the deltaDoubleDagger state with filtered preimages
// It integrates preimages into deltaDoubleDagger using the provided tauPrime time slot
// v0.6.4 (12.39)
func UpdateDeltaWithExtrinsicPreimage(eps types.PreimagesExtrinsic, deltaDoubleDagger types.ServiceAccountState, tauPrime types.TimeSlot) (types.ServiceAccountState, error) {
	for _, ep := range eps {
		preimageHash := hash.Blake2bHash(ep.Blob)
		preimageLength := types.U32(len(ep.Blob))
		lookupKey := types.LookupMetaMapkey{
			Hash:   preimageHash,
			Length: preimageLength,
		}
		...
		// Update map
		serviceAccount.LookupDict[lookupKey] = types.TimeSlotSet{tauPrime}
		serviceAccount.PreimageLookup[preimageHash] = ep.Blob

		// Write updated serviceAccount back to deltaDoubleDagger
		deltaDoubleDagger[ep.Requester] = serviceAccount
	}

	return deltaDoubleDagger, nil
}
```

Quiz angle: a preimage is accepted only if the service exists, the hash is **not** yet in a_p and a_l[(H(d), |d|)] == [] (requested, unprovided); E_P must be sorted by (requester, blob) and unique (`preimages not sorted and unique`; `preimage not required` otherwise); integration writes a_l ← [τ′] and a_p ← blob. Validation uses the **prior** δ (before accumulation) while integration is applied to δ‡ (after accumulation), matching the GP "merge and join". An "unmatched key-val" equal to the single byte `0x00` (an encoded empty timeslot set) counts as a pending request.

### 3.9 Statistics (GP §13)

**3.9.1 Validator statistics rollover and counters (13.3–13.5).** `internal/statistics/statistics.go:460-504`, `31-107`

```go
// (13.3)
// π ≡ (πV , πL, πC , πS)
// (πV, πL) => (current, last)
func UpdateValidatorActivityStatistics() {
	cs := blockchain.GetInstance()

	extrinsic := cs.GetLatestBlock().Extrinsic

	preTau := cs.GetPriorStates().GetTau()
	postTau := cs.GetPosteriorStates().GetTau()

	preEpochIndex := GetEpochIndex(preTau)
	postEpochIndex := GetEpochIndex(postTau)

	preStatistics := cs.GetPriorStates().GetPi()

	if preEpochIndex == postEpochIndex {
		// If the epoch index is the same, we will keep using the same statistics.
		valsCurrent := preStatistics.ValsCurr
		valsLast := preStatistics.ValsLast
		cs.GetPosteriorStates().SetPiCurrent(valsCurrent)
		cs.GetPosteriorStates().SetPiLast(valsLast)
	} else {
		// If the epoch index is different, we will reset the statistics.
		valsCurrent := make(types.ValidatorsStatistics, types.ValidatorsCount)
		valsLast := preStatistics.ValsCurr
		cs.GetPosteriorStates().SetPiCurrent(valsCurrent)
		cs.GetPosteriorStates().SetPiLast(valsLast)
	}

	var wg sync.WaitGroup
	wg.Add(3)

	go func() {
		defer wg.Done()
		UpdateCurrentStatistics(extrinsic)
	}()
	go func() {
		defer wg.Done()
		UpdateCoreActivityStatistics(extrinsic)
	}()
	go func() {
		defer wg.Done()
		UpdateServiceActivityStatistics(extrinsic)
	}()

	wg.Wait()
}
```

```go
// b: The number of blocks produced by the validator.
func UpdateBlockStatistics(statistics *types.Statistics, authorIndex types.ValidatorIndex) {
	statistics.ValsCurr[authorIndex].Blocks++
}

// t: The number of tickets introduced by the validator.
func UpdateTicketStatistics(statistics *types.Statistics, authorIndex types.ValidatorIndex, tickets types.TicketsExtrinsic) {
	// Only update the number of tickets for the author of the block.
	statistics.ValsCurr[authorIndex].Tickets += types.U32(len(tickets))
}

// p: The number of preimages introduced by the validator.
func UpdatePreimageStatistics(statistics *types.Statistics, authorIndex types.ValidatorIndex, preimages types.PreimagesExtrinsic) {
	// Only update the number of preimages for the author of the block.
	statistics.ValsCurr[authorIndex].PreImages += types.U32(len(preimages))
}

// d: The total number of octets across all preimages introduced by the
// validator.
func UpdatePreimageOctetStatistics(statistics *types.Statistics, authorIndex types.ValidatorIndex, preimages types.PreimagesExtrinsic) {
	// Only update the number of preimage size for the author of the block.
	for _, preimage := range preimages {
		statistics.ValsCurr[authorIndex].PreImagesSize += types.U32(len(preimage.Blob))
	}
}
```

```go
// a: The number of availability assurances made by the validator.
func UpdateAvailabilityStatistics(statistics *types.Statistics, authorIndex types.ValidatorIndex, assurances types.AssurancesExtrinsic) {
	for _, assurance := range assurances {
		statistics.ValsCurr[assurance.ValidatorIndex].Assurances++
	}
}
```

Quiz angle: on epoch change π_L ← π_V and π_V resets to zeros **before** counting this block; blocks/tickets/preimages/preimage-size are attributed to the block **author** (H_i), assurances to the assurer, guarantees to every validator whose Ed25519 key is in the reporters set (`UpdateReportStatistics`, `statistics.go:60-100`, which recomputes G/G* per guarantee).

**3.9.2 Core statistics (13.8–13.10): DA load and popularity.** `statistics.go:160-202`

```go
// (13.8) p
func CalculatePopularity(coreIndex types.CoreIndex, assurancesExtrinsic types.AssurancesExtrinsic) types.U16 {
	output := types.U16(0)
	for _, assurance := range assurancesExtrinsic {
		output += types.U16(assurance.Bitfield[coreIndex])
	}

	return output
}

// (13.10) D
func CalculateDALoad(coreIndex types.CoreIndex, WMap CoreWorkReportMap) types.U32 {
	workReport, ok := WMap[coreIndex]
	if !ok {
		return 0
	}

	ceilValue := (types.U32(workReport.PackageSpec.ExportsCount)*65 + 63) / 64
	output := workReport.PackageSpec.Length + types.SegmentSize*ceilValue

	return output
}
```

Quiz angle: D = bundle length + W_G·⌈65·n/64⌉ (the 65/64 accounts for one paged-proof segment per 64 export segments); DA load is computed from **W** (newly available reports) while imports/exports/gas/bundle-size come from **w** (reports guaranteed in this block).

**3.9.3 Service statistics (13.12–13.16).** `statistics.go:333-455` — the service set is s_R (services in this block's reports) ∪ s_P (preimage requesters) ∪ K(S) (accumulated services); per service: provided count/size from E_P, refinement count/gas/imports/exports/extrinsics from the reports, accumulate count/gas from S. If the result is empty the map is set to `nil` so that it encodes identically to an empty dictionary.

### 3.10 Work packages and reports — guarantor side (GP §14)

**3.10.1 Package-level limits (14.4–14.7).** `internal/types/types.go:394-455` (`WorkPackage.Validate`): 1 ≤ items ≤ I=16; total of authorization + config + payloads + imports·W_F(4488) + extrinsic lengths ≤ W_B = 13,791,360; imports ≤ W_M = 3072; exports ≤ W_X = 3072; extrinsics ≤ T = 128; Σ refine gas ≤ G_R; Σ accumulate gas ≤ G_A.

**3.10.2 Per-item refine result mapping (14.11/14.13).** `internal/work_package/work_package.go:166-200`

```go
	refineOuput := pvm.RefineInvoke(refineInput)
	r := refineOuput.RefineOutput
	e := refineOuput.ExportSegment
	u := refineOuput.Gas
	z := len(o) + rSum
	if len(r)+z > types.WorkReportOutputBlobsMaximumSize {
		emptyExport := make([]types.ExportSegment, expectedCount)
		return types.WorkExecResult{Type: types.WorkExecResultReportOversize}, u, emptyExport
	} else if len(e) != int(workItem.ExportCount) {
		emptyExport := make([]types.ExportSegment, expectedCount)
		return types.WorkExecResult{Type: types.WorkExecResultBadExports}, u, emptyExport
	} else if refineOuput.WorkResult != types.WorkExecResultOk {
		emptyExport := make([]types.ExportSegment, expectedCount)
		return types.WorkExecResult{Type: refineOuput.WorkResult, Data: r}, u, emptyExport
	} else {
		return types.WorkExecResult{Type: refineOuput.WorkResult, Data: r}, u, e
	}
}
```

Quiz angle: the "output-oversize" (BIG) error is decided cumulatively against previous items' outputs + auth output; "bad-exports" when the number of exported segments ≠ declared `ExportCount`; the error-code encoding of `WorkExecResult` is `0=ok(+blob) 1=out-of-gas 2=panic 3=bad-exports 4=output-oversize 5=bad-code 6=code-oversize` (`encode.go:718-773`).

**3.10.3 Availability spec A (14.16) and paged proofs (14.10).** `work_package.go:230-247`, `334-367`

```go
// A (14.16)
func A(workPackageHash types.OpaqueHash, workPackgeBundle []byte, exportsData []types.ExportSegment) (types.WorkPackageSpec, error) {
	exports := make([]types.ByteSequence, 0, len(exportsData))
	for _, export := range exportsData {
		exports = append(exports, types.ByteSequence(export[:]))
	}
	exportsRoot := merkle_tree.M(exports, hash.Blake2bHash)
	erasureRoot, err := ComputeErasureRoot(workPackgeBundle, exportsData)
	if err != nil {
		return types.WorkPackageSpec{}, fmt.Errorf("failed to compute erasure root: %w", err)
	}
	return types.WorkPackageSpec{
		Hash:         types.WorkPackageHash(workPackageHash),
		Length:       types.U32(len(workPackgeBundle)),
		ErasureRoot:  types.ErasureRoot(erasureRoot),
		ExportsRoot:  types.ExportsRoot(exportsRoot),
		ExportsCount: types.U16(len(exportsData)),
	}, nil
}
```

```go
// (14.10)
func PagedProofs(exportSegments []types.ExportSegment) ([]types.ExportSegment, error) {
	byteSequences := make([]types.ByteSequence, len(exportSegments))
	for i, segment := range exportSegments {
		byteSequences[i] = types.ByteSequence(segment[:])
	}
	maxIndex := (len(exportSegments) + 63) / 64 // ceiling
	result := make([]types.ExportSegment, 0, maxIndex)
	for i := 0; i < maxIndex; i++ {
		j6 := merkle_tree.Jx(6, byteSequences, types.U32(i), hash.Blake2bHash)
		l6 := merkle_tree.Lx(6, byteSequences, types.U32(i), hash.Blake2bHash)
		...
		encoded, err := encoder.Encode(&types.SliceHash{
			A: j6,
			B: l6,
		})
		...
		padded := PadToMultiple(output, types.SegmentSize)
		result = append(result, types.ExportSegment(padded))
	}
	return result, nil
}

// (14.17)
func PadToMultiple(x []byte, n int) []byte {
	padLen := (n - (len(x) % n)) % n
	padding := make([]byte, padLen)
	return append(x, padding...)
}
```

Quiz angle: exports root uses the **constant-depth** Merkle function M; paged proofs are pages of 2^6 = 64 leaves with path J_6 and leaf page L_6, padded to W_G = 4104; the erasure root is M_B over (bundle-shard hash ⌢ segment-shard subtree root) pairs, 1023 of them (`mergeBCloudSCloud`, `work_package.go:307-314`).


### 3.11 PVM (GP Appendix A)

**3.11.1 Program blob deblob (A.2) and the bitmask/basic-block markers.** `PVM/program_code.go:18-45`, `78-140`

```go
// 0x01 bit stores whether an index is the start of a instruction
// 0x02 bit stores whether an index is the start of a basic block
type Bitmask []byte

func MakeBitMasks(instruction []byte, bitmaskData []byte) (Bitmask, ExitReason) {
	instSize := len(instruction)
	bitmaskSize := instSize / 8
	if instSize%8 > 0 {
		bitmaskSize++
	}

	if len(bitmaskData) != int(bitmaskSize) {
		pvmLogger.Errorf("bitmask has incorrect size: expected %d, got %d", bitmaskSize, len(bitmaskData))
		return nil, ExitPanic
	}

	bitmask := make(Bitmask, instSize)
	prev := 0
	for i := range instSize {
		if bitmaskData[i/8]&(1<<(i%8)) > 0 {
			bitmask[i] = 0x01

			if i == 0 || IsBlockTerminator(instruction[prev]) {
				bitmask[i] |= 0x02
			}

			prev = i
		}
	}

	return bitmask, ExitContinue
}
```

```go
// DeBlobProgramCode deblob code, jump table, bitmask | A.2
func DeBlobProgramCode(data []byte) (_ Program, _ ExitReason) {
	// E_(|j|) : size of jumpTable
	jumpTableSize, dataUsed, exitReason := ReadUintVariable(data)
	...
	// E_1(z) : length of jumpTableLength
	jumpTableLength, exitReason := decodeUintFixedLength(data, 1)
	...
	// E_(|c|) : size of instructions
	instSize, dataUsed, exitReason := ReadUintVariable(data)
	...
	if jumpTableLength*jumpTableSize >= 1<<32 {
		pvmLogger.Errorf("jump table size %d bits exceed litmit of 32 bits", jumpTableLength*jumpTableSize)
		return Program{}, ExitPanic
	}

	// E_z(j) = jumpTableSize * jumpTableLength = E_(|j|) * E_1(z)
	jumpTableData, data, err := ReadBytes(data, jumpTableLength*jumpTableSize)
	...
	instructions := data[:instSize]
	bitmaskData := data[instSize:]
	bitmask, exitReason := MakeBitMasks(instructions, bitmaskData)
	if exitReason == ExitPanic {
		// A.2 if bitmasks cannot fit instructions, return panic
		return Program{}, ExitPanic
	}
	...
	if exitReason := prog.preDecodeBlocks(); exitReason != ExitContinue {
		return Program{}, exitReason
	}

	return prog, ExitContinue
}
```

Quiz angle: blob layout `E(|j|) ⌢ E_1(z) ⌢ E(|c|) ⌢ E_z(j) ⌢ c ⌢ k`; a bitmask of the wrong size is a panic; a basic block starts at index 0 or right after a terminator (`opcodeInfoTable[...].IsTerminator`: trap, fallthrough, jump, jump_ind, load_imm_jump, branch_*, load_imm_jump_ind).

**3.11.2 skip (A.3).** `PVM/program_code.go:142-151`

```go
// skip computes the distance to the next opcode  A.3
func skip(pc int, bitmask Bitmask) uint32 {
	j := 1
	for ; pc+j < len(bitmask); j++ {
		if bitmask.IsStartOfInstruction(j + pc) {
			break
		}
	}
	return uint32(min(24, j-1))
}
```

Quiz angle: skip returns octets-minus-one to the next opcode, capped at 24; the next PC is `pc + 1 + skip(pc)`.

**3.11.3 Single-step transition ψ_1 with gas (A.6/A.7).** `PVM/invocation.go:20-68`

```go
// (v.0.7.1 A.6, A.7) SingleStepStateTransition
func (interp *Interpreter) SingleStepStateTransition(pc ProgramCounter) (ExitReason, ProgramCounter) {
	// check program-counter exceed blob length
	if int(pc) >= len(interp.Program.InstructionData) {
		return ExitPanic, pc
	}

	var exitReason ExitReason

	// (v0.7.1  A.19) check opcode validity
	opcodeData := interp.Program.InstructionData.isOpcode(pc)
	// (GP A.6) OOG when ρ < 1 (gas insufficient for next instruction)
	if interp.Gas < 1 {
		return ExitOOG, pc
	}
	interp.Gas -= 1

	target := execInstructions[opcodeData]
	if target == nil {
		pvmLogger.Errorf("instruction not implemented")
		return ExitPanic, pc
	}
	// (v0.7.1  A.20) l = skip(iota)
	skipLength := ProgramCounter(skip(int(pc), interp.Program.Bitmasks))

	exitReason, newPC := execInstructions[opcodeData](interp, pc, skipLength) // update PVM states

	reason := exitReason.GetReasonType()
	switch reason {
	case PANIC, HALT:
		return exitReason, 0
	case HOST_CALL: // host-call: newPC = pc
		return exitReason, newPC
	}

	if pc != newPC {
		// execute branch instruction
		return exitReason, newPC
	}

	// iota' = iota + 1 +skip(iota)
	newPC += skipLength + 1

	return exitReason, newPC
}
```

Quiz angle: every instruction costs 1 gas in 0.7.2 (`GasCost = InstrCount` per block in `preDecodeBlocks`); OOG is detected **before** executing when ρ < 1; an invalid opcode maps to opcode 0 (`isOpcode`) = `trap` → panic; PC past the end panics (GP: instructions are zero-padded, and 0 = trap).

**3.11.4 Exit reason encoding.** `PVM/exit_reason.go:9-34`

```go
const (
	CONTINUE ExitReasonType = iota
	HALT
	PANIC
	OUT_OF_GAS
	PAGE_FAULT
	HOST_CALL
)

// use mask to store the status and value
type ExitReason uint64

const (
	// GP do not define CONTINUE
	// if the actual result code defined in B.1 is needed
	// result =  (res >> 56) -1
	ExitContinue  = ExitReason(CONTINUE)         // 0x00
	ExitHalt      = ExitReason(HALT) << 56       // 0x01
	ExitPanic     = ExitReason(PANIC) << 56      // 0x02
	ExitOOG       = ExitReason(OUT_OF_GAS) << 56 // 0x03
	ExitPageFault = ExitReason(PAGE_FAULT) << 56 // 0x04000000XXXXXXXX
	ExitHostCall  = ExitReason(HOST_CALL) << 56  // 0x050000000000XXXX
)
```

**3.11.5 Branch (A.17) and dynamic jump (A.18).** `PVM/branch.go:3-57`

```go
func branch(pc ProgramCounter, b ProgramCounter, C bool, bitmask Bitmask, instruction ProgramCode) (ExitReason, ProgramCounter) {
	switch {
	case !C:
		return ExitContinue, pc
	case !bitmask.IsStartOfBasicBlock(b) && instruction.isOpcodeValid(b):
		return ExitPanic, pc
	default:
		return ExitContinue, b
	}
}

// ResolveDynamicJump resolves a jump-table address to a program PC.
func ResolveDynamicJump(a uint32, jumpTable JumpTable) (ExitReason, ProgramCounter) {
	switch {
	case a == 0xffff0000:
		return ExitHalt, 0
	case a == 0 || a > jumpTable.Size*ZA || a%ZA != 0:
		return ExitPanic, 0
	}
	index := a/ZA - 1
	dest, _, err := ReadUintFixed(jumpTable.Data[index*jumpTable.Length:], int(jumpTable.Length))
	if err != nil {
		panic(err.Error())
	}
	return ExitContinue, ProgramCounter(dest)
}

func DjumpResolve(pc ProgramCounter, a uint32, jumpTable JumpTable, bitmask Bitmask) (ExitReason, ProgramCounter) {
	if a == 0xffff0000 {
		return ExitHalt, pc
	}
	reason, newPC := ResolveDynamicJump(a, jumpTable)
	if reason != ExitContinue {
		if reason.GetReasonType() == PANIC {
			return ExitPanic, pc
		}
		return reason, newPC
	}
	if !bitmask.IsStartOfBasicBlock(newPC) {
		return ExitPanic, pc
	}
	return ExitContinue, newPC
}
```

Quiz angle: djump address `2^32 − 2^16 = 0xffff0000` halts; a == 0, a > |j|·Z_A, a mod Z_A ≠ 0 (Z_A = 2) or a target that is not a basic-block start → panic; the jump-table index is `a/Z_A − 1`. A taken branch to a non-block-start panics.

**3.11.6 Memory access rule (A.8): addresses below 2^16 panic, unmapped pages fault.** `PVM/decode.go:217-269` (and `loadFromMemory` 271-334)

```go
func storeIntoMemory(interp *Interpreter, offset int, memIndex uint32, immediate uint64) ExitReason {
	mem := interp.Memory
	if memIndex < uint32(1<<16) { // 0.7.2  A.8 check memory > 2^16
		return ExitPanic
	}

	pageNum := memIndex / ZP
	pageIndex := memIndex % ZP

	page, ok := mem.Pages[pageNum]
	if !ok {
		return ExitPageFault | ExitReason(memIndex)
	}
	if page.Access != MemoryReadWrite {
		return ExitPageFault | ExitReason(memIndex)
	}
	...
	// Fast path: entirely within current page.
	if pageIndex+uint32(offset) <= ZP {
		copy(page.Value[pageIndex:], src)
		interp.noteTraceMemAfterSuccessfulStore(memIndex, immediate)
		return ExitContinue
	}

	// Cross-page slow path.
	nextPage, ok := mem.Pages[pageNum+1]
	if !ok {
		return ExitPageFault | ExitReason(memIndex)
	}
	if nextPage.Access != MemoryReadWrite {
		return ExitPageFault | ExitReason(memIndex)
	}
	...
}
```

And the ordering rule for multiple bad addresses (A.9), `PVM/exit_reason.go:103-124`:

```go
// (A.9) ParseMemoryAccessError parses the memory access error based on the given
// invalid addresses.
func ParseMemoryAccessError(invalidAddresses []uint64) ExitReason {
	for i := range invalidAddresses {
		invalidAddresses[i] = invalidAddresses[i] % (1 << 32)
	}
	// Iterate over read addresses and check for errors.0
	if len(invalidAddresses) == 0 {
		return ExitContinue
	}

	minAddress := uint32(math.MaxUint32)
	for _, addr := range invalidAddresses {
		if addr < ZZ {
			return ExitPanic
		}
		if uint32(addr) < minAddress {
			minAddress = uint32(addr)
		}
	}
	return ExitPageFault | ExitReason(minAddress)
}
```

Quiz angle: page size Z_P = 4096, zone Z_Z = 2^16, page fault reports the **lowest** faulting address; any address in the first 64 KiB zone is a panic not a fault.

**3.11.7 Standard program initialization Y (A.36): memory layout and initial registers.** `PVM/single_initializer.go:13-81`

```go
func P(x int) uint32 {
	return ZP * ((uint32(x) + ZP - 1) / ZP)
}

func Z(x int) uint32 {
	return ZZ * ((uint32(x) + ZZ - 1) / ZZ)
}

// A.36 Y func
func SingleInitializer(p StandardCodeFormat, a Argument) (Instructions, Registers, Memory, ExitReason) {
	c, o, w, z, s, err := DecodeSerializedValues(p)
	if err != nil {
		return nil, Registers{}, Memory{}, ExitPanic
	}
	if 5*ZZ+uint64(Z(len(o)))+uint64(Z(len(w)+int(z)*int(ZP)+int(s)+ZI)) > 1<<32 {
		pvmLogger.Errorf("memory layout calculations failed")
		return nil, Registers{}, Memory{}, ExitPanic
	}

	// Memory layout calculations
	readOnlyStart := uint32(ZZ)
	readOnlyEnd := readOnlyStart + uint32(len(o))
	readOnlyPadding := readOnlyStart + P(len(o))
	readWriteStart := 2*ZZ + Z(len(o))
	readWriteEnd := readWriteStart + uint32(len(w))
	readWritePadding := readWriteStart + P(len(w)) + uint32(z)*ZP
	heapStart := readWritePadding
	// heapEnd := readWritePadding + ZP // ZP is according to davxy, traces-on-sbrk

	stackEnd := uint32(1<<32 - 2*ZZ - ZI)
	stackStart := stackEnd - P(int(s))
	argumentStart := uint32(1<<32 - ZZ - ZI)
	// argumentEnd := argumentStart + uint32(len(a))
	argumentEnd := argumentStart + uint32(len(a))
	argumentPadding := argumentEnd + P(len(a))

	mem := Memory{
		Pages:       make(map[uint32]*Page),
		heapPointer: uint64(heapStart),
		heapLimit:   uint64(stackStart),
	}

	allocateMemorySegment(&mem, readOnlyStart, readOnlyEnd, o, MemoryReadOnly)
	allocateMemorySegment(&mem, readOnlyEnd, readOnlyPadding, nil, MemoryReadOnly) // Padding
	...
	allocateMemorySegment(&mem, readWriteStart, readWriteEnd, w, MemoryReadWrite)
	allocateMemorySegment(&mem, readWriteEnd, readWritePadding, nil, MemoryReadWrite) // Padding
	...
	allocateStack(&mem, stackStart, stackEnd)
	...
	allocateMemorySegment(&mem, argumentStart, argumentEnd, a, MemoryReadOnly)
	allocateMemorySegment(&mem, argumentEnd, argumentPadding, nil, MemoryReadOnly) // Padding
	...
	// Registers initialization
	var regs Registers
	regs[0] = uint64(1<<32 - 1<<16)
	regs[1] = uint64(1<<32 - 2*ZZ - ZI)
	regs[7] = uint64(1<<32 - ZZ - ZI)
	regs[8] = uint64(len(a))

	return c, regs, mem, ExitContinue
}
```

Quiz angle: program header `E_3(|o|) E_3(|w|) E_2(z) E_3(s) o w E_4(|c|) c` (`DecodeSerializedValues`, lines 120-166); RO data at Z_Z, RW data at 2Z_Z + Q(|o|), heap of z extra pages after RW, stack ends at 2^32 − 2Z_Z − Z_I, arguments at 2^32 − Z_Z − Z_I; ω_0 (RA) = 2^32 − 2^16 (the halt address), ω_1 (SP) = stack end, ω_7/ω_8 = argument address/length. Note `argumentPadding := argumentEnd + P(len(a))` is a (harmless) over-allocation vs. `argumentStart + P(len(a))`.

**3.11.8 sbrk (opcode 101) semantics.** `PVM/instructions.go:800-830`

```go
// opcode 101
func instSbrk(interp *Interpreter, pc ProgramCounter, skipLength ProgramCounter) (ExitReason, ProgramCounter) {
	rD, rA, err := decodeTwoRegisters(interp.Program.InstructionData, pc)
	...
	// this reivision is according to jam-test-vector traces: Note on SBRK
	if interp.Registers[rA] == 0 {
		interp.Registers[rD] = interp.Memory.heapPointer
		return ExitContinue, pc
	}

	mem := interp.Memory
	newHeapPointer := mem.heapPointer + interp.Registers[rA]
	if newHeapPointer < mem.heapPointer || newHeapPointer > mem.heapLimit {
		interp.Registers[rD] = 0
		return ExitContinue, pc
	}

	nextPageBoundary := P(int(mem.heapPointer))
	if newHeapPointer > uint64(nextPageBoundary) {
		finalBoundary := P(int(newHeapPointer))
		allocateMemorySegment(mem, uint32(mem.heapPointer), uint32(finalBoundary), nil, MemoryReadWrite)
	}

	mem.heapPointer = newHeapPointer
	interp.Registers[rD] = newHeapPointer
	return ExitContinue, pc
}
```

Quiz angle: `sbrk 0` queries the heap pointer; growth beyond the stack start returns 0 (no fault); new pages are allocated writable up to the next page boundary. (GP 0.8.0 replaces sbrk-style growth with the `grow_heap` host call — not implemented here.)

**3.11.9 Division/remainder corner cases (A.5.13).** `PVM/instructions.go:1746-1791`, `1944-1994`

```go
// opcode 193
func instDivU32(interp *Interpreter, pc ProgramCounter, skipLength ProgramCounter) (ExitReason, ProgramCounter) {
	...
	bMod32 := uint32(interp.Registers[rB])
	aMod32 := uint32(interp.Registers[rA])

	if bMod32 == 0 {
		interp.Registers[rD] = ^uint64(0) // 2^64 - 1
	} else {
		interp.Registers[rD], err = SignExtend(4, uint64(aMod32/bMod32))
		...
	}

	return ExitContinue, pc
}

// opcode 194
func instDivS32(interp *Interpreter, pc ProgramCounter, skipLength ProgramCounter) (ExitReason, ProgramCounter) {
	...
	a := int64(int32(interp.Registers[rA]))
	b := int64(int32(interp.Registers[rB]))

	if b == 0 {
		interp.Registers[rD] = ^uint64(0) // 2^64 - 1
	} else if a == int64(-1<<31) && b == -1 {
		interp.Registers[rD] = uint64(a)
	} else {
		interp.Registers[rD] = uint64(a / b)
	}

	return ExitContinue, pc
}
```

```go
// opcode 206
func instRemS64(interp *Interpreter, pc ProgramCounter, skipLength ProgramCounter) (ExitReason, ProgramCounter) {
	...
	if int64(interp.Registers[rA]) == -(1<<63) && int64(interp.Registers[rB]) == -1 {
		interp.Registers[rD] = 0
	} else {
		interp.Registers[rD] = uint64(smod(int64(interp.Registers[rA]), int64(interp.Registers[rB])))
	}

	return ExitContinue, pc
}
```

with `smod` (`instructions.go:172-178`) returning `a` when `b == 0`. Quiz angle: division by zero → 2^64 − 1 (all ones), remainder by zero → dividend, signed MIN/−1 → MIN (division) and 0 (remainder); 32-bit results are sign-extended to 64 bits.

**3.11.10 Opcode categories (A.5) and the argument decoders.** `PVM/opcode_info.go:6-21`, `PVM/decode.go:151-165`

```go
const (
	InstrCatInvalid      InstrCategory = iota // not a valid opcode
	InstrCatNoArg                             // 0, 1
	InstrCatOneImm                            // 10
	InstrCatOneRegExtImm                      // 20
	InstrCatTwoImm                            // 30-33
	InstrCatOneOffset                         // 40
	InstrCatOneRegOneImm                      // 50-62
	InstrCatOneRegTwoImm                      // 70-73
	InstrCatOneRegImmOff                      // 80-90
	InstrCatTwoReg                            // 100-111
	InstrCatTwoRegOneImm                      // 120-161
	InstrCatTwoRegOneOff                      // 170-175
	InstrCatTwoRegTwoImm                      // 180
	InstrCatThreeReg                          // 190-230
)
```

```go
func decodeTwoRegistersAndOneImmediate(instructionCode []byte, pc ProgramCounter, skipLength ProgramCounter) (uint8, uint8, uint64, error) {
	rA := min(12, instructionCode[pc+1]&15)
	rB := min(12, instructionCode[pc+1]>>4)
	lX := min(4, max(0, skipLength-1))
	decodedVX, err := utils.DeserializeFixedLength(instructionCode[pc+2:pc+2+lX], types.U64(lX))
	...
	vX, err := SignExtend(uint8(lX), uint64(decodedVX))
	...
	return rA, rB, vX, nil
}
```

Quiz angle: register indices are the low/high nibble of the byte after the opcode, clamped to 12 (`min(12, …)`); immediates are little-endian, length `min(4, skip − 1)`, sign-extended (`SignExtend`, `signed_unsigned_transitions.go:110-130`); `load_imm_64` (opcode 20) is the only 8-byte immediate.

**3.11.11 Ψ_M dispatch and R (A.40/A.41).** `PVM/argument_invocation.go:42-91`

```go
// (A.40) Ψ_M
func Psi_M(
	code StandardCodeFormat,
	counter ProgramCounter, // program counter
	gas types.Gas, // gas counter
	argument Argument, // argument
	omegas Omegas, // jump table
	addition HostCallArgs, // host-call context
) (
	psi_result Psi_M_ReturnType,
) {
	// Recompiler when selected and linked; otherwise fall back to interpreter
	// (e.g. recompiler requested on a build that did not link it).
	if ExecutionBackend == BackendRecompiler && Psi_M_recompilerHook != nil {
		return Psi_M_recompilerHook(code, counter, gas, argument, omegas, addition)
	}
	if Psi_M_interpreterHook != nil {
		return Psi_M_interpreterHook(code, counter, gas, argument, omegas, addition)
	}
	panic("PVM.Psi_M: no execution backend registered (interpreter backend not linked)")
}

// (A.41) R
func R(priorGas types.Gas, Psi_H_Return Psi_H_ReturnType) (Gas, any, HostCallArgs) {
	u := priorGas - types.Gas(max(*Psi_H_Return.VM.Gas, 0))

	switch Psi_H_Return.ExitReason.GetReasonType() {
	case OUT_OF_GAS:
		return Gas(u), OUT_OF_GAS, Psi_H_Return.Addition
	case HALT:
		start := uint64(Psi_H_Return.VM.Registers[7])
		length := uint64(Psi_H_Return.VM.Registers[8])
		mem := Psi_H_Return.VM.Mem
		if mem.IsReadable(start, length) {
			if length == 0 {
				return Gas(u), nil, Psi_H_Return.Addition
			}
			return Gas(u), mem.Read(start, length), Psi_H_Return.Addition
		}
		return Gas(u), []byte{}, Psi_H_Return.Addition
	default:
		return Gas(u), PANIC, Psi_H_Return.Addition
	}
}
```

Quiz angle: gas used = prior − max(remaining, 0); on HALT the return blob is memory[ω_7 .. ω_7+ω_8) (empty if unreadable); a page fault at the top level is reported as PANIC.

**3.11.12 Recompiler: gas check emission (0.7.2 per-instruction vs 0.8.0 block-based).** `PVM/recompiler/gas.go:10-44`

```go
// Two inline instructions per PVM instruction (GP v0.7.2), fused charge+check:
//   - SubMemImm32: charge 1 gas
//   - Jcc(S): branch to the OOG landing pad when the result went negative
//
// (GP A.6) OOG when pre-charge Gas < 1. Gas is never negative at entry, so
// post-charge < 0 (SF=1) ⟺ pre-charge <= 0 ⟺ pre-charge < 1 — the same
// condition the interpreter checks, so a gas-exhausted program stops at the
// same instruction on both backends. The landing pad un-charges the 1 so the
// reported remaining gas also matches (the interpreter never charges on OOG).
func (c *Compiler) emitGasCheck(a *asm.Assembler, oog asm.Label) {
	a.SubMemImm32(RegGuestBase, -int32(OffsetGas), 1)
	a.Jcc(asm.CondS, oog)
}

// emitOutOfGasExit emits the temporary GP v0.7.2 per-instruction OOG landing pad.
// Each instruction gets its own exit label so ExitPC matches interpreter semantics.
func emitOutOfGasExit(a *asm.Assembler, oog asm.Label, instrPC PVM.ProgramCounter) {
	_ = a.BindLabel(oog)
	// Undo the fused charge: on OOG the interpreter leaves gas unchanged.
	a.SubMemImm32(RegGuestBase, -int32(OffsetGas), -1)
	// per-instruction (GP v0.7.2): report the exact instruction PC that failed.
	a.MovMemImm32_32(RegGuestBase, -int32(OffsetExitPC), int32(instrPC))
	a.MovImm64ToReg(RegScratch, uint64(PVM.ExitOOG))
	a.MovRegToMem(RegGuestBase, -int32(OffsetExitReason), RegScratch)
	a.Jmp(a.ExitTrampoline())
}
```

**3.11.13 Recompiler: register pinning and the block loop.** `PVM/recompiler/register_map.go:17-38`, `recompiler.go:50-115`

```go
var PVMToX86 = [PVMRegCount]asm.Register{
	/* RA = 0  */ asm.RAX,
	/* SP = 1  */ asm.RDX,
	/* T0 = 2  */ asm.RBX,
	/* T1 = 3  */ asm.RSI,
	/* T2 = 4  */ asm.RDI,
	/* S0 = 5  */ asm.R8,
	/* S1 = 6  */ asm.R9,
	/* A0 = 7  */ asm.R10,
	/* A1 = 8  */ asm.R11,
	/* A2 = 9  */ asm.R12,
	/* A3 = 10 */ asm.R13,
	/* A4 = 11 */ asm.R14,
	/* A5 = 12 */ asm.RBP,
}

// Reserved registers (not allocated to any PVM register):
const (
	RegGuestBase = asm.R15 // R15 = guest memory base; control region at [R15 - offset]
	RegScratch   = asm.RCX // scratch for DIV (needs CL), shifts, address calculation
	// RSP is the native stack pointer — implicitly reserved
)
```

```go
// BlockBasedInvoke runs one or more compiled basic blocks until the
// native side signals a non-CONTINUE exit.
func (r *Recompiler) BlockBasedInvoke(pc PVM.ProgramCounter) (PVM.ExitReason, PVM.ProgramCounter) {
	x86_signal_linux.SetupSignalHandler()
	runtime.LockOSThread()
	defer runtime.UnlockOSThread()
	...
	for {
		blockStartPC := pc
		block, err := r.lookupOrCompileBlock(pc)
		if err != nil {
			return PVM.ExitPanic, 0
		}

		r.ctx.WriteExitPC(pc)
		r.ctx.WriteExitReason(PVM.ExitContinue)
		...
		exitReason := executeBlockLocked(r.ctx, block)
		exitPC := r.ctx.ReadExitPC()

		if exitReason.GetReasonType() == PVM.HOST_CALL && exitReason.GetHostCallID() == DjumpCallID {
			exitReason, pc = r.resolveDjump(blockStartPC, uint32(exitPC))
			switch exitReason.GetReasonType() {
			case PVM.CONTINUE:
				continue
			case PVM.HALT, PVM.PANIC:
				return exitReason, djumpInstrPC(r.program, blockStartPC)
			default:
				return exitReason, 0
			}
		}

		if IsSbrkExit(exitReason) {
			instr, ok := r.sbrkInstrForRuntimeExit(exitPC)
			if !ok {
				return PVM.ExitPanic, 0
			}
			exitReason, pc = r.resolveSbrk(instr)
			...
		}

		switch exitReason.GetReasonType() {
		case PVM.CONTINUE:
			pc = exitPC
			continue
		case PVM.HALT, PVM.PANIC:
			return exitReason, r.ctx.ReadExitPC()
		case PVM.OUT_OF_GAS, PVM.PAGE_FAULT, PVM.HOST_CALL:
			return exitReason, exitPC
		default:
			return PVM.ExitPanic, 0
		}
	}
}
```

Quiz angle: why `LockOSThread` (signal handler restores into a specific goroutine stack), why the guest base lives in a register (all guest accesses are `[R15 + addr]` with hardware `PROT_NONE` faults instead of software bounds checks, except the `< Z_Z` check which is emitted in software: `emit_memory.go:10-15`), and how djump/sbrk/ecalli are "runtime exits" resolved by the same Go code the interpreter uses (`PVM.DjumpResolve`).

### 3.12 Host calls (GP Appendix B)

**3.12.1 Numbering and per-invocation tables.** `PVM/host_call_general.go:13-52`, `host_call_invocation.go:29-72`

```go
const (
	// ----------------- General Functions -----------------
	GasOp    OperationType = iota // gas = 0
	FetchOp                       // fetch = 1
	LookupOp                      // lookup = 2
	ReadOp                        // read = 3
	WriteOp                       // write = 4
	InfoOp                        // info = 5

	// ----------------- Refine Functions -----------------
	HistoricalLookupOp // historical_lookup = 6
	ExportOp           // export = 7
	MachineOp          // machine = 8
	PeekOp             // peek = 9
	PokeOp             // poke = 10
	PagesOp            // pages = 11
	InvokeOp           // invoke = 12
	ExpungeOp          // expunge = 13

	// ----------------- Accumulate Functions -----------------
	BlessOp      // bless = 14
	AssignOp     // assign = 15
	DesignateOp  // designate = 16
	CheckpointOp // checkpoint = 17
	NewOp        // new = 18
	UpgradeOp    // upgrade = 19
	TransferOp   // transfer = 20
	EjectOp      // eject = 21
	QueryOp      // query = 22
	SolicitOp    // solicit = 23
	ForgetOp     // forget = 24
	YieldOp      // yield = 25
	ProvideOp    // provide = 26
	LogOp        = OperationType(100)

	MaxOperationType OperationType = 100
)
```

```go
func init() {
	// is authorized host-call functions
	IsAuthorizedOmegas = make(Omegas, len(HostCallFunctions))
	IsAuthorizedOmegas[GasOp] = HostCallFunctions[GasOp]
	IsAuthorizedOmegas[FetchOp] = HostCallFunctions[FetchOp]
	IsAuthorizedOmegas[100] = logHostCall

	// accumulate host-call functions
	AccumulateOmegas = make(Omegas, len(HostCallFunctions))
	AccumulateOmegas[GasOp] = HostCallFunctions[GasOp]
	AccumulateOmegas[FetchOp] = HostCallFunctions[FetchOp]
	AccumulateOmegas[ReadOp] = readWrapWithG
	AccumulateOmegas[WriteOp] = writeWrapWithG
	AccumulateOmegas[LookupOp] = lookupWrapWithG
	AccumulateOmegas[InfoOp] = infoWrapWithG
	AccumulateOmegas[BlessOp] = HostCallFunctions[BlessOp]
	...
	AccumulateOmegas[ProvideOp] = HostCallFunctions[ProvideOp]
	AccumulateOmegas[100] = logHostCall

	// refine host-call functions
	RefineOmegas = make(Omegas, len(HostCallFunctions))
	RefineOmegas[GasOp] = HostCallFunctions[GasOp]
	RefineOmegas[FetchOp] = HostCallFunctions[FetchOp]
	RefineOmegas[HistoricalLookupOp] = HostCallFunctions[HistoricalLookupOp]
	RefineOmegas[ExportOp] = HostCallFunctions[ExportOp]
	RefineOmegas[MachineOp] = HostCallFunctions[MachineOp]
	RefineOmegas[PeekOp] = HostCallFunctions[PeekOp]
	RefineOmegas[PokeOp] = HostCallFunctions[PokeOp]
	RefineOmegas[PagesOp] = HostCallFunctions[PagesOp]
	RefineOmegas[InvokeOp] = HostCallFunctions[InvokeOp]
	RefineOmegas[ExpungeOp] = HostCallFunctions[ExpungeOp]
	RefineOmegas[100] = logHostCall
}
```

Quiz angle: is-authorized gets only gas/fetch(/log); refine has no read/write/lookup/info (only `historical_lookup`); in accumulate, read/write/lookup/info are wrapped with G (B.12) so that mutations of the current account are mirrored into the result context X. Unknown ids → `hostCallException` sets ω_7 = WHAT (after charging gas). `log` = 100 is JIP-1.

**3.12.2 Result constants and gas charging.** `PVM/pvm_types.go:54-75`, `host_call_general.go:177-224`

```go
// HostCallResultConstants
const (
	OK   uint64 = 0
	HUH  uint64 = ^uint64(8)
	LOW  uint64 = ^uint64(7)
	CASH uint64 = ^uint64(6)
	CORE uint64 = ^uint64(5)
	FULL uint64 = ^uint64(4)
	WHO  uint64 = ^uint64(3)
	OOB  uint64 = ^uint64(2)
	WHAT uint64 = ^uint64(1)
	NONE uint64 = ^uint64(0) // 2^64 - 1
)

// Inner PVM invocations called by Omega_k(invoke)
const (
	INNERHALT uint64 = iota
	INNERPANIC
	INNERFAULT
	INNERHOST
	INNEROOG
)
```

```go
func chargeGasAndCheck(input *OmegaInput) *OmegaOutput {
	*input.VM.Gas -= 10
	if *input.VM.Gas < 0 {
		return &OmegaOutput{
			ExitReason: ExitOOG,
			Addition:   input.Addition,
		}
	}
	return nil
}

// Gas Function（ΩG）, gas = 0
func gas(input OmegaInput) OmegaOutput {
	if result := chargeGasAndCheck(&input); result != nil {
		return *result
	}

	input.VM.Registers[7] = uint64(*input.VM.Gas)
	return OmegaOutput{
		ExitReason: ExitContinue,
		Addition:   input.Addition,
	}
}
```

Quiz angle: NONE = 2^64−1, WHAT = 2^64−2, OOB = 2^64−3, WHO = 2^64−4, FULL = 2^64−5, CORE = 2^64−6, CASH = 2^64−7, LOW = 2^64−8, HUH = 2^64−9; every host call charges a flat 10 gas first and returns OOG if that drives gas negative.

**3.12.3 fetch (Ω_Y) selectors.** `host_call_general.go:228-245`, `480-542`

```go
var fetchHandlers = [16]fetchHandler{
	0:  fetchConstants,
	1:  fetchEta,
	2:  fetchAuthOutput,
	3:  fetchExtrinsicAt,
	4:  fetchExtrinsicForWorkItem,
	5:  fetchImportSegmentAt,
	6:  fetchImportSegmentForWorkItem,
	7:  fetchWorkPackage,
	8:  fetchAuthorizerConfig,
	9:  fetchAuthorization,
	10: fetchWorkPackageContext,
	11: fetchWorkPackageItems,
	12: fetchWorkItemAt,
	13: fetchWorkItemPayload,
	14: fetchOperandOrDeferredTransfers,
	15: fetchOperandOrDeferredTransferAt,
}
```

```go
// fetch = 1
func fetch(input OmegaInput) (output OmegaOutput) {
	if result := chargeGasAndCheck(&input); result != nil {
		return *result
	}

	encoder := types.NewEncoder()
	idx := input.VM.Registers[10]
	var v *[]byte
	var val []byte
	var err error
	if idx < uint64(len(fetchHandlers)) {
		val, err = fetchHandlers[idx](input, encoder)
		if err == nil && val != nil {
			v = &val
		}
	}
	...
	o := input.VM.Registers[7]
	f := min(input.VM.Registers[8], dataLength)
	l := min(input.VM.Registers[9], dataLength-f)
	// nothing to write, don't need to check memory access
	if l == 0 && v != nil {
		input.VM.Registers[7] = dataLength
		return OmegaOutput{ExitReason: ExitContinue, Addition: input.Addition}
	}
	// need to first check writable
	if !input.VM.Mem.IsWriteable(o, l) && v != nil {
		input.VM.Registers[7] = OOB
		return OmegaOutput{ExitReason: ExitPanic, Addition: input.Addition}
	}

	// otherwise if v = nil
	if v == nil {
		input.VM.Registers[7] = NONE
		return OmegaOutput{ExitReason: ExitContinue, Addition: input.Addition}
	}
	input.VM.Mem.Write(o, (*v)[f:f+l])
	input.VM.Registers[7] = dataLength
	...
}
```

Quiz angle: selector in ω_10, secondary indices in ω_11/ω_12, output window (ω_7 offset, ω_8 skip f, ω_9 length l) — the "read into memory window, return full length" pattern shared with `lookup`, `read`, `info`, `historical_lookup`; selector 0 returns the encoded protocol constants (`getFetchConstantsData`, lines 1031-1075, in GP alphabetical order B_I…Y), 1 = η′_0 (accumulate only), 14/15 = accumulate inputs.

**3.12.4 write (Ω_W) with footprint/threshold check.** `host_call_general.go:722-812`

```go
	if vz == 0 { // remove storage
		delete(a.StorageDict, string(storageRawKey))
		removeStorageFromKeyVal(input.Addition.GeneralArgs.StorageKeyVal, serviceID, storageRawKey)

		// direct update items, octets
		a.ServiceInfo.Items -= footprintItems
		a.ServiceInfo.Bytes -= footprintOctets
	} else if input.VM.Mem.IsReadable(vo, vz) { // storage append/update
		storageRawData := input.VM.Mem.Read(vo, vz)

		// compute items, octets , check a_t > a_b first (GP: a_minbalance > a_balance → FULL, s' = s)
		newItems := a.ServiceInfo.Items - footprintItems
		newOctets := a.ServiceInfo.Bytes - footprintOctets

		storageItems, storageOctets := service_account.CalcStorageItemfootprint(string(storageRawKey), storageRawData)
		newItems += storageItems
		newOctets += storageOctets
		newMinBalance := service_account.CalcThresholdBalance(newItems, newOctets, a.ServiceInfo.DepositOffset) // a_t
		if newMinBalance > a.ServiceInfo.Balance {
			input.VM.Registers[7] = FULL
			return OmegaOutput{
				ExitReason: ExitContinue,
				Addition:   input.Addition,
			}
		}

		// balance check passed, now apply the storage mutation
		a.StorageDict[string(storageRawKey)] = storageRawData
		removeStorageFromKeyVal(input.Addition.GeneralArgs.StorageKeyVal, serviceID, storageRawKey)
		...
		a.ServiceInfo.Items = newItems
		a.ServiceInfo.Bytes = newOctets
	} else {
		return OmegaOutput{
			ExitReason: ExitPanic,
			Addition:   input.Addition,
		}
	}
	...
	input.VM.Registers[7] = l
```

Quiz angle: key = μ[ω_7..+ω_8], value = μ[ω_9..+ω_10]; ω_10 = 0 deletes; returns the **previous** length (NONE if absent); FULL when the new threshold balance would exceed the balance; unreadable value → panic.

**3.12.5 query (Ω_Q): encoding the four lookup states into ω_7/ω_8.** `host_call_accumulate.go:618-643`

```go
	lookupData, lookupDataExists := account.LookupDict[lookupKey]
	if lookupDataExists {
		// a = lookupData[h,z]
		switch len(lookupData) {
		case 0:
			input.VM.Registers[7], input.VM.Registers[8] = 0, 0
		case 1:
			input.VM.Registers[7] = 1 + uint64(1<<32)*uint64(lookupData[0])
			input.VM.Registers[8] = 0
		case 2:
			input.VM.Registers[7] = 2 + uint64(1<<32)*uint64(lookupData[0])
			input.VM.Registers[8] = uint64(lookupData[1])
		case 3:
			input.VM.Registers[7] = 3 + uint64(1<<32)*uint64(lookupData[0])
			input.VM.Registers[8] = uint64(lookupData[1]) + uint64(1<<32)*uint64(lookupData[2])
		}
	} else {
		// a = panic
		input.VM.Registers[7] = NONE
		input.VM.Registers[8] = 0
		...
	}
```

**3.12.6 solicit / forget (Ω_S / Ω_F): the a_l state machine with D = `UnreferencedPreimageTimeslots`.** `host_call_accumulate.go:665-701`, `793-834`

```go
func handleSolicitNewLookup(account *types.ServiceAccount, lookupKey types.LookupMetaMapkey, itemFootprintItems types.U32, itemFootprintOctets types.U64, registers *Registers) *OmegaOutput {
	newFootprintItems := account.ServiceInfo.Items + itemFootprintItems
	newFootprintOctets := account.ServiceInfo.Bytes + itemFootprintOctets
	newMinBalance := service_account.CalcThresholdBalance(newFootprintItems, newFootprintOctets, account.ServiceInfo.DepositOffset)
	if account.ServiceInfo.Balance < newMinBalance {
		registers[7] = FULL
		return &OmegaOutput{ExitReason: ExitContinue}
	}
	account.LookupDict[lookupKey] = make(types.TimeSlotSet, 0)
	account.ServiceInfo.Items = newFootprintItems
	account.ServiceInfo.Bytes = newFootprintOctets
	return nil
}

func handleSolicitExistingLookup(account *types.ServiceAccount, lookupKey types.LookupMetaMapkey, lookupData types.TimeSlotSet, itemFootprintItems types.U32, itemFootprintOctets types.U64, timeslot types.TimeSlot) *OmegaOutput {
	newFootprintItems := account.ServiceInfo.Items - itemFootprintItems
	newFootprintOctets := account.ServiceInfo.Bytes - itemFootprintOctets
	lookupData = append(lookupData, timeslot)
	newItemFootprintItems, newItemFootprintOctets := service_account.CalcLookupItemfootprint(lookupKey)
	account.LookupDict[lookupKey] = lookupData
	account.ServiceInfo.Items = newFootprintItems + newItemFootprintItems
	account.ServiceInfo.Bytes = newFootprintOctets + newItemFootprintOctets
	return nil
}

func processSolicitLookupData(account *types.ServiceAccount, lookupKey types.LookupMetaMapkey, lookupData types.TimeSlotSet, lookupDataExists bool, timeslot types.TimeSlot, registers *Registers) *OmegaOutput {
	itemFootprintItems, itemFootprintOctets := service_account.CalcLookupItemfootprint(lookupKey)

	if !lookupDataExists {
		return handleSolicitNewLookup(account, lookupKey, itemFootprintItems, itemFootprintOctets, registers)
	}
	if len(lookupData) == 2 {
		return handleSolicitExistingLookup(account, lookupKey, lookupData, itemFootprintItems, itemFootprintOctets, timeslot)
	}
	registers[7] = HUH
	return &OmegaOutput{ExitReason: ExitContinue}
}
```

```go
		if lookupData, lookupDataExists := a.LookupDict[lookupKey]; lookupDataExists {
			lookupDataLength := len(lookupData)
			itemFootprintItems, itemFootprintOctets := service_account.CalcLookupItemfootprint(lookupKey)

			newFootprintItems := a.ServiceInfo.Items
			newFootprintOctets := a.ServiceInfo.Bytes
			if lookupDataLength == 0 || (lookupDataLength == 2 && int(lookupData[1]) < int(timeslot)-int(types.UnreferencedPreimageTimeslots)) {
				// delete (h,z) from a_l
				expectedRemoveLookupKey := types.LookupMetaMapkey{Hash: types.OpaqueHash(h), Length: types.U32(z)}
				delete(a.LookupDict, expectedRemoveLookupKey) // if key not exist, delete do nothing
				// delete (h) from a_p
				delete(a.PreimageLookup, types.OpaqueHash(h))
				newFootprintItems -= itemFootprintItems
				newFootprintOctets -= itemFootprintOctets
			} else if lookupDataLength == 1 {
				newFootprintItems -= itemFootprintItems
				newFootprintOctets -= itemFootprintOctets
				// a_l[h,z] = [x,t]
				lookupData = append(lookupData, timeslot)
				a.LookupDict[lookupKey] = lookupData
				...
			} else if lookupDataLength == 3 && int(lookupData[1]) < int(timeslot)-int(types.UnreferencedPreimageTimeslots) {
				newFootprintItems -= itemFootprintItems
				newFootprintOctets -= itemFootprintOctets
				// a_l[h,z] = [w,t]
				lookupData[0] = lookupData[2]
				lookupData[1] = timeslot
				lookupData = lookupData[:2]
				a.LookupDict[lookupKey] = lookupData
				...
			} else { // otherwise, panic
				input.VM.Registers[7] = HUH
				...
			}
```

Quiz angle: `solicit` creates `[]` (paying the footprint, FULL if unaffordable) or turns `[x,y]` into `[x,y,t]`; `forget` deletes `[]` immediately, `[x]` → `[x,t]`, `[x,y]` with y < t − D → delete entry and preimage, `[x,y,z]` with y < t − D → `[z,t]`; anything else HUH. D = 32 (tiny) / 19,200 (full: `LookupAnchorMaxAge + 4800`).

**3.12.7 new (Ω_N): registrar path vs. public index.** `host_call_accumulate.go:249-370` — ω_7..ω_12 = (o, l, g, m, f, i); code hash c = μ[o..+32]; if f ≠ 0 the caller must be the manager (HUH); the new account gets a_l = {(c,l) ↦ []}, balance a_t of its own footprint, `CreationSlot = τ′`, `ParentService = caller`; caller pays a_t and must stay above its own threshold (CASH); when the caller is the registrar and i < S = 2^16, index i is used (FULL if taken), otherwise the pre-derived `ImportServiceID` (x_i) is used and x_i is advanced with `check(S + (x_i − S + 42) mod ...)`.

**3.12.8 transfer (Ω_T) and eject (Ω_J).** `host_call_accumulate.go:413-487`, `489-575` — transfer: WHO if destination missing, LOW if gas limit l < destination's a_m, CASH if the sender would drop below a_t, otherwise queue a `DeferredTransfer{Sender, Receiver, Balance, Memo(128 bytes), GasLimit}`, debit the sender, and **charge l gas from the caller** (OOG if insufficient); eject: destination must not be self, its code hash must equal E_32(caller index) (i.e. `SerializeFixedLength(callerID, 32)`), it must have exactly 2 items and a lookup entry `(h, max(81, a_o) − 81)` whose slot-set is `[x, y]` with y < τ′ − D; then its balance is credited to the caller and it is deleted.

**3.12.9 Refine host calls: export, machine, invoke.** `host_call_refine.go:73-113`, `115-164`, `343-458`

```go
// export = 7
func export(input OmegaInput) (output OmegaOutput) {
	if result := chargeGasAndCheck(&input); result != nil {
		return *result
	}

	p := input.VM.Registers[7]
	z := min(input.VM.Registers[8], types.SegmentSize)

	if !input.VM.Mem.IsReadable(p, z) { // not readable, return
		input.VM.Registers[7] = OOB
		return OmegaOutput{ExitReason: ExitPanic, Addition: input.Addition}
	}

	segmentLength := uint64(input.Addition.ExportSegmentOffset) + uint64(len(input.Addition.ExportSegment))
	// otherwise if ζ + |e| >= W_X
	if segmentLength > types.MaxExportCount {
		input.VM.Registers[7] = FULL
		return OmegaOutput{ExitReason: ExitContinue, Addition: input.Addition}
	}

	// data = mu_p...+z
	data := input.VM.Mem.Read(p, z)
	x := zeroPadding(data, types.SegmentSize)
	exportSegment := types.ExportSegment{}
	copy(exportSegment[:], x)

	input.VM.Registers[7] = segmentLength
	input.Addition.ExportSegment = append(input.Addition.ExportSegment, exportSegment)
	...
}
```

```go
	tmpProgram := Program{
		InstructionData: input.Addition.IntegratedPVMMap[n].ProgramCode,
	}
	tempMemory := input.Addition.IntegratedPVMMap[n].Memory
	// wrap m[n]_p (program), w (registers), m[n]_u (memory), g (gas)
	tempInterp := NewInterpreter(&tmpProgram, w, &tempMemory, Gas(g))

	var c ExitReason
	var pcPrime ProgramCounter

	c, pcPrime = tempInterp.SingleStepInvoke(input.Addition.IntegratedPVMMap[n].PC)

	// mu* = mu
	encoder := types.NewEncoder()
	data = types.ByteSequence(make([]byte, offset))
	encoded, _ := encoder.Encode(&tempInterp.Gas) // encode g'
	copy(data, encoded)
	for i := uint64(1); i < offset/8; i++ {
		encoded, _ := encoder.Encode(&tempInterp.Registers[i-1])
		copy(data[8*i:8*(i+1)], encoded)
	}
	// write data into memory (mu)
	input.VM.Mem.Write(o, data)
	...
	switch c.GetReasonType() {
	case HOST_CALL:
		input.VM.Registers[7] = INNERHOST
		input.VM.Registers[8] = uint64(c.GetHostCallID())

	case PAGE_FAULT:
		input.VM.Registers[7] = INNERFAULT
		input.VM.Registers[8] = uint64(c.GetPageFaultAddress())

	case OUT_OF_GAS:
		input.VM.Registers[7] = INNEROOG

	case PANIC:
		input.VM.Registers[7] = INNERPANIC

	case HALT:
		input.VM.Registers[7] = INNERHALT

	}
```

Quiz angle: `export` zero-pads to W_G = 4104 and returns the segment's global index (offset ζ + local count), FULL at W_X = 3072; `machine` assigns the lowest unused id n and deblobs the program (HUH on bad blob); `pages` (`host_call_refine.go:272-341`) rejects r > 4, p < 16, p+c ≥ 2^32/Z_P (= 2^20 pages) with HUH and, for r > 2, requires the pages to be already accessible; then r = 1/3 → read-only, r = 2/4 → read-write, always allocating fresh zeroed pages (so this implementation zeroes even for r = 3/4 and does nothing for r = 0, whereas the GP keeps contents for r ≥ 3 and voids for r = 0 — a divergence worth a "what does the code do vs. the spec" question; this path is not covered by the STF conformance vectors); `invoke` reads 112 bytes (gas + 13 registers as E_8) from ω_8, runs the inner PVM with **no host calls** (an `ecalli` returns INNERHOST + id), writes back gas/registers, and stores the resumption PC (past the ecalli when the exit was a host call); `expunge` returns the saved PC and deletes the machine.


### 3.13 Serialization codec (GP Appendix C)

**3.13.1 Variable-length natural encoding E (C.6) and fixed-length E_l (C.5).** `internal/types/encoder.go:87-138`

```go
// EncodeUintWithLength
func (e *Encoder) EncodeUintWithLength(value uint64, l int) ([]byte, error) {
	if l == 0 {
		return []byte{}, nil
	}

	out := make([]byte, l)
	for i := 0; i < l; i++ {
		out[i] = byte(value & 0xFF)
		value >>= 8
	}

	return out, nil
}

// EncodeUint
func (e *Encoder) EncodeUint(value uint64) ([]byte, error) {
	// If x = 0: E(x) = [0]
	if value == 0 {
		return []byte{0}, nil
	}

	if value < 0x80 {
		return []byte{byte(value)}, nil
	}

	if value >= (uint64(1) << 56) {
		remainderBytes, err := e.EncodeUintWithLength(value, 8)
		if err != nil {
			return nil, err
		}
		return append([]byte{0xFF}, remainderBytes...), nil
	}

	k := bits.Len64(value) - 1
	l := k / 7
	l64 := uint(l)

	power8l := uint64(1) << (8 * l64)
	remainder := value % power8l
	floor := value / power8l

	// prefix = 2^8 - 2^(8-l) + floor(x / 2^(8*l))
	prefix := byte((256 - (1 << (8 - l64))) + floor)

	remainderBytes, err := e.EncodeUintWithLength(remainder, int(l))
	if err != nil {
		return nil, err
	}

	return append([]byte{prefix}, remainderBytes...), nil
}
```

And the decoder (`internal/types/decoder.go:90-117`):

```go
func (d *Decoder) DecodeUint(data []byte) (uint64, error) {
	if len(data) < 1 {
		return 0, errors.New("no data to deserialize U64")
	}
	prefix := data[0]

	// If x < 0x80: E(x) = [x]
	if prefix < 0x80 {
		return uint64(prefix), nil
	}

	// If prefix = 0xFF: E(x) = [255] || E_8(x)
	if prefix == 0xFF {
		if len(data) < 9 {
			return 0, errors.New("not enough data for 8-byte U64")
		}
		return binary.LittleEndian.Uint64(data[1:9]), nil
	}

	l := bits.LeadingZeros8(^prefix)
	needed := l + 1
	...
	base := 0xFF - (uint8(1) << (8 - uint(l))) + 1
	floorVal := uint64(prefix - base)
```

Quiz angle: l = ⌊log2(x)/7⌋ = number of trailing bytes; the prefix's top l bits are 1, followed by a 0, followed by the high bits of x; x ≥ 2^56 uses `0xFF` + 8 LE bytes; values < 128 are a single byte. Sequences are length-prefixed with this same encoding (`EncodeLength`), fixed-size integers in structs use E_l little-endian (`U16.Encode`, `U32.Encode`, `U64.Encode`).

**3.13.2 Where compact (C.6) vs fixed encodings are used inside structs.** `internal/types/encode.go:846-880`, `775-806`

```go
// WorkReport (C.27)
func (w *WorkReport) Encode(e *Encoder) error {
	...
	// Work report core index is compact
	// https://github.com/davxy/jam-test-vectors/commit/fed98559dabaa7058d7f9d83cb8c9353bd78d544
	// CoreIndex (c)
	if err := e.EncodeLength(uint64(w.CoreIndex)); err != nil {
		return err
	}

	// AuthorizerHash (a)
	if err := w.AuthorizerHash.Encode(e); err != nil {
		return err
	}

	// AuthGasUsed (g)
	// INFO: This field is encoded as C.6 integer
	if err := e.EncodeInteger(uint64(w.AuthGasUsed)); err != nil {
		return err
	}
```

Quiz angle: inside a work report the core index and the auth gas used are **compact** (C.6) while `WorkResult.AccumulateGas` and the `RefineLoad` fields are also compact ("This struct use C.6 integer encoding"); statistics records π_C/π_S use compact integers too (`encode.go:1467`, `1530`), but validator records π_V/π_L use fixed E_4 (see GP C(13): `E_4(v)`).

**3.13.3 Option / discriminated union encodings.** `encode.go:1804-1854` (`TicketsOrKeys`: prefix byte 0 = tickets, 1 = keys — the discriminator of γ_s in C(4)), `encode.go:718-773` (`WorkExecResult`: 0 ok+blob … 6 code-oversize), `encode.go:341-380` (header `EpochMark`/`TicketsMark` nil → `0`, else `1` + body), `encode.go:1904-1930` (MMR peaks: `0` for ∅, `1` + hash).

**3.13.4 Dictionaries are encoded sorted by key.** `encode.go:2459-2500` (`Storage`: keys sorted bytewise, each key is length-prefixed — "we follow the jamtestnet pattern: they put the length of the key before the key", `decode.go:2838-2841`), `encode.go:2520-2557` (`PreimagesMapEntry` sorted by hash), `encode.go:2331-2366` (`AlwaysAccumulateMap` sorted by service id, value = gas as U64).

**3.13.5 Legacy compact codec.** `pkg/codecs/scale/types/compact.go:61-114` — the same C.6 rule written with an explicit search for l such that 2^(7l) ≤ x < 2^(7(l+1)) (kept for the `internal/input/jam_types` legacy types; not on the STF path).

### 3.14 State merklization (GP Appendix D)

**3.14.1 State-key constructors C(i), C(i,s), C(s,h) (D.1).** `internal/utilities/merklization/state_key_constructor.go:37-76`

```go
// D.1 State-Key-Construction
func (s StateWrapper) StateKeyConstruct() (output types.StateKey) {
	// [i, 0, 0,...]
	output[0] = byte(s.StateIndex)
	return output
}

func (w StateServiceWrapper) StateKeyConstruct() (output types.StateKey) {
	// [i, n_0, 0, n_1, 0, n2, 0, n3, 0, 0,...] where n = encode_4(service_id)
	output[0] = byte(w.StateIndex)

	// Encode the service index
	n := encodeServiceID(w.ServiceIndex)

	for i := 0; i <= 3; i++ {
		output[2*i+1] = n[i]
	}
	return output
}

// StateKeyConstruct returns a OpaqueHash
func (w ServiceWrapper) StateKeyConstruct() (output types.StateKey) {
	// [n_0, h_0, n_1, h_1, n_2, h_2, n_3, h_3, h_4, h_5,...,h_26] where n = encode_4(service_id)

	// Encode the service index
	n := encodeServiceID(w.ServiceIndex)

	a := hash.Blake2bHashPartial(w.h[:], 27)

	for i := 0; i <= 3; i++ {
		output[2*i] = n[i]
		output[2*i+1] = a[i]
	}

	for i := 4; i <= 26; i++ {
		output[i+4] = a[i]
	}

	return output
}
```

Quiz angle: keys are 31 bytes (`type StateKey [31]byte`); C(255, s) is the service-info key (`encodeDelta1KeyVal`, `state_serialize.go:353-360`); the third form interleaves the 4 service-id bytes with the first 4 bytes of Blake2b(h) and appends h-hash bytes 4..26.

**3.14.2 Service sub-keys: storage, preimages, lookups.** `state_serialize.go:362-442`

```go
var (
	delta2Prefix = types.ByteSequence{0xFF, 0xFF, 0xFF, 0xFF}
	delta3Prefix = types.ByteSequence{0xFE, 0xFF, 0xFF, 0xFF}
)
...
func encodeDelta2KeyVal(id types.ServiceID, key types.ByteSequence, value types.ByteSequence) (stateKeyVal types.StateKeyVal) {
	h := make(types.ByteSequence, delta2PrefixLen+len(key))
	copy(h[:delta2PrefixLen], delta2Prefix)
	copy(h[delta2PrefixLen:], key)

	serviceWrapper := ServiceWrapper{ServiceIndex: id, h: h}
	stateKeyVal = types.StateKeyVal{
		Key:   serviceWrapper.StateKeyConstruct(),
		Value: value,
	}

	return stateKeyVal
}

func encodeDelta3KeyVal(id types.ServiceID, key types.OpaqueHash, value types.ByteSequence) (stateKeyVal types.StateKeyVal) {
	h := make(types.ByteSequence, delta3PrefixLen+len(key))
	copy(h[:delta3PrefixLen], delta3Prefix)
	copy(h[delta3PrefixLen:], key[:])
	...
}

func EncodeDelta4KeyVal(id types.ServiceID, key types.LookupMetaMapkey, value types.TimeSlotSet) (stateKeyVal types.StateKeyVal) {
	h := make(types.ByteSequence, uint32EncodedLen+len(key.Hash))
	v := uint32(key.Length)
	h[0] = byte(v)
	h[1] = byte(v >> 8)
	h[2] = byte(v >> 16)
	h[3] = byte(v >> 24)
	copy(h[uint32EncodedLen:], key.Hash[:])

	serviceWrapper := ServiceWrapper{ServiceIndex: id, h: h}

	stateValue := types.ByteSequence{}
	for _, timeSlot := range value {
		stateValue = append(stateValue, utilities.SerializeFixedLength(types.U64(timeSlot), 4)...)
	}
	stateValue = append(utilities.SerializeU64(types.U64(len(value))), stateValue...)
	...
}
```

Quiz angle: storage key h = E_4(2^32−1) ⌢ k, preimage key h = E_4(2^32−2) ⌢ hash, lookup key h = E_4(length) ⌢ hash with value = E(↕[E_4(t)…]); why a length of 2^32−1 or 2^32−2 cannot collide with a real lookup length (preimages are < 4 GiB). `IsPreimage` (`parse_state_key_vals.go:48-67`) recognises a preimage key-val by recomputing C(s, E_4(2^32−2) ⌢ Blake2b(value)).

**3.14.3 Trie node encoding and Merklization (D.2).** `internal/utilities/merklization/merklization.go:8-34`, `42-73`

```go
// encodeBranchNode encodes a branch node as [64]byte with zero heap allocation.
// Layout: {left[0] & 0x7F, left[1:32], right[0:32]}
func encodeBranchNode(left, right types.OpaqueHash) [64]byte {
	var node [64]byte
	node[0] = left[0] & 0x7F
	copy(node[1:32], left[1:])
	copy(node[32:], right[:])
	return node
}

// encodeLeafNode encodes a leaf node as [64]byte with zero heap allocation.
// Embedded leaf (value <= 32 bytes): {0x80 | len(value), key[:31], value, zero-padding}
// Regular leaf (value > 32 bytes):   {0xC0, key[:31], blake2b(value)}
func encodeLeafNode(key types.StateKey, value []byte) [64]byte {
	var node [64]byte
	if len(value) <= 32 {
		node[0] = 0x80 | byte(len(value))
		copy(node[1:32], key[:])
		copy(node[32:], value)
	} else {
		node[0] = 0xC0
		copy(node[1:32], key[:])
		h := hash.Blake2bHash(value)
		copy(node[32:], h[:])
	}
	return node
}
```

```go
// partitionByBit partitions entries in-place based on the bit at position depth.
// Returns pivot index: entries[:pivot] have bit=0 (left), entries[pivot:] have bit=1 (right).
func partitionByBit(entries []types.StateKeyVal, depth int) int {
	byteIdx := depth / 8
	bitMask := byte(1 << (7 - depth%8))
	left := 0
	for right := range entries {
		if entries[right].Key[byteIdx]&bitMask == 0 {
			entries[left], entries[right] = entries[right], entries[left]
			left++
		}
	}
	return left
}

// merklize computes the Merkle root hash using in-place partition and [64]byte encoding.
func merklize(entries []types.StateKeyVal, depth int) types.OpaqueHash {
	if len(entries) == 0 {
		return types.OpaqueHash{}
	}
	if len(entries) == 1 {
		node := encodeLeafNode(entries[0].Key, entries[0].Value)
		return hash.Blake2bHash(node[:])
	}

	pivot := partitionByBit(entries, depth)
	leftHash := merklize(entries[:pivot], depth+1)
	rightHash := merklize(entries[pivot:], depth+1)

	node := encodeBranchNode(leftHash, rightHash)
	return hash.Blake2bHash(node[:])
}
```

Quiz angle: first bit 0 = branch (left hash loses its top bit), `10xxxxxx` = embedded leaf with 6-bit length ≤ 32, `11000000` = regular leaf storing Blake2b(value); an empty (sub)trie is the zero hash; bits are consumed MSB-first from the key. The key-level cache (`blockchain/key_level_cache.go`) memoizes leaf hashes by (key, Blake2b(value)) and is cleared every `MaxKeyLevelCacheSize = E·50` entries.

**3.14.4 The state serializer T(σ) (D.2) and ordering.** `state_serialize.go:444-608` — keys 1..16 are α, φ, β, γ, ψ, η, ι, κ, λ, ρ, τ, χ, π, ϑ, ξ, θ; δ entries are produced in parallel per service (service info, storage, preimages, lookups) and the whole list is sorted by key before merklization. The `ServiceInfo.Version` byte (`ServiceInfoVersion = 0`) is forced before encoding (`encodeDelta1`, line 274).

### 3.15 General Merklization (GP Appendix E)

**3.15.1 Binary Merkle N / M_B / M (E.1).** `internal/utilities/merkle_tree/merkle_tree.go:19-57`, `134-202`

```go
// N: Calculates the Merkle root from integers.
func N(v []types.ByteSequence, hashFunc func(types.ByteSequence) types.OpaqueHash) types.ByteSequence {
	// [[]] should result zero hash
	if len(v) == 0 || v[0] == nil {
		// H0 - return zero hash as bytes
		return types.ByteSequence(zeroHash[:])
	} else if len(v) == 1 {
		// Single element: return raw data
		return v[0]
	} else {
		mid := (len(v) + 1) / 2
		left := v[:mid]
		right := v[mid:]
		// $node + N(left) + N(right)
		a := N(left, hashFunc)
		b := N(right, hashFunc)

		merge := make([]byte, 0, len(nodePrefix)+len(a)+len(b))
		merge = append(merge, nodePrefix...)
		merge = append(merge, a...)
		merge = append(merge, b...)

		// Return hash as ByteSequence
		hash := hashFunc(merge)
		return types.ByteSequence(hash[:])
	}
}

// Mb: Well-balanced binary Merkle function
func Mb(v []types.ByteSequence, hashFunc func(types.ByteSequence) types.OpaqueHash) types.OpaqueHash {
	// [[]] should go to N
	if len(v) == 1 && v[0] != nil {
		return hashFunc(v[0])
	} else {
		// N returns ByteSequence, convert to OpaqueHash
		return types.OpaqueHash(N(v, hashFunc))
	}
}
```

```go
// C: Pads a slice with zero hashes to the nearest power of 2.
func C(v []types.ByteSequence, hashFunc func(types.ByteSequence) types.OpaqueHash) []types.OpaqueHash {
	sz := 1
	for sz < len(v) {
		sz *= 2
	}
	ret := make([]types.OpaqueHash, sz)
	var merge types.ByteSequence
	for i := 0; i < sz; i++ {
		if i < len(v) {
			// Reset merge buffer and append "leaf" prefix + value
			merge = merge[:0]
			merge = append(merge, leafPrefix...)
			merge = append(merge, v[i]...)
			ret[i] = hashFunc(merge)
		} else {
			// constant for zero hash
			ret[i] = zeroHash
		}
	}
	return ret
}
...
// M: Constant-depth binary Merkle function
func M(v []types.ByteSequence, hashFunc func(types.ByteSequence) types.OpaqueHash) types.OpaqueHash {
	C_res := C(v, hashFunc)

	// Pre-allocate with exact size to avoid reallocation
	seq := make([]types.ByteSequence, len(C_res))
	for i, hash := range C_res {
		// Direct slice conversion
		seq[i] = types.ByteSequence(hash[:])
	}

	// N returns ByteSequence, convert to OpaqueHash
	nResult := N(seq, hashFunc)
	var hash types.OpaqueHash
	copy(hash[:], nResult)
	return hash
}
```

Quiz angle: N splits at ⌈n/2⌉ and hashes `"node" ⌢ left ⌢ right`; M_B hashes a singleton directly; M first hashes each leaf as `"leaf" ⌢ v` and pads to the next power of two with zero hashes (constant depth), which is what exports roots and paged proofs (J_x/L_x with x = 6) use. The MMR functions (E.2) are in §3.3.2 above.

### 3.16 Shuffle (GP Appendix F)

`internal/utilities/shuffle/shuffle.go:35-103`

```go
// numericSequenceFromHash generates a numeric sequence from a hash.
// The function defined in graypaper F.2 $\mathcal{Q}_l$
func numericSequenceFromHash(hash types.OpaqueHash, length types.U32) []types.U32 {
	const serializeLength = 4

	numericSequence := make([]types.U32, length)

	for i := types.U32(0); i < length; i++ {
		floor := i / 8

		// Serialize the floor value
		serializeOutput := SerializeFixedLength(types.U64(floor), serializeLength)

		// Concatenate the hash with the serialized output
		hashOutput := hashUtil.Blake2bHash(types.ByteSequence(append(hash[:], serializeOutput...)))

		// Select a slice of 4 bytes from the hashOutput
		selectRange := types.U32(4)
		startIndex := types.U32((4 * i) % 32)
		hashOutputSlice := hashOutput[startIndex : startIndex+selectRange]

		// Deserialize the hashOutputSlice
		numericValue := types.U32(DeserializeFixedLength(types.ByteSequence(hashOutputSlice)))
		numericSequence[i] = numericValue
	}

	return numericSequence
}

// FisherYatesShuffle is a recursive implementation of the Fisher-Yates shuffle
// algorithm.
func FisherYatesShuffle(s []types.U32, r []types.U32) []types.U32 {
	l := len(s)

	// If the sequence is empty, return an empty slice
	if l == 0 {
		return make([]types.U32, 0)
	}

	// Calculate the index
	index := r[0] % types.U32(l)

	// The selected element
	selected := s[index]

	// Swap elements
	s[index], s[l-1] = s[l-1], s[index]

	// Recursively shuffle the remaining elements
	shuffledRest := FisherYatesShuffle(s[:l-1], r[1:])

	// Return the shaffled sequence
	return append([]types.U32{selected}, shuffledRest...)
}
```

Quiz angle: Q_l(h)[i] = decode_4(Blake2b(h ⌢ E_4(⌊i/8⌋))[4(i mod 8) .. +4]) — one hash yields 8 numbers; the shuffle picks index `r[i] mod remaining`, emits it, and moves the **last** element into the hole (F.1). Used only for guarantor core assignment (11.20) in this codebase (auditing uses its own VRF-based selection).

### 3.17 Erasure coding (GP Appendix H)

**3.17.1 Rust side (rate 342:1023 over GF(2^16), 2-byte symbols).** `pkg/erasure_coding/reed-solomon-ffi/src/lib.rs:7-90`

```rust
#[no_mangle]
pub extern "C" fn rs_encode(
    data_ptr: *const u8,
    data_len: usize,
    data_shard: usize,
    parity_shard: usize,
    out_ptr: *mut *mut u8,
    out_len: *mut usize,
) -> i32 {
    let w_e = data_shard * 2;

    // Load input data
    let mut data = unsafe { slice::from_raw_parts(data_ptr, data_len).to_vec() };

    // Padding to multiple of w_e
    if data.len() % w_e != 0 {
        let pad_len = w_e - (data.len() % w_e);
        data.extend(std::iter::repeat(0).take(pad_len));
    }

    let shard_size = data.len() / data_shard;
    let total_shards = data_shard + parity_shard;

    let mut chunks: Vec<Vec<u16>> = Vec::with_capacity(shard_size / 2);
    for i in 0..shard_size / 2 {
        let mut encoder = match ReedSolomonEncoder::new(data_shard, parity_shard, 2) {
            Ok(enc) => enc,
            Err(_) => return 1,
        };

        // Add data shards
        for j in 0..data_shard {
            let shard = u16::from_le_bytes([
                data[j * shard_size + i * 2],
                data[j * shard_size + i * 2 + 1],
            ]);
            if encoder.add_original_shard(&shard.to_le_bytes()).is_err() {
                return 2;
            }
        }

        // Encode parity shards
        let encoded = match encoder.encode() {
            Ok(e) => e,
            Err(_) => return 3,
        };
        ...
    }

    // Flatten in shard-major order
    ...
}
```

**3.17.2 Go side and the constants.** `pkg/erasure_coding/erasure_coding.go:16-39`, `internal/types/const.go:185-190`

```go
func EncodeDataShards(data []byte, dataShard, parityShard int) ([][]byte, error) {
	// Call FFI for flattened shards
	flat, err := EncodeData(data, dataShard, parityShard)
	if err != nil {
		return nil, err
	}

	numShards := dataShard + parityShard
	shardSize := len(flat) / numShards
	if len(flat)%numShards != 0 {
		return nil, fmt.Errorf("unexpected output size %d is not divisible by %d shards", len(flat), numShards)
	}

	// Slice to shards [][]byte
	shards := make([][]byte, numShards)
	for i := 0; i < numShards; i++ {
		start := i * shardSize
		end := start + shardSize
		shardCopy := make([]byte, shardSize)
		copy(shardCopy, flat[start:end])
		shards[i] = shardCopy
	}
	return shards, nil
}
```

```go
// erasure coding constants
// 342:1023 (Appendix H)
const (
	DataShards  = 342
	TotalShards = 1023
)
```

Quiz angle: W_E (`ECBasicSize`) = 684 = 342·2 octets per "piece" in full, 4 = 2·2 in tiny (2 data shards of 6); a 4104-byte segment splits into W_P = 6 pieces (full) or 1026 (tiny); any 342 of the 1023 shards reconstruct (`DecodeShards` takes shard indices). Note `DataShards`/`TotalShards` are **compile-time constants** (full values) even in tiny mode; only `ECBasicSize`/`ECPiecesPerSegment` switch — so `work_package.go` always encodes 342:1023 (the tiny EC test vectors in `pkg/erasure_coding/tiny_test` exercise 2:6 explicitly).

### 3.18 Bandersnatch / ring VRF glue (GP Appendix G)

`internal/safrole/safrole.go:63-101` builds the ring root O(k) from the 32-byte Bandersnatch keys of γ′_k through `vrf.NewVerifier(ringBytes, ringSize).GetCommitment()` (144-byte `BandersnatchRingCommitment`); `internal/keystore/jip5_key_derivation.go:26-69` derives keys per JIP-5; IETF VRF contexts are the constants in `internal/types/const.go:129-139`:

```go
	// JAM protocol identifiers
	JamEntropy      = "jam_entropy"       // XE
	JamFallbackSeal = "jam_fallback_seal" // XF
	JamTicketSeal   = "jam_ticket_seal"   // XT
	JamValid        = "jam_valid"
	JamInvalid      = "jam_invalid"
	JamAvailable    = "jam_available"
	JamBeefy        = "jam_beefy"
	JamGuarantee    = "jam_guarantee"
	JamAnnounce     = "jam_announce" // XI
	JamAudit        = "jam_audit"    // XU
```

Quiz angle: which context string is used where — ticket ring proofs and ticket seals use X_T, fallback seals X_F, H_v uses X_E, judgments X_valid/X_invalid, guarantees/culprits X_G, assurances X_A, audits X_U/X_I.


---

## 4. Constants and configuration values (tiny vs full)

Source of truth: `internal/types/const.go` (`SetTinyMode` lines 29-48, `SetFullMode` lines 50-69, permanent constants lines 111-190), `PVM/const.go:6-11`, `config/config.go:66-84` (defaults for `--mode custom`), `internal/chainspec` + `types.ApplyProtocolParameters` (chainspec override of the mode-dependent set).

### 4.1 Mode-dependent (variables, overwritten by chainspec `protocol_parameters`)

| Go variable | GP symbol | tiny | full | Notes |
|---|---|---|---|---|
| `ValidatorsCount` | V | 6 | 1023 | |
| `CoresCount` | C | 2 | 341 | |
| `EpochLength` | E | 12 | 600 | also sizes ϑ, ξ, γ_s, ticket accumulator cap |
| `SlotSubmissionEnd` | Y | 10 | 500 | "contest_duration" / epoch tail start |
| `RotationPeriod` | R | 4 | 10 | guarantor rotation |
| `MaxTicketsPerBlock` | K | 3 | 16 | |
| `TicketsPerValidator` | N | 3 | 2 | ticket attempt bound (`VerifyTicketsAttempt`) |
| `ValidatorsSuperMajority` | ⌊2V/3⌋+1 | 5 | 683 | verdict "good" count, availability threshold |
| `AvailBitfieldBytes` | ⌈C/8⌉ | 1 | 43 | encoded size of an assurance bitfield |
| `UnreferencedPreimageTimeslots` | D | 32 | 19,200 (= `LookupAnchorMaxAge + 4800`) | preimage expunge period used by `forget`/`eject` |
| `TotalGas` | G_T | 20,000,000 | 3,500,000,000 | block accumulation gas ceiling |
| `MaxRefineGas` | G_R | 1,000,000,000 | 5,000,000,000 | |
| `ECPiecesPerSegment` | W_P | 1026 | 6 | pieces per 4104-byte segment |
| `ECBasicSize` | W_E | 4 | 684 | erasure piece size (= 2 · data shards) |
| `MaxLookupAge` | L | 24 | 14,400 | lookup-anchor age bound (11.34) |
| `MaxKeyLevelCacheSize` | — | E·50 = 600 | E·50 = 30,000 | merklization leaf cache bound |

### 4.2 Permanent constants (`const` in Go; chainspec must match or `ApplyProtocolParameters` errors)

| Go constant | GP symbol | Value | Where used |
|---|---|---|---|
| `AdditionalMinBalancePerItem` | B_I | 10 | `CalcThresholdBalance` |
| `AdditionalMinBalancePerOctet` | B_L | 1 | `CalcThresholdBalance` |
| `BasicMinBalance` | B_S | 100 | `CalcThresholdBalance` |
| `SlotPeriod` | P | 6 (s) | timing only |
| `MaxBlocksHistory` | H | 8 | `AddItem2BetaHPrime` |
| `AuthPoolMaxSize` | O | 8 | `STFAlpha2AlphaPrime` |
| `AuthQueueSize` | Q | 80 | `AuthQueue.Validate`, `assign` reads 32·Q bytes |
| `TranchePeriod` | A | 8 (s) | auditing |
| `MaximumWorkItems` | I | 16 | `WorkReport.Validate`, `WorkPackage.Validate` |
| `MaximumDependencyItems` | J | 8 | `ValidateLookupDictAndPrerequisites` |
| `WorkReportTimeout` | U | 5 | `FilterAvailableReports` |
| `WorkReportOutputBlobsMaximumSize` | W_R | 48·1024 | `ValidateOutputSize`, `I` in work_package |
| `MaxTotalSize` | W_B | 13,791,360 | `WorkPackage.Validate` |
| `SegmentFootprint` | W_F | 4488 (= W_G + 32·⌈log2 W_M⌉) | `WorkPackage.Validate` |
| `MaxAccumulateGas` | G_A | 10,000,000 | report gas ceiling, `calculateMaxGasUsed` |
| `IsAuthorizedGas` | G_I | 50,000,000 | `Psi_I` |
| `MaxImportCount` | W_M | 3072 | |
| `MaxExportCount` | W_X | 3072 | `export` host call FULL |
| `MaxExtrinsics` | T | 128 | |
| `MaxServiceCodeSize` | W_C | 4,000,000 | `Psi_A`, `RefineInvoke` (BIG) |
| `MaxIsAuthorizedCodeSize` | W_A | 64,000 | `Psi_I` (BIG) |
| `AccumulateQueueSize` | S (queue) | 1024 | unused constant ("v0.6.6") |
| `SegmentSize` | W_G | 4104 | `export`, paged proofs, `CalculateDALoad` |
| `TransferMemoSize` | W_T | 128 | `DeferredTransfer.Memo` |
| `LookupAnchorMaxAge` | L (full) | 14,400 | seed for D in full mode |
| `MinimumServiceIndex` | S | 65,536 (2^16) | `check`, `new` registrar path |
| `DataShards` / `TotalShards` | H: 342 / 1023 | 342 / 1023 | erasure coding (always full ratio) |
| `BiasFactor` | (17.16) | 2 | auditing |
| `GuaranteeMinCount` / `GuaranteeMaxCount` | 2 / 3 | | guarantee signatures |
| `HashSize`, `Ed25519SigSize`, `BandersnatchSigSize` | 32 / 64 / 96 | | ring VRF signature is 784 bytes (`BandersnatchRingVrfSignature`), ring commitment 144, BLS key 144, metadata 128 |
| `ServiceInfoVersion` | — | 0 | leading byte of the encoded service info (GP 0.7.1) |
| `JamCommonEra` | — | 2025-01-01 12:00 UTC | slot ↔ wall-clock |
| PVM `ZA` / `ZI` / `ZP` / `ZZ` | Z_A / Z_I / Z_P / Z_Z | 2 / 2^24 / 2^12 / 2^16 | `PVM/const.go` |
| host-call base gas | (B.x) | 10 | `chargeGasAndCheck` |
| accumulate entry PC | — | 5 | `Psi_A` → `Psi_M(..., 5, ...)`; refine and is-authorized start at 0 |

Fuzz-only: `fuzzenv.FuzzPersistentRetainBlocks = 24`; `ringVerifierCacheMax = 32`.

---

## 5. Notable engineering decisions and gotchas

1. **GP version drift, host-call numbering.** The code implements the 0.7.2 numbering (`gas=0 fetch=1 lookup=2 read=3 write=4 info=5 historical_lookup=6 export=7 machine=8 peek=9 poke=10 pages=11 invoke=12 expunge=13 bless=14 … provide=26, log=100`). GP 0.8.0 inserts `grow_heap = 1` and shifts everything after it by one (`fetch=2 … provide=27`); the repo has no `grow_heap` yet. Good trap question: "what is `ecalli 12` in this code?" (invoke) vs GP 0.8.0 (pages).

2. **Gas model.** 0.7.2 semantics: 1 gas per instruction, checked *before* execution (`SingleStepStateTransition`, `SingleStepInvokeDecodedBlocks`), 10 gas per host call, plus `transfer` charging the transfer's gas limit. `BlockMeta.GasCost = InstrCount` carries a `TODO(gas-model)` and the recompiler has `emitBlockGasCheck`/`emitBlockOutOfGasExit` prepared for 0.8.0 block-based charging but commented out (`compiler.go:382-410`).

3. **Two-level ordering trick for header validation.** Non-VRF header checks run before any state transition; VRF checks (seal, entropy, epoch mark) run *after* Safrole so they can use κ′, η′_3 and γ′_s — the GP defines these against posterior values. `ValidateHeaderEntropy`'s parameter is misleadingly named `priorState` but receives the posterior.

4. **Prior state is mutated through slice aliasing.** Prior-state getters return the underlying slices (`prior_state.go:87-91`, `199-203`, `241-245`), so `History2HistoryDagger` (patches β[last].StateRoot), `ReplaceOffenderKeys(priorState.GetIota())` (zeroes offender keys) and `ClearWorkReports` (nils ρ[c]) all write into the prior state. `FilterAvailableReports` (§3.7.2) silently *relies* on this: it guards with `rho[coreIndex] == nil` (prior ρ) but dereferences `rhoDagger[coreIndex]`; both are the same backing array, so a disputes-cleared core is skipped instead of crashing.

5. **"Unmatched key-vals" for fuzzer state restoration.** Because storage/lookup keys are hashed in the state key, a `SetState` cannot always be lifted back into `ServiceAccount` maps; leftovers are carried as raw key-vals through the STF, consulted by `read`/`write`/`query`/`solicit`/`forget`/`provide` and by `ShouldIntegratePreimage`, and appended before merklizing. `ParallelizedAccumulation` merges per-service copies of this pool by **intersection** (`accumulation.go:543-583`), and `read` only caches/removes an entry when a service reads its **own** storage ("ΩR must be side-effect free" for cross-service reads, `host_call_general.go:680-690`).

6. **Ticket-count bound checks V instead of K.** `VerifyEpochTail` (`extrinsic_tickets.go:29-33`) rejects `len(E_T) > ValidatorsCount` while the comment says `|E_T| ≤ K`; the K bound is only enforced by `TicketsExtrinsic.Validate` at decode time. Tiny: K=3, V=6.

7. **ξ slots are sorted.** `updateXi` sorts each slot's hashes with a "WONDER: this sort is not mentioned in the graypaper" comment — ξ ∈ ⟦{H}⟧ is a sequence of *sets*, and the JSON/binary test vectors serialize sets sorted, so the sort is needed for byte-exact state roots.

8. **sbrk behaviour follows test-vector traces, not only the GP.** `instSbrk` returns the heap pointer for `sbrk 0`, returns 0 when growth would exceed the stack start, and allocates pages lazily; comments cite "jam-test-vector traces: Note on SBRK" and "davxy, traces-on-sbrk" (`instructions.go:808`, `single_initializer.go:40`).

9. **Work-report `CoreIndex` is compact-encoded** (and `AuthGasUsed`, `AccumulateGas`, `RefineLoad`, π_C/π_S fields) after a davxy test-vector change (`encode.go:858-861`); `Storage` map keys are length-prefixed "to follow the jamtestnet pattern" (`decode.go:2838-2841`).

10. **Two β′ implementations.** `STFBetaHDagger2BetaHPrime` (production/traces: computes θ′ root, appends to the MMR, uses H(H) of *this* header) vs `STFBetaHDagger2BetaHPrime_ForTestVector` (per-subsystem "history" vectors where `Header.Parent` is actually the header hash and the MMR commitment is given). `stf/update_history.go` and `update_preimages.go` exist only for the per-subsystem vectors.

11. **Disputes use posterior ψ′_o when validating culprits/faults but prior ψ_o for "already reported".** `VerifyCulpritSignature` removes posterior offenders from the valid key set; `ExcludeOffenders` compares against prior ψ_o. Faults' report-hash validity is checked against posterior ψ′_g/ψ′_b (after this block's verdicts are merged).

12. **Guarantor "reporters" statistics recompute G/G*** with a `nil` offenders map (`statistics.go:69-70`; reading a nil Go map is legal), i.e. the statistics step trusts `ValidateSignatures` to have already rejected banned guarantors and does not re-check ψ′_o itself.

13. **Recompiler safety net.** JIT only compiles for `linux && amd64 && cgo`; `Psi_M` silently falls back to the interpreter otherwise. Nested `invoke` PVMs always run on the interpreter, single-stepped, without host calls (`host_call_refine.go:392-405`). The signal handler must run on a locked OS thread; executable memory is dual-mapped (RW + RX views of one memfd) so no `mprotect` flips are needed; `< 2^16` addresses get a software check while everything else is hardware-faulted.

14. **Ring verifier cache keyed by key-set hash, never `Free()`d.** `blockchain/ring_verifier.go:41-51` explains that entries handed out under a read lock may still be in use, so eviction only drops the Go reference and lets the finalizer reclaim the Rust object.

15. **Deferred transfers vs. 0.7.1.** `deferred_transfers.go:122` notes "v0.7.1 has removed deferred transfers & Ψ_T"; transfers are delivered as accumulate inputs (`OperandOrDeferredTransfer`) of the next ∆+ round, balance credited before Ψ_A runs, and `ParallelizedAccumulation` filters out transfers whose sender or receiver no longer exists (`accumulation.go:687-700`).

16. **Guarantor-side `C` (14.8) field mapping looks scrambled.** `work_package.go:205-228` sets `ExtrinsicCount: item.ExportCount`, `ExtrinsicSize: types.U32(len(item.Extrinsic))` and `Exports: zSum` (sum of extrinsic lengths) — versus the GP's (x = |w_x|, z = Σ len, e = w_e). This path is not exercised by the STF conformance vectors (which supply reports ready-made), which is presumably why it went unnoticed. Likewise the refine `pages` host call zeroes pages for r = 3/4 and ignores r = 0 (§3.12.9). The `argumentPadding := argumentEnd + P(len(a))` over-allocation in `SingleInitializer` (§3.11.7) is harmless.

17. **Timeslot-monotonicity and future-slot checks.** `BadSlot` (τ ≥ τ′) is raised inside Safrole, not in header validation; `FutureReportSlot`/`ReportEpochBeforeLast` are raised in `ValidateSignatures`; the lookup-anchor age violation returns `ReportEpochBeforeLast` rather than a dedicated code (`guarantee_controller.go:287-292`).

18. **Fuzz protocol classification.** Any `*types.ErrorCode` returned by the STF is a *protocol* error (block rejected, node continues); any other `error` is a *runtime* error (bug). Error-code → message maps mirror the fuzz-proto example strings (e.g. `VrfSealInvalid` → `"BadSealSignature"`, `CoreUnauthorized` → `"code unauthorized"`).

19. **Statistics run concurrently.** π_V, π_C, π_S are computed in three goroutines (`statistics.go:487-503`); accumulation and state serialization are parallelized with `errgroup` bounded by `MaxWorkers = 2·NumCPU`; single-service accumulation is deduplicated with `singleflight`.

20. **Version markers in comments** are the fastest way to date a rule: "GP 0.6.7 formula 4.6/7.x" (recent history), "v0.6.4 (12.20)" (gas), "v0.7.0 (12.39, 12.40)" (preimages), "v0.7.1 (13.12–13.16)" (service stats), "0.7.2 A.8" (memory ≥ 2^16 panic), "GP 0.8.0 eq 6.13" (ring root), "TODO(gas-model)" (0.8.0). `VERSION_GP` = 0.7.2 but `config.DefaultConfig().Info.JamVersion` still says "0.7.1" (overridden at build via `UpdateVersion`).

---

## 6. Quick index of "which function implements equation X"

| GP eq. | Function |
|---|---|
| 4.6 / 7.5 β† | `recent_history.History2HistoryDagger` |
| 4.7 / 7.6–7.8 β′ | `recent_history.STFBetaHDagger2BetaHPrime` |
| 5.x H_x | `utilities.CreateExtrinsicHash` (+ `g` for E_G) |
| 6.2 | `safrole.R` |
| 6.13 / 6.14 | `safrole.KeyRotate` / `safrole.ReplaceOffenderKeys` |
| 6.15 / 6.16 / 6.17 | `safrole.ValidateByTickets` / `ValidateByBandersnatchs` / `ValidateHeaderEntropy` |
| 6.22 / 6.23 | `safrole.UpdateEtaPrime0` / `UpdateEntropy` |
| 6.24 / 6.25 / 6.26 | `safrole.UpdateSlotKeySequence` / `OutsideInSequencer` / `FallbackKeySequence` |
| 6.27 / 6.28 | `safrole.CreateEpochMarker` / `CreateWinningTickets` (+ `ValidateHeaderEpochMark`/`ValidateHeaderTicketsMark`) |
| 6.30–6.34 | `safrole.VerifyEpochTail`, `VerifyTicketsProof`, `VerifyTicketsOrder`, `VerifyTicketsDuplicate`, `CreateNewTicketAccumulator` |
| 8.2 / 8.3 | `authorization.STFAlpha2AlphaPrime` / `AuthPool.RemoveLeftMostPairedValue` |
| 9.4 / 9.6 / 9.7 / 9.8 | `service_account.FetchCodeByHash` / `ValidatePreimageLookupDict` / `HistoricalLookup` / `GetServiceAccountDerivatives` |
| 10.3–10.4 | `VerdictWrapper.VerifySignature` |
| 10.7–10.10 | `VerdictController.CheckSortUnique`, `CulpritController.CheckSortUnique`, `FaultController.CheckSortUnique`, `SetDisjoint` |
| 10.11–10.12 | `GenerateVerdictSumSequence`, `CompareVerdictsWithPsi` |
| 10.13 / 10.14 | `DisputeController.ValidateFaults` / `ValidateCulprits` |
| 10.15 | `VerdictController.ClearWorkReports` |
| 10.16–10.19 | `UpdatePsiG/B/W`, `UpdatePsiO` |
| 10.20 | `DisputeController.HeaderOffenders` |
| 11.11–11.15 | `AvailAssuranceController.ValidateAnchor`, `CheckValidatorIndex`, `SortUnique`, `ValidateSignature`, `ValidateBitField` |
| 11.16 / 11.17 | `UpdateNewlyAvailableWorkReports` / `FilterAvailableReports` |
| 11.19–11.22 | `rotateCores`, `permute`, `GFunc`, `GStarFunc` |
| 11.23–11.26 | `GuaranteeController.Validate`, `Sort`, `ValidateSignatures` |
| 11.29–11.30 | `ValidateWorkReports` |
| 11.32–11.35 | `CardinalityCheck`, `ValidateContexts` |
| 11.36–11.41 | `ValidateWorkPackageHashes`, `CheckExtrinsicOrRecentHistory`, `CheckSegmentRootLookup` |
| 11.42 / 11.43 | `CheckWorkResult` / `TransitionWorkReport` |
| 12.2 / 12.4 / 12.5 / 12.6 / 12.7 / 12.8 / 12.9 | `GetAccumulatedHashes`, `UpdateImmediatelyAccumulateWorkReports`, `UpdateQueuedWorkReports`, `GetDependencyFromWorkReport`, `QueueEditingFunction`, `AccumulationPriorityQueue`, `ExtractWorkReportHashes` |
| 12.10–12.12 | `UpdateAccumulatableWorkReports` |
| 12.16 / 12.17 / 12.20 | `OuterAccumulation` / `ParallelizedAccumulation` / `SingleServiceAccumulation` (+ `R`) |
| 12.18 | `accumulation.Provide` |
| 12.20 gas / 12.21–12.22 | `calculateMaxGasUsed` / `executeOuterAccumulation`, `updatePartialStateSetToPosteriorState` |
| 12.26 θ′ | `executeOuterAccumulation` (sorted `LastAccOut`) |
| 12.28–12.29 | `calculateAccumulationStatistics`, `updateDeltaDoubleDagger` |
| 12.31–12.33 | `updateXi`, `updateVartheta` |
| 12.36 / 12.39–12.43 | `ShouldIntegratePreimage` / `ValidatePreimageExtrinsics`, `ProcessPreimageExtrinsics` |
| 13.3–13.5 | `UpdateValidatorActivityStatistics`, `UpdateCurrentStatistics` |
| 13.6–13.10 | `UpdateCoreActivityStatistics`, `CalculateWorkResults`, `CalculateDALoad`, `CalculatePopularity` |
| 13.12–13.16 | `UpdateServiceActivityStatistics`, `GetAllServices`, `CalculateServiceResults` |
| 14.4–14.7 | `WorkPackage.Validate` |
| 14.8 / 14.9 / 14.10 / 14.11 / 14.16 / 14.17 | `work_package.C` / `VerifyAuthorization` / `PagedProofs` / `WorkReportCompute` / `A` / `PadToMultiple` |
| A.2 / A.3 | `DeBlobProgramCode` / `skip` |
| A.6–A.7 | `Interpreter.SingleStepStateTransition` |
| A.8 / A.9 | `storeIntoMemory`/`loadFromMemory` / `ParseMemoryAccessError` |
| A.12–A.16 | `UnsignedToBits`, `BitsToUnsigned`, `ReverseUnsignedToBits`, `ReverseBitsToUnsigned`, `SignExtend` |
| A.17 / A.18 | `branch` / `DjumpResolve` |
| A.36 | `SingleInitializer` |
| A.40 / A.41 | `Psi_M` / `R` |
| B.7 / B.8 / B.10 / B.12 / B.13 / B.14 | `ResultContext` / `Psi_A` / `I` / `G` / `C` / `check` |
| C.5 / C.6 | `Encoder.EncodeUintWithLength` / `Encoder.EncodeUint` |
| D.1 / D.2 | `StateWrapper.StateKeyConstruct` etc. / `merklize` + `StateEncoder` |
| E.1 | `merkle_tree.N`, `Mb`, `M`, `T`, `Lx`, `Jx` |
| E.2 (E.8–E.10) | `mmr.Replace`, `mmr.P`/`AppendOne`, `SuperPeak` |
| F.1–F.3 | `FisherYatesShuffle`, `numericSequenceFromHash`, `Shuffle` |
| H | `erasurecoding.EncodeDataShards`/`DecodeShards`, `work_package.ComputeErasureRoot` |
