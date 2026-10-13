from pathlib import Path
import base64,re,json,html
R=Path(__file__).resolve().parents[1]
template=(R/'.claude/src/deck/decks/agentic-consumption.html').read_text()
slides=[]
def card(title,body,kind=''):
 return f'<div class="diff-card {kind}"><h3>{title}</h3><p>{body}</p></div>'
def cards(*items): return '<div class="cards">'+''.join(items)+'</div>'
def table(headers,rows):
 return '<table><thead><tr>'+''.join(f'<th>{h}</th>' for h in headers)+'</tr></thead><tbody>'+''.join('<tr>'+''.join(f'<td>{c}</td>' for c in row)+'</tr>' for row in rows)+'</tbody></table>'
def add(short,title,body,takeaway,source,notes):
 slides.append(dict(short=short,title=title,body=body,takeaway=takeaway,source=source,notes=notes))
def flow(items):return '<div class="flow">'+'<span class="arrow">→</span>'.join(f'<div>{a}<small>{b}</small></div>' for a,b in items)+'</div>'
add('Decision','Reliable Solana data.<br><span class="green">Three paths forward.</span>',
 '<p class="subtitle">A decision for Cambrian • 12 October 2026</p>'+cards(card('2024 first','Deliver the history customers need.'),card('Own future collection','Build on our working Agave onstream prototype.'),card('Prove completeness','Check nested calls before committing to a backfill.')),
 'Recommendation: Path 2, subject to historical quality and export approval.','Basis: team facts + Lhava repo + live ClickHouse metadata.',
 'Scope: Solana customer delivery, with Meteora DLMM as the first concrete product. Path 2 is a recommendation, not an approved deployment. User-provided operational facts are attributed to the team, not independently verified incidents. Figures use decimal TB (1 TB = 1,000 GB). Live metadata was read on 2026-10-12 around 11:30 UTC. Customer storage models retain their 2026-10-06 horizon. Press N for notes; E for edit/present. All planning estimates exclude an unmeasured full Solana block archive.')
add('Customer','Lhava needs a trustworthy history',
 cards(card('Positions','When liquidity opened, changed and closed; which price bins held the tokens.'),card('Fees','Pool state, dynamic fees and fees earned by each position.'),card('Coverage','2024 onward is required. 2023 is useful, but lower priority.'))+
 '<div class="callout">Missing inner instructions = missing actions made through other programs, including LP strategy calls.</div>',
 'Reliable delivery matters more to this customer than being first at chainhead.','[R1] Requirements • [R2] Meteora sample validation.',
 'R1: ../../cambrian/customer-lhava/quotation/Requirements.md, current requirements. R2: ../../cambrian/customer-lhava/meteora_export/README.md. The February 2025 SOL/USDC sample matched 420/420 returned ledger events and had no missing API events in that sample. The Aug–Sep 2026 sample matched amounts on 9,718 returned events but omitted 4,469 API events; the 30 unmatched transactions checked were rebalances. Only 2/9,165 adds had bins. These are sample results, not global completeness percentages. Strategy per-bin allocations are estimates and do not establish later bin holdings. This distinguishes source trimming from missing decoders and missing product models.')
add('Current setup','The $2,000 bundle carries hidden work',
 '<div class="metric-row"><div><strong>$2k</strong><small>per month, team-reported</small></div><div><strong>2</strong><small>bare-metal servers</small></div><div><strong>14 TB</strong><small>reported database capacity</small></div></div>'+
 cards(card('Frequent restarts','Old hardware creates recovery and duplicate-cleanup work.'),card('Unexpected gaps','Historic streams can omit inner instructions. Gaps are difficult to detect.'),card('Limited control','More storage is unanswered; retention deletes old rows; a previous export triggered a warning.')),
 'The bundle also includes Base. A Solana move alone does not replace it.','[U] Team-provided facts; current invoice and incident logs were not audited.',
 'U: User facts 1–9. Pinax provides database/indexer/API servers plus Firehose endpoints for Base and Solana for $2,000/month total. Do not allocate the entire invoice to Solana or assume all $2,000 is saved after a Solana cutover. The team reports historical trimming in Pinax and in the Google BigTable/BigQuery sources it evaluated. This is not a claim that every dataset on those Google products is trimmed. Agave onstream has successfully streamed live/historic blocks according to the team; production reliability and retained historical coverage remain unverified.')
