#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Assign each item 2–3 tags from a fixed vocabulary of GP terms (plus delta-0.8.0 if present).
Usage: python3 scripts/retag.py [--dry]   — rewrites "tags": [...] in items/*.py in place.
Greek-letter patterns are matched case-sensitively (ψ ≠ Ψ, ξ ≠ Ξ); ASCII patterns ignore case."""
import sys, importlib, pkgutil, re, io, collections, os
os.chdir(os.path.join(os.path.dirname(__file__), '..')); sys.path.insert(0, '.')
VOCAB = [
 ('accumulate', r'accumulat|Δ\+|Δ\*|Δ1|operand tuple|R\*'),
 ('refine', r'\brefin|Ψ_R'),
 ('guarantee', r'guarant|\bρ'),
 ('assurance', r'assur|\bavailab'),
 ('audit', r'\baudit'),
 ('dispute', r'disput|verdict|judg|culprit|(?<!page )\bfaults?\b|offender|\bψ'),
 ('ticket', r'ticket|γ_A|γ′_A'),
 ('seal', r'\bseal|H_S'),
 ('Safrole', r'safrole|γ_S|γ′_S|sealer'),
 ('fallback', r'fallback'),
 ('entropy', r'entropy|\bη'),
 ('epoch', r'\bepoch'),
 ('timeslot', r'timeslot|common era|(?<!value )\bslots?\b|H_T|\bτ'),
 ('validator set', r'validator[- ]set|\bκ|\bι\b|\bλ|γ_P|γ′_P|staging|pending set'),
 ('ring VRF', r'ring[- ]?vrf|ring root|ring proof|γ_Z|γ′_Z'),
 ('Bandersnatch', r'bandersnatch|\bvrf\b|H_V'),
 ('Ed25519', r'ed25519'),
 ('BEEFY', r'beefy|\bbls\b'),
 ('GRANDPA', r'grandpa|finalit|finaliz|best chain|best block'),
 ('header', r'\bheader|H_P|H_R|H_X|H_I|H_E|H_W|H_O|marker'),
 ('extrinsic', r'extrinsic|E_T|E_A|E_D|E_G|E_P'),
 ('state root', r'state[- ]root|M_σ'),
 ('recent history', r'recent history|\bβ'),
 ('MMR', r'\bmmr\b|mountain|\bbelt|super-?peak'),
 ('preimage', r'preimage|\blookup\b|a_l\b|a_p\b|solicit|\bforget|historical'),
 ('storage', r'\bstorage|a_s\b'),
 ('balance', r'\bbalance\b|threshold|a_t\b|a_b\b'),
 ('privileges', r'privileg|\bχ|manager|delegator|registrar|assigner|\bbless|designate|\bassign\b'),
 ('transfer', r'transfer|\bmemo\b'),
 ('checkpoint', r'checkpoint'),
 ('yield', r'\byield|\bθ'),
 ('gas', r'\bgas|G_A|G_T|G_R|out-of-gas'),
 ('PVM', r'\bpvm|risc|instruction|opcode|\bregisters?\b|\bΨ\b|Ψ_M|Ψ_H|interpreter|recompiler'),
 ('host call', r'host[- ]?call|host function|ecalli|\bΩ_|\bfetch\b|grow_heap|sbrk|\binvoke\b'),
 ('basic block', r'basic[- ]block'),
 ('memory', r'\bmemory|\bpages?\b|\bram\b|heap'),
 ('segment', r'segment|D³L'),
 ('erasure coding', r'erasure|shard|chunk|reed'),
 ('lookup-anchor', r'lookup[- ]anchor|\banchor'),
 ('statistics', r'statistic|\bπ'),
 ('ready queue', r'ready queue|\bω'),
 ('accumulated set', r'\bξ'),
 ('dependency', r'prerequisite|dependenc'),
 ('coretime', r'coretime'),
 ('authorizer', r'authoriz|Ψ_I|\bα\b|α\[|\bφ\b|φ\[|\bpool\b|\bqueue\b|is-authorized'),
 ('work-package', r'work[- ]?package|\bpackage|\bbundle'),
 ('work-item', r'work[- ]?item'),
 ('work-report', r'work[- ]?report|\breport'),
 ('work-digest', r'work[- ]?digest|\bdigests?\b(?! log)'),
 ('core', r'\bcores?\b|in-core'),
 ('service', r'\bservices?\b|\bδ'),
 ('ELVES', r'elves'),
 ('Polkadot', r'polkadot|parachain|\bbabe\b|relay'),
 ('Ethereum', r'ethereum|\bevm\b|snark|roll-?up'),
 ('dependency graph', r'dependency graph|≺'),
 ('prior/posterior', r'\bprior\b|posterior|†|‡'),
 ('serialization', r'serializ|encod|codec|\bE_4|\bE_2|discriminator'),
 ('Merklization', r'merkl|\btrie|state key|M_B\b'),
 ('shuffle', r'shuffl|fisher'),
 ('notation', r'notation|§3\b|\bN_L|⟦|sequence-set|dictionar|ellipsis'),
 ('JAM Prize', r'\bprize|milestone|fellowship|fuzz|conformance'),
 ('CoreJam', r'corejam|collect.refine|join.accumulate'),
 ('design factors', r'driving factor|coheren|resilien|accessib|sweet spot|further work'),
]
FALLBACK = {'A':'PVM','B':'host call','C':'serialization','D':'Merklization','E':'Merklization','F':'shuffle','G':'Bandersnatch','H':'erasure coding',
 '3':'notation','4':'core','5':'header','6':'Safrole','7':'recent history','8':'authorizer','9':'service','10':'dispute','11':'guarantee','12':'accumulate',
 '13':'statistics','14':'work-package','ARCH':'ELVES','N1':'JAM','N2':'block','N3':'Safrole','N4':'service','N5':'work-package','N6':'assurance','N7':'PVM'}
GENERIC = {'core','service','work-report','work-package','timeslot','epoch','header','prior/posterior','extrinsic'}
def hits(rx, text):
    if any(ord(c) > 127 for c in rx): return len(re.findall(rx, text))
    return len(re.findall(rx, text, flags=re.I))
def choose(it):
    score = collections.Counter()
    for c, rx in VOCAB:
        n = hits(rx, it['stem']); score[c] += min(n, 3)
        if hits(rx, it['id'].replace('-', ' ')): score[c] += 2
        if hits(rx, it.get('section', '')): score[c] += 1
    order = [c for c, _ in VOCAB]
    ranked = sorted(score.items(), key=lambda kv: (-kv[1], order.index(kv[0]) if kv[0] in order else 99))
    out = [c for c, s in ranked if c not in GENERIC and s >= 2][:3]
    if len(out) < 2:
        for c, s in ranked:
            if c not in out and s >= 1 and len(out) < 2: out.append(c)
    if not out: out = [FALLBACK.get(it['ch'], 'core')]
    if 'delta-0.8.0' in it.get('tags', []): out.append('delta-0.8.0')
    return out
def set_tags(path, item_id, tags):
    src = io.open(path, encoding='utf-8').read()
    m = re.search(r'"id":\s*"' + re.escape(item_id) + r'"', src); assert m
    seg = src[m.end():]; t = re.search(r'"tags":\s*\[[^\]]*\]', seg); assert t, item_id
    new = '"tags": [' + ', '.join('"' + x + '"' for x in tags) + ']'
    io.open(path, 'w', encoding='utf-8').write(src[:m.end()] + seg[:t.start()] + new + seg[t.end():])
if __name__ == '__main__':
    dry = '--dry' in sys.argv
    import items
    dist = collections.Counter(); n = 0
    for m in pkgutil.iter_modules(items.__path__):
        mod = importlib.import_module('items.' + m.name)
        for it in getattr(mod, 'ITEMS', []):
            tg = choose(it); n += 1
            for x in tg: dist[x] += 1
            if not dry: set_tags(f'items/{m.name}.py', it['id'], tg)
    print(f'{n} items; vocab used {len([k for k in dist if k != "delta-0.8.0"])}')
