"""All-phase infinite certificates and adversarial full-field controls."""
import json
import sys
import wake


def main():
    if sys.flags.optimize:
        raise SystemExit('Run without -O')
    certified = 0
    for phase in range(104):
        word = wake.STANDARD[phase:] + wake.STANDARD[:phase]
        for heading in range(4):
            seed, _, _ = wake.periodic_data(word, heading)
            assert wake.verify_forever(seed, word, heading)
            certified += 1
    seed, _, drift = wake.periodic_data(wake.STANDARD)
    removed = 0
    for q in seed:
        assert not wake.verify_forever(seed - {q}, wake.STANDARD)
        removed += 1
    far = (10**100 * drift[0], 10**100 * drift[1])
    assert far not in seed
    assert not wake.verify_forever(seed | {far}, wake.STANDARD)
    positions, _, _ = wake.plan(wake.STANDARD)
    classes = {wake.class_key(q, drift) for q in positions}
    marker = next((x, 0) for x in range(1000)
                  if wake.class_key((x, 0), drift) not in classes)
    assert wake.verify_forever(seed | {marker}, wake.STANDARD)
    print(json.dumps({'status': 'PASS', 'all_phase_heading_certificates': certified,
                      'required_seed_deletions_rejected': removed,
                      'far_blocker_epoch': str(10**100),
                      'far_blocker_rejected': True, 'off_trace_marker_accepted': True},
                     sort_keys=True))


if __name__ == '__main__':
    main()