add('Measured size','Retention keeps today’s footprint manageable',
 '<div class="metric-row"><div><strong>4.96 TB</strong><small>Solana active table data</small></div><div><strong>1.32 TB</strong><small>raw token balances within it</small></div><div><strong>0.134 TB</strong><small>Meteora DLMM within it</small></div></div>'+
 table(['Live disk snapshot','What it tells us'],[['15.36 TB total / 7.31 TB free','About 14.0 TiB total; broadly consistent with “14 TB” reporting.'],['2.53 TB of Solana tables have a 1-month TTL','Old rows expire automatically; small retained size hides historical demand.'],['4.96 TB is a subset of the shared database disk','Base, derived tables, system logs and inactive data also use space.']]),
 'Free space today is not a capacity plan for keeping several years.','[Q1–Q5] Read-only ClickHouse system metadata, 12 Oct 2026.',
 'Q1 database-sizes.json: sum(bytes_on_disk), active system.parts, grouped by database. Solana = 4,963,606,741,342 bytes. Q2 disks.json: total 15,360,858,259,456; free 7,305,587,920,896 bytes. Disk used is 8.06 TB; active parts across all databases total about 7.78 TB. These measures differ because filesystem use includes inactive parts and other files; no exact reconciliation was attempted. Q3 retention.json extracts table TTL and sorting/partition keys. Q4 retention-sizes.json sums table metadata by TTL expression: 2.526 TB at one month, 1.142 TB at one year, 1.213 TB without TTL, 0.084 TB other. Q5 dlmm-size.json excludes meteora_damm prefixes. These are compressed active storage measurements, not unique event counts, full-chain archive sizes or guaranteed export sizes. Table sizes changed slightly between snapshots due to ongoing ingestion.')
add('History size','The scope determines the storage bill',
 table(['One compressed copy','2024 onward','What changes with 2023?'],[['Meteora positions + fees','~0.56 TB now → 0.87 TB in 12 months','Unmeasured. Budget a sensitivity of +0–0.32 TB.'],['Raw token balances, every change','~40 TB through 11 Oct 2026','~55 TB at the same activity rate.'],['Daily balance snapshots','~0.45 TB per added year','Much smaller, but lose intraday transaction detail.']])+
 '<p class="subtle">Raw-balance figures use a recent daily rate across all historical days. They are scenarios, not measured historical sizes. Full raw blocks are not sized.</p>',
 'Start with selected customer datasets; price full raw history separately.','[R3] Lhava storage model, 6 Oct • [M1] Reproducible arithmetic.',
 'R3: quotation/estimates/storage_model.py and storage.md in the customer repo. H1 positions = 0.2086 TB; H2 incremental pool-state/fees = 0.3465 TB, total 0.5551 TB. After one year: 0.8704 TB. Includes collected and proposed data, with assumed decoder/state/ledger rows. H2 depends on H1, so add each exactly once. Two serving copies at year one with 30% free disk require 0.8704 × 2 / 0.7 = 2.49 TB aggregate, excluding OS, temporary rebuilds, other products and raw node history. 2023 Meteora is unmeasured: +0–0.3153 TB is a planning sensitivity of zero to one recent annual growth increment, not a hard upper bound. Raw balances: 668 million rows/day × 59.4 compressed bytes/row = 39.68 GB/day; 1,015 days from 2024-01-01 to 2026-10-12 exclusive = 40.27 TB; another 365 days gives 54.76 TB. The customer model uses a slightly lower 39.08 GB/day from its retained buffer. Historical activity is not constant; neither rate proves historical volume. Daily snapshots: 25.33 million changed pairs/day × 49.1 bytes × 365 = 0.454 TB/year. Snapshots cannot substitute for transaction-level balances or fill a deleted past without a historical source.')
add('Options','Three choices, three customer promises',
 table(['','1 · Improve Pinax','2 · Bridge, then own','3 · Own from now'],[['History target','2023 onward, if source passes','2024 onward, if source passes','From verified retained start; older data best effort'],['Future collection','Pinax Firehose','Our onstream on OVH','Our onstream on OVH'],['Hosting','Keep database at Pinax','GCP archive + proposed OVH database/API','Proposed OVH database/API + archive'],['Main tradeoff','Least platform change; vendor dependency stays','More migration work; better control','Earlier independence; 2024 demand remains open']]),
 'All three require data unification and customer-level validation.','[U] Paths from the brief; OVH serving placement is a proposed implementation.',
 '“GCP” is interpreted as durable Google Cloud Storage export/archive. For a comparable cost scenario, serving ClickHouse and APIs sit on OVH with onstream, not directly on object storage. If serving must also move to GCP, obtain a separate compute/ClickHouse quote and re-estimate latency and transfer charges. A GCS export by itself is not a working customer API. Path 3 preserves useful existing data where export rights permit; it does not imply deleting current data. Each endpoint must publish its verified start date and gaps.')
