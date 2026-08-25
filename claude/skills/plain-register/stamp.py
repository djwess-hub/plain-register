#!/usr/bin/env python3
"""Record that plain-register ran on a file, so it can be told apart later.

Markdown gets frontmatter, which Dataview can query. Word and PowerPoint get a
document property, which readers never see.

usage:  stamp.py <file> [<file> ...] [--date YYYY-MM-DD]
        stamp.py --read <file>       show the existing stamp
"""
import os, re, sys, shutil, zipfile

KEY = 'plain_register'


def stamp_md(p, date, read=False):
    t = open(p, errors='ignore').read()
    if read:
        m = re.search(rf'^{KEY}:\s*(\S+)', t, re.M)
        return m.group(1) if m else None
    line = f'{KEY}: {date}'
    if t.startswith('---'):
        a, fm, body = t.split('---', 2)
        fm = re.sub(rf'^{KEY}:.*$', line, fm, flags=re.M) \
            if re.search(rf'^{KEY}:', fm, re.M) else fm.rstrip() + '\n' + line + '\n'
        t = '---' + fm + '---' + body
    else:
        t = f'---\n{line}\n---\n\n' + t
    open(p, 'w').write(t)
    return date


def stamp_ooxml(p, date, read=False):
    """Write into docProps/core.xml <cp:category>. Invisible to readers."""
    tag = f'plain-register:{date}'
    with zipfile.ZipFile(p) as z:
        names = z.namelist()
        core = z.read('docProps/core.xml').decode('utf8') if 'docProps/core.xml' in names else None
    if core is None:
        return None
    if read:
        m = re.search(r'plain-register:([^<\s]+)', core)
        return m.group(1) if m else None
    # The element may already exist, and may be self-closing. Replace either
    # form, otherwise a duplicate is written and readers see the empty one.
    existing = r'<cp:category\s*/>|<cp:category>.*?</cp:category>'
    if re.search(existing, core, re.S):
        core = re.sub(existing, f'<cp:category>{tag}</cp:category>', core, count=1, flags=re.S)
    else:
        core = core.replace('</cp:coreProperties>',
                            f'<cp:category>{tag}</cp:category></cp:coreProperties>')
    tmp = p + '.stamping'
    with zipfile.ZipFile(p) as zin, zipfile.ZipFile(tmp, 'w', zipfile.ZIP_DEFLATED) as zout:
        for it in zin.infolist():
            data = zin.read(it.filename)
            if it.filename == 'docProps/core.xml':
                data = core.encode('utf8')
            zout.writestr(it, data)
    shutil.move(tmp, p)
    return date


UNSUPPORTED = object()   # distinct from None, which means "no stamp found"


def run(p, date, read=False):
    ext = os.path.splitext(p)[1].lower()
    if ext in ('.md', '.markdown', '.txt'):
        return stamp_md(p, date, read)
    if ext in ('.docx', '.pptx', '.xlsx'):
        return stamp_ooxml(p, date, read)
    return UNSUPPORTED


def main(argv):
    read = '--read' in argv
    date = None
    if '--date' in argv:
        date = argv[argv.index('--date') + 1]
    if not date:
        # Passed in rather than computed, so the caller controls the date.
        date = os.environ.get('STAMP_DATE', '')
    paths = [a for a in argv if not a.startswith('--') and a != date]
    if not paths or (not read and not date):
        print(__doc__)
        return 1
    for p in paths:
        if not os.path.exists(p):
            print(f'{p}: not found')
            continue
        if not read and os.path.exists(os.path.join(os.path.dirname(p) or '.',
                                                    '~$' + os.path.basename(p))):
            print(f'{p}: OPEN IN OFFICE (~$ lock present), not stamped')
            continue
        got = run(p, date, read)
        if got is UNSUPPORTED:
            print(f'{p}: unsupported type, not stamped')
        elif read:
            print(f'{p}: {got or "NO STAMP"}')
        elif got is None:
            print(f'{p}: could not stamp (no docProps/core.xml)')
        else:
            print(f'{p}: stamped {got}')
    return 0


if __name__ == '__main__':
    sys.exit(main(sys.argv[1:]))
