#!/usr/bin/env python3
r"""hvac_run.py - one house, start to finish.

    python hvac_run.py jobs/<house>/job.json [--pdf <plans.pdf>] [--skip-scan] [--no-live] [--result trades/hvac/result.json]

  1. hvacscan.py     hvac_scan.json - the WSEC credits, the system they name, the envelope, the window schedule,
                     the fans, hood and dryer, off the plan TEXT (skipped with --skip-scan, or when the set has no
                     text layer - then job.json carries it; LOOK at the energy sheet either way)
  2. hvackit.py      hvac_takeoff.json + hvac_report.md (loads -> system -> every part, run, check)
  3. hvac_model.py   <slug>_app.json (the house in the electrical skill's wall visual, the HVAC inside)
  4. hvac_render.py  shot_35.png, shot_215.png, shot_top.png (straight down = the mechanical plan)
  5. hvac_bid.py     hvac_bid.json + hvac_bid.md (+ the worker's result.json with --result)
  6. hvac_pdf.py     <slug>.pdf (the parts list)
  7. receipts.py     receipts.md
"""
import argparse, os, subprocess, sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import hvac_common as C

PY = sys.executable
PLANS = r"C:\Users\Naro2\Google Drive\RVM Docs\Plans for Leads"


def run(cmd):
    print('$', ' '.join(os.path.basename(c) if c.endswith('.py') else c for c in cmd))
    r = subprocess.run(cmd, env=dict(os.environ, PYTHONIOENCODING='utf-8'))
    if r.returncode:
        sys.exit(f'failed: {cmd[1]}')


if __name__ == '__main__':
    ap = argparse.ArgumentParser(); ap.add_argument('job'); ap.add_argument('--pdf', default=None); ap.add_argument('--skip-scan', action='store_true')
    ap.add_argument('--no-live', action='store_true'); ap.add_argument('--result', default=None, help='write the rvm-app worker result.json here')
    a = ap.parse_args()
    job = C.load(a.job); d = os.path.dirname(os.path.abspath(a.job))
    interior = C.resolve(job.get('interior', 'interior.json'), d)
    if not os.path.exists(interior):
        sys.exit(f"no interior.json at {interior} - run the finish skill's interior.py first (the room source every interior trade shares)")
    pdf = a.pdf or os.path.join(PLANS, job.get('plans') or '')
    if not a.skip_scan and os.path.isfile(pdf):
        run([PY, os.path.join(HERE, 'hvacscan.py'), pdf, '--out', os.path.join(d, 'hvac_scan.json'), '--png', os.path.join(d, 'energy_p{N}.png')])
    elif not a.skip_scan:
        print(f"  (no plan set at {pdf} - scan skipped; {'hvac_scan.json from an earlier read is used' if os.path.exists(os.path.join(d, 'hvac_scan.json')) else 'job.json carries the system'})")
    run([PY, os.path.join(HERE, 'hvackit.py'), a.job, '--interior', interior])
    tk = os.path.join(d, 'hvac_takeoff.json')
    run([PY, os.path.join(HERE, 'hvac_model.py'), tk, '--interior', interior, '--job', a.job])
    payload = os.path.join(d, f"{job['slug']}_app.json")
    run([PY, os.path.join(HERE, 'hvac_render.py'), payload, '--out', os.path.join(d, 'shot_35.png'), '--yaw', '35'])
    run([PY, os.path.join(HERE, 'hvac_render.py'), payload, '--out', os.path.join(d, 'shot_215.png'), '--yaw', '215'])
    # the mechanical plan: straight down, the walls reading as the floor-plan outline
    run([PY, os.path.join(HERE, 'hvac_render.py'), payload, '--out', os.path.join(d, 'shot_top.png'), '--yaw', '0', '--pitch', '88'])
    bid = [PY, os.path.join(HERE, 'hvac_bid.py'), tk] + (['--no-live'] if a.no_live else [])
    if a.result:
        bid += ['--result', a.result, '--model-file', payload]
    run(bid)
    run([PY, os.path.join(HERE, 'hvac_pdf.py'), tk, os.path.join(d, f"{job['slug']}.pdf")])
    run([PY, os.path.join(HERE, 'receipts.py'), d])
    print('done', d)