add('Path 1','Path 1 · Stay, but require concrete changes',
 flow([('Pinax Firehose','2023+ source'),('New tables','repair + validate'),('Pinax API','switch after approval')])+
 cards(card('What improves','Replace unreliable hardware; agree storage expansion, source quality and export rights.'),card('What stays','Pinax operates the source and hardware. We maintain decoders, history and deduplication.'),card('What blocks it','More hardware cannot restore instructions already missing from the archive.')),
 'Rebuild beside the current data; replace only the windows that pass checks.','[U] Team facts • [E1] Planning estimate: ~20 engineer-days, range 15–27.5.',
 'Path 1 adjusted central estimate: H1 production positions 13 engineer-days, plus 5 assumed days for infrastructure coordination, ingestion hardening and unification beyond H1, plus 2 assumed days for a 2023 extension = 20. Planning range 15–27.5. All projected person-days are calibrated to 50% of the initial estimates at the user’s request; the source repo baseline is unchanged. Pinax upgrade cost and delivery date remain unknown. Preserve the current validated dataset until the replacement passes coverage and amount checks. Historical source availability remains an external dependency.')
add('Path 2','Path 2 · Use Pinax as a bridge',
 flow([('Pinax history','verify 2024 first'),('GCP archive','export + restore test'),('OVH + onstream','own future collection'),('Customer API','validated cutover')])+
 cards(card('Best fit for demand','Recover what is available from 2024 while building independent live capture.'),card('Durable control','Keep replayable exports and quality records. Improve onstream without losing new history.'),card('Exit conditions','Export approval, source completeness, restore test, stable live service and a Base plan.')),
 'Preferred path if Pinax’s historical sample meets the customer’s needs.','[U] Existing onstream prototype • [E2] ~30.5 engineer-days, range 20–42.5.',
 'Path 2 adjusted central estimate = H1 13 days + platform/migration 17.5 assumed days: onstream hardening 6; OVH deployment/security/monitoring 3; GCP export/restore 3; overlap verification and cutover 3; Base dependency discovery and exit planning 2.5. Total 30.5, planning range 20–42.5. This is 50% of the initial person-day estimate. Excludes actual Base rebuilding, separate source procurement, full raw archive engineering and H2 fees. Onstream still needs upgrade rehearsal, finality handling, reconnect/backpressure, checkpoints and recovery. A second collection path is not included in the lean allowance.')
add('Path 3','Path 3 · Own collection starting now',
 flow([('Solana network','available blocks'),('OVH + onstream','capture + retain'),('Unified data','quality labels'),('Customer API','explicit history limits')])+
 cards(card('Immediate benefit','Start building an archive we control. Reduce dependence on future Pinax collection.'),card('Customer consequence','A recent-history product can ship, but cannot meet 2024 demand on its own.'),card('Same node obligations','Agave upgrades, disk health, replay, monitoring and incident response still belong to us.')),
 'Choose this if history cannot be recovered and the customer accepts a narrower scope.','[U] Archive access is difficult • [E3] ~25 engineer-days, range 17.5–35.',
 'Path 3 adjusted central estimate = H1 13 minus 2 historical backfill-operation days = 11 for recent-only positions, plus 14 assumed platform/cutover days: onstream hardening 6, OVH deployment 3, archive/restore 2, endpoint limits and cutover 1.5, Base exit discovery 1.5. Total 25, planning range 17.5–35. This is 50% of the initial person-day estimate. Decoder, ledger and validation work remain in scope. Onstream can replay only available historical ledger/metadata; a fresh snapshot does not imply history since 2024. Difficulty finding two-week archives is a team observation, not a network retention guarantee.')
