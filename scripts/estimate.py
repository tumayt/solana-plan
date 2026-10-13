"""Reproduce planning arithmetic; no network access or database writes."""
import json
from pathlib import Path
from datetime import date
root=Path(__file__).resolve().parents[1]
read=lambda n: json.loads((root/'evidence'/n).read_text())['data']
db=read('database-sizes.json'); disk=read('disks.json')[0]
# Lhava storage_model.py, measured inputs + explicitly assumed derived tables, 2026-10-06.
h1=.02082+.1878; h2=.11307+.2334
raw_day=668e6*59.4/1e12 # 2026-10-04 sample; flat historical activity is a sensitivity assumption.
snapshot_day=25.33e6*49.1/1e12
days=(date(2026,10,12)-date(2024,1,1)).days
out={
 'units':'decimal TB; USD unless vendor currency needs confirming; engineering days are person-days',
 'live_solana_tb':next(r[1]/1e12 for r in db if r[0]=='solana'),
 'disk_total_tb':disk[1]/1e12,'disk_free_tb':disk[2]/1e12,
 'meteora_2024_tb':h1+h2,'meteora_12_month_tb':h1+h2+.124+.1913,
 'meteora_12_month_two_replicas_30pct_free_tb':(h1+h2+.124+.1913)*2/.7,
 'raw_balances_tb_day':raw_day,'raw_balances_tb_year':raw_day*365,
 'raw_balances_2024_flat_rate_tb':raw_day*days,'raw_balances_2023_flat_rate_tb':raw_day*(days+365),
 'snapshots_tb_year':snapshot_day*365,
 'gcs_us_standard_usd_tb_month':1e12/(2**30)*.02,
 'gcs_meteora_usd_month':(h1+h2)*1e12/(2**30)*.02,
 'gcs_solana_retained_usd_month':next(r[1]/(2**30)*.02 for r in db if r[0]=='solana'),
 'history_days':days,
 'replay_rate_historical_days_per_day':32,
 'replay_rate_source':'User-reported approximate rate; sustained throughput and workload scope not independently verified',
 'dedicated_backfill_calendar_days':{'32x':days/32},
 'additional_2023_replay_days':365/32,
 'dedicated_backfill_including_2023_days':(days+365)/32,
 'catch_up_days_if_32x_includes_live':days/(32-1),
 'transfer_hours_at_100Mbps_70pct_efficiency':{str(tb)+'TB':tb*1e12*8/(100e6*.7)/3600 for tb in [.56,4.96]},
 'path_engineering_days_assumed':{'1':{'product':26,'infra_and_2023':14,'total':40,'range':[30,55]},'2':{'product':26,'platform_and_migration':35,'total':61,'range':[40,85]},'3':{'product_without_old_backfills':22,'platform_and_cutover':28,'total':50,'range':[35,70]}},
 'own_platform_monthly_allowance':{'node':[1500,3000],'database_api':[1000,2000],'monitoring_backup_misc':[200,500],'subtotal':[2700,5500]},
 'exclusions':['Base replacement','extra HA replicas','full raw-block archive','historical source fees','egress','labor','tax and setup adjustments']
}
# User calibration: halve all projected person-day estimates, not elapsed replay time.
out['effort_calibration_factor'] = 0.5
for path in out['path_engineering_days_assumed'].values():
    for key, value in path.items():
        path[key] = [v * 0.5 for v in value] if isinstance(value, list) else value * 0.5
out['incremental_pool_state_fees_engineer_days'] = {'total':14,'range':[8.5,19]}
out['onstream_maintenance_engineer_days_per_month'] = [1,2.5]
out['pilot_engineer_days'] = [2.5,4]
print(json.dumps(out,indent=2))
