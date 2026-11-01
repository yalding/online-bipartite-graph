"""Download pinned arXiv papers and extract page-delimited text."""
from pathlib import Path
import hashlib
import json
import gzip
import tarfile
import requests
from pypdf import PdfReader

ROOT = Path(__file__).resolve().parents[1]
PAPERS = [
    ('1305.1694v1', 'wang-wong-2013'),
    ('2602.18049v1', 'tang-2026-matching'),
    ('2608.09210v1', 'lu-2026-vertex-cover'),
    ('1904.08255v1', 'gamlath-et-al-2019'),
    ('2202.02948v2', 'tang-zhang-2024'),
    ('2608.04994v1', 'tang-zhang-2026-edge-cover'),
    ('2607.14656v2', 'assadi-jiang-xiang-2026-blueprints'),
    ('2608.24630v1', 'baligacs-et-al-2026-trees'),
]
PROCEEDINGS = [
    ('10.4230/LIPIcs.ESA.2017.22', 'buchbinder-segev-tkach-2017',
     'https://drops.dagstuhl.de/storage/00lipics/lipics-vol087-esa2017/'
     'LIPIcs.ESA.2017.22/LIPIcs.ESA.2017.22.pdf'),
]

def main():
    manifest = []
    for aid, name in PAPERS:
        base = ROOT / 'papers' / name
        for suffix, endpoint in [('.pdf', 'pdf'), ('.source', 'src')]:
            target = base.with_suffix(suffix)
            url = f'https://arxiv.org/{endpoint}/{aid}'
            if not target.exists():
                response = requests.get(url, timeout=60)
                response.raise_for_status()
                if suffix == '.pdf' and not response.content.startswith(b'%PDF'):
                    raise ValueError(f'Not PDF: {aid}')
                target.write_bytes(response.content)
            digest = hashlib.sha256(target.read_bytes()).hexdigest()
            manifest.append(dict(arxiv=aid, url=url, file=str(target.relative_to(ROOT)),
                                 bytes=target.stat().st_size, sha256=digest))
            print(target.name, target.stat().st_size, flush=True)
        reader = PdfReader(base.with_suffix('.pdf'))
        extracted = '\n\n'.join(
            f'===== PDF PAGE {i+1} =====\n' + (p.extract_text(extraction_mode='layout') or '')
            for i, p in enumerate(reader.pages))
        base.with_suffix('.txt').write_text(extracted, encoding='utf-8')
        print('extracted', len(reader.pages), 'pages', flush=True)
        archive = base.with_suffix('.source')
        source_dir = base.parent / (base.stem + '-source')
        source_dir.mkdir(exist_ok=True)
        if tarfile.is_tarfile(archive):
            with tarfile.open(archive) as bundle:
                for member in bundle.getmembers():
                    relative = Path(member.name)
                    if relative.is_absolute() or '..' in relative.parts:
                        raise ValueError(f'Unsafe source path: {member.name}')
                    if member.isfile() and relative.suffix in ('.tex', '.bib', '.bbl', '.sty'):
                        target = source_dir / relative
                        target.parent.mkdir(parents=True, exist_ok=True)
                        target.write_bytes(bundle.extractfile(member).read())
        else:
            (source_dir/'main.tex').write_bytes(gzip.decompress(archive.read_bytes()))
    for doi, name, url in PROCEEDINGS:
        target = ROOT / 'papers' / (name + '.pdf')
        if not target.exists():
            response = requests.get(url, timeout=60)
            response.raise_for_status()
            if not response.content.startswith(b'%PDF'):
                raise ValueError(f'Not PDF: {doi}')
            target.write_bytes(response.content)
        data = target.read_bytes()
        manifest.append(dict(doi=doi, url=url, file=str(target.relative_to(ROOT)),
                             bytes=len(data), sha256=hashlib.sha256(data).hexdigest()))
        reader = PdfReader(target)
        extracted = '\n\n'.join(
            f'===== PDF PAGE {i+1} =====\n' + (p.extract_text(extraction_mode='layout') or '')
            for i, p in enumerate(reader.pages))
        target.with_suffix('.txt').write_text(extracted, encoding='utf-8')
        print(target.name, len(data), flush=True)
    (ROOT / 'papers' / 'manifest.json').write_text(json.dumps(manifest, indent=2), encoding='utf-8')

if __name__ == '__main__':
    main()