add('Common work','Unification makes the data usable',
 flow([('Collect','keep source + version'),('Normalize','one record format'),('Reconcile','duplicates + gaps'),('Serve','clear quality flags')])+
 cards(card('Repair known gaps','Add v2 and rebalance decoding; repair affected months; model open/close events.'),card('Make retries safe','Use stable event IDs and checkpoints. Verify amounts, instruction paths and finalized blocks.'),card('Expose quality','Label verified, reconstructed and unavailable fields. Publish coverage by date and endpoint.')),
 'Better servers reduce failures; they do not remove the need for safe replay.','[R2, R4] Known gaps + effort model • [C1–C4] ClickHouse rules.',
 'R4: quotation/estimates/mandays.md and mandays_model.py. The 14 engineer-day Meteora prototype is a historical yardstick; its task split is assumed in that repo. H1 already includes missing decoders, ledger materialization, repair/backfill validation and endpoint work; do not charge that work again as a second “unification” project. Proposed stable event identity should include chain, finalized block/slot context, transaction signature and full instruction/event path; exact schema requires validation, because one transaction can contain multiple actions. Per insert-batch-size, replay in batches around 10k–100k rows and watch merge load. Per insert-mutation-avoid-update, prefer versioned corrected rows or replacement tables over frequent whole-part mutations; ReplacingMergeTree merges are eventual and reads must apply the chosen deduplication semantics. Per insert-optimize-avoid-final, do not routinely force OPTIMIZE FINAL. Per schema-partition-lifecycle, design retention around lifecycle partitions for new tables; existing Meteora tables partition only by chain, while live balance/trades tables now use monthly partitions. These are scoped recommendations, not a full schema review. All ClickHouse access here was read-only metadata with 30-second defaults and scan caps on the explicit queries.')
add('Monthly cost','Operating our own infrastructure has a higher visible budget',
 table(['Monthly, before labor','1 · Pinax','2 · After migration','3 · Own from now'],[['Core platform','Current $2,000 + upgrade quote','$2,700–5,500 allowance','$2,700–5,500 allowance'],['Selected archive on GCP','Optional / not priced','~$10 for 0.56 TB','~$10 at the same size'],['Base continuity','Included in current bundle','Add B: quote required','Add B: quote required'],['Pinax during transition','Already included','Add $2,000 while overlapping','Add $2,000 until safe exit']])+
 '<p class="subtle">Own-platform allowance: node $1.5–3k + database/API $1–2k + monitoring/backup $0.2–0.5k. No savings claim.</p>',
 'Archive storage is cheap relative to running reliable collection and APIs.','[P1] GCS published rate • [P2] OVH price reference • [M1] Budget assumptions.',
 'P1 https://cloud.google.com/storage/pricing checked 2026-10-12: illustrative US regional Standard rate $0.000027397/GiB-hour ≈ $0.020/GiB-month at 730 hours. Thus 1 decimal TB ≈ $18.63/month; 0.555 TB ≈ $10.34; current 4.96 TB Solana data ≈ $92/month if exported at the same compressed size. Actual export encoding/compression must be measured. Operations, network egress, retrieval classes and database compute are separate. P2 https://www.ovhcloud.com/en/bare-metal/high-grade/ checked 2026-10-12 lists HGR-SDS-1 2024 from $1,986/month incl. VAT and $1,986 installation in the displayed global locale; 256 GB RAM and six 7.68 TB NVMe drives. This is a database/storage price anchor, not a Solana node recommendation, binding quote or region/currency-normalized comparison. P3 https://docs.anza.xyz/operations/requirements recommends additional RPC resources including 16 cores and 512 GB for all account indexes, separate account/ledger disks, and performance testing. The $1.5–3k node allowance needs a real suitable-hardware quote and benchmark. Lean own-platform budget is $2.7–5.5k + selected archive + B (Base replacement) + transfer/source fees. Two months of Path 2 overlap adds $4k in Pinax invoices, not an assumed two-month completion promise. Extra HA nodes/replicas, labor, tax normalization, setup fees, raw-block archive and historical source fees are excluded. Customer repo $4,000/14 TB is a customer pricing convention, not the actual Pinax cost or a cloud quote.')
