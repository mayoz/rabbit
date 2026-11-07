"""Turn a Rabbit workflow file into per-stage instruction lists, as JSON."""
import json
import os
import re
import sys

STAGES = ['Brief', 'Spec', 'Plan', 'Execute', 'Review', 'Integration', 'Push']
RABBIT_VARS = {'<KEY>', '<SUMMARY>', '<REPO>', '<BRANCH>', '<BASE>', '<TASK_DIR>'}
BULLET = re.compile(r'(- |\* |\d+[.)] )')
# <name> or <two words>; skips autolinks (<https://x>), HTML (<br/>) and generics (List<T>).
PLACEHOLDER = re.compile(r'(?<!\w)<[A-Za-z][\w .-]*>')
HTML = {'<br>', '<hr>', '<b>', '<i>', '<p>', '<em>', '<strong>', '<code>', '<kbd>', '<sub>',
        '<sup>', '<details>', '<summary>'}


def _targets(heading):
    """Return [(stage, when)] for a heading, or [] when it maps to no stage."""
    name = ' '.join(heading.lower().split())
    when = 'in'
    stage, sep, suffix = name.rpartition(':')
    if sep and suffix.strip() in ('before', 'after'):
        when, name = suffix.strip(), stage.strip()
    if name == 'spec and plan':
        return [('Spec', when), ('Plan', when)]
    return [(s, when) for s in STAGES if s.lower() == name]


def _items(lines):
    """Split a section body into bullets (with continuation lines) and paragraphs."""
    items, cur = [], []
    for line in lines:
        if not line.strip():
            if cur:
                items.append('\n'.join(cur))
                cur = []
        elif BULLET.match(line) and cur:
            items.append('\n'.join(cur))
            cur = [line.rstrip()]
        else:
            cur.append(line.rstrip())
    if cur:
        items.append('\n'.join(cur))
    return items


def parse(text):
    sections, heading, body, fence = [], None, [], None
    for line in text.splitlines():
        mark = line.lstrip()[:3]
        if mark in ('```', '~~~') and fence in (None, mark):
            fence = None if fence else mark
        if line.startswith('## ') and not fence:
            if heading is not None:
                sections.append((heading, body))
            heading, body = line[3:].strip(), []
        elif heading is not None:
            body.append(line)
    if heading is not None:
        sections.append((heading, body))

    stages, unknown, placeholders = {}, [], []
    for heading, body in sections:
        items = _items(body)
        targets = _targets(heading)
        if not targets:
            unknown.append(heading)
            continue
        for stage, when in targets:
            if items:
                slot = stages.setdefault(stage, {'before': [], 'in': [], 'after': []})
                slot[when].extend(items)
        for p in PLACEHOLDER.findall('\n'.join(items)):
            if p not in RABBIT_VARS and p not in HTML and p not in placeholders:
                placeholders.append(p)
    return {'stages': stages, 'unknown': unknown, 'placeholders': placeholders}


def main(argv):
    if len(argv) != 2:
        print('usage: workflow.py <workflow-file>', file=sys.stderr)
        return 2
    path = os.path.expanduser(argv[1])
    try:
        with open(path, encoding='utf-8-sig') as f:
            text = f.read()
    except OSError:
        print(f'workflow file not found: {path}', file=sys.stderr)
        return 3
    except UnicodeDecodeError:
        print(f'workflow file is not UTF-8 text: {path}', file=sys.stderr)
        return 3
    print(json.dumps(parse(text), indent=2))
    return 0


if __name__ == '__main__':
    sys.exit(main(sys.argv))
