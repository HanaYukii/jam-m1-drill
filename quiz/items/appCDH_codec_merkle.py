# -*- coding: utf-8 -*-
# Appendix C — Serialization Codec; D — State Merklization; E — General Merklization; H — Erasure Coding (GP 0.8.0)
ITEMS = [
{
 "id": "appE-merkle-functions",
 "lens": "演算法",
 "ch": "E", "section": "E.1 Binary Merkle Trees & E.2 MMR", "gpRef": "eq. E.1–E.8",
 "difficulty": 2, "kind": "concept", "tags": ["Merklization", "MMR"],
  "stemZh": "附錄 E 定義了通用的 Merklization 函數 N、M_B、M 與 MMR 的 append A。每一個各做什麼？各用在哪裡？",
  "optionsZh": [
   "N（節點）：在 ⌈n/2⌉ 處切分序列，並雜湊 '$node' ⌢ 左 ⌢ 右（well-balanced）；M_B 是對原始 blob 取的 well-balanced root（它刻意不對每一項先做雜湊）；M（定深）先把每片葉子雜湊成 '$leaf' ⌢ v，再用零雜湊補到 2 的冪——用於 segment root 與 paged proof；MMR 的 append 函數 A 以二進位加法式的進位加上一個 peak，而 super-peak 則以 '$peak' 前綴把各 peak 摺疊起來",
   "N：在 ⌊n/2⌋ 處切分序列所以右半較大，並雜湊 '$node' ⌢ 左 ⌢ 右；M_B 是對原始 blob 取的 well-balanced root；M（定深）先把每片葉子雜湊成 '$leaf' ⌢ v，再以重複最後一片葉子（而非零雜湊）補到 2 的冪；MMR 的 append 函數 A 為每片葉子直接開一個新 peak、完全不進位，而 super-peak 以 '$peak' 前綴摺疊",
   "N：在 ⌈n/2⌉ 處切分，並雜湊 左 ⌢ 右、不加任何 domain-separation 前綴（前綴保留給葉子）；M_B 是補到 2 的冪的定深 root，而 M 才是對原始 blob 取的 well-balanced root——兩者是依葉子處理方式而非形狀命名的；MMR 的 append 像二進位加法一樣進位，而 super-peak 以 '$node' 前綴在 Blake2b 之下摺疊",
   "N：在 ⌈n/2⌉ 處切分，並雜湊 '$node' ⌢ 左 ⌢ 右（well-balanced）；M_B 會先把每一項雜湊成 '$leaf' ⌢ v 再建樹，這正是它每項多花一次雜湊的原因；M（定深）取的是原始 blob，並用零雜湊補到 2 的冪；MMR 的 append 像二進位加法一樣進位，而 super-peak 以 '$peak' 前綴摺疊，但只在 peak 數為 2 的冪時才有定義"
  ],
  "stem": "Appendix E defines the general Merklization functions N, M_B, M and the MMR append A. What does each one do, and where does each get used?",
 "options": [
  "N (node): splits the sequence at ⌈n/2⌉ and hashes '$node' ⌢ left ⌢ right (well-balanced); M_B is the well-balanced root taken over the RAW blobs (it deliberately avoids hashing each item); M (constant-depth) first hashes each leaf as '$leaf' ⌢ v and pads to a power of two with zero hashes — used for segment roots and paged proofs; the MMR append A adds a peak with binary-addition-style carrying and the super-peak folds the peaks with a '$peak' prefix",
  "N (node): splits the sequence at ⌊n/2⌋ so the right half is the larger one, and hashes '$node' ⌢ left ⌢ right; M_B is the well-balanced root taken over the RAW blobs; M (constant-depth) first hashes each leaf as '$leaf' ⌢ v and pads to a power of two by repeating the final leaf rather than with zero hashes; the MMR append A gives every leaf its own new peak without any carrying, and the super-peak folds the peaks with a '$peak' prefix",
  "N (node): splits the sequence at ⌈n/2⌉ and hashes left ⌢ right with no domain-separation prefix, the prefixes being reserved for leaves; M_B is the constant-depth root that pads to a power of two while M is the well-balanced root over the raw blobs — the two are named for their leaf treatment, not their shape; the MMR append A carries like binary addition and the super-peak folds the peaks with a '$node' prefix under Blake2b",
  "N (node): splits the sequence at ⌈n/2⌉ and hashes '$node' ⌢ left ⌢ right (well-balanced); M_B hashes every item as '$leaf' ⌢ v before building the tree, which is what costs it one extra hash per item; M (constant-depth) takes the RAW blobs and pads to a power of two with zero hashes; the MMR append A carries like binary addition and the super-peak folds the peaks with a '$peak' prefix, but is defined only when the number of peaks is a power of two"
 ],
 "answer": 0,
 "optNotes": [
   "M_B 直接把原始 blob 當 leaf（GP 明說 avoids hashing each item），M 才先 $leaf 雜湊再零填。",
   "三處都相反：GP 是 ⌈n/2⌉ 切、補 zero hash H_0、A 遇到已占用的 slot 就折疊進位。",
   "N 的定義本身就含 $node 前綴，M_B 與 M 的角色被對調，super-peak 用 $peak 且是 Keccak。",
   "加 $leaf 的是 constancy preprocessor C，且 super-peak 對任意個非 ∅ peak 都遞迴定義。",
 ],
 "explanation": "eq. E.1：N(v, H) = H_0 若空；v_0 若單一；否則 H($node ⌢ N(v[..⌈n/2⌉]) ⌢ N(v[⌈n/2⌉..]))——「well-balanced」使最大深度最小。前綴 $node/$leaf 防止 preimage collision。E.3：M_B(v, H) = H(v_0) 當 |v| = 1，否則 N(v, H)——直接把原始 blob 當 leaf、不加 $leaf 前綴（GP 明說它「avoids hashing each item in the sequence」）；用於 extrinsic hash 與 accumulation output belt 的每塊 root（Keccak）。E.4：M（constant depth）先 $leaf 雜湊、零填到 2 的冪——segment root 與 paged proofs（J_x/L_x, x = 6 即每 64 個 leaf 一頁）用它，因為固定深度讓 import 證明大小固定。E.8：MMR append A（peaks 序列，像二進位加法進位），super-peak 用 $peak 前綴從左到右摺疊。β_B 就是這種 MMR（Keccak）。",
 "trap": "M_B 取 root 的分割點是 ⌈n/2⌉（左邊較多）；M 是零填到 2^k。"
},
]