add('Effort','Budget engineering separately from server rent',
 table(['Meteora positions first','1 · Pinax','2 · Bridge, then own','3 · Own from now'],[['Central estimate','20 days','30.5 days','25 days'],['Planning range','15–27.5 days','20–42.5 days','17.5–35 days'],['Included product work','13 days','13 days','11 days, recent-only'],['Platform / migration / 2023','7 days','17.5 days','14 days']])+
 '<div class="callout">Pool state and fees add ~14 engineer-days (adjusted range 8.5–19). Reserve 1–2.5 engineer-days/month for onstream operations after launch.</div>',
 'One engineer-day means one person working one day; it is not a calendar deadline.','[R4] H1/H2 effort baseline • [E1–E3] Assumed platform work and ranges.',
 'Effort calibration: all projected person-days and ranges are 50% of the initial deck estimates, as requested by the user. Adjusted H1 = 13 days, range 8.5–18; incremental H2 = 14 days, range 8.5–19. H1 + H2 = 27 product days before platform work. Central positions+fees totals: Path 1 34, Path 2 44.5, Path 3 39 days. Recent-only fee scope may change. Onstream maintenance reserve is 1–2.5 engineer-days/month, assumed; releases or incidents can exceed it. Path 2 is 6.1 person-weeks at 5 working days/week, or about 4.4 calendar weeks with two engineers at 70% allocation, before dependency and replay delays. Calendar replay, transfer and test-window durations were not halved. Current Pinax cleanup is unmeasured. Labor cost is person-days times the organization’s loaded rate. The historical 14-day prototype and original customer-repo estimates remain unchanged as source evidence, not current planning figures.')
add('Elapsed time','About 32 days to replay the 2024 backlog',
 table(['Scope','Calculation at ~32 historical days/day','Continuous replay'],[['2024 → 11 Oct 2026','1,015 ÷ 32','~31.7 days'],['Add 2023','365 ÷ 32','~11.4 more days'],['2023 → 11 Oct 2026','1,380 ÷ 32','~43.1 days total']]),
 'Allow about 32 days of continuous replay, plus transfer, validation and interruptions.','[U] User-reported ~32 historical days/day • [M1] Replay arithmetic.',
 'Rate supplied by the user: around 32 historical days per elapsed day. This is an approximate reported rate, not an independently verified sustained benchmark; hardware, source and workload scope were not supplied. Keep the deck baseline of 2024-01-01 through 2026-10-11 inclusive (1,015 days; cutoff 2026-10-12 exclusive). Dedicated replay: 1015/32 = 31.71875 calendar days. Adding 2023 gives 365/32 = 11.40625 additional days, or 1380/32 = 43.125 total days. If 32 is total processing capacity shared with live ingestion, net historical catch-up is 31 days/day and 1015/31 = 32.74 elapsed days. Do not subtract live capacity again if the reported 32 is already historical-only throughput. Assumes continuous operation, available source history and a representative sustained rate. Engineering, transfer, import, validation, retries and downtime are not included in this replay-only calculation; some stages may overlap. Exporting already-decoded data requires a separate export/transfer/import throughput model.')
add('Decision gates','Make Path 2 earn the cutover',
 cards(card('1 · History passes','Check 2024 samples, protocol versions and nested strategy calls. Record unrecoverable gaps.'),card('2 · Exit is possible','Written export terms, measured transfer, archive restore and a priced Base continuity plan.'),card('3 · Operations pass','Restart/replay and upgrade tests; stable parallel collection; customer signs off on output.'))+
 '<div class="callout">If history fails: ship a clearly scoped Path 3 product only with customer acceptance, and pursue older history separately.</div>',
 'Discussion: is 2024 completeness essential, and what gaps will Lhava accept?','[R1–R2] Customer evidence • Proposed acceptance gates, not existing guarantees.',
 'Proposed acceptance approach: stratified windows across 2024, the April 2025 v2 transition, repaired February 2025, and recent rebalance-heavy periods; include nested program calls and known failure examples. Compare expected signatures/action counts, raw token amounts and instruction path coverage against independent evidence where available. Sample agreement alone is not proof of whole-period completeness. Track coverage per date, protocol/version and source, including missing metadata. Require an agreed customer quality threshold instead of reusing the old informal 95–96% estimate as an SLA. Operational gate proposal: 14 days of parallel collection including peak traffic, deliberate restarts, replay verification, restore drill and an upgrade/rollback rehearsal. Fourteen days is a proposed test window, not proven sufficient for every risk. Price high availability explicitly; a second replica alone does not guarantee 50 ms P99.')
add('Next steps','Fund the pilot. Keep the history promise conditional.',
 table(['Responsible team','Next action','Decision evidence'],[['Data engineering','Sample 2024 + 2023; check missing instructions','Coverage report and source feasibility'],['Platform engineering','Benchmark onstream on suitable OVH hardware','Replay rate, bytes/day, restart + upgrade results'],['Commercial / operations','Agree Pinax export/upgrade terms; price Base continuity','Written terms and complete run-cost estimate'],['Product + customer team','Validate a unified Meteora sample with Lhava','Accepted fields, gaps and history start']])+
 '<p class="subtle">Proposed first checkpoint: 5 working days, using 2.5–4 engineer-days across data and platform. This is part of the path budget.</p>',
 'Proceed with Path 2 only when evidence supports history, export and operational readiness.','Notes: press N • Sources and calculations included with this deck.',
 'The proposed pilot uses 2.5–4 total engineer-days over a five-working-day checkpoint if staff are available. It is included within the path-specific effort allowances, not additive. No full deployment, vendor cancellation or customer promise is authorized by this deck. The existing dev team already owns Solana; the user reports a deliberate lower priority over the last six months. Decisions required: revised priority and dev-team allocation; budget for the pilot; allocated dev-team capacity for Agave/onstream maintenance; target geography; whether GCP is archive-only or also serving; customer quality threshold; whether 2023 is a separate phase. Sources: R1 Requirements; R2 meteora_export README; R3 storage.py/storage.md; R4 mandays_model.py/mandays.md; Q1–Q5 dated live metadata under evidence; M1 scripts/estimate.py and evidence/estimates.json; P1 Google storage pricing, P2 OVH High Grade, P3 Anza hardware requirements. The source repo was inspected read-only; credentials and transaction payloads are not packaged.')
from visuals import apply
apply(slides)
content=[]
for i,s in enumerate(slides):
 h='h1' if i==0 else 'h2'
 content.append(f'<div class="slide {"active" if i==0 else ""}" data-slide="{i}" data-title="{s["short"]}"><div><div class="label">CAMBRIAN / SOLANA DATA / {i+1:02d}</div><{h}>{s["title"]}</{h}><div class="fragment">{s["body"]}</div><p class="takeaway fragment">{s["takeaway"]}</p><p class="source">{s["source"]}</p></div></div>')
start=template.index('    <!-- ===== SLIDE 1:')
end=template.index('  <div class="progress"',start)
out=template[:start]+'\n'.join(content)+'\n</div>\n'+template[end:]
out=out.replace('Cambrian API: Agentic Consumption Final','Cambrian | Solana data delivery paths')
# Official Cambrian pattern, embedded for offline portability.
# Source: https://www.cambrian.org/redesign/background-pattern.svg
background=(R/'scripts/background.svg').read_text()
background_data=base64.b64encode(background.encode()).decode()
for filename in ['cambrian_slides_background_dark.svg', 'cambrian_bg_light.jpg']:
 out=out.replace("url('"+filename+"')", "url('data:image/svg+xml;base64,"+background_data+"')")
css='''
.cards {display:grid;grid-template-columns:repeat(3,1fr);gap:18px;margin:22px 0}
.cards .diff-card {padding:20px;background:var(--risk-bg);border:1px solid var(--border-light);border-radius:10px}
.cards h3 {font-size:24px;margin-bottom:12px;color:var(--accent-light)}
.cards p {font-size:21px;line-height:1.4;color:var(--text-dim)}
.slide h1{font-size:64px;line-height:1.06;margin:16px 0 28px}
.slide h2{font-size:43px;line-height:1.12;margin:16px 0 26px;letter-spacing:-1px}
.slide .label{font-size:12px;letter-spacing:2px;color:var(--accent-light)}
.slide table{width:100%;border-collapse:collapse;margin:18px 0;font-size:19px}
.slide td,.slide th{padding:14px 15px;border-bottom:1px solid var(--border-light);text-align:left;font-size:19px;line-height:1.3}
.slide th{color:var(--accent-light);font-weight:600;background:var(--surface)}
.slide td:first-child{font-weight:600}
.metric-row{display:flex;gap:24px;margin:25px 0 30px}.metric-row>div{flex:1;border-left:2px solid var(--accent);padding-left:20px}
.metric-row strong{font-size:45px;font-weight:500;color:var(--accent-light);display:block}
.metric-row small{display:block;font-size:18px;color:var(--text-dim);margin-top:7px}
.takeaway{font-size:23px!important;color:var(--text)!important;border-top:1px solid var(--border-light);padding-top:17px;margin-top:24px;line-height:1.35}
.source{font-size:12px!important;color:var(--text-dim)!important;margin-top:15px;line-height:1.3}
.subtle{font-size:17px!important;line-height:1.45;color:var(--text-dim);margin-top:18px}
.callout{font-size:22px;line-height:1.4;padding:18px 22px;border-left:3px solid var(--accent);background:var(--surface);margin-top:20px}
.flow{display:flex;align-items:center;gap:12px;margin:25px 0}.flow>div{flex:1;padding:20px 12px;border:1px solid var(--accent);border-radius:10px;font-size:23px;text-align:center}
.flow small{display:block;color:var(--text-dim);font-size:16px;margin-top:10px}.arrow{color:var(--accent);font-size:28px}
#notesDialog{background:var(--bg);color:var(--text);border:1px solid var(--accent);border-radius:12px;width:min(900px,90vw);max-height:85vh;padding:30px;margin:auto;line-height:1.65;font-size:18px}#notesDialog::backdrop{background:#000a}#notesDialog h3{margin-bottom:16px}#notesDialog button{float:right;padding:8px 14px;cursor:pointer}#notesDialog a{color:var(--accent-light)}
@media print {
 @page {size: 13.333in 7.5in;margin:0}
 .slide-frame{background-image:none!important}.slide-frame::before{display:none!important}
 body.print-all .slide,body.print-current .slide.active{height:720px!important;min-height:720px!important;width:1280px!important;padding:42px 60px!important;break-inside:avoid}
 .slide>div{zoom:1!important}.slide h1{font-size:56px}.slide h2{font-size:38px}.slide td,.slide th{font-size:17px;padding:11px 12px}.cards p{font-size:19px}.cards h3{font-size:22px}.metric-row strong{font-size:38px}.takeaway{font-size:20px!important}
 .source{font-size:11px!important}.cards{margin:18px 0}.slide-hidden,#notesDialog{display:none!important}body.print-all .slide.slide-hidden{display:none!important}
}
'''
css += (R/'scripts/visuals.css').read_text()
css += (R/'scripts/background.css').read_text()
leaf_svg='''<svg viewBox="0 0 64 76" fill="none" aria-hidden="true" focusable="false">
<path fill-rule="evenodd" d="M32 14C21-3 5 3 4 18L21 24L3 23Q2 30 6 35L23 35L8 40Q11 47 17 51L27 45L20 55Q26 61 32 65Q39 60 44 55L37 45L49 51Q55 45 57 40L41 35L59 34Q62 29 60 23L43 25L59 18C57 3 42-3 32 14Z M23 14C18 10 16 14 20 20C23 24 27 19 23 14Z M41 14C46 10 48 14 44 20C41 24 37 19 41 14Z M26 28C21 25 21 31 25 34C28 36 29 30 26 28Z M38 28C43 25 43 31 39 34C36 36 35 30 38 28Z" fill="currentColor" fill-opacity=".32" stroke="currentColor" stroke-width="1.4" stroke-linejoin="round"/>
<path d="M32 16V62Q32 70 27 74M32 30L26 23M32 30L38 23M32 43L25 39M32 43L39 39M32 55L28 51M32 55L36 51" stroke="currentColor" stroke-width="1.3" stroke-linecap="round"/>
</svg>'''
leaves='<div class="drifting-leaves" aria-hidden="true">'+''.join(f'<span class="drifting-leaf leaf-{i}">{leaf_svg}</span>' for i in range(4))+'</div>'
out=out.replace('<body>', '<body>'+leaves, 1)
out=out.replace('<body>', '<body>'+re.sub(r'<svg\b', '<svg class="deck-background" aria-hidden="true" focusable="false" preserveAspectRatio="xMidYMid slice"', background, count=1), 1)
out=out.replace('</style>',css+'</style>')
out=out.replace('<div class="toolbar" id="toolbar">','<div class="toolbar" id="toolbar"><button class="toolbar-btn" onclick="showNotes()"><span class="label-text">notes · N</span></button>')
out=out.replace('<div class="toolbar" id="toolbar">','''<div class="toolbar" id="toolbar"><button type="button" class="toolbar-btn" id="fullscreenToggle" onclick="toggleFullscreen()" aria-pressed="false" aria-keyshortcuts="F11" title="F11: toggle full screen; Esc: exit"><span class="label-text" id="fullscreenLabel">full screen · F11</span></button>''')
out=out.replace('<body>','<body><dialog id="notesDialog"><button onclick="document.getElementById(\'notesDialog\').close()">Close</button><h3 id="notesTitle"></h3><p id="notesText"></p></dialog>')
out=out.replace('  window.next = next;','  window.goToSlide = goToSlide;\n  window.next = next;')
notes=json.dumps([{k:s[k] for k in ['short','notes']} for s in slides]).replace('</','<\\/')
extra='''<script>
document.querySelectorAll('.drifting-leaf').forEach(leaf=>{
  const duration=28+Math.random()*30;
  leaf.style.setProperty('--leaf-size',(22+Math.random()*26).toFixed(1)+'px');
  leaf.style.setProperty('--fall-duration',duration.toFixed(2)+'s');
  leaf.style.setProperty('--fall-delay',(-Math.random()*duration).toFixed(2)+'s');
  leaf.style.setProperty('--sway-duration',(5+Math.random()*6).toFixed(2)+'s');
});
window.toggleFullscreen=async()=>{
  try {
    if(document.fullscreenElement) await document.exitFullscreen();
    else if(document.documentElement.requestFullscreen) await document.documentElement.requestFullscreen();
    else alert('Full screen is unavailable in this browser. Use your browser’s full screen command.');
  } catch(error) {
    alert('Unable to enter full screen. Use your browser’s full screen command.');
  }
};
document.addEventListener('keydown',event=>{
  if(event.key!=='F11'||event.ctrlKey||event.metaKey||event.altKey||event.shiftKey) return;
  event.preventDefault();
  if(!event.repeat) window.toggleFullscreen();
});
document.addEventListener('fullscreenchange',()=>{
  const active=Boolean(document.fullscreenElement);
  document.getElementById('fullscreenToggle').setAttribute('aria-pressed',String(active));
  document.getElementById('fullscreenLabel').textContent=active?'exit full screen · F11':'full screen · F11';
});
const deckNotes=NOTES;
window.showNotes=()=>{const i=Number(document.querySelector('.slide.active').dataset.slide);document.getElementById('notesTitle').textContent=deckNotes[i].short+' · sources and assumptions';document.getElementById('notesText').textContent=deckNotes[i].notes;document.getElementById('notesDialog').showModal()};
document.addEventListener('keydown',e=>{if(e.key.toLowerCase()==='n'&&!e.target.isContentEditable){e.preventDefault();showNotes()}});
document.fonts.ready.then(()=>window.dispatchEvent(new Event('resize')));
</script>'''.replace('NOTES',notes)
out=out.replace('</body>',extra+'</body>')
(R/'solana-data-paths.html').write_text(out)
# Plain companion supports reviewing sources without a presentation viewer.
notes_html='<html><head><meta charset="utf-8"><title>Solana data paths: evidence and assumptions</title><style>body{font:18px/1.65 system-ui;max-width:980px;margin:50px auto;padding:25px;color:#182018}h2{margin-top:50px;color:#3b7120}a{color:#3b7120}pre{white-space:pre-wrap;background:#f0efe8;padding:25px;font-size:14px}</style></head><body><h1>Solana data paths: evidence and assumptions</h1><p>12 October 2026 · TB are decimal. Live facts, customer-model projections and planning assumptions are distinguished below.</p>'
for i,s in enumerate(slides):notes_html+=f'<h2>{i+1}. {html.escape(s["short"])}</h2><p>{html.escape(s["notes"])}</p>'
notes_html+='<h2>Reproduce the model</h2><p>Run <code>python3 scripts/estimate.py</code>. The model reads the bundled metadata snapshots and does not connect to a server.</p><pre>'+html.escape((R/'evidence/estimates.json').read_text())+'</pre>'
notes_html+='<h2>Primary public references</h2><ul>'+''.join(f'<li><a href="{u}">{t}</a></li>' for t,u in [('Google Cloud Storage pricing','https://cloud.google.com/storage/pricing'),('OVH High Grade servers','https://www.ovhcloud.com/en/bare-metal/high-grade/'),('Anza hardware requirements','https://docs.anza.xyz/operations/requirements')])+'</ul></body></html>'
(R/'sources-and-assumptions.html').write_text(notes_html)
print(f'Built {len(slides)} slides')
